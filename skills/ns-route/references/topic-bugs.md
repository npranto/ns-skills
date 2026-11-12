# Bugs

## Bugs enter differently than features

A bug does not take the feature entrance (`/ns-to-grill-me` -> `/ns-to-spec` -> `/ns-to-tickets` -> `/ns-to-implement`). It is existing behavior that is wrong, not a new decision to interrogate or a scope to ticket up front.

**Golden rule: no fix before evidence of root cause.** Not literally 100% of bugs - some are trivial and the cause is obvious on sight - but that is the default, not the exception. Reproduce end to end, as close to how a real user experiences it as possible, find the real cause, then fix.

`/ns-flow-bugfix` is this entrance. It reproduces and root-causes via `mattpocock-skills:diagnosing-bugs` - a single tight loop that already covers triage, reproduction, diagnosis, and root-causing - before any fix, then runs the fix through the same branch/scope-check/implement/understand/review/quality-check/save/pr phases as other work. Like every ticket, the fix then ships to production and closes. An incident (live in production right now) takes the same entrance in incident mode: stop the harm first (rollback or flag off), then a hotfix branch, fastest safe checks, and a mandatory rollback-prepared release. Prefer that one skill over inventing separate triage/reproduce/diagnose/root-cause phase skills unless a specific bug genuinely needs a step it doesn't cover.
