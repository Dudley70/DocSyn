#!/usr/bin/env python3
import re, json, hashlib
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
DIST = PROJ / "dist"
BPS  = PROJ / "blueprints"

# targets we consider "global"
GLOBAL_TITLES = [
    "Query-Pattern Matrix",
    "Unified Risk",
    "Unified Risk & Control Model",
    "Standard Development Environment",
    "Agent Query Index",
    "High-Level Risk",
]

def norm(txt: str) -> str:
    # normalize for fingerprinting: lowercase, strip spaces/punct
    t = txt.lower()
    t = re.sub(r"[\s\|`*_>:\-]+", "", t)
    t = re.sub(r"[\p{P}]+", "", t) if hasattr(re, "FULLCASE") else t  # fallback: already stripped above
    return t

def split_sections(text: str):
    # yields (title,line_index) for headings H1-H3 (normal or escaped)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s{0,3}#{1,3}\s+", line) or re.match(r"^\s{0,3}\\#{1,3}\s+", line):
            title = re.sub(r"^\s{0,3}(?:\\)?#{1,3}\s+", "", line).strip()
            yield (title, i)
    return

def extract_global_blocks_from_partA(partA: str):
    # Extract blocks for the three key globals by heading ranges
    lines = partA.splitlines()
    sections = list(split_sections(partA))
    blocks = {}
    def block_text(start_idx, end_idx):
        return "\n".join(lines[start_idx:end_idx])

    for idx, (title, line_i) in enumerate(sections):
        title_clean = re.sub(r"^\d+\.\s*", "", title).strip()
        for key in ["Query-Pattern Matrix", "Unified Risk & Control Model", "Standard Development Environment", "Agent Query Index"]:
            if key.lower() in title_clean.lower():
                end_line = sections[idx+1][1] if idx+1 < len(sections) else len(lines)
                blocks[key] = block_text(line_i, end_line)
    return blocks

def build_fingerprints(blocks: dict):
    fps = {}
    for k, v in blocks.items():
        n = norm(v)
        fps[k] = hashlib.sha256(n.encode("utf-8")).hexdigest()
    return fps

def contains_any_fingerprint(text: str, fps: dict):
    n = norm(text)
    hits = []
    for k, h in fps.items():
        if h in hashlib.sha256(n.encode("utf-8")).hexdigest():
            hits.append(k)
    # the above doesn't work as intended; use substring match of normalized block inside normalized text
    hits = []
    for k, h in fps.items():
        # recompute block norm from hash: not possible; keep original norm in a parallel map
        pass

def strip_by_headings(md: str):
    # remove sections whose heading matches any global title (supports escaped headings and numbering)
    lines = md.splitlines()
    out = []
    skip = False
    for i, line in enumerate(lines):
        hnorm = None
        if re.match(r"^\s{0,3}#{1,3}\s+", line) or re.match(r"^\s{0,3}\\#{1,3}\s+", line):
            title = re.sub(r"^\s{0,3}(?:\\)?#{1,3}\s+", "", line).strip()
            title = re.sub(r"^\d+\.\s*", "", title).strip()
            if any(t.lower() == title.lower() or t.lower() in title.lower() for t in GLOBAL_TITLES):
                skip = True
                continue
            else:
                skip = False
        if not skip:
            out.append(line)
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip() + "\n"
    return txt

def strip_by_fingerprints(md: str, norms: dict):
    # remove any block whose NORMALIZED text contains a normalized global block substring
    # Strategy: windowed scan by paragraphs
    paras = re.split(r"\n\s*\n", md.strip())
    kept = []
    removed = []
    for para in paras:
        pn = norm(para)
        hit = False
        for key, nb in norms.items():
            if nb and nb in pn:
                hit = True
                removed.append((key, para[:120]))
                break
        if not hit:
            kept.append(para)
    cleaned = "\n\n".join(kept).strip() + "\n"
    return cleaned, removed

def ensure_h1(name: str, md: str) -> str:
    if not re.match(r"^\s{0,3}(?:\\)?#\s", md):
        return f"# {name}\n\n" + md
    return md

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    partA_path = DIST / "PartA_Core.md"
    partA = partA_path.read_text(encoding="utf-8") if partA_path.exists() else ""

    # Build normalized global block map (norm text, not hash)
    blocks = extract_global_blocks_from_partA(partA)
    global_norms = {k: norm(v) for k, v in blocks.items() if v and len(v) > 0}

    combined, used = [], []
    leakage = {}
    for p in sorted(BPS.glob("*.md")):
        raw = p.read_text(encoding="utf-8")
        name = p.stem.replace("-", " ").title()

        a = strip_by_headings(raw)
        b, removed = strip_by_fingerprints(a, global_norms)
        b = ensure_h1(name, b)

        if len(b.strip()) < 100:
            continue

        combined.append(b.strip())
        used.append(p.name)
        leakage[p.name] = {
            "removed_blocks": [{"key": k, "sample": s} for (k, s) in removed],
            "sizes": {"raw": len(raw.encode()), "after_headings": len(a.encode()), "after_fps": len(b.encode())}
        }

    partB = "\n\n---\n\n".join(combined) + ("\n" if combined else "")
    (DIST / "PartB_Blueprints.md").write_text(partB, encoding="utf-8")
    ssot = partA.strip() + "\n\n" + partB
    (DIST / "SSOT.md").write_text(ssot, encoding="utf-8")
    banner = "<!-- AUTOGENERATED: DO NOT EDIT. Built via CI consolidation. -->\n"
    (PROJ / "SSOT.md").write_text(banner + ssot, encoding="utf-8")

    # store leakage report
    (DIST / "LEAKAGE_REPORT.json").write_text(json.dumps(leakage, indent=2), encoding="utf-8")

    # update VALIDATION.json with sources used
    val_path = DIST / "VALIDATION.json"
    data = {}
    if val_path.exists():
        try:
            data = json.loads(val_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["ci_used_sources"] = used
    (val_path).write_text(json.dumps(data, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
