---
name: ns-to-split-ticket
description: Refine ONE existing ticket into the smallest coherent, independently verifiable implementation units (recursive sizing, about 15-minute human review each). Propose first, write files only after approval.
disable-model-invocation: true
argument-hint: "<ticket path or id>"
---

# ns-to-split-ticket

Read first: `../ns-route/references/core.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Refine ONE ticket. This is not project replanning: do not reconsider sibling tickets, redesign the parent spec, or implement anything. If no ticket is given, ask which one (list candidates from the tracker).

## Inputs

CURRENT_TICKET, its parent `spec.md`, `CONTEXT.md`, and only the architecture/design docs relevant to the ticket. All settled. The ticket defines the scope boundary. Human comprehension is the binding constraint: an unfamiliar engineer should understand each resulting change in about 15 minutes.

## When to split

Any one is enough:

- **Too large:** it fails the sizing test below.
- **A bug fix carrying extra changes:** a refactor, a rename, a dependency change, or a second bug. The fix ships alone.
- **Several isolated domains:** each part could land and be reverted without the others.

## Sizing test (any meaningful failure means split)

1. Exactly one primary concept, capability, integration, or component?
2. Purpose explainable in one sentence?
3. Result independently demonstrable or verifiable?
4. One fresh context can understand, implement, test, explain, and review it?
5. Important diff understandable in about 15 minutes?
6. Does it combine independent concerns that could land one after another?
7. Does it need several unrelated architectural boundaries at once?
8. Would splitting yield real checkpoints, or artificial fragments?

**Recursive:** apply the same test to every candidate and split again until each leaf is one cohesive concept. Stop when further splitting creates nothing independently verifiable.

## Valid leaves

Need not be user-visible: buildable scaffold, env validation, provider integration, DB connection, one migration, one route boundary, one provider wrapper, one UI primitive, one domain behavior, one server mutation, one focused interaction, one integration of existing pieces. Each must answer "What can I demonstrate or verify when this is done?"

Split on behavioral or architectural boundaries, not database/backend/frontend/tests layers. Prefer a small vertical slice. Do not create "helper function", "add type", "write tests" tickets. Tests live with the behavior they protect. No speculative infrastructure.

## First pass output (write nothing yet)

- **Assessment**: ticket, VERDICT (appropriately sized / requires decomposition), WHY.
- **Proposed breakdown**, per leaf `<ID> - <Title>` with: Purpose (one sentence), Blocked by, Scope, Out of scope, Demo/verification, Expected conceptual surface, Review-budget assessment, Risk/hotspot.
- **Dependency graph** (tree or arrows) and BLOCKED BY / UNBLOCKS per leaf. Prefer a simple chain when shared files make parallel work risky.
- **Parallelism**: which leaves are safe concurrently, and why.
- **Coverage check**: map every requirement of the parent to leaves. Confirm no acceptance criterion dropped, no new behavior invented, no needless duplication.
- **Alternatives**: always at least one other split and "keep as one", each with its real cost (for example "one PR of about 220 lines across 3 domains: faster to open, harder to review and to revert"). Recommend one.

Then ask via the multiple-choice question tool for approval (approve / adjust / leave as is) and STOP.

## After approval

1. Create leaf ticket files in the same issue directory, IDs preserving dependency order (`03.01-...`, `03.01.02-...`).
2. Update the parent into an umbrella/index: original outcome, original acceptance criteria, child list, completion checklist, status showing implementation is delegated. Keep its history, and move each entry under its `## Decisions` to the leaf it now belongs to.
3. Touch no unrelated tickets. Do not implement or run `/ns-to-implement`.
