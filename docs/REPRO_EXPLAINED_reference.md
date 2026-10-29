# S05 baseline reproduction — differences beyond ±0.02 (explained, not tuned away)

Result: 87 origins (cutoffs 808..1410, every 7 report days) × 7 statsforecast models × 54 long-history series. Naive, n_items, and the deterministic models at h ≥ 7 match the committed baseline; AutoETS (the headline model) matches within 0.01 at every horizon in the ALL stratum (1.178/1.046/1.039/1.033 vs 1.168/1.047/1.038/1.033).

Outside tolerance (ALL stratum): AutoTheta h=1 (+0.273), AutoARIMA all horizons (+0.022..+0.063), WindowAverage h=1 (+0.025), SeasonalNaive h=1 (+0.021). Per-stratum differences (see repro_diff_all_strata.csv) concentrate at h=1 and in AutoARIMA/AutoTheta.

Why (best explanation from the evidence; the original settings were never recorded):
1. Treatment of not-reported days in the training input. This run carries the last reported price forward (DEVIATIONS.md). Deterministic models (SeasonalNaive, WindowAverage) differ only in volatile_perishable, the stratum with long not-reported stretches (hilsa bans, imported onion curb, local ginger 2025), so the original pipeline must have handled gaps differently (e.g. dropped them, which shifts the 7-step season and the 7-report window).
2. Automatic model selection. AutoARIMA and AutoTheta choose orders/decomposition per fit; small input differences (point 1) and library version (statsforecast 2.1.1 here; original version unknown) change the selected model, which matters most at h=1 where naive errors are tiny.
3. MASE scaling. Median MASE is ~10–20% higher at every horizon for every model, including Naive, so the scale differs (here: mean |Δ| of the carried-forward training series up to cutoff 808, excluding the 2022 gap; the original scale window is unknown). relMAE is unaffected by the scale.

Conclusion unchanged: no classical model beats naive at any horizon in any stratum; AutoETS is closest; significantly-better counts are 0 everywhere (the baseline had 1 for AutoTheta h7 and RWD h1/h7, the imported-onion series). The original baseline_results_by_group.csv is untouched (hash checked).
