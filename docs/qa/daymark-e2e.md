# Daymark end-to-end test catalog

This catalog is written for QA review and doubles as the visual-validation index for the Playwright suite. Each image is a Playwright screenshot baseline: a normal test run compares the current app against it, and `npm run test:e2e:update` intentionally refreshes it after a reviewed UI change.

## Reproducible environment

Committed baselines are `chromium-win32`. CI uses **windows-2022** (Windows Server 2022), **Node 22.14.0**, and **Playwright 1.63.0**, exactly pinned with `package-lock.json`. `npm ci` and `npx playwright install chromium` select its bundled Chromium; do not substitute a system Chrome channel. Locale is `en-US`, timezone is `America/Chicago`, and the test clock is fixed. Hosted Windows images still receive updates, so exact OS/font identity is not immutable.

Use Windows for visual comparisons. Linux/macOS have no approved baselines; a normal run fails on missing baselines and must not generate them automatically. An intentional expansion to another platform needs separately reviewed images. Config sets `updateSnapshots: "none"`; only the explicit local update command overrides it.

Before the first run:

```text
npm ci
npx playwright install chromium
```

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

## CI artifacts and review

The browser job uploads `playwright-report/` and `test-results/` even on failure, with 14-day retention. Open the HTML report to inspect retries, expected/actual/diff screenshots, and retained failure traces or videos. A retry that passes should still be reviewed as a flaky result. No CI step updates baselines.

For an intentional visual change, run the local update command, inspect the complete image diff in version control, and rerun the normal suite. A green run after an unreviewed baseline replacement is not visual regression evidence.
