"""S11 Results pack: RESULTS_REGISTER.md (every table with provenance) and reports/README.md (index by RQ).
Optional: python src/stages/s11.py --rerun-diff   (clean re-run of the LightGBM stages on a copy and exact diff of T5, T7, T9)."""
import sys, subprocess, hashlib, json, shutil, time
sys.path.insert(0, "src")
import pandas as pd, numpy as np
from fpw.state import ROOT, load, start
start("S11")
def git(*a): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
PRODUCER = {"T1": ("S01", "python src/stages/s01.py"), "T1_late_starters": ("S01", "python src/stages/s01.py"), "T3": ("S04", "python src/stages/s04.py"),
    "T4": ("S06", "python src/stages/s06_score.py"), "T5": ("S06", "python src/stages/s06_score.py"), "T5b": ("S06", "python src/stages/s06_score.py"),
    "T6": ("S07", "python src/stages/s07_score.py"), "T7": ("S07", "python src/stages/s07_score.py"), "T7_event_level": ("S07", "python src/stages/s07_score.py"),
    "T8": ("S07", "python src/stages/s07_score.py"), "T8b_precision_recall": ("S07", "python src/stages/s07_score.py"), "T9": ("S09", "python src/stages/s09_score.py"),
    "T9b_sign_checks": ("S09", "python src/stages/s09_score.py"), "T9c_shap_importance": ("S09", "python src/stages/s09_score.py"), "T9_shap_by_episode": ("S09", "python src/stages/s09_score.py"),
    "T10": ("S09", "python src/stages/s09_score.py"), "T11": ("S10", "python src/stages/s10.py")}
RQ = {"Data": ["T1", "T1_late_starters", "T3", "F1", "F2"], "RQ1 Benchmark": ["T4", "F3"], "RQ2 Driver value": ["T5", "T5b", "F4"],
      "RQ3 Alerts": ["T6", "T7", "T7_event_level", "T8", "T8b_precision_recall", "F5", "F6", "F7"], "RQ4 Explanation": ["T9", "T9b_sign_checks", "T9c_shap_importance", "T9_shap_by_episode", "T10", "F8", "F9"],
      "Robustness": ["T11"], "RQ5 Locate": [], "Data validation (audit, external cross-checks)": []}
commit = git("rev-parse", "--short", "HEAD"); led = {s["id"]: s for s in load()["stages"]}
L = [f"# Results register\n", f"Generated {time.strftime('%Y-%m-%d %H:%M')} at commit `{commit}`. Every number in reports/ comes from the table below it; each table lists the command that produced it.",
     "Numbers not in this register were not produced by this project. Author: see config.yaml (TO_CONFIRM means no name is used).\n",
     "## Stage status\n", "| stage | title | status | notes |", "|---|---|---|---|"]
for s in led.values(): L.append(f"| {s['id']} | {s['title']} | {s['status']} | {s['notes'].replace('|', '/')} |")
s05 = ROOT / "outputs/05_baseline/repro_diff_ALL.csv"
if s05.exists():
    d = pd.read_csv(s05); L += ["\n## S05 baseline reproduction (ALL stratum)\n", f"File `outputs/05_baseline/repro_diff_ALL.csv` · command `python src/stages/s05_score.py` · sha `{sha(s05)}`\n",
        d.round(4).to_markdown(index=False), f"\nMax |difference| in gmean relMAE: {d['diff'].abs().max():.4f} (tolerance 0.02)."]
for t in sorted((ROOT / "reports/tables").glob("*.csv")):
    k = t.stem; stg, cmd = PRODUCER.get(k, ("?", "?")); df = pd.read_csv(t)
    L += [f"\n## {k}\n", f"File `reports/tables/{t.name}` · stage {stg} · command `{cmd}` · rows {len(df)} · sha `{sha(t)}` · stage commit `{led.get(stg, {}).get('git_commit') or commit}`\n"]
    show = df if len(df) <= 60 else df.head(60)
    L.append(show.round(4).to_markdown(index=False)); 
    if len(df) > 60: L.append(f"\n(first 60 of {len(df)} rows; full table in the CSV)")
(ROOT / "reports/RESULTS_REGISTER.md").write_text("\n".join(L))
R = ["# Results pack index\n", "Tables are in `tables/`, figures in `figures/`. Write the report from these; every number is in `RESULTS_REGISTER.md`.\n"]
for rq, items in RQ.items():
    R.append(f"## {rq}\n")
    if not items: R.append("- Not produced: " + ("S08 blocked (WFP data not supplied)." if "Locate" in rq else "S02/S03 blocked (original TCB files and external datasets not supplied).")); continue
    for it in items:
        if it.startswith("F"):
            f = list((ROOT / "reports/figures").glob(f"{it}_*.png")); R.append(f"- {it}: " + (f"`figures/{f[0].name}`" if f else "missing"))
        else:
            R.append(f"- {it}: `tables/{it}.csv`" + ("" if (ROOT / f"reports/tables/{it}.csv").exists() else " (missing)"))
    R.append("")
R += ["## Open items carried into the report\n", "- See `DECISIONS.md` (defaults awaiting confirmation) and `DEVIATIONS.md` (every change from SPEC.md)."]
(ROOT / "reports/README.md").write_text("\n".join(R)); print("wrote RESULTS_REGISTER.md and README.md")
if "--rerun-diff" in sys.argv:
    dst = ROOT.parent / (ROOT.name + "_rerun")
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("06_lgbm", "07_alerts", "09_explain"))
    for c in ["s06_run.py", "s06_score.py", "s07_run.py", "s07_score.py", "s09_run.py", "s09_score.py"]:
        subprocess.run([sys.executable, "-W", "ignore", f"src/stages/{c}"], cwd=dst, check=True, env={**__import__("os").environ, "PYTHONPATH": "src"})
    out = []
    for t in ["T4", "T5", "T5b", "T7", "T8", "T9", "T10"]:
        a, b = pd.read_csv(ROOT / f"reports/tables/{t}.csv"), pd.read_csv(dst / f"reports/tables/{t}.csv")
        same = a.shape == b.shape and all((a[c].astype(str) == b[c].astype(str)).all() if a[c].dtype == object else np.allclose(a[c].fillna(-9e9), b[c].fillna(-9e9), atol=1e-9) for c in a.columns)
        out.append(dict(table=t, identical=bool(same)))
    pd.DataFrame(out).to_csv(ROOT / "reports/rerun_diff.csv", index=False); print(pd.DataFrame(out))
