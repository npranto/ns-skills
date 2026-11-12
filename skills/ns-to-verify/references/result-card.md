# The result card

```markdown
### Proof · 03 Archive a note · local @ `a73c82f`

**92 / 100** 🟢 **SAFE TO RELEASE** · ✅ VERIFIED · lost 8: goal 3 needs your manual check

| Goal | | Proof | Evidence |
|---|---|---|---|
| 1 Archive from the menu | ✅ | walk, e2e test | 📱 🖥 · clip |
| 2 Leaves the main list | ✅ | integration test | `queries.test.ts` |
| 3 Only the owner | ✅ | request as another user | `403` |

**Also proven** console **0** errors · **0** failed requests · E2E **4 / 4** · existing notes flows still pass
**Performance** `/notes` 📱 **96** ▲ +2 · LCP **1.8 s** 🟢 · 🖥 **99** ▲ 0
**Left out** tablet: no layout change · accessibility scan: no new control
**Risk** medium: a new endpoint, touches the `notes` table
**Safe because** the column is nullable, so old code ignores it *(measured)*
**Undo** revert the PR, under **5 min**, no data step
**View** evidence page opened · `.verification/feat-03-archive-note/evidence.html`
```

- **Verdict:** VERIFIED (every criterion has passing evidence, no new console errors or failed requests), PARTIAL (everything run passed, some rows are skipped or wait on the user: list them), or FAILED (a criterion failed or a screen is broken).
- **Score and release verdict:** `references/evidence.md`. This is the one score every other skill quotes.
- Mark each claim *measured*, *inferred*, or *guess*.
- FAILED: name the failing step with its error line, keep the trace and logs locally, and stop. Nothing continues to a PR or a deploy.
