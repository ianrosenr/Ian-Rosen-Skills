---
name: retro
description: 'After a /irs:shipit run that is not clean after review 2 (or a PR comment that shows a skill gap), talk through what went wrong, then fix the skills in the Ian-Rosen-Skills repo, add test cases with the user''s expected outputs, bump versions, run the tests until they pass, and open a PR there. args: "[T-n]"'
metadata:
  version: "1.0.1"
---

# retro

Input: the run dir `$(git rev-parse --git-dir)/shipit/T-<n>/` in the app repo (default: newest), its `report.md` and JSON files, plus this chat.
Skills repo: `~/Projects/Skills` (github.com/ianrosenr/Ian-Rosen-Skills). Not there -> ask for the path.

## Steps
1. Diagnose with the user, one gap at a time. For each outstanding finding, miss_reason and flagged comment, find the step that let it through: plan (line item too big or vague), research, architecture (missing decision), implementme (missing file, decision or test), implementer (ignored its instructions), reviewer (missed it in round 1). Blame the process, never the run. Propose a root cause; the user confirms or corrects.
2. Expected output: per confirmed gap, ask what the skill should have produced (e.g. "reviewer round 1 flags the missing name check at notes.py:12"). Write down the user's words.
3. Skill edit: the smallest change that stops this class of miss. Show the diff; apply only what the user approves.
4. Test case per gap: `tests/cases/<skill>/<slug>/` in the Skills repo (format: Skills repo README, Tests). Build the fixture by hand from this run's files, trimmed to the minimum. No secrets, no recorded model output, no saved session. `expected.md` = the user's words from step 2.
5. Bump the version of each edited skill file (minor: new rule; patch: wording) and add a CHANGELOG.md line.
6. In the Skills repo run `python3 tests/run.py <skill>`: the new cases must pass, and every existing case of the edited skills must still pass. A failure -> revise the skill (show the user), rerun. Stop after 3 tries and report.
7. Branch `retro-t<n>-<slug>`, commit, push, `gh pr create` (body: gaps, skill edits, new cases, test results). Never merge.

## Done
Reply: PR link, gaps -> edits -> cases, test results. Next, in the app repo after the retro PR merges: implementme was the gap -> `/irs:implementme T-<n>` (rewrites the file; review it), then `/irs:shipit`. Otherwise `/irs:shipit` (re-runs the same IMPLEMENTME.md from a clean branch).
