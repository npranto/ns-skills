# Architecture guardrail

## Deciding whether architecture work is needed

Do not run `/ns-to-architect` after every grilling session by default. Trigger it only when the change modifies an important structural boundary: new persistence strategy, new service, new domain boundary, new external provider, new authentication model, new queue, new cache, new API contract, new infrastructure, major state architecture. Ordinary feature work (for example "add wishlist sorting") does not qualify.

When it is unclear, ask: **can the existing architecture support this?**

- **YES** -> use it, skip `/ns-to-architect`, go straight to `/ns-to-spec`.
- **MOSTLY** -> extend minimally: a delta note in the existing `docs/architecture/*` docs, not a full pass.
- **NO** -> architecture decision required: run `/ns-to-architect`.

For module, interface, and seam-level decisions, not just system diagrams, lean on `mattpocock-skills:codebase-design`.
