# CHANGELOG

Each skill file has its own semver (`metadata.version` in SKILL.md; `version` in shipit/implementer.md and shipit/reviewer.md). Minor = new rule or behavior. Patch = wording. Every bump: a line here, and `python3 tests/run.py <skill>` passes.

## 2026-11-24: plugin irs 1.0.2, research answers any question
- research 1.1.0: researches what it's given. Idea check (does this exist, what to use instead of building, verdict) or "how is this usually done": 2-4 tried-and-tested approaches judged against plan.md's size and Growth, with a recommendation, growth path and sources. Returns a findings block when called by another skill; appends to plan.md `## Research` when run directly.
- grill 1.1.0, architecture 1.2.0: before recommending on a question with an industry-standard answer, run research in a subagent and build the options from its findings (cited; ADRs link them). The user can say "research it" anytime.
- New case: `research/standard-background-jobs-small-app`.

## 2026-11-24: plugin irs 1.0.1, branch hygiene
- implementme 1.2.1: before each item, `git fetch --prune` and delete local branches whose remote was deleted by a merge (never ones without an upstream).
- shipit 1.0.2: PR body note that `Closes #I` closes the issue and the merge deletes the branch (repo auto-delete; new-repo sets it, ADR 0056).

## 2026-11-24: plugin irs 1.0.0
- The repo is a Claude Code plugin (`irs`, marketplace `irskills`). Commands are now `/irs:<skill>`; every skill's text uses the prefixed names. Patch bumps: grill 1.0.2, research 1.0.1, shipit 1.0.1, implementer 1.1.1, reviewer 1.1.1, retro 1.0.1.
- Removed `scripts/link-skills.sh` (symlinks would duplicate the plugin's commands); use `claude --plugin-dir` for live edits.

## 2026-11-24: ADRs + architecture page, diagram and video
- architecture 1.1.0: an ADR per decision (`docs/adr/NNNN-slug.md`, template `adr-template.md`: options with pros/cons, decision, why, consequences); every chunk ends with an "Architecture page, diagram and video" line item; large line items can get their own `/architecture T-n` + page item. Page kit in `page/`: instructions (assume the reader knows nothing: every acronym spelled out, one analogy family, step by step) and templates (index.html, D2 diagram, Manim + Kokoro narrated video, build.sh).
- Audience: a junior software engineer (was: no coding knowledge). Every numbered step states how the hop works: transport, auth, payload, sync/async, failure, why. Diagram arrows carry the protocol.
- Page adapts to any screen (width and text scale, diagram and video fit the window, click to zoom). Video template has `link()` (edge-to-edge arrows) and `fit()` (scale to frame) because Manim has no layout engine; rule: render a still frame and inspect it before the full build.
- ready 1.1.0: checks the page item is last and every decision has an ADR; commits `docs/adr/` in the plan PR.
- implementme 1.2.0: page items read the page instructions, copy its Done when, copy templates the first time.
- grill 1.0.1: plan template shows the page item and ADR note.
- New case: `ready/missing-page-and-adr`.

## 2026-11-24: lazy senior dev rules
- implementme 1.1.0: rewritten around the smallest complete change: approach ladder (skip, reuse, stdlib, installed dep, one-liner, minimal code), find every caller first, fix root cause once in shared code, no unneeded abstractions, named shortcuts. Template gains `## Approach`. Reply ends with what was skipped + risks.
- implementer 1.1.0: `shortcut:` comments for Approach shortcuts; moved code keeps error handling and validation.
- reviewer 1.1.0: over-building (unneeded abstraction, option, duplicate code) is a finding; checks shortcut comments.
- New cases: `implementme/root-fix-and-callers`, `shipit/reviewer-unneeded-wrapper`.

## 2026-11-24: plan-driven flow, all skills 1.0.0
- Replaced everything with one flow: grill, research, architecture, ready, implementme, shipit (+ implementer, reviewer), retro.
- Removed: explain, spec, the config dials, the multi-agent shipit workflow, ship docs, the old eval harness, the flag-complete plugin.
- New test runner `tests/run.py` (live runs, no cached inputs). Seed case: `shipit/reviewer-missing-name-check`.
