---
name: ns-to-deploy
description: Ship a reviewed PR - preflight checks, one release card whose answer is the merge, and confirmation that production is live on the right commit. Also sets up optional versioning, where each PR carries its own version bump.
disable-model-invocation: true
argument-hint: "[PR number or branch | release scope | setup-versioning]"
---

# ns-to-deploy

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-reading-ci.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/profile.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Read the project profile (`docs/agents/workflow.md`) for the production branch, how this project deploys, and the fastest undo. Missing: say so and ask (`../ns-route/references/profile.md` "When it is missing").

`setup-versioning`: read `references/versioning.md` and run its "Setup". It is optional and only done on the user's yes.

## 1. Gather

Reuse what the PR holds: the score and verdict, the preview check, the undo block, flags, migrations, env changes, and the risk from `/ns-route` or the ticket. A project with versioning: read `references/versioning.md` "At release". Ask only for what is on neither the PR nor the profile.

## 2. Preflight

Stop and report when one fails:

- The preview check passed for the current head commit. PARTIAL needs the user to accept the open rows.
- CI is green on the head commit and the PR is up to date with the base (`../ns-route/references/topic-reading-ci.md` "Reading CI"). A failed, running, or missing required check fails this. On a project with UI, the E2E run on the preview is one of those checks.
- **The PR carries its reports so far** (`../ns-route/references/pr-writing.md`): both description regions, the local and preview verification comments, the stakeholder review, and an evidence link that opens. One is missing: post it now.
- No blocking review finding is open.
- The undo steps in the PR are concrete and were checked.
- **With versioning:** the version in `package.json` is still the next one (`references/versioning.md` "The bump commit", step 4).
- **High or critical risk, a migration, or an incident:** `/ns-to-rollback` Prepare has run.

## 3. The release card

```markdown
### Release · 03 Archive a note · PR #482

| CI | E2E on preview | Preview check | Score | Risk | Undo |
|:-:|:-:|:-:|:-:|:-:|:-:|
| ✅ 5 passed | ✅ 4 / 4 | ✅ 3 / 3 | **92** 🟢 | medium | revert, **< 5 min** |

**Ships** the archive action and the Archived page
**How** a merge to `main` deploys to production (Vercel)
**Migrations and env** 1 additive migration · no new env vars
**Flags** none
**On the PR** local proof · preview proof · stakeholder review · evidence page
**After the merge** the smoke E2E run on production, the production check, observe, then the Shipped comment
```

- **Version**, with versioning: `v1.4.2 → v1.5.0 · minor, from the title "[MINOR] Archive a note" · package.json says 1.5.0 ✅`.
- **High or critical risk, a migration, or several PRs at once:** the card also carries the full release plan: RELEASE SUMMARY, FEATURES INCLUDED, FEATURES EXCLUDED, MIGRATIONS (ordering and reversibility), ENVIRONMENT CHANGES, DEPLOYMENT STEPS in order, FEATURE FLAGS, BACKUP/RESTORE READINESS, MONITORING AND ALERTS TO WATCH, the ROLLBACK PLAN from `/ns-to-rollback`, KNOWN LIMITATIONS, FOLLOW-UP TICKETS.
- **Monitoring:** reuse the observability notes `/ns-to-implement` and `/ns-to-review` recorded. A new critical path with no log, metric, or event to watch is a gap: say so on the card and ask whether to add it now or accept the risk with a reason.

**Stop.** The release card is one stop, and the answer "merge and ship" is the authorization to merge. Ask via the multiple-choice question tool: merge and ship, leave the PR open, request changes, prepare a rollback plan first, or discard.

- **Leave the PR open:** stop here. Rerunning the command continues from this card.
- **Request changes:** back to `/ns-to-implement` on the same branch.
- **Discard:** list exactly what will be deleted (the PR, the remote branch, the local branch, the worktree), get a second explicit yes, then do it.

## 4. Execute

Only after "merge and ship":

1. Env changes and expand-phase migrations first, in the card's order. Human-only steps (dashboards, secrets, DNS) go through `mattpocock-skills:wizard`.
2. Squash-merge the PR with `gh-axi` (or the repo's documented merge method).
3. **A host where merging does not deploy:** promoting is its own stop, after the merge build is ready.
4. Wait for the production deployment and confirm it: status ready, and the deployed commit is the merge commit. Read the build log for new warnings. The smoke E2E run on production starts by itself once the deployment succeeds; `/ns-to-verify production` reads it.
5. With versioning: confirm the Release run (`references/versioning.md` "At release").
6. Note the undo target: the previous production deployment, and with versioning the previous version.
7. **A flag change** (turning a feature on) is its own stop.

The build or deployment fails: production is still on the previous release. Report the error and stop. Production is serving a broken build: go to `/ns-to-observe`, which opens with the mitigate-first decision.

## Finish

Report the production URL, the deployment, the commit, the previous deployment, and the flag state. With versioning, the new version with its release link. Suggest `/ns-to-verify production`.
