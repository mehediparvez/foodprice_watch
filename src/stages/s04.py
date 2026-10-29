"""S04 Driver panel: one long item x report-date table with slots G0..G5, E1..E5, has_ flags. Idempotent."""
import sys, json, yaml
sys.path.insert(0, "src")
import numpy as np, pandas as pd
from fpw.io import panel, PROC, CFG, ROOT, raw
from fpw import drivers as D, state
from fpw.checkpoint import sha256
state.start("S04")
MAP = yaml.safe_load((ROOT/"config/item_driver_map.yaml").read_text())
CAP = CFG["carry_cap_days"]
p = panel()[["Date","item_id","Product","eval_stratum","short_history","Price_Avg","gap_2022","report_idx"]].copy()
dates = pd.DataFrame({"Date": sorted(p.Date.unique())})
def asof(src, valcols, cap_days, prefix=""):
    """For each report date: last record with available <= Date, NaN if older than cap (beyond availability). Also returns src availability date."""
    s = src.sort_values("available")[["available", *valcols]].dropna(subset=valcols, how="all")
    out = pd.merge_asof(dates, s, left_on="Date", right_on="available", direction="backward")
    stale = (out.Date - out.available).dt.days > cap_days
    out.loc[stale, valcols] = np.nan
    return out.rename(columns={c: prefix + c for c in valcols} | {"available": prefix + "src_available"})
# ---------- G0 calendar (known in advance)
re_ = D.events("bd_ramadan_eid.csv")
adha = pd.to_datetime(re_.eid_ul_adha.astype(str).str.split(";").explode().str.strip())   # some years have two Eid ul-Adha dates
for c in ["ramadan_start","eid_ul_fitr"]: re_[c] = pd.to_datetime(re_[c])
def days_to_next(ds, ev):
    ev = np.sort(ev.values); idx = np.searchsorted(ev, ds.values)
    nxt = np.where(idx < len(ev), ev[np.minimum(idx, len(ev)-1)], np.datetime64("NaT"))
    return (pd.to_datetime(nxt) - ds).dt.days
cal = dates.copy()
cal["month"] = cal.Date.dt.month; cal["dow"] = cal.Date.dt.dayofweek
cal["days_to_ramadan"] = days_to_next(cal.Date, re_.ramadan_start)
cal["days_to_eid_fitr"] = days_to_next(cal.Date, re_.eid_ul_fitr)
cal["days_to_eid_adha"] = days_to_next(cal.Date, adha)
cal["in_ramadan"] = False
for r in re_.itertuples(): cal.loc[cal.Date.between(r.ramadan_start, r.eid_ul_fitr - pd.Timedelta(days=1)), "in_ramadan"] = True
hol = pd.to_datetime(D.events("bd_public_holidays_2019_2027.csv").date)
cal["holiday_next7"] = [((hol > d) & (hol <= d + pd.Timedelta(days=7))).sum() for d in cal.Date]
cal["days_since_prev_report"] = cal.Date.diff().dt.days
# ---------- world prices (G1, E5)
imf = D.imf()
codes = list(MAP["G1_world_price"]) + list(MAP["E5_world_explain"])
imf_l = imf[["month","available",*codes]].copy()
for c in codes:
    imf_l[c+"_lvl"] = np.log(imf_l[c]); imf_l[c+"_ch3"] = np.log(imf_l[c]).diff(3)
w_asof = asof(imf_l, [f"{c}_{k}" for c in codes for k in ("lvl","ch3")], CAP["monthly"], prefix="")
fao = D.fao(); fao_l = fao[["available"]].assign(fao_oils_lvl=np.log(fao.Oils), fao_cereals_lvl=np.log(fao.Cereals), fao_dairy_lvl=np.log(fao.Dairy))
fao_asof = asof(fao_l, ["fao_oils_lvl","fao_cereals_lvl","fao_dairy_lvl"], CAP["monthly"], prefix="")
# ---------- daily: brent, fx
br = D.brent(); br["brent_lvl"] = np.log(br.brent); br["brent_ch30"] = br.brent_lvl - br.set_index("date").brent_lvl.shift(30, freq="D").reindex(br.date).values
br_asof = asof(br, ["brent_lvl","brent_ch30"], CAP["daily"])
fx = D.fx(); fx["fx_lvl"] = np.log(fx.bdt_per_usd); fx["fx_ch30"] = fx.fx_lvl - fx.set_index("date").fx_lvl.shift(30, freq="D").reindex(fx.date).values
fx_asof = asof(fx, ["fx_lvl","fx_ch30"], CAP["daily"])
# ---------- fuel (event step, effective date)
fu = D.events("bd_fuel_price_events.csv"); fu = fu[fu["product"] == "diesel"].copy()
fu["available"] = pd.to_datetime(fu.date_effective); fu["diesel_bdt"] = fu.new_price_bdt_per_litre.astype(float)
fu_asof = pd.merge_asof(dates, fu[["available","diesel_bdt"]].sort_values("available"), left_on="Date", right_on="available").drop(columns="available")
# ---------- weather (+5 d), candidates aggregated
w = D.weather(); bd = w[w.location_id <= 10].groupby("time").agg(rain=("precipitation_sum","mean"), tmax=("temperature_2m_max","mean"),
        tmean=("temperature_2m_mean","mean"), soilm=("soil_moisture_0_to_7cm_mean","mean"), rh=("relative_humidity_2m_mean","mean"))
nas = w[w.location_id == 12].set_index("time").precipitation_sum.rename("nashik_rain")
bd = bd.join(nas).asfreq("D")
cand = pd.DataFrame({"wx_bd_rain_7d": bd.rain.rolling(7).sum(), "wx_bd_rain_30d": bd.rain.rolling(30).sum(), "wx_bd_tmax_7d": bd.tmax.rolling(7).mean(),
        "wx_bd_tmean_30d": bd.tmean.rolling(30).mean(), "wx_bd_soilm_30d": bd.soilm.rolling(30).mean(), "wx_nashik_rain_30d": bd.nashik_rain.rolling(30).sum()})
cand["available"] = cand.index + pd.Timedelta(days=CFG["availability"]["weather"])
wx_asof = asof(cand.reset_index(drop=True), list(cand.columns.drop("available")), CAP["daily"])
# ---------- assemble long table
F = p.merge(cal, on="Date", how="left")
for t in [w_asof, fao_asof, br_asof, fx_asof, fu_asof, wx_asof]:
    F = F.merge(t.drop(columns=[c for c in t.columns if c.endswith("src_available")] + (["available"] if "available" in t else []), errors="ignore"), on="Date", how="left")
F["log_price"] = np.log(F.Price_Avg)
# slot G1 own_world_price
F["own_world_price"] = np.nan; F["own_world_price_ch3"] = np.nan; F["own_world_code"] = None
for code, items in MAP["G1_world_price"].items():
    m = F.item_id.isin(items); F.loc[m, "own_world_price"] = F.loc[m, f"{code}_lvl"]; F.loc[m, "own_world_price_ch3"] = F.loc[m, f"{code}_ch3"]; F.loc[m, "own_world_code"] = code
F["has_world_price"] = F.own_world_code.notna().astype(int)
F["e5_world_explain"] = np.nan
for code, items in MAP["E5_world_explain"].items():
    m = F.item_id.isin(items); F.loc[m, "e5_world_explain"] = F.loc[m, f"{code}_lvl"]
# slot G2 brent
g2 = F.item_id.isin(MAP["G2_brent"]); F["has_brent"] = g2.astype(int)
F["own_brent"] = np.where(g2, F.brent_lvl, np.nan); F["own_brent_ch30"] = np.where(g2, F.brent_ch30, np.nan)
# slot G3 export measure (onion; India) — event active on report date; out of table coverage = unknown
ex = D.events("exporter_policy_events.csv"); ex["start"] = pd.to_datetime(ex.start); ex["end"] = pd.to_datetime(ex.end)
cov0, cov1 = ex.start.min(), ex.end.max()
def ev_active(items_by_key, keycol, prefix):
    out = pd.Series(np.nan, index=F.index)
    for key, items in items_by_key.items():
        m = F.item_id.isin(items); e = ex[ex[keycol] == key]
        incov = F.Date.between(cov0, cov1)
        act = pd.Series(0.0, index=F.index)
        for r in e.itertuples(): act[F.Date.between(r.start, r.end)] = 1.0
        out[m & incov] = act[m & incov]
    return out
F["own_export_measure"] = ev_active(MAP["G3_export_measure"], "item", "g3"); F["has_export_measure"] = F.item_id.isin(sum(MAP["G3_export_measure"].values(), [])).astype(int)
F["e4_exporter_measure"] = ev_active(MAP["E4_events"]["exporter_items"], "item", "e4")
# slot G4 fishing ban
fb = D.events("bd_fishing_bans.csv"); fb["start"] = pd.to_datetime(fb.start); fb["end"] = pd.to_datetime(fb.end)
g4 = F.item_id.isin(MAP["G4_fishing_ban"]); ban = pd.Series(0.0, index=F.index)
for r in fb.itertuples(): ban[F.Date.between(r.start, r.end)] = 1.0
F["own_fishing_ban"] = np.where(g4, ban, np.nan); F["has_fishing_ban"] = g4.astype(int)
# slot G5 weather: choose <= 3 of the candidates on 2024 only (|Spearman| with 14-report-ahead log change, pooled G5 long-history items)
g5 = F.item_id.isin(MAP["G5_weather"]); F["has_weather"] = g5.astype(int)
F = F.sort_values(["item_id","Date"]); F["fwd14"] = F.groupby("item_id").log_price.shift(-14) - F.log_price
sel = F[g5 & (F.Date.dt.year == 2024) & ~F.short_history]
wxc = [c for c in cand.columns if c != "available"]
scores = {c: abs(sel[[c,"fwd14"]].dropna().corr(method="spearman").iloc[0,1]) for c in wxc}
chosen = sorted(scores, key=scores.get, reverse=True)[:CFG["weather_max_features"]]
for i, c in enumerate(chosen, 1): F[f"weather_{i}"] = np.where(g5, F[c], np.nan)
# E1 FX, E3 imports, E4 events
F["e1_fx"] = np.where(F.eval_stratum.isin(MAP["E1_fx_strata"]), F.fx_lvl, np.nan); F["e1_fx_ch30"] = np.where(F.eval_stratum.isin(MAP["E1_fx_strata"]), F.fx_ch30, np.nan)
F["e2_diesel"] = np.log(F.diesel_bdt)
ct = D.comtrade(); F["e3_imports_log_t"] = np.nan; F["e3_unit_value"] = np.nan; F["e3_src_month"] = pd.NaT
for hs, items in MAP["E3_imports_hs"].items():
    s = ct[ct.hs_code == hs][["available","tonnes","unit_value","month"]].sort_values("available")
    a = pd.merge_asof(dates, s, left_on="Date", right_on="available")
    stale = (a.Date - a.available).dt.days > CAP["monthly"]; a.loc[stale, ["tonnes","unit_value","month"]] = np.nan
    a["lt"] = np.log1p(a.tonnes)
    m = F.item_id.isin(items); mm = F.loc[m, ["Date"]].merge(a[["Date","lt","unit_value","month"]], on="Date", how="left")
    F.loc[m, "e3_imports_log_t"] = mm["lt"].values; F.loc[m, "e3_unit_value"] = mm.unit_value.values; F.loc[m, "e3_src_month"] = mm.month.values
F["has_imports"] = F.item_id.isin(sum(MAP["E3_imports_hs"].values(), [])).astype(int)
dis = D.events("bd_disruption_events.csv"); dis["start"] = pd.to_datetime(dis.start); dis["end"] = pd.to_datetime(dis.end)
F["e4_disruption"] = np.where(F.Date.between(dis.start.min(), dis.end.max()), 0.0, np.nan)
for r in dis.itertuples(): F.loc[F.Date.between(r.start, r.end), "e4_disruption"] = np.maximum(F.loc[F.Date.between(r.start, r.end), "e4_disruption"].fillna(0), r.intensity)
cy = D.events("bd_cyclones_floods.csv"); cy["start"] = pd.to_datetime(cy.start); cy["end"] = pd.to_datetime(cy.end)
F["e4_cyclone_flood"] = 0.0
for r in cy.itertuples(): F.loc[F.Date.between(r.start, r.end + pd.Timedelta(days=14)), "e4_cyclone_flood"] = 1.0
du = D.events("bd_import_duty_changes.csv"); du["start"] = pd.to_datetime(du.start); du["end"] = pd.to_datetime(du.end)
F["e4_duty_cut"] = np.nan
for key, items in MAP["E4_events"]["duty_items"].items():
    m = F.item_id.isin(items) & F.Date.between(du.start.min(), du.end.max()); F.loc[m, "e4_duty_cut"] = 0.0
    for r in du[du["item"] == key].itertuples(): F.loc[F.item_id.isin(items) & F.Date.between(r.start, r.end), "e4_duty_cut"] = 1.0
pw = D.events("bd_political_wage_events.csv"); reg = pw[pw.group == "regime"].copy(); reg["start"] = pd.to_datetime(reg.start); reg["end"] = pd.to_datetime(reg.end)
F["e4_regime_interim"] = 0.0
for r in reg[reg.feature == "regime_interim"].itertuples(): F.loc[F.Date.between(r.start, r.end), "e4_regime_interim"] = 1.0
# drop helper columns, keep slots only
keep = ["Date","item_id","Product","eval_stratum","short_history","gap_2022","report_idx","Price_Avg","log_price","month","dow","days_to_ramadan","days_to_eid_fitr",
        "days_to_eid_adha","in_ramadan","holiday_next7","days_since_prev_report","own_world_price","own_world_price_ch3","own_world_code","has_world_price","own_brent","own_brent_ch30",
        "has_brent","own_export_measure","has_export_measure","own_fishing_ban","has_fishing_ban","weather_1","weather_2","weather_3","has_weather","e1_fx","e1_fx_ch30","e2_diesel",
        "e3_imports_log_t","e3_unit_value","e3_src_month","has_imports","e4_exporter_measure","e4_disruption","e4_cyclone_flood","e4_duty_cut","e4_regime_interim","e5_world_explain",
        "fao_oils_lvl","fao_cereals_lvl","fao_dairy_lvl"]
F = F[keep].sort_values(["item_id","Date"]).reset_index(drop=True)
num = F.select_dtypes("number"); assert np.isfinite(num.fillna(0)).all().all(), "inf in features"
out = PROC/"features.parquet"; tmp = out.with_suffix(".parquet.tmp"); F.to_parquet(tmp, index=False); tmp.replace(out)
meta = {"weather_candidates_abs_spearman_2024": scores, "weather_chosen": chosen, "comtrade_lag_days": CFG["availability"]["comtrade_after_month_start"],
        "comtrade_lag_evidence": "File fetched 2026-10-26 (SOURCES); months from 2026-05 incomplete, so 2026-04 is the latest complete month at fetch: 2026-04-01 + 208 d = 2026-10-26."}
(ROOT/"config/s04_frozen.json").write_text(json.dumps(meta, indent=2)); print(json.dumps(meta, indent=1))
# T3 driver inventory
inv = [("G0 calendar","forecast+explain","Ramadan/Eid, holidays, month, dow","daily (known ahead)","0","n/a"),
 ("G1 own_world_price","forecast+explain","IMF PSOIL/PPOIL/PWHEAMT/PRICENPQ/PMILK (log USD, 3m change)","monthly","month end + 40 d",f"{CAP['monthly']} d"),
 ("G2 own_brent","forecast+explain","FRED Brent (log, 30d change)","daily","as of date",f"{CAP['daily']} d"),
 ("G3 own_export_measure","forecast+explain","India onion duty/MEP/ban (reconstructed)","event","start date","coverage only"),
 ("G4 own_fishing_ban","forecast+explain","hilsa 22-day, jatka, marine bans","event","announced dates","n/a"),
 ("G5 weather_1..3","forecast+explain","chosen on 2024: "+", ".join(chosen),"daily","+5 d",f"{CAP['daily']} d"),
 ("E1 fx","explain","BDT/USD spliced (npm from 2024-03-02, Yahoo x1.0151 before)","daily","as of date",f"{CAP['daily']} d"),
 ("E2 diesel","explain","diesel administered price","event","effective date","n/a"),
 ("E3 imports","explain","Comtrade mirror tonnes + unit value by HS","monthly","month start + 208 d",f"{CAP['monthly']} d"),
 ("E4 events","explain","exporter measures (rice/wheat/sugar/palm), disruptions, cyclones/floods +14 d, duty cuts, interim regime","event","event dates","out of coverage = NaN"),
 ("E5 world (explain)","explain","IMF PSUGAISA (sugar), PCHANA (chickpea)","monthly","month end + 40 d",f"{CAP['monthly']} d")]
T3 = pd.DataFrame(inv, columns=["slot","role","source","frequency","availability","carry_cap"])
cov = []
for s, col in [("G1 own_world_price","own_world_price"),("G2 own_brent","own_brent"),("G3 own_export_measure","own_export_measure"),("G4 own_fishing_ban","own_fishing_ban"),("G5 weather_1..3","weather_1"),
               ("E1 fx","e1_fx"),("E2 diesel","e2_diesel"),("E3 imports","e3_imports_log_t"),("E4 events","e4_disruption"),("E5 world (explain)","e5_world_explain")]:
    x = F[F[col].notna()]; cov.append((s, x.item_id.nunique(), str(x.Date.min().date()) if len(x) else "", str(x.Date.max().date()) if len(x) else ""))
cov = pd.DataFrame(cov, columns=["slot","n_items","first_date","last_date"]); T3 = T3.merge(cov, on="slot", how="left")
T3.to_csv(ROOT/"reports/tables/T3.csv", index=False); print(T3[["slot","n_items","first_date","last_date"]].to_string())
