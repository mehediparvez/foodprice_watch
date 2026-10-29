"""S01 Rebuild TCB panel (idempotent). Outputs parquet, corrections_proposed, T1, F1, F2."""
import sys, json
sys.path.insert(0, "src")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fpw.io import raw, item_meta, PROC, CFG, ROOT
from fpw.checkpoint import is_done, sha256
from fpw import state
OUT = PROC / "tcb_v1.0_rebuilt.parquet"
state.start("S01")
df = pd.read_csv(raw("tcb_dhaka_daily_prices_2021_2026.csv"), parse_dates=["Date"])   # rule 9: CSV once
df["item_id"] = df["Product"] + " | " + df["Unit"]                                       # rule 3
meta = item_meta()
assert set(df.item_id) == set(meta.item_id), "item_id mismatch with item_meta"
# corrections.csv reflected?
corr = pd.read_csv(raw("corrections.csv"), parse_dates=["Date"])
corr_status = []
for r in corr.itertuples():
    v = df.loc[(df.Date == r.Date) & (df.item_id == r.item_id), r.column]
    want = r.new_value
    applied = (v.isna().all() if pd.isna(want) else np.isclose(v.astype(float), float(want)).all())
    corr_status.append(dict(Date=r.Date.date(), item_id=r.item_id, column=r.column, applied=bool(applied)))
# calendar features
dates = pd.DataFrame({"Date": sorted(df.Date.unique())})
dates["report_idx"] = range(len(dates))
dates["days_since_prev_report"] = dates.Date.diff().dt.days
g0, g1 = pd.Timestamp(CFG["gap_2022"][0]), pd.Timestamp(CFG["gap_2022"][1])
dates["gap_2022"] = dates.Date.between(g0, g1)
df = df.merge(dates, on="Date", how="left").sort_values(["item_id","Date"]).reset_index(drop=True)
df["is_reported"] = df.Price_Avg.notna()
df["spread_rel"] = (df.Price_Max - df.Price_Min) / df.Price_Avg
# reports_since_change
def rsc(s):
    out, c, last = [], 0, np.nan
    for v in s:
        if pd.isna(v): out.append(np.nan); continue
        c = 0 if (pd.isna(last) or v != last) else c + 1
        out.append(c); last = v
    return out
df["reports_since_change"] = df.groupby("item_id")["Price_Avg"].transform(lambda s: pd.Series(rsc(s.values), index=s.index))
# flags (rules 4-6)
df["flag_min_only"] = df.Price_Min.notna() & df.Price_Max.isna()
cand = pd.read_csv(raw("audit_candidates.csv"))
print("audit_candidates cols:", list(cand.columns))
dcol = [c for c in cand.columns if "date" in c.lower()][0]
icol = [c for c in cand.columns if "item" in c.lower()][0]
ck = set(zip(pd.to_datetime(cand[dcol]), cand[icol]))
df["flag_audit_candidate"] = [ (d,i) in ck for d,i in zip(df.Date, df.item_id)]
df = df.merge(meta[["item_id","eval_stratum","stratum","short_history"]], on="item_id", how="left")
df["exclude_palm_olein"] = df.Product.str.startswith("Palm Olein")
# proposed correction (rule 4) — not applied
po = df[(df.item_id == "Palm Olein - Bottled | 2 litre") & (df.Date == "2025-04-18")]
prop = pd.DataFrame([dict(Date="2025-04-18", item_id="Palm Olein - Bottled | 2 litre", column=c, old_value=po[c].iloc[0], new_value="",
        reason="5-litre price (840-845) sits on the 2-litre row; 2 L is 345-350 on 2025-04-19..27; mirror of corrections.csv 5 L fix. PROPOSED — needs user approval")
        for c in ["Price_Min","Price_Max","Price_Avg"]])
prop.to_csv(PROC / "corrections_proposed.csv", index=False)
tmp = OUT.with_suffix(".parquet.tmp"); df.to_parquet(tmp, index=False); tmp.replace(OUT)
(PROC / "tcb_v1.0_rebuilt.sha256").write_text(sha256(OUT) + "  tcb_v1.0_rebuilt.parquet\n")
# checks summary
chk = {}
chk["rows"] = len(df); chk["dates"] = df.Date.nunique(); chk["date_min"] = str(df.Date.min().date()); chk["date_max"] = str(df.Date.max().date())
chk["items"] = df.item_id.nunique(); chk["dup_keys"] = int(df.duplicated(["Date","item_id"]).sum())
both = df.Price_Min.notna() & df.Price_Max.notna()
chk["avg_mid_violations"] = int((both & ~np.isclose(df.Price_Avg, (df.Price_Min+df.Price_Max)/2)).sum())
chk["min_gt_max"] = int((df.Price_Min > df.Price_Max).sum())
chk["min_only_rows"] = int(df.flag_min_only.sum())
chk["missing_share"] = round(df.Price_Avg.isna().mean(), 4)
# Week_Ago check: own Min 7 calendar days earlier
lag = df[["item_id","Date","Price_Min"]].copy(); lag["Date"] = lag.Date + pd.Timedelta(days=7)
m = df[["item_id","Date","Week_Ago_Min"]].merge(lag, on=["item_id","Date"]).dropna()
chk["week_ago_match_share"] = round(float(np.isclose(m.Week_Ago_Min, m.Price_Min).mean()), 4); chk["week_ago_n"] = len(m)
chk["corrections"] = corr_status
chk["gap_2022_reports"] = int(dates.gap_2022.sum())
(ROOT / "outputs/s01_checks.json").parent.mkdir(exist_ok=True)
(ROOT / "outputs/s01_checks.json").write_text(json.dumps(chk, indent=2, default=str))
print(json.dumps({k:v for k,v in chk.items() if k!="corrections"}), corr_status)
# T1
rows = []
for st, g in df.groupby("eval_stratum"):
    per = g.groupby("item_id")
    unchanged = per.apply(lambda x: (x.Price_Avg.dropna().diff().dropna()==0).mean())
    rows.append(dict(eval_stratum=st, n_series=g.item_id.nunique(), report_days=g.Date.nunique(),
        share_unchanged_median=round(unchanged.median(),3), share_missing=round(g.Price_Avg.isna().mean(),4),
        first_report=str(per.apply(lambda x: x.loc[x.Price_Avg.notna(),"Date"].min()).min().date())))
late = meta[(~meta.short_history) & (meta.first_date > "2021-06-01")][["item_id","first_date"]]
T1 = pd.DataFrame(rows); T1.to_csv(ROOT/"reports/tables/T1.csv", index=False)
late.to_csv(ROOT/"reports/tables/T1_late_starters.csv", index=False); print(T1.to_string()); print(late.to_string())
# F1 indexed staples
staples = {"Atta (Wheat Flour) - Loose | per kg":"Atta (loose)","Egg - Farm | per hali (4 pcs)":"Farm eggs","Lentil (Masur) - Large Grain | per kg":"Lentil, large",
    "Onion - Local | per kg":"Onion (local)","Potato | per kg":"Potato","Rice - Coarse (Swarna/China IRRI) | per kg":"Coarse rice",
    "Soybean Oil - Loose | per litre":"Soybean oil (loose)","Sugar | per kg":"Sugar"}
sub = df[df.item_id.isin(staples)].copy(); sub["m"] = sub.Date.dt.to_period("M").dt.to_timestamp()
mm = sub.groupby(["item_id","m"]).Price_Avg.mean().unstack(0)
idx = mm / mm.iloc[0] * 100
fig, ax = plt.subplots(figsize=(10,5))
for c in idx: ax.plot(idx.index, idx[c], label=staples[c], lw=1.4)
ax.axvspan(pd.Timestamp("2022-03-01"), pd.Timestamp("2022-12-31"), color="0.85", label="sparse 2022")
ax.axhline(100, color="0.5", lw=.6); ax.set_ylabel("Index, May 2021 = 100"); ax.set_title("F1. Monthly mean TCB mid-price, eight staples")
ax.legend(ncol=3, fontsize=8, frameon=False); fig.tight_layout(); fig.savefig(ROOT/"reports/figures/F1_indexed_staples.png", dpi=150)
# F2 reporting calendar
cal = pd.DataFrame({"Date": pd.date_range(df.Date.min(), df.Date.max())}); cal["rep"] = cal.Date.isin(dates.Date).astype(int)
cal["y"] = cal.Date.dt.year; cal["doy"] = cal.Date.dt.dayofyear
H = cal.pivot_table(index="y", columns="doy", values="rep")
fig, ax = plt.subplots(figsize=(11,3)); ax.imshow(H.values, aspect="auto", cmap="Greys", interpolation="nearest")
ax.set_yticks(range(len(H.index))); ax.set_yticklabels(H.index); ax.set_xlabel("Day of year"); ax.set_title("F2. TCB report days (black = report published)")
fig.tight_layout(); fig.savefig(ROOT/"reports/figures/F2_report_calendar.png", dpi=150)
