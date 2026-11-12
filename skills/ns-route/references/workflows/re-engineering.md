### Re-engineering: restructure, stack-move, rebuild, modernize

All four start by recording a **baseline**: what the system does today on its key flows (`/ns-to-verify baseline`, `ns-to-verify/references/refactor.md`). You confirm the list as "what must not change" ◆, and every later ticket is proven against it: each difference is either the ticket's stated intent or a regression. Start each with `/ns-route "<goal>"`.

#### restructure

Untangle modules, change the data model, or replace a pattern everywhere, inside one stack, behavior unchanged.

```
discover ─▶ verify:baseline ◆ ─▶ grill ◆ ─▶ architect ◆ ─▶ tickets ◆ ─▶ [TICKET] ×N ─▶ integration-check
```

#### stack-move

A working app moves to a new framework, runtime, database, or host, piece by piece, while it stays live.

```
discover ─▶ verify:baseline ◆ ─▶ grill ◆ ─▶ architect ◆ (which seam, which order) ─▶ spec ◆ ─▶ tickets ◆
   ─▶ [TICKET] ×N (old and new side by side until each flow matches) ─▶ integration-check ─▶ remove the old
```

#### rebuild

A new build of a product that already exists. The baseline is recorded from the reference product and becomes the acceptance criteria.

```
verify:baseline ◆ (of the reference) ─▶ then greenfield from capture
```

#### modernize

Old code with few tests, made safe to change before it is improved.

```
discover ─▶ verify:baseline ◆ ─▶ kept tests where the baseline shows gaps ([TICKET] ×N) ─▶ then restructure
```
