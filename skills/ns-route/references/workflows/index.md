# Engineering workflows

The map of which `ns-*` skills to run, in what order, for every kind of engineering task. `/ns-route` reads it to route and run workflows. It owns the chains of workflows that have no flow skill. For workflows that do, the diagram here is the map and the flow's `SKILL.md` holds the step-by-step detail; keep the two in sync. Every workflow follows `../ns-route/references/core.md`.

Visual version: `workflow-map.html` in the package's `docs/`. Keep it in sync with this folder (see the package's `docs/MAINTENANCE.md`).

- Not sure which workflow fits: `/ns-route <task>`. It classifies the task, picks a workflow below, applies modifiers (risk, security, data, scope), and can run it.
- Every workflow runs by hand (one skill at a time), as a flow (pauses after each phase), or on autopilot (runs start to finish, still stopping at every ◆). See section 2.

## 1. Pick a workflow

| You have | Workflow | Start with |
|---|---|---|
| An empty directory and an idea | [greenfield](greenfield.md) | `/ns-flow-new-project` |
| A codebase you do not know yet | [onboard](onboard.md) | `/ns-flow-existing-project` |
| A new capability to add | [feature](feature.md) | `/ns-flow-feature` |
| One existing ticket, or one small task | [ticket](ticket.md) | `/ns-flow-ticket` |
| Tickets for an agent to build while you do something else | [delegate](delegate.md) | `/ns-flow-delegate` |
| Wrong behavior, not live-broken right now | [bug](bug.md) | `/ns-flow-bugfix` |
| Production broken, degraded, or exposed right now | [incident](incident.md) | `/ns-flow-bugfix` (incident mode) |
| An architecture decision | [architecture](architecture.md) | `/ns-flow-architecture` |
| Data, schema, service, or platform moving to a new shape | [migration](migration.md) | `/ns-flow-architecture` (migration path) |
| A big destination with too many unknowns for one session | [wayfinder](wayfinder.md) | `/ns-flow-wayfinder` |
| A small refactor or tech-debt cleanup | [refactor](refactor.md) | `/ns-route` |
| A large restructure inside one stack | [restructure](re-engineering.md#restructure) | `/ns-route` |
| A working app moving to a new stack | [stack-move](re-engineering.md#stack-move) | `/ns-route` |
| A new build of a product that already exists | [rebuild](re-engineering.md#rebuild) | `/ns-route` |
| Old code with few tests to make safe to change | [modernize](re-engineering.md#modernize) | `/ns-route` |
| Correct but too slow or expensive | [performance](performance.md) | `/ns-route` |
| A package or platform version bump | [dependency](dependency.md) | `/ns-route` |
| CI/CD, hosting, IaC, observability tooling | [infrastructure](infrastructure.md) | `/ns-route` |
| A spike: a question to answer, not something to ship | [spike](spike.md) | `/ns-route` |
| A plan, estimate, or design doc requested before committing | [proposal](proposal.md) | `/ns-route` |
| Docs out of date | [docs](docs.md) | `/ns-flow-docs` |
| A teammate's PR to review | [pr-review](pr-review.md) | `/ns-to-understand` |
| A reviewed PR that needs to ship | [ship](ship.md) | `/ns-route` |
| Anything else, or unsure | classify first | `/ns-route` |

## 2. How to run a workflow

### Reading the diagrams

```
a ─▶ b        run a, then b
name?         conditional - runs only when its note says so
name ◆        needs you (a decision, approval, commit, or outward action) - stops even on autopilot
[BLOCK]       a shared block (`shared-blocks.md`, or `ticket.md` for [TICKET])
×N            once per ticket, in dependency order
⟲             repeats across sessions until done
```

Every project file change is also approved by you, one file at a time (`../ns-route/references/core.md` "Code change approval"). That applies everywhere and is not drawn.

Phase names drop their prefix: `grill` is `/ns-to-grill-me`, `discover` is `/ns-to-discover-codebase`, `rollback:prepare` is `/ns-to-rollback` in Prepare mode, `quality-check(setup-ci)` is `/ns-to-quality-check setup-ci`, `verify:local` is `/ns-to-verify local` (likewise `verify:preview`, `verify:production`, `verify:baseline`, `verify:setup`). `mp:<name>` is `mattpocock-skills:<name>`, invoked with the harness's skill-invocation tool.

### Four ways to run

| Mode | How | Stops |
|---|---|---|
| By hand | `/ns-route <task>` and choose "by hand": it prints the exact commands with their real arguments and stops. Or type each `/ns-to-*` command from the diagram yourself. Every phase ends by suggesting the next one. Files on disk carry the handoff, so `/clear` between phases is safe. | wherever you stop |
| Flow, step mode | `/ns-flow-<name> <input>` | after every phase (continue, redo, or stop), plus every ◆ |
| Flow, autopilot | `/ns-flow-<name> <input> --auto` | only at ◆ (`../ns-route/references/core.md` "Run modes") |
| Composed workflow | `/ns-route <task>` (add `--auto` for autopilot). For workflows with no flow skill, ns-route runs the chain itself. | same as the chosen mode |
| Hand to an agent | `/ns-route <task>` and choose "hand to an agent", or `/ns-flow-delegate <tickets>`. Low or medium risk tickets with settled plans only. | the agent works alone to a review-ready PR; you review what it decided, then the release card (`../ns-route/references/core.md` "Code change approval", the delegate exception) |

### Handing a workflow to another agent

Autopilot needs an interactive Claude session (terminal, VS Code, or a Herdr pane), because file edits and ◆ gates need a human. Headless runs (the harness's non-interactive mode) can only run read-only phases (`discover`, `/ns-route` classification, `understand`, `review` report).

- Any session: open Claude in the repo and send the same command, for example `/ns-flow-feature "wishlist sorting" --auto`.
- Herdr pane: `herdr agent prompt <name> "/ns-flow-ticket .scratch/<slug>/issues/03-slug.md --auto"`.
- Many tickets at once, built without you: `/ns-flow-delegate <tickets>` starts one agent per ticket in its own worktree (see [delegate](delegate.md)).
- If the host cannot type slash commands, send the prompt `Read the ns-route skill's references/workflows/index.md and run workflow <name> for: <task>, on autopilot, following the ns-route skill's references/core.md.` Phase skills are manual-only, so agents read their `SKILL.md` instead of calling them through the harness's skill-invocation tool.

### Resuming

Flows track progress in `.scratch/<slug>/progress.md` (workflow, run mode, stop point, choices, phase checklist), except the wayfinder map, which is its own progress record until a slug exists. Rerun the same command in a fresh session to pick up where it stopped. Not sure where you left off: `/ns-route status` works it out from git, ticket files, progress files, and open PRs, and prints the next command.

## 4. Workflows

Each workflow's file is linked in the table above. [TICKET] is in `ticket.md`, [PLAN] and [FEATURE-END] are in `shared-blocks.md`, and the skill inventory is in `skill-inventory.md`.

## 5. Modifiers

`/ns-route` adjusts any workflow above for scope, uncertainty, familiarity, security, data risk, risk, and reversibility (its step 3 "Modifiers"). The ones that change a diagram most:

- Security-sensitive: a security pass inside `architect`, then the `security-review` skill ◆ before `quality-check`.
- High risk or hard to reverse: `split-ticket` even at medium scope, `understand` and `review` never skipped, `rollback:prepare` ◆ before any `deploy`, `observe` at High tier.
- High uncertainty at large scope over several sessions: put [wayfinder](wayfinder.md) in front.

When ns-route hands off to a flow, its printed sequence, with modifiers applied, takes precedence over the flow's defaults.
