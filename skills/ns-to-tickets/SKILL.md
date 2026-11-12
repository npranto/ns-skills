---
name: ns-to-tickets
description: Break a spec into small vertical-slice implementation tickets with dependency graph and parallelism classification, one file per ticket.
disable-model-invocation: true
argument-hint: "[path to spec.md or feature-slug]"
---

# ns-to-tickets

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-delivery.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Input: the spec (ask for it if not given or found; never invent one). Follow the repo's issue-tracker convention (`docs/agents/issue-tracker.md`): one file per ticket, `.scratch/<slug>/issues/NN-slug.md`, numbered from `01`, never one combined file.

## Decomposition

Tracer-bullet / vertical-slice. Prefer "User can create a note and see it after refresh" over "Build database layer". Each ticket travels through whatever layers are needed to produce demonstrable behavior. Foundation work (scaffold, env validation, auth integration, DB connection) may stand alone when required by upcoming behavior and independently verifiable.

Each ticket must fit comfortably in one fresh coding-agent context. If it needs a massive diff or many independent concepts, split it (or leave it for `/ns-to-split-ticket`). One ticket, one purpose: a bug fix is its own ticket, and work in two isolated domains is two tickets.

**A new project's ticket 01 is the walking skeleton:** the thinnest slice that runs end to end and is live in production. Its acceptance criteria are what it leaves behind: CI running types, lint, tests, and build on every PR; preview deployments on PRs; the E2E suite passing locally, on the preview, and as `@smoke` on production (`../ns-route/references/e2e.md`); the project profile filled in; the project verification skill proven once (`/ns-to-verify setup`); one log line findable in the host's logs; the rollback path tried once; and, when the architecture has a database or auth, each touched once. Feature tickets start after 01 has shipped.

## Ticket template

`Status: open` and `Blocked by: NN, NN` lines at the top, then:

TITLE, USER/VISIBLE OUTCOME, SCOPE, OUT OF SCOPE, ACCEPTANCE CRITERIA, TESTING SEAM, DEPENDENCIES, BLOCKED BY, DEMO, RISKS, UNDO, RELEVANT ARCHITECTURE CONSTRAINTS, then two empty headings: `## Decisions` and `## Comments` (`../ns-route/references/core.md` "Artifact locations").

- **ACCEPTANCE CRITERIA** are numbered, each an action and a visible result that a non-engineer could check on a preview link. Later phases (verification, the PR, close) reuse them word for word.
- **UNDO** says how this ticket is reversed once shipped: revert, drop a column, flag off, and anything that would need restoring.

## After the tickets

Show the dependency graph and classify every ticket as SEQUENTIAL, PARALLEL-SAFE, or PARALLEL-WITH-CONFLICT-RISK. Do not parallelize just because workers are available. Optimize for total delivery time including merge and review cost.

**Order:** dependencies first. Where they leave a choice, the riskiest and least understood ticket goes first, while changing the plan is still cheap.

**Release strategy** (more than one ticket): put it to the user as one decision (`../ns-route/references/topic-learn-box.md` "Learn box"): hide the feature behind one flag until the last ticket ships, ship each ticket visibly, or order the tickets so nothing user-visible appears until the last one. With a flag, the first ticket adds it, the feature's last step turns it on, and a flag-removal ticket is written now. A project with no flag system: say so, and offer a minimal one (an env var or a config constant) as an option.

Present the proposed ticket list first and ask via the multiple-choice question tool for approval before writing files. Do not implement. Suggest `/ns-to-split-ticket` for any ticket that looks large, otherwise `/ns-flow-ticket`.
