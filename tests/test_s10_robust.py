from pathlib import Path
import pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; T = R/"reports/tables/T11.csv"
pytestmark = pytest.mark.skipif(not T.exists(), reason="S10 not run")
def test_t11(): t = pd.read_csv(T); assert t.check.str.contains("placebo").any() and t.check.str.contains("leave-one").any()
