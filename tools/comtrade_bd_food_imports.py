#!/usr/bin/env python3
"""
Download monthly UN Comtrade data on Bangladesh's essential food (and steel scrap)
imports, 2019-2026, into a tidy CSV. Uses the Python standard library only (no pip).

Two pulls:
  1. DIRECT : reporter = Bangladesh (50), flow = M (imports), all partners.
              (Bangladesh is an infrequent Comtrade reporter, so expect few or no rows.)
  2. MIRROR : reporters = main exporters (India 699, Myanmar 104, ...),
              partner = Bangladesh (50), flow = X (exports). This is the
              main usable source.

Endpoints (UN Comtrade API v1):
  * No key  : https://comtradeapi.un.org/public/v1/preview/C/M/HS
              - max 500 rows per call, ONE period per call, no daily quota
                published, but throttles ("try again in N seconds").
  * Free key: https://comtradeapi.un.org/data/v1/get/C/M/HS
              - register at https://comtradeplus.un.org (free "comtrade - v1"
                product), 500 calls/day, up to 100,000 rows/call,
                up to 12 periods per call.
              Set the key with:  set COMTRADE_KEY=xxxxxxxx   (Windows)
                                 export COMTRADE_KEY=xxxxxxxx (Linux/macOS)

Usage:
  python comtrade_bd_food_imports.py                 # full run -> CSV
  python comtrade_bd_food_imports.py --dry-run       # only print URLs
  python comtrade_bd_food_imports.py --start 2023-01 --end 2023-12
  python comtrade_bd_food_imports.py --only mirror
  python comtrade_bd_food_imports.py --test-parse sample.json

The output CSV is appended to as each call finishes, and a cache directory keeps
the raw JSON responses. If you run the script again it skips calls that are
already cached, so you can stop it and restart it.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_PREVIEW = "https://comtradeapi.un.org/public/v1/preview/C/M/HS"
BASE_KEYED = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

BANGLADESH = 50

# HS codes requested (HS4 headings). Comtrade accepts comma-separated cmdCode.
HS_CODES = {
    "1006": "Rice",
    "1001": "Wheat and meslin",
    "1101": "Wheat or meslin flour",
    "0713": "Dried leguminous vegetables (lentils, pulses)",
    "0703": "Onions, shallots, garlic, leeks",
    "0701": "Potatoes, fresh or chilled",
    "0910": "Ginger, saffron, turmeric, etc.",
    "0904": "Pepper; dried capsicum/chilli",
    "0906": "Cinnamon",
    "0907": "Cloves",
    "0908": "Nutmeg, mace, cardamoms",
    "0909": "Seeds of anise, coriander, cumin, etc.",
    "1507": "Soya-bean oil",
    "1511": "Palm oil",
    "1701": "Cane or beet sugar",
    "0402": "Milk and cream, concentrated (milk powder)",
    "0804": "Dates, figs, pineapples, etc.",
    "0407": "Birds' eggs, in shell",
    "1005": "Maize (corn)",
    "2304": "Soybean oilcake/meal",
    "7204": "Ferrous waste and scrap",
}

# Main exporters to Bangladesh (UN M49 codes as used by Comtrade).
# NB: Comtrade uses 699 for India, 842 for USA, 251 for France.
MIRROR_REPORTERS = {
    699: "India",
    104: "Myanmar",
    156: "China",
    36: "Australia",
    124: "Canada",
    360: "Indonesia",
    458: "Malaysia",
    76: "Brazil",
    32: "Argentina",
    804: "Ukraine",
    643: "Russian Federation",
    842: "USA",
    764: "Thailand",
    704: "Viet Nam",
    586: "Pakistan",
    702: "Singapore",
    682: "Saudi Arabia",
    784: "United Arab Emirates",
    554: "New Zealand",
    792: "Turkiye",
    398: "Kazakhstan",
    368: "Iraq",
    818: "Egypt",
    528: "Netherlands",
    251: "France",
}

# Split HS codes into groups so preview calls stay under 500 rows.
HS_GROUPS = [
    ["1006", "1001", "1101", "1005", "2304", "7204"],
    ["0713", "0703", "0701", "0407", "0402", "0804"],
    ["0910", "0904", "0906", "0907", "0908", "0909"],
    ["1507", "1511", "1701"],
]

PREVIEW_ROW_CAP = 500
SLEEP_BETWEEN_CALLS = 2.0  # seconds; the preview endpoint throttles quickly
MAX_RETRIES = 6

CSV_FIELDS = [
    "period", "reporter_code", "reporter", "partner_code", "partner",
    "flow", "hs", "hs_desc", "qty_kg", "qty", "qty_unit", "value_usd",
    "cif_usd", "fob_usd", "source", "is_reported",
]


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def month_range(start, end):
    """'2019-01','2019-03' -> ['201901','201902','201903']"""
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    out = []
    while (y, m) <= (ey, em):
        out.append("%04d%02d" % (y, m))
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return out


def build_url(periods, reporters, partners, flow, cmd_codes, key=None):
    """Build a Comtrade v1 URL. The query parameter names follow the
    comtradeapicall package / Comtrade developer portal."""
    params = {
        "reporterCode": ",".join(str(r) for r in reporters),
        "period": ",".join(periods),
        "cmdCode": ",".join(cmd_codes),
        "flowCode": flow,
        "partner2Code": "0",      # World only (no second partner breakdown)
        "customsCode": "C00",     # TOTAL customs procedure
        "motCode": "0",           # TOTAL mode of transport
        "includeDesc": "true",
    }
    if partners is not None:
        params["partnerCode"] = ",".join(str(p) for p in partners)
    if key:
        params["maxRecords"] = "100000"
        base = BASE_KEYED
    else:
        params["maxRecords"] = str(PREVIEW_ROW_CAP)
        base = BASE_PREVIEW
    return base + "?" + urllib.parse.urlencode(params, safe=",")


def fetch_json(url, key=None):
    headers = {"User-Agent": "bd-food-imports/1.0 (research script)",
               "Accept": "application/json"}
    if key:
        headers["Ocp-Apim-Subscription-Key"] = key
    delay = 3.0
    for attempt in range(1, MAX_RETRIES + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            if e.code in (429, 500, 502, 503, 504):
                print("  HTTP %s, retry %d in %.0fs: %s" % (e.code, attempt, delay, body),
                      file=sys.stderr)
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("HTTP %s for %s\n%s" % (e.code, url, body))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print("  network error, retry %d in %.0fs: %s" % (attempt, delay, e), file=sys.stderr)
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("Giving up after %d retries: %s" % (MAX_RETRIES, url))


def _num(x):
    if x is None or x == "":
        return ""
    try:
        f = float(x)
        return int(f) if f.is_integer() else f
    except (TypeError, ValueError):
        return ""


def parse_rows(payload, source):
    """Turn a Comtrade v1 JSON response into tidy dict rows."""
    if payload is None:
        return []
    if payload.get("error"):
        print("  API error: %s" % payload.get("error"), file=sys.stderr)
    rows = []
    for r in payload.get("data") or []:
        # Skip any breakdown rows that slipped through (we want totals).
        if str(r.get("partner2Code", 0)) not in ("0", "None"):
            continue
        if r.get("customsCode") not in (None, "C00"):
            continue
        if str(r.get("motCode", 0)) not in ("0", "None"):
            continue
        period = str(r.get("period") or r.get("refPeriodId") or "")
        if len(period) == 6:
            period = period[:4] + "-" + period[4:]
        qty_unit = r.get("qtyUnitAbbr") or r.get("qtyUnitCode")
        rows.append({
            "period": period,
            "reporter_code": r.get("reporterCode"),
            "reporter": r.get("reporterDesc") or r.get("reporterISO") or "",
            "partner_code": r.get("partnerCode"),
            "partner": r.get("partnerDesc") or r.get("partnerISO") or "",
            "flow": r.get("flowCode"),
            "hs": r.get("cmdCode"),
            "hs_desc": HS_CODES.get(str(r.get("cmdCode")), r.get("cmdDesc") or ""),
            "qty_kg": _num(r.get("netWgt")),
            "qty": _num(r.get("qty")),
            "qty_unit": qty_unit if qty_unit is not None else "",
            "value_usd": _num(r.get("primaryValue")),
            "cif_usd": _num(r.get("cifvalue")),
            "fob_usd": _num(r.get("fobvalue")),
            "source": source,
            "is_reported": r.get("isReported", ""),
        })
    return rows


# ----------------------------------------------------------------------------
# Job planning
# ----------------------------------------------------------------------------
def plan_jobs(periods, only, key):
    """Return a list of (label, source, url) jobs."""
    jobs = []
    # The free key accepts up to 12 periods per call; preview accepts 1.
    chunk = 12 if key else 1
    period_chunks = [periods[i:i + chunk] for i in range(0, len(periods), chunk)]
    all_codes = [c for g in HS_GROUPS for c in g]
    mirror_reps = list(MIRROR_REPORTERS)

    for pc in period_chunks:
        tag = pc[0] if len(pc) == 1 else "%s-%s" % (pc[0], pc[-1])
        if only in (None, "direct"):
            groups = [all_codes] if key else HS_GROUPS
            for gi, g in enumerate(groups):
                url = build_url(pc, [BANGLADESH], None, "M", g, key)
                jobs.append(("direct_%s_g%d" % (tag, gi), "direct_BGD_imports", url))
        if only in (None, "mirror"):
            if key:
                # 12 months x 25 reporters x 21 codes ~ 6,300 rows max; fine.
                url = build_url(pc, mirror_reps, [BANGLADESH], "X", all_codes, key)
                jobs.append(("mirror_%s_all" % tag, "mirror_partner_exports", url))
            else:
                for gi, g in enumerate(HS_GROUPS):
                    url = build_url(pc, mirror_reps, [BANGLADESH], "X", g, key)
                    jobs.append(("mirror_%s_g%d" % (tag, gi), "mirror_partner_exports", url))
    return jobs


def split_reporters_url(url):
    """If a preview call hit the 500-row cap, split its reporters in two."""
    parts = urllib.parse.urlsplit(url)
    q = dict(urllib.parse.parse_qsl(parts.query))
    reps = q["reporterCode"].split(",")
    codes = q["cmdCode"].split(",")
    halves = []
    if len(reps) > 1:
        mid = len(reps) // 2
        for sub in (reps[:mid], reps[mid:]):
            q2 = dict(q, reporterCode=",".join(sub))
            halves.append(urllib.parse.urlunsplit(parts._replace(
                query=urllib.parse.urlencode(q2, safe=","))))
    elif len(codes) > 1:
        mid = len(codes) // 2
        for sub in (codes[:mid], codes[mid:]):
            q2 = dict(q, cmdCode=",".join(sub))
            halves.append(urllib.parse.urlunsplit(parts._replace(
                query=urllib.parse.urlencode(q2, safe=","))))
    return halves


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def run(args):
    key = os.environ.get("COMTRADE_KEY", "").strip() or None
    periods = month_range(args.start, args.end)
    jobs = plan_jobs(periods, args.only, key)
    print("Mode: %s | periods: %d | jobs: %d"
          % ("keyed /data/v1/get" if key else "public preview", len(periods), len(jobs)))

    if args.dry_run:
        for label, source, url in jobs:
            print(label, url)
        return

    os.makedirs(args.cache, exist_ok=True)
    new_file = not os.path.exists(args.out)
    out_f = open(args.out, "a", newline="", encoding="utf-8")
    writer = csv.DictWriter(out_f, fieldnames=CSV_FIELDS)
    if new_file:
        writer.writeheader()

    queue = list(jobs)
    total_rows = 0
    n = 0
    while queue:
        label, source, url = queue.pop(0)
        n += 1
        cache_path = os.path.join(args.cache, label + ".json")
        if os.path.exists(cache_path):
            print("[%d] %s cached, skipping" % (n, label))
            continue
        print("[%d/%d+] %s" % (n, len(jobs), label))
        try:
            payload = fetch_json(url, key)
        except RuntimeError as e:
            print("  FAILED: %s" % e, file=sys.stderr)
            continue
        data = payload.get("data") or []
        if not key and len(data) >= PREVIEW_ROW_CAP:
            subs = split_reporters_url(url)
            if subs:
                print("  hit 500-row cap; splitting into %d calls" % len(subs))
                for i, su in enumerate(subs):
                    queue.insert(0, ("%s_s%d" % (label, i), source, su))
                time.sleep(SLEEP_BETWEEN_CALLS)
                continue
            print("  WARNING: 500 rows and cannot split further; data may be truncated",
                  file=sys.stderr)
        rows = parse_rows(payload, source)
        writer.writerows(rows)
        out_f.flush()
        total_rows += len(rows)
        with open(cache_path, "w", encoding="utf-8") as cf:
            json.dump(payload, cf)
        print("  %d rows (total %d)" % (len(rows), total_rows))
        time.sleep(SLEEP_BETWEEN_CALLS)

    out_f.close()
    print("Done. %d rows written to %s" % (total_rows, args.out))
    print("Note: when you re-run, rows are appended. Delete the CSV first, or "
          "remove duplicates by (period, reporter_code, partner_code, flow, hs).")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default="2019-01", help="YYYY-MM (default 2019-01)")
    ap.add_argument("--end", default="2026-12", help="YYYY-MM (default 2026-12)")
    ap.add_argument("--only", choices=["direct", "mirror"], default=None)
    ap.add_argument("--out", default="comtrade_bd_food_imports_monthly.csv")
    ap.add_argument("--cache", default="comtrade_cache")
    ap.add_argument("--dry-run", action="store_true", help="print URLs, no download")
    ap.add_argument("--test-parse", metavar="JSON_FILE",
                    help="parse a saved Comtrade JSON response and print tidy rows")
    args = ap.parse_args()

    if args.test_parse:
        with open(args.test_parse, encoding="utf-8") as f:
            payload = json.load(f)
        w = csv.DictWriter(sys.stdout, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(parse_rows(payload, "test"))
        return
    run(args)


if __name__ == "__main__":
    main()
