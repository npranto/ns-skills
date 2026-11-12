---
name: ns-to-wayfinder
description: Resolve fundamental architectural or product uncertainty one decision ticket at a time, across as many sessions as it takes, before a spec can be trusted. For destinations with too many interconnected unknowns for one grilling session - not for ordinary features.
disable-model-invocation: true
argument-hint: "[destination statement, or leave blank to resume docs/product/wayfinder/map.md]"
---

# ns-to-wayfinder

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Pre-phase, ahead of GRILL/ARCHITECT. For a destination with too much interconnected uncertainty to settle in one session - not a replacement for `/ns-to-grill-me`. Run `/ns-to-grill-me` instead if the open questions can plausibly be settled in one sitting.

## Self-check before starting

Ask: "Can this get from idea to a trustworthy spec in one session?" If yes, stop and suggest `/ns-to-grill-me` instead - do not run Wayfinder out of caution alone. Genuine signals for Wayfinder: replacing a subsystem (CMS, auth provider, database), introducing multi-tenancy, splitting a monolith, an AI workflow/agent platform, a redesign where the *behavior* itself is unsettled, or a greenfield program with several interlocking unknowns. The tell is the "fog/frontier" pattern: settling one question predictably exposes another you couldn't have listed up front.

## Inputs

`docs/product/project-brief.md` if present - Wayfinder needs a destination, not just a scope; run `/ns-to-capture-idea` first if there is none. `docs/product/wayfinder/map.md` if resuming. `CONTEXT.md`, `docs/adr/*`, `docs/architecture/*` for anything already settled - never reopen a settled decision here without a genuine contradiction (`../ns-route/references/core.md` rule 5).

## The map: `docs/product/wayfinder/map.md`

The frontier, one place. Rewrite it in place each session - do not let it accumulate history, individual ticket files carry that.

```markdown
# Wayfinder: <destination>

## Destination
<one or two sentences - where this ends up, not how it gets built>

## Resolved
- [DT-01](wayfinder/01-slug.md) - <one-line decision>

## Open (frontier)
- [DT-04](wayfinder/04-slug.md) - <question> - type: decision
- [DT-05](wayfinder/05-slug.md) - <question> - type: research - blocked by DT-04

## Parked
- <question> - not yet relevant, or blocked on something outside this project's control
```

Ticket types:

| Type | Means | Delegate to |
|---|---|---|
| `decision` | Settle by reasoning through tradeoffs together | Inline, same discipline as `/ns-to-grill-me`, ending with a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box") |
| `research` | Factual unknown (does provider X support Y, how does library Z behave) | `mattpocock-skills:research` |
| `prototype` | Discussion alone can't settle it - build a disposable variant and observe | `mattpocock-skills:prototype` |
| `grill` | A call only the human can make - risk tolerance, budget, downtime, scope cuts | Ask directly, state the stakes plainly, do not recommend an answer |

## Ticket file: `docs/product/wayfinder/NN-slug.md`

`Status: open | in-progress | resolved | parked` and `Blocked by: NN` near the top, then:

QUESTION, WHY IT MATTERS, TYPE, CONTEXT, OPTIONS (with tradeoffs), RECOMMENDATION (skip for `grill` tickets), RESOLUTION (filled once settled), NEW QUESTIONS SURFACED (fill in as you resolve it - this is how the frontier grows).

## Loop (repeat every session)

1. Read the map. If it does not exist yet, create it: state the destination (ask via the multiple-choice question tool if unclear), then decompose only the *visible* first layer of unknowns into decision tickets. Do not try to enumerate the whole tree up front.
2. Pick the next unblocked ticket. If several are equally ready and order matters, ask which to take first.
3. Resolve it by its type (see table above), one ticket at a time - never batch decisions.
4. Write the RESOLUTION into the ticket, mark it resolved, and list any new questions it exposed as new ticket files under NEW QUESTIONS SURFACED.
5. Update the map: move the ticket to Resolved, add newly surfaced tickets to Open, re-check Parked for anything now relevant or unblocked.
6. Stop. Summarize what was resolved, what's newly open, and what's still blocked. Ask via the multiple-choice question tool: continue to the next ticket now (Recommended if several are ready and cheap), or stop here and resume later - files on disk carry the handoff, per `../ns-route/references/core.md`.

## Done

The map is clear when every ticket is resolved or explicitly parked as not-yet-relevant. At that point, summarize the settled decisions, offer ADRs for the costly-to-reverse ones via `mattpocock-skills:domain-modeling`, and suggest `/ns-to-architect` (if the decisions need to become formal architecture docs) or straight to `/ns-to-spec` if they are already concrete enough to record as-is.

## Do not

Do not write implementation tickets here (that's `/ns-to-tickets`, after the spec). Do not write production code, only a prototype's throwaway scope. Do not enumerate the entire decision tree in one pass - let the frontier reveal itself. Do not resolve a `grill` ticket on the user's behalf, and do not silently reopen a Resolved ticket - if new information contradicts it, surface that explicitly and let the user decide.
