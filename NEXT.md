# NEXT

Resume point. Agent: read CONTEXT.md first, then work through this top-down. Grill user; record answers in CONTEXT.md; strike resolved items here.

## Status (2026-11-04)
- Planning phase. Grilling paused by user.
- Repo: ianrosenr/Ian-Rosen-Skills (public). Local ~/Projects/Skills. Docs uncommitted.
- ADRs 0001-0006 created, all barren (why + investigate only).

## Outstanding questions
1. Rename `learning` level tier to avoid confusion w/ `teach-me`? Candidates: `novice`, `beginner`, `junior`, `new`.
2. `teach-me` mechanics. User offered to go deeper. Ask:
   - Blocking? Must user answer/pass before model proceeds, or quiz non-blocking alongside work?
   - Exit: how to turn off (flag, `stop`, end of session)?
   - Persist across sessions? Track what user has learned?
   - Interaction w/ level tier: quiz difficulty from level?
3. Style prefs (e.g. analogies): separate setting vs implied by tier. User flagged.
4. Final level tier names/count: currently learning / working / senior / expert / project-manager.
5. Skill list (ADR 0004): dedicated convo. SE principles + roles -> ~10-15 skills.
6. project-manager tier: confirm flag name for opting into code.
7. Settings file format + location per harness (feeds ADR 0005).

## Next steps
1. Finish grilling: questions above.
2. Skill-set convo -> fill ADR 0004.
3. Research ADRs w/ user (user wants to learn, not get answers): 0001 budget/effort, 0006 skills+tools, 0005 harnesses, 0002 usage routing, 0003 arg hints.
4. Write decisions back into ADRs (Status -> Accepted).
5. Design config schema (levels, budgets, audience, per-skill model defaults, layering).
6. Build first skill (likely `spec`) end-to-end as reference impl.
