### migration

Data, schema, service, or platform moving to a new shape. This is [architecture](architecture.md)'s code path with mandatory safety steps. `/ns-flow-architecture "<migration>"`

```
discover ─▶ grill ◆ (migration risk) ─▶ architect ◆ (expand/contract plan) ─▶ spec ◆ ─▶ tickets ◆
   ─▶ [TICKET] ×N (one expand, move, or contract step each) ─▶ integration-check (against the migration plan)
```

- Inside each ticket: quality-check's migration-safety stage is mandatory, `rollback:prepare` ◆ is mandatory, `deploy` carries the full release plan with migration ordering, and `observe` runs at High (migration validation).
- Destructive data changes add an explicit authorization ◆ before the destructive step, plus a backup and restore plan.
- `close` confirms the expand/contract cleanup is done or ticketed.
