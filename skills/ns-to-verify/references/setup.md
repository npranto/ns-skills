# Creating the project verification skill (`/ns-to-verify setup`)

Every project gets one small skill that records how to drive the real app and prove behavior. It is written for the next agent, which reads it cold in the middle of a ticket. Run once per project: in the walking skeleton for a new project, at onboarding or the first proof for an existing one.

## 1. Interview the repo

Answer these from the code. Ask the user only what cannot be observed.

- **Surface:** what does a user touch? A web UI, an API, a CLI, a library. Pick the primary one and note the rest.
- **Launch:** how does it start locally? Prefer the repo's documented dev command. Note ports, env vars, seed data, auth.
- **Drive:** how can an agent interact with it? An existing harness first (Playwright specs, API test helpers). Otherwise a browser for web, plain HTTP for a service, a terminal session for a CLI.
- **Observe:** what evidence can be captured? Screenshots, responses, logs, exit codes, database state.
- **Secrets:** which env variables hold what a proof needs (a test login, a preview bypass)? Record the names and the env file. Never a value.
- **E2E:** does a suite exist, does it run locally from a clean checkout, and does CI run it on the preview and on production? Check it against `../ns-route/references/e2e.md`. Each gap is fixed now or becomes a ticket.
- **Isolate:** can two instances run side by side? If not, say so in the skill.

A checkout that does not build or start is fixed first, or reported precisely.

## 2. Write `.claude/skills/verify-<app>/SKILL.md`

Frontmatter: `name: verify-<app>` and a description that names the app and the surface. Then these sections, each grounded in what the interview found, with no placeholder left:

- **Launch:** the exact command, how to tell it is ready (a log line, a port answering), and how to stop it.
- **Doctor:** one read-only check that answers "is this instance worth driving?".
- **Drive:** the harness recipe with real selectors and commands from this repo. Stable handles (roles, labels, route paths) over coordinates.
- **Secrets:** the variable names and the env file, for example `E2E_USER_EMAIL`, `E2E_USER_PASSWORD`, `VERCEL_AUTOMATION_BYPASS_SECRET` in `.env.local`. The file must be git-ignored, and every name is also in `.env.example`.
- **E2E:** the command, how a test signs in, which tests carry `@smoke`, and the CI workflow that runs the suite on the preview and on production.
- **Evidence:** what to capture and where it goes (`.verification/<branch>/`). Proof standards: exercise the real user path, capture the action and the resulting state, and check side effects (rows written, messages sent) alongside what is visible.
- **Cleanup:** how to stop what the run started. Stop what you started, never by process name. Evidence survives cleanup.

## 3. Seed the feature map

`.claude/skills/verify-<app>/features/README.md` as the index, plus one file per user-facing feature. Start with the top three to five, from routes, menus, or docs. Each file answers, from the user's side:

- **What it is,** and its sub-features
- **How to get to it**
- **How to drive it** with the harness
- **What proves it works:** the observable end state
- **Gotchas**

Mark one feature as the **core flow**: the one that shows the app is basically alive.

## 4. Prove the skill

Run its own instructions once, end to end: launch, doctor, drive one mapped feature, capture evidence, clean up. Fix what fails. A skill that was never run is a draft.

## 5. Hand over

Show the files, write them as approved edits, and commit them with the project. Add the skill's path to the project profile's **Verification skill** line (`../ns-route/references/profile.md`).

A feature a later ticket adds or changes is added to the map by `/ns-to-docs` in that ticket.

Adapted from pstack's create-verification-skill by poteto (MIT license).
