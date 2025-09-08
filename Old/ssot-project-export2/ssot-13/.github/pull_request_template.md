# SSOT Structured Merge — Pull Request

## Summary
Briefly describe what this PR does (e.g., "Structured merge from SOURCED excerpts into blueprints").

## Merge Report (auto)
> If you ran `make merge-from-sourced`, paste or attach the generated report:
- Report file: `merge_pr/report.json`
- Patches: `merge_pr/patches/`
- Proposed files: `merge_pr/updated/`

<details>
<summary>Paste report.json here</summary>

```json
{
  "changed": ["..."],
  "skipped": ["..."],
  "apply": false
}
```
</details>

## Provenance
- Sources: `/sources/raw/*.md`
- Seeding command: `make seed-from-sources`
- Merge command: `make merge-from-sourced` (dry run) → `make merge-apply` (in a feature branch)

## Governance Impact
- Router changes required?  ☐ No  ☐ Yes (describe and update `core/00-router.md`)
- Risk model changes required?  ☐ No  ☐ Yes (describe and update `core/01-risks.md`)
- Stable anchors preserved?  ☑ Yes

## Observability Impact
- KPIs/metrics added or changed?  ☐ No  ☐ Yes (list)
- Dashboards adjustments needed?  ☐ No  ☐ Yes (describe)

## CI
- [ ] `make ci` passed locally (code-lift check, assemble, router-test)
- [ ] Long code blocks (if any) lifted to `/reference/` (CI enforces)

## Checklist
- [ ] Edited only curated sources (`core/`, `blueprints/`); did not change `SSOT.md` directly
- [ ] Kept blueprint template structure and stable IDs intact
- [ ] Updated Router/Risks if semantics changed
- [ ] Added provenance notes in merged sections
