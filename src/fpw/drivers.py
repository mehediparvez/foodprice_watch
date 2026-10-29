"""Driver loaders with availability dates (data rules 13-28). Each returns (date_or_period, value, available_date)."""
import numpy as np, pandas as pd
from .io import raw, CFG
AV = CFG["availability"]
def imf():
    hdr = pd.read_csv(raw("imf_commodity_prices.csv"), nrows=0).columns
    df = pd.read_csv(raw("imf_commodity_prices.csv"), skiprows=4, header=None)
    df.columns = [f"{c}" for c in hdr]                         # duplicated POILAPSP -> pandas auto-suffix .1
    df = df.rename(columns={"Commodity": "period"})
    df["month"] = pd.PeriodIndex(df.period.str.replace("M", "-"), freq="M").to_timestamp()
    df = df.drop(columns="period")
    for c in ["PTOMATO", "PAPPLE"]:
        if c in df: df[c] = df[c].replace(0, np.nan)
    df["available"] = df.month + pd.offsets.MonthEnd(0) + pd.Timedelta(days=AV["monthly_world_after_month_end"])
    return df
def fao():
    df = pd.read_csv(raw("fao_food_price_index.csv"), skiprows=1)
    df["month"] = pd.to_datetime(df.Date + "-01"); df = df.drop(columns="Date")
    df["available"] = df.month + pd.offsets.MonthEnd(0) + pd.Timedelta(days=AV["monthly_world_after_month_end"])
    return df
def fx():
    y = pd.read_csv(raw("yahoo_bdt_per_usd.csv"), parse_dates=["Date"]).rename(columns={"Date": "date", "bdt_per_usd": "yahoo"})
    n = pd.read_csv(raw("usd_cross_rates_npm_2024_2026.csv"), parse_dates=["date"])[["date", "bdt_per_usd"]].rename(columns={"bdt_per_usd": "npm"})
    d = y.merge(n, on="date", how="outer").sort_values("date")
    cut = pd.Timestamp(CFG["fx_splice"]["npm_from"])
    d["bdt_per_usd"] = np.where(d.date >= cut, d.npm, d.yahoo * CFG["fx_splice"]["yahoo_scale"])
    d = d.dropna(subset=["bdt_per_usd"]); d["available"] = d.date
    return d
def brent():
    b = pd.read_csv(raw("fred_DCOILBRENTEU.csv"), parse_dates=["observation_date"]).rename(columns={"observation_date": "date", "DCOILBRENTEU": "brent"})
    b["brent"] = pd.to_numeric(b.brent, errors="coerce"); b = b.dropna(); b["available"] = b.date; return b
def comtrade(rule_days=None):
    c = pd.read_csv(raw("bd_food_imports_mirror_comtrade_monthly_agg.csv"), dtype={"hs_code": str})
    c["hs_code"] = c.hs_code.str.zfill(4)                                  # rule 13
    c.loc[c.period >= CFG["comtrade_blank_from"], ["tonnes", "fob_kusd", "india_tonnes"]] = np.nan
    c["month"] = pd.to_datetime(c.period.astype(str), format="%Y%m")
    c["unit_value"] = np.where(c.tonnes > 0, c.fob_kusd * 1000 / c.tonnes, np.nan)   # rule 26
    c["flag_zero_tonnes"] = c.tonnes.eq(0)
    lag = AV["comtrade_after_month_start"] if rule_days is None else rule_days
    c["available"] = c.month + pd.Timedelta(days=lag)                       # rule 25
    return c
def weather():
    lines = raw("weather_open_meteo_13_locations_2019_2026.csv").read_text(encoding="utf-8").splitlines()
    k = [i for i, l in enumerate(lines) if l.startswith("location_id,time")][0]
    from io import StringIO
    w = pd.read_csv(StringIO("\n".join(lines[k:])), parse_dates=["time"])
    w = w[w.time < w.time.max()]                                            # rule 16: drop incomplete last day
    w.columns = [c.split(" (")[0] for c in w.columns]
    return w
def events(name):
    return pd.read_csv(raw(name), encoding="utf-8-sig")                     # rule 19
