---
name: architecture
description: 'Decide only what the next chunk of plan.md needs to be built (layout, data, interfaces, dependencies, security, tests), note everything else without asking, and refine the chunk''s line items. Use after /grill and /research, before /ready. args: "[chunk N]"'
metadata:
  version: "1.0.0"
---

# architecture

Input: repo-root `plan.md`. Chunk = `chunk N`, else the first chunk whose `needs` includes architecture.

## Core principle
Build the simplest thing that lets the app grow into `## Growth`. Every question's options include the simplest one; recommend it unless it blocks Growth, and then say what it blocks.

## Defaults
- Python 3.12+, uv, pytest, unless the user picks otherwise.
- Use the `## Research` services the user agreed to.

## Loop
- Ask only what blocks this chunk's line items. One question at a time: 1-2 lines of context, 2-4 options (simplest included), your recommendation + why.
- Edge cases, later-chunk questions, nice-to-knows: don't ask. Add to Open questions as `E-n` tagged with a chunk.
- Always ask (never defer): security (auth, untrusted input, secrets, PII) and anything that can lose user data.
- One-way doors (data model, public interface, hosting, security model): probe harder; say the reversal cost.
- The user decides. Write each decision to `## Decisions` right away: `- D-n: <decision> | why: <reason> | door: one-way|two-way | chunk: N`.
- Aim for the fewest questions that let the chunk start. User says "enough" -> stop; remaining questions -> Open questions.

## Check each (ask only what blocks)
- Layout: top-level folders (packages) and what each owns, drawn so a line item touches 1-2 folders. Mostly chunk 1, or when a chunk adds a folder.
- Data: what is stored, where, rough shape.
- Interfaces: CLI, API or UI entry points and their shapes.
- Dependencies: which libraries and services.
- Security: trust boundaries, where secrets live, auth.
- Testing: `test_cmd`, what is faked.
- Running: how it runs and deploys (chunk 1: minimal).

## Write
- Decisions -> plan.md. Set `test_cmd` once decided.
- Line items of this chunk: split anything that is more than one change, add missing ones (project skeleton, CI), order by dependency. Format: `- [ ] T-n: <change> (folders: a/, b/)`.
- Layout decided -> repo-root `AGENTS.md` `## Layout` (create if missing): one line per top-level folder: what it owns. Each folder's `README.md` is written by the line item that creates the folder.
- Remove `architecture` from the chunk's `needs`.

## Done
Reply: decisions added (id + one line), line item count, open questions added. Next: `/ready chunk N`.
