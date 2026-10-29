"""S00 intake (idempotent): copy inbox files into data/raw/, hash them into MANIFEST.csv, set blocked stages for missing data.
Never edits data/raw/ files that already exist."""
import sys, csv, hashlib, shutil
from pathlib import Path
sys.path.insert(0, "src")
from fpw.state import ROOT, update, load
EXPECTED = ["TCB_Dhaka_Daily_Prices_2021-2026.xlsx", "audit_candidates.csv", "audit_sample_2pct.csv", "baseline_results_by_group.csv", "bb_fx_reserves_monthly.csv",
    "bb_remittance_monthly.csv", "bd_cyclones_floods.csv", "bd_disruption_events.csv", "bd_fishing_bans.csv", "bd_food_imports_mirror_comtrade_monthly_agg.csv",
    "bd_food_price_shocks.csv", "bd_fuel_price_events.csv", "bd_import_duty_changes.csv", "bd_import_figures_from_secondary_sources.csv", "bd_political_wage_events.csv",
    "bd_public_holidays_2019_2027.csv", "bd_ramadan_eid.csv", "corrections.csv", "exporter_policy_events.csv", "fao_food_price_index.csv", "fred_DCOILBRENTEU.csv",
    "fred_DEXCHUS.csv", "fred_DEXINUS.csv", "fred_DEXMAUS.csv", "imf_commodity_prices.csv", "item_meta.csv", "shock_events.csv", "tcb_dhaka_daily_prices_2021_2026.csv",
    "usd_cross_rates_npm_2024_2026.csv", "weather_open_meteo_13_locations_2019_2026.csv", "wti_daily_datahub.csv", "yahoo_bdt_per_usd.csv"]
EXTERNAL = ["wfp/wfp_food_prices_bgd.csv", "wfp/wfp_markets_bgd.csv", "agripricebd/chickpea.csv", "agripricebd/cucumber.csv", "agripricebd/garlic.csv",
    "agripricebd/green_chilli.csv", "agripricebd/sweet_pumpkin.csv", "pinksheet/CMO-Historical-Data-Monthly.xlsx", "ohlc/Food Commodity Price OHLC Dataset of Bangladesh.csv"]
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inbox, raw = ROOT / "inbox", ROOT / "data/raw"
log = {}
if (inbox / "SOURCES_LOG.txt").exists():
    for line in (inbox / "SOURCES_LOG.txt").read_text().splitlines():
        if ":" in line: k, v = line.split(":", 1); log[k.strip()] = v.strip()
rows = []
for name in EXPECTED:
    src, dst = inbox / "project" / name, raw / "project" / name
    if not dst.exists() and src.exists(): dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); print("copied", name)
    rows.append(dict(path=str(dst.relative_to(ROOT)), source="project file", retrieved_at=log.get(name, "unknown"), bytes=dst.stat().st_size if dst.exists() else "",
                     sha256=h(dst) if dst.exists() else "", status="present" if dst.exists() else "MISSING"))
for name in EXTERNAL:
    src, dst = inbox / "external" / name, raw / "external" / name
    if not dst.exists() and src.exists(): dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); print("copied", name)
    rows.append(dict(path=str(dst.relative_to(ROOT)), source="user-held external", retrieved_at=log.get(name, "unknown"), bytes=dst.stat().st_size if dst.exists() else "",
                     sha256=h(dst) if dst.exists() else "", status="present" if dst.exists() else "MISSING"))
orig = list((inbox / "tcb_originals").glob("*")) if (inbox / "tcb_originals").exists() else []
man = raw / "MANIFEST.csv"; man.parent.mkdir(parents=True, exist_ok=True)
with open(man, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
missing = [r["path"] for r in rows if r["status"] == "MISSING"]
print(f"MANIFEST: {sum(r['status']=='present' for r in rows)} present, {len(missing)} missing")
for m in missing: print("  MISSING", m)
if any(r["status"] == "MISSING" and r["source"] == "project file" for r in rows):
    print("STOP: core project files missing. Put them in inbox/project/ and re-run this cell."); sys.exit(1)
st = {s["id"]: s["status"] for s in load()["stages"]}
if not orig and st["S02"] == "pending": update("S02", status="blocked", notes="blocked: original TCB files not supplied (inbox/tcb_originals/ empty)")
if any("wfp/" in m for m in missing) and st["S03"] == "pending":
    update("S03", status="blocked", notes="blocked: WFP/AgriPriceBD/Pink Sheet/OHLC not supplied"); update("S08", status="blocked", notes="blocked: needs S03 WFP data")
