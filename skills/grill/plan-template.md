<!-- plan.md: the source of truth for this repo. /irs:grill, /irs:research and /irs:architecture write it; /irs:ready commits it in a plan PR; each /irs:shipit PR checks off its line item.
     IDs: D-n decisions, T-n line items, E-n open questions. Never renumber; deleted IDs stay retired. -->
# <app name>

## Vision
<1-3 sentences: what it is, for whom, why>

## Users
- <who: what they need from it>

## Hosting
<where it runs, who can reach it>

## Growth
- now: <users, data, load at launch>
- next year: <realistic>
- maximum potential: <the most it could become if it takes off: users, data, load, features>
- how fast: <how quickly it could get there, e.g. "weeks, if a post goes viral">
<Architecture builds the simplest thing that fits now and can reach the maximum potential in time.>

## Non-goals
- <not building>

## Research
<written by /irs:research>

## Decisions
<written by /irs:architecture; each decision also has an ADR in docs/adr/>
- test_cmd: `<one command that runs all tests from repo root>`

## Chunks
Walking skeleton = production-quality code with bare-bones scope: the smallest end-to-end version that shows how the app looks and feels. Not throwaway: tests, error handling and security are real. Cut scope, never quality.
Line item = one PR that changes one thing (one behavior, fix, or enhancement), small enough for the user to review in about 15 minutes. Two things -> two line items. Many small items is right.
Chunk status: draft -> ready (user, via /irs:ready) -> done (last item merged).

### Chunk 1: <name> | status: draft
- goal: <what the user can see or do when this chunk is done>
- needs: research, architecture
- [ ] T-1: <one change>
- [ ] T-2: Architecture page, diagram and video for chunk 1 (folders: docs/architecture/)

### Chunk 2: <name> | status: draft
- goal: <...>
- needs: grill, architecture
- to figure out:
  - <question>

## Open questions
<noted, not asked; settled in a later /irs:grill or /irs:architecture>
- E-1: <question or edge case> | chunk: 2
