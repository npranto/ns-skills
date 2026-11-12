# Harnesses

The skills use capability words, never a harness's tool names. This file maps each capability to the real tool in each supported harness. "verified" means it was run in a spike (see the package's `docs/spikes/README.md`); "unverified" means nobody has tested it, so do not assume it.

## Capabilities

| Capability | Words used in the skills | Claude Code | Codex | Cursor | OpenCode |
|---|---|---|---|---|---|
| Ask a choice | the multiple-choice question tool | `AskUserQuestion` | unverified | unverified | unverified |
| Edit a file for approval | the harness's file-edit tool | the Edit and Write tools | unverified | unverified | unverified |
| Run a phase from a flow | read its `SKILL.md` and follow it, never the harness's skill-invocation tool | the Read tool, never the Skill tool (verified) | read the file with the shell (verified) | unverified | the Read tool (verified) |
| Start a skill by hand | the command | `/ns-name` or `/ns-skills:ns-name` (verified) | `$ns-name` (verified) | the `/` menu, per the owner's notes (unverified) | ask for the skill by name; there is no typed command (verified) |
| Manual-only | manual-only | `disable-model-invocation: true` in the frontmatter, honored (verified) | `agents/openai.yaml` with `policy: allow_implicit_invocation: false`, honored; the frontmatter key is ignored (verified) | unverified | cannot be enforced from the skill file (verified) |
| Non-interactive run | the harness's non-interactive mode | `claude -p` (verified) | `codex exec` (verified) | none found (unverified) | `opencode run` (verified) |
| A fresh review agent | a fresh review agent | a subagent (unverified) | unverified | unverified | unverified |
| A structured findings report | the host's structured findings report | `ReportFindings` (unverified) | unverified | unverified | unverified |
| A broad read-only sweep of a repo | a read-only exploration agent | the Explore subagent (unverified) | unverified | unverified | unverified |

## When a capability is missing

Say plainly which capability is missing. Ask the same question as plain text, list the options with the recommended one first, then stop and wait for the answer. Never continue as if it had been answered.
