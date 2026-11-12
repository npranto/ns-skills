# Proving a change with UI

## Driving the browser

Only these tools (`../ns-route/references/topic-proof.md` "Proof"): the harness the project verification skill names, `playwright-cli` by default, to drive the browser and record clips; `chrome-devtools-axi` (`npx -y chrome-devtools-axi`) for console, network, and the accessibility audit; the Lighthouse CLI (`npx -y lighthouse`) for performance and the vitals; `ffmpeg` to convert clips. Install a missing one and say so in one line.

- **Watched:** run the browser headed, with about a second on each result. **Hidden:** headless.
- Reach each screen the way a user does: through the menu and the link, not a typed-in URL, unless the URL is the entry point.
- Prefer stable handles: roles, labels, and text a user sees.
- Sign in with the test account the verification skill names. Its credentials come from the env file by variable name.

## Viewports

| Viewport | Size | Emulation | Captured |
|---|---|---|---|
| Mobile | 390 x 844 | touch, mobile user agent | always |
| Desktop | 1440 x 900 | mouse | always |
| Tablet | 820 x 1180 | touch | when layout or breakpoint styles changed |

Use the project's own breakpoints when its design contract defines them. Save as `NN-goal.<viewport>.png`.

## Clips

Record the main flow at desktop (at mobile when the change is mostly a mobile layout): 5 to 40 seconds, at a pace a person can follow. Convert the `.webm` to `.mp4` with `ffmpeg` (H.264, `-movflags +faststart`, about 1280 px wide, under 15 MB). A bug fix gets two clips: the failure on the base, and the same steps passing.

## States

For a changed screen, walk the states its design contract lists: loading, empty, error, success, disabled. Screenshot each one the change touched. Be picky: anything that looks off on screen is a finding.

## Console and network

On every page visited, record console errors and failed requests. A new console error is a finding even when the walk passed.

## Lighthouse and vitals (every change with UI, every target)

Run the Lighthouse CLI on each page the change touches, once for mobile (its default) and once with `--preset=desktop`, writing both the HTML and the JSON report under `lighthouse/`. Locally, measure the production build, not the dev server.

| Target | Measured on | Base |
|---|---|---|
| Local | the local production build | the default branch, built the same way |
| Preview | the preview URL | current production |
| Production | the production URL | this PR's preview |

A page that does not exist on the base has no base: say `new page`. Run twice and keep the median when two runs differ by more than five points.

| Vital | Good | Poor |
|---|---|---|
| LCP | 2.5 s or less | over 4 s |
| INP (TBT in the lab) | 200 ms or less | over 500 ms |
| CLS | 0.1 or less | over 0.25 |

- Record the performance score, LCP, TBT, and CLS per page and screen size in `result.json`, each beside the base's number.
- A protected deployment needs the bypass header on the Lighthouse run. Read `protected-previews.md` first: the report stores that header.
- A score that falls by five or more, or a vital that leaves the good range, is a finding with a suggestion. A problem that was already there on the base is reported under "found outside the ticket", not charged to this change.

## Accessibility (when the diff calls for it)

- An automated scan (the repo's own axe setup, else the `axe` CLI from `@axe-core/cli` if installed, else `@axe-core/playwright`): no serious or critical violation.
- Walk the keyboard path with Tab, Shift+Tab, Enter, Space, and Escape: every control reachable, focus visible and in a sensible order, focus returned when a dialog closes.
- Labels and names on every new control, and contrast on new text.

Each violation is a finding that names the element.

## Forms, auth, and flags (when the diff touches them)

- **Forms:** valid, invalid, empty, and oversized input; the error shown; a double submit.
- **Auth and roles:** each role, signed out, another user's data.
- **A flag:** on, off, and the default for a user it does not reach.
