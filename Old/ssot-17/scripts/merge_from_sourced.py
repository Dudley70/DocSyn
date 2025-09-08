#!/usr/bin/env python3
import re, sys, json
from pathlib import Path
from difflib import unified_diff
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
BP = ROOT / "blueprints"
MERGE = ROOT / "merge_pr"
UPDATED = MERGE / "updated"
PATCHES = MERGE / "patches"
UPDATED.mkdir(parents=True, exist_ok=True)
PATCHES.mkdir(parents=True, exist_ok=True)

def split_sections(md: str):
    lines = md.splitlines()
    meta = []
    anchors_prev = []
    for i, line in enumerate(lines):
        for a in re.findall(r"\{\{#([A-Za-z0-9_-]+)\}\}", line):
            if not re.match(r"^#{1,6} ", line):
                anchors_prev.append(a)
        m = re.match(r"^(#{2,6})\s+(.*)", line)
        if m:
            title = m.group(2).strip()
            anchors_here = re.findall(r"\{\{#([A-Za-z0-9_-]+)\}\}", line)
            anchor = anchors_here[0] if anchors_here else (anchors_prev[0] if anchors_prev else "")
            anchors_prev = []
            meta.append([title, anchor, i, None])
    for idx in range(len(meta)):
        meta[idx][3] = meta[idx+1][2] if idx+1 < len(meta) else len(lines)
    return lines, meta

def find_section_index(meta, target_title: str, target_anchor_hint: str = ""):
    if target_anchor_hint:
        hint = target_anchor_hint.lower()
        for i, (title, anchor, start, end) in enumerate(meta):
            if anchor and hint in anchor.lower():
                return i
    for i, (title, anchor, start, end) in enumerate(meta):
        if title.strip().lower() == target_title.strip().lower():
            return i
    for i, (title, anchor, start, end) in enumerate(meta):
        if target_title.strip().lower() in title.strip().lower():
            return i
    return -1

def extract_excerpts(md: str):
    res = []
    lead = "> **Sourced excerpt from:**"
    if lead not in md: return res
    parts = md.split(lead)
    for i in range(1, len(parts)):
        tail = parts[i]
        seg = lead + tail.split("\n\n##", 1)[0].split("\n---", 1)[0]
        res.append(seg.strip())
    return res

def normalise_text(s: str) -> str:
    s = s.replace("\r\n","\n").replace("\r","\n")
    s = re.sub(r"\n{3,}", "\n\n", s.strip())
    return s

def synthesise(excerpt: str):
    words = len(re.findall(r"\b\w+\b", excerpt))
    if words > 1200:
        return {"mode":"excerpt-only","text": normalise_text(excerpt)}
    cmds = []
    short_blocks = []
    json_blocks = []
    for line in excerpt.splitlines():
        line = line.strip()
        if re.match(r"^/[A-Za-z0-9_-]+", line):
            cmds.append(line)
    for m in re.finditer(r"```([a-zA-Z0-9_-]*)\n(.*?)```", excerpt, flags=re.DOTALL):
        lang = (m.group(1) or "").lower(); code = m.group(2).strip()
        if len(code) <= 600:
            if lang in ("json","yaml","yml"): json_blocks.append((lang, code))
            else: short_blocks.append((lang, code))
        if len(short_blocks) + len(json_blocks) >= 5: break
    out = {}
    if cmds or short_blocks:
        parts = []
        if cmds: parts.append("**Quick Commands**\n\n" + "\n".join([f"- `{c}`" for c in cmds[:8]]))
        for lang, code in short_blocks[:2]:
            parts.append(f"```{lang}\n{code}\n```")
        out["Snippets"] = normalise_text("\n\n".join(parts))
    if json_blocks:
        lang, code = json_blocks[0]
        out["JSON Handoff"] = normalise_text(f"```{lang}\n{code}\n```")
    if not out:
        return {"mode":"excerpt-only","text": normalise_text(excerpt)}
    return {"mode":"synth","sections": out}

def insert_block(md: str, section_title: str, block_md: str, anchor_hint: str, prov: str):
    lines, meta = split_sections(md)
    idx = find_section_index(meta, section_title, anchor_hint)
    block = f"\n\n> _Provenance: {prov}_\n\n{block_md}\n"
    if idx == -1:
        return md.rstrip() + f"\n\n## {section_title}\n" + block
    title, anchor, start, end = meta[idx]
    before = "\n".join(lines[:end]).rstrip()
    after = "\n".join(lines[end:])
    return before + "\n\n" + block + "\n" + after

def merge_file(md_path: Path):
    src = md_path.read_text(encoding="utf-8")
    excerpts = extract_excerpts(src)
    if not excerpts: return None, None
    synth = synthesise(excerpts[0])
    if synth["mode"] == "excerpt-only":
        quoted = "\n".join(["> " + ln for ln in synth["text"].splitlines()])
        merged = insert_block(src, "Sourced Excerpts (Review)", quoted, "", f"Auto-quoted from {md_path.name} on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        return src, merged
    merged = src
    for section, body in synth["sections"].items():
        hint = {"Snippets":"SNP","Command":"CMD","I/O & Tools":"IO","Objective":"OBJ","JSON Handoff":"JSON","Verification":"VER","Telemetry & KPIs":"KPI"}.get(section,"")
        merged = insert_block(merged, section, body, hint, f"Synthesised from sourced excerpt in {md_path.name} on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    return src, merged

def main():
    changed, skipped = [], []
    for f in sorted(BP.glob("*.md")):
        orig, merged = merge_file(f)
        if merged is None: skipped.append(f.name); continue
        if merged != orig:
            (UPDATED/f.name).write_text(merged, encoding="utf-8")
            diff = unified_diff(orig.splitlines(True), merged.splitlines(True),
                                fromfile=str(f), tofile=str(f)+" (proposed)")
            (PATCHES/(f.name + ".patch")).write_text("".join(diff), encoding="utf-8")
            changed.append(f.name)
        else:
            skipped.append(f.name)
    (MERGE/"report.json").write_text(json.dumps({"changed": changed, "skipped": skipped, "apply": False}, indent=2), encoding="utf-8")
    print(f"Changed: {len(changed)}; Skipped: {len(skipped)}")

if __name__ == "__main__":
    main()
