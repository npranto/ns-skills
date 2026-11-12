# Stages

| # | Stage | What it does |
|---|---|---|
| 1 | Types | type-check |
| 2 | Lint | linter in check mode |
| 3 | Format | formatter in check mode |
| 4 | Unit tests | fast tests, scoped to changed code first, then full |
| 5 | Integration tests | tests against a real DB or service boundary |
| 6 | E2E tests | run the whole browser or API journey suite against the local build, after checking by name that every variable it needs is in the local env file (`../ns-route/references/e2e.md` "Local env"). A test skipped for a missing variable is a failure, not a pass. A user-facing criterion with no kept E2E test (`../ns-route/references/topic-kept-tests.md` "Kept tests") is a failure, fixed through `/ns-to-implement` |
| 7 | Build | production build succeeds, no new warnings |
| 8 | Dependencies and secrets | vulnerability and license audit, secret scan on the diff |
| 9 | Migration safety | migrations are reversible or expand/contract, no destructive change without a plan |
| 10 | Accessibility | automated a11y audit plus a keyboard and focus spot check for UI changes |
| 11 | Performance | bundle size, unnecessary client JS, slow queries, N+1, missing indexes where justified |
| 12 | Docs | run `/ns-to-docs` against the diff |
| 13 | Review follow-through | confirm `/ns-to-review` findings marked to-fix were actually fixed |
| 14 | Verify follow-through | the `/ns-to-verify local` result is for the current commit, and nothing changed since that would invalidate it. Otherwise re-run `/ns-to-verify local` |
| 15 | Hygiene | read-only scan of the diff: no stray debug output, TODOs, commented-out code, dead code (unused exports, unreachable branches, orphaned files), or unrelated files; no secrets or PII; no edits to `CHANGELOG.md` or auto-generated files; migrations and env changes noted for the PR description |
