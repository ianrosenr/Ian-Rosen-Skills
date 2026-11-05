#!/usr/bin/env bash
set -euo pipefail
git init -q .
mkdir -p .irskills
cat > .irskills/config <<'CFG'
budget=normal
colour=red
CFG
