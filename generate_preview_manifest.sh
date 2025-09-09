#!/bin/bash

echo "=== Generating Preview Manifest Snippet ==="

# Copy current manifest as preview
cp build.manifest.json build.manifest.preview.json

echo "New files promoted to blueprints:"
git ls-files blueprints | grep -E "(Claude|Bible|Chat|code-assistant|deployment-agent)" | head -20

echo ""
echo "Add these lines to 'curated_sources' array in build.manifest.preview.json:"
echo "["

# Generate JSON array entries for new files
git ls-files blueprints | grep -E "(Claude|Bible|Chat|code-assistant|deployment-agent)" | head -20 | while read file; do
    echo "    \"$file\","
done

echo "]"

echo ""
echo "Preview build command:"
echo "python3 scripts/assemble_ssot.py --manifest build.manifest.preview.json"
