### architecture

An architecture decision. Large restructures take the [re-engineering](re-engineering.md) workflows. `/ns-flow-architecture "<question or goal>"`

```
discover ─▶ grill ◆ ─▶ architect ◆ ─▶ ADRs? ◆ ─┬─ decision only ─▶ docs ─▶ save ◆
                                               │
                                               └─ code must change ─▶ spec ◆ ─▶ tickets ◆ ─▶ [TICKET] ×N ─▶ [FEATURE-END]
```

- `discover` uses `mp:codebase-design` for seams and `mp:research` for primary-source facts. `architect` can use `mp:prototype`.
- ADRs go through `mp:domain-modeling`: supersede accepted ADRs, never edit them.
- Tickets are small and always shippable.
