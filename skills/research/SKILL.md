---
name: research
description: After /grill, research whether the idea already exists (competitors) and which existing services, APIs or libraries could replace building parts of it, then give a pursue verdict. Writes the Research section of plan.md. args: "[chunk N | topic]"
metadata:
  version: "1.0.0"
---

# research

Input: repo-root `plan.md` (Vision, Users, Hosting, Growth, Chunks). No arg = the whole idea. `chunk N` or a topic = only that.

## Steps
1. Competitors: search for products, open-source projects and apps doing the same job for the same users. Per hit: name, link, what it does, price, how this idea differs. 3-8, most similar first. None found -> say so and list what you searched.
2. Use instead of build: per chunk feature or line item, look for services, APIs and libraries (Python first) that already do it. Per hit: name, link, what it replaces (T-ids), cost, lock-in (one-way door?), maturity (last release, adoption). Only ones that fit Hosting and Growth.
3. Verdict: `pursue` | `pursue with changes` | `reconsider`, plus 1-2 lines why (the gap competitors leave, or the reason not to build).

## Rules
- Every claim has a link. No link -> don't claim it. Note the date you searched.
- Use web search and page fetches; prefer recent sources.
- Propose, don't decide. Build-vs-use is settled with the user in /architecture.

## Write
plan.md `## Research`: date, verdict + why, competitors table, use-instead list (each with the T-ids or chunk it affects), `proposed plan changes` (e.g. drop T-4, a service covers it). Don't apply proposed changes yourself.

## Done
Reply in at most 10 bullets: verdict, top 3 competitors and how this differs, top services to use, proposed plan changes. Ask: pursue? Which proposed changes to apply? Apply only the approved ones (edit chunks). Next: `/architecture`.
