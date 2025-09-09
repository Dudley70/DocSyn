# DocSyn - Document Synthesiser

**DocSyn** is a document synthesis system that processes multiple source documents and compiles them into a single, de-duplicated knowledge base. It prevents "Global Leakage" by identifying and removing duplicate sections across different modules.

**Universal System:** Works with any document set - academic papers, API docs, legal documents, technical specifications, or any collection of related documents.

```
sources → staging → promotion → build → DocSyn_Compiled.md
```

## Quick Start

**Prerequisites:** `make`, `python3`

```bash
git clone <repository-url>
cd DocSyn

# Add your documents to staging
cp your-docs.md merge_pr/updated/

# Process and build  
make docsyn                 # Complete pipeline: promote + build + validate
```

**Output:** `dist/DocSyn_Compiled.md` - The compiled knowledge base

## Document Processing Workflows

### Method 1: Direct Staging (Recommended)
```bash
# Add files to staging
cp your-docs.md merge_pr/updated/

# Run complete pipeline
make docsyn

# Verify output matches baseline
make verify
```

### Method 2: Bulk Source Processing
```bash
# Add raw documents
cp *.md sources/raw/

# Extract and seed blueprint content
make seed-from-sources

# Process and build
make docsyn
```

## Core Commands

```bash
make docsyn        # Complete pipeline (recommended)
make verify        # Verify output matches baseline hash
make qa            # Run quality assurance checks
make ci            # CI pipeline with staging cleanup
make clean-staging # Remove duplicate files from staging
make seed-from-sources # Extract content from sources/raw/
```

## Project Structure

```
DocSyn/
├── core/                    # Global sections (router, risks, environment)
├── blueprints/              # Curated content modules (universal templates)
├── sources/raw/             # Bulk document input (for seed-from-sources)
├── merge_pr/updated/        # Staging area for direct document input
├── scripts/                 # Build and validation scripts
├── dist/                    # Generated outputs
│   ├── DocSyn_Compiled.md   # Main compiled output
│   ├── QA_SUMMARY.txt       # Quality assurance report
│   └── QA_REPORT.json       # Detailed QA data
├── tests/                   # Quality baselines
│   └── BASELINE_SHA256      # Expected output hash
├── STRUCTURAL_CONTRACT.md   # Infrastructure preservation guide
└── build.manifest.json      # Source file configuration
```

## File Flow

1. **Input**: Place files in `merge_pr/updated/` (direct) or `sources/raw/` (bulk)
2. **Extraction**: `seed-from-sources` extracts content to blueprint templates (if using bulk)
3. **Promotion**: Files copied to `blueprints/` or `core/` directories
4. **Assembly**: Sources compiled into `dist/DocSyn_Compiled.md`
5. **Validation**: Structure, content, and quality checks
6. **Cleanup**: Staging cleaner removes duplicates

## Quality Assurance

DocSyn v1.1.0+ includes comprehensive quality gates:

- **Structural Integrity**: Ensures automation infrastructure is intact
- **Forbidden Terms**: Prevents contamination from previous document batches
- **Router Contract**: Validates route codes and blueprint mappings
- **Baseline Verification**: `make verify` ensures consistent output
- **Deterministic Assembly**: Identical inputs always produce identical output
- **Unicode Support**: Proper handling of international characters
- **Cross-Platform**: Consistent behavior across operating systems

## Key Features

- **Universal Document Processing**: Works with any document set or domain
- **Deterministic Builds**: Same input always produces same output hash
- **Global Deduplication**: Prevents duplicate sections across modules
- **Multiple Input Methods**: Direct staging or bulk source processing
- **Quality Gates**: Comprehensive QA with structural integrity checks
- **Staging Management**: Automatic cleanup of processed files
- **Template System**: Reusable blueprint structure for any content type
- **Unicode Support**: Proper handling of international characters
- **Cross-Platform**: Consistent behavior across operating systems

## For New Document Batches

**Between document sets, clear previous content:**

```bash
# Archive previous output (optional)
cp dist/DocSyn_Compiled.md archive/previous_batch_$(date +%Y%m%d).md

# Clear staging and sources  
rm -rf merge_pr/updated/* sources/raw/*

# Verify system integrity
make qa

# Add new documents and process
cp new-docs/*.md merge_pr/updated/
make docsyn
```

**See `STRUCTURAL_CONTRACT.md` for what must never be deleted.**

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
