from pathlib import Path
import pandas as pd, pytest, yaml, glob
R = Path(__file__).resolve().parents[1]; T4 = R/"reports/tables/T4.csv"
pytestmark = pytest.mark.skipif(not T4.exists(), reason="S06 not scored")
def test_units_complete():
    pre = yaml.safe_load((R/"state/prereg_S06.yaml").read_text())
    files = glob.glob(str(R/"outputs/06_lgbm/*__cut_*.parquet")); assert len(files) == 12 * 11
def test_tables():
    t4 = pd.read_csv(T4); assert {"LGBM_core", "LGBM_M1", "AutoETS", "Naive"} <= set(t4.model)
    t5b = pd.read_csv(R/"reports/tables/T5b.csv"); assert set(t5b.group) <= {"G1","G2","G3","G4","G5"} and len(t5b) > 0
