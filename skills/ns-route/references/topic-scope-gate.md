# Scope-check gate

## Scope-check gate (anti-overengineering)

`/ns-to-scope-check` runs immediately before every `/ns-to-implement` call - wired into `/ns-flow-ticket` (the shared inner loop) and `/ns-flow-bugfix`, and inserted directly into any baseline in `/ns-route` that reaches `/ns-to-implement` without going through a flow (incident, refactor/tech-debt, performance, dependency, infrastructure). It checks the plan against the ticket or fix, not against what would be nice to have: what's actually required, what's explicitly out of scope, which abstractions and dependencies are actually necessary (a second concrete use case today, not a hypothetical future one), whether unrelated files are being touched, whether unasked-for cleanup has crept in, and whether the change could be smaller.

It also checks what the change could break (the one fact it is safe because of, and the risks a symbol search misses) and, when there is something to attack, the abuse cases and what stops each.

It is a fast pass, not a redesign. When the plan is already minimal and nothing is left unresolved, it says so in one line and hands off to `/ns-to-implement` without a separate approval. It stops and asks via the multiple-choice question tool only when it finds something to trim, a risk or abuse case with nothing stopping it, or a real design choice: more than one plausible structure for the change. A design choice is shown as designs side by side with a pick and a Learn box, and the user's answer is recorded in the ticket's `## Decisions`.
