"""S09 step A: real-time M0/M1/M2 predictions (+ M2 TreeSHAP group sums) on a refit grid. Unit = (model, h, refit)."""
import sys, time
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, yaml
from fpw.ml import load, fit, features, GROUPS, EXPLAIN, CAL, OWN
from fpw.checkpoint import run_unit
from fpw.io import ROOT, CFG, panel
from fpw import state
state.start("S09")
pre = yaml.safe_load((ROOT / "state/prereg_S06.yaml").read_text()); prm = dict(num_leaves=pre["model"]["num_leaves"]); ne = pre["model"]["n_estimators"]
F = load(); d = panel().drop_duplicates("report_idx").set_index("report_idx").Date
start = int(d[d >= "2023-04-01"].index.min()); STEP = 60
refits = list(range(start, 1411, STEP))
MODELS = {"M0": features([]), "M1": features(list(GROUPS)), "M2": features(list(GROUPS)) + EXPLAIN}
def grp_of(c):
    for g, cs in GROUPS.items():
        if c in cs: return g
    if c in EXPLAIN: return {"e1": "E1_fx", "e2": "E2_fuel", "e3": "E3_imports", "e4": "E4_events", "e5": "E5_world"}[c[:2]]
    return "own_calendar"
OUTD = ROOT / "outputs/09_explain"; OUTD.mkdir(parents=True, exist_ok=True); n = 0
for h in [30, 14, 7]:
    for mname, cols in MODELS.items():
        for rc in refits:
            out = OUTD / f"{mname}_h{h}_refit_{rc:04d}.parquet"
            def compute(rc=rc, cols=cols, mname=mname, h=h):
                m = fit(F, rc, h, cols, params=prm, n_estimators=ne); X = F[(F.report_idx >= rc) & (F.report_idx < rc + STEP)]
                D = pd.DataFrame({"item_id": X.item_id.values, "origin": X.report_idx.values, "h": h, "model": mname, "lp": X.lp.values, "pred": m.predict(X[cols]), "y_true": X[f"y{h}"].values, "refit": rc})
                if mname == "M2":
                    sv = m.predict(X[cols], pred_contrib=True); base = sv[:, -1]; D["shap_base"] = base
                    for g in sorted(set(grp_of(c) for c in cols)):
                        idx = [i for i, c in enumerate(cols) if grp_of(c) == g]; D[f"shap_{g}"] = sv[:, idx].sum(1)
                    for c in ["e1_fx_ch30", "own_world_price_ch3", "e5_world_explain"]:
                        D[f"x_{c}"] = X[c].values; D[f"s_{c}"] = sv[:, cols.index(c)]
                return D
            t = time.time(); r = run_unit(out, compute, inputs={"model": mname, "h": h, "refit": rc}, config_hash="s09", seed=CFG["seed"]); n += 1
            state.update("S09", last_unit=f"{mname}_h{h}_{rc}", units_done=n); print(n, mname, h, rc, r, round(time.time() - t, 1), flush=True)
print("ALL UNITS DONE")
