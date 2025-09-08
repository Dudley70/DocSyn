#!/usr/bin/env python3
"""
Lift long fenced code blocks from Markdown to /reference and replace them with links.

Usage:
  python3 scripts/lift_code_blocks.py check   # fail if any long blocks found (CI)
  python3 scripts/lift_code_blocks.py fix     # move long blocks into /reference and rewrite MD

Threshold: 800 characters per code block (configurable with CODE_LIFT_THRESHOLD env var).
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "reference"
REF.mkdir(exist_ok=True)

THRESH = int(os.environ.get("CODE_LIFT_THRESHOLD", "800"))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "check").lower()
TARGETS = [ROOT/"core", ROOT/"blueprints"]

ext_for = {
    "json":"json", "yaml":"yaml", "yml":"yml", "bash":"sh", "shell":"sh", "dockerfile":"Dockerfile",
    "python":"py", "ts":"ts", "tsx":"tsx", "js":"js", "sh":"sh", "txt":"txt"
}

def lift_in(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    changed = False
    problems = []
    out = []
    pos = 0
    idx = 0
    for m in re.finditer(r"```([a-zA-Z0-9_-]*)\n(.*?)```", text, flags=re.DOTALL):
        lang = (m.group(1) or "").strip().lower()
        code = m.group(2)
        start, end = m.span()
        if len(code) >= THRESH:
            problems.append((md_path, lang, len(code)))
            if MODE == "fix":
                out.append(text[pos:start])
                stem = md_path.stem.replace(" ", "_")
                ext = ext_for.get(lang, "txt")
                base = f"{stem}_block{idx+1}.{ext}"
                ref_path = REF / base
                suffix = 1
                while ref_path.exists():
                    base = f"{stem}_block{idx+1}_{suffix}.{ext}"
                    ref_path = REF / base
                    suffix += 1
                ref_path.write_text(code, encoding="utf-8")
                rel = f"./reference/{base}"
                out.append(f"> **Code moved to reference:** [{base}]({rel})\n")
                pos = end
                idx += 1
                changed = True
    out.append(text[pos:])
    if MODE == "fix" and changed:
        md_path.write_text("".join(out), encoding="utf-8")
    return problems, changed

def main():
    total_problems = []
    changed_any = False
    for tdir in TARGETS:
        for md in tdir.glob("*.md"):
            probs, ch = lift_in(md)
            total_problems.extend(probs)
            changed_any |= ch
    if MODE == "check":
        if total_problems:
            print("Long code blocks detected (run `make code-lift` locally to fix):")
            for p, lang, n in total_problems:
                print(f" - {p.name} ({lang or 'text'}): {n} chars")
            sys.exit(1)
        print("No long code blocks detected.")
        sys.exit(0)
    else:
        if changed_any:
            print("Long code blocks were lifted into /reference and links inserted.")
        else:
            print("No changes needed; no long blocks found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
