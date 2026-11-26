# <NNNN>: <decision as a short title, e.g. "Store notes as files, not in a database">

- date: <YYYY-MM-DD>
- status: accepted          <!-- accepted | superseded by NNNN -->
- chunk: <N>                <!-- or line item T-n -->
- plan.md: D-<n>

## Context
<2-4 lines: what needed deciding and why it came up now. The constraints that mattered (Growth, Hosting, security, cost).>

## Options considered
### <Option A>
- pros: <...>
- cons: <...>

### <Option B>
- pros: <...>
- cons: <...>

## Decision
<the option chosen, concretely: what we will do>

## Why
<the reasons, in the user's words where they gave them>

## Consequences
- <what this commits us to; what gets easier; what gets harder>
- door: <one-way | two-way>: <what reversing it would cost>
- growth path: <what changes, and roughly when, if Growth needs more than this>

<!-- Only when /irs:architecture modeled this flow with statechart: -->
## Rules
- R-1: <rule in the user's words> | invariant: <TLA+ name>

## Statechart
- chart: <NNNN>-statechart/chart.mmd
- re-run: <command, new --out folder>
- fixed bug paths: <R-n: 1. step 2. step ...>
- model leaves out: <...>
- chart hides: <steps>
