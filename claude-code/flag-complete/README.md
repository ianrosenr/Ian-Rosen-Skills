# flag-complete (Claude Code only)

Typeahead dropdowns for slash-command flag values. Type `/explain -r` and pick `engineer`, `pm`, `business-manager`, ... from the list. Type `-` to list the flags not used yet.

Generic: reads each command's `argument-hint` frontmatter. Any skill whose hint has groups shaped `[-x a|b|c]` (or `[-x|--long a|b]`) gets dropdowns. No per-skill config.

Install once (user scope = every session after). From a shell:

```
claude plugin install flag-complete --marketplace ianrosenr/Ian-Rosen-Skills -s user
```

Or inside a session: `/plugin install flag-complete --marketplace ianrosenr/Ian-Rosen-Skills`. Repo README's Claude Code block chains this with the skills install.

Optional. Skills work without it. Built on Claude Code's early-access hooks-module API; may break on a Claude Code update.

Dev: `claude plugin test claude-code/flag-complete` (unit tests for hint parsing + completion).
