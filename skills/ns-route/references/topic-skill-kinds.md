# Skill kinds and how skills run

## Three kinds of skills

- **Phase skills** (`/ns-to-*`): one job each, runnable alone on any project, feature, or bug. They read their inputs from disk, write their outputs to disk, then stop.
- **Flow skills** (`/ns-flow-*`): ordered chains of phase skills for a situation (new project, existing codebase, feature, ticket, delegated tickets, bugfix and incident, architecture and migration, wayfinder, docs). A flow never does the phase work itself. It reads the phase's `SKILL.md` and follows it, then gates before the next phase (see `../ns-route/references/core.md` "Run modes").
- **Router skill** (`/ns-route`): the front door and the command menu. Picks a workflow from `../ns-route/references/workflows/index.md` instantly when the situation is already obvious, otherwise classifies the task (type, scope, uncertainty, risk, reversibility, codebase familiarity, security sensitivity, data risk, sessions expected) and composes the exact phase/flow sequence and human gates for it, including modifiers a flat table can't express. Then runs it, or stops with just the plan. Start here.

`../ns-route/references/workflows/index.md` is the catalog: which skills chain in which order for every kind of task, with a diagram per workflow. It is the source of truth for which workflow fits a task and for the chains of workflows that have no flow skill; a flow's own `SKILL.md` holds its step-by-step detail. `workflow-map.html` is the visual version of `../ns-route/references/workflows/index.md`, shipped as the package's `docs/workflow-map.html`. Keeping the workflow files and that map in sync is a maintainer task: see the package's `docs/MAINTENANCE.md`.

Phase and flow skills are manual-only, so a flow or `/ns-route` never calls them through the harness's skill-invocation tool. It reads `../<skill>/SKILL.md` and follows it as the current phase. `mattpocock-skills:*` and other installed skills are invoked with the harness's skill-invocation tool as usual.
