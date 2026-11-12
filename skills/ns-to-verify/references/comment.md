# The verification comments

One comment per target: local, preview, production. Each is posted once and updated in place (`../ns-route/references/pr-writing.md`), built with the blocks in `../ns-route/references/report-blocks.md`, and filled from `result.json`. A reviewer who reads only this comment knows what was checked, what it measured, and where to see it.

## Local (`<!-- ns-verify:local -->`)

````markdown
<!-- ns-verify:local -->
<!-- ns-evidence: https://claude.ai/artifact/… -->
## 🧪 Verification · Local

> [!TIP]
> ### 🟢 95 / 100 · SAFE TO RELEASE · local `a73c82f`
> **03 Archive a note** · 3 of 3 criteria pass · 0 console errors · risk medium

### 🎬 📱 🖥 [Open the evidence page](https://claude.ai/artifact/…)
1 clip · 6 screenshots at two sizes · 2 Lighthouse reports. Private: ask the PR author for access.

| ✅ Criteria | 🧪 E2E | 🧹 Console | 🌐 Requests | ⚡ Performance | ⏪ Undo |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **3 / 3** | **4 / 4** | **0** errors | **0** failed | **96** 📱 · **99** 🖥 | **< 5 min** |

### ✅ Acceptance criteria
| # | Criterion | Local | Proof |
|:---:|---|:---:|---|
| 1 | Archive a note from the menu | ✅ | walk 📱 🖥 · 🎬 12 s · e2e `archive.spec.ts` |
| 2 | An archived note leaves the main list | ✅ | integration `queries.test.ts` |
| 3 | Only the owner can archive a note | ✅ | request as another user: `403` |

### ⚡ Performance and web vitals
| Page | | Performance | LCP | TBT | CLS |
|---|:---:|---|:---:|:---:|:---:|
| `/notes` | 📱 | 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ **96** ▲ +2 | **1.8 s** 🟢 | **90 ms** 🟢 | **0.01** 🟢 |
| `/notes` | 🖥 | 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **99** ▲ 0 | **0.7 s** 🟢 | **0 ms** 🟢 | **0.00** 🟢 |

Base: `main` @ `4f2a9c1`, built locally. Lab numbers; TBT stands in for INP. Full reports are on the evidence page.

### 🧪 Tests
| Suite | Result | Ran |
|---|:---:|---|
| E2E | ✅ **4 / 4** · 38 s | `npm run e2e`, against the local build |
| Unit and integration | ✅ **48 / 48** · 6 s | `npm test` |

**Left out** tablet: no layout change · accessibility scan: no new control
**Found outside the ticket** mobile LCP on `/about` is **3.6 s**, not caused by this change

<details><summary>How the score was worked out</summary>

86 of 90 points, rescaled and never rounded up: criteria 35/35, screens 10/10, console and requests 10/10, tests and checks 15/15, performance 10/10, undo 4/5 (read, not run), coverage 2/5 (the weekly export was not exercised). Accessibility did not run: no new control.

</details>
````

## Preview (`<!-- ns-verify:preview -->`)

The same shape, with these differences:

- The banner names the preview and its commit: `🟢 95 / 100 · SAFE TO RELEASE · preview a73c82f`.
- The criteria table has a `Local` and a `Preview` column.
- The performance base is current production. Say so in the base line.
- The tests table is replaced by the CI checks for the head commit, one row per check, with the E2E run among them (`../ns-route/references/topic-reading-ci.md` "Reading CI"):

  ```markdown
  ### 🧪 CI checks · `a73c82f`
  | Check | Result | Time |
  |---|:---:|:---:|
  | checks (types + lint) | ✅ | 48 s |
  | test | ✅ | 1 m 54 s |
  | build | ✅ | 1 m 20 s |
  | E2E (preview) | ✅ **4 / 4** | 2 m 31 s |
  ```

- One line says how the run got past the host's protection, without the value: `This run used the project's protection bypass.`
- A criterion that cannot be proven on a preview is ➖ with the reason and where it was proven.

## Production (`<!-- ns-verify:production -->`)

The same shape, with these differences:

- The banner names production, the merge commit, and the version when the project has versioning: `🟢 95 / 100 · SAFE TO RELEASE · production 58473bd · v1.5.0`.
- The criteria table has `Local`, `Preview`, and `Production` columns. A step that was not run on production reads `not run on production, proven on preview`.
- The performance base is this PR's preview.
- The tests table is the production E2E run: `E2E (production) · ✅ 2 / 2 @smoke · 41 s`, with the run's link.
- It ends with the undo: the step, how long it takes, and whether it was checked.

## Rules

- Every number is real and comes from the result file. A number that is not known is left out.
- A FAILED or PARTIAL run uses `[!CAUTION]` or `[!WARNING]`, and lists what failed or what waits on the user directly under the banner.
- A manual run says so in the banner and quotes the user's report as the proof.
- A skipped target is still posted: `[!WARNING]`, "not proven on <target>", and the reason.
- A change with no screen has no performance table and no screenshots. Say `no page touched` in the stat strip and show the requests or measured numbers in the proof column.
- A re-run adds `Previous run: <sha> <verdict>` under the banner.
- Keep the two marker lines first, exactly as shown. The second one is how later runs find the evidence page.
