"""Shared benchmark utilities: series matrix, origins, metrics, DM-HLN + Holm."""
import numpy as np, pandas as pd
from scipy import stats
from .io import panel
H = [1, 7, 14, 30]
def wide(long_history_only=True):
    p = panel()
    if long_history_only: p = p[~p.short_history]
    y = p.pivot(index="report_idx", columns="item_id", values="Price_Avg")
    return y
def cutoffs(first_test_idx=809, last_idx=1411, step=7):
    return list(range(first_test_idx - 1, last_idx, step))          # cutoff = last training index; 87 for the 2025-26 test
def tuning_cutoffs():
    # 2024 report days as validation; same spacing
    p = panel(); d = p.drop_duplicates("report_idx").set_index("report_idx").Date
    i0 = int(d[d >= "2024-01-01"].index.min()); i1 = int(d[d <= "2024-12-31"].index.max())
    return list(range(i0 - 1, i1 - 30, 7))
def dm_hln(e1, e2, h):
    """Diebold-Mariano with Harvey-Leybourne-Newbold correction on absolute loss. Returns (stat, p) ; stat<0 => model 1 better."""
    d = np.abs(e1) - np.abs(e2); d = d[~np.isnan(d)]; n = len(d)
    if n < 8 or np.allclose(d, 0): return np.nan, np.nan
    q = max(int(np.ceil(h / 7)) - 1, 0)                              # origins every 7 report days -> overlap lags
    dc = d - d.mean(); g = [np.dot(dc[k:], dc[:n-k]) / n for k in range(q + 1)]
    v = (g[0] + 2 * sum(g[1:])) / n
    if v <= 0: return np.nan, np.nan
    dm = d.mean() / np.sqrt(v); k = np.sqrt((n + 1 - 2 * q + q * (q - 1) / n) / n)
    t = dm * k; p = 2 * stats.t.sf(abs(t), df=n - 1); return t, p
def holm(p):
    p = np.asarray(p, float); m = np.isfinite(p).sum(); out = np.full_like(p, np.nan); idx = np.argsort(np.where(np.isfinite(p), p, np.inf))
    run = 0
    for r, i in enumerate(idx[:m]): run = max(run, min(1, (m - r) * p[i])); out[i] = run
    return out
def score(fc, y, models, strata, train_naive_mae):
    """fc: rows (item_id, cutoff, step, model columns). Returns per-item table and grouped table like baseline_results_by_group."""
    fc = fc.copy(); fc["target_idx"] = fc.cutoff + fc.step
    yy = y.stack().rename("y").reset_index(); yy.columns = ["target_idx", "item_id", "y"]
    fc = fc.merge(yy, on=["target_idx", "item_id"], how="inner")
    rows = []
    for (it, h), g in fc[fc.step.isin(H)].groupby(["item_id", "step"]):
        en = g["Naive"] - g.y; mae_n = en.abs().mean(); sc = train_naive_mae.get(it, np.nan)
        for m in models:
            e = g[m] - g.y; mae = e.abs().mean()
            t, pv = dm_hln(e.values, en.values, h) if m != "Naive" else (np.nan, np.nan)
            rows.append(dict(item_id=it, step=h, model=m, mae=mae, relMAE=mae / mae_n if mae_n > 0 else np.nan,
                             MASE=mae / sc if sc and sc > 0 else np.nan, dm=t, p=pv, n=len(g)))
    per = pd.DataFrame(rows).merge(strata, on="item_id")
    out = []
    for grp in list(strata.eval_stratum.unique()) + ["ALL"]:
        s = per if grp == "ALL" else per[per.eval_stratum == grp]
        for (m, h), g in s.groupby(["model", "step"]):
            r = g.relMAE.replace([np.inf], np.nan).dropna(); r = r[r > 0]
            padj = holm(g.p.values) if m != "Naive" else np.full(len(g), np.nan)
            sig = padj < 0.05
            out.append(dict(eval_stratum=grp, model=m, step=h, gmean_relMAE=float(np.exp(np.log(r).mean())) if len(r) else np.nan,
                            win_rate=float((r < 1).mean()) if len(r) else np.nan, median_MASE=g.MASE.median(), n_items=len(r),
                            better=float((sig & (g.dm.values < 0)).sum()), worse=float((sig & (g.dm.values > 0)).sum())))
    return per, pd.DataFrame(out)
