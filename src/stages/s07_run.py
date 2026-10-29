"""S07 step A: real-time h=7 expected prices for every item and report day from 2023-06 (M1 = core + mapped forecasting groups).
Unit = refit block (30 report days). No event data is used here."""
import sys, json, hashlib, time
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, yaml
from fpw.ml import load, fit, features, GROUPS
from fpw.checkpoint import run_unit
from fpw.io import ROOT, CFG, panel
from fpw import state
state.start("S07")
pre = yaml.safe_load((ROOT / "state/prereg_S06.yaml").read_text())
F = load(long_history_only=False); cols = features(list(GROUPS)); H7 = 7
d = panel().drop_duplicates("report_idx").set_index("report_idx").Date
start = int(d[d >= CFG["alert_eval_start"]].index.min()); last = int(d.index.max())
refits = list(range(start - H7, last, CFG["refit_every"]))
OUTD = ROOT / "outputs/07_alerts/pred"; OUTD.mkdir(parents=True, exist_ok=True)
for i, rc in enumerate(refits):
    out = OUTD / f"refit_{rc:04d}.parquet"
    def compute(rc=rc):
        m = fit(F, rc, H7, cols, params=dict(num_leaves=pre["model"]["num_leaves"]), n_estimators=pre["model"]["n_estimators"])
        X = F[(F.report_idx >= rc) & (F.report_idx < rc + CFG["refit_every"])]      # origins in block; info <= origin only
        return pd.DataFrame({"item_id": X.item_id.values, "origin": X.report_idx.values, "target": X.report_idx.values + H7, "lp_origin": X.lp.values, "pred": m.predict(X[cols]), "refit": rc})
    t = time.time(); r = run_unit(out, compute, inputs={"refit": rc}, config_hash="s07", seed=CFG["seed"])
    state.update("S07", last_unit=f"pred:{rc}", units_done=i + 1); print(i + 1, len(refits), rc, r, round(time.time() - t, 1), flush=True)
print("ALL UNITS DONE")
