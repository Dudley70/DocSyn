#!/usr/bin/env python3
"""
Simple targeted cleaning of blueprint files.
Keep the header content and useful commands, remove global sections.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def simple_clean_blueprint(text, blueprint_name):
    """Simple approach: keep header and useful parts, remove global content"""
    
    title = blueprint_name.replace('-', ' ').title()
    
    # Split on the first major separator (---)
    parts = text.split('---', 1)
    
    # Keep the first part (header content)
    header_content = parts[0].strip()
    
    # Look for useful commands in the rest
    commands = []
    if len(parts) > 1:
        rest_content = parts[1]
        
        # Extract bash commands that seem blueprint-specific
        bash_commands = re.findall(r'```bash\s*\n([^`]+)\n```', rest_content)
        for cmd in bash_commands:
            # Keep commands that mention the blueprint name or useful patterns
            if any(term in cmd.lower() for term in [blueprint_name.lower(), '/document', '/test', '/janitor', '/guard', '/adapt', '/orchestrate', 'claude']):
                commands.append(cmd.strip())
    
    # Build the cleaned content
    result = header_content + '\n\n'
    
    # Add useful commands if found
    if commands:
        result += "## Commands\n\n"
        for cmd in commands:
            result += f"```bash\n{cmd}\n```\n\n"
    
    # Ensure proper title
    if not result.strip().startswith(f'# {title}'):
        lines = result.split('\n')
        if lines[0].startswith('# '):
            lines[0] = f'# {title}'
        else:
            lines.insert(0, f'# {title}')
        result = '\n'.join(lines)
    
    return result.strip() + '\n\n'

def main():
    blueprints_dir = ROOT / "blueprints"
    
    # First restore the full content
    print("📂 Restoring full content...")
    import subprocess
    subprocess.run(['rsync', '-a', str(ROOT / 'merge_pr' / 'updated') + '/', str(blueprints_dir) + '/'], check=True)
    
    print("✂️  Simple cleaning of blueprints...")
    
    for blueprint_file in blueprints_dir.glob("*.md"):
        blueprint_name = blueprint_file.stem
        print(f"  Cleaning {blueprint_name}...")
        
        # Read current content
        original_content = blueprint_file.read_text(encoding="utf-8", errors="ignore")
        original_size = len(original_content)
        
        # Clean it simply
        cleaned_content = simple_clean_blueprint(original_content, blueprint_name)
        cleaned_size = len(cleaned_content)
        
        # Write back
        blueprint_file.write_text(cleaned_content, encoding="utf-8")
        
        reduction = original_size - cleaned_size
        print(f"    ✅ {original_size:,} → {cleaned_size:,} chars (-{reduction:,})")
    
    print("✅ Simple cleaning complete!")

if __name__ == "__main__":
    main()
