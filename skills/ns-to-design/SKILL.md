---
name: ns-to-design
description: Create a lightweight UI/UX contract (flows, layouts, states, accessibility, design tokens, ASCII wireframes) one design decision at a time, before implementation.
disable-model-invocation: true
argument-hint: "[project or feature to design]"
---

# ns-to-design

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Phase 4 - DESIGN. Act as a pragmatic senior product designer and frontend architect. Create the UX contract before feature implementation so implementation agents never redesign approved UI while coding.

## Inputs (authoritative)

`CLAUDE.md`, `CONTEXT.md`, `docs/product/project-brief.md`, `docs/adr/*`, `docs/architecture/*`. For existing UIs also inspect the current design system, tokens, and components (`/ns-to-discover-codebase`). Ask via the multiple-choice question tool for missing facts: product feel/reference apps, accessibility target (default WCAG 2.2 AA), supported breakpoints, component library in use, brand constraints.

Honor the frontend decisions in `docs/architecture/system.md` (rendering strategy, client state, i18n, performance budget). Also consider: dark mode/theming, reduced motion, content length and localization stress, and offline or slow-network behavior where relevant.

Do not reopen product or architecture decisions without a genuine contradiction. Do not scaffold, install, write production code, create tickets, or write the spec.

## Objective

Not a giant design system or Figma replacement. A lightweight explicit contract optimized for fast implementation, clarity, accessibility, responsive behavior, visual consistency, maintainability, familiar interaction patterns, and minimal custom complexity. Prefer existing component-library primitives. Do not invent reusable components merely because reuse might happen someday.

## Process

Decide **one at a time**: what needs deciding, recommendation, meaningful alternatives, tradeoff, a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box"), then ask for approval. Cover as relevant: app shell, navigation/search, primary creation interaction, item card, editor, list/grid behavior, secondary views (archive, trash, filters, settings), management UIs, pickers, search results, desktop/tablet/mobile behavior, loading, empty, error, success and saving states, conflict state, destructive confirmations, keyboard and focus behavior, accessibility.

For visual uncertainty, recommend a disposable prototype via `mattpocock-skills:prototype` rather than debating in prose.

## Design system (small)

typography hierarchy, spacing scale, radii, surfaces, borders, elevation, semantic colors, domain-specific color tokens, hover, focus, destructive, disabled and interaction states. Semantic tokens over arbitrary values. No arbitrary pixel values unless they express a real constraint. Define which components are shared primitives and which are feature-specific.

## Output

- `docs/design/ui-spec.md`: design principles, app shell, navigation, view structure, component hierarchy, creation and editing behavior, item interactions, search, secondary views, responsive behavior, loading/empty/error states, autosave/status feedback, accessibility, keyboard interactions, design tokens, shared vs feature-specific components.
- `docs/design/wireframes.md`: simple ASCII wireframes for each major view, mobile and desktop, editor, empty state, and search results.

End with **WHAT I NEED TO UNDERSTAND BEFORE IMPLEMENTATION** (the few UI/UX concepts to grasp). Then stop. Suggest `/ns-to-spec`.
