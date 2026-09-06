---
feature: habit-tracker-example
artifact: spec
status: implementing
owner: user
version: 0.1
created: 2026-09-06
updated: 2026-09-06
---

# Specification: Habit Tracker Example

## Summary

Create a runnable, self-contained habit tracker under `plugins/adaptive-sdd/examples/habit-tracker/`. It demonstrates Adaptive SDD 0.4 with daily check-ins, browser-local persistence, a quick daily list, and calendar history.

## Problem

The repository has specification-only examples, but no runnable application that demonstrates how a LiteSpec can guide a small, locally persistent user-facing product from intent through verification.

## Desired outcome

A person can define habits, complete or undo today's check-in from a concise list, and inspect each habit's history in a calendar. Their data remains available after reopening the app on the same browser and device.

## Boundaries

### Goals

- Provide an executable example app alongside the existing Adaptive SDD examples.
- Make daily completion fast, visible, and reversible.
- Preserve habit names and completion history locally in the browser.

### Non-goals

- User accounts, cloud synchronization, shared habits, reminders, notifications, and analytics.
- Native mobile packaging, a backend service, or a production deployment.
- Importing or exporting data.

### Constraints

- The example runs without a server or external service.
- It lives under `plugins/adaptive-sdd/examples/habit-tracker/` and does not change the installed Adaptive SDD workflow or existing examples.

## Requirements

### Current release

- **R-01:** Visitors can add, rename, and remove habits.
- **R-02:** Visitors can record and undo a completion for the current local calendar day from a daily habit list.
- **R-03:** Visitors can view a selected habit's completion history in a navigable calendar.
- **R-04:** Habit data and completion history persist locally across browser reloads on the same device.

### Deferred

- **D-01:** Streak counts, targets, and progress summaries.
- **D-02:** Reminders, notifications, account sign-in, cloud sync, and cross-device sharing.
- **D-03:** Data import and export.

## User stories

### US-01 — Manage personal habits

**Story:** As a person building a routine, I want to create and maintain my list of habits, so that the daily list reflects what I currently want to practice.

**Rationale:** A tracker has no value until it contains habits meaningful to its user, and routines change over time.

**Acceptance criteria:**

- **AC-01.1:** A visitor can add a non-empty habit name and sees it in the daily list.
- **AC-01.2:** A visitor can rename an existing habit and the new name appears in the daily list and calendar view.
- **AC-01.3:** Given an existing habit, when the visitor removes it, then it and its recorded check-ins no longer appear in the app.

**Edge cases:**

- Empty or whitespace-only names are not added and the visitor receives an understandable validation message.
- Removing a habit requires an in-app confirmation because it also removes that habit's local history.

### US-02 — Check in for today

**Story:** As a person tracking my routine, I want to mark or undo today's completion from a quick list, so that daily tracking takes minimal effort.

**Rationale:** The daily list is the primary interaction and must make the current state clear at a glance.

**Acceptance criteria:**

- **AC-02.1:** The daily list displays every saved habit with an explicit control for today's completion state.
- **AC-02.2:** Given an incomplete habit, when the visitor marks it complete, then the list visibly shows it as complete for the current local calendar day.
- **AC-02.3:** Given a completed habit, when the visitor undoes the check-in, then the list visibly shows it as incomplete for the current local calendar day.

**Edge cases:**

- Repeating a mark or undo action does not create duplicate records or affect another date.
- When no habits exist, the daily view explains how to create the first one.

### US-03 — Review calendar history

**Story:** As a person reflecting on consistency, I want to see a habit's completed dates in a calendar, so that I can understand its recent history.

**Rationale:** A calendar complements quick check-ins with a visual history without adding goals or analytics to this release.

**Acceptance criteria:**

- **AC-03.1:** A visitor can choose a habit and see a calendar for that habit.
- **AC-03.2:** Dates completed for the selected habit are visually distinct from incomplete dates.
- **AC-03.3:** A visitor can navigate to earlier and later calendar months without changing recorded completions.

**Edge cases:**

- A habit with no completions displays a readable calendar with no dates marked complete.
- Calendar navigation correctly represents month lengths and leap-year February.

### US-04 — Keep local progress

**Story:** As a returning visitor, I want my habits and check-ins to remain on this device, so that I do not have to recreate my progress after closing the app.

**Rationale:** Local persistence meets the requested continuity without requiring accounts or a backend.

**Acceptance criteria:**

- **AC-04.1:** Given saved habits and check-ins, when the visitor reloads the app in the same browser, then the daily list and calendar history retain the saved state.
- **AC-04.2:** Habit edits, removals, completions, and undone completions remain reflected after a reload.

**Edge cases:**

- If no usable saved data exists, the app opens in its empty state instead of failing.
- Data remains local; the app does not require sign-in or make a network request to store habit data.

## Non-functional requirements

- **NFR-01 — Accessibility:** All interactive controls are reachable by keyboard and expose an accessible name that communicates their action or state.
- **NFR-02 — Privacy:** Habit data is stored only in browser-local storage; no account or remote data service is used.
- **NFR-03 — Resilience:** The app presents a usable empty state when local data is absent or cannot be read.

## Codebase context

`plugins/adaptive-sdd/examples/` contains the `simple-kanban` specification example and profile documents, but no runnable client application or frontend build setup. The plugin uses Markdown artifacts and Python validation tests; the habit tracker will be isolated beneath its own example directory and include its own runnable assets and verification approach.

## Assumptions and open questions

### Assumptions

- **A-01:** The example may use browser-local storage supported by modern browsers; clearing browser site data resets saved habits and history.
- **A-02:** The app starts with no preloaded habits so its empty-state and creation flow are demonstrated.
- **A-03:** A calendar presents one selected habit at a time; comparing several habits on one calendar is deferred.

### Open questions

- None.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-09-06 | Initial draft | Approved LiteSpec discovery | All |
