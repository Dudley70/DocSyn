.PHONY: ssot clean verify

ssot:
	python3 scripts/assemble_ssot.py
	@echo "✅ Built dist/SSOT.md"

clean:
	rm -rf dist
	mkdir -p dist

verify:
	@echo "Checking for duplicates and fence parity..."
	@python3 - <<'PY'
import re, sys, pathlib
p=pathlib.Path('dist/SSOT.md')
if not p.exists():
  print('dist/SSOT.md not found'); sys.exit(1)
text=p.read_text()
# global headings appear once
for g in ['Query-Pattern Matrix','Unified Risk','Standard Development Environment','Agent Query Index']:
  n=len(re.findall(r'^#.*'+re.escape(g), text, flags=re.M|re.I))
  print(g, n)
# fence parity
t=text.count('```')
print('fences', t, 'even' if t%2==0 else 'ODD');
PY
