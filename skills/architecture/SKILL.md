---
name: architecture
description: 'Decide only what the next chunk of plan.md (or one large line item) needs to be built, note everything else without asking, refine the line items, write an ADR for every decision, and end the chunk with an architecture page + diagram + video line item. Use after /irs:grill and /irs:research, before /irs:ready. args: "[chunk N | T-n]"'
model: opus
metadata:
  version: "1.4.0"
---

# architecture

Input: repo-root `plan.md`. Scope = `chunk N`, or `T-n` (one line item marked `needs: architecture`), else the first chunk whose `needs` includes architecture.

## Core principle
Build the simplest thing that fits now and can reach `## Growth`'s maximum potential faster than the app could grow there. Every question's options include the simplest one; recommend it unless its path to the maximum is too slow (a data migration or rewrite when growth could come in weeks), and then say so and recommend the next option up. Record each decision's growth path and its trigger in the ADR.

## Defaults
- Python 3.12+, uv, pytest, unless the user picks otherwise.
- Use the `## Research` services the user agreed to, and its earlier findings.

## Brain dump (first message of every session)
- Show the scope's goal, line items and `to figure out` list, then ask only: "Tell me everything you already have in mind for how to build this: tech you want or don't want, constraints, things you've used before, worries. Any order, any length, or 'nothing'." No options, no other question. Stop and wait.
- Write each stated preference to plan.md under the scope as `- user wants: <their words>`. A firm choice ("use Postgres") is still a decision: confirm it in one line, then record D-n + ADR; don't re-ask it as options.
- Everything after shapes around it: the research suggestion targets what the dump left open, options include what they named, questions skip what it answered.

## Research? (right after the brain dump)
Ask: "Research before we start? Suggested: <the tried-and-tested ways to build this scope's goal, covering its `to figure out` list>. Yes / no / research something else: ___".
- Yes or a custom topic -> spawn one subagent (Agent tool): "Read `../research/SKILL.md` from this skill's directory (absolute path) and follow it. Question: <the user's topic or the suggestion>. Called by /irs:architecture: return the findings block only." Paste the findings into plan.md `## Research`; build the options from them, citing the source; link them from the ADRs.
- No -> go straight to the questions.
- Later in the session, more research only when the user says "research it" on a question.

## Loop
- Ask only what blocks this scope's line items. One question at a time: 1-2 lines of context, 2-4 options (simplest included) with a pro and a con each, your recommendation + why.
- Edge cases, later-chunk questions, nice-to-knows: don't ask. Add to Open questions as `E-n` tagged with a chunk.
- Always ask (never defer): security (auth, untrusted input, secrets, PII) and anything that can lose user data.
- One-way doors (data model, public interface, hosting, security model): probe harder; say the reversal cost.
- The user decides. Write each decision to `## Decisions` right away: `- D-n: <decision> | why: <reason> | door: one-way|two-way | chunk: N | adr: <NNNN>`. Keep the options you offered and the user's reasons: the ADR needs them.
- A line item turns out to need its own architecture conversation (new component, new data, new outside service) -> don't hold up the chunk: mark it `(needs: architecture)` and move on.
- Aim for the fewest questions that let the work start. User says "enough" -> stop; remaining questions -> Open questions.

## Check each (ask only what blocks)
- Layout: top-level folders (packages) and what each owns, drawn so a line item touches 1-2 folders. Mostly chunk 1, or when a chunk adds a folder.
- Data: what is stored, where, rough shape.
- Interfaces: CLI, API or UI entry points and their shapes.
- Dependencies: which libraries and services.
- Security: trust boundaries, where secrets live, auth.
- Testing: `test_cmd`, what is faked.
- Running: how it runs and deploys (chunk 1: minimal).
- States: a flow that moves between states (session, payment, sync, retries, jobs, multi-step forms) -> once its decisions are made, follow the repo's `.claude/skills/statechart/SKILL.md` (pstack's, added by /new-repo) with the user as the reader (missing -> tell the user to run `gh skill install backnotprop/pstack skills/statechart --dir .claude/skills` and commit it). Each bug path -> ask: change the design or accept it (D-n). Agreed rules go in the flow's ADR as `R-n: <rule>`; the flow's line items end with `(rules: ADR NNNN R-n)`.

## Write
- Decisions -> plan.md. Set `test_cmd` once decided.
- ADRs: one file per decision made in this conversation, `docs/adr/<NNNN>-<slug>.md` (next free number, 4 digits), from `adr-template.md` in this skill's directory. Options considered = every option you offered, with its pros and cons. Why = the user's reasons, in their words where they gave them; link any research findings used. A decision that replaces an earlier one -> new ADR; set the old one's status to `superseded by NNNN`. Never delete an ADR.
- Line items of this scope: split anything that is more than one change, add missing ones (project skeleton, CI), order by dependency. Format: `- [ ] T-n: <change> (folders: a/, b/)`.
- Last line item: a chunk always ends with `- [ ] T-n: Architecture page, diagram and video for chunk N (folders: docs/architecture/)`. Add it if missing; keep it last. A `T-n` scope instead gets `- [ ] T-m: Architecture page, diagram and video for T-n (folders: docs/architecture/)` right after T-n. Rules for that item: `page/instructions.md` in this skill's directory.
- Layout decided -> repo-root `AGENTS.md` `## Layout` (create if missing): one line per top-level folder: what it owns. Each folder's `README.md` is written by the line item that creates the folder.
- Remove `architecture` from the scope's `needs`.

## Done
Reply: decisions added (id + one line), ADR files written, line item count, open questions added. Next: `/irs:ready chunk N` (it commits plan.md and the ADRs in the plan PR).
