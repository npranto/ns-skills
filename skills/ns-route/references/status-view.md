# Status view

Read-only. Work it out fresh every time from what is on disk and on the remote, never from memory of an earlier session:

- `git status --porcelain=v1 -b`, the current branch, and its last commit.
- Every `.scratch/*/progress.md`: the workflow, the run mode, and which phases are ticked.
- Ticket files under `.scratch/*/issues/`: `Status:` and `Blocked by:` for each.
- Open PRs and their check state (`gh-axi`).

Print:

```markdown
### Where you are · <repo>

**In flight** 04 Archive a note · branch `feat/04-archive-note` · ns-flow-ticket, step mode
**Done** branch, scope-check, implement, understand · **Now** review · **Left** quality-check, save, pr

| | |
|---|---|
| Uncommitted | 3 files changed since the last commit |
| Open PRs | #23 docs: close 01.02.04 (checks green, not merged) |
| Feature | notes-archive · 3 of 5 tickets done |

**Next** `/ns-flow-ticket .scratch/notes-archive/issues/04-archive-note.md`
**Or** merge PR #23 · start 05 About page (unblocked)
```

Name anything that could not be checked (no remote, `gh-axi` unavailable, no progress file) instead of filling the gap with a guess. Nothing in flight: say so and list the unblocked tickets.
