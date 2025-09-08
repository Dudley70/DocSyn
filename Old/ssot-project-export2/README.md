# SSOT Project Export

**Version:** 1.1.4  
**Exported:** 2025-09-08

## Structure

- `ssot-13/` — main repo tree (core, blueprints, sources, etc.)
- `scripts/verify_manifest.py` — verifies curated files exist
- `.github/workflows/build-ssot.yml` — CI workflow (verify + build)
- `.gitignore` — ignores macOS artefacts

## Usage

```bash
make -C ssot-13 verify
ALLOW_MISSING=0 make -C ssot-13 ssot
```
