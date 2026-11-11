# Architecture

One pipeline, run stage by stage. Each stage reads earlier outputs, writes new files next to them (never over earlier results), and is accepted by tests before `state/stages.json` marks it done.

```
inbox/ (user drops files)
   │  S00 intake: copy + SHA-256 (data/raw/MANIFEST.csv)
   ▼
data/raw/            read-only inputs (never edited)
   │  S01 rebuild panel        S04 driver panel (availability-dated, has_<slot> flags)
   ▼
data/processed/      tcb_v1.0_rebuilt.parquet, features.parquet, corrections_proposed.csv
   │  S05 baseline repro  →  S06 benchmark + driver groups (RQ1, RQ2)
   │  S07 alerts (RQ3)    →  S09 explanation ladder (RQ4)  →  S10 robustness
   ▼
outputs/, reports/   tables T*, figures F*, RESULTS_REGISTER.md (every number: value, file, command, commit)
```

## Layers

| Layer | Where | Rule |
|---|---|---|
| Settings | `config.yaml`, `config/*.yaml` | the only place for dates, horizons, thresholds, driver mapping |
| Library | `src/fpw/` | importable, no side effects on import beyond reading config |
| Stage scripts | `src/stages/` | one resumable script per step; write units atomically with a `_SUCCESS.json` marker |
| Registry | `src/fpw/registry.py` | what each stage runs, produces and is tested by (code, not state) |
| Ledger | `state/stages.json` | status and hashes only; entries are never deleted or reordered |
| Tests | `tests/` | acceptance checks per stage plus leakage, no-inf, seal and wording tests |
| Docs | `SPEC.md`, `DECISIONS.md`, `DEVIATIONS.md`, `PROGRESS.md`, `docs/` | scope, choices, changes from the spec, narrative log |
| Tools | `tools/` | user-run data collection helpers, outside the pipeline |

## `src/fpw/` modules

| Module | Role |
|---|---|
| `paths.py` | `ROOT` and the standard directories (standard library only) |
| `io.py` | loaders for raw files (data rules 1-12) |
| `drivers.py` | driver readers and availability dating (Comtrade month start + 208 d) |
| `ml.py`, `bench.py` | LightGBM features and fits, placebo assignment, DM-HLN, Holm, scoring |
| `alerts.py` | interval bounds, persistence rule, event matching, false alarms, Kupiec |
| `checkpoint.py` | atomic writes, unit markers, the one-shot test seal |
| `state.py` | ledger updates (status fields only) |
| `registry.py`, `runner.py` | stage definitions and the command-line runner (`make stage S=S01`) |
| `check.py` | `make check`: raw hashes, ledger vs disk, tests |

## Running

- Colab (heavy stages): `FoodPriceWatch_Colab.ipynb`.
- Local, standard library only for the runner: `make check`, `make stage S=S01 [DRY=1]`.
- Stage dependencies come from `state/stages.json`; the runner refuses to start a stage before they are done.

## Not built yet

S02 (audit, needs the original TCB Excel files), S03 and S08 (WFP intake and locate), Chronos-2. S12-S14 are optional and skipped.
