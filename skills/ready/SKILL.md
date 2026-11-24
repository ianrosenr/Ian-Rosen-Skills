---
name: ready
description: 'Check one chunk of plan.md for obvious gaps (open questions, security, data loss, line items that are not one change), then on the user''s yes mark it ready and open a plan PR. args: "[chunk N]"'
metadata:
  version: "1.0.0"
---

# ready

Input: repo-root `plan.md`. Chunk = `chunk N`, else the first chunk with `status: draft`.

## Checks (obvious gaps only)
1. `needs:` is empty. Else stop: run those conversations first.
2. Open questions tagged with this chunk that a line item needs answered to be built right.
3. Security: untrusted input, auth, secrets or PII touched by a line item with no decision.
4. Data: a line item can lose or corrupt user data with no decision.
5. Line items: each is one change, ordered so each builds on earlier ones, together they reach the chunk goal (anything missing?).
6. Decisions conflict with each other or with Non-goals.

Not blockers: naming, details the implementme step can settle from the code, rare edge cases (add as `E-n`).

## Rules
- Never answer questions or edit decisions. Propose splits; the user decides.
- Each blocker: where (T-n, D-n or E-n), problem, a question for the user with 2-3 options.

## Done
- Block -> list blockers. Next: answer them (in this chat for small ones, or `/architecture chunk N` / `/grill chunk N`), then `/ready chunk N` again.
- Pass -> ask "Mark chunk N ready?" On yes: set `status: ready`; create branch `plan-chunk-N` from main; commit plan.md (and AGENTS.md if changed) as `Plan: chunk N ready`; push; `gh pr create` with the chunk's goal and line items in the body. Reply with the PR link. Next: merge it, then `/implementme`.
