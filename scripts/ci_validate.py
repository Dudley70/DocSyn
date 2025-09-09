#!/usr/bin/env python3
import sys, json, re
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
DIST = PROJ / "dist"
SSOT = DIST / "DocSyn_Compiled.md"
VAL  = DIST / "VALIDATION.json"
BPS  = PROJ / "blueprints"
UPD  = PROJ / "merge_pr" / "updated"
LEAK = DIST / "LEAKAGE_REPORT.json"

def die(msg, code=1):
    print(f"[FAIL] {msg}")
    sys.exit(code)

def ok(msg):
    print(f"[OK] {msg}")

def contains_heading(text: str, label: str) -> int:
    pattern = r"(?m)^\s*(?:>\s*)*(?:\\)?#{1,6}\s+(?:\d+\.\s*)?.*" + re.escape(label) + r"\s*$"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

def norm(txt: str) -> str:
    t = txt.lower()
    t = re.sub(r"[\s\|`*_:>\-]+", "", t)
    return t

def split_sections(text: str):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*(?:>\s*)*(?:\\)?#{1,3}\s+", line):
            title = re.sub(r"^\s*(?:>\s*)*(?:\\)?#{1,3}\s+", "", line).strip()
            yield (title, i)
    return

def extract_blocks(partA: str):
    lines = partA.splitlines()
    sections = list(split_sections(partA))
    blocks = {}
    def block_text(start, end):
        return "\n".join(lines[start:end])
    keys = ["Router — Query-Pattern Matrix", "Query-Pattern Matrix", "Unified Risk & Control Model", "Standard Development Environment", "Agent Query Index"]
    for idx, (title, li) in enumerate(sections):
        clean = re.sub(r"^\d+\.\s*", "", title).strip()
        for key in keys:
            if key.lower() in clean.lower():
                end = sections[idx+1][1] if idx+1 < len(sections) else len(lines)
                blocks[key] = block_text(li, end)
    return blocks

def main():
    if not SSOT.exists():
        die("dist/DocSyn_Compiled.md not found")
    text = SSOT.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) < 100_000:
        die(f"SSOT too small: {len(text.encode('utf-8'))} bytes (<100k).")
    ok("SSOT size OK.")

    required_once = [
        "Router — Query-Pattern Matrix",
        "Unified Risk & Control Model",
        "Standard Development Environment",
    ]
    for label in required_once:
        c = contains_heading(text, label)
        if c != 1:
            die(f"Heading '{label}' occurrences = {c}, expected 1.")
        ok(f"Heading '{label}' present once.")

    aqi = contains_heading(text, "Agent Query Index")
    if aqi not in (0,1):
        die(f"'Agent Query Index' occurrences = {aqi}, expected 0 or 1.")
    ok("'Agent Query Index' count acceptable (0 or 1).")

    fences = len(re.findall(r"```", text))
    if fences % 2 != 0:
        die(f"Code fence count is odd ({fences}).")
    ok("Code-fence parity even.")

    # Promotion enforcement
    bps = list(BPS.glob("*.md"))
    upd = list(UPD.glob("*.md"))
    if not bps:
        die("No blueprints found in blueprints/.")
    small = [p.name for p in bps if p.stat().st_size < 1000]
    if small:
        die(f"Blueprints too small (post-promotion check): {small}")
    for u in upd:
        b = BPS / u.name
        if b.exists() and u.stat().st_mtime > b.stat().st_mtime + 1:
            die(f"Promotion required: {u.name} newer than blueprints/{u.name}.")
    ok("Promotion checks OK.")

    # Part B checks
    partB_path = DIST / "PartB_Blueprints.md"
    if not partB_path.exists():
        die("dist/PartB_Blueprints.md missing.")
    partB = partB_path.read_text(encoding="utf-8")

    # a) no global headings in Part B (supports escaped and blockquoted)
    for label in ["Query-Pattern Matrix", "Unified Risk", "Unified Risk & Control Model", "Standard Development Environment", "Agent Query Index"]:
        c = contains_heading(partB, label)
        if c != 0:
            die(f"Global heading leaked in Part B: '{label}' occurrences = {c}.")
    ok("No global headings in Part B.")

    # b) fingerprint match of Part A blocks in Part B
    partA_path = DIST / "PartA_Core.md"
    if partA_path.exists():
        partA = partA_path.read_text(encoding="utf-8")
        blocks = extract_blocks(partA)
        nb = {k: norm(v) for k,v in blocks.items() if v}
        nb_partB = norm(partB)
        leftover = [k for k, nv in nb.items() if nv and nv in nb_partB]
        if leftover:
            die(f"Global block(s) from Part A still present in Part B: {leftover}.")
        ok("No Part A global blocks detected in Part B.")
    else:
        print("[WARN] PartA_Core.md not found; skipping fingerprint leakage check.")

    print("\nAll invariant checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
