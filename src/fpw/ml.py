"""LightGBM direct multi-horizon design (S06/S07/S09). Global model across items; target = log(y_{t+h}) - log(y_t)."""
import numpy as np, pandas as pd, yaml, lightgbm as lgb
from .io import ROOT, PROC, CFG
H = [1, 7, 14, 30]
CAL = ["month", "dow", "days_to_ramadan", "days_to_eid_fitr", "days_to_eid_adha", "in_ramadan", "holiday_next7", "days_since_prev_report"]
OWN = ["lp", "r1", "r7", "r14", "r30", "dev30", "vol30", "rsc", "item_code", "stratum_code"]
GROUPS = {"G1": ["own_world_price", "own_world_price_ch3"], "G2": ["own_brent", "own_brent_ch30"], "G3": ["own_export_measure"],
          "G4": ["own_fishing_ban"], "G5": ["weather_1", "weather_2", "weather_3"]}
FLAGS = {"G1": "has_world_price", "G2": "has_brent", "G3": "has_export_measure", "G4": "has_fishing_ban", "G5": "has_weather"}
EXPLAIN = ["e1_fx", "e1_fx_ch30", "e2_diesel", "e3_imports_log_t", "e3_unit_value", "e4_exporter_measure", "e4_disruption", "e4_cyclone_flood", "e4_duty_cut", "e4_regime_interim", "e5_world_explain"]
def load(long_history_only=True):
    F = pd.read_parquet(PROC / "features.parquet")
    if long_history_only: F = F[~F.short_history]
    F = F.sort_values(["item_id", "report_idx"]).reset_index(drop=True)
    g = F.groupby("item_id")
    F["lp"] = g.log_price.ffill()                                   # input only; carry last reported price
    g = F.groupby("item_id")
    for k in [1, 7, 14, 30]: F[f"r{k}"] = F.lp - g.lp.shift(k)
    F["dev30"] = F.lp - g.lp.transform(lambda s: s.rolling(30, min_periods=10).mean())
    F["vol30"] = g.r1.transform(lambda s: s.rolling(30, min_periods=10).std())
    chg = (F.r1.fillna(0) != 0).astype(int); F["rsc"] = chg.groupby([F.item_id, chg.groupby(F.item_id).cumsum()]).cumcount()
    F["item_code"] = F.item_id.astype("category").cat.codes; F["stratum_code"] = F.eval_stratum.astype("category").cat.codes
    gi = F.report_idx.values
    gap_idx = F.loc[F.gap_2022, "report_idx"]; g0, g1 = int(gap_idx.min()), int(gap_idx.max())
    F["touch_gap"] = (gi >= g0) & (gi - 30 <= g1)                   # feature window overlaps 2022 gap
    for h in H:
        F[f"y{h}"] = g.log_price.shift(-h) - F.lp                  # target uses actual reported future price only
        F[f"tgap{h}"] = (gi + h >= g0) & (gi <= g1)
    F["gap_bounds"] = f"{g0}-{g1}"
    return F
def features(variant_groups):
    cols = OWN + CAL
    for gname in variant_groups: cols += GROUPS[gname]
    return cols
PARAMS = dict(objective="l1", learning_rate=0.05, num_leaves=31, min_data_in_leaf=50, feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=1, verbose=-1, seed=CFG["seed"], num_threads=int(__import__("os").environ.get("FPW_THREADS", "2")))
def fit(F, cutoff, h, cols, params=None, n_estimators=300, objective=None, alpha=None):
    p = dict(PARAMS, **(params or {}))
    if objective: p["objective"] = objective
    if alpha is not None: p["alpha"] = alpha
    tr = F[(F.report_idx + h <= cutoff) & F[f"y{h}"].notna() & ~F.touch_gap & ~F[f"tgap{h}"] & F.lp.notna()]
    ds = lgb.Dataset(tr[cols], tr[f"y{h}"], categorical_feature=[c for c in ["item_code", "stratum_code"] if c in cols], free_raw_data=False)
    return lgb.train(p, ds, num_boost_round=n_estimators)
def placebo_assign(F, group, seed):
    """Copy the group's driver columns from mapped items onto a random set of unmapped items (same dates). Returns (F2, placebo_items)."""
    rng = np.random.default_rng(seed); flag = FLAGS[group]
    mapped = sorted(F.loc[F[flag] == 1, "item_id"].unique()); unm = sorted(F.loc[F[flag] == 0, "item_id"].unique())
    pick = list(rng.choice(unm, size=min(len(mapped), len(unm)), replace=False)); donor = list(rng.choice(mapped, size=len(pick), replace=True))
    F2 = F.copy()
    for tgt, src in zip(pick, donor):
        s = F.loc[F.item_id == src, ["report_idx", *GROUPS[group]]].set_index("report_idx")
        m = F2.item_id == tgt
        for c in GROUPS[group]: F2.loc[m, c] = F2.loc[m, "report_idx"].map(s[c]).values
    return F2, pick, donor
