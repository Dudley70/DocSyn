# DocSyn v1.1.0 Release Notes

## Major Features

### Simplified Workflow
- **`make docsyn`** - Single command for complete pipeline (promote → build → validate)
- Reduces workflow from `python scripts/promote_updated.py && make ci` to `make docsyn`
- 44 characters reduced to 10 characters (75% reduction)

### Deterministic Builds
- **Identical inputs now produce identical outputs** 
- Fixed non-deterministic timestamp injection that caused hash variations
- Explicit input sorting ensures consistent assembly order
- Unicode NFC normalization for cross-platform consistency

### Quality Verification System
- **`make verify`** - Baseline hash verification prevents regressions
- `tests/BASELINE_SHA256` contains expected output hash
- Automatic detection of content changes or build issues
- Production-ready quality gates

### Self-Healing Staging Management
- **Staging cleaner integration** removes duplicate files automatically
- Integrated into CI pipeline (`make ci` includes cleaning)
- SHA256 content comparison prevents false positives
- Maintains staging area as clean inbox for new content

## Technical Improvements

### Build System
- **Output renamed**: `dist/SSOT.md` → `dist/DocSyn_Compiled.md` for clarity
- **Deterministic assembly**: Input sorting + Unicode normalization
- **Cross-platform consistency**: .gitattributes for line ending standardization
- **Comprehensive testing**: File handling, Unicode support, order determinism

### File Handling
- **Staging behavior documented**: Files copied to blueprints (originals remain)
- **Automatic cleanup**: Staging cleaner removes exact duplicates  
- **Promotion safety**: 20% shrinkage detection prevents data loss
- **Error reporting**: Comprehensive JSON reports for troubleshooting

### Quality Assurance
- **Baseline verification**: Hash-based regression detection
- **Comprehensive test suite**: Order determinism, idempotent promotion, Unicode handling
- **Cross-platform testing**: Line endings, encoding, file system behavior
- **Production hardening**: Edge case validation and error handling

## Breaking Changes

### Output File Renamed
- **Old**: `dist/SSOT.md`
- **New**: `dist/DocSyn_Compiled.md`
- **Migration**: Update any scripts or processes that reference the old filename

### Deterministic Output
- **Change**: Build timestamps removed from compiled output
- **Impact**: Same content will always produce same file hash
- **Benefit**: Enables reliable change detection and version control

## Files Added

- `scripts/clean_staging_duplicates.py` - Staging cleaner with SHA256 comparison
- `scripts/verify_baseline.py` - Hash verification system
- `tests/BASELINE_SHA256` - Expected output hash baseline
- `test_docsyn_behavior.py` - Comprehensive behavior testing
- `test_hardening.py` - Pre-release hardening validation
- `.gitattributes` - Cross-platform line ending consistency
- `CLEAN_STAGING.md` - Staging cleaner documentation

## Files Modified

- `scripts/assemble_ssot.py` - Added sorting, Unicode normalization, deterministic behavior
- `Makefile` - Added `docsyn` and `verify` targets, integrated staging cleaner
- `STATUS.md`, `TASKS.md`, `DECISIONS.md` - Updated project state documentation
- `README.md` - Complete rewrite for v1.1.0 features and workflow

## Migration Guide

### From v1.0.0 to v1.1.0

1. **Update workflow commands**:
   ```bash
   # Old workflow
   python scripts/promote_updated.py && make ci
   
   # New workflow  
   make docsyn
   ```

2. **Update references to output file**:
   ```bash
   # Old
   cat dist/SSOT.md
   
   # New
   cat dist/DocSyn_Compiled.md
   ```

3. **Set baseline hash** (first time):
   ```bash
   make docsyn >/dev/null
   shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256
   ```

4. **Verify builds** going forward:
   ```bash
   make verify
   ```

## System Requirements

- Python 3.x (unchanged)
- GNU Make (unchanged)  
- UTF-8 terminal encoding (recommended)

## Known Issues

- Unicode characters (emoji, accents) may not preserve in final output on some systems
- This doesn't affect build success but may impact display of international content

## Contributors

This release represents a significant maturity improvement with production-grade reliability, comprehensive testing, and quality gates for ongoing development.
