---
type: llm
focus: { source: file, path: specs/out.md }
---
<!-- body synced from evals/rubrics/artifact.md by scripts/test.sh; edit the rubric, not this -->
Judge: a written ARTIFACT (spec file). Rules: max word economy, grammar sacrificable, zero fluff; goal = implementing agent executes ~100% correctly; examples/edge cases only when they raise accuracy, written tersely. Economize words, not information. Role/level/budget must have no effect. audience=agent: terse bullets, no prose. audience=human: same + short Context section + 1-line rationale for non-obvious choices.

Required sections in order: Goal, Constraints, Interfaces, Files touched, Acceptance criteria, Out of scope (human adds Context first; Open questions at end if unknowns).

Checklist (PASS/FAIL each, quote evidence for FAIL):
1. All required sections present, in order.
2. Acceptance criteria are testable (observable, specific).
3. No invented requirements beyond the request; unknowns go to Open questions.
4. No filler sentences/words; every line carries info.
5. An implementing agent could build it without asking questions (or the questions are listed).
6. Prose level matches audience (agent: none; human: brief, still economical).

PASS only if all 6 pass.
