---
name: ns-to-verify
description: Prove a change the way a person would check it - full proof on local, a smoke check on preview and production, with a score and an evidence page. Also records a baseline before re-engineering and sets up the project verification skill.
disable-model-invocation: true
argument-hint: "[local | preview | production | baseline | setup] [ticket, PR, or URL]"
---

# ns-to-verify

Answers one question: does the change do what the ticket says, on a real screen or a real request? It writes tests and evidence, never production code. A check that exposes a bug is reported, and the fix goes back to `/ns-to-implement`.

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-proof.md`, `../ns-route/references/topic-kept-tests.md`, `../ns-route/references/topic-reading-ci.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/profile.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Read the project profile (`../ns-route/references/profile.md`) for the URLs, the env file, and the E2E command.

## Target

| Argument, or the situation | Run |
|---|---|
| `local`, or work with no PR | the full proof |
| `preview`, or an open PR with a preview | the smoke check |
| `production`, or a merged and deployed PR | the smoke check |
| `baseline` | read `references/refactor.md` and record today's behavior |
| `setup` | read `references/setup.md` and create the project verification skill |

Preview and production get the full proof instead of the smoke check when `/ns-route` scored the risk high or critical, or when the change depends on the environment (env vars, host config, caching, auth callbacks, cron).

## Before any run

1. **The project verification skill.** Read `.claude/skills/verify-<app>/SKILL.md`: it says how to launch the app, check it is healthy, drive it, capture evidence, clean up, and which env variables hold the secrets. None exists: offer `setup` (Recommended), or continue by working those out once and saying what was assumed.
2. **The proof plan.** Use `/ns-to-implement`'s verification plan: one row per acceptance criterion, plus scope-check's regression checks and abuse cases. None: build one row per criterion and get it approved.
3. **The environment.** Every name the app and the E2E suite read is present in the local env file (`../ns-route/references/e2e.md` "Local env"). One is missing: stop and fix it. A run with tests skipped is never started.
4. **Ask how to run it** (`../ns-route/references/topic-proof.md` "Proof"; on autopilot the mode chosen at setup applies): automatic, watched (Recommended) · automatic, hidden · manual · skip.
   - **Manual:** the user starts the app and checks it themselves. Give a numbered checklist (each criterion's steps in the ticket's words, the states and breakpoints to look at, the console to watch) and wait for their report. Record it as the proof. Parts of the score that only automation measures are left out and rescaled.
   - **Skip:** record that this target was not proven, and why. Nothing continues as if it had passed.

## The full proof

1. **Kept tests.** Every test the plan names exists (`../ns-route/references/topic-kept-tests.md` "Kept tests"). One is missing: write it, following the repo's test conventions and helpers, and tag each one that is safe on production `@smoke`. Where it is cheap, confirm each new test fails when the behavior is broken.
2. **Launch and check health** as the verification skill says. Start only what you will also stop.
3. **Walk every criterion** the way a user would, in the ticket's order, at a pace a person can follow. Print a step line as each thing happens:

   ```
   ▶ goal 1 of 3   Archive a note from the menu
     ✓ opened /notes
     ✓ clicked ⋯ > Archive
     ✓ saw "Note archived", back on the list
   ```

   Screenshot the state that proves the criterion, not the page after load.
4. **Capture the evidence** the table below calls for.
5. **Criteria with no screen** are proven by a real request, test output, or measured numbers. Read the reference the diff calls for: `references/api.md`, `references/data.md`, `references/infra.md`, `references/refactor.md`.
6. **Run the E2E suite** against the local build, and the existing tests for the touched area. A skipped test counts as not run: fix its cause and run again.
7. **Check each remaining risk** scope-check named, and each abuse case.
8. **Clean up** what you started. Evidence stays.
9. **Result:** write the result file and the evidence page (`references/evidence.md`), open the page, and print the result card.

Be picky. Something that looks off on screen is reported even when it is outside this ticket.

## Evidence

Read `references/capture.md` and follow it.

## The smoke check

Read `references/smoke-check.md` and follow it when the Target table above calls for the smoke check.

## The result card

Read `references/result-card.md` and follow it.

## Publishing

Read `references/publishing.md` and follow it.

## Finish

Add only what the card does not show: tests added with their run command, and anything found outside the ticket.

NEXT  after `local`: `/ns-to-understand`. After `preview`: back to `/ns-to-pr`. After `production`: `/ns-to-observe`. FAILED on any target: `/ns-to-implement`; on production, `/ns-to-observe` decides what happens next.
