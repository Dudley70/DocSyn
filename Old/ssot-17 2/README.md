# SSOT-5: Claude Code Knowledge Base for Gemini Gem

**SSOT-5** is a **dual-surface, single-source** knowledge system for Claude Code. Small modular docs (the source) are compiled into one authoritative manual `SSOT.md` (the surface) used by a Gemini Gem to deliver expert guidance on setup, safe use, and agent blueprints.

```
/core + /blueprints  →  build  →  SSOT.md  →  Gemini Gem  →  Expert Claude Code answers
```

### What’s in here
- **`/core/`** — Router (intent → section), Unified Risk Model, Devcontainer setup  
- **`/blueprints/`** — Normalized agent datasheets (Documenter, Guardian, Janitor, Tester, CI/CD Analyst, Adaptive, Orchestrator)  
- **`/dashboards/`** — Grafana JSON stubs for KPIs & logs (Prom + Loki)  
- **`/scripts/`** — Build + validation (assembler, router smoke test, code-lift)  
- **`SSOT.md`** — Compiled manual (auto-generated; **do not edit directly**)

---

## Quickstart (≤5 minutes)

**Prereqs:** `make`, `python3`.

```bash
git clone <repository-url>
cd ssot-5
make ci                 # builds SSOT, runs router smoke test, checks long code blocks
```

> **Heads-up:** Don’t edit `SSOT.md` directly — it’s compiled. Edit the small files in `core/` and `blueprints/`, then `make ssot`.

---

## Original Sources (Seeding)

Place your raw manuals in `sources/raw/` and run:

```bash
make seed-from-sources
make ssot
```

This creates `core/*.SOURCED.md` (for comparison) and appends provenance excerpts to relevant blueprints.
Review diffs, incorporate what you want into the curated chapters, then open a PR.

---

## Make commands

```bash
make ssot          # Compile sources → SSOT.md
make check         # Basic validation (warnings)
make router-test   # Router smoke tests
make code-lift     # Move long code blocks to /reference and link them
make seed-from-sources  # Heuristically seed curated files from sources/raw
make merge-from-sourced # Dry-run: structured merge proposal (writes merge_pr/)
make merge-apply   # Apply proposed merges (use in a feature branch → PR)
make pr-body       # Generate PR body text from merge_pr/report.json
make ci            # CI bundle: code-lift check + assemble + router-test
```

## Contributing

PRs must keep **stable section IDs** intact and update Router/Risks when semantics change.

## Project structure

```
ssot-5/
├── core/                    # Router, Risks, Devcontainer
├── blueprints/              # Agent datasheets (normalized)
├── dashboards/              # Grafana JSON stubs
├── reference/               # Lifted code, schemas, examples
├── scripts/                 # Assembler, router test, code-lift, merge tools
├── .github/workflows/       # CI (make ci)
├── build.manifest.json      # Assembly order
├── SSOT.md                  # Compiled surface (auto-generated)
└── README.md
```
