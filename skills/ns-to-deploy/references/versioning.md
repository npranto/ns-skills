# Versioning (optional)

A project has versioning when `.github/workflows/release.yml` exists (the profile's **Versioning** line says so). Nothing else records the choice, and it is never set up without the user's yes.

## What it gives

- **A version on every merge.** The PR carries its own version in `package.json`. CI tags the merged commit `vX.Y.Z` with that version and publishes a GitHub release with generated notes. The tagged commit therefore contains its own version, CI commits nothing back, and `CHANGELOG.md` is never touched.
- **A Rollback workflow, run by hand.** Actions > Rollback > Run workflow. An empty version goes back one version from what is live; a named version goes to that one. It uses the host's instant rollback when that version's deployment still exists (seconds), and rebuilds from the tag when it does not (minutes).

## The bump

It comes from the PR title: `[MAJOR]`, `[MINOR]`, or `[PATCH]` anywhere in it, any letter case. No marker means patch. When several PRs merged since the last version, the largest bump wins.

| PR title | 1.4.2 becomes |
|---|:---:|
| `Fix archive button focus` | 1.4.3 |
| `[MINOR] Archive a note` | 1.5.0 |
| `[MAJOR] Remove the v1 notes API` | 2.0.0 |

Recommend from what the PR changes: patch for fixes and internal changes, minor for a new capability that breaks nothing, major when existing users or API consumers must change something. Say the version it would produce from the newest tag. When the recommendation and the title differ, ask (with a Learn box, `../ns-route/references/topic-learn-box.md` "Learn box"), and edit the title with `gh-axi` after confirmation.

## The bump commit

Every PR carries the version it will release as, written by `/ns-to-pr` before the first push.

1. **Work out the next version** from the newest `v*` tag on the fetched base and the title's marker. Never from what `package.json` says today: it may be behind.
2. **Write it** as a normal approved edit to `package.json`, and to the lockfile where it records the project's own version (`package-lock.json` does, in two places). A project with another manifest (`pyproject.toml`, `Cargo.toml`) gets the same edit there.
3. **Commit it alone:** `chore(release): v1.5.0`.
4. **Check it again on the release card.** Another PR merged first, or the title's marker changed: the next version moved. Write the new one as a second commit, push, and wait for CI. Two PRs that both claim `1.5.0` merge without a conflict, so only this check catches it.

The Release workflow takes the version from `package.json` when it is newer than the last tag. A merge that did not carry the bump still gets a version, worked out from the title, and the run summary says `package.json` is behind. The next PR's bump is counted from the tag, so it catches up by itself.

## At release

- On the release card: `v1.4.2 → v1.5.0 · minor, from the title · package.json says 1.5.0 ✅`.
- After the merge: wait for the Release run on the merge commit and confirm it is green, the tag points at the merge commit, the release page exists, the version is the one the card named, and the run summary reads `package.json matches: yes`.
- A failed Release run does not undo the deploy: production is live but unversioned. Read the log, fix the cause, and re-run it; a commit already inside a version is skipped. Never create the tag by hand.

## Rolling back to a version

1. **Pick the version.** Default: the one before what is live (leave `version` empty). The user can name another: list recent versions with their dates and titles (`gh-axi`). Going back more than one version also undoes everything released in between: name those releases before confirming.
2. **Dry run first when in any doubt:** run the workflow with `dry_run` on and read which version and deployment it resolved. It changes nothing.
3. **Run it** after the go-ahead, and watch the run to the end. Its summary says which path it took.
4. **Confirm production** is on the target: the deployed commit is the version's commit.
5. **Say what state this leaves:**
   - Instant rollback: the host stops pointing the production domain at new deployments until one is promoted. Merging the fix builds it without putting it live; promote it after it is verified.
   - Rebuild from the tag: the production branch still holds the bad change, and the next merge deploys it again. The revert has to merge before anything else.
6. **Versions only move forward.** The rolled-back version keeps its tag. The revert and the later fix each get a new version. Offer one line in the bad version's release notes saying it was rolled back and why.

## Setup

1. **Detect.** A GitHub remote (without one, the workflows are written now and start on the first push). The production branch. The host. Existing version tags. An existing release tool (semantic-release, changesets, release-please): stop and say so. Never add a second versioning system.
2. **Ask,** one question at a time:
   - Confirm versioning on every merge to the production branch, showing the bump table. A no ends the setup with nothing written.
   - With no version tag yet, the first version: `0.1.0` (Recommended, still changing) or `1.0.0` (already in real use). Write the answer into `package.json` in the same PR.
   - The Rollback workflow too? Yes (Recommended). On a host other than Vercel, say that the template's deploy steps are Vercel's, and offer to adapt them or skip it.
3. **Write the workflows** as approved edits, from the templates beside the skill:
   - `../ns-to-deploy/workflows/release.yml` to `.github/workflows/release.yml`, with `branches` set to the production branch and `INITIAL_VERSION` to the answer.
   - `../ns-to-deploy/workflows/rollback.yml` to `.github/workflows/rollback.yml`.

   Copy the version and target logic as it is.
4. **Secrets for Rollback** are a human-only step: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`. Hand this to `mattpocock-skills:wizard`. Never ask for the token in chat.
5. **Document it.** Offer a short "Releases" section in the README: the bump table, and how to run Rollback. Set the profile's **Versioning** line to `yes`.
6. **Ship it like any change:** `/ns-to-save`, then a PR. The PR that adds the workflows is also the first release.
7. **Prove it** after that merge: the Release run is green, the tag and release page exist, and the tag equals the version in `package.json` at that commit. Then run Rollback once with `dry_run` on: it must resolve a target and report that production was not changed. Neither template has run in a real Actions job before its first project: treat the first run as the test.

Say at setup: a ruleset that blocks tag creation makes the Release run fail (the user allows GitHub Actions to create `v*` tags), and limiting who can run Rollback is a repository setting the user changes.
