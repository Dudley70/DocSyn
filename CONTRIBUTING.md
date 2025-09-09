# Contributing to DocSyn

## Quick Start Workflow

### 1. Add Your Documents
```bash
# Add documents to staging
cp your-documents.md merge_pr/updated/
```

### 2. Build and Validate
```bash
# Complete pipeline: promote + build + validate
make docsyn

# Verify output matches baseline
make verify
```

### 3. Check Quality
```bash
# Run comprehensive QA including manifest validation
make qa

# Generate/update curation index
make gen-curation-index
```

## Understanding the System

### Hybrid Architecture
DocSyn uses a hybrid content model:
- **Core sections** (vendor-neutral): Universal patterns in `core/`
- **Blueprint sections**: Templates in `blueprints/` (both neutral and vendor-specific)
- **Appendix**: Vendor-specific implementations clearly separated

### Policy-Aware Content
Files are classified via front-matter:
```yaml
# Vendor-specific content (allows vendor terms)
policy: vendor-specific
tags: [vendor, claude]

# Small blueprint files (exempt from size requirements)
anchor: true

# Neutral content (default) - no special annotations needed
```

### Quality Gates
The system enforces:
- **Manifest integrity**: File existence, no duplicates, proper vendor ordering
- **Policy compliance**: Vendor terms only allowed in vendor-specific files
- **Structural integrity**: Router contracts and required files
- **Deterministic builds**: Same input always produces same output

## Advanced Workflows

### Bulk Document Processing
```bash
# Add raw documents
cp *.md sources/raw/

# Extract and seed blueprint content
make seed-from-sources

# Build and validate
make docsyn
```

### Manifest Management
```bash
# Validate manifest integrity
make manifest-guard

# Check what's currently curated
cat core/95-curation-index.md

# See detailed QA report
cat dist/QA_SUMMARY.txt
```

### Baseline Management
```bash
# Set new baseline after content changes
make docsyn >/dev/null
shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256

# Always verify your changes
make verify
```

## File Organization

### Input Paths
- `merge_pr/updated/` - Direct document input (recommended)
- `sources/raw/` - Bulk document input for extraction

### Output Files
- `dist/DocSyn_Compiled.md` - Main compiled output
- `dist/QA_SUMMARY.txt` - Quality assurance report
- `core/95-curation-index.md` - Self-documenting curated sources index

### Configuration
- `build.manifest.json` - Defines which files are curated
- `tests/BASELINE_SHA256` - Expected output hash for verification

## Pre-commit Setup
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Troubleshooting

### Common Issues
- **Hash mismatch**: Content changed, run `make verify` to see details
- **Manifest errors**: Run `make manifest-guard` for specific issues
- **QA failures**: Check `dist/QA_SUMMARY.txt` for policy violations

### Getting Help
- Check `TROUBLESHOOTING.md` for detailed guidance
- Review `STRUCTURAL_CONTRACT.md` for infrastructure requirements
- See `README.md` for complete system overview

## Quality Standards

### Required Checks
All contributions must pass:
- `make manifest-guard` - Manifest integrity
- `make qa` - Policy compliance and structural validation
- `make verify` - Deterministic build verification

### Best Practices
- Use descriptive front-matter for proper classification
- Keep vendor-specific content clearly marked
- Test with `make docsyn` before committing
- Regenerate curation index with `make gen-curation-index`

The system is designed to handle any document set while maintaining quality and architectural integrity.
