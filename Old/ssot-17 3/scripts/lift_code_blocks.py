#!/usr/bin/env python3
import re, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT/"reference"/"auto_lifted"
REF.mkdir(parents=True, exist_ok=True)
MODE = sys.argv[1] if len(sys.argv)>1 else "check"

def scan_file(p: Path):
    text = p.read_text(encoding="utf-8", errors="ignore")
    big = []
    for m in re.finditer(r"```([a-zA-Z0-9_-]*)\n(.*?)```", text, flags=re.DOTALL):
        code = m.group(0)
        lines = code.count("\n")
        if lines >= 80:  # threshold
            big.append((m.start(), m.end(), code))
    return text, big

def replace_block(text: str, start: int, end: int, placeholder: str):
    return text[:start] + placeholder + text[end:]

violations = 0
targets = list((ROOT/"blueprints").glob("*.md")) + list((ROOT/"core").glob("*.md"))
for p in targets:
    if p.name.endswith(".SOURCED.md"):
        continue
    text, big = scan_file(p)
    if not big: 
        continue
    for i, (s, e, code) in enumerate(reversed(big), 1):
        violations += 1
        if MODE == "fix":
            h = hashlib.sha1(code.encode("utf-8")).hexdigest()[:10]
            ref_path = REF/f"{p.stem}_{h}.md"
            ref_path.write_text(code, encoding="utf-8")
            placeholder = f"**[Code lifted to](/reference/auto_lifted/{ref_path.name})**"
            text = replace_block(text, s, e, placeholder)
    if MODE == "fix" and big:
        p.write_text(text, encoding="utf-8")

if MODE == "check":
    if violations:
        print(f"[warn] long code blocks detected: {violations}. Run `make code-lift`.")
    else:
        print("code-lift check: OK")

if MODE == "fix":
    print(f"code-lift fix complete. Blocks moved: {violations}")
