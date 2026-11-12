---
name: ns-to-architect
description: Design the simplest production-quality architecture one decision at a time, then write system, data-model, and flows docs plus ADR candidates. Design only, no code.
disable-model-invocation: true
argument-hint: "[project or feature to architect]"
---

# ns-to-architect

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/topic-delivery.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Phase 3 - ARCHITECT. Act as a pragmatic Staff/Principal full-stack engineer.

## Inputs (authoritative)

`CLAUDE.md`, `CONTEXT.md`, `docs/product/project-brief.md`, `docs/adr/*`, and for existing code `docs/architecture/codebase-map.md` (run `/ns-to-discover-codebase` if missing). If `CONTEXT.md` is missing, run `mattpocock-skills:domain-modeling` first to build it from the brief. Do not reopen settled decisions or the already chosen stack unless there is a serious technical issue or genuine contradiction.

Ask (via the multiple-choice question tool) for anything missing: scale expectations, team size and timeline, hosting constraints, chosen stack if not recorded.

## Do not

Scaffold, install dependencies, write production code, create tickets, or move into UX design.

## Objective

The simplest architecture that satisfies the scope, is production-safe, stays understandable to the human maintainer, supports reasonable growth, keeps migration paths open, follows the framework's current conventions, and slices cleanly into vertical tickets.

Avoid architecture astronautics: no microservices, queues, caches, event buses, generic repository frameworks, unneeded global state, speculative infrastructure, or excessive DI without a concrete requirement. Prefer boring, replaceable, direct, explicit, readable.

## Process

Work through unresolved decisions **one at a time**, in dependency order; among decisions that do not depend on each other, one-way doors (expensive to reverse) come first. For each: what must be decided, your recommendation, why it fits this scope, meaningful alternatives, the tradeoff, reversibility, a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box"), then ask the user to approve or change it. Cover at least:

**Core:** system shape, server/client boundaries, route/page organization, module organization, schema, state representation, relationship modeling, ownership/authorization enforcement, input validation, query and mutation architecture, autosave/write flow, concurrency and versioning, search strategy, error handling, loading and mutation states, cache/revalidation, environment config, logging/observability, migrations, testing seams, deployment assumptions, security.

**Often missed (decide explicitly or record as "not needed"):**

- Identity: authn method, sessions/tokens, roles and permissions model, multi-tenancy or org boundaries.
- API contract: style (server actions, REST, RPC, GraphQL), typing shared across the boundary, error shape, pagination, versioning, idempotency for retried writes.
- Frontend: rendering strategy (SSR/SSG/SPA/islands), data-fetching and client state ownership, SEO and metadata needs, i18n and time zones, browser/device support, bundle and performance budget.
- External integrations: third-party services, webhooks in and out, failure and timeout behavior, secrets handling, vendor lock-in and exit path.
- Async work: background jobs, scheduled tasks, email/notifications, long-running operations. Default to none or in-process until a concrete requirement exists.
- Files and media: uploads, storage, size and type limits, scanning, delivery/CDN.
- Data lifecycle: retention, soft vs hard delete, export, backups and restore, PII and compliance (GDPR and similar), audit trail, seed and test data.
- Abuse and resilience: rate limiting, quotas, input abuse, graceful degradation, expected failure modes.
- Delivery: environments, CI/CD, migration rollout (expand/contract, backward compatible), feature flags, rollback, cost and quota ceilings, dependency and license choices.
- Non-functional targets: latency, availability, scale numbers, analytics/product metrics, accessibility constraints that affect structure.

Skip items that do not apply, and add any the project needs.

**Migration** (existing data or schema moves to a new shape): also decide the expand, move, contract plan. List each step in order (add the new shape, write to both, backfill, read from the new, remove the old), what makes it safe to stop after that step, and how it is undone. Each step later becomes its own ticket. Record the plan in `docs/architecture/data-model.md` under "Migration plan".

For module boundaries and seams, use `mattpocock-skills:codebase-design` vocabulary (deep modules, small interfaces). For any decision that hinges on a library or platform fact you are unsure of, run `mattpocock-skills:research` or check current docs rather than guessing. Use `mattpocock-skills:prototype` for a decision best answered by trying it.

## Output (after all decisions resolve)

- `docs/architecture/system.md`: overall shape, boundaries, module structure, server/client responsibilities, authn/authz, validation, API contract, query/mutation approach, errors, caching, observability, integrations and async work (if any), security/privacy and data lifecycle, deployment and rollout, expected scale and NFR targets, known bottlenecks, **what we are NOT building**, deliberate non-abstractions, future extension points.
- `docs/architecture/data-model.md`: tables, key columns, relationships, constraints, indexes, ownership rules, state representation, concurrency/version behavior.
- `docs/architecture/flows.md`: each important end-to-end flow as a compact path, for example `UI -> server boundary -> application logic -> database -> response/revalidation -> UI`.
- Every major decision lists WHY, ALTERNATIVES, TRADEOFF, REVERSIBILITY. Flag ADR-worthy ones and offer to write them via `mattpocock-skills:domain-modeling`.

Finish with a section **WHAT I NEED TO UNDERSTAND BEFORE IMPLEMENTATION**: the few architectural concepts the human must grasp to maintain this. Then stop. Suggest `/ns-to-design` (UI work) or `/ns-to-spec`.
