# The smoke check

A few minutes. For preview and production.

1. Confirm the deployed commit: the PR head on preview, the merge commit on production.
2. A protected deployment: read `references/protected-previews.md`.
3. Walk each criterion once at desktop size, with a screenshot of each proving state, and record one clip of the main flow. Step lines as above.
4. A mobile screenshot of each changed screen.
5. Console errors and failed requests on every page visited.
6. Lighthouse and the web vitals on every touched page (`references/ui.md`).
7. **The E2E run in CI for this deployment:** wait for it and read it (`../ns-route/references/e2e.md` "Reading a run"). Red, or never started: FAILED. No E2E workflow yet: say so, and the result says the suite did not run here.
8. **Production:** read-only steps always run. A step that creates or changes data runs only with a test account the user named. Otherwise mark it `not run on production, proven on preview`.

Print `✅ SMOKE PASS · preview @ a73c82f · 3 / 3 criteria · E2E 4 / 4 · console 0 · failed requests 0`, and add the target to the result file and the evidence page.
