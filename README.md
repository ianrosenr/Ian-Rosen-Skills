# Ian-Rosen-Skills

Claude Code skills for building an app one small, reviewed PR at a time. You make the decisions in short conversations, agents write the code, and you review every PR before it merges.

## Install
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a claude-code -g -y
```
Working on the skills themselves: clone and run `scripts/link-skills.sh` (symlinks `~/.claude/skills/<name>` to this repo, so edits take effect at once).

Needs: `gh` (logged in), `git`. Apps default to Python (uv, pytest).

## The flow
Two files drive everything in the app repo:
- `plan.md`: vision, research, decisions, and chunks of line items. One line item = one PR = one change.
- `IMPLEMENTME.md`: exact instructions for the one line item being built. It becomes the GitHub issue, and the PR deletes it.

| You type | What happens |
|---|---|
| `/new-repo <name>` | Creates the repo (separate tool). |
| `/grill` | Light conversation about the idea. Writes plan.md: chunk 1 (the first walking skeleton) with every line item, later chunks with what still needs figuring out. |
| `/research` | Does this exist already? What services can we use instead of building? Gives a pursue verdict. |
| `/architecture` | Decides only what chunk 1 needs; edge cases get noted, not asked. Writes an ADR (Architecture Decision Record) per decision in `docs/adr/`. Refines the line items, ending the chunk with an architecture page item. |
| `/ready` | Checks the chunk for obvious gaps. On your yes, marks it ready and opens a plan PR (plan.md + ADRs). You merge it. |
| `/implementme` | Writes IMPLEMENTME.md for the next line item. You review it and ask for edits. |
| `/shipit` | Your approval. Creates the issue, then implement, review, at most one fix and a second review, then stops and reports. Clean -> PR (checks off the line item, deletes IMPLEMENTME.md). |
| `/shipit <PR#>` | After you comment on the PR: the implementer addresses each comment, the reviewer checks the fixes, replies go on each thread. You resolve threads and merge. |
| `/retro` | When review 2 isn't clean: we find which step let the problem through, fix that skill here, add test cases with your expected output, run the tests, open a PR in this repo. Then `/shipit` re-runs the same item. |

After a merge, `/implementme` starts the next item. When a chunk is done, run its `needs` (`/grill chunk N`, `/research`, `/architecture chunk N`), then `/ready chunk N`. Each command ends by naming the next one, and every step works from a fresh session because state lives in files and GitHub.

Walking skeleton = production-quality code with bare-bones scope: the smallest end-to-end version that shows how the app looks and feels. Cut scope, never quality.

Architecture page: every chunk's last line item updates `docs/architecture/`: a page (`index.html`, open it in a browser), a D2 diagram and a narrated video (Manim + Kokoro), all written for someone who has never written code: every acronym spelled out, analogies, step by step. Rules: `skills/architecture/page/instructions.md`. Rebuild: `docs/architecture/build.sh` (needs `brew install d2 cairo pango pkgconf espeak-ng` and uv).

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

`/retro` adds a case for every gap it fixes, so this set grows from real misses.
