---
name: ns-flow-architecture
description: Make or change architecture in a new or existing project - discover, focused grill, architecture decisions and ADRs, then either docs (decision only) or migration tickets delivered and shipped safely. Covers data, schema, service, or platform migrations. Large restructures, stack moves, rebuilds, and modernization take the re-engineering workflows via /ns-route.
disable-model-invocation: true
argument-hint: "<architectural question or migration goal> [--auto]"
---

# ns-flow-architecture

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/architecture.md`, `../ns-route/references/workflows/migration.md`, `../ns-route/references/workflows/shared-blocks.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-delegate, ns-flow-ticket, ns-to-architect, ns-to-close, ns-to-deploy, ns-to-discover-codebase, ns-to-docs, ns-to-grill-me, ns-to-integration-check, ns-to-observe, ns-to-quality-check, ns-to-rollback, ns-to-save, ns-to-spec, ns-to-tickets
This flow is the `architecture` and `migration` workflows in `../ns-route/references/workflows/architecture.md` and `../ns-route/references/workflows/migration.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

Ask what is being decided or changed and why now (via the multiple-choice question tool if not given). Note whether it is a **migration** (existing data, schema, service, or platform moves to a new shape): that turns on the migration requirements in steps 2, 3, and 7.

## Sequence

1. `ns-to-discover-codebase` scoped to the affected area (existing code only). Use `mattpocock-skills:codebase-design` vocabulary to find deepening opportunities and seams, and `mattpocock-skills:research` for questions needing primary-source facts.
2. `ns-to-grill-me`, focused on constraints, non-goals, and migration risk. One decision at a time.
3. `ns-to-architect`, updating (not rewriting) `docs/architecture/*`. Use `mattpocock-skills:prototype` to answer a design question by trying it, then throw it away. For a migration, the output includes an expand/contract plan.
4. **ADRs**: for each costly-to-reverse decision, offer an ADR via `mattpocock-skills:domain-modeling`. Supersede rather than edit accepted ADRs.
5. **Decision only** (no code must change): `ns-to-docs`, then `ns-to-save`, and stop.
6. **Code must change**: `ns-to-spec`, then `ns-to-tickets` sized for safe incremental, always-shippable steps, then `ns-flow-ticket` per ticket (or `ns-flow-delegate` for independent low or medium risk ones; migration tickets stay with the user); each ticket ships to production and closes before the next. Once every ticket has closed, `ns-to-integration-check` against the spec - individually safe steps do not guarantee the end state matches the plan - then the feature end ([FEATURE-END] in `../ns-route/references/workflows/shared-blocks.md`).
7. **Migration safety**, inside each ticket's delivery: `ns-to-quality-check` with the migration-safety stage mandatory; `ns-to-rollback` Prepare is mandatory (expand/contract ordering, DB backwards compatibility, data restoration); `ns-to-deploy` carries the full release plan with migration ordering; `ns-to-observe` runs at High tier (migration validation); `ns-to-close` confirms the expand/contract cleanup is done or ticketed. A destructive data step also needs explicit authorization before it runs, plus a backup and restore plan.

Stop after the architecture docs unless the user wants the migration tickets. This flow never implements directly; code changes happen only inside `ns-flow-ticket`. Gate after each step per `../ns-route/references/core.md` "Run modes", and track progress in `.scratch/<slug>/progress.md` once a slug exists.
