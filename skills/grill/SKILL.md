---
name: grill
description: 'Light conversation about an app idea (vision, users, hosting, features, growth), then write plan.md as chunks of small line items, each one PR. Use first in a new repo, or for a later chunk marked `needs: grill`. args: "[chunk N]"'
metadata:
  version: "1.1.0"
---

# grill

A conversation, not an interrogation. Keep it light and non-technical; how it is built belongs to /irs:architecture.

## Input
- No `plan.md` at repo root -> new idea: create it from `plan-template.md` in this skill's directory.
- `chunk N` -> talk through only that chunk's `to figure out` list. No arg + plan.md exists -> first chunk whose `needs` includes grill.

## Loop
- One question at a time: 1-2 lines of context, 2-4 options, your recommendation. Give honest feedback: say when an idea is risky, big, or common.
- New idea covers: vision, users, hosting (where it runs, who can reach it), the features they want, what the first release must show, growth, non-goals.
- Growth is four answers, all recorded: now, next year, maximum potential (the most it could become if it takes off), and how fast it could get there. Push for a real number on the last two; "it could go viral" is an answer (then: how big, how soon?).
- No technical design (libraries, data models, folders). User raises one -> add it to Open questions for /irs:architecture and move on.
- Research only when the user says "research it": spawn a subagent with `../research/SKILL.md` from this skill's directory (absolute path) and the question, called by /irs:grill; use the findings block it returns.
- Edge cases: don't ask. Add each to Open questions as `E-n`.
- The user decides. Never write down something they did not say. Write plan.md as you go, so the session can be resumed.
- Aim for about 10 questions for a new idea, fewer for one chunk. User says "enough" -> stop and write.

## Writing plan.md
- Chunk 1 = the first walking skeleton (definition in plan.md). Later chunks = further skeletons or iterations toward v1, then going live and scaling, however the conversation shapes it. No fixed count.
- Chunk 1: list every line item. Later chunks: goal, `needs:`, a `to figure out` list; line items only where obvious.
- Line items follow the plan.md rule: one PR, one change. In doubt -> split. Order them so each builds on merged ones; chunk 1 usually starts with the project skeleton (package, test runner, CI passing).
- `needs:` = conversations still required before /irs:ready (grill, research, architecture). Chunk 1 after the first grill: `needs: research, architecture`.

## Done
Reply: plan.md path; per chunk: name, line item count, needs; open question count. Next: `/irs:research` (new idea) or `/irs:architecture chunk N`.
