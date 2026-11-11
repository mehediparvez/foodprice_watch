"""Stage registry: the one place that says what each stage runs, produces and is tested by.

Used by src/stages/finalize.py (acceptance) and fpw.runner (`make stage S=NN`).
state/stages.json stays the ledger (status, hashes); this file is code, not state.
Commands run from the project root. Each command is itself resumable (unit markers).
"""
PY = "python -W ignore"

STAGES = {
    "S00": dict(
        run=["python src/stages/s00_intake.py"], commit="S00: scaffold and intake",
        outputs=["data/raw/MANIFEST.csv", "DECISIONS.md"], tests=["tests/test_s00.py"]),
    "S01": dict(
        run=[f"{PY} src/stages/s01.py"], note="Palm Olein 2L proposed correction not applied",
        outputs=["data/processed/tcb_v1.0_rebuilt.parquet", "data/processed/corrections_proposed.csv", "reports/tables/T1.csv"],
        tests=["tests/test_s01_panel.py"]),
    "S04": dict(
        run=[f"{PY} src/stages/s04.py"],
        outputs=["data/processed/features.parquet", "reports/tables/T3.csv", "config/s04_frozen.json", "config/item_driver_map.yaml"],
        tests=["tests/test_s04_drivers.py", "tests/test_leakage.py", "tests/test_no_inf.py"]),
    "S05": dict(
        run=[f"{PY} src/stages/s05_run.py test", f"{PY} src/stages/s05_score.py"],
        outputs=["outputs/05_baseline/results_by_group_repro.csv", "outputs/05_baseline/repro_diff_ALL.csv"],
        tests=["tests/test_s05_repro.py"]),
    # S06 and S07: tune/run -> pre-register -> commit -> unseal the test once -> score
    "S06": dict(
        before=[f"{PY} src/stages/s06_tune.py"], prereg=(f"{PY} src/stages/s06_prereg.py", "state/prereg_S06.yaml"),
        prereg_commit="S06: pre-registration committed before unsealing",
        run=[f"{PY} src/stages/s06_run.py", f"{PY} src/stages/s06_score.py"],
        outputs=["state/prereg_S06.yaml", "reports/tables/T4.csv", "reports/tables/T5.csv", "reports/tables/T5b.csv"],
        tests=["tests/test_s06_grid.py", "tests/test_seal.py"]),
    "S07": dict(
        before=[f"{PY} src/stages/s07_run.py"], prereg=(f"{PY} src/stages/s07_prereg.py", "state/prereg_S07.yaml"),
        prereg_commit="S07: pre-registration committed before event scoring",
        run=[f"{PY} src/stages/s07_score.py"],
        outputs=["state/prereg_S07.yaml", "reports/tables/T6.csv", "reports/tables/T7.csv", "reports/tables/T8.csv"],
        tests=["tests/test_s07_alerts.py", "tests/test_seal.py"]),
    "S09": dict(
        run=[f"{PY} src/stages/s09_run.py", f"{PY} src/stages/s09_score.py"],
        outputs=["reports/tables/T9.csv", "reports/tables/T10.csv", "reports/tables/T9b_sign_checks.csv"],
        tests=["tests/test_s09_explain.py", "tests/test_wording.py"]),
    "S10": dict(
        run=[f"{PY} src/stages/s10.py"],
        outputs=["reports/tables/T11.csv"], tests=["tests/test_s10_robust.py"]),
    "S11": dict(
        run=[f"{PY} src/stages/s11.py"],
        outputs=["reports/RESULTS_REGISTER.md", "reports/README.md"], tests=["tests/test_wording.py"]),
}
