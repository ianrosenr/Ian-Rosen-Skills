# evals-pending
Cases not runnable yet. Not scanned by `claude plugin eval` (outside evals/).
- e02-global: global layer (`~/.config/irskills/config`). Blocker: model resolves `~` by guessing real home from paths, not eval's temp HOME; no Bash -> can't read $HOME. Real-session behavior fine on single-user machines. Decide: allow `Bash(echo $HOME)`? env-var override? -> ADR 0005.
