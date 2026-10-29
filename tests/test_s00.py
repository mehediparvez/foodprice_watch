import csv, json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
def test_manifest_present():
    rows = list(csv.DictReader((R/"data/raw/MANIFEST.csv").open()))
    assert sum(r["status"]=="present" and r["path"].startswith("data/raw/project/") for r in rows) == 32
def test_ledger_valid():
    d = json.loads((R/"state/stages.json").read_text()); assert len(d["stages"]) == 16
