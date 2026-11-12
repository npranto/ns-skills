# Stakeholder comment templates

Text and links only. "See it" is a link to the PR's evidence page, with a note that it is private until the PR author shares it.

## Review (`<!-- ns-brief-review -->`)

````markdown
<!-- ns-brief-review -->
## 👀 Stakeholder Review

> [!IMPORTANT]
> ### Ready for your review: archive a note
> Users can now archive a note they are done with and find it later under Archived.

| 👥 Who it affects | 📅 Goes live | 🛡 Score | ⏪ If it goes wrong |
|:---:|:---:|:---:|:---:|
| **all users** | **when merged** | **92 / 100** 🟢 safe to release | **undone in < 5 min** |

### 🎬 See it
[▶ Watch the recording and see the screenshots](https://claude.ai/artifact/…) (private: ask the PR author for access)

### 🔁 What changes for users
| 🔴 Before | 🟢 After |
|---|---|
| Finished notes stay in the list forever | One click moves a note to Archived |
| The only option was Delete | Archived notes can be brought back |

### 💼 Why it matters
- **Better:** shorter lists, fewer accidental deletes.
- **Watch:** people may look for old notes in the main list for the first week.

### 🧪 Try it yourself
1. Open the preview link at the top of this PR.
2. Open any note, click the menu, choose **Archive**.
3. Open **Archived** in the sidebar: the note is there.

> [!TIP]
> **We checked it for you:** 3 of 3 checks pass on phone and desktop, and all 5 automated checks on the code are green. The page loads in **1.8 s** on a phone.

💬 **Feedback:** reply here, or message @owner.
````

For a bug fix, "Why it matters" becomes "How we caught it", and "What changes for users" shows the failure before and the fix after.

## Release (`<!-- ns-brief-release -->`)

The PR's Shipped message. Posted on the merged PR.

````markdown
<!-- ns-brief-release -->
## 🚀 Shipped

> [!TIP]
> ### Shipped: archive a note
> Live for all users since **Thu 8 Oct, 14:32** · version **v1.5.0** · https://app.example.com

| ✅ Checks | 🩺 Health | ⚡ Speed | 👥 Who has it | ⏪ Undo |
|:---:|:---:|:---:|:---:|:---:|
| **3 / 3** | **healthy** | **96** 📱 · **99** 🖥 | **100%** | **< 5 min** |
| on production | 0 new errors | loads in **1.8 s** on a phone | of users | roll back one version |

### 🎬 On production
[▶ Watch it on production, with screenshots](https://claude.ai/artifact/…) (private: ask the PR author for access)

### 🔁 What changed for users
| 🔴 Before | 🟢 After |
|---|---|
| Finished notes stay in the list forever | One click moves a note to Archived |

### ✅ Same checks, run three times
| Check | Local | Preview | Production |
|---|:---:|:---:|:---:|
| Archive a note from the menu | ✅ | ✅ | ✅ |
| Archived note leaves the main list | ✅ | ✅ | ✅ |

### 🩺 How it is doing
🟢 Pages load cleanly · 🟢 no new errors in **1,240** requests · 🟢 the automated tests pass on production

### ⏪ If something goes wrong
Running **Rollback** goes back to `v1.4.2` in about **30 s**. Nothing has to be restored.

### ⏭ What is next
**Next up:** #04 Restore a note. **Not included this time:** bulk archive (#07).

📣 Questions: @owner
````

The two are separate comments. The Shipped comment never replaces the review.

## Rules

- The version line appears only on a project with versioning.
- **Speed** is the production performance score and the phone LCP from the production proof, in plain words. A change with no page leaves the column out.
- **Health** quotes the observe verdict. With little traffic so far, say so: the check gets stronger with time.
- A check that could not run somewhere is ➖ with the reason in plain words.
