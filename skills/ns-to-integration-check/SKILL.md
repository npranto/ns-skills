---
name: ns-to-integration-check
description: After every ticket for a feature has merged, validate the assembled feature against the original spec end to end - not per-ticket acceptance criteria, but cross-ticket seams, composed user flows, and regressions between tickets. Catches "A works, B works, C works, A+B+C doesn't."
disable-model-invocation: true
argument-hint: "<feature slug or path to spec.md>"
---

# ns-to-integration-check

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-reading-ci.md`, `../ns-route/references/topic-proof.md`, `../ns-route/references/topic-delivery.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Runs once, after every ticket belonging to a feature has shipped to production and closed - never per ticket. Each ticket's own `/ns-to-review` and `/ns-to-quality-check` already proved that ticket in isolation, against the base branch as it stood at that ticket's merge time. This phase proves the assembled result: the feature as a whole, against `spec.md`, on the base branch as it stands now with every ticket composed together. "Ticket A works. Ticket B works. Ticket C works. A + B + C does not work" is exactly the failure mode this exists to catch. Especially important after `/ns-flow-delegate`, where agents wrote sibling tickets without seeing each other's final diff.

## Preconditions

- Every ticket under the feature's slug is `Status: closed` (shipped to production and closed by `/ns-to-close`) with a merged PR. List them and stop to ask if any is still open, in-progress, or its PR unmerged - do not partially integration-check a feature.
- Base branch checked out and pulled (`git fetch`, checkout the base, pull). This is the first time the tickets are seen composed together, so a stale local base defeats the point.

## Inputs

`spec.md` for the feature (ask for the slug if not given or found; never invent one), and the ticket list under `.scratch/<slug>/issues/`. Do not re-read each ticket's individual diff in isolation - read and exercise the assembled code on the base branch as it stands now.

## What per-ticket gates cannot see

Per-ticket review and quality-check each only ever compared one branch to the base at that ticket's own merge time. They cannot see:

- Two tickets, each individually reasonable, that disagree on a contract - the shape of data one produces vs. what another expects, an ordering assumption, a naming or unit mismatch.
- A user flow in the spec that only exists once every ticket has landed - no single ticket owned all of it, so nobody proved it end to end.
- A later ticket silently regressing an earlier one's acceptance criteria (a shared component's behavior shifted, a shared util's contract changed).
- Duplicate or conflicting implementations of the same concern, introduced independently by parallel tickets.

## Checklist

1. **Re-derive the feature's user flows and acceptance criteria from `spec.md` directly**, not from any one ticket. Every USER FLOWS and ACCEPTANCE CRITERIA line in the spec is a row to verify.
2. **Walk each flow end to end on the assembled base branch**, exactly as a real user would, with `/ns-to-verify`'s method and evidence (`../ns-route/references/topic-proof.md` "Proof"; never skip silently for a user-facing flow). For API-only features, drive the real endpoints in sequence instead of one at a time.
3. **Check the seams.** For every pair of tickets that hand off state, data, or control to each other, confirm the contract actually matches on both sides as merged, not as separately assumed while each was implemented alone.
4. **Run the project's integration/E2E suite** against the assembled base branch, not any single ticket's own isolated test run.
5. **Re-check acceptance criteria no single ticket explicitly claimed** - anything in the spec implicitly assumed to fall out of composition.
6. **Check for cross-ticket regressions** - re-verify earlier tickets' acceptance criteria now that later tickets have landed on top of them.
7. **Repeat the flows on production,** with the feature flag on for a test account when the feature is flagged, and read the latest `@smoke` E2E run on production (`../ns-route/references/e2e.md` "Reading a run"). A step that would change real data runs only with a test account the user named.

## Output

Two tables:

- Spec item (flow or AC) | Verified how | Verdict (PASS / GAP / REGRESSION).
- Seam | Tickets involved | Contract checked | Verdict (PASS / GAP / REGRESSION).

- **All PASS**: say so in one line, then the feature end: when the feature is behind a flag, turning it on for everyone is its own stop (`/ns-to-deploy` for the flag change, then `/ns-to-observe`); then `/ns-to-stakeholder-brief release <slug>` writes one Shipped report for the whole feature, its own stop.
- **Any GAP or REGRESSION**: stop and ask via the multiple-choice question tool, per finding:
  - **File an integration-fix ticket (Recommended for anything non-trivial)** - `/ns-to-tickets` (or `/ns-to-split-ticket` if it is a slice of an existing one), then deliver it through `/ns-flow-ticket` like any other ticket.
  - **Fix inline now** - only for an obviously small, well-scoped fix; still runs through `/ns-to-scope-check` -> `/ns-to-implement` -> `/ns-to-review` -> `/ns-to-quality-check` -> `/ns-to-save` -> `/ns-to-pr`, one file per approval as always.
  - **The spec itself was wrong or incomplete** - escalate to `/ns-to-spec` to correct it before deciding on a fix. Do not silently reinterpret the spec to match what shipped.

Do not turn the feature on for everyone, or write the feature's Shipped report, until every GAP and REGRESSION is resolved, or explicitly accepted by the user with a stated reason.

## Do not

Do not re-review each ticket's own diff - that already happened in `/ns-to-review`. Do not implement a fix without going through one of the three paths above. Do not merge or deploy from here.
