# NEXT

Resume point. Agent: read CONTEXT.md first, then work through this top-down. Grill user; record answers in CONTEXT.md; strike resolved items here.

## Status (2026-11-05)
- SCOPE (user, 2026-11-05): POC-1 = bare `/spec` + `/explain` only. OUT of POC-1 (later): plugin, versioning, version pinning, update warnings, skill testing/evals. DONE: `scripts/link-skills.sh` symlinks each skill -> `~/.claude/skills/<name>` (Pocock-style); old `~/.claude/skills/irskills` plugin link removed (was cause of `irskills:` prefix). Shared rules via per-skill symlink `config-rules.md -> ../_shared/`.
- POC-1 implemented (skills/, examples/, .gitignore, symlinked into ~/.claude/skills/). Pending manual testing.
- Repo: ianrosenr/Ian-Rosen-Skills (public). Local ~/Projects/Skills. Commit after each session.
- ADRs 0001-0009 created, all barren (why + investigate only).

## Outstanding questions
1. Skill list (ADR 0004): dedicated convo. SE principles + roles -> ~10-15 skills. Roles incl designer/QA/exec; skills may extend beyond SE.
2. Config folder name (`irskills` provisional).

## NEXT SESSION (user request)
- "Something is still wrong." Figure out proper test design + shipping. Start from TEST-APPARATUS.md + SHIPPING.md (handoffs w/ suspect items + questions). Grill user.

## Immediate next: test POC-1
- `scripts/test.sh` (automated; supersedes most of POC-1-TESTS.md manual list). Then `--save-baseline`.
- Fails (precedence errors, free-word misparse) -> feed ADR 0001/0003/0005. Then update CONTEXT.md.
- Known weak: topic starting w/ vocab word (`explain normal distribution`) misparsed; workaround `--`.
- Impl decisions beyond POC-1.md (confirm w/ user): `<root>`=git root else cwd; `--` ends free words; flag > free word; dup dial last wins; notes appended to echo line as `note: ...`; human-audience spec also ignores role/level/budget, adds Context section; spec path via "to <path>.md" in input; spec default dir `specs/`.

## Testing + versioning (2026-11-05) -> TESTING.md
- Built: scripts/test.sh (static | plugin eval | pairs + judges), 17 cases, 6 rubrics, 3 pairs, semver per skill + plugin, CHANGELOG.
- Smoke: e01 pass ($0.05). Full paid run not yet done; no baseline saved.
- Pair smoke p01: pipeline works. Side A got 'skill isn't installed': cause = ~/.claude/skills symlinks shadow plugin -> skills register as `explain` not `irskills:explain`. Fixed in runner via `--setting-sources project,local` (also drops user CLAUDE.md bias). Added echo-line check to pairs. DONE: per-skill symlinks removed; install = `~/.claude/skills/irskills -> repo` (loads as plugin irskills@skills-dir, live edits). User types `/explain`; tests use same. Judge flagged factual error in expert reply (HKDF arg order) -> real quality signal.
- Finding: model resolves `~` by guessing real home -> global layer untestable in eval (evals-pending/). Decide fix (ADR 0005).
- Budget scoped to replies only; artifacts rule added (see CONTEXT).

## Next steps
- (2026-11-05) ADR 0003 CC done: `claude-code/flag-complete/` + root marketplace.json, spec D2 exception. TODO: verify live (`/plugin install flag-complete --marketplace /Users/ianrosen/Projects/Skills`, type `/explain -r`); decide long flags in hints (skill change -> bump + tests); commit.
0. Distribution spec (specs/distribution-migration.md): P1-P4 folded + grilled; update check revised to script + daily + warn-once (2026-11-05). NEXT: impl in new session. First verify: CC `!` preprocessing in skills + `${CLAUDE_SKILL_DIR}` + allowed-tools form, `CODEX_SANDBOX_NETWORK_DISABLED`, `npx skills update`/`add --skill` scoping (fixes `<AU>`), same-name clash behavior, Pi alias, `--setting-sources` loads ws skills, Codex rules via `codex execpolicy check`. Before POC-1 test run.
0b. After impl: GH issue #1 — revisit POC-1 'model resolves config, no script' (script-side config/args/echo?). Grill user.
1. Finish grilling: questions above.
2. Skill-set convo -> fill ADR 0004.
3. Research ADRs w/ user (user wants to learn, not get answers): 0001 budget/effort, 0006 skills+tools, 0005 harnesses, 0002 usage routing, 0003 arg hints, 0007 teach-me memory/adaptive, 0008 styles (back burner), 0009 per-skill model class.
4. Write decisions back into ADRs (Status -> Accepted).
5. Design config schema (roles, levels, budgets, audience, per-skill model defaults, layering).
6. ~~POC-1 impl~~ done -> test per POC-1-TESTS.md.
