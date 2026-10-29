import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parents[1]
def _commit_time(path):
    out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", path], cwd=R, capture_output=True, text=True).stdout.strip(); return out
def test_seals_after_prereg_commit():
    for s in (R/"state/seals").glob("S*.json"):
        rec = json.loads(s.read_text()); assert len(rec["unsealings"]) == 1, f"{s.name} unsealed {len(rec['unsealings'])}x"
        pre = R/f"state/prereg_{s.stem}.yaml"; assert pre.exists() and _commit_time(f"state/prereg_{s.stem}.yaml"), "prereg not committed"
        import hashlib; assert rec["unsealings"][0]["prereg_sha256"] == hashlib.sha256(pre.read_bytes()).hexdigest(), "prereg changed after unsealing"
