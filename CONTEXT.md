# CONTEXT

Agent-facing. Terse. Planning phase. Read this + NEXT.md + POC-1.md + docs/adr/*. Resume from NEXT.md.

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
  - Controls output verbosity mainly; work effort should not drop (ADR 0001). No hard caps.
- Dials (level/budget) apply to conversational output to the human. NOT to agent-facing artifacts.
- Agent-facing artifacts (e.g. spec w/ audience=agent) always machine-optimized: full relevant detail, zero fluff.
- Audience flag: agent (default) | human. Overridable in settings/per call. Human = slightly more prose for readability, not much.
- Per-skill model class guidance (ADR 0009): in skill instructions, abstract classes not hard-coded names. Ex: implement=low, plan/spec=high, explain=low-mid by length/difficulty. Overridable global/project/per prompt. Not in POC.
- project-manager role: assume non-technical. Frame by impact/risk/timelines.
- Code for non-eng roles: no flag. Agent decides; show only if critical. Keep simple.
- Settings: one universal format, all harnesses. No per-harness/per-model translation.
- Config resolution: MODEL reads config files (no script) -> OS-agnostic, zero deps. Mitigations: tiny flat files; shared resolution rules in one reference file; model echoes resolved values in 1 line (verifiable).
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

## Process
- ADRs = barren: only what to investigate + why. Research after grilling done.
- One ADR per major research question.
