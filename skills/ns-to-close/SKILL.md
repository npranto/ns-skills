---
name: ns-to-close
description: Verify a piece of work is truly finished after /ns-to-observe reports HEALTHY - acceptance criteria, merged PR and its reports, flag/migration cleanup, docs, follow-ups, branches - then close the ticket, clear local evidence, and name the next ticket from real state. Ends with an explicit CLOSED/NOT CLOSED verdict.
disable-model-invocation: true
argument-hint: "[ticket, PR, or deploy/observe summary]"
---

# ns-to-close

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

The last phase of a ticket. A healthy production is not completion: closing means every loose end this work created is accounted for, and every ticket and doc describing it says what the code does.

## Precondition

An explicit HEALTHY verdict from `/ns-to-observe` for this release. Reuse it from this session, or ask for the evidence if resuming cold. Observation not run, UNHEALTHY, or a rollback in flight: stop and say so.

## Gather

Reuse what this session has: the ticket and spec (`.scratch/<slug>/issues/*`), the PR, the release card, the proof results, and the observe verdict. Ask via the multiple-choice question tool for whatever is missing.

## Checklist

Run the real check for each row: read the file, query `gh-axi`, read the flag or migration state. Each row is pass, gap, or accepted risk with the user's reason, with its evidence.

| # | Check | How to verify |
|---|---|---|
| 1 | Acceptance criteria hold on production | The `/ns-to-verify production` result and the smoke E2E run on the merge commit. Reuse `/ns-to-integration-check` evidence when it ran. |
| 2 | PR merged | `gh-axi`: the PR's real merge state into the base branch. |
| 3 | The PR carries every report | The table in `../ns-route/references/pr-writing.md`: both description regions, the local, preview, and production proof, the stakeholder review, the Shipped comment, and an evidence link that opens. One is missing: post it now. |
| 4 | The ticket tells the truth | Scope and criteria match what shipped; every decision is under `## Decisions`; deviations and deferrals are under `## Comments` with the PR link. |
| 5 | Flags removed or planned | Each flag this work added or toggled is removed from code and config, or has its own removal ticket. |
| 6 | Migration cleanup tracked | Expand/contract cleanup (dropping old columns, removing dual-write code) is done or has its own ticket. |
| 7 | Docs updated | `/ns-to-docs` ran for this work, or record why nothing needed it. Drift found now becomes a follow-up through the docs workflow. |
| 8 | Follow-ups ticketed | Trimmed scope, declined or accepted findings, skipped proof rows, known limits, accepted risks: anything not already a ticket becomes one via `/ns-to-tickets`. |
| 9 | No throwaway code merged | No leftover prototype code, scratch scripts, or dead paths this work introduced. |
| 10 | Parent tickets updated | The child is marked done on its umbrella, a sibling whose assumptions changed gets a comment, and the spec is corrected if behavior differs. |
| 11 | Branch and worktree cleaned up | The merged branch deleted locally and on the remote, and any worktree this ticket created removed. Ask first, and check for unpushed work. |
| 12 | External tracker updated | When the project uses one: an outward action, confirm first. |

## Verdict

State explicitly: **CLOSED** or **NOT CLOSED**.

- **NOT CLOSED:** list exactly what is missing and the phase that resolves each. Leave the ticket's `Status:` alone and stop.
- **CLOSED:** every row holds, or its gap is accepted with a reason. In one approved edit to the ticket file, set `Status: closed` and append the closing entry under `## Comments`: the PR and merge commit, the version (with versioning), the preview and production proof with their scores, the health verdict, and what was deferred. Then the last steps.

## Last steps, on CLOSED

1. **The next ticket, from real state.** Read every ticket file's `Status:` and `Blocked by:` as it is on disk. Confirm with `gh-axi` that each ticket marked done has a merged PR. A ticket is ready when it is `open`, every blocker is closed and merged, and no branch or open PR exists for it. Order ready tickets by dependencies, then risk first. Several equally ready: list them and recommend one. None: say what blocks each, or that this was the feature's last ticket. Anything that could not be checked is stated, never guessed.
2. **Clear local evidence.** Delete `.verification/<branch>/` for this ticket only, after looking at it and after row 3 holds: the published evidence page opens and holds the files. A published page is never deleted.
3. **Report:** the full checklist table, what shipped, and the next step as an exact command: `/ns-flow-ticket <next ticket path>`, or for the feature's last ticket the feature end (`/ns-to-integration-check <slug>`). Under it, offer `announce it`: a company announcement written from `references/announcement.md`, never posted by the agent.

## Do not

Do not mark any row satisfied without checking the real state. Do not close a ticket with an open gap; record it as an accepted risk with a reason instead. Do not write follow-up tickets inline; hand off to `/ns-to-tickets`.
