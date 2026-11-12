---
name: ns-flow-bugfix
description: Fix a bug or production incident properly - reproduce it end to end first, find the root cause, fix test-first, verify, understand, review, check, open a PR with its reports, and ship it to production. Incident mode (live in production) stops the harm first, then uses a hotfix branch and a rollback-prepared release.
disable-model-invocation: true
argument-hint: "<bug report, incident summary, error, or issue reference> [--auto]"
---

# ns-flow-bugfix

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-bugs.md`, `../ns-route/references/topic-proof.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/bug.md`, `../ns-route/references/workflows/incident.md`, `../ns-route/references/workflows/ticket.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-ticket, ns-to-branch, ns-to-close, ns-to-deploy, ns-to-discover-codebase, ns-to-implement, ns-to-observe, ns-to-postmortem, ns-to-pr, ns-to-quality-check, ns-to-review, ns-to-rollback, ns-to-save, ns-to-scope-check, ns-to-spec, ns-to-stakeholder-brief, ns-to-understand, ns-to-verify
This flow is the `bug` and `incident` workflows in `../ns-route/references/workflows/bug.md` and `../ns-route/references/workflows/incident.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

If the bug description is missing, ask: what happened, what was expected, steps, environment, and how often. Facts in the repo are investigated, not asked.

This is the bug entrance, not the feature one - see `../ns-route/references/topic-bugs.md` "Bugs enter differently than features". Golden rule: no fix before evidence of root cause, unless the cause is trivially obvious on sight.

## Mode

If it is not already clear (for example from `/ns-route`), ask via the multiple-choice question tool whether this is broken, degraded, or exposed in production right now.

- **Bug** (not live-broken): the sequence below as written.
- **Incident** (live now, risk is critical): before anything else, stop the harm. Print the mitigate-first decision from `ns-to-observe` "Not healthy: mitigate first" (instant rollback, flag off, or continue to a fix, each with its time and what it leaves) and ask; a rollback runs `ns-to-rollback` Execute. Keep explanations short until production is healthy. Then skip step 1 unless the area is entirely unknown, branch `hotfix/...` from the release ref, keep the fix to the smallest change with no incidental refactor, run only the fast quality-check stages (types, lint, format, unit), and mark the PR expedited.

## Sequence

1. **Orient**: `ns-to-discover-codebase` scoped to the affected area, if unfamiliar.
2. **Branch**: `ns-to-branch` (`fix/...`, or `hotfix/...` from the release ref for a production fix).
3. **Reproduce first, end to end**, as close to how a real user experiences it as possible (real browser or app, real request path; for UI bugs ask the proof mode per `../ns-route/references/topic-proof.md` "Proof" and keep the failing run, with a clip of the failure, as the "before"), using `mattpocock-skills:diagnosing-bugs`. No fix until the bug is reproduced and the real cause is found. If it cannot be reproduced, report that and ask the user for more input.
4. **Root cause and fix plan**: state the cause and the smallest fix, and ask via the multiple-choice question tool for approval. If the fix implies a settled-decision change, escalate as in `ns-to-implement`. For non-trivial bugs write a short bugfix spec via `ns-to-spec`.
5. **Scope check**: `ns-to-scope-check` against the fix plan - a bug fix is especially prone to growing into an unasked-for refactor. Confirm the fix is the smallest change that resolves the root cause before writing code.
6. **Fix**: follow `ns-to-implement`, test-first with `mattpocock-skills:tdd`: a failing regression test that captures the reproduction, then the fix. Re-run the original E2E reproduction to confirm.
7. `ns-to-verify` (local: the original failure, then the same steps passing), `ns-to-understand`, `ns-to-review`, `ns-to-quality-check` (run, staged, last gate), `ns-to-save`, `ns-to-pr` (its stakeholder review explains how the bug was caught and fixed, and how to check it on the preview). As in `ns-flow-ticket`, gate after each, looping back on findings.
8. **Ship**, as `ns-flow-ticket` phases 11 to 16: `ns-to-rollback` (Prepare; mandatory for incidents and high risk), `ns-to-deploy` (hotfix path for incidents; "leave the PR open" stops here), `ns-to-verify production`, `ns-to-observe` (High tier for incidents; UNHEALTHY shows the mitigate-first decision), then on HEALTHY `ns-to-stakeholder-brief release` (the Shipped comment), `ns-to-postmortem` (mandatory in incident mode; it ends with the lessons card), and `ns-to-close`.

## Gates

Gate after each step per `../ns-route/references/core.md` "Run modes": in step mode ask continue (Recommended), redo, or stop. Fix nearby lint or flaky-test issues you meet, or flag them if large.
