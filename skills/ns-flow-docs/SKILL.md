---
name: ns-flow-docs
description: Docs-only change - branch, update docs to match the code, review, check, commit, and open a PR.
disable-model-invocation: true
argument-hint: "[scope: current branch, range, or full audit] [--auto]"
---

# ns-flow-docs

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/docs.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-to-branch, ns-to-docs, ns-to-pr, ns-to-quality-check, ns-to-review, ns-to-save
This flow is the `docs` workflow in `../ns-route/references/workflows/docs.md`.

Phase skills are manual-only: read `../<phase>/SKILL.md` and follow it, never through the harness's skill-invocation tool.

## Sequence

1. `ns-to-branch` (`docs/...`), unless already on a suitable branch.
2. `ns-to-docs` for the scope the user chose. If `CONTEXT.md` or ADRs are missing or stale, use `mattpocock-skills:domain-modeling`.
3. `ns-to-review`, parts D (repo standards) and F (simplicity) only. Docs should be concise and point at the source of truth.
4. `ns-to-quality-check` (run), offering only the stages that fit docs (format, lint, hygiene).
5. `ns-to-save`, then `ns-to-pr`.

Gate after each step per `../ns-route/references/core.md` "Run modes": in step mode ask continue (Recommended), redo, or stop.
