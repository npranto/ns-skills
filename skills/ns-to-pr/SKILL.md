---
name: ns-to-pr
description: Push the branch, open (or continue) the pull request, run the preview check, and put every report on the PR - the description, the local and preview proof with the evidence page, and the stakeholder review. Never merges.
disable-model-invocation: true
argument-hint: "[ticket or base branch]"
---

# ns-to-pr

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-reading-ci.md`, `../ns-route/references/pr-writing.md`, `../ns-route/references/topic-proof.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Read `../ns-route/references/pr-writing.md` and the project profile (`docs/agents/workflow.md`) for how previews are found.

A PR opened here lets a reviewer have everything without asking: what changed, where to try it, proof it works, how risky it is, and how to undo it.

## Steps

1. **Preconditions.** Stop and say so if any fails: work committed (`/ns-to-save`), not on the default branch, a remote exists, no merge or rebase in progress. If `/ns-to-verify local` or `/ns-to-quality-check` did not run for this commit, ask whether to run it first. Ask which ticket/spec this PR closes if unclear.
2. **Sync with base.** Fetch, then report how far behind the base the branch is. If behind, ask whether to rebase or merge (conflicts: `mattpocock-skills:resolving-merge-conflicts` if the plugin has it, else plain git with each resolution approved). Re-run the fast checks (types, unit) if the sync changed anything. Never force-push without explicit confirmation (rebasing an already pushed branch needs `--force-with-lease`).
3. **Title and version.** Title `NN - Ticket title`. With versioning (the profile says so, or `.github/workflows/release.yml` exists), read `../ns-to-deploy/references/versioning.md`: recommend the bump marker for the title ("The bump") and add the bump commit ("The bump commit") before the first push.
4. **Stop, then open.** Show the title, what will be pushed, and the report set this PR will carry (the table in `pr-writing.md`). Say that this approval also covers those reports. Ask via the multiple-choice question tool: push and open the PR (Recommended), change the title, show me each report first, or not yet. Then `git push -u origin <branch>` and create the PR with `gh-axi`. Its first description is the ticket region (`references/description.md`) with one line under it: "Preview check running". An existing PR for this branch is found and continued, never duplicated.
5. **The local proof.** Publish the evidence page and post the local verification comment from the result file (`../ns-to-verify/SKILL.md` "Publishing").
6. **CI.** Wait for the checks on the head commit and report them per `../ns-route/references/topic-reading-ci.md` "Reading CI". A failed check stops here: its error lines go back to `/ns-to-implement`. The E2E run starts only once the preview is ready, so step 8 reads it.
7. **Preview.** Find the preview URL the way the profile says and wait until it is ready. The build fails: read the log, report the error, stop. The project has no previews: say so, post the preview comment saying `not available` and why, and skip step 8.
8. **Preview check.** Read `../ns-to-verify/SKILL.md` and run it with target `preview`. It waits for the E2E run on the preview and posts the preview comment. A FAILED check stops here.
9. **The review region.** Read `references/description.md` and add the region to the description, under the ticket region, folding in `.verification/<branch>/review.md` and `quality-check.md`. Print it in chat.
10. **Stakeholder review.** Read `../ns-to-stakeholder-brief/SKILL.md` and run it with mode `review`.
11. **Check the PR** against the table in `pr-writing.md`: both description regions, the local and preview comments, the stakeholder review, and an evidence link that opens. Post what is missing.

A PR with nothing to prove (docs or planning files only) runs steps 1 to 4, 6, and 9. Its description is the whole report.

## Finish

Never merge. Report the PR URL, the preview URL, the evidence page, the CI result, the score and verdict from the preview check, and what is on the PR. Suggest `/ns-to-deploy <PR>`.
