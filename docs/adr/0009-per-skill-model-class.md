# ADR 0009: Per-skill model class guidance

Status: research pending. Not in POC.

## Why
Diff skills need diff model capability. Impl (from good spec) -> low model; planning/spec/context-file writing -> high (must optimize every word for ~100% impl accuracy); explain -> low-mid depending on length + topic difficulty. Saves cost. Must be guidance in instructions, not hard-coded names. Overridable global / project / per prompt.

## Investigate
- Abstract classes (low/mid/high) -> concrete model mapping per harness/provider; where mapping lives
- Mechanism: running model usually can't switch itself mid-session. Options: delegate to subagent w/ chosen model; recommend switch to user; harness-native per-skill model field (Claude Code `model`)
- Which harnesses support subagent model choice
- Dynamic picks (explain: length/difficulty) vs static per skill
- Interaction w/ ADR 0002 usage-limit routing
