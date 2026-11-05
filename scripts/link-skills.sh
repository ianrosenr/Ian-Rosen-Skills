#!/bin/sh
# Link each skill into ~/.claude/skills/<name> -> bare /<name>. Live edits.
set -e
REPO=$(cd "$(dirname "$0")/.." && pwd)
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
[ -L "$DEST/irskills" ] && rm "$DEST/irskills"  # old plugin-style link (caused irskills: prefix)
for d in "$REPO"/skills/*/; do
  name=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  ln -sfn "${d%/}" "$DEST/$name"
  echo "linked /$name"
done
