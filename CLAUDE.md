# Ian-Rosen-Skills

- Skills in `skills/`. Flow + usage: README.md.
- Changing a skill file -> bump its version, add a CHANGELOG.md line, run `python3 tests/run.py <skill>` (costs tokens), all cases of that skill pass.
- Test fixtures are hand-built inputs. Never commit recorded model output, sessions, or baselines.
