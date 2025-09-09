#!/usr/bin/env python3
import argparse, json, sys, re
from pathlib import Path
from typing import Dict, List

FM_RE = re.compile(r"(?s)^\s*---\s*(.*?)\s*---\s*")

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="strict")

def parse_fm(text: str) -> Dict[str, any]:
    m = FM_RE.match(text)
    if not m: return {}
    block = m.group(1)
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or ":" not in line: continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"\'')
    if "tags" in out and out["tags"].startswith("[") and out["tags"].endswith("]"):
        out["tags"] = [t.strip(" '\"") for t in out["tags"][1:-1].split(",") if t.strip()]
    return out

def is_vendor(fm: Dict[str, any]) -> bool:
    pol = (fm.get("policy") or "").lower()
    tags = [t.lower() for t in (fm.get("tags") or [])]
    return pol == "vendor-specific" or "vendor" in tags

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="build.manifest.json")
    ap.add_argument("--root", default=".")
    ap.add_argument("--vendor-appendix", default="core/90-appendix-vendors.md")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    man = json.loads(read(root/args.manifest))
    curated = man.get("curated_sources") or []
    if not curated:
        print("[error] curated_sources is empty", file=sys.stderr); return 2

    # existence + duplicates
    seen = set()
    for rel in curated:
        if rel in seen:
            print(f"[error] duplicate curated path: {rel}", file=sys.stderr); return 3
        seen.add(rel)
        p = (root / rel).resolve()
        if not p.exists():
            print(f"[error] curated path missing: {rel}", file=sys.stderr); return 4
        fm = parse_fm(read(p))
        # Note: anchor files are allowed in our architecture as placeholders

    # vendor ordering rule
    vendor_idx = []
    appendix_idx = None
    for i, rel in enumerate(curated):
        p = (root / rel).resolve()
        fm = parse_fm(read(p))
        if rel == args.vendor_appendix:
            appendix_idx = i
        if is_vendor(fm):
            vendor_idx.append(i)

    if vendor_idx and appendix_idx is None:
        print("[error] vendor-specific items curated but vendor appendix missing", file=sys.stderr)
        return 6

    if appendix_idx is not None:
        bad = [i for i in vendor_idx if i <= appendix_idx]
        if bad:
            print(f"[error] vendor items must come *after* {args.vendor_appendix}; bad indices: {bad}", file=sys.stderr)
            return 7

    print("[ok] manifest guard passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
