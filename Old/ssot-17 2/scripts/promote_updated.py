#!/usr/bin/env python3
import shutil, sys, time, json, os
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
UPDATED = PROJ / "merge_pr" / "updated"
BLUEPRINTS = PROJ / "blueprints"
BACKUPS = PROJ / "dist" / "backups" / "blueprints"
BACKUPS.mkdir(parents=True, exist_ok=True)

def main():
    ts = time.strftime("%Y%m%d-%H%M%S")
    snap = BACKUPS / f"pre-promotion-{ts}"
    snap.mkdir(parents=True, exist_ok=True)
    # backup current blueprints
    for p in BLUEPRINTS.glob("*.md"):
        shutil.copy2(p, snap / p.name)

    # keep previous sizes for shrink check
    sizes_prev = {p.name: p.stat().st_size for p in BLUEPRINTS.glob("*.md")}

    # promote
    promoted = []
    for src in UPDATED.glob("*.md"):
        dst = BLUEPRINTS / src.name
        shutil.copy2(src, dst)
        promoted.append(dst.name)

    # safety net: no shrinks > 20%
    sizes_new = {p.name: p.stat().st_size for p in BLUEPRINTS.glob("*.md")}
    shrunk = []
    for name, new_size in sizes_new.items():
        prev = sizes_prev.get(name, 0)
        if prev > 0 and new_size < prev * 0.8:
            shrunk.append((name, prev, new_size))

    report = {
        "timestamp": ts,
        "promoted": promoted,
        "sizes_previous": sizes_prev,
        "sizes_new": sizes_new,
        "shrunk_gt_20pct": shrunk
    }
    (PROJ / "dist" / "PROMOTION_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    if shrunk:
        print("[WARN] Some blueprints shrank > 20%:", shrunk)

if __name__ == "__main__":
    main()
