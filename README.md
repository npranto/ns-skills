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

## Requirements and setup

The skills call a few command-line tools. Install them once per machine, with one command that asks before every step:

```
curl -fsSL https://raw.githubusercontent.com/npranto/ns-skills/main/scripts/setup-tools.sh | bash
```

(or `bash scripts/setup-tools.sh` from a clone). Options: `--only core,ui,delegate,vercel,plugins`, `--harness claude,codex,opencode,cursor`, `--dry-run`, `--yes`. It uses Homebrew for system tools and npm for the rest, never upgrades or removes anything, and works on macOS and Linux (Windows: WSL).

Check the result at any time, from any harness, with `python3 <skills folder>/ns-route/scripts/ns doctor`. The router also runs `ns doctor --quiet` at the start of a run and shows one line when a tool is missing.

| Group | Tool | Used for |
|---|---|---|
| core | `git` | everything |
| core | Node 20+ and npm | runs `gh-axi` and `chrome-devtools-axi` through `npx` |
| core | Python 3.9+ | the `ns` usage tool behind every phase footer |
| core | `gh`, logged in (`gh auth login`) | `gh-axi` wraps it: issues, pull requests, CI |
| ui | `playwright-cli` (`@playwright/cli`) | browser proof, screenshots, clips in `ns-to-verify` |
| ui | `chrome-devtools-axi` and Google Chrome | console, network and accessibility checks |
| ui | `lighthouse` | web vitals |
| ui | `ffmpeg` | clips |
| ui | `axe` (`@axe-core/cli`) | accessibility scan when the repo has no axe setup of its own |
| delegate | `herdr` and `claude` | `ns-flow-delegate` runs one agent per ticket |
| vercel | `vercel` | only for projects deployed on Vercel |
| plugins | the `mattpocock-skills` skills | grilling, TDD, domain modeling and more; without them the skills follow the same practice inline and say so |

A missing tool is reported at the step that needs it instead of being guessed around. Defaults and fallbacks: [skills/ns-route/references/topic-tools.md](skills/ns-route/references/topic-tools.md).

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

`skills/ns-route/references/herdr.md` is the herdr agent skill from [herdrdev/herdr](https://github.com/herdrdev/herdr), copied under the Apache License 2.0 (copy in [licenses/herdr-APACHE-2.0.txt](licenses/herdr-APACHE-2.0.txt)).

`ns-to-verify`'s setup guide and several principles in `ns-route/references/principles.md` are adapted from pstack by poteto (MIT). The workflow ideas lean on Matt Pocock's skills. See [LICENSE](LICENSE).

## License

MIT
