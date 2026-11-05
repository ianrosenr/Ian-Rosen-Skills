# Skills
Claude skills

## Install
Pick your harness. `-g` = all projects (drop it for current project only).

**Claude Code** (skills + flag-value dropdowns: `/explain -r` -> engineer, pm, ...):
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a claude-code -g -y \
  && claude plugin install flag-complete --marketplace ianrosenr/Ian-Rosen-Skills -s user
```
Skills only: drop the second line. Dropdowns details: `claude-code/flag-complete/README.md`.

**Codex**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a codex -g -y
```

**Cursor**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a cursor -g -y
```

**OpenCode**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a opencode -g -y
```

**Pi**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a pi -g -y
```

**Gemini CLI**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a gemini-cli -g -y
```

**GitHub Copilot**
```
npx skills@latest add ianrosenr/Ian-Rosen-Skills -a github-copilot -g -y
```

Other harnesses: omit `-a` and pick from the list. Non-Claude harnesses get flag hints only where the harness shows them; no dropdowns yet.
