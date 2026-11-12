---
name: ns-to-discover-codebase
description: Inspect an existing repository and produce a concise system map of its structure, conventions, and constraints before proposing anything. Read-only.
disable-model-invocation: true
argument-hint: "[optional focus area, e.g. auth or checkout]"
---

# ns-to-discover-codebase

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Use before architecture, features, or bugfixes in a codebase you do not know. **Read-only: do not change files** because you would design something differently.

## Inspect

repository structure, package boundaries, framework conventions, routing, state management, backend architecture, database/data access, authentication, authorization, validation, styling/design system, testing, CI/CD, deployment, feature flags, observability, relevant existing abstractions, relevant docs, ADRs, coding standards. Also read `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `docs/agents/*`, and `docs/adr/*` when present.

If an optional focus area is given, go deep there and stay shallow elsewhere. For a large repo, use a read-only exploration agent for broad sweeps.

Prefer adapting to strong existing conventions over inventing new ones. Note weak spots as observations, not action items.

## Output

A concise system map. Show it in chat, then ask via the multiple-choice question tool whether to save it as `docs/architecture/codebase-map.md`. Include: stack, layout, key flows, conventions to follow, test and CI commands, documentation gaps (missing `CONTEXT.md`, ADRs, tracker config), and open questions.

Then suggest the next flow: `/ns-flow-feature`, `/ns-flow-bugfix`, `/ns-flow-architecture`, `/ns-flow-docs`, or `/ns-route` for anything else. If domain docs are missing, mention `mattpocock-skills:domain-modeling`.
