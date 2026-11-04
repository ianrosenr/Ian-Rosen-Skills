# ADR 0003: Argument discoverability

Status: research pending

## Why
Users forget the options (level and budget tiers, flags). They should see their options while they type.

## Investigate
- Claude Code skill frontmatter `argument-hint`: what it shows and its limits
- Autocomplete or completion options in each harness
- Keeping hints in sync with the config schema (generate them from one source?)
- A fallback for harnesses with no hint support, e.g. a `--help` arg handled deterministically
