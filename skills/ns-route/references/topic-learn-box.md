# Learn box

## Learn box

Every decision asked in grill, wayfinder, architect, design, and scope-check's design section ends with a short Learn box, so the user builds judgment rather than just approving:

```markdown
> 💡 **Learn: one-way and two-way doors**
> A nullable column is a two-way door: dropping it later loses nothing.
> **Flips when** archived rows outnumber live ones and slow every list.
> **Ask yourself** which option makes "restore" hardest, and why?
```

- The heading names the principle that actually decided the choice, by its exact name from `../ns-route/references/principles.md`.
- One or two lines apply it to this decision, in this repo's terms.
- **Flips when** names the concrete condition that would change the answer.
- **Ask yourself** is one question the user can answer from the options shown.
- A "your call only" question (risk tolerance, budget, downtime, a scope cut) carries no recommendation; its Learn box names what is at stake instead of a pick.
