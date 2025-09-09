# DocSyn — Staging Cleaner

This tool keeps `merge_pr/updated/` tidy by removing **exact duplicates** that already exist under curated trees (e.g. `blueprints/`, `core/`). It compares by **SHA256 content**, not just names.

## Why
- Prevents drift when a promotion ran in *copy-retention* mode.
- Keeps staging a true *inbox* so contributors don't re‑ingest the same file.
- Safe: removes only files that are byte‑for‑byte duplicates of curated content.

## Usage

```bash
# Dry run (default): prints what it would remove and writes a JSON report
python scripts/clean_staging_duplicates.py

# Actually remove duplicates
python scripts/clean_staging_duplicates.py --delete

# Fail CI if anything remains in staging (excluding _triage/)
python scripts/clean_staging_duplicates.py --delete --fail-if-leftovers
```

### Options
- `--staging merge_pr/updated` (default)
- `--curated blueprints core` (default; multiple allowed)
- `--include-triage` include `_triage/` in cleanup (default: skip)
- `--no-ignore-hidden` include dotfiles/hidden paths (default: ignore)
- `--report dist/CLEAN_STAGING_REPORT.json` output report path
- `--delete` remove duplicates (default: dry run)
- `--fail-if-leftovers` exit non-zero if non-duplicates remain in staging

### Env flags
- `DOCSYN_RETAIN_STAGING=1` → forces DRY RUN regardless of `--delete`

## CI integration
Add a `clean-staging` step before build:
```makefile
clean-staging:
	python3 scripts/clean_staging_duplicates.py --delete --fail-if-leftovers

ci: clean-staging
	python3 scripts/lift_code_blocks.py check
	python3 scripts/assemble_ssot.py
	python3 scripts/router_smoke_test.py
```
Reports are written to `dist/CLEAN_STAGING_REPORT.json`.
