---
name: ns-flow-new-project
description: Full greenfield process - start, capture, grill, architect, design, spec, tickets, then the walking skeleton and every ticket delivered to production one at a time, then the integration check and feature end. Run manually for a brand-new project.
disable-model-invocation: true
argument-hint: "[project name or rough idea] [--auto]"
---

# ns-flow-new-project

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/workflows/greenfield.md`, `../ns-route/references/workflows/shared-blocks.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-delegate, ns-flow-ticket, ns-flow-wayfinder, ns-to-architect, ns-to-capture-idea, ns-to-design, ns-to-grill-me, ns-to-integration-check, ns-to-quality-check, ns-to-save, ns-to-spec, ns-to-stakeholder-brief, ns-to-start, ns-to-tickets
This flow is the `greenfield` workflow in `../ns-route/references/workflows/greenfield.md`.

Phase skills are manual-only: for each phase, read `../<phase>/SKILL.md` and follow it as the current phase, never through the harness's skill-invocation tool.

## Sequence

| # | Phase | Output |
|---|---|---|
| 1 | `ns-to-start` | repo, README, tracker, first commit |
| 2 | `ns-to-capture-idea` | `docs/product/project-brief.md` (with success signals, risks, and suggested blind spots) |
| 3 | `ns-to-grill-me` (or `ns-flow-wayfinder` instead, if several interlocking unknowns cannot be settled in one session) | `CONTEXT.md`, ADRs, settled decisions |
| 4 | `ns-to-architect` | `docs/architecture/*` |
| 5 | `ns-to-design` (only if there is a UI) | `docs/design/*` |
| 6 | `ns-to-spec` | `.scratch/<slug>/spec.md` |
| 7 | `ns-to-tickets` | `.scratch/<slug>/issues/*` |
| 8 | Ticket 01, the walking skeleton (`ns-to-tickets`): `ns-flow-ticket`, which takes it to production and closes it | the whole path live in production: CI core checks (via `ns-to-quality-check setup-ci` inside the ticket), preview deployments, E2E in three places, the profile and verification skill, a findable log line, rollback tried once |
| 9 | `ns-flow-ticket` for every other ticket, in dependency order then risk first, only after 01 has shipped (or `ns-flow-delegate` to hand independent low or medium risk tickets to agents) | each ticket live in production and closed, one at a time |
| 10 | The feature end: `ns-to-integration-check`, flag on for everyone (when flagged), `ns-to-stakeholder-brief release <slug>` | the assembled project verified against the spec, on the base branch and on production, and one Shipped report |

## Gates

After each phase, commit the artifacts with `ns-to-save` (ask first, even on autopilot), summarize in two or three lines, and gate per `../ns-route/references/core.md` "Run modes": in step mode ask continue (Recommended), revise this phase, or stop and resume later. Recommend clearing context between planning phases since artifacts on disk are authoritative.

Ask at the start which phases to skip (for example no UI means no design, tiny project means fold tickets into the spec). Track progress in a short checklist in `.scratch/<slug>/progress.md` so the flow can resume, and on start read it if it exists.

Do not begin implementation until the spec and tickets are approved.
