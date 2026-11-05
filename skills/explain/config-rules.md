<!-- GENERATED from skills/_shared/config-rules.md by scripts/sync-shared.sh; do not edit -->
# irskills config rules

Version: shared rules versioned with plugin (`.claude-plugin/plugin.json`). Change here -> bump plugin + every skill using it.

Shared by all irskills skills. Follow exactly. Resolve dials yourself by reading files; no scripts.

## Dials + vocab
| dial | flag | values | default |
|---|---|---|---|
| role | `-r` `--role` | engineer, project-manager (alias `pm`), business-manager, designer, qa, executive | engineer |
| level | `-l` `--level` | novice, competent, proficient, expert | competent |
| budget | `-b` `--budget` | bare, lean, normal, verbose | normal |
| audience | `-a` `--audience` | agent, human | agent |

- Match case-insensitive. Normalize `pm` -> `project-manager`. Value sets are disjoint, so a bare word maps to at most one dial.

## Config files
Read each with your file tool. Missing file = skip silently, no mention.
1. global: `~/.config/irskills/config`
2. project shared (committed): `<root>/.irskills/config`
3. project personal (gitignored): `<root>/.irskills/config.local`

- `<root>` = git repo root of cwd; if not in a git repo, cwd.
- Format: one `key=value` per line. Trim whitespace around key + value. Ignore blank lines + lines starting `#`. Inline `# ...` after a value = comment. No nesting, no quotes.
- Keys: `role`, `level`, `budget`, `audience` only.
- Unknown key -> ignore, note `unknown key <file>:<key>`.
- Invalid value -> ignore that entry (lower layer/default applies), note `invalid <file>:<key>=<value>`.
- Duplicate key in one file -> last line wins.
- Project shared file setting `role` or `level` -> ignore it (role/level are personal; belong in config.local or global), note `ignored shared <key>`.

## Args
Args = text the user passed after the skill name.
1. Flags anywhere: `-r X`, `--role X`, `--role=X` (same for l/b/a). Remove flag + value from input.
2. Free words: from the start of remaining input, consume each token that exactly matches a known value of any dial; stop at first non-matching token. Never consume mid-input.
3. `--` stops free-word consumption; everything after is task input verbatim. (Use when topic starts with a vocab word, e.g. `-- normal distribution`.)
4. Remainder = task input.
- Flag beats free word for same dial. Same dial twice -> last wins, note `dup <dial>`.
- Invalid flag value (e.g. `-l guru`) -> ignore it, use value resolved from layers below, note `invalid -l guru`. Unknown flag -> leave in task input, note `unknown flag <x>`.

## Precedence (per key, independently)
args > project personal > project shared > global > defaults.

## Echo line
First line of the skill's response, always, every budget incl bare:
`[role·level·budget·audience]` -> e.g. `[engineer·competent·normal·agent]`
- Separator = `·` (U+00B7). Values only, fixed order, normalized names.
- Notes (unknown/invalid/ignored/dup) -> append on same line: `[engineer·competent·normal·agent] note: ignored shared level; invalid -l guru`. Each note once per invocation. No notes -> nothing appended.
- Nothing else on that line.

## Tier rules
Apply to conversational output (your replies to the human). Never to artifacts (see Artifacts).

Role (frame output for this reader; level is then read through role):
- engineer: technical framing, code ok.
- project-manager: non-technical. Impact, risk, timelines, dependencies. No code unless critical.
- business-manager: cost, value, risk, business outcome. No code unless critical.
- designer: user experience, flows, constraints on UI. No code unless critical.
- qa: behavior, edge cases, test strategy, failure modes. Code/tests ok when useful.
- executive: decision, impact, risk, cost; shortest framing. No code unless critical.
- "critical" = reader can't make the decision/understand the point without it. Agent judges; no flag.

Level (act at this level for this role):
- novice: define terms, analogies ok, explain why. Check in at decision points + after file changes (what + why), don't halt work.
- competent: assume basics, explain non-obvious.
- proficient: skip basics, focus tradeoffs.
- expert: minimal explanation, edge cases/gotchas only.

Budget (output verbosity, not effort; never cut work/reading to save words). Universal across skills, but ONLY for conversational replies (answers to user). Never applies to written artifacts (specs, context files, docs). Resolved default applies regardless of skill; per-call override only. Skills must not set own budget default:
- bare: zero fluff, densest format, every char justified.
- lean: short bullets, no preamble/recap.
- normal: concise prose + bullets.
- verbose: full explanation, examples.

Artifacts (spec files, context files, any written-up doc): budget/role/level never apply. Always: max word economy, grammar sacrificable, zero fluff. Goal: implementer executes ~100% correctly. Include examples + edge cases when they raise accuracy, written tersely. Economize words, not information.

Audience (artifacts only):
- agent: full relevant detail, machine-optimized.
- human: same content + slightly more connective prose for readability. Still word-economical.
