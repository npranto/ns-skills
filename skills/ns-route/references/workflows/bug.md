### bug

Wrong behavior that is not live-broken. Reproduce before fixing. `/ns-flow-bugfix "<bug report>"`

```
discover? ─▶ branch (fix/) ─▶ mp:diagnosing-bugs (reproduce end to end) ─▶ root cause + fix plan ◆
   ─▶ spec? ◆ ─▶ scope-check ─▶ implement (mp:tdd: failing regression test first)
   ─▶ verify:local ◆ (the original failure, then the same steps passing) ─▶ understand
   ─▶ review ◆ ─▶ quality-check ◆ ─▶ save ◆ ─▶ pr ◆ ─▶ the rest of [TICKET], from rollback:prepare? to close
```

- No fix before evidence of root cause (`../ns-route/references/topic-bugs.md` "Bugs enter differently than features").
- `spec`: a short bugfix spec for non-trivial bugs.
- The fix ships alone, to production, like any ticket. Its stakeholder review explains how the bug was caught and fixed.
