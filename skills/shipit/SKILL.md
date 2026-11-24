---
name: shipit
description: "`/shipit` approves and builds IMPLEMENTME.md: issue, implementer, reviewer, at most 2 review rounds, PR, report. `/shipit <PR#>` addresses the user's review comments on that PR with the same loop. Never merges. args: \"[PR#]\""
metadata:
  version: "1.0.0"
---

# shipit

You orchestrate. Implementer and reviewer are fresh subagents (Agent tool, general-purpose). Prompt each: "Read `<this skill's dir>/implementer.md` (or `reviewer.md`) and follow it exactly. Inputs: <paths, mode, round>." Pass file paths, never pasted content. Never merge. Never push to main.

Run dir: `R = $(git rev-parse --git-dir)/shipit/T-<n>` (inside .git, never committed). Save every subagent's JSON there (`impl-1.json`, `review-1.json`, ...) plus `report.md`. /retro reads it.

## Build mode (`/shipit`)
1. Preconditions: on a `t-*` branch; repo-root IMPLEMENTME.md exists; its Questions section says none (else stop: answer them first); `gh auth status` ok.
2. Issue:
   - `issue:` line is none -> `gh issue create --title "T-<n>: <title>" --body-file IMPLEMENTME.md`; write the number into the `issue:` line.
   - `issue: #I` already set (re-run after /retro) -> copy IMPLEMENTME.md to R, `git reset --hard main`, restore the copy, `gh issue edit I --body-file IMPLEMENTME.md`.
3. Record `base = git rev-parse HEAD`. Implementer, mode `build`.
4. Reviewer, round 1 (base, IMPLEMENTME.md).
5. Findings -> implementer, mode `fix` (findings file) -> reviewer, round 2 (prior findings + implementer result). Andon from either -> skip to 7.
6. Stop after round 2 whatever it says. Never a third round.
7. Clean (round 1 or 2 clean):
   - `git rm IMPLEMENTME.md`; check `- [x] T-<n>` in plan.md; it was the chunk's last unchecked item -> also set that chunk's `status: done`. Commit `T-<n>: done`.
   - Push; `gh pr create --title "T-<n>: <title>"`, body: `Closes #I`, what changed, tests, the review summary (below).
8. Not clean (round 2 findings or an andon): no PR, no push. Branch and IMPLEMENTME.md stay.

## Comment mode (`/shipit <PR#>`)
1. `gh pr checkout <PR#>`; `git pull`. Issue I = the `Closes #I` in the PR body. `gh issue view I --json body` -> `R/issue.md` (the original IMPLEMENTME).
2. Unresolved review threads (`gh api graphql`, pullRequest.reviewThreads where isResolved false: thread id, path, line, comment bodies) + the latest review's summary body -> `R/comments-<k>.json` (k = 1, 2, ... per comment-mode run).
3. `base = HEAD`. Implementer, mode `comments` (issue.md + comments file).
4. Reviewer round 1 and 2 as in build steps 4-6, plus it checks every comment was addressed.
5. Clean -> push; reply on each thread with the implementer's reply + commit sha (`addPullRequestReviewThreadReply`). Never resolve threads; the user does.
6. Not clean -> no push, no replies.

## Report (always; also write `R/report.md`)
Bullets, terse:
- Built: what changed (files), tests added.
- Review 1: each finding (id, one line) and how it was fixed. Clean -> "clean".
- Review 2: clean, or each outstanding finding (id, one line). Not run -> say so.
- Disputes and andons (question + options).
- Comment mode: per comment: changed | answered | disputed, one line.
- Gaps worth a test case: each review-1 finding's `miss_reason`, and in comment mode any comment the reviewer should have caught.
- Not clean: "Outstanding after review 2" list, then suggested skill edits (file, section, one-line change) drawn from the miss_reasons, then "Next: `/retro T-<n>`".
- PR link, or "no PR".
- Clean, build mode: "Next: review PR #n on GitHub. Comments -> `/shipit <n>`. Merged -> `/implementme`."
