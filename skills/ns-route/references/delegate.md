# Delegate mode

For "take this and come back with a PR". Started only by `/ns-flow-delegate` (the "hand to an agent" run mode). An agent works alone in its own worktree and branch, runs `/ns-flow-ticket` as far as a review-ready PR, and stops. The user's session (the captain) reports and asks in plain English.

Low and medium risk tickets only (`/ns-route`'s risk score, or the ticket's). Planning, high or critical risk, migrations, and incidents are done with the user.

This is the one exception to `../ns-route/references/core.md` "Code change approval": inside its own worktree, a delegated agent changes files without per-file approval. Nothing it does reaches the base branch or production without the user's final review and the release card.

## What the agent does without asking

Inside its own worktree and branch:

- edits, creates, and deletes project files, with no per-file approval
- takes the recommended answer at every routine question and at scope-check's TRIM, FLAG, and design-choice stops, recording each in the ticket's `## Decisions` marked `decided by agent`, with what it rejected and why
- runs installs, tests, builds, linters and formatters (including `--fix` and `--write`), the proof tools (`playwright-cli`, `chrome-devtools-axi`, `lighthouse`, `ffmpeg`), `git`, `gh-axi`, and read-only host commands
- runs `/ns-to-verify` automatic and hidden, and quality-check with its recommendation, listing every skipped stage in the PR description
- fixes every blocking and should-fix review finding, and lists the nits in the PR
- commits, pushes its own branch, opens the PR, and writes the PR's report set up to review-ready: the description, the local and preview verification comments, the evidence page, and the stakeholder review
- starts read-only research or review subagents, three at most at a time

## What always stops and goes to the user

- merging, promoting, deploying, rolling back, changing a flag
- force-push, history rewrite, `git reset --hard`, deleting a branch or worktree it did not create, `rm -rf` outside its worktree
- destructive data operations, or a migration against a shared or production database
- creating, changing, or printing secrets or environment variables
- writing anywhere outside the repo, its PR, and that PR's evidence page
- a new paid service, a dependency with a restrictive license, or a change that contradicts a settled decision
- the risk turning out high or critical, a root cause it cannot prove, an ESCALATION from implement, or the same phase failing twice

When it is unsure whether something is destructive, it stops.

## Launch

Edits auto-accepted, an allowlist for the tools above, and the stop list denied at the tool level:

```
herdr agent start <name> --kind claude --pane <pane-id> -- \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Edit" "Write" "Glob" "Grep" "Agent" "Skill" "Artifact" \
    "Bash(git:*)" "Bash(gh:*)" "Bash(gh-axi:*)" "Bash(vercel:*)" \
    "Bash(npm:*)" "Bash(pnpm:*)" "Bash(yarn:*)" "Bash(bun:*)" "Bash(npx:*)" "Bash(node:*)" \
    "Bash(playwright-cli:*)" "Bash(chrome-devtools-axi:*)" "Bash(ffmpeg:*)" "Bash(curl:*)" "Bash(ls:*)" "Bash(mkdir:*)" \
  --disallowedTools "Bash(gh pr merge:*)" "Bash(gh-axi pr merge:*)" "Bash(npx -y gh-axi pr merge:*)" "Bash(git push --force:*)" "Bash(git push -f:*)" \
    "Bash(git reset --hard:*)" "Bash(git branch -D:*)" "Bash(git worktree remove:*)" \
    "Bash(vercel --prod:*)" "Bash(vercel deploy --prod:*)" "Bash(vercel promote:*)" "Bash(vercel rollback:*)" \
    "Bash(vercel env add:*)" "Bash(vercel env rm:*)" "Bash(rm -rf:*)"
```

Extend the allowlist with the project's own task runner after reading its scripts. Check `herdr agent --help` and `claude --help` for the flag syntax before the first launch: this command has not been run on a real repo yet.

## How the agent runs

The agent is prompted with `/ns-flow-ticket <ticket> in delegate mode: stop at a review-ready PR`. It runs the flow on autopilot, with the differences above: every stop that is not on the "always stops" list takes the recommended answer without waiting, and the run ends after `/ns-to-pr` with the PR open, before the release card. The PR description gets two extra folds: the scope-check output (with each design choice the agent made) and the `/ns-to-understand` brief.

## The review gate

The captain shows the "decided without you" table from the ticket's `## Decisions` and asks what to do with the PR (`../ns-flow-delegate/SKILL.md` "Final review, per PR"). Nothing merges without that answer and the release card.
