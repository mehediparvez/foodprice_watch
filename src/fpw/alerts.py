"""Alert rules on real-time h=7 predictions (S07). All quantities at date t use only residuals whose target date <= t."""
import glob, numpy as np, pandas as pd
from .io import ROOT, panel, raw, CFG
from scipy import stats
def preds():
    P = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(ROOT / "outputs/07_alerts/pred/refit_*.parquet")))])
    p = panel()[["item_id", "report_idx", "Date", "log_price", "eval_stratum", "short_history"]]
    P = P.merge(p.rename(columns={"report_idx": "target", "log_price": "lp_target"}), on=["item_id", "target"], how="inner")
    P["expected"] = P.lp_origin + P.pred; P["resid"] = P.lp_target - P.expected
    return P.sort_values(["item_id", "target"]).reset_index(drop=True)
def bounds(P, levels=(0.9, 0.95, 0.975, 0.99), window=120, floor=0.01):
    """Trailing per-item conformal quantiles of residuals known before the target date (target - 7 report days, i.e. available at origin)."""
    out = P.copy(); g = out.groupby("item_id").resid
    # residual of target s is known at report s; at origin o we may use residuals with target <= o  -> shift by 7 rows within item (rows are report days)
    lagged = g.shift(7)
    for lv in levels:
        out[f"q{int(lv*1000)}"] = lagged.groupby(out.item_id).transform(lambda s: s.rolling(window, min_periods=30).quantile(lv))
    out["q050"] = lagged.groupby(out.item_id).transform(lambda s: s.rolling(window, min_periods=30).quantile(0.05))
    med = lagged.groupby(out.item_id).transform(lambda s: s.rolling(window, min_periods=30).median())
    mad = (lagged - med).abs().groupby(out.item_id).transform(lambda s: s.rolling(window, min_periods=30).median()) * 1.4826
    out["z"] = (out.resid - med) / np.maximum(mad, floor)
    return out
def persist(flag, item, k=3, m=5):
    f = flag.astype(float).groupby(item).transform(lambda s: s.rolling(m, min_periods=1).sum()) >= k
    return f
def episodes(df, col):
    """Start rows of alert runs (alert on, previous row off) per item."""
    on = df[col].fillna(False).astype(bool); prev = on.groupby(df.item_id).shift(1, fill_value=False)
    return df[on & ~prev][["item_id", "Date", "target"]]
def events():
    e = pd.read_csv(raw("shock_events.csv"))
    e = e[e.in_window.astype(str).str.lower() == "true"].copy()
    for c in ["onset", "news_peak", "end"]: e[c] = pd.to_datetime(e[c])
    return e
def item_of_product(prod):
    p = panel()[["Product", "item_id"]].drop_duplicates()
    return list(p[p.Product == prod].item_id)
def windows(ev, before=14, after=30):
    rows = []
    for r in ev.itertuples():
        for it in item_of_product(r.product):
            rows.append(dict(event_id=r.event_id, product=r.product, item_id=it, onset=r.onset, news_peak=r.news_peak, end=r.end, confidence=r.confidence,
                             w0=r.onset - pd.Timedelta(days=before), w1=max(r.news_peak, r.onset) + pd.Timedelta(days=after)))
    return pd.DataFrame(rows)
def in_any_window(df, W):
    m = pd.Series(False, index=df.index)
    for r in W.itertuples(): m |= (df.item_id == r.item_id) & df.Date.between(r.w0, r.w1)
    return m
def fa_per_item_year(df, col, W, period):
    d = df[df.Date.between(*period)].copy(); d["inwin"] = in_any_window(d, W)
    ep = episodes(d, col); ep = ep.merge(d[["item_id", "Date", "inwin"]], on=["item_id", "Date"])
    nonev = d[~d.inwin]; years = nonev.groupby("item_id").Date.agg(lambda s: s.nunique()) / 250.0     # ~250 report days per year
    fa = ep[~ep.inwin].groupby("item_id").size().reindex(years.index, fill_value=0)
    return float(fa.sum() / years.sum()), fa, years
def kupiec(n_exc, n, p):
    if n == 0: return np.nan
    x = n_exc; ph = x / n
    if x in (0, n): ll1 = 0.0
    else: ll1 = x * np.log(ph) + (n - x) * np.log(1 - ph)
    ll0 = x * np.log(p) + (n - x) * np.log(1 - p); lr = -2 * (ll0 - ll1); return float(stats.chi2.sf(lr, 1))
