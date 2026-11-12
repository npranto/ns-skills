# Output

Print exactly this shape:

```
## Classification

| Dimension | Value | Why |
|---|---|---|
| Task type | ... | ... |
| Scope | ... | ... |
| Uncertainty | ... | ... |
| Risk | ... | ... |
| Reversibility | ... | ... |
| Codebase familiarity | ... | ... |
| Security sensitivity | ... | ... |
| Data risk | ... | ... |
| Sessions expected | ... | ... |

<one line, only when what the user asked for does not fit: "You asked for a ticket, but this needs several: feature workflow.">

## Recommended workflow

Baseline: <workflow name> (`../ns-route/references/workflows/index.md`), <flow command if it has one>

`/command-one` (note)
→ `/command-two`
→ per ticket: `/ns-flow-ticket`
→ ...

## Skipped

- <phase>: <one-line reason tied to a dimension value>
- ...

## Human gates

1. <gate>
2. <gate>
...
```

Each **Why** is at most ten words and names the evidence behind the value: a file, a ticket line, or a repo fact (for example "three queries read `notes`", "codebase map updated 2 days ago"). A value with no evidence says so ("asked: depends on intent").

Human gates always include every commit and every PR and, per `../ns-route/references/core.md`, every file edit's own approval (do not list the latter separately, it is implicit). Add to the numbered list only the phase-level gates that actually appear in the composed workflow: continue-or-stop after each Wayfinder decision ticket (if `/ns-flow-wayfinder` is included - it is inherently multi-session), spec approval (if `/ns-to-spec` is included), ticket approval (if `/ns-to-tickets` is included), ADR sign-off (if `/ns-to-architect` produced an ADR-worthy decision), security-review sign-off (if security sensitivity is sensitive), destructive-operation authorization (if data risk is destructive), deploy authorization (if `/ns-to-deploy` is included), rollback plan review (if `/ns-to-rollback` runs in Prepare mode), rollback authorization if `/ns-to-observe` reports UNHEALTHY (whenever `/ns-to-deploy` is included, since `/ns-to-observe` always follows it, and hands off to `/ns-to-rollback` in Execute mode). These are the gates autopilot still stops at (`../ns-route/references/core.md` "Run modes").
