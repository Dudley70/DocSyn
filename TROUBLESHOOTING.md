# Troubleshooting

## Build Issues

### `make: command not found`
Install GNU Make:
- **macOS**: `brew install make`
- **Ubuntu/Debian**: `sudo apt-get install make`
- **Windows**: Use WSL or install Make for Windows

### `python3: command not found`
Install Python 3.11+ from python.org or your package manager

### Permission denied errors
Ensure you have write permissions to the project directory and that scripts are executable:
```bash
chmod +x scripts/*.py
```

## File Processing

### Promotion did nothing / files stuck in staging
1. Check `dist/PROMOTION_REPORT.json` for details
2. Verify YAML front-matter in your files:
   ```yaml
   ---
   blueprint: documenter  # or guardian, janitor, etc.
   part: A               # for core/ content only
   ---
   ```
3. Files without proper front-matter go to `_triage/`

### Leakage detection unexpected results
1. Open `dist/LEAKAGE_REPORT.json` for detailed analysis
2. Ensure headings use actual Markdown `#` syntax, not:
   - Quoted headings: `"# Header"`
   - Code blocks: `` `# Header` ``
   - HTML: `<h1>Header</h1>`

### Staging cleaner removes too much/too little
Check `dist/CLEAN_STAGING_REPORT.json`:
- Cleaner uses SHA256 content comparison (exact matches only)
- Use `--include-triage` to clean `_triage/` area
- Files with different content won't be removed

## Verification Issues

### Hash mismatch on `make verify`
1. Check if content changes were intentional
2. Re-run build: `make docsyn`
3. If changes are expected, update baseline:
   ```bash
   shasum -a 256 dist/DocSyn_Compiled.md | awk '{print $1}' > tests/BASELINE_SHA256
   ```
4. Document changes in CHANGELOG.md

### Deterministic build failures
1. Ensure UTF-8 encoding: `export PYTHONUTF8=1`
2. Check for:
   - System clock changes during build
   - File system case sensitivity issues
   - Concurrent access to files

## Output Quality

### Missing content in compiled output
1. Check `dist/VALIDATION.json` for structural issues
2. Verify source files are in `build.manifest.json`
3. Check file permissions and encoding

### Unicode characters not displaying correctly
1. Ensure terminal supports UTF-8
2. Check file encoding: `file -bi your-file.md`
3. Convert if needed: `iconv -f ISO-8859-1 -t UTF-8 file.md`

## Performance

### Slow builds
- Large files: Consider splitting into smaller modules
- Many files: Check if staging cleaner is running efficiently
- Debug: Add `--verbose` to individual scripts

## Getting Help

1. Check `dist/` for detailed JSON reports
2. Run `make verify` to confirm system state
3. Create GitHub issue with:
   - Error message
   - System info (`uname -a`, `python3 --version`, `make --version`)
   - Relevant report files (redact sensitive content)
