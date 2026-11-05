# ADR 0005: Multi-harness support

Status: research pending

## Why
Skills should work across the major agent harnesses, not only Claude Code. Initial targets: Claude Code, Codex, Cursor, Pi, OpenCode.

## Investigate
- What each harness supports: SKILL.md / Agent Skills standard, slash commands, hooks, frontmatter (args, argument hints, model)
- Lowest common denominator vs per-harness adapters
- One universal settings format possible across harnesses? (pref: yes; JSON candidate) Else per-harness translation by deterministic script.
- Where config lives in each harness; mapping our layered config (global/project shared/project local/args)
- Shipping deterministic scripts portably (runtime deps: bash/python/node?)
- Install/distribution per harness (plugin, marketplace, copy, installer script)
- Per-harness gaps for ADR 0002 (usage limits) and ADR 0003 (arg hints)
- Background subagents per harness (teach-me inline mode: quiz in main thread while subagent implements)

## Findings (2026-11-05)
- Agent Skills std (agentskills.io) supported natively: Claude Code, Codex, Cursor (2.4+), Pi. OpenCode unclear (native vs `npx skills add`) -> verify.
- Portable frontmatter: name, description, license, compatibility, metadata, allowed-tools (experimental). `argument-hint`, `model` = Claude Code extensions; may fail strict validation elsewhere.
- Harnesses: model reads SKILL.md via its own tools -> config read by model is portable.
- Still verify: arg passthrough per harness; OpenCode native support; frontmatter extension tolerance.
