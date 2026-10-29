"""S09 step B: explanation ladder per episode (T9), event studies (T10), sign checks (T9b), F8, F9."""
import sys, glob, yaml
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fpw.io import ROOT, CFG, panel, item_meta
from fpw.alerts import events, item_of_product
from fpw import drivers as D
Pr = pd.concat([pd.read_parquet(f) for f in glob.glob(str(ROOT / "outputs/09_explain/*.parquet"))])
key = Pr.pivot_table(index=["item_id", "origin", "h"], columns="model", values="pred")
shap = Pr[Pr.model == "M2"].set_index(["item_id", "origin", "h"])
pn = panel(); dmap = pn.drop_duplicates("report_idx").set_index("report_idx").Date; rmap = pd.Series(dmap.index, index=dmap.values)
lpf = pn.sort_values(["item_id", "report_idx"]).assign(lp=lambda x: x.groupby("item_id").log_price.ffill()).set_index(["item_id", "report_idx"]).lp
def ridx(date, side="le"):
    s = rmap[rmap.index <= date] if side == "le" else rmap[rmap.index >= date]
    return int(s.iloc[-1] if side == "le" else s.iloc[0]) if len(s) else None
def chunks(i0, i1):
    out, o = [], i0
    while o < i1:
        rem = i1 - o; h = 30 if rem >= 30 else (14 if rem >= 14 else (7 if rem >= 7 else None))
        if h is None: break
        out.append((o, h)); o += h
    return out
def decompose(item, i0, i1):
    rec = dict(r=0.0, m0=0.0, m1=0.0, m2=0.0, n=0, covered_to=i0); sg = {}
    for o, h in chunks(i0, i1):
        if (item, o, h) not in key.index or (item, o + h) not in lpf.index or (item, o) not in lpf.index: continue
        k = key.loc[(item, o, h)]; r = lpf[(item, o + h)] - lpf[(item, o)]
        if k.isna().any() or pd.isna(r): continue
        rec["r"] += r; rec["m0"] += k.M0; rec["m1"] += k.M1; rec["m2"] += k.M2; rec["n"] += 1; rec["covered_to"] = o + h
        s = shap.loc[(item, o, h)]
        for c in [c for c in s.index if c.startswith("shap_") and c != "shap_base"]: sg[c] = sg.get(c, 0) + s[c]
    return rec, sg
# ---------- T9 episodes
EV = events(); rows, srows = [], []
for e in EV.itertuples():
    for it in item_of_product(e.product):
        if it not in key.index.get_level_values(0): continue
        i0 = ridx(e.onset, "le"); i1 = ridx(max(e.news_peak, e.onset), "le")
        if i0 is None or i1 is None or i1 - i0 < 7: continue
        rec, sg = decompose(it, i0, i1)
        if rec["n"] == 0: continue
        R = rec["r"]; row = dict(event_id=e.event_id, item_id=it, confidence=e.confidence, rise_start=dmap[i0].date(), rise_end=dmap[rec["covered_to"]].date(), report_days=rec["covered_to"] - i0,
            realized_log_change=R, realized_pct=np.expm1(R) * 100, M0_persistence_calendar=rec["m0"], M1_minus_M0_forecast_drivers=rec["m1"] - rec["m0"], M2_minus_M1_explain_drivers=rec["m2"] - rec["m1"],
            not_explained_by_measured_cost_drivers=R - rec["m2"], n_chunks=rec["n"])
        if R > 0:
            row.update(share_M0=rec["m0"] / R, share_forecast_drivers=(rec["m1"] - rec["m0"]) / R, share_explain_drivers=(rec["m2"] - rec["m1"]) / R, share_not_explained=(R - rec["m2"]) / R)
            row["label"] = ("mostly not explained by measured cost drivers" if row["share_not_explained"] > 0.5 else "mostly explained by persistence, calendar and measured cost drivers")
        else: row["label"] = "no rise over the window (realized change <= 0)"
        rows.append(row); srows.append(dict(event_id=e.event_id, item_id=it, **{k.replace("shap_", "shap_sum_"): v for k, v in sg.items()}))
T9 = pd.DataFrame(rows); T9.to_csv(ROOT / "reports/tables/T9.csv", index=False); pd.DataFrame(srows).to_csv(ROOT / "reports/tables/T9_shap_by_episode.csv", index=False)
print(T9[["event_id", "item_id", "realized_pct", "share_M0", "share_forecast_drivers", "share_explain_drivers", "share_not_explained", "label"]].round(2).to_string())
# ---------- T9b sign checks
S = Pr[Pr.model == "M2"]; sg = []
for c, items_desc in [("e1_fx_ch30", "E1 strata (imported, administered, spice)"), ("own_world_price_ch3", "G1 items"), ("e5_world_explain", "sugar, chickpea")]:
    x = S[[f"x_{c}", f"s_{c}", "h"]].dropna()
    for h, g in x.groupby("h"):
        rho = g[[f"x_{c}", f"s_{c}"]].corr(method="spearman").iloc[0, 1] if g[f"x_{c}"].nunique() > 2 else np.nan
        sg.append(dict(feature=c, items=items_desc, h=h, n=len(g), spearman_value_vs_shap=rho, expected_sign="+", sign_ok=bool(rho > 0) if pd.notna(rho) else None))
T9b = pd.DataFrame(sg); T9b.to_csv(ROOT / "reports/tables/T9b_sign_checks.csv", index=False); print(T9b.round(3).to_string())
# ---------- T10 event studies (abnormal change = realized - M0 predicted, vs placebo origins)
rng = np.random.default_rng(CFG["seed"]); W = []
from fpw.alerts import windows
EVW = windows(EV)
def ar(item, o, h):
    if (item, o, h) not in key.index or (item, o + h) not in lpf.index: return np.nan
    return (lpf[(item, o + h)] - lpf[(item, o)]) - key.loc[(item, o, h)].M0
def placebo(items, h, excl_dates, n=200):
    origins = sorted(key.index.get_level_values(1).unique()); vals = []
    for _ in range(n * 3):
        it = items[rng.integers(len(items))]; o = int(origins[rng.integers(len(origins))]); dt = dmap.get(o)
        if dt is None or any(abs((dt - x).days) < 60 for x in excl_dates): continue
        bad = EVW[(EVW.item_id == it) & (EVW.w0 - pd.Timedelta(days=30) <= dt) & (EVW.w1 >= dt)]
        if len(bad): continue
        v = ar(it, o, h)
        if pd.notna(v): vals.append(v)
        if len(vals) >= n: break
    return np.array(vals)
studies = []
on_items = ["Onion - Local | per kg", "Onion - Imported | per kg"]; ban = pd.Timestamp("2023-12-08")
studies.append(("India onion export ban (verified 2023-12-08)", on_items, ban, "verified"))
fx = D.fx().set_index("date").bdt_per_usd; ch = (fx / fx.shift(30, freq="D").reindex(fx.index) - 1)
jump = fx.pct_change(); big = jump["2024":"2025"]; jd = big.idxmax()
imp = list(item_meta().query("eval_stratum in ['imported_staple','administered'] and not short_history").item_id)
studies.append((f"BDT/USD jump {jd.date()} (+{big.max()*100:.1f}% in one day; largest 2024-25 move)", imp, jd, "data"))
for name, items, dt, conf in studies:
    o = ridx(dt - pd.Timedelta(days=1), "le")
    for h in [7, 14, 30]:
        obs = [ar(it, o, h) for it in items]; obs = [v for v in obs if pd.notna(v)]
        if not obs: continue
        m = float(np.mean(obs)); pl = placebo(items, h, [dt]); pm = np.array([rng.choice(pl, len(obs)).mean() for _ in range(2000)])
        W.append(dict(event=name, date_confidence=conf, origin=dmap[o].date(), h=h, n_items=len(obs), mean_abnormal_log_change=m, mean_abnormal_pct=np.expm1(m) * 100,
                      placebo_mean=float(pl.mean()), p_one_sided=float((pm >= m).mean()), n_placebo=len(pl)))
W.append(dict(event="Sep 2023 price caps", date_confidence="not studied: no dated, sourced cap event in the project files (DECISIONS D10)"))
T10 = pd.DataFrame(W); T10.to_csv(ROOT / "reports/tables/T10.csv", index=False); print(T10.round(4).to_string())
# ---------- F8 stacked decomposition for case studies
cases = [("BD-S13", "Onion - Local | per kg"), ("BD-S21", "Soybean Oil - Loose | per litre"), ("BD-S17", "Potato | per kg"), ("BD-S15", "Rice - Coarse (Swarna/China IRRI) | per kg")]
C = T9.set_index(["event_id", "item_id"]); fig, ax = plt.subplots(figsize=(8, 4)); xs = []
comp = [("M0_persistence_calendar", "persistence + calendar", "0.6"), ("M1_minus_M0_forecast_drivers", "forecasting drivers (G1-G5)", "tab:blue"),
        ("M2_minus_M1_explain_drivers", "explanation drivers (FX, fuel, imports, events)", "tab:green"), ("not_explained_by_measured_cost_drivers", "not explained by measured cost drivers", "tab:orange")]
lab = []
for i, ck in enumerate(cases):
    if ck not in C.index: continue
    r = C.loc[ck]; pos = neg = 0
    for col, nm, colr in comp:
        v = r[col] * 100
        ax.bar(i, v, bottom=pos if v >= 0 else neg, color=colr, label=nm if i == 0 else None)
        if v >= 0: pos += v
        else: neg += v
    ax.plot([i - .4, i + .4], [r.realized_log_change * 100] * 2, c="k", lw=2); lab.append(f"{ck[0]}\n{ck[1].split(' |')[0]}")
ax.set_xticks(range(len(lab))); ax.set_xticklabels(lab, fontsize=8); ax.axhline(0, c="k", lw=.6); ax.set_ylabel("contribution to log change (x100)")
ax.set_title("F8. Explained vs not explained by measured cost drivers (black line = realized change)", fontsize=9); ax.legend(fontsize=7, frameon=False); fig.tight_layout(); fig.savefig(ROOT / "reports/figures/F8_decomposition.png", dpi=150)
# ---------- F9 global SHAP importance by stratum (M2, h=30, origins in test period)
S30 = S[(S.h == 30) & (S.origin >= 809)].merge(item_meta()[["item_id", "eval_stratum"]], on="item_id")
gcols = [c for c in S30.columns if c.startswith("shap_") and c != "shap_base"]
imp = S30.groupby("eval_stratum")[gcols].apply(lambda g: g.abs().mean()); imp.columns = [c.replace("shap_", "") for c in imp.columns]
imp.to_csv(ROOT / "reports/tables/T9c_shap_importance.csv")
fig, ax = plt.subplots(figsize=(8, 3.8)); imp.plot.bar(ax=ax, width=.8); ax.set_ylabel("mean |SHAP| (log change)"); ax.set_title("F9. Feature-group importance in M2 (h=30, 2025-26 origins)", fontsize=9)
ax.legend(fontsize=7, ncol=3, frameon=False); plt.xticks(rotation=20, fontsize=7); fig.tight_layout(); fig.savefig(ROOT / "reports/figures/F9_shap_importance.png", dpi=150)
