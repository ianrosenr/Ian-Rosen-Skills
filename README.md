# Ian-Rosen-Skills

Claude Code skills for building an app one small, reviewed PR at a time. You make the decisions in short conversations, agents write the code, and you review every PR before it merges.

## Install
Claude Code plugin `irs`; commands are `/irs:grill`, `/irs:shipit`, ...
```
claude plugin marketplace add ianrosenr/Ian-Rosen-Skills
claude plugin install irs@irskills
```
Every repo made by `/new-repo` already declares it in `.claude/settings.json`, so opening one in Claude Code offers to install it. Update: `claude plugin marketplace update irskills && claude plugin update irs@irskills`.

Working on the skills themselves: `claude --plugin-dir ~/Projects/Skills` loads your local copy (edits apply on the next session) instead of the installed one.

Needs: `gh` (logged in), `git`. Apps default to Python (uv, pytest).

## The flow
Two files drive everything in the app repo:
- `plan.md`: vision, research, decisions, and chunks of line items. One line item = one PR = one change.
- `IMPLEMENTME.md`: exact instructions for the one line item being built. It becomes the GitHub issue, and the PR deletes it.

| You type | What happens |
|---|---|
| `/new-repo <name>` | Creates the repo (separate tool). |
| `/irs:grill` | Light conversation about the idea. Writes plan.md: chunk 1 (the first walking skeleton) with every line item, later chunks with what still needs figuring out. |
| `/irs:research [question]` | No question, after the first grill: does this exist already, what can we use instead of building, pursue verdict. With a question: the tried-and-tested ways to do it at this app's size and growth, with a recommendation and sources. |
| `/irs:architecture` | Decides only what chunk 1 needs; edge cases get noted, not asked. Writes an ADR (Architecture Decision Record) per decision in `docs/adr/`. Refines the line items, ending the chunk with an architecture page item. |
| `/irs:ready` | Checks the chunk for obvious gaps. On your yes, marks it ready and opens a plan PR (plan.md + ADRs). You merge it. |
| `/irs:implementme` | Writes IMPLEMENTME.md for the next line item. You review it and ask for edits. |
| `/irs:shipit` | Your approval. Creates the issue, then implement, review, at most one fix and a second review, then stops and reports. Clean -> PR (checks off the line item, deletes IMPLEMENTME.md). |
| `/irs:shipit <PR#>` | After you comment on the PR: the implementer addresses each comment, the reviewer checks the fixes, replies go on each thread. You resolve threads and merge. |
| `/irs:retro` | When review 2 isn't clean: we find which step let the problem through, fix that skill here, add test cases with your expected output, run the tests, open a PR in this repo. Then `/irs:shipit` re-runs the same item. |

After a merge, `/irs:implementme` starts the next item. When a chunk is done, run its `needs` (`/irs:grill chunk N`, `/irs:research`, `/irs:architecture chunk N`), then `/irs:ready chunk N`. Each command ends by naming the next one, and every step works from a fresh session because state lives in files and GitHub.

## Planning: from idea to a ready chunk
Before any code, two conversations build `plan.md`. Nothing is committed until you approve a chunk.

```
/new-repo my-app                 empty repo: rules, checks, protection, plugin
  │
/irs:grill                       light, non-technical conversation, one question at a time
  │   vision, users, hosting, features, what the first release must show, growth, non-goals
  │   edge cases are noted (E-n), not asked
  └─► plan.md: chunk 1 = first walking skeleton, every line item listed (one PR each)
               later chunks = goal + "needs" + "to figure out"
  │
/irs:research                    idea check: competitors, services to use instead of building, pursue verdict
  └─► plan.md ## Research; proposed plan changes applied only if you agree
  │
/irs:architecture                technical conversation, only what chunk 1 needs to start
  │   layout, data, interfaces, dependencies, security, tests; simplest option first
  │   security and data-loss questions always asked; everything else noted, not asked
  │   questions with an industry-standard answer: researched first (subagent), options cite it
  └─► plan.md ## Decisions (D-n), docs/adr/NNNN-*.md per decision, AGENTS.md ## Layout,
      line items split to one change each, last item = architecture page + diagram + video
  │
/irs:ready                       checks the chunk for obvious gaps (open questions, security,
  │                              data loss, items that are more than one change, missing ADRs)
  │   gaps → answer them (in chat or another /irs:architecture), re-run /irs:ready
  └─► your yes → status: ready, plan PR (plan.md + ADRs) → you merge = chunk approved
```
- **Grill is the "what", architecture is the "how".** If you start talking technology in grill, it's parked for architecture; if an architecture answer would change what the app does, it sends you back to grill.
- **You approve in chunks.** Only the next chunk gets detailed planning; later chunks stay as goals and questions until their turn: `/irs:grill chunk N` and/or `/irs:architecture chunk N` (whatever its `needs` says), then `/irs:ready chunk N`.
- **Sessions are resumable.** Everything is written to plan.md as you go, so `/clear` between steps is fine.

## Inside `/irs:shipit`
One line item, one run, one PR. You stay in control at three points: approving IMPLEMENTME.md (typing `/irs:shipit` is the approval), reading the report, and merging the PR.

```
/irs:shipit
  1. issue      gh issue create, body = IMPLEMENTME.md (re-run after /irs:retro: reuse the issue, reset the branch)
  2. implement  implementer subagent: tests first, only the files IMPLEMENTME.md lists
  3. review 1   reviewer subagent: whole diff, defects only, each with evidence
       clean ───────────────────────────────────────────────┐
       findings → 4. fix (implementer) → 5. review 2         │
                    clean ──────────────────────────────────┤
                    still findings / question → STOP        │
                      report: what's done, what's open,     │
                      suggested skill edits; no PR          │
                      next: /irs:retro                      │
  6. PR  ← ─────────────────────────────────────────────────┘
     removes IMPLEMENTME.md, checks the line item off in plan.md,
     body "Closes #<issue>"; report includes review 1's findings
  you review on GitHub, then merge: issue closes, branch is deleted
```
- Never a third review round: if two rounds don't settle it, the process has a gap, and that's what `/irs:retro` is for.
- Implementer or reviewer hits a decision IMPLEMENTME.md doesn't make: it stops and asks (an andon) instead of guessing.
- Your PR comments: `/irs:shipit <PR#>` runs the same loop on them (fix, review, at most 2 rounds), replies on each thread and pushes. Questions get answers, not code. You resolve threads.
- Every run's details are saved in `.git/shipit/T-<n>/` (never committed) for `/irs:retro`.

## What to use when
| Situation | Use |
|---|---|
| New app idea, no repo yet | `/new-repo <name>`, then `/irs:grill` in it |
| Repo exists but has no plan.md | `/irs:grill` |
| Idea talked through, not sure it's worth building | `/irs:research` |
| "How do apps like mine usually do X?" | `/irs:research <question>` (grill and architecture also do this on their own; say "research it" mid-conversation) |
| A chunk's line items need technical decisions | `/irs:architecture chunk N` |
| One line item is big (new component, data or outside service) | `/irs:architecture T-n` |
| Chunk looks done in plan.md, want to start building | `/irs:ready chunk N` |
| Plan PR merged, or the last item's PR merged | `/irs:implementme` |
| IMPLEMENTME.md looks wrong | Say what to change in the same session; it rewrites the file |
| IMPLEMENTME.md looks right | `/irs:shipit` |
| You left review comments on a PR | `/irs:shipit <PR#>` |
| Report says "not clean after review 2", or a PR comment shows the reviewer should have caught something | `/irs:retro` |
| After a `/irs:retro` PR merged | `/irs:shipit` (re-runs the same item) or `/irs:implementme T-n` first if IMPLEMENTME.md was the gap |
| Chunk finished, next chunk says `needs: grill` | `/irs:grill chunk N` |
| Not sure where you are | Run `/irs:implementme`: it checks for open PRs, ready chunks and what the next chunk needs, then tells you |

Walking skeleton = production-quality code with bare-bones scope: the smallest end-to-end version that shows how the app looks and feels. Cut scope, never quality.

Architecture page: every chunk's last line item updates `docs/architecture/`: a page (`index.html`, open it in a browser), a D2 diagram and a narrated video (Manim + Kokoro), written for a junior software engineer: every acronym spelled out, one analogy family, and for each step how the hop works (transport, auth, payload, sync/async, failure, why). Rules: `skills/architecture/page/instructions.md`. Rebuild: `docs/architecture/build.sh` (needs `brew install d2 cairo pango pkgconf espeak-ng` and uv).

Folder docs: `AGENTS.md` `## Layout` lists each top-level folder; each folder has a README.md (purpose, public interface, conventions). IMPLEMENTME.md points the implementer at only the folders it needs.

## Skills
| Skill | File |
|---|---|
| grill | `skills/grill/SKILL.md`, plan.md template `skills/grill/plan-template.md` |
| research | `skills/research/SKILL.md` |
| architecture | `skills/architecture/SKILL.md`, ADR template `adr-template.md`, page kit `page/` (instructions + templates) |
| ready | `skills/ready/SKILL.md` |
| implementme | `skills/implementme/SKILL.md`, template `skills/implementme/implementme-template.md` |
| shipit | `skills/shipit/SKILL.md`; subagents `skills/shipit/implementer.md`, `skills/shipit/reviewer.md` |
| retro | `skills/retro/SKILL.md` |

Each file carries its own version. CHANGELOG.md records every bump.

## Tests
```
python3 tests/run.py            # all cases
python3 tests/run.py shipit     # one skill folder
python3 tests/run.py --case reviewer-missing-name-check --runs 3
```
Free check that every skill's frontmatter parses: `uv run --with pyyaml tests/check_frontmatter.py`.

Each run builds a fresh temp workspace from the case's fixture, runs the skill in a fresh `claude -p` session (never resumed, never saved), and a judge model grades the output against `expected.md`. No cached inputs, no baselines. Costs tokens. Results go to `tests/results/<time>/` (gitignored).

A case is a folder `tests/cases/<skill folder>/<case>/`:
- `case.toml`: `skill = "shipit/reviewer.md"` (the file under test, relative to `skills/`)
- `prompt.md`: what the agent is told; `{skill}` becomes that file's absolute path
- `files/`: the fixture, copied into the workspace
- `setup.sh` (optional): runs in the workspace after copying (e.g. builds git history)
- `expected.md`: bullets starting `must:` or `must not:`, in your words

`/irs:retro` adds a case for every gap it fixes, so this set grows from real misses.
