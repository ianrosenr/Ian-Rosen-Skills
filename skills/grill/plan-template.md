<!-- plan.md: the source of truth for this repo. /grill, /research and /architecture write it; /ready commits it in a plan PR; each /shipit PR checks off its line item.
     IDs: D-n decisions, T-n line items, E-n open questions. Never renumber; deleted IDs stay retired. -->
# <app name>

## Vision
<1-3 sentences: what it is, for whom, why>

## Users
- <who: what they need from it>

## Hosting
<where it runs, who can reach it>

## Growth
<what it must be able to grow into (users, data, features), roughly when. Architecture builds the simplest thing that does not block this.>

## Non-goals
- <not building>

## Research
<written by /research>

## Decisions
<written by /architecture>
- test_cmd: `<one command that runs all tests from repo root>`

## Chunks
Walking skeleton = production-quality code with bare-bones scope: the smallest end-to-end version that shows how the app looks and feels. Not throwaway: tests, error handling and security are real. Cut scope, never quality.
Line item = one PR that changes one thing (one behavior, fix, or enhancement), small enough for the user to review in about 15 minutes. Two things -> two line items. Many small items is right.
Chunk status: draft -> ready (user, via /ready) -> done (last item merged).

### Chunk 1: <name> | status: draft
- goal: <what the user can see or do when this chunk is done>
- needs: research, architecture
- [ ] T-1: <one change>

### Chunk 2: <name> | status: draft
- goal: <...>
- needs: grill, architecture
- to figure out:
  - <question>

## Open questions
<noted, not asked; settled in a later /grill or /architecture>
- E-1: <question or edge case> | chunk: 2
