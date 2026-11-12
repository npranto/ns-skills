---
name: ns-flow-feature
description: Add a feature to an existing project - discover, scoped grill, optional architecture and design, spec, tickets, each ticket delivered to production and closed, then the integration check and the feature end.
disable-model-invocation: true
argument-hint: "<feature description> [--auto]"
---

# ns-flow-feature

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-architecture-guardrail.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/workflows/feature.md`, `../ns-route/references/workflows/shared-blocks.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-delegate, ns-flow-ticket, ns-to-architect, ns-to-branch, ns-to-deploy, ns-to-design, ns-to-discover-codebase, ns-to-grill-me, ns-to-integration-check, ns-to-observe, ns-to-save, ns-to-spec, ns-to-stakeholder-brief, ns-to-tickets
This flow is the `feature` workflow in `../ns-route/references/workflows/feature.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

If the feature description is missing, ask for it. Pick a `<slug>` for `.scratch/<slug>/` and confirm.

## Sequence

| # | Phase | When |
|---|---|---|
| 1 | `ns-to-discover-codebase` (scoped to the feature area) | skip if a fresh codebase map exists |
| 2 | `ns-to-branch` for docs/spec work | optional, ask |
| 3 | `ns-to-grill-me` (scoped to this feature, reads brief if any) | always, unless the user says decisions are settled |
| 4 | `ns-to-architect` (delta only) | per the architecture guardrail in `../ns-route/references/topic-architecture-guardrail.md`. Skip for local changes |
| 5 | `ns-to-design` (delta only) | UI changes |
| 6 | `ns-to-spec` | sized to the work (`ns-to-spec` "Output"): skip for a one-ticket feature |
| 7 | `ns-to-tickets` | always (one ticket is fine for a small feature) |
| 8 | `ns-flow-ticket` per ticket, dependency order then risk first (or `ns-flow-delegate` to hand independent low or medium risk tickets to agents). Each ticket ships to production and closes before the next starts; the release strategy chosen in `ns-to-tickets` (one flag, visible, or ordered) keeps unfinished work hidden | always |
| 9 | `ns-to-integration-check` | more than one ticket, once every ticket has closed - proves the assembled feature against the spec, on the base branch and on production |
| 10 | Flag on for everyone (`ns-to-deploy` for the flag change, then `ns-to-observe`) | the feature is behind a flag; its own stop |
| 11 | `ns-to-stakeholder-brief release <slug>` (one Shipped report for the whole feature) | more than one ticket; its own stop |

Decide skips with the user using the multiple-choice question tool, recommending based on the discovery map. After each phase: summarize briefly, offer to commit artifacts via `ns-to-save` (ask first, even on autopilot), and gate per `../ns-route/references/core.md` "Run modes": in step mode ask continue / revise / stop. Track progress in `.scratch/<slug>/progress.md`. Do not begin implementation until the spec (when one is written) and the tickets are approved.
