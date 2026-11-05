# ADR 0007: teach-me memory + adaptive difficulty

Status: research pending

## Why
- `teach-me` should remember across sessions what user learned (no re-quizzing known material) without bloating context/memory.
- Quiz difficulty shouldn't be fixed by level tier: a senior can be new to a tech. Want difficulty that adapts to the user's answers.

## Investigate
- Storage: per-user learned-concepts file? format, location (global vs project), harness portability
- Context cost: load only relevant concepts (topic-keyed lookup, deterministic script) vs whole file
- Granularity: concept/topic/tech; how mastery recorded (seen / passed / shaky)
- Adaptive difficulty: seed (level tier? per-tech calibration Q? prior memory?) + step rule after each answer
- Decay/refresh: re-quiz old/shaky items?
- Privacy for shared/team repos: learning data must stay personal (gitignored/global)
