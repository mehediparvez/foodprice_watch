# Bangladesh Food Price Watch — Colab codebase

1. Upload this folder (unzipped) to Google Drive as `MyDrive/FoodPriceWatch/`, or upload the zip to `MyDrive/` and let notebook cell 2 unzip it.
2. Put the 32 project data files in `MyDrive/FoodPriceWatch/inbox/project/` (exact file names as in the project).
   Optional: external data in `inbox/external/{wfp,agripricebd,pinksheet,ohlc}/`, original TCB Excel files in `inbox/tcb_originals/`.
3. Open `FoodPriceWatch_Colab.ipynb` in Colab and run the cells top to bottom.

Resume after any disconnect: run cells 1–4 again, then re-run the stage cell that was interrupted. Every unit of work
(one forecast origin, one model block, one refit) writes its result plus a `_SUCCESS.json` marker on Drive, so finished units are skipped.
Stages already marked `done` in `state/stages.json` are skipped automatically.

Layout: `src/fpw/` shared library · `src/stages/sNN*.py` one script per stage step · `src/stages/finalize.py` runs a stage's tests and marks it done ·
`tests/` acceptance tests · `config/` settings and the item→driver map · `state/` ledger, pre-registrations, seals · `reports/` results pack.
