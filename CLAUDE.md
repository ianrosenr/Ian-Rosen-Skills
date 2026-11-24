# Ian-Rosen-Skills

- Skills in `skills/`. Flow + usage: README.md.
- Changing a skill file -> bump its version and `.claude-plugin/plugin.json` version (installed copies only update when it changes), add a CHANGELOG.md line, run `python3 tests/run.py <skill>` (costs tokens), all cases of that skill pass.
- Frontmatter must parse as YAML (quote any description containing `: `). Check (free): `uv run --with pyyaml tests/check_frontmatter.py`.
- Test fixtures are hand-built inputs. Never commit recorded model output, sessions, or baselines.
