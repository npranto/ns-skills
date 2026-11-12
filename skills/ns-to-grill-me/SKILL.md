---
name: ns-to-grill-me
description: Grill a project, feature, or plan one decision at a time until product and engineering ambiguity is low, recording vocabulary in CONTEXT.md and costly decisions as ADRs.
disable-model-invocation: true
argument-hint: "[brief path, feature name, or plan to grill]"
---

# ns-to-grill-me

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-architecture-guardrail.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Phase 2 - GRILL. Inputs: `docs/product/project-brief.md` (or the feature description / plan the user names), plus `CONTEXT.md` and `docs/adr/` if present. Outputs: `CONTEXT.md`, ADRs, and settled decisions recorded back in the brief or spec draft.

## Rules

- Delegate the questioning philosophy to `mattpocock-skills:grilling`, and vocabulary/ADR upkeep to `mattpocock-skills:domain-modeling`. If unavailable, follow the loop below inline.
- Ask **exactly one** decision question at a time. Never batch.
- For each decision: give context, explain why it matters, give your recommendation for this specific scope and timeline, list meaningful alternatives with tradeoffs, end with a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box"), then ask via the multiple-choice question tool (recommended option first).
- A call only the user can make (risk tolerance, budget, acceptable downtime, a scope cut) is asked with the stakes stated plainly and no recommendation.
- Investigate the repo instead of asking about facts it can answer.
- Build the list of open decisions from the brief's unresolved questions, then its risks and the "Suggested improvements and blind spots" section (each is a proposal to accept, defer, or reject, not a settled requirement), then the decision branches you discover. Challenge weak success signals and unstated assumptions.
- Order the list: a decision that depends on another comes after it. Among decisions that do not depend on each other, one-way doors (expensive to reverse: data model, auth provider, a public API shape) come first. Each answer can open new decisions; add them and reorder.
- Identify non-goals explicitly.
- Agreement locks that decision only. Do not implement.
- Do not write application code, scaffold, write the spec, or create tickets.

## Recording

- Stable vocabulary goes in `CONTEXT.md`: a concise glossary of canonical terms and relationships, with `_Avoid_` entries for competing terms. It is not a copy of the brief and not a spec.
- Only expensive-to-reverse, surprising, real-tradeoff decisions qualify for an ADR. Offer the ADR, do not auto-write one per decision.
- Product requirements and ordinary implementation decisions stay in the brief.
- Every settled decision also goes on the decision trail (`../ns-route/references/core.md` "Artifact locations"): for a ticket-level grill, the ticket's `## Decisions`; for planning, the spec's DECISIONS section, or the brief until a spec exists.

## Domain-model catch-up mode

If the user says grilling was already done, do not redo it. Read the brief, extract only what belongs in the domain model, create or update `CONTEXT.md`, point out decisions that qualify for ADRs and offer them, and change no product decisions.

## Finish

Summarize what was settled, what remains open, and files touched. Apply the architecture guardrail in `../ns-route/references/topic-architecture-guardrail.md` ("Deciding whether architecture work is needed") before suggesting a next step: suggest `/ns-to-architect` only if a settled decision touches a structural boundary, otherwise suggest `/ns-to-spec` directly.
