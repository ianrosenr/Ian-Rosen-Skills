# ADR 0001: Budget vs work effort

Status: research pending

## Why
Budget mode should cut cost without hurting the quality of the work. Hypothesis: savings can come from deterministic context management plus less verbose replies, instead of doing less work.

## Investigate
- Deterministic context-reduction techniques (AST outlines, symbol lookup, diff-only/targeted reads, caching), and how much each saves
- Output-token savings vs context-token savings: which matters more for cost?
- How to measure the quality drop-off between budget tiers
- Per-skill model defaults: which skills tolerate cheaper models?
