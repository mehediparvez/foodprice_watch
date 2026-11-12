# tools/

Standalone data-collection helpers. Standard library only. They are NOT part of the pipeline and are never run by the agent.

- `tcb_download.py` downloads the TCB daily Excel reports (pages 1-15 of tcb.gov.bd). Run by the user only; project rule: the agent never downloads from TCB.
- `tcb_append.py` adds newly converted report days to the existing price CSV. It checks the columns, prices and duplicates, stops on any conflict, and never overwrites a file. Run by the user after `tcb_download.py` (which skips files it already has) and the Bangla-to-English converter. A longer panel changes the sample: log it in DEVIATIONS.md first.
- `comtrade_bd_food_imports.py` builds the monthly Comtrade import table (public preview API, or a free key in COMTRADE_KEY). Run by the user only.

Outputs go to inbox/ (never straight into data/raw/); S00 intake copies and hashes them.
