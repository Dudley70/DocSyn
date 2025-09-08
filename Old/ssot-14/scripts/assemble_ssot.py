\
#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

def read(p: Path)->str:
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def normalize(md: str)->str:
    import re
    md = re.sub(r"\n{3,}", "\n\n", md)
    if not md.endswith("\n"):
        md += "\n"
    return md

def main():
    manifest = json.loads(read(ROOT / "build.manifest.json"))
    cfg = json.loads('{"IGNORE_HEADINGS": []}')
    # merge_config.yaml is guidance; assembler here assumes curated files are pre-cleaned
    curated = [ROOT / p for p in manifest["curated_sources"]]
    dist = ROOT / "dist"; dist.mkdir(exist_ok=True)

    # Load parts
    core = [p for p in curated if p.parts[-2] == "core"]
    blue = [p for p in curated if p.parts[-2] == "blueprints"]

    partA = "\n\n".join(read(p) for p in core)
    partB = "\n\n---\n\n".join(read(p) for p in blue)

    banner = f"# Single Source of Truth (SSOT)\\n\\n> Build: {datetime.utcnow().isoformat()}Z\\n\\n"

    ssot = normalize(banner + partA + "\\n---\\n\\n" + partB)

    # Deduplicate consecutive identical H1s
    lines = ssot.splitlines()
    out = []
    prev_h = None
    for ln in lines:
        m = re.match(r"^#\\s+(.+)$", ln)
        if m:
            h = m.group(1).strip().lower()
            if h == prev_h:
                continue
            prev_h = h
        out.append(ln)
    ssot = "\\n".join(out) + "\\n"

    (dist / "PartA_Core.md").write_text(partA, encoding="utf-8")
    (dist / "PartB_Blueprints.md").write_text(partB, encoding="utf-8")
    (dist / "SSOT.md").write_text(ssot, encoding="utf-8")

if __name__ == "__main__":
    sys.exit(main())
