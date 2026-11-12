# Reading CI

## Reading CI

Whenever a skill reads CI for a commit or a PR (`gh-axi`):

- Confirm the checks belong to the current head commit, not an earlier push.
- Wait for running or queued checks to finish before giving a verdict.
- List every check with its real name and result. "CI is green" alone is never the report.
- A required check that was skipped or never started is a problem, not a pass. Say so.
- No CI ran on this commit: that is a finding. Say which event or workflow did not run.
- A failure is reported with the failing test or step, its first real error line from the log, and the job link.
