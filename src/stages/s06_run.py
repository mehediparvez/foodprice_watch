"""S06 step 3: test run. Unit = (variant, refit block). Refuses to run unless prereg is committed (seal)."""
import sys, json, hashlib, time
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, yaml
from fpw.ml import load, fit, features, GROUPS, placebo_assign
from fpw.checkpoint import run_unit, unseal_test
from fpw.io import ROOT, CFG
from fpw import state
import os; os.chdir(ROOT)
print("seal:", unseal_test("S06", ROOT / "state/prereg_S06.yaml", seal_dir=ROOT / "state/seals"))
pre = yaml.safe_load((ROOT / "state/prereg_S06.yaml").read_text())
F0 = load(); cuts = list(range(pre["test_cutoffs"]["first"], 1411, 7)); k = pre["refit_every_n_cutoffs"]
blocks = [cuts[i:i+k] for i in range(0, len(cuts), k)]
variants = [("core", [] , None), ("M1_all", list(GROUPS), None)] + [(g, [g], None) for g in GROUPS] + [(f"placebo_{g}", [g], i) for i, g in enumerate(GROUPS)]
prm = dict(num_leaves=pre["model"]["num_leaves"]); ne = pre["model"]["n_estimators"]
OUTD = ROOT / "outputs/06_lgbm"; OUTD.mkdir(parents=True, exist_ok=True)
cfgh = hashlib.sha256((ROOT / "state/prereg_S06.yaml").read_bytes()).hexdigest()[:12]
n = 0
for vname, groups, pidx in variants:
    F = F0 if pidx is None else placebo_assign(F0, groups[0], CFG["seed"] + pidx)[0]
    cols = features(groups)
    for b in blocks:
        out = OUTD / f"{vname}__cut_{b[0]:04d}.parquet"
        def compute(b=b, F=F, cols=cols):
            parts = []
            for h in pre["horizons_report_days"]:
                m = fit(F, b[0], h, cols, params=prm, n_estimators=ne)
                X = F[F.report_idx.isin(b)]
                parts.append(pd.DataFrame({"item_id": X.item_id.values, "cutoff": X.report_idx.values, "step": h, "lp": X.lp.values, "pred": m.predict(X[cols])}))
            return pd.concat(parts)
        t = time.time(); r = run_unit(out, compute, inputs={"variant": vname, "block": b[0]}, config_hash=cfgh, seed=CFG["seed"]); n += 1
        state.update("S06", last_unit=f"{vname}:{b[0]}", units_done=n); print(n, vname, b[0], r, round(time.time() - t, 1), flush=True)
print("ALL UNITS DONE")
