# E2E tests: one suite, three places

Read by `/ns-to-verify`, `/ns-to-quality-check`, and any phase that writes or sets up E2E tests. What gets a test is `../ns-route/references/topic-kept-tests.md` "Kept tests". The examples use Playwright, Vercel, and GitHub Actions; on another stack keep the rules and swap the tools.

## Where the suite runs

| Place | Runs | Started by | Base URL |
|---|---|---|---|
| Local | the whole suite | `/ns-to-verify local`, and quality-check stage 6 | the local production build the test config starts |
| Preview | the whole suite | CI, when the preview deployment succeeds | the deployment's own URL, from the event |
| Production | tests tagged `@smoke` | CI, when the production deployment succeeds | the production URL, from a repository variable |

CI never builds the app a second time to test it. The deployment is the thing under test, with its own environment.

## The test config

One config serves all three places. It:

- takes the base URL from `E2E_BASE_URL`, and starts the local build itself only when that is unset
- loads the local env file, so a local run sees the same names CI passes in
- sends the protection bypass to the deployment's own origin when `VERCEL_AUTOMATION_BYPASS_SECRET` is set (`../ns-to-verify/references/protected-previews.md`)
- fails, naming the variable, when one it needs is missing. A `test.skip` on a missing variable turns a broken setup into a green run.
- keeps screenshots and video on failure, and leaves tracing off wherever a secret is in play: a trace records request headers and every typed value

## Tags

- `@smoke` marks a test that is safe on production: it only reads, or it signs in as the dedicated test account and removes what it created, also when it fails halfway.
- The main path of every user-facing criterion carries `@smoke` when it can meet that bar. A test that cannot is proven on local and the preview only, and the production result says so.

## Local env

The local env file is git-ignored and named in the project profile (`.env.local` by default). `.env.example` is committed and lists every name the app and the suite read, with a comment and no value.

1. **The host is the source.** Keep every local value in the host's Development environment, test accounts included, so `vercel env pull .env.local` rebuilds the file. The pull rewrites the whole file: check by name afterward that the bypass secret is still there, and have the user put it back when it is not.
2. **Check before any run, by name only:** every name in `.env.example` is present in the local env file. Print the missing names, never a value.
3. **One is missing:** stop and fix it now. Adding a value is the user's step, through `mattpocock-skills:wizard`; a secret is never typed into chat.

## Where each secret lives

| Secret | Local | CI | The deployed app |
|---|---|---|---|
| App secrets (database, auth keys) | the local env file | not needed: CI tests a deployment | the host's environment variables |
| `VERCEL_AUTOMATION_BYPASS_SECRET` | the local env file | a GitHub Actions repository secret of the same name | set by Vercel itself |
| Preview test account | the local env file | GitHub Actions repository secrets | - |
| Production test account | nowhere, unless a production check needs it | GitHub Actions repository secrets under their own names (`E2E_PROD_...`) | - |

- The bypass secret is created in Vercel: Project > Settings > Deployment Protection > Protection Bypass for Automation. One secret opens every preview and production deployment of that project. Create one for CI and one for local use, so either can be revoked alone.
- Rotating it: regenerate in Vercel, update the GitHub secret and the local env file, then redeploy. Deployments built before the change stop accepting the old value.
- A secret never appears in a workflow file, a URL, a log, a trace, a report, a comment, or the evidence page.
- Public repository: keep the host's fork protection on. Authorizing a fork's deployment also lets its test code run with these secrets, so read the fork's diff first.

## The CI workflow

`.github/workflows/e2e.yml`, copied from `../ns-to-quality-check/workflows/e2e.yml` and adapted to the project's commands, shown first and written as an approved edit. Set it up in the walking skeleton, at onboarding, or the first time quality-check finds it missing on a project with UI.

- It listens for the `deployment_status` event the host's GitHub integration sends. The run uses the workflow and the tests of the deployed commit, and its check lands on that commit, so it shows on the PR with no extra wiring.
- **`E2E (preview)`** runs the whole suite. Recommend it as a required check on the production branch. Changing branch protection is the user's action.
- **`E2E (production)`** runs `@smoke` against the production URL, not the deployment's own URL, because logins and callbacks are bound to the real domain. Where the app exposes its commit, the first smoke test asserts it equals `E2E_EXPECT_COMMIT`, so a run that reached the previous release fails instead of passing by accident.
- It needs the secret `VERCEL_AUTOMATION_BYPASS_SECRET`, the variable `PRODUCTION_URL`, and the test-account secrets the suite reads. Creating them is the user's step, through `mattpocock-skills:wizard`.
- The project turned `deployment_status` events off in Vercel: trigger on `repository_dispatch` with `vercel.deployment.success` instead, read the URL from `github.event.client_payload.url`, check out `github.event.client_payload.git.sha`, and report with `vercel/repository-dispatch/actions/status@v1`. That form only runs once the file is on the default branch.

**Prove it** the first time, as `../ns-to-verify/references/infra.md` "CI/CD pipelines" says: green on a real preview, red once on a deliberate failure, green again, then green on production after the merge.

## Reading a run

- `/ns-to-verify preview` waits for `E2E (preview)` on the head commit. `/ns-to-verify production` waits for `E2E (production)` on the merge commit. Report it per `../ns-route/references/topic-reading-ci.md` "Reading CI".
- Red on the preview: the error lines go back to `/ns-to-implement`. Red on production: FAILED, and `/ns-to-observe` decides what happens next.
- A run that never started is a finding, not a pass. Say which event did not arrive.
- A flaky test is fixed, or quarantined with a ticket, the day it is seen. A retry that hides it is not a fix.
