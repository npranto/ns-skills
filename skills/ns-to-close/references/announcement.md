# Company announcement

Written when the user types `announce it` at close. Never written unasked, never posted: sharing is the user's action.

Ask which form: `Slack · Markdown · both`. Say so when the work has nothing a non-engineer would notice.

## What it covers

One message for everyone in the company, read like a note from a project manager. In this order, each only when there is something real to say:

1. **Headline:** what launched, as a person would say it out loud.
2. **What it is:** what people can do now that they could not before. For a bug: what was going wrong for users, and that it is fixed.
3. **Why it matters:** the value, and who benefits.
4. **When and who has it:** the real date it went live, and whether everyone has it.
5. **What you might notice or need to do.** "Nothing to do" is a fine answer.
6. **What is next,** from the next-ticket check. No date unless the user gives one.
7. **Not included yet,** so nobody promises a customer something that is not there.
8. **Questions and feedback:** who to ask, and where.
9. **Thanks,** only when the user names people to credit.

## How it is written

- No jargon and nothing internal: no file names, branches, commits, flags, "PR", "deploy", "migration", scores, or percentages. One link at the end, labelled "Details for the curious".
- 120 to 180 words. Short sentences, active voice, the reader as "you". Warm, not hyped.
- Only true things, from the deploy summary, the observe verdict, and the tickets. What is not known is left out or asked for.
- A feature made of several tickets is announced once.

## Handing it over

Each version in its own four-backtick fenced block with nothing else inside, so it copies in one go. One line above each block says where it is for.

- **Slack:** `*bold*`, `_italic_`, `•` bullets, no `#` headings, no tables, links as plain URLs, emoji as Slack codes.
- **Markdown:** `##` for the headline, `**bold**` labels, `-` bullets, emoji as characters.

After printing, ask once whether to adjust anything, and reprint the whole block after a change.
