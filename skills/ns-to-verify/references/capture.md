# Evidence capture

For a change with UI, read `references/ui.md`.

| Capture | When |
|---|---|
| Every criterion walked in a real browser | always |
| A mobile and a desktop screenshot of each changed screen | always |
| One demo clip of the main flow | always |
| Console errors and failed requests on every page visited | always |
| Lighthouse and the web vitals on every touched page, mobile and desktop, against the base | always, on every target |
| Tablet viewport | layout or breakpoint styles changed |
| A clip per criterion | a bug fix (before and after), or the user asks |
| Accessibility scan and keyboard walk | a new interactive control, form, dialog, or navigation |

A change with no screen leaves the UI rows out and says so. High or critical risk captures all of it. The result card lists each conditional capture as added or left out, with the reason, and the user can add any of them.
