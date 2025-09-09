#!/usr/bin/env python3
import shutil, sys, time, json, os, re
from pathlib import Path
from typing import Optional

PROJ = Path(__file__).resolve().parents[1]
UPDATED = PROJ / "merge_pr" / "updated"
BLUEPRINTS = PROJ / "blueprints"
CORE = PROJ / "core"
BACKUPS = PROJ / "dist" / "backups" / "blueprints"
DIST = PROJ / "dist"
BACKUPS.mkdir(parents=True, exist_ok=True)
DIST.mkdir(exist_ok=True)

def _slugify(bp: str) -> str:
    """Convert blueprint name to safe filename slug."""
    return re.sub(r"[^a-z0-9._-]+", "-", bp.lower()).strip("-._") or "unnamed"

def ensure_blueprint_stub(slug: str, title: Optional[str] = None) -> bool:
    """Create blueprints/<slug>.md if missing (empty anchor, UTF-8, NFC)."""
    path = BLUEPRINTS / f"{slug}.md"
    if path.exists(): 
        return False
    
    title = title or slug.replace('-', ' ').title()
    content = f"""---
blueprint: {slug}
owner: TBD
tags: [blueprint, anchor]
---

# {title}

## Objective
Provide {slug.replace('-', ' ')} functionality.

## Snippets
Short, actionable snippets belong here.

---

<!-- Content will be populated from document processing -->
"""
    
    # Ensure UTF-8 NFC normalization
    import unicodedata
    content = unicodedata.normalize("NFC", content)
    path.write_text(content, encoding="utf-8")
    return True

def suggest_router_mapping(slug: str, code_hint: Optional[str] = None) -> None:
    """Append a non-blocking suggestion to dist/ROUTER_SUGGESTIONS.txt."""
    code = code_hint or f"CH4-BP-{slug.replace('-', '').upper()[:6]}"
    line = f"{code} → blueprints/{slug}.md\n"
    suggestions_file = DIST / "ROUTER_SUGGESTIONS.txt"
    
    # Check if suggestion already exists
    if suggestions_file.exists():
        existing = suggestions_file.read_text(encoding="utf-8")
        if line.strip() in existing:
            return
    
    with suggestions_file.open("a", encoding="utf-8") as f:
        f.write(line)

def parse_front_matter(content: str) -> dict:
    """Extract YAML front-matter from markdown content."""
    lines = content.split('\n')
    if not lines or not lines[0].strip() == '---':
        return {}
    
    try:
        end_idx = lines[1:].index('---') + 1
        front_matter_lines = lines[1:end_idx]
        
        # Simple YAML parser for basic key: value pairs
        metadata = {}
        for line in front_matter_lines:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                metadata[key] = value
        
        return metadata
    except (ValueError, IndexError):
        return {}

def determine_target_path(src_path: Path, metadata: dict) -> Path:
    """Determine where to promote the file based on front-matter."""
    # Check for part: A (goes to core)
    if metadata.get('part') == 'A':
        return CORE / src_path.name
    
    # Check for blueprint: <slug> (goes to blueprints)
    if 'blueprint' in metadata:
        blueprint_slug = metadata['blueprint']
        slug = _slugify(blueprint_slug)
        
        # Ensure blueprint anchor exists
        created = ensure_blueprint_stub(slug, blueprint_slug)
        if created:
            suggest_router_mapping(slug)
            print(f"[INFO] Created blueprint anchor: blueprints/{slug}.md")
            print(f"[INFO] Router suggestion logged: see dist/ROUTER_SUGGESTIONS.txt")
        
        return BLUEPRINTS / f"{slug}.md"
    
    # Default: goes to blueprints with original filename
    return BLUEPRINTS / src_path.name

def main():
    ts = time.strftime("%Y%m%d-%H%M%S")
    snap = BACKUPS / f"pre-promotion-{ts}"
    snap.mkdir(parents=True, exist_ok=True)
    
    # backup current blueprints
    for p in BLUEPRINTS.glob("*.md"):
        shutil.copy2(p, snap / p.name)

    # keep previous sizes for shrink check
    sizes_prev = {p.name: p.stat().st_size for p in BLUEPRINTS.glob("*.md")}

    # promote with front-matter awareness
    promoted = []
    auto_created = []
    
    for src in UPDATED.glob("*.md"):
        try:
            content = src.read_text(encoding="utf-8")
            metadata = parse_front_matter(content)
            dst = determine_target_path(src, metadata)
            
            # Ensure target directory exists
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Promote the file
            shutil.copy2(src, dst)
            promoted.append(f"{src.name} → {dst.relative_to(PROJ)}")
            
            # Track auto-created blueprints
            if 'blueprint' in metadata:
                slug = _slugify(metadata['blueprint'])
                if (BLUEPRINTS / f"{slug}.md").exists() and slug != src.stem:
                    auto_created.append(f"{slug}.md")
                    
        except Exception as e:
            print(f"[WARN] Failed to promote {src.name}: {e}")
            # Fallback to original behavior
            dst = BLUEPRINTS / src.name
            shutil.copy2(src, dst)
            promoted.append(f"{src.name} → {dst.relative_to(PROJ)} (fallback)")

    # safety net: no shrinks > 20%
    sizes_new = {p.name: p.stat().st_size for p in BLUEPRINTS.glob("*.md")}
    shrunk = []
    for name, new_size in sizes_new.items():
        prev = sizes_prev.get(name, 0)
        if prev > 0 and new_size < prev * 0.8:
            shrunk.append((name, prev, new_size))

    report = {
        "timestamp": ts,
        "promoted": promoted,
        "auto_created_blueprints": auto_created,
        "sizes_previous": sizes_prev,
        "sizes_new": sizes_new,
        "shrunk_gt_20pct": shrunk
    }
    
    (DIST / "PROMOTION_REPORT.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    # Summary output
    if promoted:
        print(f"[INFO] Promoted {len(promoted)} files:")
        for p in promoted:
            print(f"  - {p}")
    
    if auto_created:
        print(f"[INFO] Auto-created {len(auto_created)} blueprint anchors:")
        for a in auto_created:
            print(f"  - {a}")
        print("[INFO] Check dist/ROUTER_SUGGESTIONS.txt for router mappings to add")
    
    if shrunk:
        print("[WARN] Some blueprints shrank > 20%:", shrunk)

if __name__ == "__main__":
    main()
