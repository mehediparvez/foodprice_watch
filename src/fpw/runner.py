"""Run one stage the way the Colab notebook does: `python -m fpw.runner S01 [--dry]` (or `make stage S=S01`).

Skips done/blocked/skipped stages, refuses to start before its dependencies are done, runs each resumable
command, then finalizes (acceptance tests -> ledger -> PROGRESS.md -> commit). Standard library only.
"""
import subprocess, sys
from .paths import ROOT
from .registry import STAGES
from . import state


def sh(cmd: str) -> int:
    print(f"\n$ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, cwd=ROOT).returncode


def git_commit(msg: str):
    subprocess.run("git add -A", shell=True, cwd=ROOT)
    subprocess.run(["git", "commit", "-qm", msg], cwd=ROOT)       # no-op when nothing changed


def plan(sid: str):
    """The commands this stage would run now (used by --dry and by run)."""
    spec = STAGES[sid]
    steps = list(spec.get("before", []))
    if "prereg" in spec and not (ROOT / spec["prereg"][1]).exists():
        steps += [spec["prereg"][0], f"git add -A && git commit -qm '{spec['prereg_commit']}' || true"]
    return steps + list(spec["run"]) + [f"python src/stages/finalize.py {sid} {spec.get('note', '')}".strip()]


def run(sid: str, dry: bool = False) -> int:
    if sid not in STAGES:
        print(f"{sid}: not a runnable stage here (S02/S03/S08 have no code yet; S12-S14 optional; S99 is a fresh-session review)")
        return 2
    led = {s["id"]: s for s in state.load()["stages"]}
    st = led[sid]["status"]
    if st in ("done", "skipped"):
        print(f"{sid} already {st} - nothing to do"); return 0
    if st == "blocked":
        print(f"{sid} is blocked: {led[sid]['notes']}"); return 1
    waiting = [d for d in led[sid]["depends_on"] if led[d]["status"] not in ("done", "skipped")]
    if waiting:
        print(f"{sid} depends on {waiting}, which are not done"); return 1
    for cmd in plan(sid):
        if dry:
            print("DRY:", cmd); continue
        if sh(cmd) != 0:
            print(f"STOP: {sid} failed at: {cmd}"); return 1
        if sid == "S00" and cmd.endswith("s00_intake.py"):
            git_commit(STAGES[sid]["commit"])
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit("usage: python -m fpw.runner S01 [--dry]")
    sys.exit(run(args[0].upper() if args[0][0].lower() == "s" else f"S{int(args[0]):02d}", dry="--dry" in sys.argv))
