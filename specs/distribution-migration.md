# Spec: skill delivery, invocation, update warnings

Status: draft, not implemented. P1-P4 folded + grilled 2026-11-05; remaining = impl-time verifications (Open q 1, 3, 4, 7). Reference: github.com/mattpocock/skills @ v1.3.2 (README, `.agents/invocation.md`, `.agents/install-block.md`, `scripts/link-skills.sh`; read 2026-11-05) + vercel-labs/skills (`npx skills`). Supersedes SHIPPING.md problems 1-6, 8; TEST-APPARATUS suspect 8.

## Decisions (user, 2026-11-05)
- D1: Delivery + consumption mimic mattpocock/skills' **non-plugin route** (`npx skills`) + his user-invoked convention + his dev link script. Not copied: his folder layout, skills, process.
- D2: Bare names in every harness: user types `/explain`, `/spec`. Never `/irskills:explain`. -> No plugin/marketplace channel (Claude Code namespaces plugin skills `<plugin>:<skill>`; Matt's plugin routes inherit that). Repo layout may change freely to achieve this.
  - Exception (user, 2026-11-05): `flag-complete` = hooks-only Claude Code plugin (no skills -> no prefix), optional, for flag-value dropdowns (ADR 0003). Repo root `.claude-plugin/marketplace.json` lists only it. Plugin updates manual (`claude plugin update`), matching D4.
- D3: Skills user-invoked only (typed). Never model-chosen; no per-session description cost.
- D4: No auto-update by default. New release -> warn ONCE per skill per release (with update cmd), then silent until next release (user may prefer staying on a version). Network check ≤ 1/day, via deterministic script; Claude Code runs it via preprocessing (no model tool call) (revised 2026-11-05). User can disable via config/flag (globally or per skill). Opt-in pref `auto_update=on` = skill runs update cmd itself.

## Scope boundary
| Area | Source |
|---|---|
| Install: `npx skills add` for all harnesses; manual update via `npx skills update` | Matt (his "any other agent" route), applied to every harness |
| User-invoked markers (`disable-model-invocation` + Codex `agents/openai.yaml` policy), human-facing descriptions | Matt |
| Self-contained skill folders (no `../`), same-folder bare-filename links | Matt |
| Dev local install `scripts/link-skills.sh` (symlinks per skill) | Matt |
| Plugin/marketplace channels for skills (Claude Code, Codex, Copilot) | **dropped** (prefix + auto-update violate D2, D4) |
| CC hooks-only plugin `flag-complete` (dropdowns), via repo marketplace | ours (D2 exception) |
| Folder layout, skill set/content, dials, config | ours |
| Shared rules distribution (generated per-skill copy) | ours |
| Update-warning mechanism | ours (Matt has none) |
| Test design (cases, graders, rubrics, judges, thresholds, SUMMARY, baselines) | ours, per TESTING.md; only skill loading changes |
| Versioning/CHANGELOG/release | ours (TESTING.md#versioning) |

## Diagnosis (current state wrong)
1. Repo = Claude plugin; dev = skills-dir symlink -> skills load as `irskills:explain` (prefix); no user install path; Claude-only.
2. `../_shared/config-rules.md` breaks per-folder installers (`npx skills` copies single skill folders).
3. Skills model-invocable; e08 tests auto-trigger (opposite of D3).
4. No update signal; version tied to `plugin.json`.
5. Tests load via plugin (`claude plugin eval`, `--plugin-dir`) -> namespace + load path differ from users.

## Constraints
- Every harness: skills land as standalone folders in the harness skills dir (`npx skills` agent table, e.g. claude-code `.claude/skills/<name>` | `~/.claude/skills/<name>`; codex/cursor/opencode/pi/gemini-cli/github-copilot project `.agents/skills/<name>`, global per agent). Standalone folder => bare `/<name>`.
- One SKILL.md per skill, identical for all harnesses. Harness-specific keys only if ignored elsewhere.
- No `../` under `skills/`. No plugin manifest that ships skills (prevents users installing a prefixed variant). Allowed: `claude-code/flag-complete/.claude-plugin/plugin.json` + root `.claude-plugin/marketplace.json` listing only flag-complete.
- User-invoked markers both present + in sync: frontmatter `disable-model-invocation: true` (Claude Code, Cursor, Pi); `agents/openai.yaml` `policy.allow_implicit_invocation: false` (Codex). Others: none exists (see markers table).
- Update check never fails the skill: reply always proceeds. Errors/timeouts silent; only blocked gets BLOCK line.
- Echo line stays line 1 (contract unchanged). Warning = line 2.
- Kept: `argument-hint`, `metadata.version`. Added: `allowed-tools`. Writes: only update-check.sh, only its state file.

## Interfaces

### Layout after migration
```
skills/explain/SKILL.md
skills/explain/config-rules.md        # GENERATED
skills/explain/update-check.sh        # GENERATED
skills/explain/agents/openai.yaml
skills/spec/...                       # same 4 files
shared/config-rules.md                # source of truth (moved from skills/_shared/)
shared/update-check.sh                # source of truth
versions.json                         # NEW: latest released version per skill (fetched by update check)
scripts/link-skills.sh                # NEW (Matt's, adapted)
scripts/sync-shared.sh                # NEW
scripts/release.sh                    # NEW: writes versions.json
scripts/test.sh                       # edit
.claude-plugin/marketplace.json       # lists flag-complete only
claude-code/flag-complete/            # CC hooks-only plugin (ADR 0003)
```
- Deleted: `.claude-plugin/plugin.json` (marketplace.json stays), `skills/_shared/`.

### SKILL.md (explain shown; spec same pattern)
```markdown
---
name: explain
description: Explain a topic, concept, code, or file, tuned to your role, level, and budget.
argument-hint: "[-r role] [-l level] [-b budget] <topic>"
disable-model-invocation: true
allowed-tools: <CC-ALLOW>
metadata:
  version: "0.2.0"
---

# explain

Installed version: 0.2.0   <!-- GENERATED from metadata.version by sync-shared.sh -->

Update check output (Claude Code fills this; other harnesses: see config-rules.md Update check):
!`sh "${CLAUDE_SKILL_DIR}/update-check.sh"`

1. Read [config-rules.md](config-rules.md). Follow it exactly (incl. Update check).
...
```
- Body version line needed: some harnesses strip frontmatter before model sees it.
- `` !`…` `` = Claude Code preprocessing: runs before model sees skill, output inlined, no model tool call. Other harnesses show it literally -> config-rules tells model to run script itself. Verify at impl: `!` supported in skills (not only commands), `${CLAUDE_SKILL_DIR}` var exists, permission needed + exact `<CC-ALLOW>` value (e.g. `Bash(sh:*)` too broad; prefer exact cmd; std is space-delimited -> may need comma/YAML list form; check portability validators).
- No `$ARGUMENTS` passed to script (shell injection risk from user text). Flag handled by model (see below).
- spec description: `Write a spec for a feature or change to a markdown file, for an agent (default) or human reader.`

### `agents/openai.yaml`
```yaml
interface:
  display_name: "Explain"
  short_description: "Explain tuned to role, level, budget"
policy:
  allow_implicit_invocation: false
```

### `versions.json` (repo root, `main` branch)
```json
{"explain": "0.2.0", "spec": "0.2.0"}
```
- Written only by `scripts/release.sh` (reads each `metadata.version`). Edits on `main` between releases must not touch it -> unreleased bumps never trigger warnings.
- URL: `https://raw.githubusercontent.com/ianrosenr/Ian-Rosen-Skills/main/versions.json`.

### Config additions (shared/config-rules.md; MINOR bump)
New keys. Allowed in all 3 layers (personal prefs; NOT subject to "ignored shared" rule). Values `on` | `off`. Resolved by update-check.sh (deterministic), not model; model still ignores them silently when resolving dials (no `unknown key` note).
| key | default | meaning |
|---|---|---|
| `update_check` | on | all skills |
| `update_check.<skill>` | unset | this skill only; `<skill>` = `[a-z0-9-]+`, any name accepted |
| `auto_update` | off | when newer version found, run `<AU>` |
| `auto_update.<skill>` | unset | this skill only |
- Effective `update_check` for skill S (specificity first, then layer):
  1. `update_check.S` set in any layer -> value from highest layer setting it (local > shared > global).
  2. `update_check` set in any layer -> highest layer.
  3. default on.
- Effective `auto_update`: same w/ `auto_update.S` / `auto_update`, default off. Only consulted if update_check on.
- Invalid value (not on/off) -> treat as unset; script prints nothing about it.
- Ex: global `update_check.explain=off` + local `update_check=on` -> explain off. Global `update_check=off` + local `update_check.explain=on` -> explain on, spec off.
- Flag `--no-update-check` (model-handled; no value; not a free word; removed from task input): suppress line 2 this call. Non-CC: model also skips running script. CC: preprocessing already ran -> model just drops line 2; if script had just recorded a warning, that release's warning is consumed (accepted: user asked for silence).
- Echo line unchanged.

### Update check: `shared/update-check.sh` (POSIX sh; deterministic; user decision 2026-11-05)
Goal: network ≤ 1/day; each new release warned once per skill; then silent until next release.
- Invocation: `sh <skill-dir>/update-check.sh` (no args). Reads own dir `SKILL.md`: `name:` -> S, `Installed version:` -> I.
- Paths: config global `${XDG_CONFIG_HOME:-$HOME/.config}/irskills/config`; root = `git rev-parse --show-toplevel` else `$PWD`; `<root>/.irskills/config`, `<root>/.irskills/config.local`. State `${XDG_CONFIG_HOME:-$HOME/.config}/irskills/update-state`.
- State format (key=value, same parser as config): `last_check=<unix epoch>`, `latest.<skill>=<ver>` (from last successful fetch, all skills), `warned.<skill>=<ver>`.
- Algorithm:
  1. Effective update_check(S) off -> exit 0, no output, no network, no write.
  2. `now - last_check < 86400` -> L = `latest.S` from state (no network). Else: `curl -fsS --max-time 3 <URL>`; always write `last_check=now` (even on failure -> offline costs ≤1 attempt/day); on success parse JSON (flat string map; sed/grep, no jq) -> rewrite all `latest.*`.
  3. L missing/unparseable, or L ≤ I (semver numeric) -> exit 0 silent.
  4. `warned.S` ≥ L -> silent (already told about this release; user stays on I). Else:
     - auto_update off -> print WARN; write `warned.S=L`.
     - auto_update on -> run `<AU>` (timeout 120s). exit 0 -> print UPD; else print AUFAIL. Write `warned.S=L` either way.
  5. Sandbox: curl failed AND `CODEX_SANDBOX_NETWORK_DISABLED=1` (verify var name at impl) -> print BLOCK instead of nothing (once per failed daily attempt; if state unwritable in sandbox -> every call until allowed).
  - State write: atomic (tmp + mv), mkdir -p. Write failure -> ignore. Any error anywhere -> exit 0, no stderr leak (`2>/dev/null`). Total runtime w/o network < 50ms.
- Output = at most one line; model copies it verbatim as reply line 2 (every budget incl bare). No output -> no line 2.
- Line 2 strings (exact). `<S>` skill, `<I>` installed, `<L>` latest, `<R>` = `https://github.com/ianrosenr/Ian-Rosen-Skills#permissions`, `<U>` = manual scoped update cmd (= `<AU>` minus `-y`):
| case | line |
|---|---|
| WARN | `⚠ irskills: <S> <L> available (installed <I>). Update: <U> · Disable: update_check.<S>=off` |
| UPD | `✓ irskills: <S> updated <I> -> <L> (active next call)` |
| AUFAIL | `⚠ irskills: <S> <L> available (installed <I>); auto-update failed. Update: <U> · Disable: auto_update.<S>=off` |
| BLOCK | `⚠ irskills: update check blocked. Allow: <R> · Disable: update_check=off` |
- `<AU>` MUST touch only S from this repo, never other skills/authors (user hard req). DECIDED 2026-11-05 (verified vs vercel-labs/skills v1.7.6 source):
  - Scope X: script's own dir (resolve symlinks, `cd -P`) under `<root>` -> `-p`, run from `<root>`; else `-g`.
  - `<AU>` = `npx -y skills@latest update S X -y` (project: `cd <root> &&` first). `<U>` = `npx skills@latest update S X`.
  - Why scope flag mandatory: `update <name>` w/o `-g`/`-p` updates BOTH scopes; lock keyed by name, not source -> foreign same-name skill in other scope gets updated. Within one scope name unique + this script lives in it -> S there = ours.
  - CLI facts: positional args = exact skill names only (`update owner/repo` = no-op "No installed skills found matching"); named update reinstalls only that skill folder from its locked source (subpath); `-y` never deletes upstream-removed skills. Project-scope whole-repo reinstall bug (vercel-labs/skills#982) fixed v1.5.2 -> always `skills@latest`.
  - Bare `npx skills update` (no name) forbidden.
- Examples: I 0.2.0, L 0.10.0 -> WARN (numeric). I 0.3.0 (dev link), L 0.2.0 -> silent. I 0.2.0, warned 0.3.0, L 0.3.0 -> silent. Then 0.4.0 released -> WARN once.

### Update check rule (shared/config-rules.md section; model side)
- Claude Code: script output already inlined under "Update check output". Copy it as line 2 (unless `--no-update-check`). Do not run script again.
- Other harnesses (literal `` !`…` `` visible, no output): unless `--no-update-check`, run `sh <this skill's dir>/update-check.sh` once via shell before main work; copy output as line 2.
- Shell call denied by harness/user -> print BLOCK as line 2. No shell tool / `sh` missing (e.g. Windows w/o Git Bash) -> nothing.
- Never fetch versions.json yourself, never run `<AU>` yourself, never edit state.

### Permissions
- SKILL.md `allowed-tools: <CC-ALLOW>` = narrowest rule letting CC run the preprocessing cmd (resolved at impl). No `Bash(curl:*)`, no `Bash(npx:*)`. curl + `<AU>` run inside script (child processes), so only the script cmd needs approval.
- Other harnesses ignore/misread it; accepted.

### README "Permissions" section (anchor `#permissions`)
- Why: skills run `update-check.sh` each call (network ≤1/day; auto_update runs npx). Without allow rule harness may prompt or block (-> BLOCK line).
- Claude Code: pre-approved by skill (`allowed-tools`). Managed-only policy (`allowManagedPermissionRulesOnly`) -> ignored; ask admin or `update_check=off`.
- Codex: `~/.codex/rules/default.rules` `prefix_rule(pattern = ["sh", "<abs skills dir>/explain/update-check.sh"], decision = "allow")` per skill (runs outside sandbox -> network + state write). Alt: `[sandbox_workspace_write] network_access = true` + writable `~/.config/irskills` (broader). Rules experimental.
- Copilot, Cursor, Pi, OpenCode, Gemini/Antigravity: approve the prompt, add allow rule for `sh <skill dir>/update-check.sh`, or `update_check=off`.
- Windows: needs Git Bash/WSL `sh`; else no update checks (silent).
- Disable all: `update_check=off` in `~/.config/irskills/config`. One skill: `update_check.<skill>=off`. One call: `--no-update-check`.
- State file location + safe to delete (resets: next call fetches; current release re-warned once).

### User-invoked markers per harness
| harness | marker | explicit invoke |
|---|---|---|
| Claude Code | `disable-model-invocation: true` | `/explain` |
| Codex | `agents/openai.yaml` `policy.allow_implicit_invocation: false` | `$explain` |
| Cursor | `disable-model-invocation` | `/explain` |
| Pi | `disable-model-invocation` | `/skill:explain` native; impl investigates alias -> `/explain` (Open q 1) |
| OpenCode, Copilot, Gemini/Antigravity | none -> model-visible; README notes it (OpenCode: `permission.skill` can deny auto-use) | harness default |
- `disable-model-invocation` hard-fails claude.ai/Skills API upload; not a target channel -> accepted, README notes.

### `scripts/sync-shared.sh [--check]`
- For each `skills/*/`: write `config-rules.md` = `<!-- GENERATED from shared/config-rules.md by scripts/sync-shared.sh; do not edit -->` + source; `update-check.sh` = `# GENERATED from shared/update-check.sh; do not edit` (after shebang) + source; rewrite `Installed version:` line from `metadata.version`.
- `--check`: no writes; exit 1 + list stale.

### `scripts/release.sh`
- Runs sync-shared.sh, writes `versions.json` from all `metadata.version`, prints tag cmds (`<skill>/vX.Y.Z`). Existing release steps (CHANGELOG, `--save-baseline`) unchanged.
- Repo-level version (formerly plugin.json): `VERSION` file at root; baselines `evals/baselines/irskills@<VERSION>.json`.

### README "Install" (Matt's npx wording, all harnesses)
- `npx skills@latest add ianrosenr/Ian-Rosen-Skills -a <agent>` — e.g. `claude-code`, `codex`, `cursor`, `opencode`, `pi`, `gemini-cli`, `github-copilot`; omit `-a` to choose. `-g` = all projects.
- One skill: `--skill=<name>`. Update (manual, never automatic): `npx skills@latest update explain spec -g` (or `-p` from project root, matching install; list every irskills skill). Never bare `npx skills update` (updates all authors' skills). `update ianrosenr/Ian-Rosen-Skills` does NOT work (names only). Re-run `add` for new skills.
- Caveat (with bare-names warning): `update <name>` w/o `-g`/`-p` also updates a same-name skill from another author in the other scope.
- Usage: type `/explain ...`, `/spec ...`. Skills never run unless typed.
- Install section = one block per harness (user, 2026-11-05). Claude Code block chains skills + plugin: `npx skills@latest add ianrosenr/Ian-Rosen-Skills -a claude-code -g -y && claude plugin install flag-complete --marketplace ianrosenr/Ian-Rosen-Skills -s user`. Other harnesses: `npx` line only w/ own `-a`. Verified 2026-11-05 (local source, fake CLAUDE_CONFIG_DIR): adds marketplace + installs, no prompt.
- Update warnings: once per new release per skill (checks ≤1/day); disable `update_check=off` (all) / `update_check.<skill>=off` in `~/.config/irskills/config`, or `--no-update-check` per call. Opt-in `auto_update=on`. Link to #permissions.
- Harness note: OpenCode/Copilot/Gemini have no user-only marker -> model may auto-invoke.
- No-Node fallback: copy `skills/<name>/` into your agent's skills dir.

### Dev local install (Matt's)
- `rm ~/.claude/skills/irskills` first.
- `scripts/link-skills.sh`: Matt's script adapted: for each `skills/*/SKILL.md` dir, `ln -sfn <dir> <dest>/<basename>` into `~/.claude/skills` + `~/.agents/skills`; bail if a dest dir is a symlink into repo; replace non-symlink targets. No bucket exclusions. Header: dev-only. Live edits; bare names.

### Tests (TESTING.md design unchanged; loading + new cases only)
- Skill loading (all tiers): per workspace, `npx skills@latest add "$REPO" -a claude-code -y --copy` (project scope -> `ws/.claude/skills/<name>`) = user path, bare names. Install once per run into template dir, `cp -R` per workspace.
- Agent run: `claude -p "<prompt>"` in ws w/ existing flags minus `--plugin-dir`; keep `--setting-sources project,local` (excludes dev links in `~/.claude/skills`; Open q 3 confirms project skills still load).
- Eval tier: `claude plugin eval` requires a plugin -> replace with in-script runner over same case dirs + graders (regex, file_exists, tool_used, llm via existing `judge()`), N runs, THRESHOLD. Case/grader/rubric files unchanged except below. `case.yaml` deleted.
- Fixtures add `update_check=off` to `.irskills/config.local` for all existing cases (no network, line 2 clean).
- Runner: per-case optional `extra_flags` file (appended to `claude -p`), `env` file. New graders: `tool_not_used`, regex `negate: true`, `line: N`.
- Line-2 regexes: WARN `^⚠ irskills: explain \d+\.\d+\.\d+ available \(installed 0\.0\.1\)\. Update: .+ · Disable: update_check\.explain=off$`; UPD `^✓ irskills: explain updated 0\.0\.1 -> \d+\.\d+\.\d+ \(active next call\)$`; AUFAIL `^⚠ irskills: explain .* auto-update failed\. .*Disable: auto_update\.explain=off$`; BLOCK `^⚠ irskills: update check blocked\. Allow: https://github\.com/ianrosenr/Ian-Rosen-Skills#permissions · Disable: update_check=off$`; NONE = no line matching `^[⚠✓] irskills:`.
- **Script unit tier** (new `unit`, free, in `static` + `all`): `scripts/test-update-check.sh`. Each test: temp `HOME`/`XDG_CONFIG_HOME`, temp git repo cwd, copy of a skill dir w/ `Installed version: 0.0.1`, PATH shims: `curl` (serves fixture JSON or exit 7; appends to `curl.log`), `npx` (appends args to `npx.log`; exit per test), `date` not shimmed -> write `last_check` directly. Asserts stdout + logs + state.
  | id | setup | expect |
  |---|---|---|
  | u01 | latest 0.3.0 | WARN; state `warned.explain=0.3.0`, `last_check` set; curl.log 1 |
  | u02 | u01 then run again | silent; curl.log still 1 (cached <1d) |
  | u03 | u01, then `last_check` = now-90000, latest 0.3.0 | silent; curl.log 2 |
  | u04 | u03 but fixture latest 0.4.0 | WARN w/ 0.4.0 |
  | u05 | latest 0.10.0, installed 0.9.0 | WARN (numeric) |
  | u06 | installed 0.3.0, latest 0.2.0 | silent |
  | u07 | curl exit 7 | silent; `last_check` written; 2nd run no curl |
  | u08 | curl exit 7 + `CODEX_SANDBOX_NETWORK_DISABLED=1` | BLOCK |
  | u09 | global `update_check=off` | silent; curl.log absent; no state file |
  | u10 | local `update_check.explain=off` | silent |
  | u11 | local `update_check.spec=off` | WARN |
  | u12 | global `update_check=off` + local `update_check.explain=on` | WARN |
  | u13 | global `update_check.explain=off` + local `update_check=on` | silent |
  | u14 | shared-layer `update_check=off` | silent (allowed in shared) |
  | u15 | `update_check=maybe` | WARN (treated unset) |
  | u16 | `auto_update=on`, npx exit 0, skill dir outside root | UPD; npx.log == `update explain -g -y` args (after `-y skills@latest`), not bare `update` |
| u23 | u16 but skill dir inside `<root>` (`.claude/skills/explain`) | UPD; npx.log has `-p`; npx cwd == `<root>` |
| u24 | latest 0.3.0, skill dir inside `<root>` | WARN `Update:` = `npx skills@latest update explain -p` |
  | u17 | `auto_update=on`, npx exit 1 | AUFAIL; `warned.explain` set |
  | u18 | `auto_update=on` + `update_check=off` | silent; npx.log absent |
  | u19 | malformed JSON | silent |
  | u20 | state dir unwritable | WARN printed; exit 0; no stderr |
  | u21 | key `explain` missing in JSON | silent |
  | u22 | runtime cached path | < 50ms |
- Agent cases (Claude Code; fixture `evals/fixtures/update-base.sh`: installed `0.0.1`, removes `update_check=off`, temp `XDG_CONFIG_HOME` in ws, curl shim via `env` PATH serving latest 0.3.0 -> no real network):
  | case | delta | pass |
  |---|---|---|
  | e10-update-warn | default | line 2 WARN; no WebFetch/Bash tool call in transcript (preprocessing did it) |
  | e11-update-once | e10 twice same ws (2 sessions) | run 2 NONE |
  | e12-update-flag | prompt `/explain --no-update-check -b bare -- what is a mutex` | NONE; no `unknown flag` note |
  | e13-update-off | local `update_check=off` | NONE |
  | e14-auto-update | local `auto_update=on`, npx shim exit 0 | line 2 UPD |
  | e15-no-unknown-key-note | local `update_check.explain=on` | echo line has no `unknown key` note |
  - Model-path (non-CC) BLOCK / script-run behavior: covered when Codex test harness exists (ADR 0005); until then manual AC.
- Install tier (new; in `all`): npx add `-a claude-code -a codex --copy` into temp dir -> each skill has SKILL.md, config-rules.md, update-check.sh, agents/openai.yaml; no `../`; folder names = bare skill names.
- Static tier: remove `_shared`, plugin.json checks; add `sync-shared.sh --check`; no `.claude-plugin/`; every skill has `agents/openai.yaml` + both markers + `allowed-tools: <CC-ALLOW>` exactly + `` !`sh "${CLAUDE_SKILL_DIR}/update-check.sh"` `` line; `sh -n` + shellcheck (if installed) on shared/update-check.sh; `versions.json` valid JSON, keys == skill dirs, each value ≤ that skill's `metadata.version`; no `../`; frontmatter allowlist += `disable-model-invocation`, `allowed-tools`; shared/update-check.sh contains all 4 line-2 templates + exact curl + `<AU>`; no `npx skills update` w/o scope arg anywhere in skills/ shared/; README has `## Permissions` + Codex prefix_rule; CHANGELOG keyed on `VERSION`.

### CLAUDE.md additions
- New/renamed skill: run `scripts/sync-shared.sh`, `scripts/link-skills.sh`; add to README + `versions.json` at release.
- Skills user-invoked: both markers. No `../`. No plugin manifests.

## Files touched
- Delete: `.claude-plugin/`, `skills/_shared/`, `evals/*/*/case.yaml`.
- New: `VERSION` (0.2.0), `versions.json`, `shared/config-rules.md` (moved + Update check section + keys + `--no-update-check`), `shared/update-check.sh`, `skills/*/update-check.sh`, `scripts/test-update-check.sh`, `skills/*/config-rules.md`, `skills/*/agents/openai.yaml`, `scripts/{link-skills.sh,sync-shared.sh,release.sh}`, `evals/explain/{e09..e15}-*/`, `evals/fixtures/update-base.sh`.
- Edit: `skills/{explain,spec}/SKILL.md` (frontmatter, version line, step 1; 0.2.0); `scripts/test.sh` (loading, eval runner, install tier, static, new graders); all `evals/**/fixture.sh` + `evals/fixtures/*.sh` (`update_check=off`); `evals/explain/e08-trigger` -> `e08-no-auto-invoke`; `examples/*` (document `update_check`); `CHANGELOG.md`; `README.md`; `CLAUDE.md`; `TESTING.md`; `CONTEXT.md`; `SHIPPING.md`; `TEST-APPARATUS.md`; `NEXT.md`; `docs/adr/0005-multi-harness-support.md`.
- Machine: `rm ~/.claude/skills/irskills`; run `scripts/link-skills.sh`.

## Acceptance criteria
- Repo has no `.claude-plugin/`; `grep -r '_shared\|plugin-dir\|plugin eval' skills scripts evals` -> none.
- `scripts/test.sh static` passes; fails on stale generated file, missing marker/openai.yaml, `../`, versions.json ahead of skill.
- Fresh project: `npx skills add <repo> -a claude-code` -> new Claude session lists `explain`, `spec` (no `irskills:`); `/explain -b bare -- what is a mutex` -> line 1 echo, no line 2 warning when installed == latest.
- Same for `-a codex` (Codex invokes by bare name).
- Unit tier u01-u24 pass (incl. once-per-release, ≤1 fetch/day, precedence, auto_update scoping).
- e10-e15 pass ≥ THRESHOLD; e08 no auto-invoke ≥ THRESHOLD; e01, e09 pass.
- Claude Code: update check adds zero model tool calls (transcript) + no permission prompt (fresh install, default perms, interactive).
- User stays on old version: after first WARN, no further line 2 and no network for ≥24h; next release -> exactly one WARN.
- Offline -> reply identical to `update_check=off`; ≤1 curl attempt/day.
- `<AU>` affects only S (install 2 foreign skills + explain; auto-update -> foreign SKILL.md byte-identical). Incl clash: foreign `explain` in project scope + ours global -> auto-update ours -> foreign byte-identical.
- Codex: README prefix_rule verified w/ `codex execpolicy check`; real Codex run: warning shows once, BLOCK when sandboxed w/o rule.
- After link-skills.sh: `~/.claude/skills/{explain,spec}`, `~/.agents/skills/{explain,spec}` = symlinks into repo; bare `/explain` works.

## Out of scope
- Plugin/marketplace channels, official listings.
- Matt's buckets, skills, docs pages, changesets.
- Configurable check interval (fixed 1 day). Per-version pinning/ignore lists beyond warned-once.
- Test runner items TEST-APPARATUS suspects 1-7, 9-11 beyond what loading change forces.
- Non-update dial/config behavior.

## Open questions
1. Pi: DECIDED investigate alias (Pi prompt template / extension mapping `/explain` -> skill). Found -> ship it + test; none -> fallback undecided, ask user.
2. ~~Codex network~~ resolved: off by default in workspace-write; `prefix_rule` allow / `network_access=true` (README Permissions). Verify w/ real run at impl.
3. Impl verify (not user decision): `--setting-sources project,local` still loads `ws/.claude/skills/`? Else isolate w/ temp HOME.
4. Name clash: DECIDED keep bare names (user: source repo in `add` cmd identifies the skill). Caveat: install target = `<skills-dir>/<name>/` regardless of source -> 2 same-name skills can't coexist. Impl verifies npx behavior (overwrite/prompt/fail); README warns; revisit if overwrite silent.
5. ~~Cost vs cache~~ REVISED 2026-11-05: ≤1 fetch/day + warn once per release; state file; script; CC preprocessing.
6. ~~Node~~ DECIDED: README prereq Node ≥ 22.20 + manual copy fallback; no Node -> auto_update fails -> AUFAIL line.
7. ~~auto_update scoping~~ DECIDED 2026-11-05: `<AU>` = named update + mandatory scope flag (see Update check). Impl verify w/ real run: foreign same-name skill in other scope byte-identical.
8. ~~Hint frequency~~ DECIDED every call while blocked; under new design = per failed daily attempt (every call only if state unwritable).
9. Impl verify: CC `!` preprocessing in skills, `${CLAUDE_SKILL_DIR}`, `<CC-ALLOW>` form; Codex `CODEX_SANDBOX_NETWORK_DISABLED`; non-CC harnesses show `` !`…` `` literally (harmless?).
10. Distribution channel DECIDED 2026-11-05: stay on `npx skills`. Upstream ask: `update` accept source like `remove owner/repo` does (draft issue; user posts). Fallback if upstream never fixes + clash matters: git clone + `link-skills.sh`-style symlinks per harness; update = `git pull` (source-scoped by construction, no Node; costs: per-harness path table, Windows symlinks, verify each harness follows symlinked skills, 2-step install).
   - Considered + deferred 2026-11-05: own CLI via pip (pipx/uvx). Gains: own install manifest -> fully source-scoped update; no Node; room for own cmds (`irskills config set ...`). Costs: PEP 668 blocks plain `pip install` (needs pipx/uv = new prereq); no post-install hook -> 2-step install; own per-harness path table; one pack version vs per-skill versions; PyPI release overhead; off the familiar `npx skills` route. Revisit only if own CLI wanted (config mgmt, teach-me memory, routing); then real choice = owning path table, not language.
