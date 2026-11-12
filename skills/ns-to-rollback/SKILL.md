---
name: ns-to-rollback
description: Prepare a rollback strategy before high-risk deployment, and execute it if a release turns out unhealthy. Preparation, not panic - deployment already knows what failure means before it ships.
disable-model-invocation: true
argument-hint: "[release scope, deploy summary, or 'execute' plus the failure evidence]"
---

# ns-to-rollback

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Rollback is preparation, not panic. Deciding how to undo something while production is broken is vastly worse than deciding it beforehand. This phase runs before `/ns-to-deploy` for high-risk releases, so deployment already knows what failure means, and again after `/ns-to-observe` reports UNHEALTHY, to execute the plan that already exists.

## Two modes

If not already clear from the invocation, ask via the multiple-choice question tool which mode applies: **Prepare** (before deploying, no failure yet) or **Execute** (a release has been marked UNHEALTHY and needs to come down).

### Prepare

Reuse what this session already knows: the release scope and the risk/reversibility/data-risk classification from `/ns-route`, `/ns-to-deploy`, or `/ns-to-architect`. Ask only for what's missing.

Answer each of the following concretely for this release - name the actual commit, flag, artifact, and command, not a generic description:

- **Revert commit?** Is the change a clean `git revert`, or does it depend on commits that shipped after it?
- **Feature flag?** Can the change be dark-launched or killed via a flag instead of a deploy?
- **Previous artifact?** Is the last-known-good build/image/artifact still available to redeploy, and where does it live?
- **DB backwards compatible?** Do old code with new schema, or new code with old schema, coexist during a rollback window? If not, the rollback needs its own ordering (expand/contract), not just a code revert.
- **Data restoration?** If data was migrated, mutated, or backfilled, how is it restored? Backup location, restore command, expected data-loss window.
- **Traffic switch?** Blue/green, canary, or load-balancer switch - is there a fast, mechanical way to move traffic back?

Any "no" or "unclear" answer is a gap. Either close it before shipping (add the flag, make the migration backwards compatible) or state it out loud as an accepted risk - never let it pass silently.

State the time each step takes. The target is production back on the previous behavior **within a minute, by a mechanical step** (an instant rollback to the previous deployment, a flag off), with the code revert after it. Slower than that, or needing judgment: say so plainly. Check the facts the plan rests on, not from memory: the previous deployment still exists (the profile's **Fastest undo** line says how), the migration is additive, the flag works. With versioning, read `../ns-to-deploy/references/versioning.md` "Rolling back to a version".

Produce a ROLLBACK PLAN and stop for its approval (accept the plan, close a gap first, or change the trigger):

```markdown
### ⏪ Rollback plan · #482 Archive a note

**Time to undo** under **1 min** · **Data to restore** none · **Gaps** 0
**Trigger** error rate on `/notes/*/archive` above **2%** for 5 minutes

| # | Do this | Who | Takes |
|:---:|---|---|:---:|
| 1 | Instant rollback to deployment `dpl_8fK2` | you | **30 s** |
| 2 | Revert PR #482 and merge the revert | agent | 5 min |

**Confirm it worked** the Archive item is gone from the note menu
**Checked** `dpl_8fK2` still exists · the migration is additive
```

The trigger reuses `/ns-to-observe`'s rollback threshold if one is already set. The plan goes onto `/ns-to-deploy`'s release card and into the PR as the undo block (`../ns-route/references/report-blocks.md` "Rollback block").

### Execute

Only after explicit go-ahead - never roll back without confirmation, per `../ns-route/references/core.md` "Safety rules". Reuse the ROLLBACK PLAN from Prepare mode (or the PR's undo block if Prepare did not run as its own step) and the evidence behind `/ns-to-observe`'s UNHEALTHY verdict.

Present the plan's steps and confirm the target state (what "rolled back" means for this release), then execute step by step, verifying after each one. With versioning, the Rollback workflow is the mechanical step: dry run first when in any doubt (`../ns-to-deploy/references/versioning.md`). Run the real check at each step - do not assume or fabricate a result, same standard as `/ns-to-observe`. Report pass/fail per step, with evidence.

Finish with the release's actual state - rolled back cleanly, partially rolled back, or rollback failed - and hand off:

- **Rolled back cleanly** - run `/ns-to-verify production` and `/ns-to-observe` again on the restored release to confirm the rollback itself is healthy. Then, each as its own approved action: revert the PR with `gh-axi` so the production branch matches what is deployed (otherwise the next merge ships the problem again), set the ticket's `Status:` back to `in-progress`, and write a follow-up ticket for the root cause through `/ns-to-tickets`. After an instant rollback, say that the host will not put new deployments live until one is promoted.
- **Partial or failed rollback** - this is now its own incident. Escalate and say so plainly; do not keep retrying silently.

## Do not

Do not execute a rollback without explicit user go-ahead, even when a rollback threshold has been breached - present the plan and confirm first. Do not skip a Prepare-mode question because the failure it covers seems unlikely; an unlikely gap is still a gap. Do not accept "we'll figure it out if it breaks" as an answer to any of the six questions - that is the panic this phase exists to prevent.
