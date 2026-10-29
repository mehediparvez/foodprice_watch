from pathlib import Path
import pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; T9 = R/"reports/tables/T9.csv"
pytestmark = pytest.mark.skipif(not T9.exists(), reason="S09 not scored")
def test_ladder_adds_up():
    t = pd.read_csv(T9); s = t.M0_persistence_calendar + t.M1_minus_M0_forecast_drivers + t.M2_minus_M1_explain_drivers + t.not_explained_by_measured_cost_drivers
    assert (abs(s - t.realized_log_change) < 1e-9).all()
def test_t10(): assert (R/"reports/tables/T10.csv").exists()
