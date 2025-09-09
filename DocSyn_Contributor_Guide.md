# Document Synthesiser (DocSyn) — Contributor Guide
**How to ingest, triage, promote, clean, synthesise, and validate content into the SSOT — including brand‑new domains.**

_Last updated: 09 September 2025_

---

## 1. Purpose & Principles
This guide shows exactly how to add documents to **DocSyn** while preserving the **Single Source of Truth (SSOT)** guarantees. It covers the common path (10th doc into existing blueprints) and the edge path (completely new domain).

**Principles**
- **Staging → Curation → Build:** never edit the root `SSOT.md` directly.
- **Surgical de‑duplication:** the build removes global leakage (escaped headings, tables) while preserving provenance.
- **Human‑in‑the‑Loop:** contributors propose content; CI gates and reviewers approve.

---

## 2. Where to Drop Your File
### 2.1 If you know the blueprint (recommended)
Put your file in a matching subfolder:
```
merge_pr/updated/<blueprint>/
  └── your-file-name.md
```
**Example**
```
merge_pr/updated/documenter/api-style-guide-v4.md
```

### 2.2 If you’re unsure of the blueprint
Use a triage area or drop at the root — promotion still works and reports will flag it as _uncategorised_.
```
merge_pr/updated/_triage/candidate-risk-controls-checklist.md
# or
merge_pr/updated/candidate-risk-controls-checklist.md
```

**Where not to put it (unless global):** If the doc adjusts **Part A** (Router, Unified Risk & Control Model, Standard Dev Environment), mark it `part: A` (see §6.2) and use `_triage` to route to `/core` during review.

---

## 3. Minimal Front‑Matter (Provenance)
Add a small YAML header at the top. This makes provenance auditable and helps the Curator Agent learn.
```yaml
---
source: Company Policy v3.1 (PDF)
source_url: https://example.com/policy_v3_1.pdf
retrieved: 2025-09-09
owner: Risk/Legal
tags: [policy, risk, controls]
---
```

---

## 4. Commands You’ll Run (Promotion → Build)
```bash
# 1) Promote staged docs into curated blueprints (with backups)
python scripts/promote_updated.py

# 2) Clean, synthesise, validate (surgical de-dup + invariants)
make ci

# 3) Review artifacts
less dist/PROMOTION_REPORT.json
less dist/LEAKAGE_REPORT.json
less dist/VALIDATION.json
open dist/SSOT.md
```
_No `make`? Use the one‑click entrypoint if present:_
```bash
python one_click_repair_and_build.py
```

---

## 5. Decision Tree — Where Does My Doc Go?
- **Clearly blueprint‑specific?** → `merge_pr/updated/<blueprint>/…`
- **Unsure which blueprint?** → `merge_pr/updated/_triage/…` (or root)
- **Clearly global (Part A)?** → add `part: A` in front‑matter and drop into `_triage` for curator routing.

---

## 6. Completely Different Documents (Brand‑New Domains)
Use this path when material doesn’t fit any existing blueprint (e.g., a new function or product area).

### 6.1 Create a new blueprint
```text
# New blueprint skeleton
blueprints/<new_blueprint>.md           # built from promoted content
merge_pr/updated/<new_blueprint>/new-topic-overview.md
merge_pr/updated/<new_blueprint>/runbook-v1.md
```
Then run promotion and build. The consolidator synthesises a clean datasheet and removes global leakage automatically.

### 6.2 If the content is **Global (Part A)**
If your material adjusts **Router**, **Unified Risk & Control Model**, or **Standard Dev Environment**, mark it as Part A and route via triage:
```yaml
---
part: A
section: Router
source: Team Design Notes (md)
owner: Platform
---

# Proposed Router addition
...
```
A reviewer merges the best version into the single canonical Part‑A sections; CI ensures they appear **only once** in the SSOT.

### 6.3 New repository vs. federation (bigger expansions)
- Large, distinct corpora (e.g., a new business line) → consider a **separate repo** with the same pipeline.
- Use **federation** later to reuse Part‑A building blocks across repos and publish a unified catalog.
- Keep **namespacing** clean to avoid cross‑domain contamination in retrieval.

---

## 7. Quality Gates You Can Trust
- **De‑duplication:** heading‑scoped + content fingerprints (escaped headings and tables handled).
- **Leakage reports:** structured blocks (e.g., “Agent Query Index” tables) removed from blueprints; see `dist/LEAKAGE_REPORT.json`.
- **Invariants:** single copy of Part‑A globals; code‑fence parity; file size sanity; promotion safety nets with timestamped backups.

---

## 8. Reset or Clean Rebuild (Optional)
Normally unnecessary — the pipeline is idempotent. If you want a fresh slate:
```bash
rm -rf dist/
python scripts/promote_updated.py
make ci
```
If promotion went wrong, restore from `dist/backups/blueprints/<timestamp>/`.

---

## 9. Examples
### 9.1 Existing blueprint (Documenter)
```text
merge_pr/updated/documenter/api-style-guide-v4.md
---
source: Internal API Guide (GDoc)
owner: DevEx
tags: [api, style]
---
# API Style Guide v4
...
```

### 9.2 Unsure → triage
```text
merge_pr/updated/_triage/candidate-risk-controls-checklist.md
---
source: Audit Deck (PPTX)
owner: Risk
---
# Risk Controls Checklist (Draft)
...
```

### 9.3 Completely new domain (Analytics)
```text
merge_pr/updated/analytics/analytics-oncall-playbook.md
merge_pr/updated/analytics/kpi-definitions-v1.md
```

---

## 10. Troubleshooting — Fast Signals
- **Validation says OK but you see duplicates** → ensure front‑matter and headings are **not blockquoted**; re‑run `make ci` and open `LEAKAGE_REPORT.json`.
- **Promotion did nothing** → check paths under `merge_pr/updated/`; see `PROMOTION_REPORT.json` for moved/ignored files.
- **Root SSOT overwritten** → expected: it’s **AUTOGENERATED**. Always edit staged sources instead.
- **Non‑markdown sources** → convert to `.md` first, keep headings/tables, add provenance front‑matter.

---

## One‑Page Cheat Sheet — Add the 10th Document
- **Drop here:** `merge_pr/updated/<blueprint>/` or `_triage/`
- **Front‑matter:** `source`, `source_url`, `retrieved`, `owner`, `tags`
- **Promote:** `python scripts/promote_updated.py`
- **Build:** `make ci`
- **Review:** `dist/SSOT.md`, `dist/LEAKAGE_REPORT.json`, `dist/VALIDATION.json`
- **Reset (optional):** `rm -rf dist/` then promote + build

---

## Appendix A — Optional Staging Cleaner (Self‑Healing)
To keep `merge_pr/updated/` tidy when a promotion runs in copy mode, add a **staging cleaner** to CI that removes exact duplicates already in curated trees.

**Script:** `scripts/clean_staging_duplicates.py` (SHA256‑based; dry‑run by default).  
**Makefile target (example):**
```make
PY ?= python3
.PHONY: clean-staging ci

clean-staging:
	@$(PY) scripts/clean_staging_duplicates.py --delete --fail-if-leftovers || \
	 (echo "Staging not clean. See dist/CLEAN_STAGING_REPORT.json" && exit 2)

ci: clean-staging
	@$(PY) scripts/lift_code_blocks.py check
	@$(PY) scripts/assemble_ssot.py
	@$(PY) scripts/router_smoke_test.py
```

**Env override:** `DOCSYN_RETAIN_STAGING=1` → forces dry‑run even with `--delete`.

---

© 2025 DocSyn — Document Synthesiser
