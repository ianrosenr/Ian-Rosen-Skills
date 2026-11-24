---
name: research
description: 'Research what it is given, sized to this app: whether an idea already exists (competitors, services to use instead of building), or the industry-standard, tried-and-tested way to do something at this app''s size and growth. Use directly (`/irs:research <question>`), after the first /irs:grill (idea check), at the start of an /irs:architecture session if the user says yes, or when the user says "research it". args: "[question | idea | chunk N]"'
metadata:
  version: "1.1.0"
---

# research

Research exactly what you're given; nothing more. Every finding comes with a source link and is judged against this app's size and growth.

## Input
- The question, from the args or the calling skill. No args + plan.md has no `## Research` yet -> **idea check** for the whole app. `chunk N` -> idea check for that chunk's features.
- Context from repo-root `plan.md`: Users, Hosting, Growth, Decisions (what's already chosen), Non-goals. That's the yardstick: "standard for a single-user homelab app growing to tens of users" is a different answer from "standard at a large company". No plan.md -> ask for size and growth in one question first.

## Kinds of question
**Idea check** ("does this exist?")
1. Competitors: products, open-source projects and apps doing the same job for the same users. Per hit: name, link, what it does, price, how this idea differs. 3-8, most similar first. None -> say so and list what you searched.
2. Use instead of build: services, APIs and libraries (Python first) that already do a feature. Per hit: name, link, what it replaces (T-ids), cost, lock-in (one-way door?), maturity (last release, adoption). Only ones that fit Hosting and Growth.
3. Verdict: `pursue` | `pursue with changes` | `reconsider`, plus 1-2 lines why.

**How is this usually done?** (an approach, pattern, tool, or "what's normal here")
1. Standard approaches: 2-4 tried-and-tested ways, most common first. Per approach: what it is in 1-2 lines, who uses it at what scale, pros, cons, a link to an authoritative source (official docs, well-known engineering write-ups, widely used projects).
2. Fit: for each, does it suit this app's size and growth now? At what scale would you outgrow it, and what's the usual next step?
3. Recommendation: the simplest approach that holds up through `## Growth`, with why and its growth path. Fit to this app's size beats popularity: most write-ups describe large teams; say so when that's why an option is out. Say clearly when the answer is "the boring default is fine".

Several questions at once (e.g. a whole chunk): the same for each, in one findings block, and check the recommendations fit together. Every question gets 2-4 sourced options even when one is clearly standard: name the alternatives with a line on why they lose here. Never present your own design as the only option.

Anything else (a library comparison, a limit, a protocol detail): answer the question directly, with sources, in the same shape: options, fit, recommendation.

## Rules
- Every claim has a link, including options you mention only to dismiss. An option you can't source: leave it out. Note the date.
- Prefer primary sources (official docs, maintainers) and recent ones; say when something is contested or sources disagree.
- Before saying "no source", look where design guidance lives: the framework's own docs (e.g. FastAPI, Django, SQLAlchemy), standards and security guides (OWASP cheat sheets, RFCs), and well-known engineering write-ups. Patterns like a join table for permissions are documented there.
- Propose, don't decide. The user decides in the conversation that asked.
- Stay on the question. No surveys of everything nearby.

## Output
A findings block, at most ~15 lines + sources:
```
### <question> (YYYY-MM-DD)
- context: <size/growth used>
- options: <name>: <one line> | fits now: yes/no | outgrow at: <...> | <link>
- recommendation: <option> because <...>; growth path: <...>
- sources: <links>
```
Several questions: still one block with one `###` heading (the question you were given); each sub-question is a `- <sub-question>:` bullet with its options and recommendation nested under it, then one `- fit together:` line.
Idea check uses: verdict, competitors table, use-instead list, `proposed plan changes`.

## Where it goes
- Called by another skill (/irs:grill, /irs:architecture): return the findings block only; don't edit files. The caller uses it in its options and records it.
- Run directly: append the findings block to plan.md `## Research` (create the section if missing). Idea check: also ask "pursue? which proposed changes to apply?" and apply only the approved ones. Next: whatever plan.md says the chunk still needs.
