"""S07 step B: choose the operating point on 2024 non-event periods ONLY, then write prereg_S07.yaml (commit before scoring)."""
import sys, yaml, json
sys.path.insert(0, "src")
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from fpw.alerts import preds, bounds, persist, events, windows, fa_per_item_year
from fpw.io import ROOT, CFG
TARGET_FA = 2.0          # pre-registered: at most 2 false-alarm episodes per item-year in 2024 non-event periods
P = bounds(preds()); W = windows(events())
res = {}
for lv in [0.9, 0.95, 0.975, 0.99]:
    q = f"q{int(lv*1000)}"; P["a"] = persist(P.resid > P[q], P.item_id, 3, 5) & P[q].notna()
    fa, _, _ = fa_per_item_year(P, "a", W, (pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31"))); res[lv] = fa
ok = [lv for lv, fa in res.items() if fa <= TARGET_FA]; chosen = min(ok) if ok else 0.99
pre = dict(stage="S07", written="2026-10-29", expected_price="real-time LightGBM M1 (core + mapped forecasting groups G1..G5), h = 7 report days, refit every 30 report days, origins from 2023-06-01 (horizon h=7 so the bound for day t is set one week earlier)",
    interval="per-item trailing conformal quantiles of past h=7 log residuals (window 120 report days, min 30), residuals usable only once their target date has passed",
    primary_rule=dict(name="conformal_upper", level=chosen, persistence="3 of 5 report days", fa_target_per_item_year=TARGET_FA, fa_2024_by_level=res),
    secondary_rule=dict(name="robust_z_ladder", z="(resid - trailing median) / max(1.4826*MAD, 0.01)", bands=dict(stress=1, alert=2, crisis=3), persistence="3 of 5", headline_band="alert (z>=2)"),
    baselines=dict(ALPS_style="per item: OLS log price on linear trend + month dummies, expanding (real-time) refit monthly; z = residual / residual sd; alert z>=1, crisis z>=2; 3-of-5 persistence on daily data",
                   IFPA_style="monthly means; IFPA = 0.4*z(CQGR) + 0.6*z(CAGR), z standardized over each item's expanding history (all months pooled: too few years for calendar-month standardization); abnormal >= 1; flag applies from month end"),
    event_scoring=dict(events="12 in-window shocks (16 event-product rows) from shock_events.csv", window_days=dict(before_onset=14, after_peak=30),
        detected="an alert episode starts inside the window", lead_days="news_peak minus first alert date in window (calendar and report days)",
        periods=dict(in_sample_for_threshold="2023-06-01..2024-12-31", clean_test="2025-01-01..2026-10-24"),
        false_alarms="alert episodes starting outside every labelled window of that item, per item-year of non-event report days (250 report days = 1 year)",
        pr_curve="vary conformal level and z band; precision = share of alert episodes inside labelled windows, among items with at least one labelled event"),
    calibration=dict(coverage="share of residuals <= upper bound (q950) and inside [q050, q950], per stratum; pinball at 0.9/0.95; Winkler 90%; Kupiec on non-event periods for q950"),
    caveat="labels cover only 12 episodes; many real rises are unlabelled, so 'false alarm' means 'outside a labelled window'")
(ROOT / "state/prereg_S07.yaml").write_text(yaml.safe_dump(pre, sort_keys=False)); print(json.dumps(res), "chosen", chosen)
