#!/usr/bin/env python3
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
router = ROOT/"core/00-router.md"
bp_dir = ROOT/"blueprints"

if not router.exists():
    print("Router missing"); sys.exit(1)

text = router.read_text(encoding="utf-8")
rows = [r for r in text.splitlines() if r.strip().startswith("|") and "Intent" not in r]
ok = True
if len(rows) < 3:
    print("[fail] router has too few routes")
    ok = False

# ensure referenced routes exist as blueprint files (by rough mapping)
route_map = {
    "CH4-BP-DOC": "documenter.md",
    "CH4-BP-GRD": "guardian.md",
    "CH4-BP-JAN": "janitor.md",
    "CH4-BP-TST": "tester.md",
    "CH4-BP-CICD": "cicd-analyst.md",
    "CH4-BP-ORCH": "orchestrator.md",
    "CH4-BP-ADAPT": "adaptive-learning.md"
}
for code, f in route_map.items():
    if code in text:
        if not (bp_dir/f).exists():
            print(f"[fail] route {code} -> missing {f}")
            ok = False

print("Router smoke test:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 2)
