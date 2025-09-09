# DocSyn Structural Contract

This document defines the **structural invariants** that must be preserved across all document batches to maintain system automation. These are **infrastructure components**, not content.

## 🔒 NEVER DELETE (Infrastructure Files)

### Router System
```
core/00-router.md              # Router table with CH4-BP-* route codes
core/00-router.SOURCED.md      # Router query index (populated by automation)
```

### Core Infrastructure
```
core/01-risks.SOURCED.md       # Risk framework (populated by automation)
core/02-devcontainer.SOURCED.md # Development environment (populated by automation)
```

### Blueprint Templates (Automation Anchors)
```
blueprints/documenter.md       # CH4-BP-DOC target
blueprints/guardian.md         # CH4-BP-GRD target  
blueprints/janitor.md          # CH4-BP-JAN target
blueprints/tester.md           # CH4-BP-TST target
blueprints/cicd-analyst.md     # CH4-BP-CICD target
blueprints/orchestrator.md     # CH4-BP-ORCH target
blueprints/adaptive-learning.md # CH4-BP-ADAPT target
```

### Input Directories
```
sources/raw/                   # Input for seed_from_sources.py
merge_pr/updated/              # Input for promote_updated.py
```

## 🔗 ROUTER CONTRACT (Immutable)

The router table **MUST** contain these route codes mapping to blueprint files:

| Route Code | Target File | Purpose |
|------------|-------------|---------|
| `CH4-BP-DOC` | `blueprints/documenter.md` | Documentation generation |
| `CH4-BP-GRD` | `blueprints/guardian.md` | File system monitoring |
| `CH4-BP-JAN` | `blueprints/janitor.md` | File management |
| `CH4-BP-TST` | `blueprints/tester.md` | Testing automation |
| `CH4-BP-CICD` | `blueprints/cicd-analyst.md` | CI/CD analysis |
| `CH4-BP-ORCH` | `blueprints/orchestrator.md` | Multi-agent coordination |
| `CH4-BP-ADAPT` | `blueprints/adaptive-learning.md` | Learning systems |

**Breaking this contract breaks automation.**

## ✅ SAFE TO MODIFY (Content Only)

### File Contents
- Content **inside** blueprint files (keep templates, replace sourced sections)
- Content **inside** .SOURCED files (preserve structure, replace content)
- Compiled outputs in `dist/` (regenerated automatically)

### Per-Batch Files
- Source documents in `sources/raw/` (cleared between batches)
- Staging files in `merge_pr/updated/` (cleared after promotion)
- Build artifacts and reports (regenerated)

## 🛡️ AUTOMATED PROTECTION

The QA system (`scripts/qa_build.py`) enforces this contract:

- **Required Files Check**: Fails if structural files are missing
- **Router Contract Check**: Validates route codes and blueprint mappings  
- **Forbidden Terms Check**: Prevents content contamination
- **Deterministic Build**: Ensures reproducible outputs

## 🚨 VIOLATION RECOVERY

If structural files are accidentally deleted:

```bash
# Restore from last known good state
git restore --source v1.1.0 -- core/00-router.SOURCED.md core/01-risks.SOURCED.md core/02-devcontainer.SOURCED.md
git restore --source v1.1.0 -- blueprints/documenter.md blueprints/guardian.md blueprints/janitor.md blueprints/tester.md blueprints/cicd-analyst.md blueprints/orchestrator.md blueprints/adaptive-learning.md

# Strip Claude Code content but keep structure
# (Replace content sections with "<!-- Content will be populated from document processing -->")

# Rebuild and regenerate baseline  
make docsyn
shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256
```

## 📋 BATCH RESET CHECKLIST

Before processing a new document batch:

1. ✅ Archive previous compiled output if needed
2. ✅ Clear `sources/raw/*` and `merge_pr/updated/*`
3. ✅ Run `make qa` to verify structural integrity
4. ✅ Confirm all CH4-BP-* routes are intact
5. ✅ Blueprint templates exist but contain minimal content
6. ✅ Add new documents and run `make docsyn`

## 🔧 FOR DEVELOPERS

**Remember:** This system processes **any document set**, not just Claude Code. The structure enables automation for:

- Academic papers → research synthesis
- API docs → unified documentation  
- Legal documents → compliance guides
- Technical specs → implementation guides

The router codes and blueprint templates are **universal infrastructure** that gets populated with content from whatever document set you're processing.

---

*This contract is enforced by CI/QA. Breaking it will cause automation failures.*
