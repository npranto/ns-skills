# Proof

## Proof

Tests passing is not proof that a user can do the thing. `/ns-to-verify` proves each change on a real screen or a real request: the full proof locally after `/ns-to-implement`, and a smoke check on the preview and on production. A change that depends on the environment, or that `/ns-route` scored high or critical risk, gets the full proof on preview and production too.

Never run it unasked. Before each run, ask via the multiple-choice question tool (on autopilot, the mode chosen once at setup applies for the whole run):

- **Automatic, watched** (Recommended): the agent drives a headed browser at a pace a person can follow.
- **Automatic, hidden**: the same, headless.
- **Manual**: the user starts the app and checks it themselves; the agent gives a checklist (each criterion's steps, the states and breakpoints, the console) and waits for the report.
- **Skip**: recorded as not proven, with the reason.

Agent-driven browsing uses only these tools: `playwright-cli` (drive the browser, screenshots, clips), `chrome-devtools-axi` (console, network, accessibility audit), the Lighthouse CLI (performance and web vitals), and `ffmpeg` (convert clips). No other tool, MCP server, or improvised script for launching a browser, navigating, or taking screenshots. Start only what you will also stop. This does not restrict the project's own committed test suites (for example a Playwright suite), which always run as they are.

Record which mode was chosen and the outcome, with evidence, in the result file (`.verification/<branch>/`, git-ignored) and the ticket's `## Comments`. E2E tests run in three places (`../ns-route/references/e2e.md`).
