# Bangladesh Food Price Watch

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehediparvez/foodprice_watch/blob/main/FoodPriceWatch_Colab.ipynb)

Master's project (not a thesis): detect and explain unexplained food price rises in Dhaka, using TCB daily retail prices (63 items, May 2021 – Oct 2026) with world prices, exchange rate, fuel, weather, policy and event drivers.

| RQ | Question | Stage |
|---|---|---|
| RQ1 | Does any model beat "tomorrow = today"? | S05, S06 |
| RQ2 | Which driver groups add value beyond persistence, and for which goods (with placebo control)? | S06 |
| RQ3 | Do forecast-interval alerts flag the 12 documented shocks, at what false-alarm rate? | S07 |
| RQ4 | How much of each rise is explained by measured cost drivers, and how much is not? | S09 |
| RQ5 | Is a flagged rise national or local (WFP markets)? | S08 — blocked until WFP data is supplied |

## Run it in Colab

1. Click **Open in Colab** above.
2. On Google Drive, create `MyDrive/FoodPriceWatch/inbox/project/` and put the 32 project data files there. Data is **not** in this public repo (TCB reuse terms are still unconfirmed).
3. Run the cells top to bottom. Cell 2 clones this repo into `MyDrive/FoodPriceWatch/` the first time and pulls code updates afterwards.

**Disconnects:** reconnect, run cells 1–4, then re-run the interrupted stage cell. Every unit of work is saved to Drive with a `_SUCCESS.json` marker, finished stages are skipped, and each test period can be unsealed only once.

## Layout

- `src/fpw/` shared library (loaders, availability lags, checkpoints, benchmark metrics, alert rules)
- `src/stages/sNN*.py` one script per stage step; `src/stages/finalize.py` runs a stage's tests, marks it done, commits
- `tests/` acceptance tests (panel invariants, leakage, no ±inf, seals, wording, …)
- `config/` settings, item→driver map, verified event dates
- `state/` ledger (`stages.json`), pre-registrations and seals (written during runs)
- `AGENTS.md`, `SPEC.md`, `DECISIONS.md`, `DEVIATIONS.md`, `PROGRESS.md`: the agent instruction set and the run log
- `docs/` full instruction set, data inventory, prompts, reference notes

Author: to be confirmed (`config.yaml → author`).
