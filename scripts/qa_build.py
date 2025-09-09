#!/usr/bin/env python3
"""
Quality assurance checks for DocSyn builds.
Ensures clean, consistent output free of contamination from previous document batches.
"""

import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
COMPILED_FILE = DIST_DIR / "DocSyn_Compiled.md"

def check_forbidden_terms():
    """Check for terms that shouldn't appear in cleaned builds."""
    FORBIDDEN = [
        r"Claude Code",
        r"Claude AI",
        r"SSOT\.md",  # Old filename references
        r"Single Source of Truth",  # Old terminology
    ]
    
    if not COMPILED_FILE.exists():
        return {"forbidden_terms": [], "error": "Compiled file not found"}
    
    content = COMPILED_FILE.read_text(encoding="utf-8")
    bad = []
    
    for pattern in FORBIDDEN:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            bad.extend([f"{pattern}: {len(matches)} occurrences"])
    
    return {"forbidden_terms": bad}

def check_unicode_integrity():
    """Ensure proper Unicode handling."""
    if not COMPILED_FILE.exists():
        return {"unicode_check": "FAIL", "error": "Compiled file not found"}
    
    try:
        content = COMPILED_FILE.read_text(encoding="utf-8")
        # Try to normalize - this will fail if there are encoding issues
        import unicodedata
        normalized = unicodedata.normalize("NFC", content)
        return {"unicode_check": "OK", "length": len(content)}
    except UnicodeDecodeError as e:
        return {"unicode_check": "FAIL", "error": str(e)}

def check_determinism():
    """Verify build determinism by checking if multiple builds produce same hash."""
    if not COMPILED_FILE.exists():
        return {"determinism": "FAIL", "error": "Compiled file not found"}
    
    baseline_file = ROOT / "tests" / "BASELINE_SHA256"
    if not baseline_file.exists():
        return {"determinism": "UNKNOWN", "error": "Baseline not found"}
    
    import hashlib
    current_hash = hashlib.sha256(COMPILED_FILE.read_bytes()).hexdigest()
    baseline_hash = baseline_file.read_text().strip()
    
    return {
        "determinism": "OK" if current_hash == baseline_hash else "FAIL",
        "current_hash": current_hash,
        "baseline_hash": baseline_hash
    }

def main():
    """Run all QA checks and generate report."""
    report = {
        "timestamp": str(Path().cwd()),
        "checks": {}
    }
    
    # Run all checks
    report["checks"]["forbidden_terms"] = check_forbidden_terms()
    report["checks"]["unicode"] = check_unicode_integrity()
    report["checks"]["determinism"] = check_determinism()
    
    # Check for failures
    has_failures = False
    
    if report["checks"]["forbidden_terms"]["forbidden_terms"]:
        has_failures = True
        print("❌ FORBIDDEN TERMS DETECTED:")
        for term in report["checks"]["forbidden_terms"]["forbidden_terms"]:
            print(f"   {term}")
    else:
        print("✅ Forbidden terms check: CLEAN")
    
    if report["checks"]["unicode"]["unicode_check"] != "OK":
        has_failures = True
        print(f"❌ Unicode check: {report['checks']['unicode'].get('error', 'FAIL')}")
    else:
        print("✅ Unicode integrity: OK")
    
    if report["checks"]["determinism"]["determinism"] != "OK":
        has_failures = True
        print(f"❌ Determinism check: {report['checks']['determinism'].get('error', 'Hash mismatch')}")
    else:
        print("✅ Deterministic build: OK")
    
    # Write detailed report
    qa_file = DIST_DIR / "QA_SUMMARY.txt"
    DIST_DIR.mkdir(exist_ok=True)
    
    summary_lines = [
        "# DocSyn QA Summary",
        "",
        f"Build Status: {'FAIL' if has_failures else 'PASS'}",
        "",
        "## Checks:",
        f"- Forbidden Terms: {'FAIL' if report['checks']['forbidden_terms']['forbidden_terms'] else 'PASS'}",
        f"- Unicode Integrity: {report['checks']['unicode']['unicode_check']}",
        f"- Deterministic Build: {report['checks']['determinism']['determinism']}",
        "",
    ]
    
    if report["checks"]["forbidden_terms"]["forbidden_terms"]:
        summary_lines.extend([
            "## Forbidden Terms Found:",
            *[f"- {term}" for term in report["checks"]["forbidden_terms"]["forbidden_terms"]],
            ""
        ])
    
    qa_file.write_text("\n".join(summary_lines), encoding="utf-8")
    
    # Write detailed JSON report
    json_file = DIST_DIR / "QA_REPORT.json"
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 QA report: {qa_file}")
    print(f"📊 Detailed JSON: {json_file}")
    
    return 0 if not has_failures else 1

if __name__ == "__main__":
    sys.exit(main())
