# CONTEXT

Agent-facing. Terse. Planning phase. Read this + NEXT.md + docs/adr/*. Resume from NEXT.md.

## Goal
- Hone reusable AI dev workflow. ~10-15 lean skills covering normal SDLC. Counter to verbose popular skill packs.
- Core dials: engineer level + budget. User-tunable, overridable per call.
- Max deterministic work (scripts/tools > model reasoning) -> protect context window, cut cost.
- Audiences: individual devs + teams (same skills/principles, diff level/budget per person).

## Decided
- Harnesses: multi-harness. Start: Claude Code, Codex, Cursor, Pi, OpenCode. More later (ADR 0005).
- Config layers, precedence: args > project local (gitignored) > project shared (committed) > global.
- Args: support both short flags (`-l learning -b lean`) and free words (`learning lean`).
- Level = named tiers (provisional): learning / working / senior / expert / project-manager.
- Budget = 4 named tiers: bare / lean / normal / verbose.
  - bare: zero fluff, every char scrutinized, bullets/any densest format.
  - Controls output verbosity mainly; work effort should not drop (ADR 0001). No hard caps.
- Dials (level/budget) apply to conversational output to the human. NOT to agent-facing artifacts.
- Agent-facing artifacts (e.g. spec w/ audience=agent) always machine-optimized: full relevant detail, zero fluff.
- Audience flag: agent (default) | human. Overridable in settings/per call. Human = slightly more prose for readability, not much.
- Per-skill model defaults in settings.json, overridable at any layer/per call. Not per-tier for now.
- project-manager tier: assume non-technical. Frame by impact/risk/timelines. No code by default; flag to opt in; surface that flag to user.
- learning tier: not stronger model. Check-ins/narration at decision points + after file changes -- explain what + why, without halting progress (pausing governed by harness). Model-agnostic.
- Options must be visible while typing (ADR 0003).
- Usage-limit-aware routing wanted (ADR 0002).

## Skill ideas (feed ADR 0004)
- `spec`: audience flag, agent default.
- `teach-me`: invocable anytime mid-convo (impl, post-impl, architecture, etc). Switches model output to teaching mode for rest of session: quizzes user, gauges grasp, explores interactively. Respects budget. Distinct from learning level tier (tier = explanation depth for someone learning SE generally; teach-me = active teaching skill). Key use: architecture -- counter juniors/full-stack devs letting models make all decisions unexamined.

## Open
See NEXT.md for full outstanding question list + next steps.
- Style prefs (e.g. analogies): separate setting vs implied by tier. User flagged revisit.
- Final level tier names/count.
- The 10-15 skill list -> ADR 0004. Needs dedicated convo: SE principles + roles.
- Skills + built-in tools combo for cost optimization -> ADR 0006.

## Process
- ADRs = barren: only what to investigate + why. Research after grilling done.
- One ADR per major research question.
