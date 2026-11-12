---
name: ns-to-scope-check
description: Fast gate run immediately before implementation - trims unneeded scope, names what the change could break and why it is safe, lists abuse cases, and settles real design choices with you before any code.
disable-model-invocation: true
argument-hint: "<ticket path or id>"
---

# ns-to-scope-check

Read first: `../ns-route/references/core.md`, `../ns-route/references/topic-scope-gate.md`, `../ns-route/references/topic-learn-box.md`, `../ns-route/references/principles.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.
Cite principles by name from `../ns-route/references/principles.md`.

Runs immediately before `/ns-to-implement`, on the ticket or fix about to be built. Its job is to catch unnecessary scope, hidden breakage, and unguarded attack paths before they are written, and to put any real design choice to the user. It is a fast pass, not a redesign, and it writes no project file except the ticket's `## Decisions` after the user answers.

## Input

A ticket (its SCOPE, OUT OF SCOPE, and ACCEPTANCE CRITERIA sections), the confirmed restatement of a task with no ticket (`ns-flow-ticket` "Input"), or for a bug, the root-cause and fix plan from `mattpocock-skills:diagnosing-bugs` / `ns-flow-bugfix` step 4. Ask if none is given.

Read the code the change touches, and how this codebase already solves the nearest similar problem. Done when every file that will change is named.

## Checklist

Answer each against the ticket or fix plan as written, not against what would be nice to have:

1. **What exactly is required?** Restate the acceptance criteria and the demoable outcome in one or two lines.
2. **What is explicitly out of scope?** Pull it from the ticket's OUT OF SCOPE section, or state that none was written.
3. **What abstractions are actually necessary?** List any new interface, base class, config layer, or generalization the plan introduces. For each, name the concrete second use case that justifies it today. No second use case, no abstraction.
4. **What dependencies are actually necessary?** List any new package, library, or service the plan pulls in. For each, could the standard library or an already-installed dependency do this instead?
5. **Are we modifying unrelated code?** List every file the plan expects to touch. Flag any file not required to satisfy the acceptance criteria.
6. **Are we "cleaning up" things the ticket didn't ask for?** Flag any rename, reformat, reorganization, or refactor bundled in that isn't required to implement the ticket.
7. **Could the implementation be smaller?** State the smallest change that would satisfy every acceptance criterion and compare it to the plan.
8. **What could break?** See "Blast radius".
9. **What could someone abuse?** Only when the change touches something to attack: user input, auth, another user's data, files, money, or an external call. See "Abuse cases".
10. **Is there a real design choice?** More than one plausible structure for the change (where the data lives, who owns the behavior, what the caller must know). See "Design section". One obvious structure: say so in one line.

## Blast radius

1. **Find the one fact the change is safe because of.** Most changes that look risky are safe because of a single fact, such as "the new column is nullable, so old code ignores it". Name it, and how far it was proven:

   | Level | Means |
   |---|---|
   | ran it | a test, script, or command against the real code showed it |
   | traced it | you walked the failure step by step and it does not reach |
   | unproven | you believe it, and nothing was run or traced |

2. **Look where a symbol search stops:** the JSON an API returns and who reads it; a column read by another query, job, or service; a stored or cached shape written by the old code; a feature flag, env var, or config key; when things run (build time, request time, a cron, a retry); code two or three hops downstream of a changed function.
3. **List each remaining risk:** how it breaks, the `file:line`, how likely and how bad, and how to check. Keep cleared risks in a short separate list.

```markdown
**Safe because** the column is nullable, so old code ignores it. *Ran: migration up and down.*
**Still at risk** the nightly export reads `notes` directly (`jobs/export.ts:41`): add the filter.
```

A remaining risk with a clear fix inside the ticket's scope is OK, and it becomes a regression check in implement's verification plan. A risk with no fix in scope, or an unproven safety fact on shared code, is a FLAG.

## Abuse cases

Read `references/abuse-cases.md` and follow it when the change touches something to attack.

## Design section

Read `references/design-section.md` and follow it when there is a real design choice.

## Output

Print one table: Item | Finding | Verdict (OK / TRIM / FLAG / CHOOSE), then the blast-radius lines, the abuse-case table when it applies, and the design section when there is one.

- **All OK:** say so in one line and hand off straight to `/ns-to-implement`. No separate approval when the plan is already minimal and nothing is unresolved.
- **Any TRIM or FLAG:** stop and ask via the multiple-choice question tool: trim to the smaller scope (Recommended), keep the larger scope with a stated reason, or escalate per `/ns-to-implement`'s Escalation section if trimming means the ticket itself needs re-splitting or rewriting (loop back to `/ns-to-tickets` or `/ns-to-split-ticket`).
- **CHOOSE (a design choice):** stop and ask via the multiple-choice question tool with the designs as options (recommended first), plus "combine" and "dig deeper on one". An answer that changes the plan: reprint the section and ask again.

Record each answer in the ticket's `## Decisions` (a task with no ticket: `progress.md`): trims made, risks or abuse cases accepted with the user's reason, and the design picked with what was rejected and its principle. Do not proceed to implementation until every stop resolves.

## Finish

Hand off to `/ns-to-implement`, carrying forward the confirmed scope (the abstractions, dependencies, or files dropped from the plan), the chosen design, each remaining risk as a regression check, and each abuse case as a test for the verification plan.
