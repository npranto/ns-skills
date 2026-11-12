# Delivery and flags

## Delivery ends in production

A ticket is done when it is live, healthy, and closed, not when its PR is open. `/ns-flow-ticket` takes each ticket through PR, the release card in `/ns-to-deploy` (whose "merge and ship" answer is the only merge), `/ns-to-verify production`, `/ns-to-observe`, the Shipped comment, and `/ns-to-close`, before the next ticket starts. "Leave the PR open" on the release card stops there, and rerunning the flow continues from the card. A multi-ticket feature keeps unfinished work out of users' sight with the release strategy chosen in `/ns-to-tickets`, then ends with the feature end: `/ns-to-integration-check`, the flag on for everyone, and one Shipped report for the feature.

## Feature flags

- A flag is added only when the ticket or the release strategy calls for one. Its removal ticket is written when it is added.
- Turning a flag on or off in production is its own stop, followed by `/ns-to-observe`.
- `/ns-to-close` checks each flag the work added is removed or has its removal ticket.
- A project with no flag system uses the minimal one the release strategy agreed (an env var or a config constant), recorded in the project profile's **Flags** line.
