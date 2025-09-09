#!/usr/bin/env python3
"""
DocSyn Behavior Testing - Validate processing consistency and file handling

Tests:
1. File handling behavior (copy vs move, cleanup)
2. Incremental vs batch processing differences  
3. Reprocessing determinism
4. Output quality metrics
5. Staging area management

Usage: python test_docsyn_behavior.py
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent
STAGING = REPO_ROOT / "merge_pr" / "updated"
BLUEPRINTS = REPO_ROOT / "blueprints"
DIST = REPO_ROOT / "dist"

def sha256_file(path):
    """Calculate file hash for comparison"""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def backup_state():
    """Create snapshot of current state"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = DIST / f"test_backup_{timestamp}"
    backup_dir.mkdir(exist_ok=True)
    
    # Backup blueprints
    if BLUEPRINTS.exists():
        shutil.copytree(BLUEPRINTS, backup_dir / "blueprints")
    
    # Backup staging
    if STAGING.exists():
        shutil.copytree(STAGING, backup_dir / "staging")
        
    return backup_dir

def restore_state(backup_dir):
    """Restore from snapshot"""
    if BLUEPRINTS.exists():
        shutil.rmtree(BLUEPRINTS)
    if STAGING.exists():
        shutil.rmtree(STAGING)
        
    if (backup_dir / "blueprints").exists():
        shutil.copytree(backup_dir / "blueprints", BLUEPRINTS)
    if (backup_dir / "staging").exists():
        shutil.copytree(backup_dir / "staging", STAGING)

def create_test_documents():
    """Generate test documents with varying content"""
    docs = {
        "test_doc_1.md": '''---
blueprint: documenter
source: Test Document 1
---

# Test Document 1

This is a test document with unique content for testing incremental processing.

## Section A
Content specific to document 1.
''',
        "test_doc_2.md": '''---
blueprint: guardian  
source: Test Document 2
---

# Test Document 2

Different content for batch processing tests.

## Section B
Guardian-specific testing content.
''',
        "test_doc_3.md": '''---
blueprint: janitor
source: Test Document 3  
---

# Test Document 3

Third document for comprehensive testing.

## Section C  
Janitor blueprint testing content.
'''
    }
    return docs

def run_docsyn():
    """Execute the DocSyn pipeline"""
    try:
        result = subprocess.run(
            ["make", "docsyn"], 
            cwd=REPO_ROOT, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def analyze_output():
    """Analyze generated output quality"""
    compiled_file = DIST / "DocSyn_Compiled.md"
    if not compiled_file.exists():
        return {"error": "DocSyn_Compiled.md not found"}
    
    content = compiled_file.read_text()
    
    metrics = {
        "file_size": compiled_file.stat().st_size,
        "line_count": len(content.splitlines()),
        "word_count": len(content.split()),
        "char_count": len(content),
        "hash": sha256_file(compiled_file),
        "code_fence_count": content.count("```"),
        "heading_count": len([l for l in content.splitlines() if l.startswith("#")]),
        "global_sections": {
            "router_matrix": "Query-Pattern Matrix" in content,
            "risk_model": "Unified Risk & Control Model" in content,
            "dev_env": "Standard Development Environment" in content
        }
    }
    
    return metrics

def test_file_handling():
    """Test 1: Verify file handling behavior"""
    print("=== Test 1: File Handling Behavior ===")
    
    # Clear staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True, exist_ok=True)
    
    # Add test document
    test_docs = create_test_documents()
    test_file = STAGING / "test_doc_1.md"
    test_file.write_text(test_docs["test_doc_1.md"])
    
    print(f"Staged: {test_file}")
    print(f"Files in staging before promotion: {len(list(STAGING.glob('*.md')))}")
    
    # Run promotion only
    success, output = subprocess.run(
        ["python3", "scripts/promote_updated.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    ), ""
    
    files_after_promotion = len(list(STAGING.glob('*.md')))
    blueprint_files = len(list(BLUEPRINTS.glob('*.md')))
    
    print(f"Files in staging after promotion: {files_after_promotion}")
    print(f"Files in blueprints: {blueprint_files}")
    
    # Check if staging cleaner removes the duplicate
    subprocess.run(["python3", "scripts/clean_staging_duplicates.py", "--delete"], 
                  cwd=REPO_ROOT, capture_output=True)
    
    files_after_cleaning = len(list(STAGING.glob('*.md')))
    print(f"Files in staging after cleaning: {files_after_cleaning}")
    
    return {
        "promotion_preserves_originals": files_after_promotion > 0,
        "files_copied_to_blueprints": blueprint_files > 0,
        "cleaner_removes_duplicates": files_after_cleaning == 0
    }

def test_incremental_vs_batch():
    """Test 2: Compare incremental vs batch processing"""
    print("\n=== Test 2: Incremental vs Batch Processing ===")
    
    backup = backup_state()
    test_docs = create_test_documents()
    
    try:
        # Test incremental processing
        print("Testing incremental addition...")
        for i, (filename, content) in enumerate(test_docs.items(), 1):
            STAGING.mkdir(parents=True, exist_ok=True)
            (STAGING / filename).write_text(content)
            
            success, output = run_docsyn()
            if success:
                metrics = analyze_output()
                print(f"After adding doc {i}: {metrics['word_count']} words, hash: {metrics['hash'][:8]}")
        
        incremental_final = analyze_output()
        
        # Reset and test batch processing  
        restore_state(backup)
        print("\nTesting batch addition...")
        STAGING.mkdir(parents=True, exist_ok=True)
        
        # Add all documents at once
        for filename, content in test_docs.items():
            (STAGING / filename).write_text(content)
        
        success, output = run_docsyn()
        batch_final = analyze_output()
        
        print(f"Incremental final: {incremental_final['word_count']} words, hash: {incremental_final['hash'][:8]}")
        print(f"Batch final: {batch_final['word_count']} words, hash: {batch_final['hash'][:8]}")
        
        return {
            "incremental_metrics": incremental_final,
            "batch_metrics": batch_final,
            "identical_output": incremental_final['hash'] == batch_final['hash']
        }
        
    finally:
        restore_state(backup)

def test_reprocessing_determinism():
    """Test 3: Verify reprocessing produces identical results"""
    print("\n=== Test 3: Reprocessing Determinism ===")
    
    backup = backup_state()
    test_docs = create_test_documents()
    
    try:
        STAGING.mkdir(parents=True, exist_ok=True)
        
        # Add documents and process
        for filename, content in test_docs.items():
            (STAGING / filename).write_text(content)
        
        run_docsyn()
        first_run = analyze_output()
        
        # Process again without changes
        run_docsyn()
        second_run = analyze_output()
        
        # Process again with staging cleaner
        subprocess.run(["python3", "scripts/clean_staging_duplicates.py", "--delete"], 
                      cwd=REPO_ROOT, capture_output=True)
        run_docsyn()
        third_run = analyze_output()
        
        print(f"First run hash: {first_run['hash'][:8]}")
        print(f"Second run hash: {second_run['hash'][:8]}")  
        print(f"Third run hash: {third_run['hash'][:8]}")
        
        return {
            "first_run": first_run,
            "second_run": second_run,
            "third_run": third_run,
            "deterministic": (first_run['hash'] == second_run['hash'] == third_run['hash'])
        }
        
    finally:
        restore_state(backup)

def test_quality_metrics():
    """Test 4: Comprehensive output quality analysis"""
    print("\n=== Test 4: Quality Metrics Analysis ===")
    
    backup = backup_state()
    
    try:
        # Test with current real content
        run_docsyn()
        real_metrics = analyze_output()
        
        # Test with minimal content
        STAGING.mkdir(parents=True, exist_ok=True)
        minimal_doc = STAGING / "minimal.md"
        minimal_doc.write_text("---\nblueprint: documenter\n---\n# Minimal\nShort content.")
        
        run_docsyn()
        minimal_metrics = analyze_output()
        
        print("Real content metrics:")
        for key, value in real_metrics.items():
            if key != "hash":
                print(f"  {key}: {value}")
                
        print("\nMinimal content metrics:")
        for key, value in minimal_metrics.items():
            if key != "hash":
                print(f"  {key}: {value}")
        
        return {
            "real_content": real_metrics,
            "minimal_content": minimal_metrics,
            "quality_preserved": real_metrics["global_sections"]["router_matrix"]
        }
        
    finally:
        restore_state(backup)

def main():
    """Run all tests"""
    print("DocSyn Behavior Testing")
    print("=" * 50)
    
    results = {}
    
    # Run tests
    results["file_handling"] = test_file_handling()
    results["incremental_vs_batch"] = test_incremental_vs_batch()
    results["determinism"] = test_reprocessing_determinism()
    results["quality"] = test_quality_metrics()
    
    # Generate report
    report_file = DIST / "BEHAVIOR_TEST_REPORT.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Test Summary ===")
    print(f"File handling working: {results['file_handling']['cleaner_removes_duplicates']}")
    print(f"Incremental vs batch identical: {results['incremental_vs_batch']['identical_output']}")
    print(f"Reprocessing deterministic: {results['determinism']['deterministic']}")
    print(f"Quality preserved: {results['quality']['quality_preserved']}")
    print(f"\nDetailed report: {report_file}")

if __name__ == "__main__":
    main()
