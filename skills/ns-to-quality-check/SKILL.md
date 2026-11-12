---
name: ns-to-quality-check
description: Final staged quality gate before commit and PR (types, lint, format, tests, build, security, a11y, performance, docs, hygiene), shown first as a plan with a recommendation per stage that you confirm, then run one stage at a time. Also makes sure CI enforces types, lint, tests, and build on every PR.
disable-model-invocation: true
argument-hint: "[run | setup-ci | both]"
---

# ns-to-quality-check

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-staged-checks.md`, `../ns-route/references/topic-reading-ci.md`, `../ns-route/references/topic-kept-tests.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

The last gate before the final commit. It assumes `/ns-to-verify local` and `/ns-to-review` already ran: it confirms review findings were actually fixed rather than re-auditing code quality. Default is `both`: make sure CI enforces the core checks, then run the stages. `run` and `setup-ci` do one half.

## Detect first

Read `references/stages.md` for the stage list and follow it.

Read `package.json` scripts (or the stack's equivalent), `.github/workflows/`, and lint/format/test/build configs. Reuse what exists. Do not add tools without clear value. For each stage below work out: does its command exist (**available**, **missing**, or **not applicable**), and does it have anything to look at in this diff.

## CI enforces the core four

**Types, lint, tests, and build** run in CI on every pull request. Check the workflows on every run, not only in `setup-ci` mode.

- **All four run on PRs:** say so in one line.
- **CI is missing, or lacks one of the four:** propose the smallest change as a GitHub Actions workflow (`.github/workflows/quality.yml`, triggered on `pull_request`, with caching, least-privilege permissions, and a timeout per job), show it, and write it as an approved edit. Note any secrets or services a job needs (a test database, for example) and hand human-only steps to `mattpocock-skills:wizard`. If the user declines, record it as an accepted risk with their reason, in this phase's summary and later in the PR description.
- **A core check has no local command** (no linter, no tests): say so and propose the smallest standard setup. A check that cannot run is reported as missing, never as passed.
- **No git remote yet:** write the workflow anyway, so it runs from the first push. Do not push.
- **A project with UI and no E2E workflow,** or one that runs the suite only against a build made inside CI: offer to set it up now. Read `../ns-route/references/e2e.md`, show the proposed `.github/workflows/e2e.yml` (from `../ns-to-quality-check/workflows/e2e.yml`), and write it as an approved edit. The first run must be proven as that file says.

In `setup-ci` mode, also ask which other available stages should run in CI (one question per stage, recommended answer first); agent-driven audits (a11y, bug investigation) can be CI jobs or left to `/ns-to-review`.

Recommend marking the core jobs as required status checks on the default branch; changing branch protection is the user's action.

## The stage plan

Before anything runs, print every stage with a recommendation and the real reason from this diff, in six words or fewer:

```markdown
### Quality check · `feat/03-archive-note` · 15 stages

I recommend running **11** and skipping **4**. Nothing runs or is skipped until you confirm.

| # | Stage | I recommend | Why | Command |
|---|---|---|---|---|
| 1 | Types | run | always | `pnpm typecheck` |
| 9 | Migration safety | skip | no migrations in the diff | - |
| 11 | Performance | run | a new client component | `pnpm build --analyze` |
```

- Every stage has a row, in order. Core stages (types, lint, format, unit tests, build) are always recommended to run. Recommend skip only when there is clearly nothing to look at, or the check was already proven on this exact commit.
- A stage the workflow makes mandatory (migration safety in a migration, dependencies and secrets for a dependency change, the fast set for an incident) is recommended to run with the reason `required by <workflow>`.
- Missing stages show what the smallest setup would be.

Then ask once via the multiple-choice question tool: run my recommendation (Recommended), run everything available, choose one by one, core only, or a custom list.

- **Choose one by one:** one question per stage, in order, Run or Skip, recommended answer first.
- Skipping a core or mandatory stage is allowed when the user asks. Record their reason.
- On autopilot, take "run my recommendation" (`../ns-route/references/core.md` "Run modes").

## Run, one at a time

Strictly in order. Never two at once, never several in one command, never several reported together. Each stage gets its own result as it finishes: the exact command, the result with real output, and any failure stated plainly.

Never use `--fix` or `--write`; run linters and formatters in check mode and propose the fixes as normal file-edit tool changes the user approves file by file. On a failure, show the first real error lines and the file, deal with it before the next stage, and re-run that stage after the fix. Fix failures and flakiness you encounter even when unrelated to the current work, or ask if the fix is large.

Read `references/stages.md` for the stage list and follow it.

## Finish

End with a table: stage, result (pass, fail, skipped, missing), and command. List skipped and missing stages explicitly, and say where the user's choice differed from the recommendation, so nothing is silently unchecked. Add one line on CI: the core four enforced, a workflow added in this run, or the accepted risk. When this run changed a CI workflow on a pushed branch, read the new run per `../ns-route/references/topic-reading-ci.md` "Reading CI".

Save the summary as `.verification/<branch>/quality-check.md`, so `/ns-to-pr` can fold it into the PR description, and append one dated entry to the ticket's `## Comments`: the verdict and the counts. Suggest `/ns-to-save`, then `/ns-to-pr`.
