#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parent.parent
out = root/"SSOT.md"
out.write_text("# SSOT (placeholder build)\n\n_This is a placeholder assembler._\n", encoding="utf-8")
print("Assembled SSOT.md (placeholder).")
