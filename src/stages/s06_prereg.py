"""S06 step 2: write the pre-registration (must be committed before the test is unsealed)."""
import sys, json, yaml
sys.path.insert(0, "src")
from fpw.io import ROOT, CFG
from fpw.ml import load, GROUPS, FLAGS, placebo_assign
from fpw.bench import cutoffs
t = json.loads((ROOT / "state/tuning_S06.json").read_text())["best"]
F = load()
mapped = {g: sorted(str(x) for x in F.loc[F[FLAGS[g]] == 1, "item_id"].unique()) for g in GROUPS}
plac = {}
for i, g in enumerate(GROUPS):
    _, pick, donor = placebo_assign(F, g, CFG["seed"] + i); plac[g] = [dict(item=str(a), donor=str(b)) for a, b in zip(pick, donor)]
cuts = cutoffs()
pre = dict(stage="S06", written="2026-10-29", test_period=CFG["split"]["test"], test_cutoffs=dict(first=cuts[0], last=cuts[-1], n=len(cuts), spacing_report_days=7),
    refit_every_n_cutoffs=8, horizons_report_days=[1, 7, 14, 30],
    model=dict(type="LightGBM global direct multi-horizon, target log(y_t+h)-log(y_t), L1 objective", num_leaves=t["num_leaves"], n_estimators=t["n_estimators"], learning_rate=0.05,
               tuned_on="2024 validation cutoffs only", seed=CFG["seed"]),
    core=dict(features="own lags/returns/deviation/volatility/reports-since-change, item & stratum codes, G0 calendar"),
    driver_group_order=list(GROUPS), group_columns=GROUPS, mapped_items=mapped,
    test=dict(primary="per group: DM-HLN (core+group vs core) on each mapped long-history item at each horizon; Holm across items within group x horizon; alpha 0.05 two-sided",
              effect="delta relMAE (core+group minus core, both relative to naive) per item; mean across mapped items with 2,000-draw item bootstrap 95% CI",
              placebo="same group columns copied from random mapped donor items onto an equal number of random unmapped items (seed = config seed + group index); matched-minus-placebo gap in mean delta relMAE with bootstrap CI",
              benchmark="RQ1: LightGBM core and core+all forecasting groups (M1) vs naive on 54 long-history series, gmean relMAE / win rate / DM-HLN+Holm per stratum, alongside the S05 classical models"),
    placebo_assignment=plac, deviations_known=["Chronos-2 not run (model hub blocked)", "short-history items excluded from S06 (scored in S07 only)"])
p = ROOT / "state/prereg_S06.yaml"; p.write_text(yaml.safe_dump(pre, sort_keys=False, allow_unicode=True)); print("wrote", p)
