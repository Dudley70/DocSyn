#!/usr/bin/env python3
"""
Simple router smoke test.
- Parses core/00-router.md for the routing matrix.
- Runs sample queries through positive/negative pattern checks.
- Exits nonzero if any query fails to match a row.
"""
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
router_md = (root / "core" / "00-router.md").read_text(encoding="utf-8")

# Parse markdown table rows (skip header + divider)
lines = [l.strip() for l in router_md.splitlines() if l.strip()]
table = []
in_table = False
for i, l in enumerate(lines):
    if l.startswith("| Intent ") and "| Positive Patterns" in l:
        in_table = True
        continue
    if in_table:
        if l.startswith("|---"):
            continue
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip("|").split("|")]
            if len(cells) >= 7:
                intent, pos_pat, neg_pat, chapter, blueprint, action, risks = cells[:7]
                # extract patterns in backticks
                pos = re.findall(r"`([^`]+)`", pos_pat)
                neg = re.findall(r"`([^`]+)`", neg_pat)
                table.append((intent, pos, neg, chapter, blueprint, action, risks))
        else:
            break

if not table:
    print("Router table not found or empty.", file=sys.stderr)
    sys.exit(2)

# Sample queries for smoke test (can be extended)
samples = [
    ("Generate documentation from a repo", "please summarise the repo docs and README"),
    ("Watch a folder and lint/guard", "need a file watcher to lint changes, guard violations"),
    ("Cleanup repo hygiene", "run janitor to remove dead code and format"),
    ("Automated testing", "kick off unit and integration test with coverage"),
    ("CI/CD security analysis", "scan ci/cd pipeline for secrets, run sast and dast"),
    ("Adaptive learning/self-tuning", "run retrospective and adapt based on feedback"),
    ("Multi-agent orchestration", "plan a multi agent workflow and orchestrate handoffs"),
]

def matches(sample, row):
    intent, pos, neg, *_ = row
    s = sample.lower()
    ok_pos = any(p.lower() in s for p in pos) if pos else False
    bad_neg = any(n.lower() in s for n in neg) if neg else False
    return ok_pos and not bad_neg

failures = []
for label, q in samples:
    matched = None
    for row in table:
        if matches(q, row):
            matched = row
            break
    if not matched:
        failures.append((label, q))

if failures:
    print("Router smoke test FAILURES:")
    for lbl, q in failures:
        print(f" - [{lbl}] no match for: {q}")
    sys.exit(1)

print("Router smoke test PASSED.")
sys.exit(0)
