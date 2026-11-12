# Staged checks

## Staged checks

`/ns-to-quality-check` first shows every stage with its recommendation and the reason from this diff, then asks once how to proceed (my recommendation, all, one by one, core only, or a custom list). Nothing runs before that answer. The chosen stages then run strictly one at a time, each reported as it finishes, and skipped stages are always listed. On autopilot, the recommendation is taken per `../ns-route/references/core.md` "Run modes", and skipped stages are still reported.
