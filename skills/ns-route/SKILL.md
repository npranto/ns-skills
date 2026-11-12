---
name: ns-route
description: The front door for this skill family. Picks a workflow from the workflow catalog instantly when the situation is already obvious (new feature, bug, one ticket, docs-only...), otherwise classifies the task (type, scope, uncertainty, risk, reversibility, codebase familiarity, security sensitivity, data risk, sessions expected) and composes the exact ns-to-*/ns-flow-* sequence and human gates for it. Then runs it step by step or on autopilot, or stops with just the plan. Run this whenever it is unclear what to run, or to see the full command menu.
disable-model-invocation: true
argument-hint: "<task description, ticket, bug report, dependency bump, incident, or reference - or blank to see the menu, or status> [--auto]"
---

# ns-route

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-skill-kinds.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/index.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-architecture, ns-flow-bugfix, ns-flow-delegate, ns-flow-docs, ns-flow-existing-project, ns-flow-feature, ns-flow-new-project, ns-flow-ticket, ns-flow-wayfinder
The workflow files in `../ns-route/references/workflows/` own every workflow chain this skill routes to; `index.md` there is the catalog.

Router, and the runner for workflows that have no flow skill. While routing (steps 0-4) it never edits project files, writes docs, creates tickets, or implements. Only once the user chooses to run (step 5) does it hand off to a flow or follow the phases in order.

## 0. Already know what you need?

If the user names a clear, ordinary situation, pick its workflow from `../ns-route/references/workflows/index.md` ("Pick a workflow"), print that workflow's diagram and notes from its file beside it, and go straight to step 5 - no classification needed.

If the user just asks for the menu, print the "Pick a workflow" table in `../ns-route/references/workflows/index.md` and the phase skill list in `../ns-route/references/workflows/skill-inventory.md`, and stop.

If the argument is `status`, or the user asks "where am I", print the status view (`references/status-view.md`) and stop.

Anything less ordinary - or where risk, data sensitivity, security, uncertainty, or reversibility might change the sequence - goes through classification instead. Continue to step 1.

## 1. Gather

Take the task description or argument. If none, ask for it - a sentence, a ticket, a bug report, an incident summary, or a link is enough.

Read `references/gather.md` and follow it.

## 2. Classify

Score every dimension below. Use the repo investigation first; ask via a single batched multiple-choice question call (up to 4 questions at once, recommended option first) only for what genuinely depends on the user's intent, not on what the code shows.

Read `references/classification.md` and score every dimension with it.

## 3. Compose the workflow

Read `references/composition.md` and apply it.

## 4. Output

Read `references/output.md` and print the classification as it says.

## 5. Run

Ask via the multiple-choice question tool: run step by step (Recommended), run on autopilot, hand to an agent (only for low or medium risk tickets with settled plans), by hand, adjust the classification, or stop here with just the plan. `--auto` in the arguments preselects autopilot, but the plan is still printed first.

- **Hand to an agent** (`../ns-route/references/core.md` "Run modes"): run any planning phases here with the user first, then read `../ns-flow-delegate/SKILL.md` and follow it with the resulting tickets.

- **By hand** (`../ns-route/references/core.md` "Run modes"): pick and confirm the `<slug>` when the commands need one, then print the sequence as a numbered list of exact commands with their real arguments, for example `/ns-to-grill-me .scratch/notes-archive/` or `/ns-flow-ticket .scratch/notes-archive/issues/03-archive-note.md`, then `NEXT  <first command>`. Run nothing, and stop.

- **The sequence is a flow** (with or without modifiers): read that flow's `SKILL.md` and follow it with the task as its input, in the chosen run mode. Where modifiers changed the sequence, the printed sequence overrides the flow's defaults.
- **No flow covers it** (refactor, restructure, stack-move, rebuild, modernize, performance, dependency, infrastructure, spike, proposal, ship): act as the flow yourself. Pick a `<slug>` and confirm it, follow each phase's `SKILL.md` in the printed order, apply "Run modes" between phases, loop back to `/ns-to-implement` on blocking findings as `/ns-flow-ticket` does, and track progress in `.scratch/<slug>/progress.md`.

## Do not

Do not do any phase's work while routing (steps 0-4). Do not invent a phase that has no corresponding skill. If the composed sequence matches an existing `/ns-flow-*` exactly, say so and hand off to it instead of restating it step by step.

## Status view

Read `references/status-view.md` and follow it.
