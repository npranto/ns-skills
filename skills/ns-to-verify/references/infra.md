# Proving a CI, platform, or infrastructure change

The proof for infrastructure is the plan, a run somewhere safe, and the undo, in that order.

## CI/CD pipelines (worked)

A workflow file only proves itself by running.

1. Push the change on a branch and read the run with `gh-axi`, per `../ns-route/references/topic-reading-ci.md` "Reading CI".
2. Prove it fails when it should: a job that guards something is shown red once, on a deliberate failure in a scratch commit, then green after it is removed. Say that this was done.
3. Check the trigger: the workflow ran on the event it claims (`pull_request`, a push to the production branch, a schedule), and did not run where it should not.
4. Check the cost: the wall time of the PR run before and after.
5. Least privilege: `permissions` names only what the job needs, and no secret reaches a job triggered from a fork.

**Worked example.** Ticket: "Run E2E tests against the preview on every PR."

```
PR #51 run 1   e2e (preview)  ✅ passed  2 m 31 s   triggered by deployment_status
PR #51 run 2   e2e (preview)  ❌ failed  1 m 02 s   scratch commit: broken selector  (proves it catches)
PR #51 run 3   e2e (preview)  ✅ passed  2 m 29 s   scratch commit reverted
PR wall time   6 m 10 s -> 8 m 40 s
```

## Platform config (worked)

Env vars, domains, redirects, cron, headers, on a host like Vercel.

| Change | Proof |
|---|---|
| A new env var | present in every environment that needs it (list them by name; never print a value), validated at startup, in the env example |
| A redirect or rewrite | the old URL returns the expected status and `Location`, on the preview |
| A header or caching rule | the response headers, read from a real request, on the preview |
| A cron job | the handler run once by hand with the same auth the scheduler uses; the schedule read back from the host |
| A domain | DNS resolves, the certificate is valid, both the bare and `www` forms answer |

**Worked example.** Ticket: "Wire `DATABASE_URL` into the deploy config."

```
vercel env ls        DATABASE_URL   production, preview, development   ✓ (values not shown)
preview build log    ✓ env validated: DATABASE_URL
GET /api/health      -> 200  {"db":"ok"}      on the preview
```

Human-only steps (creating a token, pasting a secret into a dashboard) go through `mattpocock-skills:wizard`. Never ask for a secret in chat.

## Infrastructure as code (checklist)

- Read the plan or diff before anything is applied, and show its summary: what is created, changed, and destroyed.
- Any destroy or replace is a one-way door until proven otherwise: its own stop.
- Apply to a non-production environment first.
- State the undo: the previous state, and how to return to it.
- Check for drift before and after.
- Secrets are created by the user.

## Containers (checklist)

- The image builds from a clean checkout and runs locally.
- The health check answers, and fails when the app is unhealthy.
- The rollout strategy and the command that rolls back are stated and tried once.
- The image runs as a non-root user and carries no secret.
