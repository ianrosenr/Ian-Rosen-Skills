# CONTEXT

Agent-facing. Terse. Planning phase. Read this + NEXT.md + POC-1.md + TEST-APPARATUS.md + SHIPPING.md + docs/adr/*. Resume from NEXT.md.

## Goal
- Hone reusable AI dev workflow. ~10-15 lean skills covering normal SDLC. Counter to verbose popular skill packs.
- Core dials: engineer level + budget. User-tunable, overridable per call.
- Max deterministic work (scripts/tools > model reasoning) -> protect context window, cut cost.
- Audiences: individual devs + teams (same skills/principles, diff level/budget per person).

## Decided
- Harnesses: multi-harness. Start: Claude Code, Codex, Cursor, Pi, OpenCode. More later (ADR 0005).
- Config layers, precedence: args > project local (gitignored) > project shared (committed) > global.
- Args: support both short flags (`-l learning -b lean`) and free words (`learning lean`).
- Level = Dreyfus skill model tiers (4 tiers: novice / competent / proficient / expert). Chosen bc domain-agnostic -> skills may transfer beyond SE.
- Role = separate dial (`--role`). Default: software engineer. List: engineer, project-manager, business-manager, designer, QA, executive.
- Level interpreted through role: role first, then "act at this level for this role". Level applies to all roles.
- Role + level settable globally or per project. Per-project role/level = personal (project local, gitignored), so teammates differ. Shared project file must not dictate per-person role/level.
- Budget = 4 named tiers: bare / lean / normal / verbose.
  - bare: zero fluff, every char scrutinized, bullets/any densest format.
  - Universal across skills, but ONLY conversational replies (answers). Not written artifacts. Resolved default applies regardless of skill; override per call. Skills never set own budget default.
  - Controls output verbosity mainly; work effort should not drop (ADR 0001). No hard caps.
- Dials (role/level/budget) apply to conversational replies only. NOT to any written artifact (spec, context file, docs), agent or human audience.
- Artifacts: max word economy, grammar sacrificable, zero fluff. Goal ~100% impl accuracy. Examples/edge cases ok when they raise accuracy, written tersely. Economize words, not information. Human audience = slightly more connective prose, still economical.
- Spec/context-file writing -> high model class by default (ADR 0009); needs intelligence to optimize every word.
- Agent-facing artifacts (e.g. spec w/ audience=agent) always machine-optimized: full relevant detail, zero fluff.
- Audience flag: agent (default) | human. Overridable in settings/per call. Human = slightly more prose for readability, not much.
- Per-skill model class guidance (ADR 0009): in skill instructions, abstract classes not hard-coded names. Ex: implement=low, plan/spec=high, explain=low-mid by length/difficulty. Overridable global/project/per prompt. Not in POC.
- project-manager role: assume non-technical. Frame by impact/risk/timelines.
- Code for non-eng roles: no flag. Agent decides; show only if critical. Keep simple.
- Settings: one universal format, all harnesses. No per-harness/per-model translation.
- Config resolution: MODEL reads config files (no script) -> OS-agnostic, zero deps. UNDER REVIEW: update check now a script; revisit -> GH issue #1 (deferred, after distribution impl). Mitigations: tiny flat files; shared resolution rules in one reference file; model echoes resolved values in 1 line (verifiable).
- Skill format: Agent Skills std (SKILL.md, portable frontmatter only). Harness extras (e.g. Claude Code `argument-hint`) optional, never required.
- Priority: POC soon. Defer nice-to-haves to ADRs.
- novice tier (was 'learning'): not stronger model. Check-ins/narration at decision points + after file changes -- explain what + why, without halting progress (pausing governed by harness). Model-agnostic.
- Options must be visible while typing (ADR 0003).
- Usage-limit-aware routing wanted (ADR 0002).

## Skill ideas (feed ADR 0004)
- `spec`: audience flag, agent default.
- `teach-me`: invocable anytime mid-convo (impl, post-impl, architecture, etc). Switches model output to teaching mode for rest of session: quizzes user, gauges grasp, explores interactively. Respects budget. Distinct from novice level tier (tier = explanation depth; teach-me = active teaching skill).
  - Flags must autocomplete so user discovers options (ADR 0003).
  - Blocking vs inline = flag. Default = inline: user quizzed in main thread while subagent implements from spec in background. Interactive flow + work proceeds. (Harness subagent/background support -> ADR 0005.)
  - Off: explicit stop supported; default = ends with session.
  - Cross-session memory of what user learned: wanted, mind context/memory cost (ADR 0007).
  - Difficulty: NOT fixed by level tier (senior may learn new tech). Adaptive: adjusts harder/easier per answer (ADR 0007). Key use: architecture -- counter juniors/full-stack devs letting models make all decisions unexamined.

## Open
See NEXT.md for full outstanding question list + next steps.
- Style prefs: back burner -> ADR 0008.
- The 10-15 skill list -> ADR 0004. Needs dedicated convo: SE principles + roles.
- Skills + built-in tools combo for cost optimization -> ADR 0006.

## Install
- (2026-11-05) Delivery mimics mattpocock/skills non-plugin route: `npx skills add` for ALL harnesses; his user-invoked markers; his `link-skills.sh` for dev. No plugin/marketplace (forces `irskills:` prefix + auto-update). Not copied: his layout, skills, process. Spec: specs/distribution-migration.md (not yet impl).
- (2026-11-05) Bare names everywhere: `/explain`, `/spec`. Repo layout may change to guarantee it.
- (2026-11-05) Skills user-invoked only (`disable-model-invocation: true` + Codex `agents/openai.yaml` `allow_implicit_invocation: false`).
- (2026-11-05) No auto-update by default; opt-in `auto_update=on` (+ `auto_update.<skill>`). REVISED: warn once per new release per skill (incl update cmd), then silent until next release (user may stay on a version). Fetch ≤1/day. Deterministic `update-check.sh` (POSIX sh) + state file `~/.config/irskills/update-state`; Claude Code runs it via `` !`…` `` preprocessing (zero model tool calls), other harnesses model runs it once/call (local, cheap). Disable `update_check=off` / `update_check.<skill>=off` / `--no-update-check`.
- (2026-11-05) Precedence update_check/auto_update: specificity-first: flag > per-skill key (highest layer) > global key (highest layer) > default.
- (2026-11-05) auto_update must touch ONLY the irskills skill being updated, never other skills/authors. Verified: `npx skills update <name> -g|-p` scoped (names only; no by-source update). Scope flag mandatory (else foreign same-name skill in other scope updated).
- (2026-11-05) Stay on `npx skills`. Upstream ask: `update owner/repo`. Fallback: git clone + symlinks (spec Open q 10).
- (2026-11-05) Fetch blocked -> BLOCK hint line. Offline/errors silent, ≤1 attempt/day.
- (2026-11-05) Permissions: `allowed-tools` = narrowest rule for script cmd (exact form at impl); README #permissions per-harness allow rules (Codex prefix_rule on script).
- (2026-11-05) Pi: investigate alias so `/explain` works (native `/skill:explain`).
- (2026-11-05) Names stay bare despite clash risk; README warns.
- (2026-11-05) Prereq Node ≥ 22.20; manual copy fallback.
- Exact strings/tests: specs/distribution-migration.md.

## Testing + versioning
- Dev-only eval harness: TESTING.md. One cmd `scripts/test.sh`; agent instruction "run the skill tests".
- Specialized judge rubrics per quality dimension; pass/fail checklists + evidence; judges never see skill instructions; judges may propose skill edits.
- No real-time feedback needed; summary per run.
- Semver per skill (`metadata.version`) + plugin version; CHANGELOG enforced; baselines per plugin version; regression = drop > 0.1.

## Process
- ADRs = barren: only what to investigate + why. Research after grilling done.
- One ADR per major research question.
