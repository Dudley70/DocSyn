#!/usr/bin/env python3
import json, sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT/"build.manifest.json"
OUT = ROOT/"SSOT.md"

def read(p: Path):
    try: return p.read_text(encoding="utf-8")
    except: return p.read_text(errors="ignore")

def main():
    if not MANIFEST.exists():
        print("No build.manifest.json"); sys.exit(1)
    mani = json.loads(MANIFEST.read_text(encoding="utf-8"))
    parts = []
    for rel in mani.get("sections", []):
        p = ROOT / rel
        if not p.exists():
            print(f"[warn] missing: {rel}")
            continue
        if p.name.endswith(".SOURCED.md"):
            continue
        parts.append(read(p).strip())
    body = "\n\n---\n\n".join(parts) + "\n"
    OUT.write_text(body, encoding="utf-8")
    print("Assembled", OUT)
if __name__ == "__main__":
    main()
