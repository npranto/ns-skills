# Launch banner

Print a compact card so it is instantly clear that new work started and from where. Fill every field truthfully. Omit rows that do not apply. Keep lines the same width.

```
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃  ▲  NEW BRANCH READY                                 ┃
  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
  ┃  branch   feat/03-create-note                        ┃
  ┃  ticket   03 - User can create a note                ┃
  ┃  base     main @ 4f2a9c1  (up to date)               ┃
  ┃  stack    none                                       ┃
  ┃  stash    none                                       ┃
  ┃  tree     clean                                      ┃
  ┃  pushed   no (local only)                            ┃
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
   main ●───────● feat/03-create-note      you are here
   next: /ns-to-scope-check .scratch/notes/issues/03-create-note.md
```

Choose the next-step line by context: `/ns-to-scope-check <ticket>` for a ticket or a bugfix (with the bug report) - the anti-overengineering gate runs right before implementing - and `/ns-to-spec` or `/ns-to-architect` for docs-only work. For a stacked branch, show the chain (`main ●─● 02-schema ●─● 03-create-note`) and the parent. For a worktree, show its path.
