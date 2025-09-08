# SSOT Clean Working Package — v1.2.0

Generated: 2025-09-08T17:13:11.378890Z

This package contains a **clean, working SSOT build** with curated sources, build scripts, and compiled outputs.

## Structure
```
core/                      # core governance (router, risks, devcontainer)
blueprints/                # cleaned blueprint datasheets only
tools/merge_config.yaml    # governance (ignore headings, snippet limits, guards)
scripts/assemble_ssot.py   # deterministic assembler
build.manifest.json        # curated-only inputs
Makefile                   # make ssot / make clean / make verify
dist/                      # compiled outputs
```

## How to build
```bash
make clean
make ssot
make verify
```

- **make ssot** compiles `dist/SSOT.md` plus part files.
- **make verify** prints quick checks for duplicates and code-fence parity.

> Note: Blueprints were cleaned to remove any global sections and to keep only blueprint-specific content.
