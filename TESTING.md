# TESTING

Dev-only. Measures skill effectiveness per version. Not part of shipped skills.

## Run
- One command: `scripts/test.sh` (all tiers). Free only: `scripts/test.sh static`.
- Or tell the agent: **"run the skill tests"** -> it runs `scripts/test.sh` and reports SUMMARY.md.
- Options: `eval|pairs|static`, `--runs N` (default 3), `--case GLOB` (only `*`), `--save-baseline`, `--max-cost USD` (default 10).
- Env: `AGENT_MODEL` (default claude-sonnet-5-5), `JUDGE_MODEL` (claude-opus-5-5), `JUDGE_VOTES` (3), `THRESHOLD` (0.8), `CONCURRENCY` (2).
- Deps: claude CLI, bash, jq. Costs tokens (tiers 2-3) on your login; cap via `--max-cost`.

## Flow
```mermaid
flowchart TD
  A[scripts/test.sh] --> B[0. sync rubrics<br/>evals/rubrics/*.md -> graders/rubric-*.md]
  B --> C[1. static — free, deterministic<br/>frontmatter portable · name=dir · metadata.version semver<br/>CHANGELOG entry per version · _shared not a skill · every case has graders]
  C --> D{mode}
  D -->|all / eval| E[2. claude plugin eval<br/>per case: fixture.sh seeds temp repo + .irskills config<br/>agent runs /skill ... N times]
  E --> E1[regex graders: echo line, sections, no-code]
  E --> E2[file graders: spec written]
  E --> E3[llm judges, 2-of-3 votes<br/>economy · level-fit · role-framing · artifact]
  D -->|all / pairs| F[3. pairs — claude -p, A vs B runs]
  F --> F1[deterministic: word ratio, header sets]
  F --> F2[judge x JUDGE_VOTES, majority<br/>pair-spread · pair-equivalence<br/>returns checklist + suggested_skill_edit]
  E1 & E2 & E3 & F1 & F2 --> G[4. summarize<br/>SUMMARY.md: versions, git sha, models, scores, cost, suggested edits]
  G --> H{baseline exists?}
  H -->|yes| I[regression = score drop > 0.1 -> FAIL]
  H -->|--save-baseline| J[evals/baselines/irskills@ver.json]
```

## Tiers
| tier | what | cost | repeatable |
|---|---|---|---|
| 1 static | lint skills, versions, changelog, case files | free | 100% |
| 2 eval | single-run cases via `claude plugin eval` | tokens | N runs, pass rate ≥ THRESHOLD |
| 3 pairs | cross-run comparisons (plugin eval can't compare runs) | tokens | deterministic checks + majority judge |

## Judges (specialized rubrics, `evals/rubrics/`)
- One rubric per quality dimension -> narrow, consistent judges.
- Pass/fail checklists, quoted evidence for each FAIL.
- Judges see output + dials (echo line) + rubric only. Never the skill instructions (rubric says exactly what to check).
- Pair judges also return `suggested_skill_edit` -> feedback for the next version.
| rubric | used for |
|---|---|
| economy | budget fit, filler detection (replies) |
| level-fit | depth vs level (replies) |
| role-framing | framing/code vs role (replies) |
| artifact | spec quality: sections, testable criteria, no invention, word economy |
| pair-spread | A vs B differ as dials imply |
| pair-equivalence | artifacts identical in substance across dials |

## Layout
```
evals/
  <skill>/<case>/prompt.md       # prompt + frontmatter (tags, tools)
  <skill>/<case>/case.yaml       # scaffold_script: fixture.sh
  <skill>/<case>/fixture.sh      # seeds temp workspace (git repo, .irskills/config*)
  <skill>/<case>/graders/*.md    # regex | file_exists | tool_used | llm (rubric-<name>.md synced)
  rubrics/*.md                   # single source for judges
  pairs/*.pair                   # key=value: a, b, compare, fixture, checks, rubric
  fixtures/*.sh                  # shared fixtures for pairs
  baselines/irskills@<ver>.json  # committed score baselines
  results/<ts>/                  # gitignored: SUMMARY.md, eval.json, pairs.json, report.html
evals-pending/                   # blocked cases (not scanned), see README
```

## Versioning
- Semver per skill: `metadata.version` in SKILL.md. Plugin version: `.claude-plugin/plugin.json` (bumps on any skill/_shared change).
- CHANGELOG.md entry required per version (static tier enforces).
- MAJOR: dial/arg/echo contract change. MINOR: new behavior/rule. PATCH: wording/fix.
- Release: bump -> `scripts/test.sh --save-baseline` -> commit baseline -> tag `<skill>/vX.Y.Z` + `irskills/vX.Y.Z`.

## Add a case
1. `mkdir -p evals/<skill>/<case>/graders`; copy a sibling case.
2. Echo regex first; add rubric graders as `graders/rubric-<name>.md` (frontmatter only; body synced).
3. Quote `description` if it contains `:`.
4. `scripts/test.sh eval --case '<case>' --runs 1` to smoke.

## Known limits
- Global config layer untestable in plugin eval (model guesses `~`; see evals-pending/README.md).
- Pairs/judges run w/ `--setting-sources project,local`: user CLAUDE.md + ~/.claude/skills excluded (no bias, no name clash).
- Tier 2 = Claude Code only. Tiers 1+3 portable later (e.g. `codex exec`).
- Evals invoke `/explain`, `/spec` = exactly what user types (resolves to plugin skill when unambiguous).
- Topic starting w/ vocab word (`normal distribution`) misparsed w/o `--`: not in suite (expected-fail).
