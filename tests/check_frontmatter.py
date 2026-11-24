"""Free check: every skill file's frontmatter parses as YAML. Run: uv run --with pyyaml tests/check_frontmatter.py"""
import sys
from pathlib import Path

import yaml

bad = 0
for f in sorted(Path(__file__).resolve().parents[1].glob("skills/**/*.md")):
    text = f.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        continue
    try:
        yaml.safe_load(text.split("---\n", 2)[1])
    except yaml.YAMLError as e:
        bad += 1
        print(f"BAD {f}: {str(e).splitlines()[0]}")
print(f"{bad} bad")
sys.exit(1 if bad else 0)
