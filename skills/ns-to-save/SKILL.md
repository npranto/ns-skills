---
name: ns-to-save
description: Stage all local changes and commit them to the current branch with a Conventional Commits message derived from the diff. Never pushes.
disable-model-invocation: true
---

# ns-to-save

Read first: `../ns-route/references/core.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Save local work to the **current branch**. Never push.

## Steps

1. `git status` and `git diff` (staged and unstaged, plus untracked files). If nothing changed, say so and stop. If on the default branch with substantial work, warn and ask whether to run `/ns-to-branch` first (it can carry the uncommitted changes onto the new branch).
2. Scan for files that should not be committed (secrets, `.env`, large binaries, build output, anything under `.verification/`). Warn and ask before including them.
3. Add all changes.
4. Write the best commit message from the diff: Conventional Commits (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `build`, `ci`) with an optional scope, imperative subject under about 72 characters, and a body when the why is non-obvious. Split into multiple commits only if the diff clearly contains unrelated concerns, and ask first. No agent co-author trailer.
5. Commit and show the resulting `git log -1 --stat`.

## On any unexpected git or terminal issue

Tell the user immediately with the exact output, and offer to revert everything done in this task (`git reset --soft HEAD~1` for a commit made here, `git restore --staged .` for staging). Do not revert without confirmation.
