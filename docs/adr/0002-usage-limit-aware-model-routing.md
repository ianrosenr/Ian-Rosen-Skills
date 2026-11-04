# ADR 0002: Usage-limit-aware model routing

Status: research pending

## Why
A user nearing their usage limits should get routed automatically to a cheaper model or tier instead of hitting a wall.

## Investigate
- Can a skill or hook read current usage or limits (Claude Code status line data, API headers, other tools)?
- Existing tools that already do this, vs building our own
- Config shape: thresholds, and the fallback order of models and budget tiers
- Should routing switch silently, or notify the user?
