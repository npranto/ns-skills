# Kept tests

## Kept tests

Every ticket leaves tests behind in the repo, not just checks that ran once:

- Every thing a user can see or do (each user-facing acceptance criterion) gets an **E2E test**: a journey through the real UI or API, including reload and persistence where they matter.
- Every rule with no screen (a permission, an ownership check, a business rule) gets an **integration test** through the real route and the real database.
- Tests assert behavior through public interfaces, the way a caller uses them (`mattpocock-skills:tdd`). Each new test is seen failing for the intended reason where that is cheap to check.
- Tests are deterministic: no sleeps, no shared state, no real third-party calls, fixed clocks and seeds.

`/ns-to-implement`'s verification plan maps every acceptance criterion to its proof using these types, and implement writes the kept tests:

| Type | Covers |
|---|---|
| Unit | logic at a seam, no I/O |
| Integration | real DB or service boundary, transactions, constraints |
| E2E journey | the demo path through the real UI or API, including reload and persistence |
| API contract | request and response shapes, status codes, error shape, backward compatibility |
| Regression | fails without a specific bug's fix |
| Edge and negative | empty, huge, unicode, boundary values, invalid input, double submit |
| Authorization and ownership | another user's data, missing role, unauthenticated access |
| Concurrency and idempotency | races, retries, lost updates, duplicate webhooks |
| Migration | up and down on realistic data, backward-compatible rollout |
| Accessibility | automated a11y assertions, keyboard path, focus and labels |
| Responsive and visual | key breakpoints, visual snapshots where the repo already uses them |
| Load and performance | a targeted benchmark or budget check for a known hot path |
| Manual exploratory script | numbered steps and expected results for a human, when automation is not worth it |
