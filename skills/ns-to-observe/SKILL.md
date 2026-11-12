---
name: ns-to-observe
description: Confirm a release is actually healthy in production - deployment is not completion. Reads the real logs first, runs checks staged by risk (low, medium, high), and ends with an explicit HEALTHY/UNHEALTHY verdict, offering a mitigate-first decision when it is not healthy.
disable-model-invocation: true
argument-hint: "[production URL, release risk, or deploy summary]"
---

# ns-to-observe

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-proof.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-delivery.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Deployment is not completion. The production check showed the acceptance criteria pass; this phase asks the next question: is anything failing quietly that a walk through the UI would not show?

## Gather

Reuse what this session already knows: the production URL, the deployment and commit, what shipped, the `/ns-to-verify production` result with its smoke E2E run, the PR's undo block, the release card's monitoring notes, and the risk from `/ns-route`. Read the project profile's **Logs** and **Fastest undo** lines. Ask via the multiple-choice question tool for whatever is missing. The production check has not run for this deployment: run it first.

## Logs first, every tier

Read the real logs for this deployment, the way the profile's **Logs** line says. On Vercel: the MCP tools (`get_runtime_errors`, `get_runtime_logs`, `list_deployment_events`) or `vercel logs`, scoped to this project, this deployment, and the time since it went live.

| Signal | Why it matters |
|---|---|
| Error signatures that are new since the deploy | an error that did not exist before is this release's until shown otherwise |
| 5xx responses and function failures on changed routes | it works for you and fails for some inputs |
| Timeouts, memory limits, cold-start spikes | degraded, not down |
| Unhandled rejections and swallowed exceptions | caught-and-ignored errors hiding broken behavior |
| Client and hydration errors reported to the server | the page renders and is broken for some browsers |
| Middleware, cron, queue, and webhook failures | paths no browser walk touches |
| New build warnings | a missing env var that only shows up later |
| Whether the changed routes got any requests | no traffic means the logs prove nothing yet: say so |

Report each as a row: the count, the count in the same window before the deploy, and one example line. A new error on a changed route is a finding at one occurrence.

## Risk determines depth

Each tier adds to the one below.

| Tier | Checks |
|---|---|
| Low | The log scan. Production URL loads. The production check passed. Browser and server console are clean. |
| Medium | + Error rate vs. the pre-deploy baseline. Analytics/product events firing correctly. Response times against the preview's. The release's critical user flows, end to end. |
| High | + Latency percentiles (p50/p95/p99). Error budget consumption. Business KPI impact. Database health (connections, replication lag, slow queries). Migration validation (row counts, data integrity spot checks). Security signals (auth failures, anomalous access patterns). A defined observation window. An explicit rollback threshold, agreed before observing. |

For High risk, before observing: if not already set by `/ns-to-deploy` or `/ns-to-rollback`, ask via the multiple-choice question tool for the observation window and the rollback threshold. If that threshold is crossed at any point, stop immediately and go straight to "Not healthy" below.

## The check plan

Before running anything beyond the log scan, print the tier's checks with a recommendation each and the reason, then ask once via the multiple-choice question tool: run my recommendation (Recommended), run all, choose one by one, or a custom list. On autopilot, take the recommendation.

Run the real check - curl or a real browser for page checks (only the tools in `../ns-route/references/topic-proof.md` "Proof"), the actual logs, metrics provider, or database - and report what was actually found. Never assume or fabricate a result; an unrun check is never a pass. For High risk, hold the observation window open: ask whether to poll at intervals or have the user watch and report back.

End with a table: check, result (pass / fail / skipped), evidence.

## Verdict

State explicitly, in writing: **HEALTHY** or **UNHEALTHY**, with the reasoning tied to the checks (or the rollback threshold, for High risk). HEALTHY needs both the log scan and the production check passing against the real production URL. Always name what the evidence does not cover (for example, a weekly job that has not run yet). Add one production-health line under the score from `/ns-to-verify`; compute no second number.

- **HEALTHY:** next is `/ns-to-stakeholder-brief release` (the Shipped comment), then for an incident `/ns-to-postmortem`, then `/ns-to-close`.
- **UNHEALTHY:** "Not healthy" below.

## Not healthy: mitigate first

Read `references/not-healthy.md` and follow it when the verdict is UNHEALTHY or the rollback threshold is crossed.

## Do not

Do not execute a rollback yourself; hand off to `/ns-to-rollback`. Do not treat an unrun check as a pass.
