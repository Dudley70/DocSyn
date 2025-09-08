#!/usr/bin/env python3
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ssot-13" / "build.manifest.json"

def main():
    if not MANIFEST.exists():
        print("ERROR: build.manifest.json not found.")
        sys.exit(2)
    mf = json.loads(MANIFEST.read_text(encoding="utf-8"))
    curated = mf.get("curated_files", [])
    missing = []
    for src in curated:
        p = ROOT / "ssot-13" / src
        if not p.exists():
            missing.append(src)
    if missing:
        print("ERROR: Missing curated files:")
        for m in missing:
            print(" -", m)
        sys.exit(2)
    print("OK: All curated files present.")
if __name__ == "__main__":
    main()
