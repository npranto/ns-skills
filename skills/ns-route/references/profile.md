# Project profile

`docs/agents/workflow.md`, written once per project by `/ns-to-start`, by `/ns-flow-existing-project`, or by `/ns-route` when it is missing. Skills read it for the host and proof facts below instead of asking for them on every run.

## Template

```markdown
# Workflow profile

- **Has UI:** yes
- **Versioning:** no

## Host

- **Host:** Vercel
- **Production branch:** main
- **Production URL:** https://example.com
- **Deploys when:** a merge to the production branch
- **Preview:** every PR gets a preview deployment; find its URL in the PR checks
- **Previews are protected:** yes; the way in is `VERCEL_AUTOMATION_BYPASS_SECRET`
- **Logs:** Vercel runtime logs, scoped to the deployment
- **Fastest undo:** instant rollback to the previous production deployment
- **Flags:** none

## Proof

- **Verification skill:** `.claude/skills/verify-<app>/`
- **Local env file:** `.env.local`
- **E2E:** Playwright · `npm run e2e` · CI workflow `.github/workflows/e2e.yml`
```

## Fields

| Field | Values | Read by |
|---|---|---|
| Has UI | yes, no | verify, design, review, quality-check |
| Versioning | yes when `.github/workflows/release.yml` exists | pr, deploy, rollback |
| Host, Production branch | the host and the branch that deploys to production | deploy, rollback |
| Production URL | the address users open | verify, deploy, observe, the E2E workflow |
| Deploys when | a merge, a manual promote, a pipeline | deploy |
| Preview | how to get a preview URL, or `none` | pr, verify |
| Previews are protected | no, or yes with the way in by variable name | verify |
| Logs | how to read runtime logs for one deployment | observe |
| Fastest undo | the mechanical step that restores the previous release | deploy, rollback, observe |
| Flags | the flag system, or `none` | tickets, implement, deploy |
| Verification skill | the project verification skill's path, or `not set up` | verify |
| Local env file | the git-ignored env file the app and E2E suite read | verify, quality-check |
| E2E | the runner, the local command, the CI workflow, or `not set up` | verify, quality-check |

## Writing it

1. Fill every field you can from the repo: the host config, the CI workflows, the env example, the package scripts.
2. Ask the user only for a host fact that is not on disk. A field not known yet says `not known` or `set by the walking skeleton`, never a guess.
3. Show the file and write it as a normal approved edit.

## When it is missing

Say so in one line and offer to write it now. If the user declines, ask each fact at the moment a skill needs it. A missing profile, or a field that reads `not known`, never turns a step off silently: a skill that cannot do a step says which fact it lacks.
