# notes

## Vision
A tiny CLI for plain-text notes in `notes/`.

## Decisions
- test_cmd: `python3 -m unittest -q`
- D-1: Python stdlib only, no dependencies | why: tiny tool | door: two-way | chunk: 1

## Chunks
Walking skeleton = production-quality code with bare-bones scope. Cut scope, never quality.
Line item = one PR that changes one thing.

### Chunk 1: basics | status: ready
- goal: list, export, and hide drafts
- needs:
- [x] T-1: `notes list` prints note names (folders: .)
- [x] T-2: `notes export <file>` writes all notes into one file (folders: .)
- [ ] T-3: Drafts: notes whose name starts with `_` are hidden from `list` and `export` (folders: .)

## Open questions
