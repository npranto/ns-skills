# Compose the workflow

**High-uncertainty override (check this first, before baselines):** if Uncertainty = high AND Scope is `large` or `program` AND Sessions expected is `several` or `many`, put the `wayfinder` workflow (`/ns-flow-wayfinder`) at the front of the sequence instead of composing `/ns-to-grill-me` + `mattpocock-skills:prototype` + `mattpocock-skills:research` directly. Wayfinder is exactly that composition, tracked across sessions as a resumable decision frontier instead of ad hoc. Its self-check will bail back out to `/ns-to-grill-me` if the uncertainty turns out to be settleable in one sitting after all. Feed its cleared decisions into the task type's workflow, starting at `/ns-to-architect` (or straight to `/ns-to-spec` if the decisions are already concrete). This applies regardless of task type - it is common for `migration`, `refactor`, `infrastructure`, and `greenfield`/`program`-scope work, but not exclusive to them.

Otherwise, the baseline is the task type's workflow file in `../ns-route/references/workflows/`, expanded through its shared blocks (`../ns-route/references/workflows/shared-blocks.md` for [PLAN] and [FEATURE-END], `../ns-route/references/workflows/ticket.md` for [TICKET]). Then apply the modifiers below. Reference real skills only - do not invent phases.

**Modifiers** (apply on top of the baseline, do not re-derive it):

| Dimension value | Effect |
|---|---|
| Scope tiny/small | Drop `/ns-to-spec`, `/ns-to-tickets`, and `/ns-to-split-ticket`; send the task description straight to `/ns-flow-ticket`. Keep `/ns-to-scope-check` - small scope is exactly where speculative abstraction creeps in unnoticed. |
| Scope large/program | Insert `/ns-to-split-ticket` per ticket. Sessions expected = many and tickets are parallel-safe and low or medium risk: offer "hand to an agent" (`/ns-flow-delegate`) instead of running tickets one at a time. |
| Uncertainty low | Drop `/ns-to-grill-me` (or `mattpocock-skills:grilling` directly) and `mattpocock-skills:prototype`. |
| Uncertainty medium | Include `/ns-to-grill-me`, scoped to the open questions only. |
| Uncertainty high | Include `/ns-to-grill-me` plus `mattpocock-skills:prototype` for a design/interaction unknown, and `mattpocock-skills:research` for a factual unknown. Do not let the agent guess either. |
| Codebase familiarity familiar | Drop `/ns-to-discover-codebase` if the map is current; otherwise refresh it. |
| Codebase familiarity partially-known/unfamiliar | Include `/ns-to-discover-codebase`, scoped to the affected area. |
| Security sensitivity none | No extra gate. |
| Security sensitivity moderate | Weight `/ns-to-review` part C (security) and the quality-check security-relevant stages; no extra skill needed. |
| Security sensitivity sensitive | Add an explicit security decision pass inside `/ns-to-architect` (identity, API contract, abuse/resilience sections), then run the `security-review` skill as a mandatory gate before `/ns-to-quality-check`. If the security boundary itself is the source of open-ended uncertainty (new trust model, provider migration), consider `/ns-flow-wayfinder` for the orientation pass instead of going straight to `/ns-to-discover-codebase` - see the high-uncertainty override above. |
| Data risk none | Drop any migration-plan step. |
| Data risk schema | Cover it in `/ns-to-architect`'s data-model section and `/ns-to-review` part J (data and compatibility); no separate migration plan needed. |
| Data risk migration | Apply the `migration` workflow's safety steps regardless of task type: expand/contract plan in `/ns-to-architect`, mandatory migration-safety stage in `/ns-to-quality-check`, mandatory `/ns-to-rollback` (Prepare), detailed MIGRATIONS section in `/ns-to-deploy`, High-tier `/ns-to-observe` (migration validation) after it. |
| Data risk destructive | Same as migration, plus an explicit authorization gate before the destructive step executes, and a mandatory backup/restore plan in `/ns-to-deploy` - covered by `/ns-to-rollback` (Prepare)'s data restoration question. Risk is forced to at least high (see escalation overrides). |
| Risk/reversibility high, difficult, or worse | Prefer `/ns-to-split-ticket` even at medium scope (smaller review surface), keep `/ns-to-understand` and `/ns-to-review` mandatory, do not skip `/ns-to-verify`, and give preview and production the full proof (`../ns-route/references/topic-proof.md` "Proof"). If `/ns-to-deploy` is in the sequence, insert mandatory `/ns-to-rollback` (Prepare) before it, and `/ns-to-observe` runs at its High tier, with a rollback threshold agreed before observing. |
| Sessions expected several | Recommend clearing context between planning phases, as `ns-flow-new-project` does; files on disk carry the handoff. |
| Sessions expected many | See scope large/program above for `/ns-flow-delegate`. |
