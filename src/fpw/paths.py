"""Single source of truth for project paths (light: standard library only).

Every module and script takes ROOT from here instead of recomputing it.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_YAML = ROOT / "config.yaml"
RAW = ROOT / "data/raw/project"          # read-only, hashed by S00
RAW_EXTERNAL = ROOT / "data/raw/external"
PROC = ROOT / "data/processed"
OUTPUTS = ROOT / "outputs"
REPORTS = ROOT / "reports"
STATE = ROOT / "state"
LEDGER = STATE / "stages.json"
