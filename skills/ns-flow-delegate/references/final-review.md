# Final review, per PR

```markdown
### Ready for review · 03 Archive a note · PR #482

**Preview** https://app-git-feat-03.vercel.app · **92 / 100** 🟢 · 3 / 3 criteria · 6 files, +142 −8

#### Decided without you (3)
| # | Decision | Picked | Instead of |
|---|---|---|---|
| 1 | how "archived" is stored | `archivedAt` timestamp | a separate table |
| 2 | where the owner check lives | the server action | middleware |
| 3 | quality-check | skipped stage 9 | no migrations in the diff |

**Needs you** criterion 3 has a manual check, 30 seconds on the preview
```

The table comes from the ticket's `## Decisions` entries marked `decided by agent`. Ask via the multiple-choice question tool: walk me through the decisions, challenge one, merge and ship, I will review it first, request changes, redo another way, take over by hand, or undo everything.

- **Walk me through:** each decision with its options, tradeoffs, and a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box").
- **Merge and ship:** continue from this session as `/ns-flow-ticket` phases 11 to 16: rollback prepare when needed, the release card in `/ns-to-deploy` (its own stop, the merge), verify production, observe, the Shipped comment, and close.
- **Request changes:** the same agent applies them on the same branch and proves them again.
- **Redo another way:** a new agent builds the design the first one rejected, on a fresh branch. The first PR stays open for comparison.
- **Take over by hand:** give the user the worktree path and branch, stop the agent, leave everything as it is.
- **Undo everything:** list exactly what will be removed (the PR, the branches, the worktree), check for work that exists nowhere else, and get a second explicit yes. Remove only what this run created, by the ids in `progress.md`.

**Editor diffs.** To read an agent's changes as diffs, open its worktree in VS Code (`code <worktree-path>`), one window per worktree.
