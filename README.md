# ns-skills

A set of Agent Skills that takes engineering work from an idea to production, with a human decision at every gate that matters. One router, nine flows and 27 phases, all manual-only: nothing runs unless you type its command.

Works with Claude Code, Codex, Cursor and OpenCode.

## What you get

- `/ns-route` is the front door. Describe the work (a feature, a bug, an incident, a refactor, a dependency bump, a spike) or ask for the menu. It sizes the task, rates risk, shows the exact sequence it will run, and waits for you before running it.
- Nine flows run a whole workflow: `ns-flow-new-project`, `ns-flow-existing-project`, `ns-flow-feature`, `ns-flow-ticket`, `ns-flow-delegate`, `ns-flow-bugfix`, `ns-flow-architecture`, `ns-flow-wayfinder`, `ns-flow-docs`.
- 27 phases do one job each and can be run by hand: `ns-to-grill-me`, `ns-to-spec`, `ns-to-tickets`, `ns-to-scope-check`, `ns-to-implement`, `ns-to-verify`, `ns-to-review`, `ns-to-save`, `ns-to-pr`, `ns-to-deploy`, `ns-to-observe`, `ns-to-rollback` and more. [docs/workflow-map.html](docs/workflow-map.html) shows how they connect.

The rules that hold everywhere: every file edit, commit, PR and deploy needs your approval (configurable), evidence is shown rather than claimed, and a run ends with an honest report of what was and was not proven. The shared rules live in [skills/ns-route/references/core.md](skills/ns-route/references/core.md).

## Install

Install the whole set. The skills read each other's files, so a partial install is not supported.

Claude Code, as a plugin:

```
/plugin marketplace add npranto/ns-skills
/plugin install ns-skills@ns-skills
```

Commands are then namespaced, for example `/ns-skills:ns-route`.

Any harness, with the [`skills`](https://www.npmjs.com/package/skills) installer:

```
npx skills add npranto/ns-skills
```

Commands are then plain, for example `/ns-route` in Claude Code and `$ns-route` in Codex.

## Requirements

Required: git. The tools below are used by the phases that need them. When one is missing, the phase says so at the step instead of guessing; the full table, with fallbacks, is in [skills/ns-route/references/topic-tools.md](skills/ns-route/references/topic-tools.md).

| Tool | Used for |
|---|---|
| `gh-axi` | GitHub issues, pull requests and CI |
| `playwright-cli`, `chrome-devtools-axi` | browser proof in `ns-to-verify` |
| `lighthouse` | performance checks |
| `ffmpeg` | video evidence |
| `herdr` | delegating tickets to other agents (`ns-flow-delegate`) |
| the `mattpocock-skills` plugin | some phases call its skills (grilling, TDD, domain modeling); without it they follow the same practice inline and say so |

## Harness notes

| Harness | Status |
|---|---|
| Claude Code | tested: plugin install, `npx skills` install, manual-only honored |
| Codex | tested: `$ns-...` commands; each skill ships `agents/openai.yaml` so Codex does not start one by itself |
| OpenCode | tested: skills load by name; the manual-only flag is not honored by OpenCode itself, so it may load one when asked loosely |
| Cursor | reads the same skill folders; not tested here yet |

More in [skills/ns-route/references/topic-harnesses.md](skills/ns-route/references/topic-harnesses.md).

## Per project setup

Nothing is needed up front. `ns-to-start` (and any phase that needs a convention such as the default branch, how to run tests or where evidence goes) asks once and records it in the project profile, `docs/agents/workflow.md`, in your project. Defaults, config layers and the safety floor are in [skills/ns-route/references/topic-tools.md](skills/ns-route/references/topic-tools.md).

## Contributing

Run the checks before every change, see [docs/MAINTENANCE.md](docs/MAINTENANCE.md). The changelog is generated from GitHub releases, so do not edit it by hand.

## Credits

`ns-to-verify`'s setup guide and several principles in `ns-route/references/principles.md` are adapted from pstack by poteto (MIT). The workflow ideas lean on Matt Pocock's skills. See [LICENSE](LICENSE).

## License

MIT
