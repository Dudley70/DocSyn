# Contributing

## Fast path
1. Put rich blueprint edits into `merge_pr/updated/*.md`.
2. Run:
   ```bash
   python scripts/one_click_repair_and_build.py
   python scripts/ci_consolidate.py
   python scripts/ci_validate.py
   ```
3. Commit. CI will re-run the same steps on PRs.

## Pre-commit
Install and run:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
