# TEST-APPARATUS (handoff, 2026-11-05)

Agent-facing. State of the test harness as built + what's suspect. User: "something is still wrong" -> next session = figure out the proper design. Usage details: TESTING.md. Shipping: SHIPPING.md.

## Goal (user)
- Repeatable, automated tests measuring skill effectiveness per version. Dev-only.
- One command / one instruction ("run the skill tests"), documented as a diagram.
- Specialized judge rubrics, pass/fail checklists, judges blind to skill instructions, judges may propose fixes. Summary per run (no real-time).
- Tests must exercise exactly what user types + ships (`/explain`, not a variant).

## Built
- `scripts/test.sh [all|static|eval|pairs]`. Deps: claude CLI, bash 3.2, jq.
  1. sync: copies `evals/rubrics/<n>.md` body into `graders/rubric-<n>.md`.
  2. static (free): portable frontmatter, name=dir, `metadata.version` semver, CHANGELOG entry, `_shared` not a skill, cases have graders.
  3. eval: `claude plugin eval <repo> --trust-plugin --scaffold --no-publish --ablation none --allow-tools Write ...`. 17 cases `evals/{explain,spec}/<case>/` (prompt.md, case.yaml, fixture.sh, graders/). Graders: regex (echo line, sections, no-code), file_exists, tool_used (trigger), llm (rubrics).
  4. pairs: `evals/pairs/*.pair` (key=value). Each side = `claude -p` in mktemp git dir, `--plugin-dir <repo> --setting-sources project,local`. Deterministic checks (echo line 1, word ratio, header set) + judge `claude -p --json-schema` x JUDGE_VOTES majority -> checklist + `suggested_skill_edit`.
  5. summary: `evals/results/<ts>/SUMMARY.md`, scores.json; baseline `evals/baselines/irskills@<ver>.json` (`--save-baseline`); regression = drop > 0.1.
- Rubrics: economy, level-fit, role-framing, artifact, pair-spread, pair-equivalence.
- Versioning: `metadata.version` per SKILL.md, plugin.json version, CHANGELOG.md, tags `<skill>/vX.Y.Z`.
- Defaults: agent claude-sonnet-5-5, judge claude-opus-5-5, runs 3, threshold 0.8, max cost $10.

## Verified (smoke only, ~$0.5 total)
- static passes. All 17 cases load.
- e01-defaults pass (with `/explain` prompt).
- p01 pair pipeline end-to-end works (judge JSON, votes, suggested edit). Judge caught real factual error (HKDF arg order).
- `--setting-sources project,local` excludes user CLAUDE.md + `~/.claude/skills`.
- NO full run. NO baseline.

## Findings
- Model resolves `~` by guessing real home from paths (read `/Users/ianrosen/.config/irskills/config` inside eval temp HOME). -> global layer untestable; case moved to `evals-pending/`.
- Models attempted Bash (`cat`, `git rev-parse`) to read config despite "no scripts"; denied in tests (Bash not allowed) but allowed in real use -> tested behavior != real behavior.
- Per-skill symlinks in `~/.claude/skills` shadowed plugin skills (`/irskills:explain` missing). Fixed by install change (SHIPPING.md).

## Suspect / likely wrong (fix in next session)
1. Two runners, two isolation models: plugin eval = temp HOME + temp config; pairs = real HOME, user settings off. Inconsistent; pairs still read real `~/.config/irskills/config` if user creates one.
2. Isolation vs "exactly what I use": tests strip user CLAUDE.md/settings/tools; real use has them. Decide what "same" means (skill files identical? environment identical?).
3. Tool grants differ from real use (no Bash in tests). Either allow same tools or forbid Bash in skill rules.
4. Feedback asymmetric: only pair judges return `suggested_skill_edit`; plugin-eval llm graders return votes only.
5. Rubric sync rewrites committed grader files (generated content in git; drift risk).
6. Pairs run once per side -> not statistically repeatable; plugin eval runs 3.
7. Echo regex checks format/values only, not that rules file was actually read (model could fake).
8. Dev-only harness lives inside the plugin root -> ships to users (see SHIPPING.md).
9. Cost per full run unknown.
10. `--case` glob supports only `*`. Known misparse (`normal distribution` w/o `--`) not in suite.
11. Tier 2 Claude-only; no plan yet for Codex/Cursor/Pi/OpenCode runs.

## Questions for next session
- Single runner (all via plugin eval? all via claude -p?) or keep two?
- Isolation policy: what environment do tests reproduce?
- Where harness lives (same repo outside plugin dir? separate repo?).
- Judge feedback format for all llm graders.
- Golden dataset shape: keep per-case dirs or move to one cases file (cf. microsoft/skills scenarios.yaml, skill-creator evals.json)?
