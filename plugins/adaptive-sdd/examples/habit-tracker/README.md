# Daymark habit tracker

A runnable, dependency-free browser example for the Adaptive SDD LiteSpec workflow.

## Run it

Open `index.html` directly in a modern browser. No server, package installation, account, or network connection is required.

## Verify it

Run the automated state and calendar checks with:

```powershell
node --test app.test.mjs
```

Then complete the keyboard and local-storage walkthrough documented in [the test plan](../../../../.litespec/habit-tracker-example/tests.md).

## Data and scope

Habits and completed dates are saved only in this browser's local storage. Clearing site data resets the example. Daymark intentionally excludes accounts, synchronization, reminders, analytics, and data import/export.
