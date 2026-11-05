# POC-1

Agent-facing. Terse. Implement in a fresh session. Read CONTEXT.md first for rationale.

## Goal
Prove the dial mechanics end-to-end in Claude Code: config layering + arg overrides -> model resolves role/level/budget/audience -> skill output changes accordingly. No scripts. Agent Skills std only.

## In scope
- Shared config rules file
- Skill `explain` (exercises role/level/budget in conversational output)
- Skill `spec` (exercises audience flag; agent-facing artifact ignores level/budget)
- Claude Code `argument-hint` (only harness extension allowed)
- Example config files

## Out of scope
teach-me, styles (ADR 0008), per-skill model class (ADR 0009), usage routing (ADR 0002), other harnesses (ADR 0005), installer, scripts/tools (ADR 0006), memory.

## Layout
```
skills/
  _shared/config-rules.md     # single source: paths, precedence, arg parsing, tier rules, echo line
  explain/SKILL.md
  spec/SKILL.md
examples/
  global.config               # sample ~/.config/irskills/config
  project.config              # sample .irskills/config
  project.config.local        # sample .irskills/config.local
```
- Skills reference `../_shared/config-rules.md` by relative path. Known portability risk (skill installed alone loses it) -> note in ADR 0005, fine for POC.
- POC install: symlink `skills/explain`, `skills/spec`, `skills/_shared` into `~/.claude/skills/`.

## Config
- Format: flat `key=value`, one per line, `#` comments. No nesting.
- Keys: `role`, `level`, `budget`, `audience`.
- Paths (folder name `irskills` provisional):
  1. global: `~/.config/irskills/config`
  2. project shared (committed): `<repo>/.irskills/config`
  3. project personal (gitignored): `<repo>/.irskills/config.local`
- Precedence: args > project personal > project shared > global > built-in defaults.
- Missing files = skip silently. Unknown keys/values = ignore + mention once.
- Project shared must not set role/level (personal). If present: ignore, mention once.
- Defaults: `role=engineer level=competent budget=normal audience=agent`.

## Args
- Flags: `-r/--role`, `-l/--level`, `-b/--budget`, `-a/--audience`.
- Free words: leading tokens matching a known value (any dial) are consumed as dials until first non-matching token. Rest = task input. Flags allowed anywhere.
- Value vocab:
  - role: engineer, project-manager (alias pm), business-manager, designer, qa, executive
  - level: novice, competent, proficient, expert
  - budget: bare, lean, normal, verbose
  - audience: agent, human
- Ambiguous/invalid -> use resolved default, note it in echo line.

## Echo line
First line of every response: `[role·level·budget·audience]`, e.g. `[engineer·novice·lean·agent]`. bare budget: still printed (cheap, verifiable).

## Tier rules (in config-rules.md, 1 line each, keep tight)
- Role: frames output for role. Non-eng roles: impact/risk/timelines; code only if agent judges critical.
- Level (read through role):
  - novice: define terms, analogies ok, check-ins at decision points + after file changes, explain why
  - competent: assume basics, explain non-obvious
  - proficient: skip basics, focus tradeoffs
  - expert: minimal explanation, edge cases/gotchas only
- Budget (conversational output only):
  - bare: zero fluff, densest format, every char justified
  - lean: short bullets, no preamble/recap
  - normal: concise prose + bullets
  - verbose: full explanation, examples
- Audience (artifacts): agent = full relevant detail, zero fluff, machine-optimized; human = slightly more prose for readability, not much. Role/level/budget never apply to artifacts (either audience). Artifacts: max word economy, examples/edge cases ok if terse.

## Skill: explain
- Input: topic / code ref / question.
- Resolve config -> echo line -> explain per role+level+budget.
- Read only what's needed to answer (targeted reads).
- argument-hint: `[-r role] [-l level] [-b budget] <topic>`

## Skill: spec
- Input: feature/change description.
- Resolve config -> echo line -> write spec to `specs/<slug>.md` (or path given).
- audience=agent (default): goal, constraints, interfaces, files touched, acceptance criteria, out of scope. Terse. No prose.
- audience=human: same sections + brief context/rationale.
- Conversational reply around the artifact still follows level/budget (e.g. bare: path + 1 line).
- argument-hint: `[-a agent|human] [-b budget] <feature>`

## Acceptance
1. No config files -> defaults used, echo `[engineer·competent·normal·agent]`.
2. Global only -> global values used.
3. Global + project + local -> precedence correct per key.
4. Project shared sets level -> ignored, mentioned.
5. Flags override all layers. Free words override all layers.
6. `explain novice bare <topic>` vs `explain expert verbose <topic>` -> visibly diff depth + length.
7. `explain -r pm <topic>` -> impact/risk framing, no code unless critical.
8. `spec <feature>` -> terse agent spec; `spec -a human <feature>` -> same sections + brief rationale.
9. spec artifact identical in density regardless of `-b`/`-l`/`-r`, either audience. Examples/edge cases only when they raise accuracy, terse.
10. SKILL.md frontmatter uses only std fields + `argument-hint`.

## Deliverables after POC
- Notes on failures (precedence errors, free-word misparse) -> feed ADR 0001/0003/0005.
- Update CONTEXT.md + NEXT.md.

## Open (decide during POC or flag)
- Config folder name (`irskills` provisional).
- Spec output dir default.
