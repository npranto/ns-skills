# Gather

Investigate before asking anything (facts discoverable in the repo are never asked):

- `git status --porcelain=v1 -b`, `git log -1`, whether the directory has any files at all (greenfield signal).
- `docs/architecture/codebase-map.md` - presence and how stale it looks against recent commits (familiarity signal).
- `CONTEXT.md`, `docs/adr/*`, `docs/product/project-brief.md` presence.
- The referenced ticket or spec, if any (`.scratch/**/issues/*`, tracker id via `gh-axi`).
- `.github/workflows/` or equivalent (whether a quality gate already exists).
- The project profile, `docs/agents/workflow.md`. Missing on a project with code: say so and offer to write it (`../ns-route/references/profile.md`) before running anything that ships.
- Whether anything is currently broken in production right now (distinguishes `bug` from `incident`, and pushes RISK toward `critical`).
