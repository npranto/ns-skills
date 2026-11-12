# Publishing

Every run on a PR ends with two writes, in this order. Both are part of the PR's report set, approved when the PR was opened (`../ns-route/references/pr-writing.md`), so neither is a stop unless the user asked to see each report first.

1. **The evidence page.** Publish or update the PR's one private evidence page with this target's screenshots, clip, and Lighthouse reports (`references/evidence.md` "Publishing").
2. **This target's comment.** Post or update it from `references/comment.md`, and print it in chat.

- **Local, with no PR yet:** the result waits on disk. `/ns-to-pr` does both writes right after it opens the PR.
- **FAILED, PARTIAL, manual, and skipped runs are published too.** The comment says what happened, so the PR never shows a stale pass.
- **No PR at all** (a baseline, a spike): nothing is published.

Also append one dated entry to the ticket's `## Comments`: the target, the verdict, the score, and the numbers that matter.
