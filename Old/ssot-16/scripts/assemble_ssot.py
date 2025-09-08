#!/usr/bin/env python3
import json, sys, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT/"build.manifest.json"
OUT = ROOT/"SSOT.md"

def read(p: Path):
    try: return p.read_text(encoding="utf-8")
    except: return p.read_text(errors="ignore")

def main():
    if not MANIFEST.exists():
        print("No build.manifest.json"); sys.exit(1)
    mani = json.loads(MANIFEST.read_text(encoding="utf-8"))
    
    # Backward-compatible: check for curated_sources (preferred) or sections (legacy)
    sources = mani.get("curated_sources", mani.get("sections", []))
    if not sources:
        print("[error] No curated_sources or sections found in manifest"); sys.exit(1)
    
    # Create dist directory
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    
    # Load parts
    curated = [ROOT / p for p in sources]
    core = [p for p in curated if p.parts[-2] == "core"]
    blue = [p for p in curated if p.parts[-2] == "blueprints"]
    
    def read_safe(p: Path) -> str:
        if not p.exists():
            print(f"[warn] missing: {p.relative_to(ROOT)}")
            return ""
        if p.name.endswith(".SOURCED.md"):
            return ""
        return read(p).strip()
    
    partA = "\n\n".join(read_safe(p) for p in core if read_safe(p))
    partB = "\n\n---\n\n".join(read_safe(p) for p in blue if read_safe(p))
    
    from datetime import datetime
    banner = f"# Single Source of Truth (SSOT)\n\n> Build: {datetime.utcnow().isoformat()}Z\n\n"
    
    # Normalize and deduplicate
    def normalize(md: str) -> str:
        md = re.sub(r"\n{3,}", "\n\n", md)
        return md if md.endswith("\n") else md + "\n"
    
    ssot = normalize(banner + partA + "\n---\n\n" + partB)
    
    # Deduplicate consecutive identical H1s
    lines = ssot.splitlines()
    out = []
    prev_h = None
    for ln in lines:
        m = re.match(r"^#\s+(.+)$", ln)
        if m:
            h = m.group(1).strip().lower()
            if h == prev_h:
                continue
            prev_h = h
        out.append(ln)
    ssot = "\n".join(out) + "\n"
    
    # Write outputs
    (dist / "PartA_Core.md").write_text(partA, encoding="utf-8")
    (dist / "PartB_Blueprints.md").write_text(partB, encoding="utf-8")
    (dist / "SSOT.md").write_text(ssot, encoding="utf-8")
    OUT.write_text(ssot, encoding="utf-8")  # Also write to root for compatibility
    
    print(f"✅ Assembled {dist / 'SSOT.md'} ({len(ssot)} chars)")
    print(f"   Core: {len(partA)} chars, Blueprints: {len(partB)} chars")
if __name__ == "__main__":
    main()
