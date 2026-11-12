---
name: ns-to-spec
description: Consolidate settled decisions into one implementation spec (spec.md) for a project, feature, or bug. A record of decisions, not a place to invent behavior.
disable-model-invocation: true
argument-hint: "[feature-slug]"
---

# ns-to-spec

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/topic-learn-box.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Run once decisions are sufficiently settled. The spec records decisions already made. **Do not quietly invent product behavior.** If something is undecided, list it under OPEN QUESTIONS and ask the user via the multiple-choice question tool whether to resolve it now (grill it) or carry it.

## Inputs

Ask for the feature slug if not given. Read whatever exists: brief, `CONTEXT.md`, `docs/adr/*`, `docs/architecture/*`, `docs/design/*`, the bug report or feature description, and the codebase map. Follow the philosophy of Matt Pocock's spec capability if installed.

## Output: `.scratch/<slug>/spec.md` (or the tracker's spec location)

Size the spec to the work. The user can ask for the full template at any size.

| The work | The spec |
|---|---|
| One ticket | None. The ticket's scope and acceptance criteria are the record. Say so and stop. |
| A small feature, two to four tickets | One page: PROBLEM, GOALS, NON-GOALS, USER FLOWS, ACCEPTANCE CRITERIA, DECISIONS, OPEN QUESTIONS, plus only the sections below that a settled decision touched. |
| A new project or a large feature | Every section below that a settled decision belongs in. |

Full template: PROBLEM, GOALS, NON-GOALS, USER FLOWS, DOMAIN MODEL, ARCHITECTURE CONSTRAINTS, DESIGN CONTRACT, FUNCTIONAL REQUIREMENTS, NON-FUNCTIONAL REQUIREMENTS, AUTHENTICATION, AUTHORIZATION, VALIDATION, API CONTRACT, INTEGRATIONS, DATA LIFECYCLE AND PRIVACY, ERROR BEHAVIOR, PERFORMANCE EXPECTATIONS, ACCESSIBILITY, OBSERVABILITY, ROLLOUT AND ROLLBACK, TESTING SEAMS, ACCEPTANCE CRITERIA, OUT OF SCOPE, DECISIONS, OPEN QUESTIONS.

Rules:

- A section with no settled decision is left out.
- **DECISIONS** is the planning decision trail: one entry per decision settled before tickets existed (what was decided, what was rejected, the principle by name). Carry over the ones the brief holds.

- Acceptance criteria describe externally verifiable behavior whenever possible.
- Keep architecture decisions and product requirements distinguishable.
- Use `CONTEXT.md` vocabulary. Flag any conflict with an ADR explicitly.
- For a bugfix spec: reproduction steps, expected vs actual, root cause (once known), fix constraints, regression test.

Stop after writing. Suggest `/ns-to-tickets`.
