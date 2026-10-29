"""Run a stage's acceptance tests and, only if they pass, mark it done in state/stages.json and append PROGRESS.md.
Usage: python src/stages/finalize.py S01 [note]"""
import sys, subprocess, time
sys.path.insert(0, "src")
from fpw.state import ROOT, finish, load
SPEC = {
 "S00": (["data/raw/MANIFEST.csv", "DECISIONS.md"], ["tests/test_s00.py"]),
 "S01": (["data/processed/tcb_v1.0_rebuilt.parquet", "data/processed/corrections_proposed.csv", "reports/tables/T1.csv"], ["tests/test_s01_panel.py"]),
 "S04": (["data/processed/features.parquet", "reports/tables/T3.csv", "config/s04_frozen.json", "config/item_driver_map.yaml"], ["tests/test_s04_drivers.py", "tests/test_leakage.py", "tests/test_no_inf.py"]),
 "S05": (["outputs/05_baseline/results_by_group_repro.csv", "outputs/05_baseline/repro_diff_ALL.csv"], ["tests/test_s05_repro.py"]),
 "S06": (["state/prereg_S06.yaml", "reports/tables/T4.csv", "reports/tables/T5.csv", "reports/tables/T5b.csv"], ["tests/test_s06_grid.py", "tests/test_seal.py"]),
 "S07": (["state/prereg_S07.yaml", "reports/tables/T6.csv", "reports/tables/T7.csv", "reports/tables/T8.csv"], ["tests/test_s07_alerts.py", "tests/test_seal.py"]),
 "S09": (["reports/tables/T9.csv", "reports/tables/T10.csv", "reports/tables/T9b_sign_checks.csv"], ["tests/test_s09_explain.py", "tests/test_wording.py"]),
 "S10": (["reports/tables/T11.csv"], ["tests/test_s10_robust.py"]),
 "S11": (["reports/RESULTS_REGISTER.md", "reports/README.md"], ["tests/test_wording.py"]),
}
sid = sys.argv[1]; note = " ".join(sys.argv[2:]) or None
outs, tests = SPEC[sid]
missing = [o for o in outs if not (ROOT / o).exists()]
if missing: print("NOT DONE — missing outputs:", missing); sys.exit(1)
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:warnings", *tests], cwd=ROOT)
if r.returncode != 0: print(f"NOT DONE — {sid} acceptance tests failed"); sys.exit(1)
finish(sid, outs, notes=note)
with open(ROOT / "PROGRESS.md", "a") as f:
    f.write(f"\n## {time.strftime('%Y-%m-%d %H:%M')} — stage {sid} — finalized\n- Verified: pytest {' '.join(tests)} → pass\n" + (f"- Note: {note}\n" if note else ""))
subprocess.run(["git", "add", "-A"], cwd=ROOT); subprocess.run(["git", "commit", "-qm", f"{sid}: done [checks pass]"], cwd=ROOT)
print(f"{sid} DONE and committed")
