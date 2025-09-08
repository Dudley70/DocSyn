\
    import subprocess, time
    from pathlib import Path
    def run(cmd, cwd=None):
        p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
        return p.returncode, p.stdout, p.stderr
    def ensure_branch(repo_root: Path, name: str):
        ts = time.strftime("%Y%m%d-%H%M%S")
        branch = f"{name}-{ts}"
        run(["git", "checkout", "-b", branch], repo_root)
        return branch
    def commit_all(repo_root: Path, msg: str):
        run(["git", "add", "-A"], repo_root)
        rc, out, err = run(["git", "commit", "-m", msg], repo_root)
        return rc == 0
    def open_pr(repo_root: Path, title: str, body_path: Path, draft: bool = True):
        draft_flag = ["--draft"] if draft else []
        cmd = ["gh", "pr", "create", "--title", title, "--body-file", str(body_path)] + draft_flag
        return run(cmd, repo_root)
