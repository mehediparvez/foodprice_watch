"""Run a stage's acceptance tests and, only if they pass, mark it done in state/stages.json and append PROGRESS.md.
Usage: python src/stages/finalize.py S01 [note]"""
import sys, subprocess, time
sys.path.insert(0, "src")
from fpw.state import ROOT, finish, load
from fpw.registry import STAGES
sid = sys.argv[1]; note = " ".join(sys.argv[2:]) or None
outs, tests = STAGES[sid]["outputs"], STAGES[sid]["tests"]
missing = [o for o in outs if not (ROOT / o).exists()]
if missing: print("NOT DONE — missing outputs:", missing); sys.exit(1)
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:warnings", *tests], cwd=ROOT)
if r.returncode != 0: print(f"NOT DONE — {sid} acceptance tests failed"); sys.exit(1)
finish(sid, outs, notes=note)
with open(ROOT / "PROGRESS.md", "a") as f:
    f.write(f"\n## {time.strftime('%Y-%m-%d %H:%M')} — stage {sid} — finalized\n- Verified: pytest {' '.join(tests)} → pass\n" + (f"- Note: {note}\n" if note else ""))
subprocess.run(["git", "add", "-A"], cwd=ROOT); subprocess.run(["git", "commit", "-qm", f"{sid}: done [checks pass]"], cwd=ROOT)
print(f"{sid} DONE and committed")
