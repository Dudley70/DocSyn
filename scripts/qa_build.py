#!/usr/bin/env python3
"""
Quality assurance checks for DocSyn builds.
Ensures clean, consistent output free of contamination from previous document batches.
Supports policy-aware validation for vendor-specific content.
"""

import re
import json
import sys
try:
    import yaml  # PyYAML
except ModuleNotFoundError:
    print("[ERROR] Missing dependency: PyYAML. Install with:")
    print("  pip install -r scripts/requirements.txt")
    raise
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
COMPILED_FILE = DIST_DIR / "DocSyn_Compiled.md"

# Constants for policy-aware validation
FORBIDDEN_TERMS = ["Claude Code", "Claude AI", "Single Source of Truth"]
MIN_BYTES_BLUEPRINT = 1000

# Helper: read YAML front-matter if present
def read_front_matter(path: Path):
    if yaml is None:
        return {}  # Skip YAML parsing if module not available
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm = text[3:end].strip()
                return yaml.safe_load(fm) or {}
    except Exception:
        pass
    return {}

# Helper: policy classification
def is_vendor_specific(path: Path, fm: dict) -> bool:
    if str(path).startswith("blueprints/vendor/"):
        return True
    if fm.get("policy") == "vendor-specific":
        return True
    tags = fm.get("tags") or []
    if isinstance(tags, list) and any(t.lower() in {"vendor", "claude"} for t in tags):
        return True
    return False

def is_anchor(path: Path, fm: dict) -> bool:
    return bool(fm.get("anchor") is True)

def check_forbidden_terms():
    """Check for forbidden terms with policy awareness for vendor-specific files."""
    problems = []
    warnings = []
    
    for path in Path(ROOT / "blueprints").rglob("*.md"):
        fm = read_front_matter(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [t for t in FORBIDDEN_TERMS if t in text]
        
        if hits:
            rel_path = str(path.relative_to(ROOT))
            if is_vendor_specific(path, fm):
                warnings.append((rel_path, hits))
            else:
                problems.append((rel_path, hits))
    
    return {"forbidden_problems": problems, "forbidden_warnings": warnings}

def check_blueprint_sizes():
    """Check blueprint file sizes with anchor exemption."""
    small = []
    for path in Path(ROOT / "blueprints").rglob("*.md"):
        fm = read_front_matter(path)
        if is_anchor(path, fm):   # anchor files are exempt
            continue
        if path.stat().st_size < MIN_BYTES_BLUEPRINT:
            small.append(str(path.relative_to(ROOT)))
    return {"small_blueprints": small}

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

def check_required_files():
    """Ensure structural files required for automation are present."""
    REQUIRED = [
        "core/00-router.SOURCED.md",
        "core/00-router.md",
        "blueprints/documenter.md",
        "blueprints/guardian.md",
        "blueprints/janitor.md",
        "blueprints/tester.md",
        "blueprints/cicd-analyst.md",
        "blueprints/orchestrator.md",
        "blueprints/adaptive-learning.md",
    ]
    
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    return {"required_missing": missing}

def check_router_contract():
    """Ensure router contains expected route codes and mappings."""
    expected_routes = {
        "CH4-BP-DOC": "blueprints/documenter.md",
        "CH4-BP-GRD": "blueprints/guardian.md",
        "CH4-BP-JAN": "blueprints/janitor.md",
        "CH4-BP-TST": "blueprints/tester.md",
        "CH4-BP-CICD": "blueprints/cicd-analyst.md",
        "CH4-BP-ORCH": "blueprints/orchestrator.md",
        "CH4-BP-ADAPT": "blueprints/adaptive-learning.md",
    }
    
    router_file = ROOT / "core" / "00-router.md"
    if not router_file.exists():
        return {"router_contract": "FAIL", "error": "Router file missing"}
    
    router = router_file.read_text(encoding="utf-8")
    missing_codes = []
    missing_mappings = []
    
    for code, target in expected_routes.items():
        if code not in router:
            missing_codes.append(code)
        # Check that the target file exists
        if not (ROOT / target).exists():
            missing_mappings.append(target)
    
    if missing_codes or missing_mappings:
        return {
            "router_contract": "FAIL",
            "missing_codes": missing_codes,
            "missing_mappings": missing_mappings
        }
    
    return {"router_contract": "OK"}

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
    report["checks"]["blueprint_sizes"] = check_blueprint_sizes()
    report["checks"]["unicode"] = check_unicode_integrity()
    report["checks"]["required_files"] = check_required_files()
    report["checks"]["router_contract"] = check_router_contract()
    report["checks"]["determinism"] = check_determinism()
    
    # Check for failures (only problems, not warnings)
    has_failures = (
        bool(report["checks"]["forbidden_terms"]["forbidden_problems"]) or
        bool(report["checks"]["blueprint_sizes"]["small_blueprints"]) or
        report["checks"]["unicode"]["unicode_check"] != "OK" or
        bool(report["checks"]["required_files"]["required_missing"]) or
        report["checks"]["router_contract"]["router_contract"] != "OK" or
        report["checks"]["determinism"]["determinism"] != "OK"
    )
    
    # Handle forbidden terms with policy awareness
    forbidden_check = report["checks"]["forbidden_terms"]
    if forbidden_check["forbidden_problems"]:
        print("❌ FORBIDDEN TERMS IN NON-VENDOR FILES:")
        for file, terms in forbidden_check["forbidden_problems"]:
            print(f"   {file}: {', '.join(terms)}")
    else:
        print("✅ Forbidden terms check: CLEAN")
    
    if forbidden_check["forbidden_warnings"]:
        print("⚠️  VENDOR-SPECIFIC TERMS (ALLOWED):")
        for file, terms in forbidden_check["forbidden_warnings"]:
            print(f"   {file}: {', '.join(terms)}")
    
    # Handle blueprint sizes
    if report["checks"]["blueprint_sizes"]["small_blueprints"]:
        print("❌ SMALL BLUEPRINT FILES (non-anchors):")
        for file in report["checks"]["blueprint_sizes"]["small_blueprints"]:
            print(f"   {file}")
    else:
        print("✅ Blueprint sizes check: OK")
    
    if report["checks"]["unicode"]["unicode_check"] != "OK":
        print(f"❌ Unicode check: {report['checks']['unicode'].get('error', 'FAIL')}")
    else:
        print("✅ Unicode integrity: OK")
    
    if report["checks"]["required_files"]["required_missing"]:
        print("❌ REQUIRED FILES MISSING:")
        for file in report["checks"]["required_files"]["required_missing"]:
            print(f"   {file}")
    else:
        print("✅ Required files check: OK")
    
    if report["checks"]["router_contract"]["router_contract"] != "OK":
        router_check = report["checks"]["router_contract"]
        print(f"❌ Router contract check: {router_check.get('error', 'FAIL')}")
        if "missing_codes" in router_check:
            print(f"   Missing codes: {router_check['missing_codes']}")
        if "missing_mappings" in router_check:
            print(f"   Missing files: {router_check['missing_mappings']}")
    else:
        print("✅ Router contract check: OK")
    
    if report["checks"]["determinism"]["determinism"] != "OK":
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
        f"- Forbidden Terms: {'FAIL' if report['checks']['forbidden_terms']['forbidden_problems'] else 'PASS'}",
        f"- Blueprint Sizes: {'FAIL' if report['checks']['blueprint_sizes']['small_blueprints'] else 'PASS'}",
        f"- Unicode Integrity: {report['checks']['unicode']['unicode_check']}",
        f"- Required Files: {'FAIL' if report['checks']['required_files']['required_missing'] else 'PASS'}",
        f"- Router Contract: {report['checks']['router_contract']['router_contract']}",
        f"- Deterministic Build: {report['checks']['determinism']['determinism']}",
        "",
    ]
    
    if report["checks"]["required_files"]["required_missing"]:
        summary_lines.extend([
            "## Missing Required Files:",
            *[f"- {file}" for file in report["checks"]["required_files"]["required_missing"]],
            ""
        ])
    
    if report["checks"]["router_contract"]["router_contract"] != "OK":
        summary_lines.extend([
            "## Router Contract Issues:",
            f"- Status: {report['checks']['router_contract']['router_contract']}",
            ""
        ])
        if "missing_codes" in report["checks"]["router_contract"]:
            summary_lines.extend([
                "### Missing Route Codes:",
                *[f"- {code}" for code in report["checks"]["router_contract"]["missing_codes"]],
                ""
            ])
        if "missing_mappings" in report["checks"]["router_contract"]:
            summary_lines.extend([
                "### Missing Blueprint Files:",
                *[f"- {file}" for file in report["checks"]["router_contract"]["missing_mappings"]],
                ""
            ])
    
    # Add forbidden terms issues
    forbidden_check = report["checks"]["forbidden_terms"]
    if forbidden_check["forbidden_problems"]:
        summary_lines.extend([
            "## Forbidden Terms in Non-Vendor Files:",
            *[f"- {file}: {', '.join(terms)}" for file, terms in forbidden_check["forbidden_problems"]],
            ""
        ])
    
    if forbidden_check["forbidden_warnings"]:
        summary_lines.extend([
            "## Vendor-Specific Terms (Allowed):",
            *[f"- {file}: {', '.join(terms)}" for file, terms in forbidden_check["forbidden_warnings"]],
            ""
        ])
    
    # Add small blueprint files
    if report["checks"]["blueprint_sizes"]["small_blueprints"]:
        summary_lines.extend([
            "## Small Blueprint Files (Non-Anchors):",
            *[f"- {file}" for file in report["checks"]["blueprint_sizes"]["small_blueprints"]],
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
