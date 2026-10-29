import json
from pathlib import Path
import pandas as pd, numpy as np, pytest
R = Path(__file__).resolve().parents[1]
P = R/"data/processed/tcb_v1.0_rebuilt.parquet"
pytestmark = pytest.mark.skipif(not P.exists(), reason="S01 not run")
@pytest.fixture(scope="module")
def df(): return pd.read_parquet(P)
def test_shape(df):
    assert len(df)==76440 and df.Date.nunique()==1412 and df.item_id.nunique()==63
    assert str(df.Date.min().date())=="2021-05-17" and str(df.Date.max().date())=="2026-10-24"
def test_keys(df): assert not df.duplicated(["Date","item_id"]).any()
def test_mid(df):
    b = df.Price_Min.notna()&df.Price_Max.notna()
    assert np.isclose(df.Price_Avg[b],(df.Price_Min[b]+df.Price_Max[b])/2).all()
    assert df.flag_min_only.sum()==2 and not (df.Price_Min>df.Price_Max).any()
def test_corrections(df):
    v = df.loc[(df.item_id=="MS Rod (40 Grade) | per metric ton")&(df.Date=="2021-06-19"),"Price_Max"].iloc[0]; assert v==70500
    assert df.loc[(df.item_id=="Palm Olein - Bottled | 5 litre")&(df.Date=="2025-04-18"),"Price_Avg"].isna().all()
def test_proposed_not_applied(df):
    assert (R/"data/processed/corrections_proposed.csv").exists()
    assert df.loc[(df.item_id=="Palm Olein - Bottled | 2 litre")&(df.Date=="2025-04-18"),"Price_Avg"].iloc[0]==842.5
def test_gap(df): assert df.loc[df.gap_2022,"Date"].nunique()==24
def test_week_ago(): assert json.loads((R/"outputs/s01_checks.json").read_text())["week_ago_match_share"]>=0.995
