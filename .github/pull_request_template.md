## Summary
<!-- What does this change do? -->

## Checklist
- [ ] Ran `make docsyn && make qa` locally (no errors)
- [ ] `python3 scripts/verify_baseline.py` passes, or I intentionally updated `tests/BASELINE_SHA256`
- [ ] `python3 scripts/manifest_guard.py` passes (no missing/dup/misordered curated sources)
- [ ] Vendor content (if any) is annotated with `policy: vendor-specific`
- [ ] No forbidden terms in vendor-neutral files
- [ ] Curation index generated (`make gen-curation-index`) and added to commit if changed

## Notes
<!-- Anything reviewers should pay special attention to? -->
