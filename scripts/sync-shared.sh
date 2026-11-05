#!/bin/sh
# Copy skills/_shared/config-rules.md into each skill as a real file.
# Installers (npx skills) skip symlinks pointing outside the skill dir.
# --check: no writes; exit 1 + list stale copies.
set -e
REPO=$(cd "$(dirname "$0")/.." && pwd)
SRC="$REPO/skills/_shared/config-rules.md"
HDR='<!-- GENERATED from skills/_shared/config-rules.md by scripts/sync-shared.sh; do not edit -->'
stale=0
for d in "$REPO"/skills/*/; do
  d=${d%/}
  [ -f "$d/SKILL.md" ] || continue
  out="$d/config-rules.md"
  want=$(printf '%s\n' "$HDR"; cat "$SRC")
  if [ "$1" = "--check" ]; then
    if [ -L "$out" ] || [ ! -f "$out" ] || [ "$(cat "$out")" != "$want" ]; then
      echo "stale: ${out#$REPO/}"; stale=1
    fi
  else
    rm -f "$out"
    printf '%s\n' "$want" > "$out"
    echo "wrote ${out#$REPO/}"
  fi
done
exit $stale
