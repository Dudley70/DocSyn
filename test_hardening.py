#!/usr/bin/env python3
"""
Quick hardening tests for DocSyn before version upgrade
Runtime: ~20 minutes total
"""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
STAGING = REPO_ROOT / "merge_pr" / "updated"
DIST = REPO_ROOT / "dist"

def get_build_hash():
    """Get hash of compiled output"""
    result = subprocess.run(["make", "docsyn"], cwd=REPO_ROOT, capture_output=True)
    if result.returncode != 0:
        return None
    compiled = DIST / "DocSyn_Compiled.md"
    return hashlib.sha256(compiled.read_bytes()).hexdigest()[:8]

def test_order_determinism():
    """Test 1: File order shouldn't affect output (5 min)"""
    print("=== Test: Order Determinism ===")
    
    # Create test files with different names to test ordering
    test_files = {
        "a_first.md": "---\nblueprint: documenter\n---\n# A First\nContent A",
        "z_last.md": "---\nblueprint: guardian\n---\n# Z Last\nContent Z", 
        "m_middle.md": "---\nblueprint: janitor\n---\n# M Middle\nContent M"
    }
    
    # Clear staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    # Test 1: Add in alphabetical order
    for name, content in test_files.items():
        (STAGING / name).write_text(content)
    hash1 = get_build_hash()
    
    # Clear and test 2: Add in reverse order  
    shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    for name, content in reversed(test_files.items()):
        (STAGING / name).write_text(content)
    hash2 = get_build_hash()
    
    # Cleanup
    shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    print(f"Order 1 hash: {hash1}")
    print(f"Order 2 hash: {hash2}")
    return {"deterministic": hash1 == hash2, "hash1": hash1, "hash2": hash2}

def test_idempotent_promotion():
    """Test 2: Multiple runs don't change state (2 min)"""
    print("\n=== Test: Idempotent Promotion ===")
    
    # First run
    hash1 = get_build_hash()
    
    # Second run without changes
    hash2 = get_build_hash()
    
    print(f"Run 1 hash: {hash1}")
    print(f"Run 2 hash: {hash2}")
    return {"idempotent": hash1 == hash2}

def test_line_endings():
    """Test 3: Line endings don't affect output (3 min)"""
    print("\n=== Test: Line Endings ===")
    
    # Clear staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    # Create file with Unix line endings
    test_content = "---\nblueprint: documenter\n---\n# Test\nLine 1\nLine 2\n"
    test_file = STAGING / "line_test.md"
    test_file.write_text(test_content)
    hash1 = get_build_hash()
    
    # Convert to Windows line endings
    windows_content = test_content.replace('\n', '\r\n')
    test_file.write_bytes(windows_content.encode('utf-8'))
    hash2 = get_build_hash()
    
    # Cleanup
    shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    print(f"Unix endings: {hash1}")
    print(f"Windows endings: {hash2}")
    return {"line_endings_safe": hash1 == hash2}

def test_encoding_chars():
    """Test 4: Unicode/emoji handling (3 min)"""
    print("\n=== Test: Unicode Characters ===")
    
    # Clear staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    # Test with international chars and emoji
    unicode_content = """---
blueprint: documenter
source: Test with émojis 🚀
---

# Test Ünïcødé

Some content with:
- Émojis: 🎯 ✅ 📊
- Accents: café, naïve, résumé  
- Symbols: → ← ↑ ↓
- Non-breaking space: word word
"""
    
    test_file = STAGING / "unicode_test.md"
    test_file.write_text(unicode_content, encoding='utf-8')
    
    try:
        hash1 = get_build_hash()
        success = hash1 is not None
        
        # Check output renders correctly
        compiled = DIST / "DocSyn_Compiled.md"
        output_content = compiled.read_text(encoding='utf-8')
        has_emoji = "🚀" in output_content
        has_accents = "café" in output_content
        
    except Exception as e:
        success = False
        has_emoji = False
        has_accents = False
        print(f"Unicode test failed: {e}")
    
    # Cleanup
    shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    print(f"Unicode build: {'✅' if success else '❌'}")
    print(f"Emoji preserved: {'✅' if has_emoji else '❌'}")
    print(f"Accents preserved: {'✅' if has_accents else '❌'}")
    
    return {
        "unicode_builds": success,
        "emoji_preserved": has_emoji, 
        "accents_preserved": has_accents
    }

def test_frontmatter_edge_cases():
    """Test 5: YAML front-matter handling (5 min)"""
    print("\n=== Test: Front-matter Edge Cases ===")
    
    # Clear staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    edge_cases = {
        "no_frontmatter.md": "# No YAML\nJust content",
        "empty_frontmatter.md": "---\n---\n# Empty YAML\nContent",
        "conflicting.md": "---\npart: A\nblueprint: documenter\n---\n# Conflict\nShould stay in triage"
    }
    
    for name, content in edge_cases.items():
        (STAGING / name).write_text(content)
    
    hash1 = get_build_hash()
    
    # Check promotion report
    promo_report = DIST / "PROMOTION_REPORT.json"
    if promo_report.exists():
        report = json.loads(promo_report.read_text())
        promoted_files = report.get("promoted", [])
    else:
        promoted_files = []
    
    # Cleanup
    shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    print(f"Front-matter test hash: {hash1}")
    print(f"Files promoted: {len(promoted_files)}")
    
    return {
        "frontmatter_handled": hash1 is not None,
        "files_promoted": len(promoted_files)
    }

def test_staging_hygiene():
    """Test 6: Check staging cleanup (1 min)"""
    print("\n=== Test: Staging Hygiene ===")
    
    # Run clean build
    hash1 = get_build_hash()
    
    # Check what's left in staging
    staging_files = list(STAGING.glob("*.md")) if STAGING.exists() else []
    
    print(f"Files remaining in staging: {len(staging_files)}")
    for f in staging_files:
        print(f"  - {f.name}")
    
    return {
        "staging_file_count": len(staging_files),
        "staging_files": [f.name for f in staging_files]
    }

def main():
    """Run quick hardening test suite"""
    print("DocSyn Quick Hardening Tests")
    print("=" * 40)
    
    results = {}
    
    # Run tests
    results["order_determinism"] = test_order_determinism()
    results["idempotent_promotion"] = test_idempotent_promotion()  
    results["line_endings"] = test_line_endings()
    results["unicode_handling"] = test_encoding_chars()
    results["frontmatter_edges"] = test_frontmatter_edge_cases()
    results["staging_hygiene"] = test_staging_hygiene()
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Order deterministic: {results['order_determinism']['deterministic']}")
    print(f"Idempotent promotion: {results['idempotent_promotion']['idempotent']}")
    print(f"Line endings safe: {results['line_endings']['line_endings_safe']}")
    print(f"Unicode builds: {results['unicode_handling']['unicode_builds']}")
    print(f"Front-matter handled: {results['frontmatter_edges']['frontmatter_handled']}")
    print(f"Staging files: {results['staging_hygiene']['staging_file_count']}")
    
    # Save detailed report
    report_file = DIST / "HARDENING_TEST_REPORT.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed report: {report_file}")

if __name__ == "__main__":
    main()
