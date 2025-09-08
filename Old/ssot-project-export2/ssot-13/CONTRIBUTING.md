
# Contributing
- Edit curated files in `core/` and `blueprints/`. Do **not** edit `SSOT.md` directly.
- Keep stable anchors (e.g., `{{#CH4-BP-DOC}}`) intact.
- If semantics change, update `core/00-router.md` and `core/01-risks.md`.
- Use `make ci` before pushing.

## Updating from raw sources
1. Place new files in `sources/raw/`
2. `make seed-from-sources`
3. `make merge-from-sourced` (review `merge_pr/` contents)
4. `git checkout -b chore/merge-sourced && make merge-apply && git commit -am "merge"`
5. Open a PR; CI will validate.
