"""S07 step C: unseal and score. Writes T6, T7, T8, F5, F6, F7, alert log."""
import sys, yaml, json, os
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fpw.alerts import preds, bounds, persist, events, windows, fa_per_item_year, episodes, kupiec, in_any_window
from fpw.checkpoint import unseal_test
from fpw.io import ROOT, CFG, panel
os.chdir(ROOT); print("seal:", unseal_test("S07", ROOT / "state/prereg_S07.yaml", seal_dir=ROOT / "state/seals"))
pre = yaml.safe_load((ROOT / "state/prereg_S07.yaml").read_text()); lv = pre["primary_rule"]["level"]; q = f"q{int(lv*1000)}"
P = bounds(preds()); EV = events(); W = windows(EV)
P["A_conf"] = persist(P.resid > P[q], P.item_id) & P[q].notna()
P["A_z2"] = persist(P.z >= 2, P.item_id) & P.z.notna(); P["A_z1"] = persist(P.z >= 1, P.item_id) & P.z.notna(); P["A_z3"] = persist(P.z >= 3, P.item_id) & P.z.notna()
# ALPS-style daily, real-time monthly refit
pp = panel()[["item_id", "Date", "report_idx", "log_price"]].dropna().sort_values(["item_id", "Date"])
alps = []
for it, g in pp.groupby("item_id"):
    g = g.copy(); g["t"] = (g.Date - g.Date.min()).dt.days / 365.25; M = pd.get_dummies(g.Date.dt.month, prefix="m", drop_first=True).astype(float)
    X = np.column_stack([np.ones(len(g)), g.t.values, M.values]); z = np.full(len(g), np.nan)
    months = g.Date.dt.to_period("M")
    for mo in months.unique():
        if mo < pd.Period(CFG["alert_eval_start"], "M"): continue
        tr = (g.Date < mo.to_timestamp()).values
        if tr.sum() < 250: continue
        b, *_ = np.linalg.lstsq(X[tr], g.log_price.values[tr], rcond=None); res_tr = g.log_price.values[tr] - X[tr] @ b; sd = res_tr.std()
        cur = (months == mo).values; z[cur] = (g.log_price.values[cur] - X[cur] @ b) / sd
    g["z_alps"] = z; alps.append(g[["item_id", "Date", "z_alps"]])
P = P.merge(pd.concat(alps), on=["item_id", "Date"], how="left")
P["A_alps1"] = persist(P.z_alps >= 1, P.item_id) & P.z_alps.notna(); P["A_alps2"] = persist(P.z_alps >= 2, P.item_id) & P.z_alps.notna()
# IFPA-style monthly
mm = pp.assign(m=pp.Date.dt.to_period("M")).groupby(["item_id", "m"]).log_price.mean().reset_index()
def ifpa(g):
    g = g.sort_values("m").copy(); g["cq"] = (g.log_price - g.log_price.shift(3)) / 3; g["ca"] = (g.log_price - g.log_price.shift(12)) / 12
    for c in ["cq", "ca"]:
        mu = g[c].expanding(12).mean().shift(1); sd = g[c].expanding(12).std().shift(1); g["z" + c] = (g[c] - mu) / sd
    g["ifpa"] = 0.4 * g.zcq + 0.6 * g.zca; return g
I = mm.groupby("item_id", group_keys=False).apply(ifpa)
I["flag_from"] = I.m.dt.to_timestamp(how="end").dt.normalize() + pd.Timedelta(days=1)          # known after month end
P["mo_known"] = (P.Date.dt.to_period("M") - 1)
P = P.merge(I[["item_id", "m", "ifpa"]].rename(columns={"m": "mo_known"}), on=["item_id", "mo_known"], how="left")
P["A_ifpa"] = (P.ifpa >= 1).fillna(False); P["A_ifpa05"] = (P.ifpa >= 0.5).fillna(False)
P.to_parquet(ROOT / "outputs/07_alerts/alert_log.parquet", index=False)
RULES = {"A_conf": f"conformal {lv} upper, 3/5", "A_z2": "robust z>=2, 3/5", "A_z1": "robust z>=1, 3/5", "A_z3": "robust z>=3, 3/5",
         "A_alps1": "ALPS-style z>=1, 3/5", "A_alps2": "ALPS-style z>=2, 3/5", "A_ifpa": "IFPA-style >=1", "A_ifpa05": "IFPA-style >=0.5"}
# ---- T7 event scorecard
d = panel().drop_duplicates("Date").set_index("Date").report_idx
rows = []
for r in W.itertuples():
    sub = P[(P.item_id == r.item_id) & P.Date.between(r.w0, r.w1)]
    rec = dict(event_id=r.event_id, item_id=r.item_id, confidence=r.confidence, onset=r.onset.date(), news_peak=r.news_peak.date(),
               period="clean_test" if r.onset >= pd.Timestamp("2025-01-01") else "in_sample_for_threshold", n_obs_in_window=len(sub))
    for col, nm in RULES.items():
        ep = episodes(P[P.item_id == r.item_id], col); ep = ep[ep.Date.between(r.w0, r.w1)]
        if len(ep):
            f = ep.Date.min(); rec[f"{col}_detected"] = True; rec[f"{col}_first"] = f.date(); rec[f"{col}_lead_days"] = (r.news_peak - f).days
            pk = d.get(r.news_peak, d[d.index <= r.news_peak].iloc[-1] if (d.index <= r.news_peak).any() else np.nan); rec[f"{col}_lead_reports"] = int(pk - d[f]) if pd.notna(pk) else np.nan
        else:
            rec[f"{col}_detected"] = False
    rows.append(rec)
T7 = pd.DataFrame(rows); T7.to_csv(ROOT / "reports/tables/T7.csv", index=False)
ev_level = T7.groupby("event_id").agg(**{f"{c}": (f"{c}_detected", "max") for c in RULES}, period=("period", "first"), confidence=("confidence", "first"))
ev_level.to_csv(ROOT / "reports/tables/T7_event_level.csv")
# ---- T8 false alarms per item-year by stratum and rule (eval period 2023-06..2026-10)
per = (pd.Timestamp(CFG["alert_eval_start"]), pd.Timestamp("2026-10-24")); rows = []
for col, nm in RULES.items():
    fa, fai, yrs = fa_per_item_year(P, col, W, per)
    st = P.drop_duplicates("item_id").set_index("item_id").eval_stratum
    for s in sorted(st.unique()) + ["ALL"]:
        its = yrs.index if s == "ALL" else [i for i in yrs.index if st.get(i) == s]
        rows.append(dict(rule=nm, eval_stratum=s, fa_per_item_year=float(fai.reindex(its).sum() / yrs.reindex(its).sum()),
                         recall_events=float(ev_level[col].mean()), recall_clean_test=float(ev_level[ev_level.period == "clean_test"][col].mean())))
T8 = pd.DataFrame(rows); T8.to_csv(ROOT / "reports/tables/T8.csv", index=False)
# ---- T6 calibration
P["inwin"] = in_any_window(P, W); cal = []
for s, g in list(P[P.q950.notna()].groupby("eval_stratum")) + [("ALL", P[P.q950.notna()])]:
    r = g.resid; u = g.q950; l = g.q050; a = 0.1
    pin = lambda qq, tau: np.mean(np.maximum(tau * (r - qq), (tau - 1) * (r - qq)))
    wink = np.mean((u - l) + (2 / a) * (l - r) * (r < l) + (2 / a) * (r - u) * (r > u))
    ne = g[~g.inwin]; exc = int((ne.resid > ne.q950).sum())
    cal.append(dict(eval_stratum=s, n=len(g), cover_upper95=float((r <= u).mean()), cover_90=float(((r >= l) & (r <= u)).mean()), pinball_90=pin(g.q900, 0.9), pinball_95=pin(u, 0.95),
                    winkler_90=float(wink), kupiec_p_nonevent=kupiec(exc, len(ne), 0.05), exceed_rate_nonevent=exc / max(len(ne), 1)))
T6 = pd.DataFrame(cal); T6.to_csv(ROOT / "reports/tables/T6.csv", index=False)
# ---- F5 coverage by level
lvls = [0.9, 0.95, 0.975, 0.99]; cov = [(P[f"q{int(x*1000)}"].notna() & (P.resid <= P[f"q{int(x*1000)}"])).sum() / P[f"q{int(x*1000)}"].notna().sum() for x in lvls]
fig, ax = plt.subplots(figsize=(4.5, 4)); ax.plot(lvls, cov, "o-", label="observed"); ax.plot(lvls, lvls, "--", c="0.5", label="nominal")
ax.set_xlabel("nominal upper-bound level"); ax.set_ylabel("share of residuals below bound"); ax.set_title("F5. Upper-bound calibration"); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(ROOT / "reports/figures/F5_calibration.png", dpi=150)
# ---- F6 timelines per event-item
Wu = W.drop_duplicates(["event_id", "item_id"]); n = len(Wu); fig, axes = plt.subplots(int(np.ceil(n / 2)), 2, figsize=(12, 2.2 * np.ceil(n / 2)))
for ax, r in zip(axes.flat, Wu.itertuples()):
    g = P[(P.item_id == r.item_id) & P.Date.between(r.w0 - pd.Timedelta(days=120), r.w1 + pd.Timedelta(days=60))]
    ax.plot(g.Date, np.exp(g.lp_target), lw=1, c="k"); ax.plot(g.Date, np.exp(g.expected + g[q]), lw=.8, c="tab:blue", alpha=.7)
    ax.scatter(g.Date[g.A_conf], np.exp(g.lp_target[g.A_conf]), s=6, c="tab:red", zorder=3); ax.axvspan(r.w0, r.w1, color="0.9"); ax.axvline(r.news_peak, c="tab:orange", lw=1)
    ax.set_title(f"{r.event_id} {r.item_id.split(' |')[0]}", fontsize=8); ax.tick_params(labelsize=6)
for ax in list(axes.flat)[n:]: ax.axis("off")
fig.suptitle("F6. Price (black), real-time upper bound (blue), alerts (red), event window (grey), news peak (orange)", fontsize=9); fig.tight_layout(); fig.savefig(ROOT / "reports/figures/F6_alert_timelines.png", dpi=130)
# ---- F7 precision-recall over thresholds (items with labels)
lab_items = set(W.item_id); Pl = P[P.item_id.isin(lab_items) & P.Date.between(*per)].copy(); pts = []
for kind, vals in [("conformal", lvls), ("z", [1, 1.5, 2, 2.5, 3, 4])]:
    for v in vals:
        Pl["x"] = (persist(Pl.resid > Pl[f"q{int(v*1000)}"], Pl.item_id) & Pl[f"q{int(v*1000)}"].notna()) if kind == "conformal" else (persist(Pl.z >= v, Pl.item_id) & Pl.z.notna())
        ep = episodes(Pl, "x").merge(Pl[["item_id", "Date", "inwin"]], on=["item_id", "Date"]); prec = ep.inwin.mean() if len(ep) else np.nan
        det = [bool(len(episodes(Pl[Pl.item_id == r.item_id], "x").query("@r.w0 <= Date <= @r.w1"))) for r in W.itertuples()]
        recall = pd.Series(det, index=W.event_id).groupby(level=0).max().mean(); pts.append(dict(kind=kind, value=v, precision=prec, recall=recall, n_episodes=len(ep)))
PR = pd.DataFrame(pts); PR.to_csv(ROOT / "reports/tables/T8b_precision_recall.csv", index=False)
fig, ax = plt.subplots(figsize=(5, 4))
for k, g in PR.groupby("kind"): ax.plot(g.recall, g.precision, "o-", label=k)
op = PR[(PR.kind == "conformal") & (PR.value == lv)]; ax.scatter(op.recall, op.precision, s=120, facecolors="none", edgecolors="r", label="pre-registered point")
ax.set_xlabel("event recall"); ax.set_ylabel("precision (alerts inside labelled windows)"); ax.set_title("F7. Precision-recall"); ax.legend(frameon=False, fontsize=8); fig.tight_layout(); fig.savefig(ROOT / "reports/figures/F7_precision_recall.png", dpi=150)
print(ev_level.to_string()); print(T8[T8.eval_stratum == "ALL"].to_string()); print(T6.round(3).to_string())
