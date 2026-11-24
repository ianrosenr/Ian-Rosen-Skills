set -e
git init -q -b main && git add -A && git -c user.email=t@example.com -c user.name=t commit -qm "T-2: export"
