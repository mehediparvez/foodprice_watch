from pathlib import Path
import numpy as np, pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; FP = R/"data/processed/features.parquet"
pytestmark = pytest.mark.skipif(not FP.exists(), reason="S04 not run")
@pytest.fixture(scope="module")
def F(): return pd.read_parquet(FP)
def test_rows(F): assert len(F) == 76440
def test_unmapped_slots_empty_not_zero(F):
    for slot, flag in [("own_world_price","has_world_price"),("own_brent","has_brent"),("own_export_measure","has_export_measure"),("own_fishing_ban","has_fishing_ban"),("weather_1","has_weather")]:
        assert F.loc[F[flag]==0, slot].isna().all(), slot
def test_slot_counts(F):
    assert F.loc[F.has_world_price==1].item_id.nunique() == 17 and F.loc[F.has_brent==1].item_id.nunique() == 5
def test_out_of_coverage_unknown(F):
    assert F.loc[F.Date < "2023-10-01", "e4_disruption"].isna().all()
def test_comtrade_blanked(F):
    assert (F.e3_src_month.dropna() < "2026-05-01").all()
def test_prices_untouched(F):
    p = pd.read_parquet(R/"data/processed/tcb_v1.0_rebuilt.parquet").sort_values(["item_id","Date"]).reset_index(drop=True)
    assert np.allclose(p.Price_Avg.fillna(-1).values, F.sort_values(["item_id","Date"]).Price_Avg.fillna(-1).values)
