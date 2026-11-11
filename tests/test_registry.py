"""The registry (code) and the ledger (state/stages.json) must agree; scripts and tests it names must exist."""
import json, re
from pathlib import Path
from fpw.registry import STAGES
from fpw import runner

R = Path(__file__).resolve().parents[1]
LEDGER = {s["id"]: s for s in json.loads((R / "state/stages.json").read_text())["stages"]}


def test_registry_ids_are_in_ledger():
    assert set(STAGES) <= set(LEDGER)


def test_ledger_outputs_are_produced_by_registry_stage():
    for sid, spec in STAGES.items():
        assert set(LEDGER[sid]["outputs"]) <= set(spec["outputs"]), sid


def test_named_scripts_and_tests_exist():
    for sid, spec in STAGES.items():
        cmds = spec.get("before", []) + spec["run"] + ([spec["prereg"][0]] if "prereg" in spec else [])
        for c in cmds:
            m = re.search(r"(src/stages/\S+\.py)", c)
            assert m and (R / m.group(1)).exists(), (sid, c)
        for t in spec["tests"]:
            assert (R / t).exists(), (sid, t)


def test_plan_orders_preregistration_before_the_test_is_unsealed():
    steps = runner.plan("S06")
    assert steps.index(next(s for s in steps if "s06_prereg" in s)) < steps.index(next(s for s in steps if "s06_run" in s)) \
        or (R / "state/prereg_S06.yaml").exists()
    assert steps[-1].startswith("python src/stages/finalize.py S06")
