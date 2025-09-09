#!/usr/bin/env python3
import argparse, sys, pathlib, re

FM_OPEN = re.compile(r'^\s*---\s*$')
FM_CLOSE = re.compile(r'^\s*---\s*$')

REQUIRED_ONE_OF = [('part', 'blueprint')]  # exactly one must exist

def has_well_formed_front_matter(text: str):
    lines = text.splitlines()
    # skip leading empty lines
    i = 0
    while i < len(lines) and lines[i].strip() == '':
        i += 1
    if i >= len(lines) or not FM_OPEN.match(lines[i]):
        return False, {}
    i += 1
    kv = {}
    while i < len(lines) and not FM_CLOSE.match(lines[i]):
        line = lines[i].strip()
        if line and not line.startswith('#'):
            # very light key: value sniff
            m = re.match(r'^([A-Za-z0-9_-]+)\s*:\s*(.*)$', line)
            if m:
                key, val = m.group(1), m.group(2)
                kv[key] = val
        i += 1
    if i >= len(lines) or not FM_CLOSE.match(lines[i]):
        return False, {}
    return True, kv

def main():
    p = argparse.ArgumentParser(description="List .md files with missing/malformed YAML front-matter.")
    p.add_argument("roots", nargs="*", default=["merge_pr/updated", "sources/raw"],
                   help="Directories to scan (default: staging + raw sources).")
    args = p.parse_args()

    roots = [pathlib.Path(r) for r in args.roots]
    md_files = []
    for root in roots:
        if root.exists():
            md_files += list(root.rglob("*.md"))

    if not md_files:
        print("No Markdown files found under given roots.")
        sys.exit(0)

    missing = []
    malformed = []
    bad_contract = []

    for f in sorted(md_files):
        text = f.read_text(encoding="utf-8", errors="replace")
        ok, kv = has_well_formed_front_matter(text)
        if not ok:
            missing.append(f)
            continue
        # contract: exactly one of part or blueprint
        for pair in REQUIRED_ONE_OF:
            present = sum(1 for k in pair if k in kv and kv[k] and not kv[k].strip().startswith('#'))
            if present != 1:
                bad_contract.append(f)
                break

    if missing:
        print("Missing front-matter:")
        for f in missing: print(f"  - {f}")
    if malformed:
        print("Malformed front-matter:")
        for f in malformed: print(f"  - {f}")
    if bad_contract:
        print("Contract violation (need exactly one of 'part' or 'blueprint'):")
        for f in bad_contract: print(f"  - {f}")

    if not (missing or malformed or bad_contract):
        print("All good: front-matter present and contract satisfied.")

    # return nonzero if anything needs fixing (handy for CI)
    sys.exit(1 if (missing or malformed or bad_contract) else 0)

if __name__ == "__main__":
    main()
