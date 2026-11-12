# Writing to a PR

Several skills write to the same PR. Each owns exactly one place, and nothing written earlier is replaced by something else.

## What every PR carries

Every PR, in every project, ends up with all of these. Reviewers and stakeholders read the PR, so a check that ran only in chat did not happen as far as they can tell.

| What | First visible line | Marker | Owner | Posted |
|---|---|---|---|---|
| Ticket details | `## 🎫 Ticket` | `<!-- ns-pr:ticket -->` to `<!-- /ns-pr:ticket -->` | `/ns-to-pr` | at open, description, first region |
| Review summary | `## ✅ Ready for review` | `<!-- ns-pr:review -->` to `<!-- /ns-pr:review -->` | `/ns-to-pr` | after the preview check, description, second region |
| Local proof | `## 🧪 Verification · Local` | `<!-- ns-verify:local -->` | `/ns-to-verify` | right after the PR opens |
| Preview proof | `## 🧪 Verification · Preview` | `<!-- ns-verify:preview -->` | `/ns-to-verify` | after the preview check |
| Stakeholder review | `## 👀 Stakeholder Review` | `<!-- ns-brief-review -->` | `/ns-to-stakeholder-brief review` | when the PR is ready |
| Production proof | `## 🧪 Verification · Production` | `<!-- ns-verify:production -->` | `/ns-to-verify` | after the production check |
| Shipped | `## 🚀 Shipped` | `<!-- ns-brief-release -->` | `/ns-to-stakeholder-brief release` | after `/ns-to-observe` reports HEALTHY |
| Evidence page | a private Claude Artifact, `Evidence · PR 482` | `<!-- ns-evidence: <url> -->` inside each verification comment | `/ns-to-verify` | with the first verification comment, then updated in place |

A PR with nothing to prove (docs or planning files only) carries its description alone. The last PR of a multi-ticket feature can also carry the feature's Shipped report, under `<!-- ns-brief-release:feature -->`, which is its own stop.

## Rules

- **Approved once.** The stop in `/ns-to-pr` that pushes and opens the PR lists this set and approves every write in it, for that PR. Each one is printed in chat as it is posted. "Show me each report first" at that stop makes every later write in the set its own stop. Anything else written to a PR, and any other published page, is its own stop (`../ns-route/references/core.md` "Run modes").
- **One marker, one owner.** A skill creates or updates only the place carrying its own exact marker. It never edits another skill's comment or text a person wrote.
- **The description is edited by region.** Read the current body. Replace only what sits between your own start and end markers, or append your region. Write everything else back unchanged.
- **Check before and after every write.** Before: read the description and list the comments with `gh-axi`, and keep that copy. After: read them again and confirm that only your place changed. If anything else changed or is missing, stop, say what, and restore it from the copy.
- **Each target has its own verification comment,** updated in place. A re-run replaces that target's comment and adds `Previous run: <sha> <verdict>`. Later comments repeat the earlier targets as columns, so the newest one reads on its own.
- **One fact, one home.** A link or number already on the PR is pointed at in a few words, not repeated.
- **Text and links only.** Pictures, clips, and Lighthouse reports live on the evidence page, and every verification and stakeholder comment links to it.
- **The title is the first visible line,** exactly as in the table.
- **Nothing is skipped quietly.** A report that cannot be written (no preview, a failed run, a skipped proof) is still posted, saying what is missing and why. `/ns-to-deploy` and `/ns-to-close` check the table and post what is absent.
