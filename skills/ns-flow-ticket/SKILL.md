---
name: ns-flow-ticket
description: Deliver ONE ticket (or one small task with no ticket) end to end, to production - split-ticket, branch, scope-check, implement, verify, understand, review, quality-check, save, PR, deploy, verify production, observe, Shipped, close. The inner loop reused by every flow that changes code.
disable-model-invocation: true
argument-hint: "<ticket path, id, or small task description> [--auto]"
---

# ns-flow-ticket

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-skill-kinds.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/workflows/ticket.md`, `../ns-route/references/workflows/shared-blocks.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-to-branch, ns-to-close, ns-to-deploy, ns-to-implement, ns-to-observe, ns-to-pr, ns-to-quality-check, ns-to-review, ns-to-rollback, ns-to-save, ns-to-scope-check, ns-to-split-ticket, ns-to-stakeholder-brief, ns-to-understand, ns-to-verify
This flow is the [TICKET] block in `../ns-route/references/workflows/ticket.md`.

## Input

A ticket path or id. If not given, list open, unblocked tickets from the tracker and let the user pick with the multiple-choice question tool. Refuse to start a ticket whose `Blocked by` tickets are not resolved unless the user overrides.

A task description instead of a ticket (small work routed here by `/ns-route` or another flow): restate it as SCOPE, OUT OF SCOPE, and ACCEPTANCE CRITERIA in the `/ns-to-tickets` template's terms, and confirm via the multiple-choice question tool before branching. That confirmation is a plan approval, so it holds even on autopilot. Write a ticket file only if the user wants one; otherwise track progress in `.scratch/<slug>/progress.md`.

## Phases

Phase skills are manual-only: for each phase, read `../<phase>/SKILL.md` and follow it exactly as the current phase, with this ticket as the input. Never call them through the harness's skill-invocation tool.

| # | Phase | Skip when |
|---|---|---|
| 1 | `ns-to-split-ticket` | ticket is already small (offer, default skip if the sizing test passes) |
| 2 | `ns-to-branch` (stacked base if `Blocked by` is unmerged; worktree if tickets run in parallel) | already on the ticket's branch |
| 3 | `ns-to-scope-check` | never (trim, blast radius, abuse cases, and design choices, right before implementing) |
| 4 | `ns-to-implement` | never |
| 5 | `ns-to-verify local` (full proof, score, evidence) | docs-only change; the user may also choose skip at its run question |
| 6 | `ns-to-understand` | never (mandatory gate) |
| 7 | `ns-to-review` | trivial docs-only change (ask) |
| 8 | `ns-to-quality-check` (run, staged, last gate before commit) | never (the user may skip individual stages) |
| 9 | `ns-to-save` | nothing to commit |
| 10 | `ns-to-pr` (push, open, reports, preview check, stakeholder review) | already opened and enriched |
| 11 | `ns-to-rollback` (Prepare) | risk below high, and no migration (`/ns-route` or the ticket) |
| 12 | `ns-to-deploy` (the release card; its "merge and ship" is the merge) | never; "leave the PR open" stops the flow here, and rerunning it continues from the release card |
| 13 | `ns-to-verify production` | never |
| 14 | `ns-to-observe` (UNHEALTHY: mitigate first, then `ns-to-rollback` Execute) | never |
| 15 | `ns-to-stakeholder-brief release` (the Shipped comment) | only after HEALTHY |
| 16 | `ns-to-close` | only after HEALTHY |

## Code changes

Every code change in every phase is applied file by file through file-edit tool for the user to approve. No scripts or automation, and no phase, worker, or pipeline may apply changes on its own. See "Code change approval" in `../ns-route/references/core.md`.

## Gates

After each phase, summarize the outcome in two or three lines, then gate per `../ns-route/references/core.md` "Run modes": in step mode ask continue to the next phase (Recommended), redo this phase, or stop here; on autopilot continue unless the phase hit a gate that is never auto-answered. If a phase reports blocking findings (a FAILED proof, failing checks, review issues), loop back to `ns-to-implement` for fixes, then re-run the affected phase (and quality-check, always last) before moving on. Note the phase progress in the ticket's `## Comments` (or `progress.md` for a task with no ticket), and set `Status:` to `in-progress`; `/ns-to-close` sets it to `closed`. When a fresh context would help, say so: files on disk carry the handoff.

**Delegate mode** (prompted "in delegate mode" by `/ns-flow-delegate`): run on autopilot under `../ns-route/references/delegate.md`. Every stop not on its "always stops" list takes the recommended answer without waiting, and each such decision is recorded in the ticket's `## Decisions` marked `decided by agent`. Stop after phase 10 with the PR open and review-ready; the captain session handles the rest.

The only merge is the one the user authorizes on `/ns-to-deploy`'s release card. Each ticket reaches production and closes before the next starts. After close, suggest the next ticket `/ns-to-close` named, or the feature end ([FEATURE-END] in `../ns-route/references/workflows/shared-blocks.md`) once every ticket of the feature has closed.
