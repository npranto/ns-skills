# Integration-check gate

## Integration-check gate (anti-fragmentation)

`/ns-to-integration-check` runs once per feature, after every one of its tickets has shipped and closed - wired into `/ns-flow-feature`, `/ns-flow-delegate`, and the migration baseline in `/ns-route`. Individually green tickets do not guarantee the assembled feature works: this gate re-derives the feature's user flows and acceptance criteria from `spec.md` (not from any one ticket) and walks them end to end on the assembled base branch and on production, checks the contracts at every cross-ticket seam, and re-verifies earlier tickets' acceptance criteria for regressions introduced by later ones.

It never re-reviews a ticket's own diff - that already happened in `/ns-to-review`. Any gap or regression it finds is resolved through a normal ticket (`/ns-to-tickets` then `/ns-flow-ticket`), a small inline fix through the usual gates, or an escalation to `/ns-to-spec` if the spec itself was wrong - never fixed in place inside this skill. The feature is not turned on for everyone, and its Shipped report is not written, until it reports clean or the user explicitly accepts a finding with a stated reason.
