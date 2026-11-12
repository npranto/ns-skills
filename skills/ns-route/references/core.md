# Shared conventions for all ns-to-*, ns-flow-*, and ns-route skills

Every skill reads this file first. Skills are manual-only (see `../ns-route/references/topic-harnesses.md`): they run only when the user invokes them by name.

Files on disk are the handoff between phases, so any phase can be run in a fresh context.

## Artifact locations (defaults)

Prefer whatever the repo already uses. Check `docs/agents/issue-tracker.md` and `docs/agents/domain.md` first. Defaults when absent:

| Artifact | Path |
|---|---|
| Project brief | `docs/product/project-brief.md` |
| Domain glossary | `CONTEXT.md` (or `CONTEXT-MAP.md` in multi-context repos) |
| ADRs | `docs/adr/NNNN-slug.md` |
| Postmortems | `docs/incidents/NNNN-slug.md` |
| Architecture | `docs/architecture/{system,data-model,flows}.md` |
| Design | `docs/design/{ui-spec,wireframes}.md` |
| Codebase map | `docs/architecture/codebase-map.md` |
| Wayfinder map | `docs/product/wayfinder/map.md` (decision tickets: `docs/product/wayfinder/NN-slug.md`) |
| Spec | `.scratch/<slug>/spec.md` |
| Tickets | `.scratch/<slug>/issues/NN-slug.md` (sub-tickets: `NN.MM-slug.md`, recursive) |
| Project profile | `docs/agents/workflow.md` |
| Project verification skill | `.claude/skills/verify-<app>/` (feature map in `features/`) |
| Proof results and evidence | `.verification/<branch>/` (git-ignored, never committed) |

Ticket files carry `Status:` and `Blocked by:` lines near the top, and end with two headings: `## Decisions` and `## Comments`. The ticket file is the one home for everything about its ticket: each decision made while building it (a scope-check trim or design pick, a declined review finding with the user's reason, a ticket-level grill answer) is appended under `## Decisions`, and progress notes, deviations, and deferrals under `## Comments`. Decisions settled before tickets exist go in the spec's DECISIONS section. Never a separate decisions file.

## Interaction rules

1. **Ask, do not assume.** Use the multiple-choice question tool for any missing requirement, ambiguous input, or choice that changes what you do next. Put the recommended option first, suffixed "(Recommended)". Facts discoverable in the repo are investigated, never asked.
2. **Missing input means stop and ask.** If a skill needs a ticket, spec, or brief and none is given or found, ask for it. Never invent one.
3. **One decision at a time** in grilling, architecture, and design phases: context, recommendation, tradeoffs, a Learn box (see `../ns-route/references/topic-learn-box.md`), then wait. Do not batch.
4. **Agreement locks only that decision.** It does not authorize implementation.
5. **Settled decisions are authoritative.** Do not reopen them unless you find a genuine contradiction or technical impossibility. Then surface it explicitly, cite the ADR or doc, and let the human decide.
6. **Stop where the skill says stop.** Phases end with a summary and a next-step suggestion, not an automatic jump. Only a flow or `/ns-route` chains to the next phase, per `../ns-route/references/core.md` "Run modes".

## Project profile

`docs/agents/workflow.md` holds the facts skills would otherwise ask on every run: whether there is UI, the host, production and preview URLs, how deploys happen, where logs are, the fastest undo, the flag system, the verification skill, the env file, the E2E setup. Template and rules: `../ns-route/references/profile.md`. Read it instead of asking. A missing profile or field is said aloud and asked, never a reason to skip a step silently.

## Phase display

Every flow and phase prints the same three things, so a run can be followed at a glance. Plain Markdown: no boxes, no ASCII art.

1. **Run tracker** (flows only): one line in a code span, one entry per phase of the flow's table in order, printed when the flow starts and again at every gate. Glyphs: `✓` done, `▶` running, `○` waiting, `–` skipped, `✗` failed. Name each phase without its `ns-to-` prefix.

   `✓ branch  ✓ scope-check  ▶ implement  ○ verify  ○ understand  ○ review  ○ quality-check  ○ save  ○ pr  ○ deploy  ○ observe  ○ close`

2. **Phase header**, the first line of every phase: `### ▶ 5/16 · ns-to-verify local`. A phase run alone has no count: `### ▶ ns-to-verify`.
3. **Phase footer**, the last line of every phase before its gate: run `python3 ../ns-route/scripts/ns phase` (read-only; it reads the session transcript) and print its output after the glyph: `✓ ns-to-verify · 5m56s · 318k weighted tokens (3% of the run so far) · 21 calls · context 127k`. A failed phase uses `✗`. If the command is missing or fails, print `tokens: unavailable (<the error>)` in its place. Never drop the line silently.

Weighted tokens put input (1x), cache write (1.25x or 2x), cache read (0.1x), and output (5x) on one scale, so one number ranks where the cost goes. A skill never estimates tokens itself. The rest is read after the fact, in a terminal: `ns usage` (one session, run by run), `ns trend` (each skill over time), `ns calls` (every call), `ns watch` (live). Run `ns` for the list.

## Run modes

Flows and `/ns-route` run in one of these modes. Phase skills do the same work in each; only who answers the routine questions, and who types the next command, changes.

- **Step** (default): after each phase, summarize in two or three lines and ask via the multiple-choice question tool: continue (Recommended), redo this phase, or stop.
- **Autopilot** (`--auto` in the arguments, or chosen at `/ns-route`'s run question): chain phases without the between-phase question, so a whole workflow can be handed to an agent session.
- **Hand to an agent** (chosen at `/ns-route`'s run question, or `/ns-flow-delegate`): low or medium risk tickets with settled plans are built by agents in their own worktrees, each to a review-ready PR, under `../ns-route/references/delegate.md`. Planning runs here with the user first. The user reviews what each agent decided, and every PR still ships through the release card.
- **By hand** (chosen at `/ns-route`'s run question): nothing runs. `/ns-route` prints the composed sequence as a numbered list of exact, copy-pasteable commands with their real arguments (paths, ids, slugs), then the first one again as a `NEXT` line, and stops. The user runs each command themselves, clearing context between phases whenever they like.

**Autopilot setup.** Before the first phase, ask once in a single batched multiple-choice question: where to stop (through deploy, observe, and close (Recommended; the release card still stops for the merge), after the PR, or after planning), the proof mode for the whole run (automatic watched, automatic hidden, manual, or skip; `../ns-route/references/topic-proof.md` "Proof"), and the flow's own skip questions. Record the answers and each phase's outcome in `.scratch/<slug>/progress.md` so any session can resume.

**Auto-answered on autopilot** with the recommended option, and logged in the phase summary:

- the between-phase continue/redo/stop question;
- the stage plan in `/ns-to-quality-check` and the check plan in `/ns-to-observe` ("run my recommendation");
- branch name and base in `/ns-to-branch`, doc scope in `/ns-to-docs`, and `/ns-to-understand`'s closing question (the brief stays in chat and goes into the PR description);
- offers to write an artifact (the file-edit approval itself remains the gate);
- optional offers the workflow does not require, such as `/ns-to-stakeholder-brief`: skip.

**Never auto-answered, even on autopilot** (the ◆ gates in `../ns-route/references/workflows/index.md`):

1. Every project file change (see "Code change approval").
2. Decisions: every question in grill, wayfinder, architect, and design phases, ADR offers, and the High-tier observation window and rollback threshold.
3. Plan approvals: spec, tickets, split-ticket breakdown, a bug's root cause and fix plan, restated acceptance criteria for a task with no ticket, scope-check TRIM, FLAG, or design choice, which review findings to fix, and integration-check GAP or REGRESSION handling.
4. Commits (`/ns-to-save`).
5. Outward or irreversible actions: push, opening a PR, editing a PR or posting to it outside its approved report set, merge (the release card in `/ns-to-deploy`), deploy, promote, a flag change, rollback, destructive data operations, writes to an external tracker, publishing any page outside the report set. The stop that pushes and opens a PR also approves that PR's report set (`../ns-route/references/pr-writing.md`): the description regions, the verification comments, the evidence page, and the stakeholder comments are then posted without further stops, each printed in chat, unless the user chose "show me each report first".
6. Anything that could lose or move uncommitted work, such as dirty-tree handling in `/ns-to-branch`.
7. Trouble: missing input, an ESCALATION from `/ns-to-implement`, a phase that still fails after one loop back to fix it, an UNHEALTHY or NOT CLOSED verdict, or any unexpected git or tool error. Stop, report, and ask.

Autopilot needs an interactive session (terminal, IDE, or Herdr pane) because of these gates. Headless runs (the harness's non-interactive mode) can only do read-only phases.

## Code change approval (non-negotiable)

Every change to project files (source, tests, config, docs, CI, tickets excepted only where a skill says it writes its own artifact after approval) goes through the user, file by file, no matter what.

- Make each change with the harness's file-edit tool so the user sees and approves that specific diff. One file per approval, never a batch of files under one approval.
- Never change files through scripts or automation: no `sed`, `awk`, `perl`, `python`, shell redirects or heredocs writing files, codemods, `--fix`/`--write` flags (eslint --fix, prettier --write, etc.), formatters, generators, or scaffolders that write files. Run linters and formatters in check mode only, then propose the fixes yourself as normal edits.
- Subagents, workers, worktrees, and pipelines (including any CI or tool auto-fix) must not apply code changes on their own. They report findings or proposed diffs, and the main session applies each one through the user.
- **The one exception: delegate mode.** When the user chooses "hand to an agent" (`/ns-flow-delegate`), that agent changes files in its own worktree and branch without per-file approval, within the limits in `../ns-route/references/delegate.md`. Its work reaches the base branch only after the user's final review of the PR, including every decision the agent made without them, and the release card.
- If a task seems to need a mass change, list the affected files, then walk through them one at a time. Do not go looking for a way around this.
- While any `ns-*` flow is active, use `ns-to-review` and `ns-to-scope-check` for review and cleanup requests, never the generic `code-review` (with `--fix`) or `simplify` skills - both apply edits directly and would bypass this gate. See `../ns-route/references/workflows/index.md` "Not part of these workflows."

## Safety rules

- Never push, merge, deploy, or force anything unless the skill's step explicitly does it and the user confirmed in this run.
- Never edit `CHANGELOG.md` or any file marked auto-generated.
- Commit messages: Conventional Commits, and no agent co-author trailer.
- Before deleting or overwriting, look at the target.
- Report outcomes faithfully. Failing tests or skipped steps are stated plainly.
- Plain hyphen `-` only, never the em dash.

## Configuration and policy

Every rule here and in the topic files applies exactly as written unless a written override says otherwise. Overrides live in two files, the later one winning: the user's global agent file (such as `AGENTS.md` in the user's home), then the project profile `docs/agents/workflow.md` (see `../ns-route/references/profile.md`). A skill's own restatement of a rule follows the same override.

Overridable policy: "Code change approval" ("non-negotiable": only a written override in one of those files may loosen it), the commit message style and no co-author trailer rule, never editing `CHANGELOG.md` or generated files, and the plain hyphen rule. Never assume an override; name the file it came from.

The safety floor is not policy and no override loosens it: never push, merge, deploy, force anything, or destroy data unless the skill's step explicitly does it and the user confirmed in this run; never read an override as that confirmation. In "Run modes", the "Never auto-answered" list keeps stopping on autopilot; its first item, every project file change, follows "Code change approval" as configured.

## Capability words and paths

If the harness lacks a capability a skill names (for example the multiple-choice question tool), see `../ns-route/references/topic-harnesses.md`: ask the same question as plain text, options listed with the recommended one first, then stop and wait.

A path that starts with `../` is relative to the folder of the skill you are running. Resolve it to a full path before using it in a shell command. Paths that start with `docs/` or `.` are relative to the project, except where the text says the package's own `docs/`.
