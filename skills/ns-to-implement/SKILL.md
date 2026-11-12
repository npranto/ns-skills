---
name: ns-to-implement
description: Implement one ticket or bugfix one vertical slice at a time, optionally orchestrating isolated worker agents, with escalation instead of silent redesign.
disable-model-invocation: true
argument-hint: "<ticket path or id>"
---

# ns-to-implement

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-kept-tests.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Input: a ticket (ask if missing), plus the relevant spec sections, architecture, design, ADRs, `CONTEXT.md`, repo conventions, and testing expectations. If the ticket looks too big for one context, suggest `/ns-to-split-ticket` first. If `/ns-to-scope-check` has not already run against this ticket in this session, suggest it before writing any code. Confirm you are on a feature branch, not the default branch, and not mid-merge or rebase or detached HEAD (`/ns-to-branch` if not). When workers run in parallel, give each its own worktree via `/ns-to-branch --worktree`.

## Verification plan (proof obligation, before coding)

Before writing any code, map every acceptance criterion in the ticket to how it will be proven, using the type vocabulary and the rule in `../ns-route/references/topic-kept-tests.md` "Kept tests": an E2E test for each thing a user can see or do, an integration test for each rule with no screen. Add a row for each regression check and abuse case `/ns-to-scope-check` carried forward. This turns testing from something done after the fact into an obligation the implementation must satisfy.

For each row, note:

- **Verification type(s)** - what kind of test or check proves it.
- **Kept test** - the test file this phase writes for it, test-first where there is a cheap seam. A row with no kept test says why.

Present this as a short table and proceed; it is a planning step, not a separate approval gate. If an AC has no plausible verification type, escalate rather than implement it as written (see Escalation).

## Orchestration

Ask via the multiple-choice question tool whether to work inline or use agents. Per the user's global rule, never launch a large swarm (dynamic workflows, ultra-style features) without explaining tradeoffs and getting explicit approval. If using orchestration (Herdr, the harness's subagents, worktrees): the main session is CAPTAIN. Workers get isolated branches/worktrees and receive only the ticket, relevant spec sections, architecture, ADRs, conventions, testing expectations, and explicit constraints. Workers may inspect the repo, but must not reinterpret requirements or redesign architecture. Workers must not write code changes: they return proposed diffs or findings, and CAPTAIN applies each one via file-edit tool for the user to approve file by file.

## Escalation

If a settled decision is invalid, dangerous, contradictory, or impossible: STOP that part and return an ESCALATION with OBSERVATION, WHY CURRENT PLAN FAILS, OPTIONS, RECOMMENDATION, IMPACT. Architecture changes need human acceptance.

## Method

- Every code change goes through the user for approval, file by file, via file-edit tool. No scripts, `sed`/`perl`/`python` rewrites, codemods, `--fix`/`--write` flags, generators, or batch edits. See "Code change approval" in `../ns-route/references/core.md`. Run linters and formatters in check mode only and apply their fixes by hand as normal edits.
- One vertical slice at a time.
- Test-first at meaningful seams: use `mattpocock-skills:tdd`. Write every kept test the verification plan names. For bugs, reproduce first with `mattpocock-skills:diagnosing-bugs` (E2E as close to the real user experience as possible), and add a regression test.
- Run targeted tests, typecheck, and lint frequently.
- No unrelated cleanup, no speculative abstractions, cohesive changes - `/ns-to-scope-check` should have already trimmed these before this phase started; if something creeps in during coding anyway, cut it rather than letting it ride.
- Use existing design-system primitives and follow the design contract.
- Enforce server-side authorization, validate untrusted input, handle failure states.
- Never log or commit secrets or PII. Keep migrations backward compatible (expand/contract) and retried writes idempotent where the architecture calls for it.
- If `docs/architecture/system.md` defines an observability approach and this slice adds a new user-facing capability, critical path, or failure mode, add the logs, metrics, or events it calls for. Note what was added (or that nothing new was needed) in Finish, so `/ns-to-deploy`'s MONITORING AND ALERTS TO WATCH can reuse it instead of inventing it later.
- Follow the code quality principles below.
- Fix nearby lint or flaky-test problems you meet.

## Code quality principles

Prefer: simple, explicit, typed, testable, observable, accessible, secure, cohesive, boring, replaceable.

Avoid: premature abstractions, mega hooks, god components, generic utility dumping grounds, business logic in presentation components, implicit authorization, unchecked external input, unnecessary global state, clever metaprogramming, hidden side effects, large cross-cutting diffs, dependencies without clear value.

## Finish

Do not mark work accepted because tests pass: proving it on a real screen or request is `/ns-to-verify`'s job. Report what was done, evidence (commands and results), deviations, and open risks. Reconcile against the verification plan: each row with its kept test and that test's result, and any row without one with its reason - nothing should be silently unaccounted for. Report the observability note from "Method" alongside this. Suggest `/ns-to-verify local`.
