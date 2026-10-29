from pathlib import Path
import numpy as np, pandas as pd, pytest
R = Path(__file__).resolve().parents[1]; FP = R/"data/processed/features.parquet"
pytestmark = pytest.mark.skipif(not FP.exists(), reason="S04 not run")
def test_no_inf():
    F = pd.read_parquet(FP); num = F.select_dtypes("number")
    assert not np.isinf(num.to_numpy(dtype=float)).any()
