# DocSyn - Document Synthesiser

**DocSyn** is a hybrid document synthesis system that compiles vendor-neutral core patterns with vendor-specific implementation examples into a single, policy-aware knowledge base. It supports both universal architectural patterns and concrete vendor implementations while maintaining strict quality controls.

**Hybrid Architecture:** Vendor-neutral core + vendor-specific appendix with policy-aware validation

[![docsyn-ci](https://github.com/Dudley70/DocSyn/actions/workflows/docsyn-ci.yml/badge.svg)](https://github.com/Dudley70/DocSyn/actions/workflows/docsyn-ci.yml)
[![nightly-qa](https://github.com/Dudley70/DocSyn/actions/workflows/nightly-qa.yml/badge.svg)](https://github.com/Dudley70/DocSyn/actions/workflows/nightly-qa.yml)

```
sources → staging → promotion → policy-aware build → DocSyn_Compiled.md
                                        │
                                        ├── Core (Universal Patterns)
                                        └── Appendix (Vendor Examples)
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
make gen-curation-index    # Generate curated sources overview
make manifest-guard        # Validate manifest integrity
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
make docsyn               # Complete pipeline (recommended)
make verify               # Verify output matches baseline hash
make qa                   # Run quality assurance + manifest validation
make ci                   # CI pipeline with staging cleanup
make clean-staging        # Remove duplicate files from staging
make gen-curation-index   # Generate deterministic curated sources index
make manifest-guard       # Validate manifest integrity and vendor ordering
make seed-from-sources    # Extract content from sources/raw/
```

## Project Structure

```
DocSyn/
├── core/                    # Global sections (router, risks, environment, curation index)
├── blueprints/              # Curated content modules (universal templates + vendor examples)
├── sources/raw/             # Bulk document input (for seed-from-sources)
├── merge_pr/updated/        # Staging area for direct document input
├── scripts/                 # Build and validation scripts
│   └── tools/               # Operational tools (curation index, manifest guard)
├── dist/                    # Generated outputs
│   ├── DocSyn_Compiled.md   # Main compiled output (with curation index)
│   ├── QA_SUMMARY.txt       # Quality assurance report
│   ├── QA_REPORT.json       # Detailed QA data
│   └── CLEAN_STAGING_REPORT.json # Staging cleanup report
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

DocSyn v1.2.1+ includes comprehensive policy-aware quality gates with operational tools:

- **Curated Sources Index**: Self-documenting system showing all curated content with metadata
- **Manifest Guard**: Validates file existence, prevents duplicates, enforces vendor ordering
- **Policy-Aware Validation**: Intelligent classification of vendor-specific vs. vendor-neutral content
- **Hybrid Content Support**: Vendor terms allowed in marked vendor files, forbidden in neutral core
- **Structural Integrity**: Ensures automation infrastructure is intact
- **Anchor File Support**: Small blueprint files exempt from size requirements via `anchor: true`
- **Router Contract**: Validates route codes and blueprint mappings
- **Baseline Verification**: `make verify` ensures consistent output (current: a9655f5a)
- **Deterministic Assembly**: Identical inputs always produce identical output
- **Unicode Support**: Proper handling of international characters
- **Cross-Platform**: Consistent behavior across operating systems

### Policy Classification

Files are classified via front-matter:

```yaml
# Vendor-specific content (allows vendor terms)
policy: vendor-specific
tags: [vendor, claude]

# Anchor files (exempt from size requirements)  
anchor: true

# Neutral content (default, enforces vendor-neutral policy)
# No special annotations needed
```

## Key Features

- **Hybrid Architecture**: Vendor-neutral core + vendor-specific appendix with clear separation
- **Policy-Aware QA**: Intelligent content classification and validation
- **Deterministic Builds**: Same input always produces same output hash (current: a9655f5a)
- **Global Deduplication**: Prevents duplicate sections across modules
- **Multiple Input Methods**: Direct staging or bulk source processing
- **Quality Gates**: Comprehensive QA with policy-aware validation
- **Staging Management**: Automatic cleanup of processed files
- **Template System**: Reusable blueprint structure for any content type
- **Unicode Support**: Proper handling of international characters
- **Cross-Platform**: Consistent behavior across operating systems
- **Vendor Content Support**: Framework for including vendor examples while preserving neutrality
- **Self-Documenting System**: Curated sources index provides real-time metadata visibility
- **Manifest Validation**: Prevents configuration drift and broken references
- **Operational Tools**: gen-curation-index and manifest-guard for enhanced workflows

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

The system maintains a quality baseline with deterministic builds:

```bash
# Set new baseline (after content changes)
make docsyn >/dev/null
shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256

# Verify against baseline
make verify

# Current baseline: a9655f5a (includes curation index)
```

## Current System Scale

**Output Statistics:**
- **Size**: ~293KB+ (with curation index)
- **Sources**: 17 curated files (4 core + 13 blueprints)
- **Architecture**: Hybrid vendor-neutral + vendor-specific with self-documentation
- **Hash**: a9655f5a (deterministic baseline including curation index)

**Content Breakdown:**
- **Core (Vendor-Neutral)**: Universal agent patterns, development environment, curation index
- **Appendix (Vendor-Specific)**: Claude implementation examples and detailed guides
- **Quality Gates**: 8 policy checks + manifest validation with vendor-aware classification
- **Operational Tools**: Curated sources index + manifest integrity validation

## Requirements

- Python 3.x
- GNU Make
- UTF-8 terminal encoding

## Version History

**v1.2.1** - Operational polish: curated sources index + manifest guard with self-documenting system  
**v1.2.0** - Hybrid architecture, policy-aware QA, vendor appendix integration  
**v1.1.0** - Deterministic builds, verification gates, comprehensive testing  
**v1.0.0** - Initial release
