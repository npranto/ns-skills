---
name: ns-to-branch
description: Start work on a clean, well-named git branch (or worktree) for a ticket, issue, or description - safe base choice, stacked-branch awareness, local changes handled without loss, and a launch banner.
disable-model-invocation: true
argument-hint: "<ticket path, id, or description> [--worktree]"
---

# ns-to-branch

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Goal: a safe, fast, reusable start to any unit of work on any repo. Never lose work, never surprise the user, never push.

## 1. Preflight (read-only, no questions yet)

Run and read: `git rev-parse --is-inside-work-tree`, `git status --porcelain=v1 -b`, `git branch --show-current`, `git remote -v`, `git worktree list`, and check for an in-progress operation (`.git/MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `BISECT_LOG`).

Stop and explain, offering the fix, when:

- **Not a git repo**: offer `git init` (ask first), otherwise stop.
- **Merge, rebase, cherry-pick, or bisect in progress**: do not branch. Offer `mattpocock-skills:resolving-merge-conflicts` or the abort command, and let the user choose.
- **Detached HEAD**: say so, and treat the base as an explicit choice in step 4.
- **No commits yet**: an unborn branch cannot be a base. Ask whether to create an initial commit first.

Note the facts: default branch (from `git symbolic-ref refs/remotes/origin/HEAD`, else `main` or `master`), whether a remote exists, submodules present, and whether the current branch is already a feature branch.

## 2. Need context

If no ticket, issue, or description is provided (argument or an obvious ticket file), take no action. Tell the user more context is needed and ask for it. Accept: a ticket path (`.scratch/<slug>/issues/NN-slug.md`), a tracker id or URL (read it, for example via `gh-axi`), or free text.

Read the ticket when there is one: its title, type, id, and `Blocked by:` line.

## 3. Name

Format: `<type>/<id>-<slug>`.

- **type**: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `ci`, `hotfix`. Infer from the ticket (bug means `fix`, docs-only means `docs`); ask only if ambiguous.
- **id**: ticket number as written (`03`, `03.02` for sub-tickets, `PROJ-123`, `#456`). Omit when there is none.
- **slug**: lowercase kebab-case, ASCII only, 3 to 5 words, at most about 50 characters total, no trailing dashes, and no characters git rejects. Strip filler words.

Follow the repo's existing convention when it differs: look at `git branch -a` history, `CONTRIBUTING`, and any prefix such as a username or tracker key. Collisions: if the name already exists locally or on the remote, do not overwrite. Ask whether to switch to it, reuse it after a status check, or pick a suffixed name.

Confirm the final name with the user (recommended name first via the multiple-choice question tool).

## 4. Base

Ask via the multiple-choice question tool only when the answer is not obvious. Options:

- **Default branch** (recommended when on the default branch or on a merged/unrelated branch).
- **Current branch** (when the work builds on it).
- **Dependency branch (stacked)**: when the ticket's `Blocked by:` points to a ticket whose branch is not yet merged. Find its branch by name pattern, and confirm. Warn that the stack must be rebased or retargeted as parents merge, and suggest `gh-axi` stacked-PR support if in use.
- **A specific ref**: tag, commit, or release branch for hotfixes and backports (name the type `hotfix`).

If already on a branch that clearly matches this ticket, say so and offer to just continue on it instead of creating another.

## 5. Local changes

If the working tree is dirty, list the changes grouped as staged, unstaged, and untracked, then ask:

- **Carry over**: safe only when the switch does not conflict. Say what will come along.
- **Stash**: `git stash push -u -m "ns-to-branch: <from-branch> before <new-branch>"`. Report the stash ref and remind the user how to restore it (`git stash pop`).
- **Commit first**: hand off to `/ns-to-save`, then resume.
- **Discard**: show exactly what will be lost, get an explicit yes, and never suggest it by default.

Ignore-only or submodule-only differences: mention them, do not act on them.

## 6. Create

1. If a remote exists, `git fetch` (prune). If offline or fetch fails, say so and continue from the local base, flagged as possibly stale.
2. Bring the base up to date only when it is a safe fast-forward. If the local base has diverged from its upstream, or has unpushed commits, stop and ask rather than resetting anything.
3. Check the base is not far behind or ahead in a surprising way (`git rev-list --left-right --count base...upstream`) and report the numbers.
4. Create it:
   - Default: `git switch -c <name> <base>`.
   - Worktree (when `--worktree` is passed, a dirty tree the user wants left untouched, or parallel agents will work on tickets): `git worktree add ../<repo>-<slug> -b <name> <base>`. Report the path and remind the user to open a new session there. Warn that dependencies and env files are per-worktree.
5. Verify: `git branch --show-current` equals the name, and the tree state matches what was agreed.
6. Do not set an upstream or push. Publishing happens later via `/ns-to-pr`.
7. If the ticket file has a `Status:` line and it says `open`, offer to set it to `in-progress` through the normal Edit flow. Never edit it silently.

If submodules exist, note that `git submodule update --init --recursive` may be needed. Do not run it uninvited.

## 7. Launch banner

Read `references/banner.md` and follow it.

## Failure handling

If a git error occurs, report it immediately with the exact output, state what has and has not changed (branch created? stash made?), and offer to restore the previous state (switch back, `git stash pop`, delete the new branch). Never force, reset, or delete a branch without explicit confirmation.
