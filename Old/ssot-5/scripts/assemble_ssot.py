#!/usr/bin/env python3
import json, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / "build.manifest.json").read_text(encoding="utf-8"))
out_path = root / manifest["output"]
sep = manifest.get("separator", "\n\n---\n\n")

parts = []
for rel in manifest["order"]:
    p = root / rel
    if not p.exists():
        print(f"[assemble] MISSING: {rel}", file=sys.stderr)
        continue
    text = p.read_text(encoding="utf-8").rstrip()
    parts.append(text)

compiled = sep.join(parts) + "\n"
out_path.write_text(compiled, encoding="utf-8")
print(f"[assemble] Wrote {out_path}")
