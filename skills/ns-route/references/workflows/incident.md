### incident

Production broken, degraded, or exposed right now. Risk is forced to critical. `/ns-flow-bugfix "<incident>"` (the flow asks whether it is live in production and switches to incident mode).

```
mitigate first ◆ ─▶ branch (hotfix/, from the release ref) ─▶ mp:diagnosing-bugs (reproduce first) ─▶ root cause + fix plan ◆
   ─▶ scope-check (smallest fix, no refactor) ─▶ implement (test-first, regression test kept) ─▶ verify:local ◆ ─▶ understand
   ─▶ review ◆ ─▶ quality-check ◆ (fast stages) ─▶ save ◆ ─▶ pr ◆ (expedited)
   ─▶ rollback:prepare ◆ ─▶ deploy ◆ (hotfix path) ─▶ verify:production ─▶ observe (High)
   ─▶ stakeholder-brief:release (Shipped) ─▶ postmortem ◆ (then the lessons card) ─▶ close
```

- `mitigate first`: a rollback or a flag off is offered before any fix is designed (`ns-to-observe` "Not healthy: mitigate first"). Explanations stay short until production is healthy.
- Everything after `pr` is mandatory.
- `postmortem` is an internal engineering/leadership record (timeline, root cause, action items), different from the stakeholder comments. It ends with a lessons card in chat: each decision made under pressure and its principle.
- UNHEALTHY at `observe` goes to `rollback:execute` ◆. A partial or failed rollback is a new incident.
