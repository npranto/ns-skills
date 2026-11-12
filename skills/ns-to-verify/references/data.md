# Proving a schema or data change

## An additive change

A new table, a new nullable column, a new index.

1. Run the migration up, then down, then up, on a local or throwaway database. All three succeed.
2. Old code against the new schema: check out the base commit's code path (or run the existing tests) with the migration applied. Nothing breaks.
3. Read back what the change writes: the row, the column, the default.
4. A new index: confirm the query that needs it uses it (`EXPLAIN`).

## Worked example

Ticket: "Archived notes leave the main list." Adds `notes.archived_at timestamptz null`.

```
$ pnpm db:migrate      ✓ 0007_archived applied
$ pnpm db:rollback     ✓ 0007_archived reverted
$ pnpm db:migrate      ✓ 0007_archived applied
$ pnpm test notes      ✓ 48 passed   (existing tests, new schema)

select count(*) from notes;                              -> 1240   (unchanged)
select count(*) from notes where archived_at is null;    -> 1240   (nothing archived by the migration)
```

Safe because the column is nullable and has no default that rewrites rows: *measured*.

## Data that moves or is deleted

Backfills, type changes, splitting or merging columns, dropping anything. The `migration` workflow, risk at least high.

- **Expand, move, contract,** as separate tickets: add the new shape, write to both, backfill, read from the new, then remove the old. Each step can be stopped after.
- **Before:** row counts and a sample of real records for every table touched. A backup exists and its restore command has been run once against a copy.
- **The backfill** is safe to run twice, runs in batches on a large table, and can be resumed.
- **After:** row counts match what the plan predicted, the sample records hold the expected values, and no row was left in the old shape.
- **A destructive step** has its own authorization stop, with the restore plan shown.

## Safe on a large table

Name the lock each statement takes. Adding a column with a volatile default, adding a non-concurrent index, or changing a type rewrites or locks the table: say so, and use the engine's online form.

## Kept tests

A rule the data must obey (a constraint, an ownership filter, a uniqueness) gets an integration test against a real database. A migration with logic gets a test that runs it on realistic rows.
