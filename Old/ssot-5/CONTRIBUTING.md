# Contributing to the Claude Code SSOT

## Workflow (DSSS Pattern)
1. Edit small source files in `core/` and `blueprints/`.
2. Run `make ssot` to compile the book into `SSOT.md`.
3. Open a PR. CI will assemble SSOT and lint Markdown.
4. Reviewers verify Router, Risks, and Blueprint template adherence.

## Authoring Conventions
- Keep sections 600–1,200 words; prefer links to long code blocks in `/reference`.
- Use **stable section IDs** (e.g., `{{#CH4-BP-ORCH}}`). Do not change them.
- Each blueprint MUST include: Objective, Diagram, I/O & Tools, Slash Command, Snippets, JSON Contract, Local Risks, Failure Modes, Ethics, Telemetry, Verification.
- Update Router and Risks when semantics change.

## Versioning
Follow semantic versions in the SSOT front-matter and maintain Change Log.
