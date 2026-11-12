# Principles

The named principles a Learn box cites (`../ns-route/references/topic-learn-box.md` "Learn box"). Cite one by its exact name. Pick the one that actually decided the choice, not the nearest match.

## Simplicity

| Principle | Rule | Applies when |
|---|---|---|
| Smallest change that solves it | Prefer deleting to adding. | sizing a diff, tempted to add a layer |
| Subtract before you add | Remove dead weight first, then build on the simpler base. | sequencing an addition or a rewrite |
| No abstraction without a second use | One caller means no interface, base class, or config layer. | a helper, a generic type, a plugin point |
| One ticket, one purpose | A fix ships alone. Two domains are two tickets. | a diff starts carrying a second concern |

## Design

| Principle | Rule | Applies when |
|---|---|---|
| Start from the caller | Write how the code will be used before how it works. | shaping a function, module, or API |
| Design it twice | Compare two different shapes before committing to one. | any decision with more than one plausible structure |
| Data shape first | The right structure makes the logic obvious. | before writing logic that branches or repeats |
| Make illegal states unrepresentable | Let the types rule out bad data. | designing a type, a status, a state machine |
| Guard at the boundary | Validate and authorize where data enters. Trust the types inside. | input, auth, an external call |
| Deep modules | A small interface with a lot behind it. | drawing a module boundary |
| Boring and replaceable | Choose the well-understood tool you could swap out. | picking a library, service, or pattern |

## Change safety

| Principle | Rule | Applies when |
|---|---|---|
| One-way and two-way doors | Decide late what is cheap to change, carefully what is not. | judging how much thought a choice deserves |
| Additive first, then contract | Add the new shape, move callers, remove the old. | a schema, an API, a config key changes |
| Safe to repeat | An operation run twice ends in the same state. | jobs, retries, webhooks, migrations |
| Vertical slices | Every ticket ends in something you can demonstrate. | slicing work into tickets or layers |
| Risk first | Do the uncertain work while changing the plan is cheap. | ordering tickets or decisions |
| Walking skeleton | Prove the whole path before building on it. | a new project, a new integration |

## Proof

| Principle | Rule | Applies when |
|---|---|---|
| Prove it on the real thing | "It compiles" is not evidence. | before calling anything done |
| Root cause before fix | Reproduce, then trace to the cause. | any bug |
| Test behavior, not implementation | Call it the way users do. Assert what they observe. | writing, changing, or keeping a test |
| Every claim carries its evidence | Measured, inferred, or guess. | reporting a result, a number, a cause |
| Know the blast radius | Name what could break and the one fact that makes it safe. | a change to anything used elsewhere |

## Operate

| Principle | Rule | Applies when |
|---|---|---|
| Mitigate, then diagnose | Restore service first. Understand after. | production is failing |
| Observable or not done | A new critical path has a signal you can watch. | adding a user-facing path or a job |
| Code is the source of truth | Docs and comments change in the same PR. | any change that makes a doc wrong |

Several of these are adapted from pstack by poteto (MIT license).
