# Protected deployments

A deployment behind the host's protection shows a login wall to an automated browser. The project profile's **Previews are protected** line records this project's way in. On Vercel there are two, tried in this order:

1. **The bypass secret,** when `VERCEL_AUTOMATION_BYPASS_SECRET` is in the local env file (in CI, a repository secret). One secret opens every preview and production deployment of the project.
2. **The CLI's short-lived token,** when no secret is stored and the directory is linked to the Vercel project: `vercel env run -- <command>` puts `VERCEL_OIDC_TOKEN` in that command's environment. It opens this project's previews and expires on its own.

Neither is available: ask the user. `../ns-route/references/e2e.md` "Where each secret lives" says where a secret goes. Never look for another way in.

## Sending it

| Way in | Header |
|---|---|
| Bypass secret | `x-vercel-protection-bypass: <secret>` and `x-vercel-set-bypass-cookie: true` |
| CLI token | `x-vercel-trusted-oidc-idp-token: <token>` |

- **To the deployment's own origin, on every request there.** A header set for the whole browser also reaches every third party the page calls. In Playwright, add it in a route handler that matches the deployment's origin. The bypass cookie also carries a tool that can send a header only once.
- **Never in a URL, and never printed.** Read it from the environment inside the command that uses it.
- **Confirm it worked** before testing: the first request returns the app's own page, not the host's login page. Still the wall: the secret is wrong, revoked, or was regenerated after this deployment was built. Stop and ask.

## Keeping it out of evidence

- Redact the header in every saved log and every command shown: `x-vercel-protection-bypass: <redacted>`.
- Lighthouse writes its settings, extra headers included, into its HTML and JSON reports. Blank the value in both before the report counts as evidence.
- Traces and HAR files record request headers. They stay out of evidence and out of CI artifacts.
- Before anything is published, search the evidence folder for the value. A hit blocks publishing.

## The app's own login

The bypass only passes the host's wall. Sign in to the app as a real user would, with the test account from the env file. Say in the result which way in the run used.

## Production

A production domain is public under Vercel's standard protection and needs no bypass. Where production is protected too, the bypass secret works there as it does on a preview. The CLI token does not, unless the project's Trusted Sources let development reach production, and changing that is the user's decision.

## Another host

Use what the profile's **Preview** and **Previews are protected** lines say. Nothing there: ask the user how previews are reached.
