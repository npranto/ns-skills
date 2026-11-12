---
name: ns-to-understand
description: Human comprehension gate - produce an implementation brief and 5-minute review path for the current diff so changes are understood, not blindly accepted.
disable-model-invocation: true
argument-hint: "[ticket ref, or base ref to diff against]"
---

# ns-to-understand

Read first: `../ns-route/references/core.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Mandatory before the user accepts any significant change. Input: the ticket (ask if missing) and the diff (`git diff <base>...HEAD` plus uncommitted changes; ask for the base if unclear). Read the code, do not guess from commit messages.

Teach the architecture rather than narrating every changed line. Never hide behind "the agents handled it": the human maintains this code.

## Output: IMPLEMENTATION BRIEF

- **TICKET**
- **WHAT CHANGED**: 3-7 bullets (3 sentences max if small)
- **WHY IT WAS IMPLEMENTED THIS WAY**
- **DATA / CONTROL FLOW**: a real path, for example `UI click -> archiveNote() -> service -> repository -> Postgres -> cache/UI refresh`
- **IMPORTANT FILES TO READ**, in order, with why (only files that teach the implementation)
- **IMPORTANT FUNCTIONS / TYPES**
- **ARCHITECTURAL CONNECTION**
- **STATE MANAGEMENT**
- **ERROR BEHAVIOR**
- **AUTHORIZATION / SECURITY**
- **TEST COVERAGE** (checklist of what is proven)
- **TRADEOFFS**, **KNOWN RISKS**, **TECHNICAL DEBT INTRODUCED**
- **WHAT I SHOULD BE ABLE TO EXPLAIN AFTER READING THIS CODE**
- **5-MINUTE REVIEW PATH**: where to start, then next, then next

Then ask via the multiple-choice question tool: quiz me on it / I understand, continue / walk through a file in detail. Suggest `/ns-to-review`.
