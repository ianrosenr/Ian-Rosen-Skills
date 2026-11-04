# ADR 0004: Skill set selection

Status: research pending. Needs a dedicated conversation with the user.

## Why
Target is ~10-15 skills covering a normal SDLC. They should rest on time-tested SE principles and cover the roles people play (dev, reviewer, PM, etc.). Avoid the verbose, sprawling packs.

## Investigate
- Foundational SE principles/practices to anchor the skills (SDLC phases, spec->impl->test->review->release, etc.)
- Roles people play on a project, and which skills each role needs
- Survey of popular skill packs: what's there, what's redundant or bloated
- Overlaps: which candidate skills merge, and which stay separate
- How each skill uses the level/budget dials + the audience flag (human vs agent)

## Seed idea
- `spec` skill with an audience flag: agent (default) | human. Overridable in settings or per call.
  - Agent spec: every detail kept, minimal characters -> lean context for implementation agents.
  - Human spec: slightly more prose for readability, not much.
- `teach-me` skill: session-wide quiz/exploration mode. Gauges user's grasp, asks questions. Respects budget. Key use: architecture.
