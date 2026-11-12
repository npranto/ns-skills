---
name: ns-to-review
description: Independent code review of the current changes in thirteen parts, with reviewers scaled by risk, and each finding carrying file:line evidence, a concrete failure scenario, and a fix.
disable-model-invocation: true
argument-hint: "[base ref, ticket, or PR number]"
---

# ns-to-review

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-kept-tests.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

A code review, read the way a senior engineer reviews a colleague's PR: to make the code correct, readable, and cheap to change. Ask for the base ref and ticket/spec if not obvious. Review the diff and the code it touches. Reviewers are read-only: they report, and fixes go through `/ns-to-implement`.

## Who reviews

Scaled by the Risk score from `/ns-route` (or the ticket, or the flow that called this). The implementing agent must not be the only reviewer of substantial work.

| Risk | Reviewers | Parts |
|---|---|---|
| low | the main session, one pass | every part the diff touches |
| medium, or no risk score known | one fresh subagent that sees only the diff, the ticket, and the repo | every part that applies |
| high or critical | three fresh subagents, splitting the parts (A, B, H · C, I, J, L · D, E, F, G, K, M), plus the `security-review` skill | all thirteen |

"Run the full review" (three reviewers, all parts) is always available on request. `mattpocock-skills:code-review` can supply parts A and D.

## The thirteen parts

Report each separately; never merge them into one score. A part with nothing to look at is "n/a" with the reason. A finding that fits two parts goes in the more specific one.

- **A. Spec compliance.** Every acceptance criterion satisfied, and nothing beyond them.
- **B. Bugs.** Wrong logic, null paths, boundaries, races, stale state, lost updates, missing error handling, retries, broken loading or responsive states.
- **C. Security.** Each abuse case from `/ns-to-scope-check` is really stopped. Authorization on the server on every path, input validation, injection, leaks in responses or logs, secrets or PII in code or logs, unsafe redirects, rate limits on abusable endpoints, least privilege.
- **D. Repo standards.** This codebase's conventions, ADRs, `CONTEXT.md` vocabulary, the framework's documented patterns, typing with no `any` hiding a real type. Where `docs/architecture/system.md` defines an observability approach, a new critical path or failure mode has the logs, metrics, or events it calls for.
- **E. Performance.** N+1 queries, missing indexes the query pattern justifies, unbounded lists, repeated work, needless client JavaScript, hydration issues, caching that can serve stale or another user's data.
- **F. Simplicity.** Could it be materially simpler without reducing correctness or maintainability? Speculative abstraction, indirection, dead code, duplication, unclear names, comments that restate the code.
- **G. Maintainability.** Hidden coupling, a crossed boundary, an unwritten contract, behavior that only works at today's scale, a TODO with no ticket.
- **H. Tests.** Every user-facing criterion has its kept test (`../ns-route/references/topic-kept-tests.md` "Kept tests"). Tests assert behavior through public interfaces and would fail if it broke. Nothing weakened, skipped, or deleted to pass.
- **I. Failure handling.** Every external call has a failure path and a timeout, with no silent catch. Partial failure leaves data consistent. Retried writes are idempotent. Errors are logged once, with context and no secrets.
- **J. Data and compatibility.** Schema changes are additive or expand and contract. Old code runs against the new schema. Public API shapes stay compatible or the break is called out.
- **K. Accessibility and UI states.** Only with UI: every state in the design contract exists, keyboard reachable with visible focus, labels, contrast, the layout holds with long text and with no data.
- **L. Dependencies and configuration.** Each new package is necessary, maintained, and compatibly licensed. New env vars are validated at startup and documented.
- **M. Reviewability.** One purpose, reviewable in about 15 minutes, no leftovers (debug output, commented-out code, stray files), and anything surprising has a comment or a PR note.

## Report

```markdown
### Review · 03 Archive a note · base `main` · 12 files, +310 −42

**Read** 12 of 12 files in full · reviewers: one fresh subagent (risk medium)

| Part | Result | Findings |
|---|---|---|
| A Spec compliance | pass | 0 |
| B Bugs | fail | 1 blocking |
| C Security | warn | 1 should fix |
| K Accessibility | n/a | no UI in the diff |

**Verdict: Request changes** · 1 blocking, 1 should fix

#### B1 blocking · The Archive button stays enabled during the request · `notes/NoteMenu.tsx:48`
**Fails when** a double click sends two requests; the second returns 404 and shows an error.
**Fix** disable it while pending; `useTransition` is already imported.
```

- Every part gets a row. **Read** names any file that was skimmed or skipped.
- Each finding has a severity (blocking, should fix, or nit), a `file:line`, **Fails when** with real inputs, and a **Fix** small enough to act on.
- A part that found nothing says so plainly. Findings are never invented to fill a part.
- End with a verdict: Approve, Approve with nits, or Request changes.

Use the host's structured findings report if it supports one. No findings: no stop. Otherwise ask via the multiple-choice question tool which findings to fix now: all blocking and should-fix (Recommended), blocking only, pick individually, or none. Do not fix without approval. A declined finding is recorded with the user's reason in the ticket's `## Decisions`.

## After the report

Save the report as `.verification/<branch>/review.md`, so `/ns-to-pr` can fold it into the PR description, and append one dated entry to the ticket's `## Comments`: the verdict and the finding counts. Update both after fixes.

After fixes are applied through `/ns-to-implement`, review the affected parts again, then suggest `/ns-to-quality-check` (the last gate before `/ns-to-save`). Reviewing a teammate's PR: fix nothing; ask which findings to post, and post them with `gh-axi` only after approval.
