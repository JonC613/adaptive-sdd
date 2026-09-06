# Daymark end-to-end test catalog

This catalog is written for QA review and doubles as the visual-validation index for the Playwright suite. Each image is a Playwright screenshot baseline: a normal test run compares the current app against it, and `npm run test:e2e:update` intentionally refreshes it after a reviewed UI change.

## Run the suite

```powershell
npm run test:e2e
```

Run this only when an intentional visual change has been reviewed:

```powershell
npm run test:e2e:update
```

The suite opens the app through a local test server, fixes the date at September 6, 2026, and gives every test an empty browser-storage state. This makes calendar and screenshot results repeatable.

## Visual flow index

| ID | QA scenario | What to validate | Visual evidence |
|---|---|---|---|
| E2E-01 | First visit | The empty state explains how to add a first habit. | [Empty state](../../tests/e2e/daymark.spec.mjs-snapshots/01-empty-state-chromium-win32.png) |
| E2E-02 | Daily check-in | Blank names show feedback; two habits display; a completion can be marked, undone, and marked again without affecting the other habit. | [Daily check-in](../../tests/e2e/daymark.spec.mjs-snapshots/02-daily-check-in-chromium-win32.png) |
| E2E-03 | Calendar history | A selected habit shows its completed date and both previous- and next-month navigation change the displayed month correctly. | [Calendar history](../../tests/e2e/daymark.spec.mjs-snapshots/03-calendar-history-chromium-win32.png) |
| E2E-04 | Habit management | Rename survives reload; removal requires confirmation and returns to a clear empty state. | [Managed habits](../../tests/e2e/daymark.spec.mjs-snapshots/04-managed-habits-chromium-win32.png) |
| E2E-05 | Keyboard path | The new-habit input and submit button are reachable in a predictable Tab order. | No screenshot; focus behavior is asserted directly. |

## QA execution notes

1. Run `npm run test:e2e` before reviewing a change. A screenshot mismatch is a test failure, not an automatic update.
2. For a visual change, inspect the changed baseline image in this catalog before running `npm run test:e2e:update`.
3. Confirm the expected behavior in the scenario table, especially dialog confirmation, reload persistence, completion state, and calendar month changes.
4. Keep the baseline images in version control; they are the reviewable evidence, not transient test output.
