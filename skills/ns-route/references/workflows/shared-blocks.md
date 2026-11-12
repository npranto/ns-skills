## 3. Shared blocks

### [PLAN]

```
discover? ─▶ grill ◆ ─▶ architect? ◆ ─▶ design? ◆ ─▶ spec ◆ ─▶ tickets ◆
```

- `discover`: codebase unfamiliar or `docs/architecture/codebase-map.md` stale.
- `grill`: skip only if the decisions are already settled. Dependencies first, then one-way doors first. Every decision in grill, architect, and design ends with a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box").
- `architect`: only when a structural boundary changes (`../ns-route/references/topic-architecture-guardrail.md` "Deciding whether architecture work is needed"); a delta for existing systems.
- `design`: only with UI changes.
- `spec`: sized to the work: none for one ticket, one page for two to four, the full template for a project.
- `tickets`: dependencies first, then riskiest first. A multi-ticket feature settles its release strategy (one flag, visible, or ordered) here.
- Tiny or small scope: drop `spec` and `tickets`, and send the task description straight to [TICKET].

### [FEATURE-END]

Once every ticket of a multi-ticket feature has closed.

```
integration-check ─▶ flag on for everyone? ◆ ─▶ stakeholder-brief:release ◆ (one Shipped report for the feature)
```

- `integration-check`: the assembled feature against the spec, on the base branch and on production. A GAP or REGRESSION becomes a new ticket through [TICKET], an inline fix, or a `spec` correction, never a silent patch.
- `flag on`: only when the release strategy put the feature behind a flag; `deploy` for the flag change, then `observe`.
- The feature's Shipped report goes on the last ticket's PR, and is its own stop.

### Full lifecycle

The greenfield and feature path end to end, for orientation:

```
start ─▶ capture ─▶ wayfinder? ⟲ ─▶ [PLAN] ─▶ [TICKET] ×N ─▶ [FEATURE-END]
```
