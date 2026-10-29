<!-- DEVIATIONS.md — one entry per change from SPEC.md, written BEFORE continuing -->
| date | stage | what changed | reason | approved by user? |
|---|---|---|---|---|
| 2026-10-29 | S00 | Decisions D4–D8 use report defaults pending confirmation (DECISIONS.md) | user asked to proceed | pending |
| 2026-10-29 | S04 | IMF codes corrected: soybean oil POILSOY→PSOIL (absent), palm oil POILAPSP→PPOIL (POILAPSP is crude oil), milk powder→PMILK | checked against the file's description row | n/a |
| 2026-10-29 | S04 | Sugar (PSUGAISA) and chickpea (PCHANA) world prices explanation-only (E5) | keep G1 = chats' map | pending |
| 2026-10-29 | S05/S06 | Training inputs carry the last reported price over not-reported days (targets scored on reported values only) | models need gap-free input; evaluation unaffected | pending |
| 2026-10-29 | S06 | Chronos-2 / foundation models not implemented in this codebase (optional S13) | blocked in the build environment | pending |
| 2026-10-29 | S06 | Refit every 8 test cutoffs (56 report days) for LightGBM | compute budget | pending |
| 2026-10-29 | S09 | India onion ban dates verified (config/verified_events.yaml); other exporter rows stay reconstructed; Sep 2023 caps not studied | verification rule / no sourced event | n/a |
| 2026-10-29 | S10 | Weekly-vs-daily and Min/Max-target robustness not run; RQ5 robustness omitted (S08 blocked) | scope / missing WFP | pending |
