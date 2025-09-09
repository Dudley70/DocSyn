#!/usr/bin/env python3
"""
one_click_repair_and_build.py
- Cleans blueprint leakage, normalizes manifest to curated_sources,
- ensures governance config, assembles SSOT, validates, and prints a summary.
- Idempotent and safe; keeps backups in dist/backups/blueprints/.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path('.').resolve()
BP = ROOT / 'blueprints'
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True, parents=True)

GLOBAL_HEADINGS = ['Query-Pattern Matrix', 'Unified Risk & Control Model', 'Standard Development Environment', 'Agent Query Index']

def normalize(md: str) -> str:
    md = re.sub(r'\n{3,}', '\n\n', md)
    if not md.endswith('\n'):
        md += '\n'
    return md

def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''

def write(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8')

def clean_blueprint(text: str, title: str) -> str:
    m = re.search(r'<!--BEGIN:blueprint:.*?-->(.*?)<!--END:blueprint:.*?-->', text, flags=re.S|re.I)
    if m:
        body = m.group(1).strip()
    else:
        cutoff = len(text)
        m1 = re.search(r'Sourced excerpt from', text, flags=re.I)
        if m1: cutoff = min(cutoff, m1.start())
        for h in GLOBAL_HEADINGS:
            mg = re.search(rf'^#.*{re.escape(h)}', text, flags=re.M|re.I)
            if mg: cutoff = min(cutoff, mg.start())
        body = text[:cutoff].strip()
    for h in GLOBAL_HEADINGS:
        body = re.sub(rf'^#.*{re.escape(h)}.*?(?=^#|\Z)', '', body, flags=re.S|re.M|re.I)
    if not re.match(r'^#\s+', body):
        body = f'# {title}\n\n' + body
    return normalize(body)

def assemble(curated):
    core_paths = [p for p in curated if '/core/' in p or p.startswith('core/')]
    bp_paths   = [p for p in curated if '/blueprints/' in p or p.startswith('blueprints/')]
    partA = '\n\n'.join(read(ROOT / p) for p in core_paths if (ROOT / p).exists())
    partB = '\n\n---\n\n'.join(read(ROOT / p) for p in bp_paths if (ROOT / p).exists())
    banner = f"# Single Source of Truth (SSOT)\n\n> Build: {datetime.utcnow().isoformat()}Z\n\n"
    ssot = normalize(banner + partA + '\n---\n\n' + partB)
    out_lines, prev_h = [], None
    for ln in ssot.splitlines():
        m = re.match(r'^#\s+(.+)$', ln)
        if m:
            h = m.group(1).strip().lower()
            if h == prev_h:
                continue
            prev_h = h
        out_lines.append(ln)
    ssot = '\n'.join(out_lines) + '\n'
    write(DIST / 'PartA_Core.md', partA)
    write(DIST / 'PartB_Blueprints.md', partB)
    write(DIST / 'DocSyn_Compiled.md', ssot)
    return ssot, partB

def main():
    # 1) Clean blueprints
    backups = ROOT / 'dist' / 'backups' / 'blueprints'
    backups.mkdir(parents=True, exist_ok=True)
    changed = []
    if BP.exists():
        for md in sorted(BP.glob('*.md')):
            raw = read(md)
            write(backups / md.name, raw)
            title = md.stem.replace('-', ' ').title()
            new = clean_blueprint(raw, title)
            if new != raw:
                write(md, new)
                changed.append(md.name)

    # 2) Ensure governance & manifest curated_sources
    tools = ROOT / 'tools'; tools.mkdir(exist_ok=True)
    merge_cfg = tools / 'merge_config.yaml'
    if not merge_cfg.exists():
        write(merge_cfg, 'IGNORE_HEADINGS:\n'
                         '  - "Query-Pattern Matrix (Router)"\n'
                         '  - "Unified Risk & Control Model"\n'
                         '  - "Standard Development Environment"\n'
                         '  - "Agent Query Index"\n'
                         'SNIPPET_LIMIT: 2000\n'
                         'DEDUP_HEADINGS: true\n'
                         'BLOCK_RECURSIVE_INPUTS: true\n'
                         'HALT_ON_DUPLICATE_GLOBALS: true\n')

    mf = ROOT / 'build.manifest.json'
    assert mf.exists(), 'build.manifest.json missing'
    manifest = json.loads(read(mf))
    sources = manifest.get('curated_sources') or manifest.get('sections') or []
    if not sources or not isinstance(sources, list):
        sources = []
        for rel in ['core/00-router.md','core/01-risks.md','core/02-devcontainer.md']:
            if (ROOT / rel).exists(): sources.append(rel)
        for md in sorted(BP.glob('*.md')):
            sources.append(f'blueprints/{md.name}')
    sources = [s for s in sources if not (s.startswith('sources/') or s.endswith('.SOURCED.md'))]
    manifest['curated_sources'] = sources
    manifest.setdefault('governance', {}).update({
        'config': 'tools/merge_config.yaml',
        'dedup_headings': True,
        'block_recursive_inputs': True
    })
    manifest.setdefault('outputs', ['dist/DocSyn_Compiled.md', 'dist/PartA_Core.md', 'dist/PartB_Blueprints.md'])
    write(mf, json.dumps(manifest, indent=2))

    # 3) Assemble
    ssot, partB = assemble(manifest['curated_sources'])

    # 4) Validate
    def hcount(label): return len(re.findall(rf'^#.*{re.escape(label)}', ssot, flags=re.M|re.I))
    def acount(label): return len(re.findall(re.escape(label), ssot, flags=re.I))
    labels = ['Query-Pattern Matrix','Unified Risk & Control Model','Standard Development Environment','Agent Query Index']
    counts_h = {l: hcount(l) for l in labels}
    counts_a = {l: acount(l) for l in labels}
    leakage = {l: (re.search(re.escape(l), partB, flags=re.I) is not None) for l in labels}
    report = {
        'blueprints_cleaned': changed,
        'globals_counts_headings': counts_h,
        'globals_counts_anywhere': counts_a,
        'globals_in_blueprints': leakage,
        'fence_parity_even': (ssot.count('```') % 2 == 0),
        'build_time_utc': datetime.utcnow().isoformat()+'Z'
    }
    write(DIST / 'ONE_CLICK_REPORT.json', json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()