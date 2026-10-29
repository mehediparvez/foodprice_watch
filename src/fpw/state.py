"""Ledger helpers: update only status fields of state/stages.json (atomic)."""
import json, os, time
from pathlib import Path
from .checkpoint import sha256
ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "state/stages.json"
ALLOWED = {"status","started_at","last_unit","units_done","output_sha256","git_commit","finished_at","notes"}
def load(): return json.loads(LEDGER.read_text())
def save(d):
    tmp = LEDGER.with_suffix(".tmp"); tmp.write_text(json.dumps(d, indent=2)); os.replace(tmp, LEDGER)
def stage(d, sid): return next(s for s in d["stages"] if s["id"] == sid)
def update(sid, **kw):
    assert set(kw) <= ALLOWED, set(kw) - ALLOWED
    d = load(); s = stage(d, sid); s.update(kw); save(d)
def start(sid):
    d = load(); s = stage(d, sid)
    if s["status"] != "in_progress":
        s["status"] = "in_progress"; s["started_at"] = s["started_at"] or time.strftime("%Y-%m-%dT%H:%M:%S")
    save(d)
def finish(sid, outputs, notes=None, status="done"):
    d = load(); s = stage(d, sid)
    s["output_sha256"] = {o: sha256(ROOT / o) for o in outputs}
    s["status"] = status; s["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    if notes is not None: s["notes"] = notes
    save(d)
