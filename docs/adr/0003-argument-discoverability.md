# ADR 0003: Argument discoverability

Status: Claude Code decided (2026-11-05); other harnesses research pending

## Why
Users forget the options (level and budget tiers, flags). They should see their options while they type.

## Investigate
- Claude Code skill frontmatter `argument-hint`: what it shows and its limits
- Autocomplete or completion options in each harness
- Keeping hints in sync with the config schema (generate them from one source?)
- A fallback for harnesses with no hint support, e.g. a `--help` arg handled deterministically

## Parked: real per-flag dropdowns (2026-11-05)
User wants: typing `-r` shows a dropdown of roles (same for every flag). Not in POC-1. Interim: values inlined into the `argument-hint` ghost text.

Investigate:
- Which harnesses (CC, Codex, Cursor, Pi, OpenCode) expose per-arg completion for skills/commands, natively or through an extension/plugin API
- Work per harness: build effort, language/runtime, whether it needs a plugin (which brings the `irskills:` prefix back?)
- Upkeep: keeping completions in sync with `config-rules.md` vocab (generate from one source?), harness API churn
- Whether adding it breaks bare `/name` or the `npx skills add` install path

## Decision: Claude Code (user, 2026-11-05)
- CC mod API (early access, CC 2.1.318) has `prompt.autocomplete` hook (rows for token at cursor) + `command.describe` (each command's `argumentHint`).
- Built `claude-code/flag-complete/`: hooks-only plugin. Source of truth = `argument-hint` (no extra vocab file). Groups `[-x a|b|c]` / `[-x|--long a|b]` -> enum flags. Generic: all skills, all flags.
- Behavior: token `-r` -> value rows (take -> `-r engineer `); `-` / `--ro` -> unused flags w/ values; `-l pro` -> filtered values; `--role=e` -> `--role=engineer`. Flag match case-insensitive. Topic words: nothing.
- Distribution: optional one-time `/plugin install flag-complete --marketplace ianrosenr/Ian-Rosen-Skills`. No skills in plugin -> bare `/explain` kept. Skills work without it. Distribution spec D2 exception recorded.
- Known: plugin rows draw below engine rows, unhighlighted; long flags only if hint lists them (current hints short-only); API may break on CC update; not yet verified in live session.
- Rejected: skill auto-installing plugin (installs code without consent).
