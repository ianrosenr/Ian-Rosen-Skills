# notes

## Vision
A tiny CLI for plain-text notes in `notes/`.

## Users
- Me: quick notes from the terminal.

## Hosting
Runs locally on my Mac. No network.

## Growth
Maybe search later. Single user.

## Non-goals
- sync between devices

## Research
- verdict: pursue | date: 2026-11-20

## Decisions
- test_cmd: `python3 -m unittest -q`
- D-1: Python stdlib only, no dependencies | why: tiny tool | door: two-way | chunk: 1 | adr: 0001
- D-2: Notes are plain `.md` files in `notes/` | why: easy to read and back up | door: one-way | chunk: 1 | adr: 0002

## Chunks
Walking skeleton = production-quality code with bare-bones scope. Cut scope, never quality.
Line item = one PR that changes one thing.

### Chunk 1: list and show | status: draft
- goal: I can list my notes and print one
- needs:
- [ ] T-1: Project skeleton: package, unittest runner, CI passing (folders: ., tests/)
- [ ] T-2: `notes list` prints note names, sorted (folders: .)
- [ ] T-3: `notes show <name>` prints one note; names must match `[A-Za-z0-9_-]+` (folders: .)

### Chunk 2: search | status: draft
- needs: grill, architecture

## Open questions
- E-1: very long notes, page them? | chunk: 2
