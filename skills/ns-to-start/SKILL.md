---
name: ns-to-start
description: Bootstrap a brand new repo - name, description, README, optional issue tracker, git init, first commit. Run manually at the very start of a project.
disable-model-invocation: true
---

# ns-to-start

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/profile.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

First step of a new project. Ask each question with the multiple-choice question tool, one at a time, and only do what the user opted into.

## Steps

1. Inspect the working directory. If it already holds project files or a git history, tell the user this is not a brand new project and suggest `/ns-flow-existing-project`. Continue only if they confirm.
2. Ask the project name (skip if obvious from the directory and confirmed).
3. Ask for a short description.
4. Ask whether to create a `README.md` containing just the name and description.
5. Ask whether they want an issue tracker in the project. If yes, run `/setup-matt-pocock-skills` (or the `mattpocock-skills` equivalent). If unavailable, create `docs/agents/issue-tracker.md` (local markdown under `.scratch/`) and `docs/agents/domain.md` by hand and reference them from `CLAUDE.md`.
6. Write the project profile, `docs/agents/workflow.md`, from `../ns-route/references/profile.md`. Host, proof, and E2E fields that are not known yet say `set by the walking skeleton`.
7. Ask whether to initialize a git repo. Only if yes: `git init`, then use the `/ns-to-save` procedure for a generic first commit (`chore: initial commit`). Do not push.

8. Ask whether to set up versioning, and explain it in the question, because the answer shapes every later PR title: every merge to the production branch gets a semantic version, a `vX.Y.Z` tag, and a GitHub release, created by CI; each PR carries that version as a bump commit in `package.json`; the bump is a patch unless the PR title carries `[MINOR]` or `[MAJOR]`; a Rollback workflow, run by hand, puts production back on any version. Options: yes (Recommended for anything deployed), not now, no. On yes, read `../ns-to-deploy/references/versioning.md` and run its "Setup". Otherwise write nothing.

CI, preview deployments, and production are set up by ticket 01, the walking skeleton (`/ns-to-tickets`).

## Report

Finish with a bullet list with emojis of exactly what was done and what was skipped, then suggest `/ns-to-capture-idea`.
