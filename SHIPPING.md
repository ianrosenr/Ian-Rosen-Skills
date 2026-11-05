# SHIPPING (handoff, 2026-11-05)

Agent-facing. How skills currently install/ship + open problems. User: "something is still wrong" -> next session = figure out proper way. Tests: TEST-APPARATUS.md.

## Requirements (user)
- User types `/explain` (no namespace prefix).
- What dev uses == exactly what ships.
- Multi-harness: Claude Code, Codex, Cursor, Pi, OpenCode (ADR 0005).
- Zero/minimal deps. Individual devs + teams.

## Current state
- Repo root = Claude Code plugin: `.claude-plugin/plugin.json` (name irskills, version 0.1.0); skills auto-discovered in `skills/`.
- Skills: `skills/explain/`, `skills/spec/` (Agent Skills std SKILL.md + `argument-hint` + `metadata.version`). Shared rules `skills/_shared/config-rules.md`, referenced by relative path `../_shared/config-rules.md`.
- Dev install (this machine): symlink `~/.claude/skills/irskills -> ~/Projects/Skills`. Loads as `irskills@skills-dir`. Verified: normal session lists `irskills:explain`, `irskills:spec`; `/explain` resolves to it; edits live.
- Removed: earlier per-skill symlinks (`~/.claude/skills/{explain,spec,_shared}`) -> they shadowed plugin skills.
- User config: `~/.config/irskills/config`, `<repo>/.irskills/config`, `<repo>/.irskills/config.local` (gitignored). Examples in `examples/`.
- No marketplace.json. No install instructions for end users. No other-harness install.

## Problems / unknowns
1. Whole repo ships as plugin: docs, ADRs, evals, scripts, examples all inside plugin root. Should plugin be a subdir (e.g. `plugin/`) or separate repo, with dev harness outside?
2. `/explain` works only while unambiguous. Generic names (`explain`, `spec`) likely collide with other users' skills/plugins -> falls back to `/irskills:explain` or wrong skill. Names/namespace strategy undecided.
3. `_shared` relative path: skills not standalone. Agent Skills installers (e.g. `npx skills add`) copy single skill folders -> `../_shared` breaks. Options: inline rules per skill (drift), build step copies shared file into each skill (dep), single meta skill, etc.
4. Distribution channel undecided: Claude marketplace (`.claude-plugin/marketplace.json`, `claude plugin marketplace add ianrosenr/Ian-Rosen-Skills`), skills-dir symlink/clone, `npx skills add`, per-harness copy. Marketplace installs copy to cache (not live) -> dev vs user path differs.
5. Other harnesses: discovery dirs differ (Pi: `~/.pi/agent/skills`, `~/.agents/skills`, `.agents/skills`; Cursor scans `.claude/skills`; Codex `.codex/skills`/`~/.agents`?). Plugin wrapper is Claude-only. Unverified: arg passthrough, slash invocation, OpenCode native support.
6. `argument-hint` is Claude-only; may fail strict validation elsewhere (blocks claude.ai/API skill upload).
7. `~` resolution by model (guesses home) -> global config may be missed on unusual setups.
8. Updates/versioning for users: how they get new versions; plugin version vs per-skill versions.
9. Config folder name `irskills` provisional; plugin name `irskills` provisional.

## Questions for next session
- Repo layout: plugin subdir vs root vs separate repos?
- One canonical install per harness that dev also uses?
- Shared rules: how to share without relative paths/deps?
- Naming to guarantee `/explain` (or accept prefix)?
- Primary channel for v0.1: marketplace? clone+symlink? `npx skills`?
