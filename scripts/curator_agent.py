\
    #!/usr/bin/env python3
    import argparse, os, sys, json, re, shutil, subprocess, hashlib, time
    from pathlib import Path
    try:
        import yaml
    except Exception:
        yaml = None
    REPO = Path(__file__).resolve().parents[1]
    CURATOR = REPO / "curator"
    CONFIG = CURATOR / "config.yaml"
    from curator_lib.norm import normalize_text, paragraph_iter, heading_iter, GLOBAL_TITLES, looks_like_aqi_table
    from curator_lib.git_ops import ensure_branch, commit_all, open_pr, run as run_cmd
    def load_config():
        if CONFIG.exists() and yaml:
            return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
        return {"input_dir":"input","staging_dir":"curator/staging","diffs_dir":"curator/diffs","core_dir":"core","blueprints_dir":"blueprints","dist_dir":"dist","branch_prefix":"curator"}
    def ensure_dirs(cfg):
        for k in ["input_dir","staging_dir","diffs_dir"]:
            (REPO / cfg[k]).mkdir(parents=True, exist_ok=True)
    def sha256_file(p: Path) -> str:
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    def simple_extract_text(p: Path) -> str:
        if p.suffix.lower() in [".md",".txt"]:
            return p.read_text(encoding="utf-8", errors="ignore")
        return f"> [Curator placeholder] Binary {p.suffix} not extracted.\\n> Path: {p}\\n"
    def analyze(args):
        cfg = load_config(); ensure_dirs(cfg)
        input_dir = REPO / cfg["input_dir"]; staging_dir = REPO / cfg["staging_dir"]
        manifest = {"inputs":[]}
        for p in sorted(input_dir.glob("*")):
            if p.is_file():
                text = simple_extract_text(p); sha = sha256_file(p)
                out_md = staging_dir / f"{p.stem}.md"
                front = ["---", "source_files:", f"  - path: {str(p)}", f"    sha256: {sha}", "generated_by: master-curator", f"generated_at: {time.strftime('%Y-%m-%d %H:%M:%S')}", "---", ""]
                out_md.write_text("\\n".join(front)+text, encoding="utf-8")
                manifest["inputs"].append({"path":str(p),"sha256":sha,"staged_md":str(out_md)})
        (staging_dir/"ANALYZE_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"[analyze] staged: {len(manifest['inputs'])}")
    def plan(args):
        cfg = load_config(); ensure_dirs(cfg)
        staging_dir = REPO / cfg["staging_dir"]; diffs_dir = REPO / cfg["diffs_dir"]; dist_dir = REPO / cfg["dist_dir"]; blueprints_dir = REPO / cfg["blueprints_dir"]
        partA = (dist_dir/"PartA_Core.md").read_text(encoding="utf-8") if (dist_dir/"PartA_Core.md").exists() else ""
        def extract_blocks(md: str):
            blocks = {}; lines = md.splitlines(); heads = list(heading_iter(md))
            def slice_block(i,j):
                start = heads[i][1]; end = heads[j][1]-1 if j < len(heads) else len(lines)
                return "\\n".join(lines[start-1:end])
            for i,(title,ln) in enumerate(heads):
                t = re.sub(r"^\\d+\\.\\s*","",title).strip()
                for key in ["Router — Query-Pattern Matrix","Query-Pattern Matrix","Unified Risk & Control Model","Standard Development Environment","Agent Query Index"]:
                    if key.lower() in t.lower():
                        blocks[key] = slice_block(i,i+1)
            return blocks
        global_blocks = extract_blocks(partA)
        global_norms = {k: normalize_text(v) for k,v in global_blocks.items() if v}
        proposals = []
        for md in sorted(staging_dir.glob("*.md")):
            raw = md.read_text(encoding="utf-8"); topic = md.stem.lower()
            target_name = f"{topic}.md"
            kept_lines=[]; skip=False
            for line in raw.splitlines():
                if re.match(r"^\\s*(?:>\\s*)*(?:\\\\)?#{1,3}\\s+", line):
                    title = re.sub(r"^\\s*(?:>\\s*)*(?:\\\\)?#{1,3}\\s+","",line).strip()
                    title = re.sub(r"^\\d+\\.\\s*","",title).strip()
                    if any(t.lower()==title.lower() or t.lower() in title.lower() for t in GLOBAL_TITLES):
                        skip=True; continue
                    else:
                        skip=False
                if not skip: kept_lines.append(line)
            body2 = "\\n".join(kept_lines)
            cleaned_paras=[]; removed=[]
            for para, ls, le in paragraph_iter(body2):
                hit=None
                if looks_like_aqi_table(para): hit="Agent Query Index"
                else:
                    pn = normalize_text(para)
                    for key, nv in global_norms.items():
                        if nv and nv in pn: hit=key; break
                if hit: removed.append({"key":hit,"line_start":ls,"line_end":le,"sample":para[:200]})
                else: cleaned_paras.append(para)
            cleaned = "\\n\\n".join(cleaned_paras).strip()+"\\n"
            if not re.match(r"^\\s*(?:\\\\)?#\\s", cleaned):
                cleaned = f"# {md.stem.title()}\\n\\n" + cleaned
            outp = diffs_dir / f"{md.stem}.proposal.md"
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(cleaned, encoding="utf-8")
            proposals.append({"staged":str(md), "proposal": str(outp), "target_blueprint": str((blueprints_dir/target_name).relative_to(REPO)), "removed_blocks": removed})
        (diffs_dir/"PLAN.json").write_text(json.dumps({"proposals":proposals}, indent=2), encoding="utf-8")
        print(f"[plan] proposals: {len(proposals)}")
    def apply(args):
        cfg = load_config(); diffs_dir = REPO / cfg["diffs_dir"]; blueprints_dir = REPO / cfg["blueprints_dir"]
        plan_path = diffs_dir/"PLAN.json"
        if not plan_path.exists(): print("[apply] no PLAN.json"); sys.exit(1)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        branch = ensure_branch(REPO, cfg.get("branch_prefix","curator"))
        changed=[]
        for p in plan.get("proposals", []):
            src = REPO / p["proposal"]; dst = REPO / p["target_blueprint"]
            dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); changed.append(str(dst))
        rc,out,err = run_cmd(["make","ci"], REPO)
        if rc != 0: print(out); print(err, file=sys.stderr); sys.exit(2)
        commit_all(REPO, f"curator: apply {len(changed)} proposal(s)")
        pr_body = diffs_dir/"PR_BODY.md"
        pr_body.write_text("Curator Agent proposals applied. See dist/VALIDATION.json and dist/LEAKAGE_REPORT.json.", encoding="utf-8")
        title = f"curator: apply {len(changed)} proposal(s)"
        rc,out,err = open_pr(REPO, title, pr_body, draft=True)
        print(out or err); print("[apply] done")
    def main():
        ap = argparse.ArgumentParser("curator")
        sp = ap.add_subparsers(dest="cmd", required=True)
        sp.add_parser("analyze").set_defaults(func=analyze)
        sp.add_parser("plan").set_defaults(func=plan)
        sp.add_parser("apply").set_defaults(func=apply)
        args = ap.parse_args(); args.func(args)
    if __name__ == "__main__":
        main()
