# Evidence: files, page, and score

## Files

```
.verification/<branch>/          git-ignored; propose the .gitignore edit when it is not
  result.json                    the one result file, every target in it
  evidence.html                  the page, every target in it
  review.md  quality-check.md    the final reports of those two phases, for the PR description
  local/  preview/  production/  baseline/
    NN-goal.mobile.png  NN-goal.desktop.png  NN-goal.mp4
    lighthouse/<page>.<mobile|desktop>.html and .json
    logs/
```

`result.json` holds, per target: the commit, the URL, the verdict, the score with its parts, each criterion (proof, status, evidence paths), the conditional captures with added or left out and why, console and request counts, the tests that ran with their counts and where they ran, per page and screen size the Lighthouse performance score and LCP, TBT, and CLS with the base's numbers, the risk, the safe-because fact with its label, the undo, anything found outside the ticket, and `evidencePage`, the published page's link once there is one. A later run adds its target and leaves the others.

## The page

`evidence.html` is rendered from `result.json` after every run and opened in the browser (`open <path>` on macOS). One self-contained file: inline CSS, images and clips by relative path, no network requests, readable on a phone, light and dark.

Top to bottom:

1. The score, the release verdict, and one line saying why, with the risk and the undo beside it.
2. The ticket: id, title, outcome, branch, PR, commit.
3. A `Local / Preview / Production` switch, newest first. A target that has not run is left out.
4. One block per criterion: the criterion in the ticket's words, the result, how it was proven, and its own evidence. For a UI criterion that is its screenshots side by side and its clip in a player; for the rest, the request, test output, or numbers with a `no UI` tag.
5. Proven and left out, as on the result card.
6. Performance, for a change with UI: per page and screen size the score, LCP, TBT, and CLS, each with the change from base, and a link to the full Lighthouse report.
7. Tests: each suite, its counts, and where it ran, with the CI run's link on preview and production.
8. How the score was worked out.

## The score

One number from 0 to 100, scored the same way every time.

| Part | Points | Full marks when |
|---|:---:|---|
| Acceptance criteria | 35 | every criterion has passing evidence |
| Screens | 10 | every captured screen is clean at every size captured |
| Console and requests | 10 | no new console errors and no failed requests |
| Tests and checks | 15 | types, lint, the E2E suite where this target runs it, and the touched area's existing tests pass; CI is green when there is a PR |
| Performance | 10 | Lighthouse performance did not fall by 5 or more, and LCP, INP, and CLS are inside their thresholds |
| Accessibility | 10 | no serious or critical violation, and the keyboard walk passes |
| Undo | 5 | a mechanical undo exists, takes under a minute, needs no data step, and was checked |
| Coverage | 5 | nothing important was left unproven |

- **A part that did not run is left out,** and the rest is rescaled to 100. Say which parts were left out in the scoring table.
- Points are lost in proportion: two of five criteria unproven loses two fifths of that part.

| Score | Release verdict |
|:---:|---|
| 90 to 100 | 🟢 SAFE TO RELEASE |
| 70 to 89 | 🟡 RELEASE WITH CARE |
| 0 to 69 | 🔴 NOT SAFE YET |

**Caps.** A failed criterion, a broken screen, a failing kept test, or an undo that does not exist caps the result at NOT SAFE YET. A criterion still waiting on a manual check, or a vital in the poor range, caps it at RELEASE WITH CARE. A score is never rounded up into a band.

`/ns-to-observe` adds a production-health line under this score. It computes no number of its own.

## Publishing

Every run on a PR publishes its evidence to one private Claude Artifact per PR, titled `Evidence · PR 482`, updated in place so its link never changes. It is part of the PR's report set, approved when the PR was opened (`../ns-route/references/pr-writing.md`).

1. Find the existing page first: the `evidencePage` field in `result.json`, then the `<!-- ns-evidence: <url> -->` line in a verification comment. Never publish a second one for the same PR.
2. Load the `artifact-design` skill, then publish `evidence.html` with the screenshots, clips, and Lighthouse reports as its supporting files, under the same folder names. A clip stays under 15 MB.
3. Record the link in `result.json` and print it. Say that it is private until the user shares it.
4. **Keep secrets off the page.** Traces, HAR files, and `logs/` with headers stay local. A Lighthouse report holds the headers it was run with: blank them first (`protected-previews.md` "Keeping it out of evidence"). Then search the folder for each secret's value. A hit blocks publishing.
5. **Real customer data in a production screenshot is a stop:** say which screenshot shows it and let the user decide.

Evidence files never go to GitHub: no branch, commit, release, or attachment holds them.

## Cleanup

`/ns-to-close` deletes `.verification/<branch>/` when the ticket closes, after checking that the published page opens and holds the files. A published page is never deleted.
