### greenfield

A brand-new project. `/ns-flow-new-project [idea]`

```
start ─▶ capture ─▶ grill ◆ ─▶ architect ◆ ─▶ design? ◆ ─▶ spec ◆ ─▶ tickets ◆
   ─▶ [TICKET] 01 walking skeleton ─▶ [TICKET] ×N ─▶ [FEATURE-END]
```

- Every planning phase ends with `save ◆` so artifacts are committed as they settle.
- Several interlocking unknowns (the destination itself is unclear): run [wayfinder](wayfinder.md) instead of `grill`.
- **Ticket 01, the walking skeleton:** the thinnest slice that runs end to end and is live in production. It leaves behind CI running types, lint, tests, and build on every PR (`quality-check(setup-ci)` inside the ticket), preview deployments, the E2E suite passing locally, on the preview, and as `@smoke` on production (`../ns-route/references/e2e.md`), the project profile, the project verification skill proven once (`verify:setup`), one findable log line, and the rollback path tried once; with a database or auth in the architecture, it touches each once. Feature tickets start after 01 has shipped.
