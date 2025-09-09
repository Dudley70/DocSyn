#!/usr/bin/env python3
import argparse, json, os, re, sys
from pathlib import Path

def count_words(text: str) -> int:
    # Unicode-friendly word split; deterministic
    return len(re.findall(r"\w+", text, flags=re.UNICODE))

def count_headings(lines):
    h1 = sum(1 for l in lines if l.startswith("# "))
    h2 = sum(1 for l in lines if l.startswith("## "))
    h3 = sum(1 for l in lines if l.startswith("### "))
    return h1, h2, h3

def curated_count(manifest_path: Path) -> int:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return len(data.get("curated_sources", []))
    except Exception:
        return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to dist/DocSyn_Compiled.md")
    ap.add_argument("--manifest", default="build.manifest.json", help="Manifest JSON")
    args = ap.parse_args()

    md_path = Path(args.input)
    if not md_path.exists():
        print(f"ERROR: not found: {md_path}", file=sys.stderr)
        sys.exit(2)

    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    size = md_path.stat().st_size
    words = count_words(text)
    h1, h2, h3 = count_headings(lines)
    curated = curated_count(Path(args.manifest))

    # Deterministic, newline-delimited key:value output
    print(f"path:{md_path}")
    print(f"bytes:{size}")
    print(f"words:{words}")
    print(f"headings_h1:{h1}")
    print(f"headings_h2:{h2}")
    print(f"headings_h3:{h3}")
    print(f"curated_sources:{curated}")

if __name__ == "__main__":
    main()
