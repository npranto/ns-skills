---
name: ns-flow-existing-project
description: Onboard onto an existing codebase safely - discover it, fill documentation gaps, then route to the feature, bugfix, architecture, docs, or ticket flow, or to /ns-route for anything else.
disable-model-invocation: true
argument-hint: "[what you want to do in this codebase] [--auto]"
---

# ns-flow-existing-project

Read first: `../ns-route/references/core.md`, `../ns-route/references/profile.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/onboard.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-architecture, ns-flow-bugfix, ns-flow-docs, ns-flow-feature, ns-flow-ticket, ns-to-discover-codebase, ns-to-quality-check, ns-to-save, ns-to-verify
This flow is the `onboard` workflow in `../ns-route/references/workflows/onboard.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

## Sequence

1. **Discover**: follow `ns-to-discover-codebase`. Read-only. Save the map if the user wants.
2. **Doc gaps**: from the map, check for `CONTEXT.md`, `docs/adr/`, `docs/agents/*`, and a useful `CLAUDE.md`. Ask via the multiple-choice question tool whether to fill them. If yes, run `mattpocock-skills:domain-modeling` for the glossary and ADR candidates (grounded in the code, not invented), set up the issue tracker docs if absent, and keep `CLAUDE.md` short per `mattpocock-skills:writing-for-agents`. Commit with `ns-to-save`.
3. **Project profile**: when `docs/agents/workflow.md` is missing, write it from `../ns-route/references/profile.md` (filled from the repo; asks only for host facts not on disk). Commit with `ns-to-save`.
4. **Verification skill**: when the profile names none, offer `ns-to-verify setup` (Recommended): the project verification skill and its feature map, proven once.
5. **Safety net**: ask whether to set up CI checks (`ns-to-quality-check` setup-ci): the core four on every PR, and for a project with UI the E2E workflow (`../ns-route/references/e2e.md`). Recommended before the first code PR.
6. **Route**: ask what the user wants to do, then hand off by reading the matching flow and following it in the same run mode:
   - new capability -> `ns-flow-feature`
   - broken behavior, or a live incident -> `ns-flow-bugfix`
   - an architecture decision or a migration -> `ns-flow-architecture`
   - a large restructure, a stack move, a rebuild, or legacy code to make safe -> `ns-route` (re-engineering workflows)
   - docs out of date -> `ns-flow-docs`
   - a ticket that already exists -> `ns-flow-ticket`
   - anything else (small refactor, performance, dependency, infrastructure, spike, proposal) -> `ns-route`

Gate after each step per `../ns-route/references/core.md` "Run modes". Prefer adapting to existing conventions over imposing new ones. Never change files just because you would design them differently.
