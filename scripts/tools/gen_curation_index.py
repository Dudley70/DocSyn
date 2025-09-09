#!/usr/bin/env python3
import argparse, json, os, re, sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple

FM_RE = re.compile(r"(?s)^\s*---\s*(.*?)\s*---\s*")
H1_RE = re.compile(r"(?m)^\s*#\s+(.+?)\s*$")

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="strict")

def parse_front_matter(text: str) -> Dict[str, any]:
    m = FM_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if ":" not in line: continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"\'')
    # crude list parser for tags
    if "tags" in out and out["tags"].startswith("[") and out["tags"].endswith("]"):
        tags = [t.strip(" '\"\t") for t in out["tags"][1:-1].split(",") if t.strip()]
        out["tags"] = tags
    return out

def strip_front_matter(text: str) -> str:
    m = FM_RE.match(text)
    return text[m.end():] if m else text

def first_h1(text: str) -> Optional[str]:
    m = H1_RE.search(text)
    return m.group(1).strip() if m else None

def words_count(s: str) -> int:
    return len(re.findall(r"\b\w+\b", s, flags=re.UNICODE))

def is_vendor(fm: Dict[str, any]) -> bool:
    pol = (fm.get("policy") or "").lower()
    tags = [t.lower() for t in (fm.get("tags") or [])]
    return pol == "vendor-specific" or "vendor" in tags

def section_label(fm: Dict[str, any], path: Path) -> str:
    if "part" in fm:
        return f"Part {fm['part'].strip()}"
    if "blueprint" in fm:
        return f"Blueprint: {fm['blueprint'].strip()}"
    # fallback from path
    parts = path.parts
    if "core" in parts: return "Part A"
    if "blueprints" in parts: return f"Blueprint: {path.stem}"
    return "—"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="build.manifest.json")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="core/95-curation-index.md")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    man_path = root / args.manifest
    if not man_path.exists():
        print(f"[error] manifest not found: {man_path}", file=sys.stderr)
        return 2
    manifest = json.loads(read_text(man_path))
    curated = manifest.get("curated_sources") or []
    if not curated:
        print("[error] curated_sources is empty", file=sys.stderr)
        return 3

    rows = []
    for idx, rel in enumerate(curated, start=1):
        p = (root / rel).resolve()
        if not p.exists():
            print(f"[error] curated path missing: {rel}", file=sys.stderr)
            return 4
        txt = read_text(p)
        fm = parse_front_matter(txt)
        body = strip_front_matter(txt)
        title = first_h1(body) or p.stem.replace("-", " ").replace("_", " ")
        sec = section_label(fm, p.relative_to(root))
        vendor = "Vendor" if is_vendor(fm) else "Neutral"
        size_b = p.stat().st_size
        size_kb = f"{size_b/1024:.1f}"
        words = words_count(body)
        rows.append((idx, sec, title, rel, vendor, size_kb, words))

    # deterministic markdown (no timestamps; stable ordering = manifest order)
    out_path = root / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# Curated Sources Index\n")
    lines.append("_This index is generated deterministically from `build.manifest.json`._\n")
    lines.append("| # | Section | Title | Path | Policy | Size (KB) | Words |")
    lines.append("|:-:|:--|:--|:--|:--:|--:|--:|")
    for r in rows:
        idx, sec, title, rel, vendor, size_kb, words = r
        # escape pipes in title
        title = title.replace("|", "\\|")
        lines.append(f"| {idx} | {sec} | {title} | `{rel}` | {vendor} | {size_kb} | {words} |")
    # trailing newline
    content = "\n".join(lines) + "\n"
    out_path.write_text(content, encoding="utf-8", errors="strict")
    print(f"[ok] wrote {out_path.relative_to(root)} ({len(rows)} entries)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
