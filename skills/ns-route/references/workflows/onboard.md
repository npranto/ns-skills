### onboard

Get oriented in an existing codebase, then hand off. `/ns-flow-existing-project [goal]`

```
discover ─▶ doc gaps? ─▶ profile? ─▶ verify:setup? ─▶ save ◆ ─▶ quality-check(setup-ci)? ─▶ route
                                                                                          │
     feature · bug · architecture · docs · ticket ◀───────────────────────────────────────┤
     anything else ─▶ /ns-route ◀─────────────────────────────────────────────────────────┘
```

- Doc gaps: `mp:domain-modeling` for `CONTEXT.md` and ADR candidates (grounded in code), issue-tracker docs, and a short `CLAUDE.md` per `mp:writing-for-agents`.
- `profile`: the project profile, `docs/agents/workflow.md` (`../ns-route/references/profile.md`).
- `verify:setup`: the project verification skill and its feature map, proven once.
- `quality-check(setup-ci)`: CI runs the core four on PRs; a project with UI also gets the E2E workflow (`../ns-route/references/e2e.md`).
