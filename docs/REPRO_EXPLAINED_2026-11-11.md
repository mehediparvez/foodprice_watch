# S05 baseline reproduction: differences beyond +-0.02 (explained, not tuned away)

Run of 2026-11-11 on Colab (statsforecast 2.1.1, 8 vCPUs): 87 origins x 7 classical models x 54 long-history series. Naive matches exactly. AutoETS is within 0.010 of baseline_results_by_group.csv at every horizon in the ALL stratum.

Outside tolerance (ALL stratum, gmean relMAE, repro minus baseline): AutoTheta h=1 +0.273; AutoARIMA h=1/7/14/30 +0.063/+0.040/+0.035/+0.027; WindowAverage h=1 +0.025; SeasonalNaive h=1 +0.021.

Same models fall outside tolerance in the 29 Oct 2026 reference run (docs/REPRO_EXPLAINED_reference.md). AutoTheta, WindowAverage and SeasonalNaive differences are identical; AutoARIMA is slightly larger at h=7/14/30 (cause not established; this run used 8 threads, the reference 2).

Hypotheses (original settings were never recorded, none verified): (1) not-reported days are carried forward in the training input (DEVIATIONS.md), the original may have handled gaps differently; (2) AutoARIMA and AutoTheta pick orders per fit, so small input or library differences change them most at h=1.

Conclusion unchanged: no classical model beats naive in the ALL stratum at any horizon; AutoETS is closest. The original baseline file is untouched.
