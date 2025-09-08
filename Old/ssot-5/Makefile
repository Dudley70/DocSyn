.PHONY: ssot check

ssot:
	@python3 scripts/assemble_ssot.py

check:
	@python3 - <<'PY'
from pathlib import Path; import re, sys, json
root = Path('.')
m = json.loads((root/'build.manifest.json').read_text())
missing = [p for p in m['order'] if not (root/p).exists()]
if missing:
    print("Missing source files:\n - " + "\n - ".join(missing)); sys.exit(1)
# basic stable-id check (ensure CH0 exists somewhere)
content = (root/'SSOT.md').read_text(encoding='utf-8') if (root/'SSOT.md').exists() else ""
if 'CH0-ROUTER' not in content and 'Agent Query Index' not in content:
    print("Warning: SSOT.md does not yet contain Router section.")
print("OK")
PY

router-test:
	@python3 scripts/router_smoke_test.py

code-lift:
	@python3 scripts/lift_code_blocks.py fix

ci:
	@python3 scripts/lift_code_blocks.py check
	@python3 scripts/assemble_ssot.py
	@python3 scripts/router_smoke_test.py
