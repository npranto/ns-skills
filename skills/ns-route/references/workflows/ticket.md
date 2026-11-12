### [TICKET]

`/ns-flow-ticket <ticket path | id | task description>`

```
split-ticket? ◆ ─▶ branch ─▶ scope-check ─▶ implement ─▶ verify:local ◆ ─▶ understand
   ─▶ review ◆ ─▶ quality-check ◆ ─▶ save ◆ ─▶ pr ◆ (reports, verify:preview, stakeholder review)
   ─▶ rollback:prepare? ◆ ─▶ deploy ◆ (release card = the merge) ─▶ verify:production ─▶ observe
   ─┬─ HEALTHY ──────▶ stakeholder-brief:release (Shipped) ─▶ postmortem? ◆ ─▶ close
    └─ UNHEALTHY ◆ ─▶ mitigate first ◆ ─▶ rollback:execute ◆ ─▶ verify:production ─▶ observe

blocking findings in verify, review, or quality-check:
   ─▶ implement ─▶ re-run that phase ─▶ quality-check (always last)
```

- `split-ticket`: only when the ticket fails the sizing test.
- `branch`: skipped when already on the ticket's branch or worktree.
- `scope-check`: trims scope, names what could break and the abuse cases, and settles real design choices. Stops only on a TRIM, a FLAG, or a design choice (`../ns-route/references/topic-scope-gate.md` "Scope-check gate").
- `implement`: writes every kept test (`../ns-route/references/topic-kept-tests.md` "Kept tests"): an E2E test per user-facing criterion, an integration test per rule with no screen.
- `verify:local`: the full proof (`../ns-route/references/topic-proof.md` "Proof"): every criterion walked on a real screen or request, mobile and desktop screenshots, a clip, console and requests, Lighthouse against the base, the E2E suite, and a score out of 100. Asks how to run it first (watched, hidden, manual, or skip).
- `review`: thirteen parts, reviewers scaled by risk; stops when there are findings to choose from.
- `quality-check`: shows every stage with a recommendation, you confirm once, then stages run one at a time. CI must enforce types, lint, tests, and build.
- `pr`: the stop that pushes and opens the PR also approves its report set (`../ns-route/references/pr-writing.md`): the ticket and review regions of the description, the local, preview, and production verification comments, the private evidence page, the stakeholder review, and the Shipped comment. Each is printed as it is posted.
- `rollback:prepare`: mandatory for high or critical risk, incidents, migrations, and destructive data changes; otherwise the PR's undo block covers it.
- `deploy`: preflight, then the release card. Its "merge and ship" answer is the only merge; "leave the PR open" stops here, and rerunning continues from the card.
- `observe`: reads the logs first, then the tier's checks (low, medium, high). UNHEALTHY opens with the mitigate-first decision.
- `postmortem`: incidents only, ending with the lessons card.
- `close`: runs only after HEALTHY. Ends CLOSED or NOT CLOSED, clears local evidence, and names the next ticket from real state.
- Each ticket reaches production and closes before the next starts (`../ns-route/references/topic-delivery.md` "Delivery ends in production").

### ticket

Deliver one existing ticket, or one small task with no ticket. `/ns-flow-ticket <ticket | "task">`

```
[TICKET]
```

- With a task description instead of a ticket, the flow restates scope and acceptance criteria and confirms them ◆ before branching.
- The ticket ends live, healthy, and closed; `close` names the next ticket. Once every ticket of the feature has closed: [FEATURE-END].
