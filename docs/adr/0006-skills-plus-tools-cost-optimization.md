# ADR 0006: Skills + tools for cost optimization

Status: research pending

## Why
Hypothesis: pairing skills with built-in/bundled tools (deterministic scripts, CLIs, MCP) moves work out of the model, which cuts tokens and cost a lot without losing quality. Closely tied to ADR 0001.

## Investigate
- Which SDLC tasks are deterministic enough to hand to tools (lint, test runs, codebase outlines, diffs, dependency graphs, git ops, formatting)
- Bundled scripts vs existing CLIs vs MCP servers: tradeoffs in tokens, portability, setup friction
- Tool output shaping: compress/filter output before it reaches context
- How skills tell the model to prefer the tool over reasoning
- Measuring token/cost savings per tool
