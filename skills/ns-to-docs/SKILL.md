---
name: ns-to-docs
description: Review code changes and bring /docs, code comments, README files, CONTEXT.md, and ADRs up to date, moving or removing outdated material.
disable-model-invocation: true
argument-hint: "[base ref, or 'all' for a full docs audit]"
---

# ns-to-docs

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Ask via the multiple-choice question tool for scope if unclear: docs for the current branch's changes (default, diff against the default branch), a specific range, or a full docs audit.

## Steps

1. Read the diff and inventory the docs: `docs/**`, `README.md` files, `CONTEXT.md`, `docs/adr/*`, `docs/architecture/*`, `docs/design/*`, `CLAUDE.md`/`AGENTS.md`, `.env.example`, the project verification skill's feature map (`.claude/skills/verify-<app>/features/`: add or update the feature this change touched), and inline docs (docstrings, comments) near changed code.
2. Search the whole codebase, not only the docs near the diff, for every other mention of anything renamed, removed, or changed in behavior: old function and type names, flags, routes, env vars, config keys.
3. For each change, find docs that are now wrong, incomplete, or missing. Also find stale material unrelated to the diff when auditing.
4. Propose the edits as a list: update, add, move to an archive (`docs/archive/`), or remove. Ask for approval on removals and moves. Do not touch `CHANGELOG.md` or auto-generated files.
5. Apply the approved edits one file at a time via file-edit tool so the user approves each diff (no scripts or bulk rewrites; see `../ns-route/references/core.md` "Code change approval"). Keep docs concise, non-duplicative, and pointing at the source of truth rather than restating code. Use `CONTEXT.md` vocabulary. Never rewrite a settled ADR: supersede it with a new one and link them (`mattpocock-skills:domain-modeling`).
6. When editing `CLAUDE.md`, `AGENTS.md`, or skills, follow `mattpocock-skills:writing-for-agents`.
7. Report every file changed and why. Suggest `/ns-to-save`.
