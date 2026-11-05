# CHANGELOG

Semver per skill (`metadata.version` in SKILL.md). Plugin version (`.claude-plugin/plugin.json`) bumps whenever any skill or `_shared` changes. Tag releases `<skill>/vX.Y.Z` + `irskills/vX.Y.Z`.
- MAJOR: dial/arg/echo contract change. MINOR: new behavior/rule. PATCH: wording/fix, no contract change.
- Every bump: run `./scripts/test.sh`, save baseline (`--save-baseline`).

## irskills 0.1.0 (2026-11-05)
- POC-1. Shared config rules (`skills/_shared/config-rules.md`).

## explain 0.1.0 (2026-11-05)
- Initial. Role/level/budget dials, echo line.

## spec 0.1.0 (2026-11-05)
- Initial. Audience flag (agent default). Artifact rules: word economy, dials ignored.
