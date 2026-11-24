# CHANGELOG

Each skill file has its own semver (`metadata.version` in SKILL.md; `version` in shipit/implementer.md and shipit/reviewer.md). Minor = new rule or behavior. Patch = wording. Every bump: a line here, and `python3 tests/run.py <skill>` passes.

## 2026-11-24: plan-driven flow, all skills 1.0.0
- Replaced everything with one flow: grill, research, architecture, ready, implementme, shipit (+ implementer, reviewer), retro.
- Removed: explain, spec, the config dials, the multi-agent shipit workflow, ship docs, the old eval harness, the flag-complete plugin.
- New test runner `tests/run.py` (live runs, no cached inputs). Seed case: `shipit/reviewer-missing-name-check`.
