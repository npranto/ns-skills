# Ship and clean up

## Several PRs

Ship one at a time, in dependency order. Before each: the PR is green and up to date with the moved base. A sync is the user's choice (rebase or merge, never force-push without confirmation); conflicts go through `mattpocock-skills:resolving-merge-conflicts` (if the plugin has it, else plain git) with each resolution approved. A sync that changed code re-runs the fast checks and the preview check. Retarget a stacked child after its parent merges.

When the tickets belong to one feature and the last has closed: the feature end ([FEATURE-END] in `../ns-route/references/workflows/shared-blocks.md`), starting with `/ns-to-integration-check`. Agents never saw each other's diffs, so this batch is the most likely to have cross-ticket seam gaps.

## Clean up

After a ticket has shipped or been undone, and on the user's yes: `herdr worktree remove --workspace <id>` and delete the local branch, after checking for unpushed work and offering any leftover stash. Only remove what this run created. End with one summary: what shipped, what is open, what was undone.
