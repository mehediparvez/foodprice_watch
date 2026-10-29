"""S06 step 4: score test predictions. T4 (RQ1), T5 (driver value), T5b (placebo gap), F3, F4."""
import sys, glob, yaml
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fpw.bench import wide, score, dm_hln, holm, H
from fpw.io import ROOT, item_meta, CFG
pre = yaml.safe_load((ROOT / "state/prereg_S06.yaml").read_text())
y = wide(); strata = item_meta()[["item_id", "eval_stratum"]]
L = []
for f in sorted(glob.glob(str(ROOT / "outputs/06_lgbm/*.parquet"))):
    v = f.split("/")[-1].split("__")[0]; d = pd.read_parquet(f); d["variant"] = v; L.append(d)
L = pd.concat(L); L["fc"] = np.exp(L.lp + L.pred); L["naive"] = np.exp(L.lp)
W = L.pivot_table(index=["item_id", "cutoff", "step"], columns="variant", values="fc").reset_index()
W["Naive"] = L[L.variant == "core"].set_index(["item_id", "cutoff", "step"]).naive.reindex(pd.MultiIndex.from_frame(W[["item_id", "cutoff", "step"]])).values
# classical from S05
C = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(ROOT / "outputs/05_baseline/test/cut_*.parquet")))])
C = C[C.step.isin(H)]                      # keep statsforecast Naive: exact last price (exp(log) adds ~1e-13 noise)
A = W.drop(columns=["Naive"]).merge(C, on=["item_id", "cutoff", "step"], how="left").rename(columns={"core": "LGBM_core", "M1_all": "LGBM_M1"})
from fpw.io import panel
p = panel(); gap = p.loc[p.gap_2022, "report_idx"]; tr = y.ffill().loc[:808]; dd = tr.diff().abs(); dd.loc[(dd.index >= gap.min()) & (dd.index <= gap.max() + 1)] = np.nan
scale = dd.mean().to_dict()
models = ["Naive", "SeasonalNaive", "WindowAverage", "RWD", "AutoARIMA", "AutoETS", "AutoTheta", "LGBM_core", "LGBM_M1"]
per, grp = score(A, y, models, strata, scale)
grp.to_csv(ROOT / "reports/tables/T4.csv", index=False); per.to_csv(ROOT / "outputs/06_lgbm/per_item_T4.csv", index=False)
print(grp[grp.eval_stratum == "ALL"].pivot(index="model", columns="step", values="gmean_relMAE").round(3))
print(grp[grp.eval_stratum == "ALL"].pivot(index="model", columns="step", values="better"), grp[grp.eval_stratum == "ALL"].pivot(index="model", columns="step", values="worse"))
# ---- T5 / T5b
A["target_idx"] = A.cutoff + A.step; yy = y.stack().rename("y").reset_index(); yy.columns = ["target_idx", "item_id", "y"]
E = A.merge(yy, on=["target_idx", "item_id"])
rng = np.random.default_rng(CFG["seed"])
def boot(x, n=2000):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return (np.nan, np.nan)
    b = rng.choice(x, size=(n, len(x)), replace=True).mean(1); return (float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)))
rows, gaprows = [], []
for g in pre["driver_group_order"]:
    mapped = set(pre["mapped_items"][g]) & set(y.columns); plac = [d["item"] for d in pre["placebo_assignment"][g]]
    for h in H:
        for kind, items, var in [("matched", mapped, g), ("placebo", plac, f"placebo_{g}")]:
            sub = E[E.item_id.isin(items) & (E.step == h)]
            recs = []
            for it, s in sub.groupby("item_id"):
                en = (s.Naive - s.y).abs().mean()
                if en <= 0: continue
                ec, ev = (s.LGBM_core - s.y).abs().mean(), (s[var] - s.y).abs().mean()
                t, pv = dm_hln((s[var] - s.y).values, (s.LGBM_core - s.y).values, h)
                recs.append(dict(group=g, kind=kind, item_id=it, step=h, relMAE_core=ec / en, relMAE_variant=ev / en, delta_relMAE=ev / en - ec / en, dm=t, p=pv,
                                 relMAE_variant_vs_naive_lt1=ev / en < 1))
            R = pd.DataFrame(recs)
            if len(R): R["p_holm"] = holm(R.p.values); R["sig_better_than_core"] = (R.p_holm < 0.05) & (R.dm < 0); R["sig_worse_than_core"] = (R.p_holm < 0.05) & (R.dm > 0); rows.append(R)
        M = rows[-2] if len(rows) >= 2 else pd.DataFrame(); Pp = rows[-1]
        if len(M) and len(Pp) and M.group.iloc[0] == g and M.kind.iloc[0] == "matched" and M.step.iloc[0] == h and Pp.kind.iloc[0] == "placebo" and Pp.step.iloc[0] == h and Pp.group.iloc[0] == g:
            gapv = M.delta_relMAE.mean() - Pp.delta_relMAE.mean()
            bm = rng.choice(M.delta_relMAE.values, (2000, len(M))).mean(1); bp = rng.choice(Pp.delta_relMAE.values, (2000, len(Pp))).mean(1); bg = bm - bp
            gaprows.append(dict(group=g, step=h, n_matched=len(M), n_placebo=len(Pp), mean_delta_matched=M.delta_relMAE.mean(), ci_matched=boot(M.delta_relMAE),
                                mean_delta_placebo=Pp.delta_relMAE.mean(), ci_placebo=boot(Pp.delta_relMAE), gap=gapv, gap_ci=(float(np.percentile(bg, 2.5)), float(np.percentile(bg, 97.5))),
                                n_sig_better_matched=int(M.sig_better_than_core.sum()), n_sig_better_placebo=int(Pp.sig_better_than_core.sum()),
                                share_beats_naive_matched=float(M.relMAE_variant_vs_naive_lt1.mean()), share_beats_naive_placebo=float(Pp.relMAE_variant_vs_naive_lt1.mean())))
T5 = pd.concat(rows); T5.to_csv(ROOT / "reports/tables/T5.csv", index=False)
T5b = pd.DataFrame(gaprows); T5b.to_csv(ROOT / "reports/tables/T5b.csv", index=False)
print(T5b[["group", "step", "n_matched", "mean_delta_matched", "mean_delta_placebo", "gap", "gap_ci", "n_sig_better_matched", "n_sig_better_placebo"]].round(4).to_string())
# ---- F3
G = grp[grp.eval_stratum != "ALL"]; strat = sorted(G.eval_stratum.unique())
fig, axes = plt.subplots(1, len(strat), figsize=(3 * len(strat), 3.2), sharey=True)
for ax, s in zip(axes, strat):
    for m in ["AutoETS", "AutoARIMA", "LGBM_core", "LGBM_M1"]:
        g2 = G[(G.eval_stratum == s) & (G.model == m)].sort_values("step"); ax.plot(g2.step, g2.gmean_relMAE, "o-", label=m, ms=3)
    ax.axhline(1, c="0.4", lw=.8, ls="--"); ax.set_title(s.replace("_", " "), fontsize=8); ax.set_xticks(H); ax.set_xlabel("h (report days)", fontsize=7)
axes[0].set_ylabel("gmean relMAE vs naive"); axes[-1].legend(fontsize=7, frameon=False); fig.suptitle("F3. Error relative to naive by stratum and horizon (test 2025-26)", fontsize=9); fig.tight_layout()
fig.savefig(ROOT / "reports/figures/F3_relmae_by_horizon.png", dpi=150)
# ---- F4
fig, ax = plt.subplots(figsize=(8, 3.6)); xs = np.arange(len(T5b))
ax.bar(xs - .18, T5b.mean_delta_matched, .36, label="matched items"); ax.bar(xs + .18, T5b.mean_delta_placebo, .36, label="placebo items", color="0.7")
ax.axhline(0, c="k", lw=.8); ax.set_xticks(xs); ax.set_xticklabels([f"{g}\nh{h}" for g, h in zip(T5b.group, T5b.step)], fontsize=7)
ax.set_ylabel("Δ relMAE (group − core)\n<0 = group helps"); ax.set_title("F4. Value of each driver group beyond the core model", fontsize=9); ax.legend(frameon=False, fontsize=8); fig.tight_layout()
fig.savefig(ROOT / "reports/figures/F4_driver_value.png", dpi=150)
