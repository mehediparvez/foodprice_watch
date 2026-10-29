"""S10 Robustness (RQ5 parts omitted: S08 blocked). Writes T11."""
import sys, glob, yaml
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from fpw.io import ROOT, CFG, panel
from fpw.alerts import events, windows, episodes, persist
from fpw.ml import load, fit, features
from fpw.bench import wide
from fpw import state
state.start("S10")
rng = np.random.default_rng(CFG["seed"]); rows = []
A = pd.read_parquet(ROOT / "outputs/07_alerts/alert_log.parquet"); EV = events(); W = windows(EV)
pre7 = yaml.safe_load((ROOT / "state/prereg_S07.yaml").read_text())
def recall(Wsub, col="A_conf"):
    det = []
    for r in Wsub.itertuples():
        ep = episodes(A[A.item_id == r.item_id], col); det.append((r.event_id, bool(len(ep[ep.Date.between(r.w0, r.w1)]))))
    return pd.DataFrame(det, columns=["e", "d"]).groupby("e").d.max().mean() if det else np.nan
base = recall(W); rows.append(dict(check="baseline (pre-registered conformal rule)", value=base, note="share of 12 events detected"))
# 1 placebo event dates
span = (pd.Timestamp(CFG["alert_eval_start"]), pd.Timestamp("2026-09-01")); pl = []
for _ in range(200):
    Wp = W.copy(); L = (W.w1 - W.w0)
    for i, r in W.iterrows():
        for _t in range(50):
            s = span[0] + pd.Timedelta(days=int(rng.integers(0, (span[1] - span[0]).days)))
            if not ((W.item_id == r.item_id) & (W.w1 >= s) & (W.w0 <= s + L[i])).any(): break
        Wp.loc[i, "w0"] = s; Wp.loc[i, "w1"] = s + L[i]
    pl.append(recall(Wp))
rows.append(dict(check="placebo event dates (200 draws, same items and window lengths)", value=float(np.mean(pl)), note=f"95% range {np.percentile(pl,2.5):.2f}-{np.percentile(pl,97.5):.2f}; p(placebo >= observed) = {np.mean(np.array(pl) >= base):.3f}"))
# 2 leave-one-event-out
lo = [recall(W[W.event_id != e]) for e in W.event_id.unique()]
rows.append(dict(check="leave-one-event-out recall", value=float(np.mean(lo)), note=f"min {min(lo):.2f}, max {max(lo):.2f}"))
# 3 confidence subsets
for c in ["medium", "high"]:
    sub = W[W.confidence.isin(["medium", "high"] if c == "medium" else ["high"])]
    rows.append(dict(check=f"events with confidence >= {c}", value=recall(sub), note=f"{sub.event_id.nunique()} events"))
# 4 reconstructed-date events excluded (onion S12 depends on reconstructed India duty date; S13 verified)
rows.append(dict(check="exclude events tied to reconstructed exporter dates (BD-S12)", value=recall(W[W.event_id != "BD-S12"]), note="BD-S13 kept: ban date verified"))
# 5 rule/threshold sensitivity
for col, nm in [("A_z1", "z>=1"), ("A_z2", "z>=2"), ("A_z3", "z>=3")]:
    rows.append(dict(check=f"alternative rule robust {nm}", value=recall(W, col), note="3-of-5 persistence"))
# 6 sliding vs expanding + 7 ginger candidates excluded (LightGBM core, test blocks, h in 1/7/14/30)
pre = yaml.safe_load((ROOT / "state/prereg_S06.yaml").read_text()); prm = dict(num_leaves=pre["model"]["num_leaves"]); ne = pre["model"]["n_estimators"]
F = load(); cols = features([]); y = wide(); cuts = list(range(808, 1411, 7)); blocks = [cuts[i:i+8] for i in range(0, len(cuts), 8)]
p = panel(); cand = p[p.flag_audit_candidate][["item_id", "report_idx"]]
Fg = F.copy(); m = Fg.set_index(["item_id", "report_idx"]).index.isin(pd.MultiIndex.from_frame(cand))
for h in [1, 7, 14, 30]: Fg.loc[m, f"y{h}"] = np.nan
Fg = Fg[~m | True]
def run(Fx, window=None):
    out = []
    for b in blocks:
        for h in [1, 7, 14, 30]:
            Ft = Fx if window is None else Fx[Fx.report_idx > b[0] - window]
            mdl = fit(Ft, b[0], h, cols, params=prm, n_estimators=ne); X = Fx[Fx.report_idx.isin(b)]
            out.append(pd.DataFrame({"item_id": X.item_id, "cutoff": X.report_idx, "step": h, "fc": np.exp(X.lp + mdl.predict(X[cols])), "naive": np.round(np.exp(X.lp), 6)}))
    o = pd.concat(out); o["t"] = o.cutoff + o.step; yy = y.stack().rename("y").reset_index(); yy.columns = ["t", "item_id", "y"]; o = o.merge(yy, on=["t", "item_id"])
    r = o.groupby(["step", "item_id"]).apply(lambda g: (g.fc - g.y).abs().mean() / (g.naive - g.y).abs().mean() if (g.naive - g.y).abs().mean() > 0 else np.nan).dropna()
    return r.groupby(level=0).apply(lambda s: float(np.exp(np.log(s[s > 0]).mean())))
e0 = run(F); e1 = run(F, window=500); e2 = run(Fg)
for h in [1, 7, 14, 30]:
    rows.append(dict(check=f"LightGBM core expanding window, h={h}", value=e0[h], note="gmean relMAE vs naive (reference)"))
    rows.append(dict(check=f"LightGBM core sliding 500-report-day window, h={h}", value=e1[h], note="gmean relMAE vs naive"))
    rows.append(dict(check=f"LightGBM core, ginger 2021 candidates removed from targets, h={h}", value=e2[h], note="gmean relMAE vs naive"))
rows.append(dict(check="not run: weekly vs daily aggregation; Min/Max instead of Avg targets; RQ5 locate robustness", value=np.nan, note="logged in DEVIATIONS.md"))
T11 = pd.DataFrame(rows); T11.to_csv(ROOT / "reports/tables/T11.csv", index=False); print(T11.round(3).to_string())
