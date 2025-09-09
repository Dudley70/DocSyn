#!/usr/bin/env python3
import argparse, sys, pathlib, re, datetime, unicodedata

FM_OPEN = re.compile(r'^\s*---\s*$')
FM_CLOSE = re.compile(r'^\s*---\s*$')

def slugify(name: str) -> str:
    s = unicodedata.normalize('NFKD', name)
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-')
    return s.lower()

def detect_existing_fm(text: str):
    lines = text.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i >= len(lines) or not FM_OPEN.match(lines[i]):
        return False, None, None
    start = i
    i += 1
    while i < len(lines) and not FM_CLOSE.match(lines[i]):
        i += 1
    if i >= len(lines):
        return False, None, None
    end = i  # index of closing fence line
    return True, start, end

def build_front_matter(args, src_path: pathlib.Path, assumed_blueprint: str):
    retrieved = args.retrieved or datetime.date.today().isoformat()
    owner = args.owner
    tags = args.tags
    if args.part_a:
        body = [
            "---",
            f"source: {args.source}",
            f"retrieved: {retrieved}",
            f"owner: {owner}",
            f"tags: [{tags}]",
            "part: A",
            "---",
            "",
        ]
    else:
        blueprint = args.blueprint or assumed_blueprint or "_triage"
        body = [
            "---",
            f"source: {args.source}",
            f"retrieved: {retrieved}",
            f"owner: {owner}",
            f"tags: [{tags}]",
            f"blueprint: {blueprint}",
            "---",
            "",
        ]
    return "\n".join(body)

def main():
    ap = argparse.ArgumentParser(description="Create corrected copies adding YAML front-matter (no in-place edits).")
    ap.add_argument("roots", nargs="*", default=["merge_pr/updated", "sources/raw"],
                    help="Directories to scan.")
    ap.add_argument("--out", default="dist/fixed_front_matter", help="Output directory for fixed copies.")
    ap.add_argument("--owner", default="curation-team")
    ap.add_argument("--tags", default="imported")
    ap.add_argument("--source", default="user-supplied documents")
    ap.add_argument("--retrieved", default=None, help="YYYY-MM-DD; default= today.")
    ap.add_argument("--blueprint", default=None, help="Force a blueprint for all files (overrides inference).")
    ap.add_argument("--part-a", action="store_true", help="Mark all as part: A (global).")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be created.")
    args = ap.parse_args()

    roots = [pathlib.Path(r) for r in args.roots]
    md_files = []
    for root in roots:
        if root.exists():
            md_files += list(root.rglob("*.md"))

    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    fixed = 0
    skipped = 0

    for f in sorted(md_files):
        text = f.read_text(encoding="utf-8", errors="replace")
        has_fm, fm_start, fm_end = detect_existing_fm(text)
        if has_fm:
            skipped += 1
            continue

        # infer blueprint from path if present: merge_pr/updated/<slug>/file.md
        assumed = None
        try:
            parts = f.parts
            if "merge_pr" in parts and "updated" in parts:
                idx = parts.index("updated")
                if idx + 1 < len(parts):
                    bp_candidate = parts[idx + 1]
                    if bp_candidate not in ("_triage",):
                        assumed = slugify(bp_candidate)
        except Exception:
            pass

        fm = build_front_matter(args, f, assumed)
        new_text = fm + text

        # write to mirrored path under outdir
        rel = None
        for root in roots:
            try:
                rel = f.relative_to(root)
                break
            except ValueError:
                continue
        rel = rel if rel is not None else f.name
        dst = outdir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        if args.dry_run:
            print(f"[DRY] would write: {dst}")
        else:
            dst.write_text(new_text, encoding="utf-8")
            print(f"wrote: {dst}")
        fixed += 1

    print(f"\nSummary: fixed={fixed}, skipped(existing FM)={skipped}, outdir={outdir}")
    if args.dry_run and fixed == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
