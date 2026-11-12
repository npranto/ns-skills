# The PR description

Two regions, written by `/ns-to-pr`, edited by region and never replaced (`../ns-route/references/pr-writing.md`). Built with the blocks in `../ns-route/references/report-blocks.md`.

## Ticket region (at open)

Written once, from the ticket file, in the ticket's own words.

```markdown
<!-- ns-pr:ticket -->
## 🎫 Ticket
**03 - Archive a note** · feature · risk medium · [spec](…)

**Outcome** A user can archive a note and find it under Archived.

**Acceptance criteria**
1. Archive a note from the menu
2. An archived note leaves the main list
3. Only the owner can archive a note

**In scope** … **Out of scope** …
<!-- /ns-pr:ticket -->
```

## Review region (after the preview check)

Read the current body. Replace only what sits between the review markers, or append the region. Remove the "Preview check running" line. Then read the description again and confirm the ticket region is unchanged.

````markdown
<!-- ns-pr:review -->
## ✅ Ready for review
> [!TIP]
> Users can archive a note and find it under Archived.

| ✅ Criteria | 🧪 CI | 🛡 Score | ⚡ Performance | ⏪ Undo | ⚠️ Risk |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **3 / 3** | **5 / 5** green | **92** 🟢 | **96** 📱 · **99** 🖥 | **< 5 min** | **medium** |
| local and preview | E2E **4 / 4** on the preview | safe to release | on the preview | revert | new column |

### 🔗 Try it
**Preview:** <preview URL>
🎬 📱 🖥 **Evidence page:** https://claude.ai/artifact/… (private: ask the author for access)
**Verification:** the Local and Preview comments below hold the proof, the performance numbers, and the CI checks.

| # | Criterion | Steps on the preview |
|:---:|---|---|
| 1 | Archive a note from the menu | Open any note > menu > Archive |
| 3 | Only the owner can archive | Sign in as a second user and open the first user's note URL |

### 🧭 What changed and why
- **Design:** an `archivedAt` column on notes. Not a separate table: restore could fail halfway.
- **Could break:** three list queries now filter on `archivedAt`. Safe because the column is nullable (measured).
- **Read the diff in 5 minutes:** migration > `notes/archive.ts` > `notes/queries.ts` > the two components (the `/ns-to-understand` review path).
- **Decisions:** one line each, from the ticket's `## Decisions`.

> [!CAUTION]
> ### ⏪ Undo · **under 5 minutes** · no data to restore
> | Step | Do this | Takes |
> |:---:|---|:---:|
> | **1** | Instant rollback to deployment `dpl_8fK2` | **30 s** |
> | **2** | Revert this PR and merge the revert | 5 min |
>
> **Confirm it worked** the Archive item is gone from the note menu

<details><summary>Code review · 13 parts · approve with nits</summary>

The report from `.verification/<branch>/review.md`: the parts table, then each finding with what was done about it.

</details>

<details><summary>Quality check · 15 stages · 13 passed · 2 skipped</summary>

The summary from `.verification/<branch>/quality-check.md`: every stage row, what was not checked, and the CI line.

</details>

<details><summary>Follow-ups, migrations, and env</summary>

- **Follow-ups:** #07 bulk archive.
- **Migrations and env:** one additive migration, no new env vars.

</details>
<!-- /ns-pr:review -->
````

## Rules

- **The proof lives in the verification comments.** The description keeps the stat strip and points at them and at the evidence page. It repeats no table of theirs.
- **The two folds carry the real tables,** as review and quality-check printed them. A reviewer should not have to ask what was checked. A phase that did not run says so in its fold's summary line.
- **The score** is the one from `/ns-to-verify`, quoted as it is.
- **Undo** names the real deployment, flag, command, or version, with the time each step takes. Check each step would work: the previous production deployment exists, the migration is reversible. A step that is not mechanical or takes over a minute: say so. With versioning, step 1 is the Rollback workflow with the version production runs today.
- **Flags, migrations, and env changes** are named when there are any. A flag gets a row: name, default, how to turn it on.
- **Delegate mode** adds two more folds: the scope-check output with each decision the agent made, and the `/ns-to-understand` brief.
- **An accepted risk** (a CI core check declined in quality-check, a scope-check flag kept) is named with the user's reason.
- Drop a section only when it does not apply.
