# DocSyn - Document Synthesiser

**DocSyn** is a document synthesis system that processes multiple source documents and compiles them into a single, de-duplicated knowledge base. It prevents "Global Leakage" by identifying and removing duplicate sections across different modules.

```
sources → staging → promotion → build → DocSyn_Compiled.md
```

## Quick Start

**Prerequisites:** `make`, `python3`

```bash
git clone <repository-url>
cd DocSyn
make docsyn                 # Complete pipeline: promote + build + validate
```

**Output:** `dist/DocSyn_Compiled.md` - The compiled knowledge base

## Simple Workflow

```bash
# Add files to staging
cp your-docs.md merge_pr/updated/

# Run complete pipeline
make docsyn

# Verify output matches baseline
make verify
```

## Core Commands

```bash
make docsyn        # Complete pipeline (recommended)
make verify        # Verify output matches baseline hash
make ci            # CI pipeline with staging cleanup
make clean-staging # Remove duplicate files from staging
```

## Project Structure

```
DocSyn/
├── core/                    # Global sections (router, risks, environment)
├── blueprints/              # Curated content modules
├── merge_pr/updated/        # Staging area for new files
├── scripts/                 # Build and validation scripts
├── dist/                    # Generated outputs
│   ├── DocSyn_Compiled.md   # Main compiled output
│   ├── VALIDATION.json      # Build validation report
│   └── PROMOTION_REPORT.json # File promotion details
├── tests/                   # Quality baselines
│   └── BASELINE_SHA256      # Expected output hash
└── build.manifest.json      # Source file configuration
```

## File Flow

1. **Staging**: Place files in `merge_pr/updated/`
2. **Promotion**: Files copied to `blueprints/` or `core/`
3. **Assembly**: Sources compiled into `dist/DocSyn_Compiled.md`
4. **Validation**: Structure and content checks
5. **Cleanup**: Staging cleaner removes duplicates

## Quality Assurance

DocSyn v1.1.0 includes deterministic builds with verification:

- **Baseline Verification**: `make verify` ensures consistent output
- **Deterministic Assembly**: Identical inputs always produce identical output
- **Comprehensive Testing**: File handling, Unicode support, cross-platform consistency
- **Staging Hygiene**: Automatic duplicate detection and removal

## Key Features

- **Deterministic Builds**: Same input always produces same output hash
- **Global Deduplication**: Prevents duplicate sections across modules
- **Staging Management**: Automatic cleanup of processed files
- **Quality Gates**: Baseline verification prevents regressions
- **Unicode Support**: Proper handling of international characters
- **Cross-Platform**: Consistent behavior across operating systems

## Contributing

1. Add your content to `merge_pr/updated/`
2. Run `make docsyn` to process and build
3. Check `dist/DocSyn_Compiled.md` for results
4. Verify with `make verify` before committing

## Baseline Management

The system maintains a quality baseline:

```bash
# Set new baseline (after content changes)
make docsyn >/dev/null
shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256

# Verify against baseline
make verify
```

## Requirements

- Python 3.x
- GNU Make
- UTF-8 terminal encoding

## Version History

**v1.1.0** - Deterministic builds, verification gates, comprehensive testing
**v1.0.0** - Initial release
