---
name: ns-to-postmortem
description: Write a blameless incident postmortem for engineering and leadership - timeline, impact, root cause, contributing factors, and action items with owners. Runs after /ns-to-observe reports HEALTHY for an incident; produces an internal record, not a customer-facing page.
disable-model-invocation: true
argument-hint: "[incident summary, PR, or deploy/observe summary]"
---

# ns-to-postmortem

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-tools.md`, `../ns-route/references/principles.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Written for engineers, SRE, and leadership: technical, specific, and blameless. This is not `/ns-to-stakeholder-brief` - no simplifying, no preview link, no "when it ships." The PR's stakeholder comments already explain the fix in plain words; a customer-facing page beyond them is `/ns-to-stakeholder-brief`'s shareable page, offered separately.

## Gather

Reuse whatever this session already has: the incident report, `mattpocock-skills:diagnosing-bugs`'s reproduction and root cause, the fix PR, `/ns-to-deploy`'s release card (and its full release plan when there was one), the rollback plan, the mitigate-first decision, and `/ns-to-observe`'s verdict and evidence (including the rollback threshold, if one was crossed). Ask via the multiple-choice question tool for whatever is missing, especially exact detection and resolution timestamps - never estimate a timeline from memory.

## Report contents

Blameless: describe what the systems and process did, not who made a mistake.

1. **Summary** - one paragraph: what broke, for how long, who was affected.
2. **Impact** - user-facing effect, duration, scope (percentage of traffic, specific customers or regions, revenue or SLA impact if known).
3. **Timeline** - timestamped sequence: start, detection (and how - alert, report, other), key investigation steps, mitigation, resolution.
4. **Root cause** - the actual mechanism, not just the trigger (a bad deploy is a trigger; the missing safeguard that let it reach production is the cause).
5. **Contributing factors** - anything that made detection slower or impact worse than it should have been (missing alert, no feature flag, insufficient test coverage, unclear runbook).
6. **What went well** - what limited the impact or sped up resolution.
7. **Action items** - concrete, each with an owner and a due date or ticket, not vague intentions. Every action item becomes a ticket via `/ns-to-tickets` unless one already exists - never left as prose in the report nobody will action.
8. **Related links** - incident channel/thread, fix PR, deploy record, observe evidence, this report's ticketized action items.

## Publishing

Ask where it should live: a file in the repo (default `docs/incidents/NNNN-slug.md`, following the ADR numbering convention), or wherever the team's existing incident log lives (check `docs/agents/issue-tracker.md` first). Not a claude.ai Artifact by default - this is an internal engineering record, not a shareable page. If the incident revealed a structural gap, offer `mattpocock-skills:domain-modeling` for a new ADR.

## The lessons card

After the record is written, and kept out of it, give the user a short lessons card in chat. The decisions made under pressure are the best teaching material, and right after the incident is when the reasoning is still fresh.

```markdown
### Lessons · duplicate invoice emails

| Decision under pressure | What we chose | Principle | With hindsight |
|---|---|---|---|
| Roll back or fix forward | rolled back in 40 s | Mitigate, then diagnose | right: the fix took 50 minutes |
| Where to put the guard | in the retry handler | Guard at the boundary | should also be idempotent at the send |

**What would have caught it earlier** an alert on send volume per invoice
**Ask yourself** what made rolling back safe here, and when would it not be?
```

One row per decision in the incident's decision trail (the ticket's `## Decisions` and the mitigate-first answer). Each principle is cited by its exact name from `../ns-route/references/principles.md`.

## Do not

Do not name individuals as the cause. Do not simplify or omit the technical root cause for readability - that is what `/ns-to-stakeholder-brief` is for, not this. Do not leave action items unassigned or ticketless.
