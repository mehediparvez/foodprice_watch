"""
Add newly converted TCB report days to the existing price CSV.

Run by the user, after tcb_download.py has fetched the new Excel files and the
converter has turned them into a CSV with the same 16 columns as
tcb_dhaka_daily_prices_2021_2026.csv.

    python tools/tcb_append.py --base OLD.csv --new NEW_DAYS.csv --out COMBINED.csv

* Python standard library only.
* Never changes OLD.csv and never overwrites an existing --out file.
* Stops (writes nothing) if the new file disagrees with the old one on a row
  both contain, has a series the old file does not know, or breaks a price rule.
  --allow-new-series lets genuinely new items through.
* Put COMBINED.csv into inbox/ afterwards; S00 intake copies and hashes it.
  A longer panel changes the sample, so log it in DEVIATIONS.md before re-running.
"""
import argparse
import csv
import datetime as dt
import os
import sys

KEY = ("Date", "Product", "Unit")
PRICE = ("Price_Min", "Price_Max", "Price_Avg")


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def num(s):
    s = (s or "").strip()
    return float(s) if s else None


def same(a, b, cols):
    for c in cols:
        x, y = (a[c] or "").strip(), (b[c] or "").strip()
        if x == y:
            continue
        try:
            if abs(float(x) - float(y)) < 1e-9:
                continue
        except ValueError:
            pass
        return False
    return True


def check_rows(rows, label):
    """Return a list of rule violations (empty = fine)."""
    bad, seen = [], set()
    for i, r in enumerate(rows, start=2):
        k = tuple(r[c] for c in KEY)
        try:
            dt.date.fromisoformat(r["Date"])
        except ValueError:
            bad.append(f"{label} line {i}: Date is not YYYY-MM-DD: {r['Date']!r}")
            continue
        if k in seen:
            bad.append(f"{label} line {i}: duplicate row for {k}")
        seen.add(k)
        try:
            lo, hi, av = (num(r[c]) for c in PRICE)
        except ValueError:
            bad.append(f"{label} line {i}: price is not a number for {k}")
            continue
        if (lo is None) != (hi is None) or (lo is None) != (av is None):
            bad.append(f"{label} line {i}: Min/Max/Avg partly missing for {k}")
        elif lo is not None:
            if lo <= 0 or hi <= 0:
                bad.append(f"{label} line {i}: zero or negative price for {k} (store 'not reported' as blank)")
            if lo > hi:
                bad.append(f"{label} line {i}: Min > Max for {k}")
            if abs(av - (lo + hi) / 2) > 0.006:
                bad.append(f"{label} line {i}: Avg is not (Min+Max)/2 for {k}")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="existing price CSV (not modified)")
    ap.add_argument("--new", required=True, help="CSV of newly converted report days")
    ap.add_argument("--out", required=True, help="combined CSV to write (must not exist)")
    ap.add_argument("--allow-new-series", action="store_true", help="accept Product|Unit pairs absent from --base")
    a = ap.parse_args()

    if os.path.exists(a.out):
        sys.exit(f"STOP: {a.out} already exists; choose a new name (earlier files are never overwritten).")
    bh, base = read(a.base)
    nh, new = read(a.new)
    if bh != nh:
        sys.exit(f"STOP: column headers differ.\n  base: {bh}\n  new : {nh}")

    problems = check_rows(new, "new")
    base_by_key = {tuple(r[c] for c in KEY): r for r in base}
    base_series = {(r["Product"], r["Unit"]) for r in base}
    base_dates = {r["Date"] for r in base}

    add, identical, conflict = [], 0, []
    for r in new:
        k = tuple(r[c] for c in KEY)
        if k in base_by_key:
            if same(r, base_by_key[k], bh):
                identical += 1
            else:
                conflict.append(k)
        else:
            add.append(r)
    for k in conflict[:20]:
        problems.append(f"conflict: {k} is in both files with different values")
    if len(conflict) > 20:
        problems.append(f"... and {len(conflict) - 20} more conflicts")

    new_series = sorted({(r["Product"], r["Unit"]) for r in add} - base_series)
    if new_series and not a.allow_new_series:
        for s in new_series:
            problems.append(f"unknown series (check the name/unit dictionary, or pass --allow-new-series): {s[0]} | {s[1]}")

    # rows added to a date the base already has = a series that base lacked on that day
    partial = sorted({r["Date"] for r in add} & base_dates)
    if partial:
        problems.append(f"new rows fall on {len(partial)} date(s) already in the base file, e.g. {partial[:5]}: "
                        "an existing report day would change. Check before continuing.")

    if problems:
        print("\n".join(problems))
        sys.exit(f"\nSTOP: {len(problems)} problem(s). Nothing was written.")
    if not add:
        sys.exit(f"Nothing to add: all {identical} rows of the new file are already in the base file.")

    def order(r):
        return (r["Product"], r["Unit"], r["Date"])
    combined = base + add
    if base == sorted(base, key=order):          # keep the base file's ordering if it has one
        combined.sort(key=order)

    tmp = a.out + ".part"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bh, lineterminator="\n")
        w.writeheader()
        w.writerows(combined)
    os.replace(tmp, a.out)

    add_dates = sorted({r["Date"] for r in add})
    all_dates = sorted(base_dates | set(add_dates))
    print(f"base rows            : {len(base)}  ({len(base_dates)} report days, last {max(base_dates)})")
    print(f"rows already present : {identical}")
    print(f"rows added           : {len(add)}  ({len(add_dates)} new report days, {add_dates[0]} to {add_dates[-1]})")
    if new_series:
        print(f"new series accepted  : {len(new_series)}")
    print(f"combined rows        : {len(combined)}  ({len(all_dates)} report days, {all_dates[0]} to {all_dates[-1]})")
    print(f"written              : {a.out}")


if __name__ == "__main__":
    main()
