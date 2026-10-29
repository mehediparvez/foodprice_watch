"""Shared loaders (data rules 1-12). Raw files are read-only."""
from pathlib import Path
import pandas as pd, yaml
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/project"
PROC = ROOT / "data/processed"
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
def raw(name): return RAW / name
def panel():
    import numpy as np
    p = pd.read_parquet(PROC / "tcb_v1.0_rebuilt.parquet"); p["log_price"] = np.log(p.Price_Avg); return p
def item_meta():
    m = pd.read_csv(raw("item_meta.csv"))
    for c in ["first_date","last_date"]:
        m[c] = pd.to_datetime(m[c], format="%d-%m-%y")          # rule 8
    m["short_history"] = m["short_history"].astype(str).str.upper().eq("TRUE")
    return m
