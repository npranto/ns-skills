---
name: ns-flow-wayfinder
description: Front end for a destination with too much interconnected uncertainty for one planning session - capture the destination, clear the decision frontier via ns-to-wayfinder across as many sessions as it takes, then hand off into architecture, spec, tickets, delivery, and ship. Run manually for a big replatform, migration, or new subsystem where you don't yet know what the plan should be.
disable-model-invocation: true
argument-hint: "<big destination with lots of unknowns - migration, replatform, new subsystem> [--auto]"
---

# ns-flow-wayfinder

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/workflows/wayfinder.md`, `../ns-route/references/workflows/shared-blocks.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-architecture, ns-flow-delegate, ns-flow-ticket, ns-to-architect, ns-to-capture-idea, ns-to-design, ns-to-save, ns-to-spec, ns-to-tickets, ns-to-wayfinder
This flow is the `wayfinder` workflow in `../ns-route/references/workflows/wayfinder.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

Use this instead of `/ns-flow-feature` or `/ns-flow-architecture` only when `/ns-to-wayfinder`'s self-check says the uncertainty cannot be settled in one session. Otherwise those flows (or `/ns-route`) already cover it - do not reach for this by default just because a project is large.

## Sequence

1. `ns-to-capture-idea`, if no `docs/product/project-brief.md` exists yet - capture the destination, not the implementation.
2. `ns-to-wayfinder`, resumed every session until its map is clear. This is the multi-session core: expect several separate runs across separate sessions, each ending with the map updated on disk and a stop-or-continue gate.
3. Once the map is clear: `ns-to-architect` to consolidate the settled decisions into `docs/architecture/*` (skip only if the decisions are already concrete enough for the spec directly).
4. `ns-to-design`, if there is a UI.
5. `ns-to-spec`.
6. `ns-to-tickets`.
7. `ns-flow-ticket`, once per ticket in dependency order (or `ns-flow-delegate` for independent low or medium risk tickets).
8. Ship: each ticket goes to production through `ns-flow-ticket`, then the feature end ([FEATURE-END] in `../ns-route/references/workflows/shared-blocks.md`) once every ticket has closed. When the destination moves existing data, schema, a service, or a platform, add the `migration` workflow's safety steps (see `ns-flow-architecture` step 7).

## Gates

After each Wayfinder session, commit `docs/product/wayfinder/*` with `ns-to-save` (ask first) - `ns-to-wayfinder` already ends each run with its own summarize-and-ask step, and every decision ticket needs the human, so do not chain straight into the next ticket without it, even on autopilot. After the map clears, and after each subsequent phase, apply the same gate as the other flows: summarize, `ns-to-save`, then gate per `../ns-route/references/core.md` "Run modes" (in step mode: continue, revise, or stop and resume later).

Track overall progress in `.scratch/<slug>/progress.md` once a slug exists (after `ns-to-spec`); before that, the wayfinder map itself is the progress record, since it's built to survive exactly this kind of gap between sessions.

Do not begin implementation until the map is clear, the spec is written, and the tickets are approved.
