#!/usr/bin/env bash
set -euo pipefail
git init -q .
mkdir -p .irskills
cat > .irskills/config <<'CFG'
budget=normal
audience=human
CFG
cat > .irskills/config.local <<'CFG'
role=engineer
level=novice
CFG
