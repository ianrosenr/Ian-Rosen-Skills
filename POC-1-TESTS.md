# POC-1 tests

Superseded mostly by automated suite: TESTING.md (`scripts/test.sh`). Keep for manual-only checks (`/` menu hints).

Manual. Fresh Claude Code session per block (skills load at start). Run inside a scratch git repo, e.g. `mkdir /tmp/irs && cd /tmp/irs && git init`. Record fails in Results.
Check first line of each reply = echo line exactly. `G`=`~/.config/irskills/config`, `P`=`.irskills/config`, `L`=`.irskills/config.local`.

## Setup
- Backup + remove existing G if any. No P/L in scratch repo.
- `/` menu shows `explain`, `spec` w/ argument-hint. `_shared` NOT listed as skill.

## Cases
| # | setup | type | expect |
|---|---|---|---|
| 1 | no G/P/L | `/explain what is a mutex` | `[engineer·competent·normal·agent]`, no note |
| 2 | G=`examples/global.config` | `/explain what is a mutex` | `[engineer·proficient·lean·agent]` |
| 3 | G + P=`examples/project.config` + L=`examples/project.config.local` | `/explain what is a mutex` | `[engineer·novice·normal·human]` (role,level<-L; budget,audience<-P) |
| 4 | case 3 + add `level=expert` to P | `/explain what is a mutex` | `[engineer·novice·normal·human] note: ignored shared level` |
| 5a | case 3 | `/explain -r qa -l expert -b bare -a agent what is a mutex` | `[qa·expert·bare·agent]` |
| 5b | case 3 | `/explain pm expert bare what is a mutex` | `[project-manager·expert·bare·human]` |
| 5c | case 3 | `/explain what is a mutex -b verbose` | `[engineer·novice·verbose·human]` (flag at end) |
| 5d | case 3 | `/explain -l guru what is a mutex` | `[engineer·novice·normal·human] note: invalid -l guru` |
| 5e | case 3 | `/explain -- normal distribution` | budget stays `normal` from P; topic = "normal distribution" |
| 5f | case 3 | `/explain normal distribution` | known misparse: `normal` eaten as budget, topic "distribution". Record behavior |
| 5g | G has `colour=red` | `/explain x` | note: `unknown key ...:colour` |
| 6 | no G/P/L | `/explain novice bare TCP handshake` vs `/explain expert verbose TCP handshake` | 1st: dense, terms defined, short. 2nd: long, examples, no basics, gotchas. Visibly diff |
| 7 | no G/P/L | `/explain -r pm how our auth token refresh works` (in a repo w/ code) | impact/risk/timeline framing, no code blocks unless justified |
| 8a | no G/P/L | `/spec add rate limiting to login endpoint` | writes `specs/<slug>.md`; sections Goal/Constraints/Interfaces/Files touched/Acceptance criteria/Out of scope; terse bullets |
| 8b | no G/P/L | `/spec -a human add rate limiting to login endpoint to specs/human.md` | same sections + Context + brief rationale; file at `specs/human.md` |
| 8c | no G/P/L | `/spec -a human -b bare ... to specs/h-bare.md` vs `-b verbose ... to specs/h-verbose.md` | files equivalent density (budget ignored in artifacts); only replies differ |
| 9 | no G/P/L | `/spec -b bare -l novice X to specs/a.md` then `/spec -b verbose -l expert X to specs/b.md` | `diff specs/a.md specs/b.md`: same sections/density (wording drift ok). Replies differ in length |
| 10 | - | `head -5 skills/*/SKILL.md` | only name, description, argument-hint |

## Results
- (date, case #, pass/fail, observed echo/behavior)
