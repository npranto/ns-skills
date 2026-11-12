## 6. Skill inventory

### Phase skills (`/ns-to-*`)

| Skill | Does | Writes |
|---|---|---|
| `start` | Bootstrap a new repo | README, tracker docs, first commit |
| `capture-idea` | Rough idea to structured brief | `docs/product/project-brief.md` |
| `wayfinder` | Clear a decision frontier across sessions | `docs/product/wayfinder/*` |
| `grill-me` | Settle decisions one at a time | `CONTEXT.md`, ADRs, brief |
| `discover-codebase` | Read-only system map | `docs/architecture/codebase-map.md` |
| `architect` | Simplest production-safe architecture | `docs/architecture/*` |
| `design` | UI/UX contract | `docs/design/*` |
| `spec` | Record settled decisions | `.scratch/<slug>/spec.md` |
| `tickets` | Vertical-slice tickets plus parallelism classification | `.scratch/<slug>/issues/*` |
| `split-ticket` | Split one ticket into reviewable leaves | `issues/NN.MM-*` |
| `branch` | Safe, well-named branch or worktree | git branch |
| `scope-check` | Trim, blast radius, abuse cases, and real design choices before implementing | the ticket's `## Decisions` |
| `implement` | One vertical slice, test-first, with every kept test | code, tests |
| `verify` | Full proof locally, smoke check on preview and production, score, evidence; also baseline and project verification skill setup | tests, `.verification/<branch>/*`, `.claude/skills/verify-<app>/` (setup) |
| `understand` | Implementation brief and review path | - |
| `review` | Thirteen-part review, reviewers scaled by risk | - |
| `quality-check` | Stage plan you confirm, then staged checks; CI enforces the core four | CI workflow |
| `integration-check` | Assembled feature against the spec, on base and production | - |
| `stakeholder-brief` | The stakeholder review and the Shipped comment on every PR | two PR comments, optional page |
| `postmortem` | Blameless incident record, then a lessons card | `docs/incidents/NNNN-slug.md` |
| `save` | Conventional commit, never pushes | commit |
| `pr` | Push, open, the PR's reports, the preview check | PR, its reports, the version bump commit |
| `rollback` | Prepare a timed plan, or execute it and clean up | rollback plan |
| `deploy` | Preflight, the release card (the merge), confirm production; versioning setup | release, version tag |
| `observe` | Logs first, staged checks, verdict, mitigate first when unhealthy | - |
| `docs` | Bring docs up to date with the code | docs |
| `close` | Verify truly done, close the ticket, name the next one | ticket status and closing entry |

### Other skills the workflows use

| Skill | Used in |
|---|---|
| `mattpocock-skills:grilling` | `grill-me`, `wayfinder` |
| `mattpocock-skills:domain-modeling` | `grill-me`, `architect`, `docs`, onboard, architecture, wayfinder |
| `mattpocock-skills:diagnosing-bugs` | bug, incident, performance |
| `mattpocock-skills:tdd` | `implement`, bug |
| `mattpocock-skills:prototype` | spike, architecture, `design`, `wayfinder` |
| `mattpocock-skills:research` | spike, performance, architecture, `capture-idea`, `wayfinder` |
| `mattpocock-skills:codebase-design` | `architect`, architecture |
| `mattpocock-skills:code-review` | `review` |
| `mattpocock-skills:wizard` | infrastructure, `deploy`, `quality-check setup-ci` |
| `mattpocock-skills:resolving-merge-conflicts` | `branch`, `pr`, delegate |
| `mattpocock-skills:writing-for-agents` | onboard, `docs` |
| `/setup-matt-pocock-skills` | `start`, onboard (tracker and domain docs setup) |
| `security-review` (built in) | security-sensitive modifier |
| `gh-axi` | tracker, PRs, CI status |
| `playwright-cli`, `chrome-devtools-axi`, Lighthouse CLI, `ffmpeg` | `verify`, the only tools for agent-driven browsing (`../ns-route/references/topic-proof.md` "Proof") |
| `herdr` | delegate |

Not part of these workflows:

- `no-mistakes`: its pipeline applies fixes and pushes on its own, which breaks `../ns-route/references/core.md` "Code change approval". You can still run it by itself.
- `code-review` (the built-in top-level skill, not `mattpocock-skills:code-review`): its `--fix` applies findings straight to the working tree, which breaks `../ns-route/references/core.md` "Code change approval". Despite the similar name it is a different skill from `mattpocock-skills:code-review`, which `ns-to-review` can use for parts A and D and which only reports findings. Use `ns-to-review` for reviews inside a flow.
- `simplify`: applies its fixes directly as its default behavior, same conflict as `code-review --fix`. Use `ns-to-scope-check` (before implementing) or `ns-to-review`'s part F, simplicity (after), inside a flow.
- `lavish`, `find-skills`: general tools, not workflow phases.
