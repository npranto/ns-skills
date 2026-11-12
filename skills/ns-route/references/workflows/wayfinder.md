### wayfinder

A destination with too many interlocking unknowns for one session (replatform, provider swap, multi-tenancy, new subsystem). `/ns-flow-wayfinder "<destination>"`

```
capture? ─▶ wayfinder ◆ ⟲ (one decision ticket per loop, save ◆ each session) ─▶ ADRs? ◆
   ─▶ architect? ◆ ─▶ design? ◆ ─▶ spec ◆ ─▶ tickets ◆ ─▶ [TICKET] ×N (or delegate) ─▶ [FEATURE-END]
```

- The `wayfinder` loop resolves decision, research (`mp:research`), prototype (`mp:prototype`), and grill tickets until the map is clear.
- Its self-check bails out to `grill` if one sitting can settle it.
- For a migration destination, add [migration](migration.md)'s safety steps to each ticket.
