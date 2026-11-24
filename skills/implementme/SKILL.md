---
name: implementme
description: Write IMPLEMENTME.md for the next unchecked line item of a ready chunk in plan.md: the exact change, files to read and touch, code to reuse, tests. Reads only the parts of the repo the item needs. The user reviews it; /shipit approves it. args: "[T-n]"
metadata:
  version: "1.0.0"
---

# implementme

## Preconditions (in order; stop with a message on the first one that fails)
1. Clean working tree. `git checkout main && git pull --ff-only`.
2. No open PR from a `t-*` branch (`gh pr list --state open --json number,headRefName`). Open -> "Review and merge PR #n first."
3. Item = `T-n` if given, else the first unchecked item of the first `status: ready` chunk. None left -> say which chunk is next and what it needs (`/grill chunk N`, `/research`, `/architecture chunk N`, `/ready chunk N`).
4. Item is `T-n` and branch `t-<n>-*` exists with an IMPLEMENTME.md (a re-run after /retro) -> rewrite that file in place, keep its `issue:` line.

## Read (as little as possible)
- `plan.md` in full: checked items = done work; Decisions; Open questions for this chunk.
- `AGENTS.md` `## Layout`: pick the folders the item touches.
- Those folders' `README.md`, then only the files the change needs. `git log --oneline -20` for recent work. Never read the whole repo.

## Write
Branch `t-<n>-<slug>` from main. Write repo-root `IMPLEMENTME.md` from `implementme-template.md` in this skill's directory. Leave it uncommitted.
- One change. The item turns out to be 2+ changes -> stop and propose a split of the line item (user decides; you edit plan.md).
- Exact: file paths, function names, test names. The implementer reads only this file and the files it lists.
- Copy the text of every decision that applies; don't just cite ids.
- Reuse: name existing functions and modules to use, so nothing is rebuilt.
- Item creates a top-level folder -> include its `README.md` and the `AGENTS.md` Layout line in `touch`.
- Fits one screen (about 60 lines). Longer -> the item is too big: propose a split.
- Behavior nobody decided -> don't guess: put it under Questions. /shipit won't run until Questions says none.

## Done
Reply: path, item, files to touch. "Review it, ask for edits, or type `/shipit` to approve."
