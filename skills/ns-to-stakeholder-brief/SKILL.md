---
name: ns-to-stakeholder-brief
description: The plain-language reports every PR carries for designers, product, and stakeholders - the stakeholder review before shipping, and the Shipped comment after production is healthy.
disable-model-invocation: true
argument-hint: "[review | release] [PR number, ticket, or feature slug]"
---

# ns-to-stakeholder-brief

Read first: `../ns-route/references/core.md`, `../ns-route/references/pr-writing.md`, `../ns-route/references/topic-tools.md`
Preflight: ns-skills is a set: install all of it (see the README), a partial install is not supported. If a file named above is missing, stop and say exactly that.

Written for non-engineers: designers, product, stakeholders. Simple words, no jargon, no code, no file names. A reader with two minutes finishes knowing what changed for users and whether it is safe. It runs on every ticket: `review` at the end of `/ns-to-pr`, `release` after `/ns-to-observe` reports HEALTHY. It can also be run by hand.

## Mode

- **review:** the PR is ready. Tells stakeholders what is about to ship and how to try it on the preview.
- **release:** after `/ns-to-observe` reports HEALTHY, before `/ns-to-close`. Its comment is the PR's Shipped message. For a whole feature, after the integration check.

With no mode given, pick by state (an open PR: review; merged and deployed: release) and confirm in one line.

## Gather

The ticket and spec, the PR (via `gh-axi`), the preview and production URLs, the proof result with its score and performance numbers, the evidence page link, the PR's undo block, and for release the version and the observe verdict. Everything is on disk or on the PR: reuse it, re-run nothing. Ask via the multiple-choice question tool only for what is missing, especially the expected release date (otherwise "when merged").

## Contents

| Review | Release |
|---|---|
| What this is, in two sentences (for a bug: the bug as users experienced it) | What went out, when, and the version |
| Why we are building it, or how the bug was caught | What changes for users: before and after |
| What changes for users: before and after | Who has it now |
| For a bug: what we are doing so it does not happen again | The same checks, on local, preview, and production |
| How to try it on the preview, per criterion | Current health and speed, in plain words |
| What we checked, and the score in one plain sentence | If something goes wrong: how it is undone, and how fast |
| When it goes live, known limits, how to give feedback | Known limits, what is next, who to contact |

For a feature of several tickets, release covers the whole feature: one row per ticket, plus the integration-check result.

## Write and post

1. Read `references/templates.md` and write the comment with the blocks in `../ns-route/references/report-blocks.md`.
2. Follow `pr-writing.md`: its own comment, its own marker, the title as the first visible line.
3. **Post it and print it in chat.** It is part of the PR's report set, approved when the PR was opened. Then offer, in one line: change it, also publish a shareable page, or give me text to paste.
   - **A shareable page** is a Claude Artifact with the same content and the recordings and screenshots inline, for people without repo access. Load `artifact-design` first. It is private until the user shares it, and publishing it is its own stop.
   - **Text to paste:** the same report as plain text for Slack or email.
4. **A whole feature's release report is its own stop:** show the draft first. It goes on the last ticket's PR as a second comment, under the marker `<!-- ns-brief-release:feature -->`.

Dates, counts, and percentages are real. A number that is not known is left out.

Suggest next: after review, `/ns-to-deploy <PR>`; after release, `/ns-to-close`.
