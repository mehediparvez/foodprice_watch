"""S05 unit runner: one unit = one cutoff (all 7 classical models x 54 series). Resumable via markers."""
import sys, time, hashlib, json
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import Naive, SeasonalNaive, WindowAverage, RandomWalkWithDrift, AutoARIMA, AutoETS, AutoTheta
from fpw.bench import wide, cutoffs
from fpw.checkpoint import run_unit
from fpw.io import ROOT, CFG
from fpw import state
which = sys.argv[1] if len(sys.argv) > 1 else "test"
OUTD = ROOT / f"outputs/05_baseline/{which}"; OUTD.mkdir(parents=True, exist_ok=True)
y = wide().ffill()          # training input only: carry last reported price over not-reported days (logged deviation); targets are scored on reported values only
cfg_hash = hashlib.sha256(json.dumps(CFG, sort_keys=True, default=str).encode()).hexdigest()[:12]
MAX_NEW = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9   # optional: stop after N newly computed units
new = 0
cuts = cutoffs() if which == "test" else __import__("fpw.bench", fromlist=["tuning_cutoffs"]).tuning_cutoffs()
for i, c in enumerate(cuts):
    out = OUTD / f"cut_{c:04d}.parquet"
    def compute(c=c):
        long = y.loc[:c].stack().reset_index(); long.columns = ["ds", "unique_id", "y"]
        sf = StatsForecast(models=[Naive(), SeasonalNaive(7), WindowAverage(7), RandomWalkWithDrift(), AutoARIMA(season_length=7), AutoETS(season_length=7), AutoTheta(season_length=7)], freq=1, n_jobs=2)
        fc = sf.forecast(df=long, h=30).rename(columns={"unique_id": "item_id", "RWD": "RWD"})
        fc["cutoff"] = c; fc["step"] = fc.ds - c; return fc.drop(columns="ds")
    t = time.time(); r = run_unit(out, compute, inputs={"cutoff": c}, config_hash=cfg_hash, seed=CFG["seed"])
    state.update("S05", last_unit=f"{which}:cut_{c}", units_done=i + 1)
    print(i + 1, len(cuts), c, r, round(time.time() - t, 1), flush=True)
    new += r == "done"
    if new >= MAX_NEW: print("STOPPED AFTER", new, "NEW UNITS (re-run to continue)"); sys.exit(0)
print("ALL UNITS DONE", which)
