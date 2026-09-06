---
feature: habit-tracker-example
artifact: tests
status: implementing
owner: user
version: 0.1
created: 2026-09-06
updated: 2026-09-06
spec_version: 0.1
plan_version: 0.1
---

# Test Plan: Habit Tracker Example

## Strategy

Use Node's built-in test runner for the state, storage-validation, date-key, and calendar functions. These pure functions cover the persistence and date boundary behavior more reliably than browser-only checks. Use a short manual browser walkthrough for semantic controls, keyboard behavior, and direct-open operation, which cannot be reliably verified without introducing a browser-test dependency to this otherwise dependency-free example.

## Acceptance traceability

| Acceptance criterion | Test IDs | Method | Status |
|---|---|---|---|
| AC-01.1 | T-01 | Automated | Planned |
| AC-01.2 | T-02 | Automated | Planned |
| AC-01.3 | T-02 | Automated | Planned |
| AC-02.1 | T-03 | Automated | Planned |
| AC-02.2 | T-03 | Automated | Planned |
| AC-02.3 | T-04 | Automated | Planned |
| AC-03.1 | T-05 | Automated | Planned |
| AC-03.2 | T-05 | Automated | Planned |
| AC-03.3 | T-06 | Automated | Planned |
| AC-04.1 | T-07 | Automated | Planned |
| AC-04.2 | T-07 | Automated | Planned |

## Critical user flows

### T-01 — Add a valid habit

- Covers: AC-01.1
- Level: unit
- Setup: An empty valid tracker state.
- Action: Add a trimmed non-empty habit name.
- Expected: State contains one habit with the supplied display name and it is available to the daily-list renderer.

### T-02 — Rename and remove a habit

- Covers: AC-01.2, AC-01.3
- Level: unit
- Setup: A state containing one habit and at least one completion date.
- Action: Rename the habit, then confirm its removal.
- Expected: The new name is retained until removal; removal eliminates the habit and all its completion dates.

### T-03 — Complete today's habit from the daily state

- Covers: AC-02.1, AC-02.2
- Level: unit
- Setup: One incomplete habit and a fixed local date key.
- Action: Render its daily state, then mark it complete.
- Expected: Rendering exposes an incomplete action first and a completed state after the toggle; the fixed date key is stored once.

### T-04 — Undo today's completion without duplicate dates

- Covers: AC-02.3
- Level: unit
- Setup: One habit completed for a fixed local date.
- Action: Undo completion, then repeat completion and undo actions.
- Expected: Undo removes only the fixed date key; repeated actions leave no duplicate dates and do not change another date.

### T-05 — Render selected-habit calendar completion state

- Covers: AC-03.1, AC-03.2
- Level: unit
- Setup: Two habits, one selected, with completed and incomplete dates in a fixed month.
- Action: Build calendar data for the selected habit.
- Expected: The selected habit is represented, its completed dates are marked, and dates for the other habit are not marked.

### T-06 — Navigate calendar months correctly

- Covers: AC-03.3
- Level: unit
- Setup: Fixed displayed months including January and February in leap and non-leap years.
- Action: Move backward and forward one month and generate month-day data.
- Expected: Year boundaries change correctly; day counts and positions match each month, including 29 days in leap-year February.

### T-07 — Restore all saved changes after reload-equivalent loading

- Covers: AC-04.1, AC-04.2
- Level: integration
- Setup: A fake local-storage adapter containing a valid serialized state after create, rename, toggle, undo, and removal mutations.
- Action: Load the storage document into a new application state.
- Expected: The restored state exactly reflects the final saved habit names, removals, and completion dates.

## Failure and recovery cases

### T-08 — Reject blank habit names

- Covers: US-01 edge case
- Level: unit
- Setup: An empty valid tracker state.
- Action: Attempt to add empty and whitespace-only names.
- Expected: No habit is added and the UI-facing validation result describes the correction needed.

### T-09 — Recover from missing or malformed local storage

- Covers: US-04 edge case, NFR-03
- Level: integration
- Setup: Empty storage, malformed JSON, and a valid JSON document with an invalid shape.
- Action: Load each value.
- Expected: Each case returns a usable empty state without throwing; a recoverable status is available to the UI.

### T-10 — Keep empty history readable

- Covers: US-02 and US-03 edge cases
- Level: unit
- Setup: A tracker state with no habits, then a habit with no completion dates.
- Action: Generate daily and calendar view models.
- Expected: The daily model supplies first-habit guidance; the calendar model renders all valid dates with none marked complete.

## Manual exceptions

### M-01 — Keyboard and accessible-control walkthrough

- Covers: NFR-01
- Automation limitation: The dependency-free example deliberately has no browser automation runtime or accessibility-tree tooling.
- Method: Open `index.html` directly, use only Tab, Shift+Tab, Enter, and Space to add a habit, toggle it, select it, navigate the calendar, rename it, and cancel then confirm deletion.
- Expected evidence: Every control receives focus in a usable order; visible labels or accessible names communicate purpose and completion state; validation and deletion confirmation are understandable.

### M-02 — Local-only data walkthrough

- Covers: NFR-02
- Automation limitation: Verifying actual browser storage and direct-open network behavior requires a browser environment.
- Method: In browser developer tools, complete a habit, reload, inspect that the saved document is in local storage, and confirm the Network panel shows no request used to save or load habit data.
- Expected evidence: The state persists after reload, a local-storage entry contains the tracker document, and no remote persistence request appears.

## Test data and setup

- Fixed local date keys: `2026-09-06`, `2026-01-31`, `2026-02-28`, `2028-02-29`, and `2026-12-31`.
- Fixture habits with stable IDs and completion dates for both selected and unselected habits.
- A minimal in-memory local-storage adapter for automated load and save behavior.
- Run the documented `node --test` command from the example directory; no package install, account, service, or environment variable is required.

## Completion criteria

- [ ] Every current-release acceptance criterion maps to passing evidence.
- [ ] Critical user flows pass.
- [ ] Relevant failure and recovery cases pass.
- [ ] Manual exceptions have recorded evidence.
- [ ] No unresolved failure blocks an approved story or non-functional requirement.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-09-06 | Initial draft | Derived from approved specification and plan | All |
