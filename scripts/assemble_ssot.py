#!/usr/bin/env python3
import argparse, json, re, sys, unicodedata
from pathlib import Path
from datetime import datetime

GLOBAL_UNIQUE = [
  "Query-Pattern Matrix",
  "Unified Risk & Control Model",
  "Standard Development Environment",
  "Agent Query Index",
]

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def normalize(md: str) -> str:
    md = re.sub(r"\n{3,}", "\n\n", md)
    if not md.endswith("\n"):
        md += "\n"
    return md

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="build.manifest.json")
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()

    root = Path(".").resolve()
    manifest_path = root / args.manifest
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(2)

    try:
        manifest = json.loads(read_text(manifest_path))
    except Exception as e:
        print(f"ERROR: manifest parse failed: {e}", file=sys.stderr)
        sys.exit(2)

    sources = manifest.get("curated_sources") or manifest.get("sections") or []
    if not isinstance(sources, list) or not sources:
        print("ERROR: No sources configured. Expected 'curated_sources' (preferred) or 'sections' (legacy).", file=sys.stderr)
        sys.exit(3)

    # Sort sources for deterministic ordering
    sources = sorted(sources)

    # Partition sources
    def is_core(p): return "/core/" in p or p.startswith("core/")
    def is_bp(p):   return "/blueprints/" in p or p.startswith("blueprints/")
    # Sort paths for deterministic ordering
    core_paths = sorted([root / p for p in sources if is_core(p)])
    bp_paths = sorted([root / p for p in sources if is_bp(p)])

    # Build strings
    partA = "\n\n".join(read_text(p) for p in core_paths if p.exists())
    partB = "\n\n---\n\n".join(read_text(p) for p in bp_paths if p.exists())

    if not partA.strip() and not partB.strip():
        print("ERROR: Sources resolved but files are empty/missing. Check paths in manifest.", file=sys.stderr)
        sys.exit(4)

    banner = f"# DocSyn Compiled Knowledge\n\n"
    ssot = normalize(banner + partA + "\n---\n\n" + partB)

    # Deduplicate consecutive identical H1s
    out_lines, prev_h = [], None
    for ln in ssot.splitlines():
        m = re.match(r"^#\s+(.+)$", ln)
        if m:
            h = m.group(1).strip().lower()
            if h == prev_h:
                continue
            prev_h = h
        out_lines.append(ln)
    ssot = "\n".join(out_lines) + "\n"
    
    # Normalize Unicode for cross-platform consistency
    ssot = unicodedata.normalize("NFC", ssot)

    outdir = root / args.out
    outdir.mkdir(parents=True, exist_ok=True)

    (outdir / "PartA_Core.md").write_text(partA, encoding="utf-8")
    (outdir / "PartB_Blueprints.md").write_text(partB, encoding="utf-8")
    (outdir / "DocSyn_Compiled.md").write_text(ssot, encoding="utf-8")

    fence_count = ssot.count("```")
    unique_counts = {g: len(re.findall(rf"^#.*{re.escape(g)}", ssot, flags=re.M|re.I)) for g in GLOBAL_UNIQUE}
    report = f"""Built {outdir / 'DocSyn_Compiled.md'}
- code fences: {fence_count} ({'even' if fence_count % 2 == 0 else 'ODD'})
- globals in SSOT: {unique_counts}
"""
    (outdir / "BUILD_REPORT.txt").write_text(report, encoding="utf-8")
    print(report)

if __name__ == "__main__":
    sys.exit(main())