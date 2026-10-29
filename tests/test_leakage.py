import sys
from pathlib import Path
import numpy as np, pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R/"src"))
FP = R/"data/processed/features.parquet"
pytestmark = pytest.mark.skipif(not FP.exists(), reason="S04 not run")
from fpw import drivers as D
@pytest.fixture(scope="module")
def F(): return pd.read_parquet(FP)
def violations(src_month, dates, lag=208):
    return ((src_month + pd.Timedelta(days=lag)) > dates).sum()
def test_imports_respect_208(F):
    x = F[F.e3_src_month.notna()]
    assert violations(x.e3_src_month, x.Date) == 0
def test_75_day_rule_fails():
    """Rebuild the import as-of under the old 75-day rule: it must use months not yet available under the true 208-day lag."""
    ct = D.comtrade(rule_days=75); s = ct[ct.hs_code == "1006"].dropna(subset=["tonnes"]).sort_values("available")
    dates = pd.DataFrame({"Date": pd.date_range("2022-01-01", "2026-10-24", freq="7D")})
    a = pd.merge_asof(dates, s[["available","month"]], left_on="Date", right_on="available").dropna()
    assert violations(a.month, a.Date) > 0
def test_world_price_independent_rederive(F):
    imf = D.imf(); rng = np.random.default_rng(0)
    x = F[F.own_world_code.notna() & F.own_world_price.notna()].sample(300, random_state=1)
    for r in x.itertuples():
        ok = imf[imf.available <= r.Date].iloc[-1]
        assert np.isclose(np.log(ok[r.own_world_code]), r.own_world_price)
def test_weather_lag(F):
    # weather on report date t must not change if weather after t-5 were removed: recompute 7d tmax mean from data <= t-5
    w = D.weather(); bd = w[w.location_id <= 10].groupby("time").temperature_2m_max.mean().asfreq("D").rolling(7).mean()
    import json; ch = json.loads((R/"config/s04_frozen.json").read_text())["weather_chosen"]
    if "wx_bd_tmax_7d" not in ch: pytest.skip("tmax not chosen")
    col = f"weather_{ch.index('wx_bd_tmax_7d')+1}"
    x = F[F[col].notna()].sample(200, random_state=2)
    for r in x.itertuples(): assert np.isclose(bd.loc[r.Date - pd.Timedelta(days=5)], getattr(r, col))
