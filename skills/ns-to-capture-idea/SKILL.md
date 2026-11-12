---
name: ns-to-capture-idea
description: Turn a rough idea, dictated notes, screenshots, or requirements into a concise structured project brief. Capture only - no grilling, no code.
disable-model-invocation: true
argument-hint: "[project name, rough idea, or path to notes]"
---

# ns-to-capture-idea

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Phase 1 - CAPTURE. Do not scaffold, install, write production code, choose detailed architecture, or create tickets.

## Inputs

Anything the user gives: rough idea, dictated notes, screenshots, existing code, requirements. Transcribed speech is messy: interpret intent, and quote the user's own words for anything ambiguous instead of guessing.

Then ask via the multiple-choice question tool, in this order, skipping what is already known and batching only truly independent basics:

1. Project name and one-sentence pitch.
2. Who it is for, and what they do today instead (the alternative or competitor).
3. Success: how will we know it worked (one or two measurable signals).
4. MVP deadline, who builds it, with what assistance.
5. Platforms and access (web, mobile, desktop, API, internal or public, logged-in or anonymous).
6. Explicit non-goals for the MVP.
7. Must-have integrations, sensitive data (PII, payments, health), compliance, expected scale.

If `docs/product/project-brief.md` exists, update it rather than replacing it. If the project has existing code, read it first (or suggest `/ns-to-discover-codebase`). For unfamiliar markets or competitors, offer `mattpocock-skills:research` instead of guessing.

## Extract

problem, users, primary user journeys, required capabilities, constraints, deadline, scale, integrations, security/privacy, business-critical requirements, success signals, alternatives, assumptions, unknowns, risks, likely future requirements, non-goals. Separate what the user **said** from what you **inferred**.

## Output: `docs/product/project-brief.md`

Only these sections, kept concise (bullets over prose):

1. Problem statement
2. Product vision
3. Target user (and what they use today)
4. Core user journey
5. MVP capabilities
6. Success signals
7. Explicit non-goals
8. Constraints (time, team, platform, budget, compliance)
9. Known facts
10. Current assumptions
11. Risks
12. Important unresolved questions
13. Suggested improvements and blind spots

Section 13 is yours: at most 5 to 7 short, labeled **suggestions, not decisions**, covering things the user probably has not considered (for example onboarding and empty first-run experience, auth and account recovery, data export or deletion, abuse or spam, monetization, analytics, accessibility, a cheaper way to validate the idea, a feature that could be cut). Each one line with why it matters. Do not add them to MVP capabilities.

Do not resolve the unresolved questions. They feed `/ns-to-grill-me`. Ask clarifying questions when something is unclear rather than guessing.

## Finish

Show a concise summary of what was captured and stop. Suggest `/ns-to-grill-me`.
