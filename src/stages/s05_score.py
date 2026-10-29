"""S05 scoring: compare reproduction with the committed baseline (never overwritten)."""
import sys, glob
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from fpw.bench import wide, score
from fpw.io import ROOT, raw, item_meta
from fpw import state
files = sorted(glob.glob(str(ROOT / "outputs/05_baseline/test/cut_*.parquet")))
assert len(files) == 87, f"only {len(files)} units"
fc = pd.concat([pd.read_parquet(f) for f in files])
models = ["Naive", "SeasonalNaive", "WindowAverage", "RWD", "AutoARIMA", "AutoETS", "AutoTheta"]
y = wide(); yf = y.ffill()
gi = yf.index
from fpw.io import panel
p = panel(); gap = p.loc[p.gap_2022, "report_idx"]
tr = yf.loc[:808]; d = tr.diff().abs(); d.loc[(d.index >= gap.min()) & (d.index <= gap.max() + 1)] = np.nan
scale = d.mean().to_dict()
strata = item_meta()[["item_id", "eval_stratum"]]
per, grp = score(fc, y, models, strata, scale)
out = ROOT / "outputs/05_baseline/results_by_group_repro.csv"; grp.to_csv(out, index=False); per.to_csv(ROOT / "outputs/05_baseline/per_item_repro.csv", index=False)
base = pd.read_csv(raw("baseline_results_by_group.csv"))
cmp = base.merge(grp, on=["eval_stratum", "model", "step"], suffixes=("_base", "_repro"))
cmp["diff"] = cmp.gmean_relMAE_repro - cmp.gmean_relMAE_base
allc = cmp[cmp.eval_stratum == "ALL"][["model", "step", "gmean_relMAE_base", "gmean_relMAE_repro", "diff", "n_items_base", "n_items_repro", "better_base", "better_repro", "worse_base", "worse_repro", "median_MASE_base", "median_MASE_repro"]]
allc.to_csv(ROOT / "outputs/05_baseline/repro_diff_ALL.csv", index=False); cmp.to_csv(ROOT / "outputs/05_baseline/repro_diff_all_strata.csv", index=False)
print(allc.round(3).to_string()); print("max |diff| ALL:", round(allc["diff"].abs().max(), 4), " all strata:", round(cmp["diff"].abs().max(), 4))
