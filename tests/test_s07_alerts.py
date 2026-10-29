from pathlib import Path
import pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; T7 = R/"reports/tables/T7_event_level.csv"
pytestmark = pytest.mark.skipif(not T7.exists(), reason="S07 not scored")
def test_all_12_events_reported():
    assert pd.read_csv(T7).event_id.nunique() == 12
def test_tables_exist():
    for t in ["T6", "T7", "T8"]: assert (R/f"reports/tables/{t}.csv").exists()
