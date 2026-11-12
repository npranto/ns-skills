---
name: ns-flow-delegate
description: Hand low or medium risk tickets to agents in their own worktrees and get review-ready PRs back, with a review of what each agent decided without you, then ship them one at a time. The "hand to an agent" run mode. Requires Herdr.
disable-model-invocation: true
argument-hint: "<one or more ticket paths, ids, or task descriptions>"
---

# ns-flow-delegate

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-integration-gate.md`, `../ns-route/references/topic-delivery.md`, `../ns-route/references/delegate.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/workflows/delegate.md`, `../ns-route/references/workflows/shared-blocks.md`, `../ns-route/references/workflows/ticket.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Calls: ns-flow-ticket, ns-to-branch, ns-to-close, ns-to-deploy, ns-to-integration-check, ns-to-observe, ns-to-rollback, ns-to-save, ns-to-split-ticket, ns-to-stakeholder-brief, ns-to-tickets, ns-to-verify
Read `../ns-route/references/delegate.md` (what an agent may do alone, what always stops, the launch command) and `../ns-route/references/herdr.md` (the herdr usage guide, copied from herdr's own skill; the `herdr` CLI is a requirement of this flow: if it is missing, stop and say so; IDs, `--no-focus`, never close panes you did not create).

This session is the **captain**. It edits no project file and builds nothing. It sets up the agents, watches them, relays their questions, and ships their PRs. Each ticket is built by its own agent, in its own worktree. Talk to the user in plain English, and name work by its ticket title, never by pane or session.

## 1. Preconditions

1. **Herdr:** `test "${HERDR_ENV:-}" = 1`. Not inside Herdr: say so and ask: open Herdr and run this again (Recommended), or run the ticket here with `/ns-flow-ticket` instead.
2. Check the installed CLIs before the first launch: `herdr agent --help`, `herdr worktree --help`, `claude --help`.
3. The repo is on the base branch, clean, with no merge or rebase in progress, and up to date with its upstream. Otherwise stop and report (`/ns-to-branch` and `/ns-to-save` can help).
4. A remote exists and `gh-axi` works.

## 2. Intake

Take the tickets from the arguments. None: list the open, unblocked tickets and ask (multi-select).

- **Risk check.** Only low and medium risk tickets are delegated (`/ns-route`'s scoring, or the ticket's). A high or critical, migration, or incident ticket is named and left out: it is built with the user through `/ns-flow-ticket`.
- **A task with no ticket:** restate it as SCOPE, OUT OF SCOPE, and ACCEPTANCE CRITERIA, confirm it, and write it as a ticket file now. The agent cannot ask later.
- **Settle what an agent would have to guess:** an ambiguous requirement, a design preference, test accounts, where the env files live. Record each answer in the ticket's `## Decisions`.
- **Size:** for each ticket, ask: keep as one, or split it. Recommend one, and say if it looks too large. Run `/ns-to-split-ticket` here, before launch, only on "split it".

## 3. Plan

- A ticket blocked by an unresolved ticket waits, or stacks on its branch if the user chooses (`/ns-to-branch` "stacked" base).
- Tickets that touch the same files, migrations, or lockfile run one after another. Prefer `/ns-to-tickets`' SEQUENTIAL / PARALLEL-SAFE / PARALLEL-WITH-CONFLICT-RISK classification when it exists.
- Three agents at once at most, unless the user asks for more.
- Name branches with the `/ns-to-branch` rules.

Print the plan and ask via the multiple-choice question tool: start (Recommended), change the plan, or stop.

```markdown
### Hand-off plan

| Ticket | Risk | Branch | Runs | Overlap |
|---|---|---|---|---|
| 03 Archive a note | medium | `feat/03-archive-note` | now | - |
| 04 Restore a note | medium | `feat/04-restore-note` | after 03 | same files as 03 |
| 05 About page | low | `feat/05-about-page` | now | - |

Each agent edits, tests, commits, pushes its branch, opens its PR, and posts that PR's
reports and evidence page without asking.
Each stops and asks you, through me, before merging, deploying, deleting, forcing,
touching secrets or data, or writing outside the repo and its PR.
```

## 4. Launch

Per ticket, in plan order:

1. `herdr worktree create --cwd "$PWD" --branch <branch> --base <base> --path ../<repo>-wt/<ticket-id> --label <ticket-id> --no-focus`. Record the workspace id, pane id, worktree path, and branch in `.scratch/<slug>/progress.md`.
2. Make the worktree runnable: install dependencies. Env files are usually untracked: copy the ones the project documents only if the user agreed in step 2, and never print their contents.
3. Start the agent with the launch command in `../ns-route/references/delegate.md`, extended with the project's task runner.
4. `herdr agent prompt <name> "/ns-flow-ticket <ticket path> in delegate mode: stop at a review-ready PR"`, without `--wait`, so all agents start together.

Tell the user in two lines what is running and that this session will report back.

## 5. Watch and relay

Check `herdr agent list` when Herdr reports a change, when the user asks, or at a relaxed interval. Never poll on a tight loop. Report one line per ticket:

```
03 Archive a note    implementing                 12 min in
05 About page        PR #483 open, preview check running
04 Restore a note    waiting for 03
```

**An agent stops:** read what it asks (`herdr agent read <name> --source recent-unwrapped`). Tell the user which ticket, what it wants to do, why it stopped, and what you recommend, with real options. Send the user's answer back. Never answer for the user.

**An agent fails or stalls:** leave its worktree in place, report what happened and what it tried, and offer the final-review actions.

The final-review actions are listed in `references/final-review.md`.

## 6. Final review, per PR

Read `references/final-review.md` and follow it.

## 7. Several PRs

Read `references/ship-and-clean-up.md` and follow it.

## 8. Clean up

Read `references/ship-and-clean-up.md` and follow it.

If the captain session ends, the agents keep running and `progress.md` holds every id. Running this command again resumes at step 5.
