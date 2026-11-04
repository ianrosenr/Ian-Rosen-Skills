# ADR 0005: Multi-harness support

Status: research pending

## Why
Skills should work across the major agent harnesses, not only Claude Code. Initial targets: Claude Code, Codex, Cursor, Pi, OpenCode.

## Investigate
- What each harness supports: SKILL.md / Agent Skills standard, slash commands, hooks, frontmatter (args, argument hints, model)
- Lowest common denominator vs per-harness adapters
- Where config lives in each harness; mapping our layered config (global/project shared/project local/args)
- Shipping deterministic scripts portably (runtime deps: bash/python/node?)
- Install/distribution per harness (plugin, marketplace, copy, installer script)
- Per-harness gaps for ADR 0002 (usage limits) and ADR 0003 (arg hints)
