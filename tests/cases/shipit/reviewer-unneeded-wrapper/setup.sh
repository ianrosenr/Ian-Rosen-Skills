# base commit on main, implementation commit on a t-* branch, IMPLEMENTME.md left uncommitted
set -e
H=$(mktemp -d); mv head "$H/"
cp -R base/. . && rm -rf base
G="git -c user.email=t@example.com -c user.name=t"
git init -q -b main && git add -A && $G commit -qm base
git checkout -qb t-2-show-note
cp -R "$H/head/." . && rm -rf "$H"
git add -A -- . ':!IMPLEMENTME.md' && $G commit -qm "T-2: show note"
