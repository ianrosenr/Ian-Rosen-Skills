# 0001: Python standard library only

- date: 2026-11-20
- status: accepted
- chunk: 1
- plan.md: D-1

## Context
Tiny personal tool.

## Options considered
### Stdlib only
- pros: nothing to install
- cons: no fancy CLI helpers
### click
- pros: nicer CLI
- cons: a dependency

## Decision
Standard library only.

## Why
"It's tiny, I don't want to install anything."

## Consequences
- door: two-way: adding click later is easy
