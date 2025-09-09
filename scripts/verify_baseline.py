#!/usr/bin/env python3
"""
Verify DocSyn build matches baseline hash
"""
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent  # Go up from scripts/ to repo root
BASELINE_FILE = REPO_ROOT / "tests" / "BASELINE_SHA256"
COMPILED_FILE = REPO_ROOT / "dist" / "DocSyn_Compiled.md"

def main():
    if not BASELINE_FILE.exists():
        print("No baseline found. Create tests/BASELINE_SHA256 first.")
        return 2
    
    if not COMPILED_FILE.exists():
        print("DocSyn_Compiled.md not found. Run 'make docsyn' first.")
        return 1
    
    # Get current hash
    current_hash = hashlib.sha256(COMPILED_FILE.read_bytes()).hexdigest()
    
    # Get baseline hash
    baseline_hash = BASELINE_FILE.read_text().strip()
    
    if current_hash == baseline_hash:
        print(f"OK: baseline match ({current_hash[:8]})")
        return 0
    else:
        print("Hash mismatch!")
        print(f" got: {current_hash}")
        print(f"base: {baseline_hash}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
