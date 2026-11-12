# Baseline, and proving behavior did not change

"Behavior unchanged" can only be checked if the behavior was written down first.

## Recording a baseline (`/ns-to-verify baseline`)

Run once, before the first change of a restructure, stack move, rebuild, or modernization.

1. **List the key flows.** Use the project verification skill's feature map. None exists: run `setup` first, so there is one.
2. **Show the list and stop:** "this is what must not change". The user adds, removes, or confirms.
3. **Record each flow as it behaves today,** into `.verification/<branch>/baseline/`:

   | Kind | Record |
   |---|---|
   | UI | a walk with a screenshot of each proving state, mobile and desktop |
   | API | the real requests and their responses |
   | Data | row counts and a sample of records for the tables in play |
   | Tests | which pass today, and which flows have none |
   | Speed, when it matters | the measured number, with how it was measured |

4. **Print the baseline card:** each flow, how it was recorded, and its test coverage today (covered, thin, none).

The baseline is working material. Copy it somewhere durable when the work will span many sessions, and say where.

## Proving a step against it

Every ticket after the baseline is proven by the same flows still matching, plus whatever the ticket meant to change.

- Walk the baseline flows the ticket could touch (scope-check's blast radius says which) and compare with the record.
- A difference is either the ticket's intent, stated in its scope or its `## Decisions`, or a regression. There is no third kind.
- Report as `baseline: 9 / 9 flows match` on the result card, or name each flow that differs.

## By kind

- **Small refactor:** no formal baseline. Walk the affected flows on the base and on the branch, and run the existing tests on both.
- **Restructure:** the baseline comes from the app itself.
- **Stack move:** old and new run side by side. A flow moves over when the new one matches the baseline; the old path is removed last.
- **Rebuild:** the baseline is recorded from the reference product and becomes the new project's acceptance criteria.
- **Modernize:** the baseline is the first safety net. Where it shows a flow with no test, a kept test is written before that area is changed.
