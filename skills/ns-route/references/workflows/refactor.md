### refactor

A small, planned refactor or opportunistic tech-debt cleanup, behavior unchanged. Larger work is [restructure](re-engineering.md#restructure). Start with `/ns-route "<refactor>"`.

```
discover? (scoped) ─▶ [TICKET] (task description as the ticket)
```

- `scope-check` is the key gate here: no bundled renames or reorganization beyond the stated goal.
- Proof: the affected flows walked on the base and on the branch, and the existing tests run on both.
