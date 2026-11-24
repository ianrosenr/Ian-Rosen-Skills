---
name: implementme
description: 'Write IMPLEMENTME.md for the next unchecked line item of a ready chunk in plan.md: the smallest complete change, every file it must reach (callers included), code to reuse, tests. Reads only the parts of the repo the item needs. The user reviews it; /shipit approves it. args: "[T-n]"'
metadata:
  version: "1.2.0"
---

# implementme

Plan like a lazy senior dev: the best code is code never written. Find the smallest change that fully does the line item, and write it so a busy human understands it in one read.

## Preconditions (in order; stop with a message on the first one that fails)
1. Clean working tree. `git checkout main && git pull --ff-only`.
2. No open PR from a `t-*` branch (`gh pr list --state open --json number,headRefName`). Open -> "Review and merge PR #n first."
3. Item = `T-n` if given, else the first unchecked item of the first `status: ready` chunk. None left -> say which chunk is next and what it needs (`/grill chunk N`, `/research`, `/architecture chunk N`, `/ready chunk N`).
4. Item is `T-n` and branch `t-<n>-*` exists with an IMPLEMENTME.md (a re-run after /retro) -> rewrite that file in place, keep its `issue:` line.

## Read (as little as possible)
- `plan.md` in full: checked items = done work; Decisions; Open questions for this chunk.
- `AGENTS.md` `## Layout`: pick the folders the item touches.
- Those folders' `README.md`, then only the files the change needs. `git log --oneline -20` for recent work.
- Every place the change must reach: grep each function, class and file you will change for its callers, tests, fixtures, config and exports. Callers that would break go in `touch`; the rest in `read`.
- What the change could break for users: data it could destroy or expose, callers that stop working.
- Never read the whole repo.

## Choose the approach
Take the first rung that fully works:
1. Not needed: part of the item already works, or nobody asked for it -> drop that part and name it under Out of scope.
2. Existing code in this repo (helper, module, pattern) -> use it the way the surrounding code does.
3. Standard library or platform feature.
4. A dependency already installed. Never add one for a few lines; a new dependency needs a plan.md decision, else it goes under Questions.
5. A line or two a reader gets at a glance.
6. The minimum new code that works.

Rules:
- Lazy about the solution, never about the change: every caller, test and fixture the change breaks is in `touch`.
- Fix -> the root cause, once, in the shared code, not at each caller.
- No abstraction, wrapper, option, config or "for later" code that Done when doesn't need. Keep values in the form the code already uses. Keep the repo's structure, layers and conventions. Deleting beats adding.
- Two options of equal size -> the one that is correct on edge cases.
- A known limit you accept -> name it under Approach as a shortcut (limit + when to upgrade).
- Never cut: validation at trust boundaries, error handling that prevents data loss, security, anything the line item asks for.

## Write
Branch `t-<n>-<slug>` from main. Write repo-root `IMPLEMENTME.md` from `implementme-template.md` in this skill's directory. Leave it uncommitted.
- One change. The item turns out to be 2+ changes -> stop and propose a split of the line item (user decides; you edit plan.md).
- Approach: the rung you took and, in one line, why the cheaper rungs don't work.
- Exact: file paths, function names, test names. The implementer reads only this file and the files it lists.
- Copy the text of every decision that applies; don't just cite ids.
- Item creates a top-level folder -> include its `README.md` and the `AGENTS.md` Layout line in `touch`.
- Architecture page item -> under `read`: `../architecture/page/instructions.md` from this skill's directory (absolute path), the ADRs, and the code of every part it describes. Copy that file's "Done when" list into Done when. `docs/architecture/` missing -> `touch` gets every file in `../architecture/page/templates/` as new. test_cmd for this item: `docs/architecture/build.sh`.
- Fits one screen (about 60 lines). Longer -> the item is too big: propose a split.
- Behavior nobody decided -> don't guess: put it under Questions. /shipit won't run until Questions says none.

## Done
Reply: path, item, approach rung, number of files to touch. Then one or two lines: what you skipped or did not check, and any risk the user must know. "Review it, ask for edits, or type `/shipit` to approve."
