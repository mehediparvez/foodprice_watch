"""make check: verify ledger vs disk, raw manifest hashes, then run tests/."""
import csv, json, subprocess, sys
from pathlib import Path
from .checkpoint import sha256
from .state import ROOT, load, save
ok = True
man = ROOT / "data/raw/MANIFEST.csv"
if man.exists():
    for r in csv.DictReader(man.open()):
        if r["status"] == "present" and sha256(ROOT / r["path"]) != r["sha256"]:
            print("RAW CHANGED:", r["path"]); ok = False
d = load(); changed = False
for s in d["stages"]:
    if s["status"] == "done":
        for o, h in s["output_sha256"].items():
            p = ROOT / o
            if not p.exists() or sha256(p) != h:
                print(f"{s['id']}: output {o} missing/changed -> pending"); s["status"] = "pending"; changed = True; ok = False
if changed: save(d)
print({s["id"]: s["status"] for s in d["stages"]})
r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(ROOT / "tests")], cwd=ROOT)
if r.returncode not in (0, 5): ok = False
print("CHECK", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
