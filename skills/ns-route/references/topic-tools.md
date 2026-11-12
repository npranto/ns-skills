# Tools and plugin skills

## Delegating to Matt Pocock's skills (plugin `mattpocock-skills`)

Invoke these with the harness's skill-invocation tool when a phase calls for them. If one is not installed, follow the philosophy inline and say so.

| Need | Skill |
|---|---|
| Interrogate a plan or decision | `mattpocock-skills:grilling` (older name: `/grill-with-docs`) |
| Glossary and ADR upkeep | `mattpocock-skills:domain-modeling` |
| Test-first implementation | `mattpocock-skills:tdd` |
| Hard bug or perf regression | `mattpocock-skills:diagnosing-bugs` |
| Throwaway prototype for a design question | `mattpocock-skills:prototype` |
| Primary-source research into a file | `mattpocock-skills:research` |
| Deep-module design vocabulary | `mattpocock-skills:codebase-design` |
| Standards + spec review of a diff | `mattpocock-skills:code-review` |
| Human-only setup steps (dashboards, secrets) | `mattpocock-skills:wizard` |
| Merge or rebase conflicts | `mattpocock-skills:resolving-merge-conflicts` |
| Writing or editing skills, AGENTS.md, CLAUDE.md | `mattpocock-skills:writing-for-agents` |
| Issue tracker + domain docs setup (`/setup-matt-pocock-skills`) | run if present, else create `docs/agents/*.md` by hand |

## Default toolchain and fallbacks

The defaults below are exactly what the skills use today. A tool is installed when `command -v <name>` finds it; plugin skills are installed when the harness lists them. The project profile may name another tool for a need, and then the rules in `../ns-route/references/topic-proof.md` "Proof" about which tools drive a browser apply to the tool it names. A missing tool is reported at the step that needs it and is never skipped silently.

| Need | Default | Used by | If it is missing |
|---|---|---|---|
| Drive a browser, screenshots, clips | `playwright-cli` | verify | report it at the step; the Proof modes Manual and Skip remain (`../ns-route/references/topic-proof.md`) |
| Console, network, accessibility audit | `chrome-devtools-axi` | verify | the same |
| Performance and web vitals | the Lighthouse CLI | verify | the same |
| Convert clips | `ffmpeg` | verify | the same |
| GitHub: issues, PRs, CI | `gh-axi` | several phases | no fallback is stated; report it at the step |
| Run agents in worktrees | `herdr` (the CLI and its skill) | `ns-flow-delegate` only | "Not inside Herdr: say so and ask: open Herdr and run this again (Recommended), or run the ticket here with `/ns-flow-ticket` instead." |
| Plugin skills | `mattpocock-skills:*` | many phases | follow the philosophy inline and say so (the rule above) |
