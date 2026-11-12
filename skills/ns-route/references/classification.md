# Classify

| Dimension | Values | How to decide |
|---|---|---|
| Task type | greenfield, feature, bug, incident, refactor, tech-debt, restructure, stack-move, rebuild, modernize, architecture, performance, dependency, migration, infrastructure, spike, proposal, docs | See table below. Ask only if genuinely ambiguous (e.g. bug vs. incident hinges on "is this live in production right now"). |
| Scope | tiny, small, medium, large, program | tiny: one file/function, no ticket needed. small: one ticket, one vertical slice. medium: one feature, a few tickets, likely needs a spec. large: needs `/ns-to-split-ticket`, spans sessions. program: multiple features/epics, spans weeks. |
| Uncertainty | low, medium, high | low: requirements and approach both clear. medium: one of the two has open questions. high: fundamental unknowns in the problem or the solution space. |
| Risk | low, medium, high, critical | low: isolated, well-tested area. medium: shared code, moderate blast radius. high: critical path (auth, billing, data integrity) or user-facing at scale. critical: production is impacted, a security exposure is live, or data loss is in progress right now. |
| Reversibility | easy, moderate, difficult, irreversible | easy: revert the commit or flag. moderate: recoverable but needs cleanup or backfill. difficult: contracts or schemas changed, external consumers affected. irreversible: destructive data operation, a public API break already shipped, or a secret exposed. |
| Codebase familiarity | familiar, partially-known, unfamiliar | familiar: a current `codebase-map.md` covers this area, or the agent has already worked here this session. partially-known: a map exists but is stale or covers an adjacent area. unfamiliar: neither. |
| Security sensitivity | none, moderate, sensitive | none: no auth, secrets, or external-facing surface touched. moderate: touches auth-adjacent code or PII-adjacent data but adds no new boundary. sensitive: new trust boundary, authn/authz change, payments, secrets, or a new external-facing integration. |
| Data risk | none, schema, migration, destructive | none: no persistent data touched. schema: additive schema change only. migration: existing data must move or be backfilled. destructive: irreversible delete or mutation of existing data. |
| Sessions expected | 1, several, many | 1: finishable in one sitting. several: multiple sessions, one engineer. many: independent tickets that justify handing to agents (see `ns-flow-delegate`). |

**Task type table** (the workflow column names the workflow file in `../ns-route/references/workflows/` that is the baseline):

| Signal | Type | Workflow |
|---|---|---|
| Directory is empty or near-empty, or the user says "new project" | greenfield | greenfield |
| Adds new user-visible or API capability to an existing system | feature | feature |
| Existing behavior is wrong, not currently live-broken | bug | bug |
| Something is broken, degraded, or exposed in production right now | incident | incident |
| Internal structure changes deliberately, behavior unchanged, planned, small | refactor | refactor |
| Same as refactor but reactive/opportunistic cleanup, usually small | tech-debt | refactor |
| A large restructure inside one stack, behavior unchanged | restructure | restructure |
| A working app moves to a new framework, runtime, database, or host | stack-move | stack-move |
| A new build of a product that already exists | rebuild | rebuild |
| Old code with few tests to make safe to change | modernize | modernize |
| An architecture decision, with or without code changes | architecture | architecture |
| Behavior is correct but too slow or expensive; needs profiling | performance | performance |
| Adding, removing, or bumping a package or platform version | dependency | dependency |
| Data, schema, service, or platform moves from one shape/system to another | migration | migration |
| CI/CD, hosting, deployment config, IaC, observability tooling | infrastructure | infrastructure |
| The goal is to answer a design or technical question, not to ship | spike | spike |
| A plan, estimate, or design is wanted before anyone commits to building | proposal | proposal |
| Only documentation is out of date | docs | docs |

**Escalation overrides (apply after scoring):** `data risk = destructive` forces `risk` to at least `high`. `task type = incident` forces `risk = critical`. Either forces a mandatory authorization gate regardless of what the other dimensions say (see step 4).
