from pathlib import Path
import pandas as pd, pytest, hashlib, csv
R = Path(__file__).resolve().parents[1]; D = R/"outputs/05_baseline/repro_diff_ALL.csv"
pytestmark = pytest.mark.skipif(not D.exists(), reason="S05 not scored")
def test_within_tolerance_or_explained():
    d = pd.read_csv(D); bad = d[d["diff"].abs() > 0.02]
    expl = R/"outputs/05_baseline/REPRO_EXPLAINED.md"
    assert bad.empty or expl.exists(), bad
def test_baseline_untouched():
    row = [r for r in csv.DictReader((R/"data/raw/MANIFEST.csv").open()) if r["path"].endswith("baseline_results_by_group.csv")][0]
    assert hashlib.sha256((R/row["path"]).read_bytes()).hexdigest() == row["sha256"]
