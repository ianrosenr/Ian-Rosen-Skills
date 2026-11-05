---
name: spec
description: Write a spec for a feature or change to a markdown file, optimized for an agent (default) or a human reader. Use when the user asks for a spec, design doc, or implementation brief before building.
argument-hint: "[-a agent|human] [-b bare|lean|normal|verbose] <feature>"
metadata:
  version: "0.1.1"
---

# spec

1. Read `config-rules.md` in this skill's directory. Follow it exactly.
2. Read the config files it lists, parse args, resolve role/level/budget/audience.
3. First line of reply = echo line per rules.
4. Gather context with targeted reads (relevant files, interfaces). Don't implement.
5. Write spec file:
   - Path: path named in task input (e.g. `to docs/x.md`) else `<root>/specs/<slug>.md`; slug = kebab-case of feature, ≤5 words. Create dir if needed. File exists -> ask before overwrite.
   - Sections, in order: Goal, Constraints, Interfaces, Files touched, Acceptance criteria, Out of scope.
   - Follow Artifacts rules in config-rules. Examples/edge cases when they raise impl accuracy, terse. Acceptance criteria testable.
   - audience=agent: terse bullets, no prose, full relevant detail.
   - audience=human: same sections + `Context` section first (2-4 sentences why) + 1-line rationale where a choice is non-obvious. Not much more prose.
   - Role/level/budget never affect artifact. Same inputs + audience -> same spec.
   - Unknowns -> `Open questions` section at end; don't invent requirements.
6. Reply after echo line follows level/budget (e.g. bare: path + 1 line; verbose: path + section summary + open questions).
