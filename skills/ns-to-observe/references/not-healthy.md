# Not healthy: mitigate first

Stop and print a decision. The first question is how to stop the harm, not how to fix it.

```markdown
### 🔴 Production check failed · 03 Archive a note

**Seen** `POST /notes/:id/archive` returns 500 · 4 of 4 requests
**Since** the deploy of `a73c82f`, 3 minutes ago
**Evidence** *measured:* the log line `column "archived_at" does not exist`
**Likely cause** *inferred:* the migration did not run in production

| | Option | Time | Leaves |
|---|---|---|---|
| **A** (Recommended) | instant rollback to the previous deployment | ~30 s | old code live, a PR to revert |
| B | run the missing migration | ~2 min | new code live, if it works |
| C | leave it and investigate | - | users keep hitting the error |

**Why A** it is certain and takes seconds. B is a fix made under pressure on an inference.
```

End it with a Learn box (`../ns-route/references/topic-learn-box.md` "Learn box"; usually "Mitigate, then diagnose") and ask via the multiple-choice question tool. Recommend the rollback (or a flag off) unless the evidence shows the problem is harmless, or rolling back would itself do damage (data written since the deploy would be lost). On a rollback, hand off to `/ns-to-rollback` Execute with this evidence and the threshold that was crossed: it owns confirming the go-ahead and executing. Never roll back without confirmation.
