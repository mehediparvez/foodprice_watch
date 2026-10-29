"""Atomic writes, per-unit done-markers and a test seal, so a dropped session resumes, not restarts."""
import hashlib, json, os, subprocess, time
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def _git(*args) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()

def atomic_write_parquet(df, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)                      # never leaves a half file that looks complete

def marker_path(out: Path) -> Path:
    return out.parent / (out.name + "._SUCCESS.json")

def is_done(out: Path) -> bool:
    m = marker_path(out)
    if not (out.exists() and m.exists()):
        return False
    return json.loads(m.read_text()).get("sha256") == sha256(out)

def mark_done(out: Path, *, inputs: dict, config_hash: str, seed: int, rows: int):
    payload = {"output": str(out), "sha256": sha256(out), "inputs": inputs, "config_hash": config_hash,
               "seed": seed, "rows": rows, "code_commit": _git("rev-parse", "HEAD"),
               "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    tmp = marker_path(out).with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2))
    os.replace(tmp, marker_path(out))

def run_unit(out: Path, compute, **meta):
    """compute() -> DataFrame. Skips if a valid marker exists."""
    if is_done(out):
        return "skipped"
    df = compute()
    atomic_write_parquet(df, out)
    mark_done(out, rows=len(df), **meta)
    return "done"

def unseal_test(stage: str, prereg: Path, seal_dir: Path = Path("state/seals"), limit: int = 1):
    """Call once before scoring the test period. Refuses if the pre-registration is not committed
    or if the stage's test was already unsealed `limit` times. A resumed session re-uses the
    existing seal (same prereg hash) instead of counting a new unsealing."""
    if _git("status", "--porcelain", str(prereg)) or not _git("log", "-1", "--format=%H", "--", str(prereg)):
        raise RuntimeError(f"{prereg} must be committed before unsealing the test for {stage}")
    seal_dir.mkdir(parents=True, exist_ok=True)
    seal = seal_dir / f"{stage}.json"
    h = sha256(prereg)
    rec = json.loads(seal.read_text()) if seal.exists() else {"unsealings": []}
    if any(u["prereg_sha256"] == h for u in rec["unsealings"]):
        return "resumed"                       # same plan; a drop mid-test does not count twice
    if len(rec["unsealings"]) >= limit:
        raise RuntimeError(f"Test for {stage} already unsealed; needs an approved DEVIATIONS.md entry")
    rec["unsealings"].append({"prereg_sha256": h, "commit": _git("rev-parse", "HEAD"),
                              "at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    tmp = seal.with_suffix(".tmp"); tmp.write_text(json.dumps(rec, indent=2)); os.replace(tmp, seal)
    return "unsealed"
