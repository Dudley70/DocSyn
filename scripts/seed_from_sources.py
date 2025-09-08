#!/usr/bin/env python3
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "raw"
CORE = ROOT / "core"
BP = ROOT / "blueprints"

def read(p: Path) -> str:
    try: return p.read_text(encoding="utf-8")
    except: return p.read_text(errors="ignore")

def find_section(text: str, titles, max_chars=6000):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s", line):
            h = re.sub(r"^#{1,6}\s*", "", line).strip().lower()
            if any(t in h for t in titles):
                j = i + 1
                chunk_lines = []
                while j < len(lines) and not re.match(r"^#{1,6}\s", lines[j]):
                    chunk_lines.append(lines[j]); j += 1
                chunk = line + "\n" + "\n".join(chunk_lines)
                return chunk[:max_chars]
    return ""

def find_code_blocks(text: str, lang="json", max_blocks=2, max_chars=3000):
    blocks = []
    for m in re.finditer(rf"```{lang}\n(.*?)```", text, flags=re.DOTALL|re.IGNORECASE):
        blocks.append(m.group(0))
        if len(blocks) >= max_blocks: break
    return "\n\n".join(blocks)[:max_chars]

def extract_router(texts):
    for name, t in texts:
        if re.search(r"agent\s+query\s+index|router|routing", t, re.IGNORECASE):
            sec = find_section(t, ["agent query index","router","routing","index"])
            if sec: return f"### Agent Query Index (sourced: {name})\n\n{sec}\n"
    return ""

def extract_risks(texts):
    for name, t in texts:
        if re.search(r"risk\s*&?\s*control|unified risk|governance.*(risk|control)", t, re.IGNORECASE):
            sec = find_section(t, ["risk & control","risk and control","unified risk","governance","controls"])
            if sec: return f"### Unified Risk & Control Model (sourced: {name})\n\n{sec}\n"
    return ""

def extract_devc(texts):
    for name, t in texts:
        if re.search(r"devcontainer|development environment|dockerfile", t, re.IGNORECASE):
            sec = find_section(t, ["devcontainer","development environment","standard development environment","dockerfile"])
            blocks = find_code_blocks(t, "json") or find_code_blocks(t, "yaml") or find_code_blocks(t, "dockerfile")
            merged = (sec or "") + ("\n\n" + blocks if blocks else "")
            if merged.strip(): return f"### Standard Development Environment (sourced: {name})\n\n{merged}\n"
    return ""

BP_TERMS = {
    "orchestrator.md": ["orchestrator","multi-agent orchestrator","/orchestrate"],
    "cicd-analyst.md": ["ci/cd security analyst","pipeline","sast","dast","/cicd"],
    "adaptive-learning.md": ["adaptive learning","/adapt","retrospective"],
    "documenter.md": ["automated documenter","documenter","docs","readme","/document"],
    "guardian.md": ["guardian","file-watcher","watch","/guard","lint","monitor"],
    "janitor.md": ["janitor","cleanup","hygiene","/janitor"],
    "tester.md": ["automated tester","tester","/test","unit test","integration test"],
}

def extract_bp(texts, terms):
    for name, t in texts:
        lines = t.splitlines()
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\s", line):
                h = re.sub(r"^#{1,6}\s*", "", line).strip().lower()
                if any(term in h for term in terms):
                    j = i+1; chunk=[line]
                    while j < len(lines) and not re.match(r"^#{1,6}\s", lines[j]):
                        chunk.append(lines[j]); j += 1
                    return name, "\n".join(chunk[:4000])
        for term in terms:
            m = re.search(rf"(/[\w\-]+).*{re.escape(term)}", t, re.IGNORECASE|re.DOTALL)
            if m:
                start = max(0, m.start()-300); end = min(len(t), m.end()+800)
                return name, t[start:end]
    return "", ""

def main():
    md_files = sorted(RAW.glob("*.md"))
    if not md_files:
        print("No .md files in sources/raw"); sys.exit(0)
    texts = [(p.name, read(p)) for p in md_files]

    router = extract_router(texts)
    risks = extract_risks(texts)
    devc = extract_devc(texts)
    if router: (CORE/"00-router.SOURCED.md").write_text(router, encoding="utf-8")
    if risks: (CORE/"01-risks.SOURCED.md").write_text(risks, encoding="utf-8")
    if devc: (CORE/"02-devcontainer.SOURCED.md").write_text(devc, encoding="utf-8")

    for fname, terms in BP_TERMS.items():
        src, snip = extract_bp(texts, terms)
        if not snip: continue
        p = BP/fname
        base = p.read_text(encoding="utf-8") if p.exists() else "# " + fname.replace(".md","").title() + "\n"
        merged = base.rstrip() + "\n\n---\n\n" + f"> **Sourced excerpt from:** {src}\n\n" + snip.strip() + "\n"
        p.write_text(merged, encoding="utf-8")

    print("Seeding complete. Review core/*.SOURCED.md and blueprints/*.md, then `make ssot`.")

if __name__ == "__main__":
    main()
