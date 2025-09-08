#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "merge_pr" / "report.json"
changed, skipped, apply = [], [], False
if REPORT.exists():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    changed = data.get("changed", []); skipped = data.get("skipped", []); apply = data.get("apply", False)
ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
print(f"""# SSOT Structured Merge — Pull Request

## Summary
Structured merge from SOURCED excerpts into blueprints (auto-prepared on {ts}).

## Merge Report (auto)
- Report file: `merge_pr/report.json`
- Patches: `merge_pr/patches/`
- Proposed files: `merge_pr/updated/`

```json
{{
  "changed": {json.dumps(changed)},
  "skipped": {json.dumps(skipped)},
  "apply": {str(apply).lower()}
}}
```
""")
