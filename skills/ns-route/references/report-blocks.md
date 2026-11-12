# Report blocks

The building blocks for anything posted to GitHub: the PR description, the verification comments, the stakeholder review, the Shipped report. A reader should get the verdict in three seconds and the detail only if they want it.

## Order

1. Verdict banner
2. The evidence link
3. Stat strip
4. Criteria
5. Performance
6. Action blocks: rollback, what to watch
7. Detail, folded in `<details>`

## Blocks

**Verdict banner.** A GitHub alert colored by outcome: `[!TIP]` pass, `[!WARNING]` partial or needs a decision, `[!CAUTION]` fail, `[!IMPORTANT]` an action the reader must take.

```markdown
> [!TIP]
> ### 🟢 92 / 100 · SAFE TO RELEASE · preview `a73c82f`
> 3 of 3 criteria pass · 0 console errors
```

**Stat strip.** The three to five numbers that matter, in one table row. The number is the headline and the label sits under it.

```markdown
| ✅ Criteria | 🧪 Tests | 🛡 Score | ⏪ Undo | ⚠️ Risk |
|:---:|:---:|:---:|:---:|:---:|
| **3 / 3** | **48 / 48** | **92** 🟢 | **< 5 min** | **medium** |
| on preview | CI green | safe to release | revert | new column |
```

**Criteria.** One row per acceptance criterion, in the ticket's words, with a column per target that has run.

```markdown
| # | Criterion | Local | Preview | Production | Proof |
|:---:|---|:---:|:---:|:---:|---|
| 1 | Archive a note from the menu | ✅ | ✅ | - | walk, e2e test |
```

**Evidence link.** One line under the banner, saying what the page holds.

```markdown
### 🎬 📱 🖥 [Open the evidence page](https://claude.ai/artifact/…)
1 clip · 6 screenshots at two sizes · 2 Lighthouse reports. Private: ask the PR author for access.
```

**Performance,** for every change with UI: one row per touched page and screen size. The meter has ten cells, one per ten points, colored by the score's band: green from 90, amber from 50, red below. Each vital carries its own dot. Always with the change from base, and a line naming the base.

```markdown
| Page | | Performance | LCP | TBT | CLS |
|---|:---:|---|:---:|:---:|:---:|
| `/notes` | 📱 | 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **96** ▲ +2 | **1.8 s** 🟢 | **90 ms** 🟢 | **0.01** 🟢 |
| `/notes` | 🖥 | 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **99** ▲ 0 | **0.7 s** 🟢 | **0 ms** 🟢 | **0.00** 🟢 |

Base: `main` @ `4f2a9c1`. Lab numbers; TBT stands in for INP.
```

**Rollback block.** Steps someone under pressure can follow.

```markdown
> [!CAUTION]
> ### ⏪ Undo · **under 1 minute** · no data to restore
>
> | Step | Do this | Takes |
> |:---:|---|:---:|
> | **1** | Instant rollback to deployment `dpl_8fK2` | **30 s** |
> | **2** | Revert PR #482 and merge the revert | 5 min |
>
> **Roll back if** error rate on `/notes/*/archive` is above **2%** for 5 minutes
> **Confirm it worked** the Archive item is gone from the note menu
```

**Before and after,** for bug fixes and visual changes: two columns, `🔴 Before` and `🟢 After`, in words.

**Detail.** Anything long goes inside `<details><summary>…</summary>`.

## Rules

- Every number is bold, has its unit, and shows the change from base where one exists.
- Color means status: 🟢 good, 🟡 watch, 🔴 bad. One emoji per heading at most.
- Two sentences at most between blocks.
- Say what a user sees and does, unless the reader is reviewing the diff.
- A number that is not known is left out, never estimated.
