# CHANGELOG

Each skill file has its own semver (`metadata.version` in SKILL.md; `version` in shipit/implementer.md and shipit/reviewer.md). Minor = new rule or behavior. Patch = wording. Every bump: a line here, and `python3 tests/run.py <skill>` passes.

## 2026-11-24: ADRs + architecture page, diagram and video
- architecture 1.1.0: an ADR per decision (`docs/adr/NNNN-slug.md`, template `adr-template.md`: options with pros/cons, decision, why, consequences); every chunk ends with an "Architecture page, diagram and video" line item; large line items can get their own `/architecture T-n` + page item. Page kit in `page/`: instructions (assume the reader knows nothing: every acronym spelled out, one analogy family, step by step) and templates (index.html, D2 diagram, Manim + Kokoro narrated video, build.sh).
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
