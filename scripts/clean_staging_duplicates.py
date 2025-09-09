#!/usr/bin/env python3
"""
DocSyn — clean_staging_duplicates.py

Safely removes exact duplicates from the staging area (merge_pr/updated/)
that already exist in curated trees (blueprints/, core/, etc.).
- Compares by SHA256 content hash (chunked), not just file name.
- Default is DRY RUN (prints/report only). Use --delete to actually remove.
- Skips dotfiles and the `_triage/` area by default (configurable).
- Emits a JSON report for CI: dist/CLEAN_STAGING_REPORT.json (default).

Usage:
  python scripts/clean_staging_duplicates.py --delete
  DOCSYN_RETAIN_STAGING=1 python scripts/clean_staging_duplicates.py    # forces dry-run
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Dict, List

CHUNK = 1 << 20  # 1 MiB

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(CHUNK), b''):
            h.update(chunk)
    return h.hexdigest()

def build_hash_index(roots: List[Path], ignore_hidden: bool = True) -> Dict[str, List[str]]:
    index: Dict[str, List[str]] = {}
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            # ignore hidden files/folders
            if ignore_hidden and any(part.startswith(".") for part in p.parts):
                continue
            try:
                digest = sha256_file(p)
                index.setdefault(digest, []).append(str(p))
            except Exception as e:
                print(f"[WARN] Could not hash {p}: {e}", file=sys.stderr)
    return index

def collect_staging_files(staging: Path, skip_triage: bool = True, ignore_hidden: bool = True):
    files = []
    if not staging.exists():
        return files
    for p in staging.rglob("*"):
        if p.is_dir():
            continue
        if skip_triage and "_triage" in p.parts:
            continue
        if ignore_hidden and any(part.startswith(".") for part in p.parts):
            continue
        files.append(p)
    return files

def main():
    ap = argparse.ArgumentParser(description="Remove exact duplicate files from staging if they already exist in curated trees.")
    ap.add_argument("--staging", default="merge_pr/updated", help="Staging root folder (default: merge_pr/updated)")
    ap.add_argument("--curated", nargs="+", default=["blueprints", "core"], help="Curated roots to compare against (default: blueprints core)")
    ap.add_argument("--report", default="dist/CLEAN_STAGING_REPORT.json", help="JSON report output path")
    ap.add_argument("--delete", action="store_true", help="Actually delete duplicates from staging (default: dry run)")
    ap.add_argument("--include-triage", action="store_true", help="Also clean _triage area (default: skip)")
    ap.add_argument("--no-ignore-hidden", action="store_true", help="Do not ignore hidden files/folders")
    ap.add_argument("--fail-if-leftovers", action="store_true", help="Exit non-zero if any non-duplicate files remain in staging after cleanup (useful in CI)")
    args = ap.parse_args()

    # Env override: DOCSYN_RETAIN_STAGING=1 forces dry-run
    retain = os.getenv("DOCSYN_RETAIN_STAGING", "0") not in ("0", "", "false", "False", "NO", "no")
    if retain and args.delete:
        print("[INFO] DOCSYN_RETAIN_STAGING is set; overriding --delete to DRY RUN.")
        args.delete = False

    staging = Path(args.staging)
    curated_roots = [Path(c) for c in args.curated]
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Build curated content hash index
    print("[INFO] Indexing curated trees:", ", ".join(str(c) for c in curated_roots))
    curated_index = build_hash_index(curated_roots, ignore_hidden=not args.no_ignore_hidden)
    print(f"[INFO] Curated files indexed: {sum(len(v) for v in curated_index.values())} (unique hashes: {len(curated_index)})")

    # Scan staging
    staging_files = collect_staging_files(staging, skip_triage=not args.include_triage, ignore_hidden=not args.no_ignore_hidden)
    print(f"[INFO] Staging files scanned: {len(staging_files)}")

    removed = []
    kept = []
    errors = []
    duplicates = []

    for src in staging_files:
        try:
            digest = sha256_file(src)
            if digest in curated_index:
                duplicates.append(str(src))
                if args.delete:
                    try:
                        src.unlink()
                        removed.append(str(src))
                        print(f"[CLEAN] removed duplicate: {src}")
                    except Exception as e:
                        errors.append({"file": str(src), "error": str(e)})
                        print(f"[ERROR] could not remove {src}: {e}", file=sys.stderr)
                else:
                    kept.append(str(src))
                    print(f"[DRYRUN] would remove duplicate: {src}")
            else:
                kept.append(str(src))
        except Exception as e:
            errors.append({"file": str(src), "error": str(e)})
            print(f"[WARN] could not hash {src}: {e}", file=sys.stderr)

    # Determine leftovers
    leftovers = []
    if args.fail_if_leftovers:
        leftovers = [p for p in kept if p not in removed]
        if leftovers:
            print("[FAIL] Staging not empty after cleanup; refusing to proceed in CI.")
            exit_code = 2
        else:
            exit_code = 0
    else:
        exit_code = 0

    # Write report
    import datetime as _dt
    report = {
        "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
        "staging": str(staging),
        "curated": [str(c) for c in curated_roots],
        "dry_run": not args.delete,
        "retain_env": bool(retain),
        "indexed_hashes": len(curated_index),
        "scanned_staging": len(staging_files),
        "duplicates_detected": len(duplicates),
        "removed": removed,
        "kept": kept,
        "errors": errors,
        "leftovers": leftovers,
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[INFO] Report written to {report_path}")
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
