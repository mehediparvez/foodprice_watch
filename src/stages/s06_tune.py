"""S06 step 1: tune LightGBM core on 2024 validation cutoffs only (test period never touched)."""
import sys, json, itertools, time
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from fpw.ml import load, fit, features, H
from fpw.bench import tuning_cutoffs
from fpw.io import ROOT
from fpw import state
state.start("S06")
OUT = ROOT / "state/tuning_S06.json"
if OUT.exists(): print("tuning already done:", OUT.read_text()); sys.exit()
F = load(); cols = features([])
cuts = tuning_cutoffs(); refits = cuts[::8]
grid = [dict(num_leaves=nl, n_estimators=ne) for nl, ne in itertools.product([15, 31], [150, 300])]
res = []
for g in grid:
    errs = {h: [] for h in H}
    for i, rc in enumerate(refits):
        block = cuts[i*8:(i+1)*8]
        for h in H:
            m = fit(F, rc, h, cols, params=dict(num_leaves=g["num_leaves"]), n_estimators=g["n_estimators"])
            X = F[F.report_idx.isin(block) & F[f"y{h}"].notna()]
            pred = m.predict(X[cols]); errs[h].append(pd.DataFrame({"item_id": X.item_id, "e_m": np.abs(np.exp(X.lp + pred) - np.exp(X.lp + X[f"y{h}"])), "e_n": np.abs(1 - np.exp(X[f"y{h}"])) * np.exp(X.lp)}))
    score = {}
    for h in H:
        d = pd.concat(errs[h]).groupby("item_id")[["e_m", "e_n"]].mean(); r = (d.e_m / d.e_n).replace([np.inf, 0], np.nan).dropna()
        score[h] = float(np.exp(np.log(r).mean()))
    res.append(dict(**g, **{f"gmean_relMAE_h{h}": v for h, v in score.items()}, mean=float(np.mean(list(score.values())))))
    print(res[-1], flush=True)
best = min(res, key=lambda r: r["mean"])
OUT.write_text(json.dumps({"grid": res, "best": best, "tuning_cutoffs": [cuts[0], cuts[-1]], "refits": refits}, indent=2)); print("BEST", best)
