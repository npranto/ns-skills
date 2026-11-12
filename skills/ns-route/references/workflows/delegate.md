### delegate

Hand tickets to agents and get review-ready PRs back. Requires Herdr. `/ns-flow-delegate <ticket> <ticket> ...`

```
intake ◆ ─▶ plan ◆ ─▶ launch (3 agents at most, one worktree each, each running [TICKET] to a review-ready PR)
   ─▶ watch and relay ─▶ final review per PR ◆ (decided without you)
   ─▶ ship PRs one at a time (the rest of [TICKET], from rollback:prepare? to close) ─▶ [FEATURE-END]? ─▶ clean up ◆
```

- Low and medium risk only. Planning, high or critical risk, migrations, and incidents are done with you.
- Inside its own worktree an agent edits without per-file approval, and takes the recommended answer at every stop except the ones in `../ns-route/references/delegate.md` "What always stops". Each decision it made is recorded in the ticket as `decided by agent`.
- The final review lists what the agent decided without you, and every PR still ships through the release card.
- `integration-check` in [FEATURE-END] matters most here, because agents never saw each other's diff.
