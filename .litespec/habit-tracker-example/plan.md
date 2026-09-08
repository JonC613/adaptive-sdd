---
feature: habit-tracker-example
artifact: plan
status: implementing
owner: user
version: 0.1
created: 2026-09-06
updated: 2026-09-06
spec_version: 0.1
---

# Implementation Plan: Habit Tracker Example

## Technical approach

Build a dependency-free static web application using HTML, CSS, and JavaScript beneath `plugins/adaptive-sdd/examples/habit-tracker/`. A browser opens `index.html` directly; no bundler, server, or package installation is needed.

Keep state and date logic in small testable JavaScript functions, with a thin DOM layer for the daily list, habit editor, and calendar. Persist one versioned JSON document in `localStorage`; validate it at load time and fall back to an empty state when it is absent or malformed.

## Key decisions

### KD-01 — Use a dependency-free static application

- **Choice:** Native HTML, CSS, and JavaScript with no build tooling.
- **Rationale:** The repository has no frontend runtime and the example must run without a server or external service.
- **Alternatives considered:** A framework-based app with npm tooling; a Python-served app.
- **Consequences:** The example is portable and easy to inspect, but UI state management remains intentionally small and bespoke.

### KD-02 — Store normalized local data with date keys

- **Choice:** Persist a versioned document containing habits and completion dates keyed as local `YYYY-MM-DD` strings.
- **Rationale:** Local date keys directly model the approved daily check-in behavior and simplify calendar lookup without time-zone conversion.
- **Alternatives considered:** One storage item per habit; timestamp-based completion records.
- **Consequences:** Clearing site data removes the example's records, and future schema changes require an explicit migration decision.

### KD-03 — Use semantic controls and status text

- **Choice:** Use native buttons, labels, dialog confirmation, and an announced validation/status region.
- **Rationale:** This supports the keyboard and accessible-name requirements without a UI dependency.
- **Alternatives considered:** Clickable non-semantic containers; a custom modal implementation.
- **Consequences:** The visual design follows native accessibility conventions and requires focused manual browser checks.

## Impacted areas

| Area | Expected change | Related IDs |
|---|---|---|
| `plugins/adaptive-sdd/examples/habit-tracker/index.html` | App structure and accessible controls | US-01–US-04, NFR-01 |
| `plugins/adaptive-sdd/examples/habit-tracker/styles.css` | Responsive visual hierarchy and completion/calendar states | AC-02.1–AC-03.2 |
| `plugins/adaptive-sdd/examples/habit-tracker/app.js` | State, storage, date, rendering, and event behavior | R-01–R-04, NFR-02–NFR-03 |
| `plugins/adaptive-sdd/examples/habit-tracker/app.test.mjs` | Automated state and calendar logic evidence | AC-01.1–AC-04.2 |
| `plugins/adaptive-sdd/examples/habit-tracker/README.md` | Direct-open instructions, scope, and local-data behavior | R-04, NFR-02 |

## Technical detail

### State model

```text
HabitTrackerState v1
├── habits: [{ id, name, completionDates: ["YYYY-MM-DD", ...] }]
└── selectedHabitId: string | null
```

The UI derives today's state from the device's local date. Completion toggling adds or removes only that date key. Calendar rendering receives a habit plus a displayed year and month and produces the correct day positions and completed-date state.

## Risks and mitigations

| Risk | Impact | Mitigation | Evidence or trigger |
|---|---|---|---|
| Malformed or unavailable local storage | The app could fail during load | Validate storage reads; use an empty state and announce recovery | Automated invalid-storage case and browser check |
| Time-zone or month-boundary errors | A completion could appear on the wrong date | Use local date-part formatting only; do not serialize timestamps | Automated month and leap-year tests |
| Irreversible habit removal | Local history could be lost unexpectedly | Require explicit in-app confirmation before deletion | Manual flow check and automated deletion-state test |

## Implementation phases

### Phase 1 — Runnable shell and reliable local state

- [ ] **P1-T1 — Create the standalone example shell and documentation**
  - Covers: R-04, NFR-02
  - Depends on: None
  - Work: Add the example directory, direct-open HTML shell, baseline styles, and README instructions.
  - Verify: Open `index.html` locally and confirm the empty state and README instructions are accurate.

- [ ] **P1-T2 — Implement validated state, date, and storage utilities**
  - Covers: AC-04.1, AC-04.2, NFR-03
  - Depends on: P1-T1
  - Work: Implement the versioned storage document, defensive loading, local date-key helpers, and state mutation functions.
  - Verify: Automated tests demonstrate reload-equivalent state restoration and malformed-data recovery.

### Phase 2 — Manage habits and check in today

- [ ] **P2-T1 — Build accessible habit creation, rename, and removal flows**
  - Covers: AC-01.1, AC-01.2, AC-01.3, NFR-01
  - Depends on: P1-T2
  - Work: Render the daily habit list; add validation, rename controls, and confirmed deletion behavior.
  - Verify: Automated state tests and a keyboard-only browser pass cover create, rename, invalid input, and deletion.

- [ ] **P2-T2 — Add reversible daily completion controls**
  - Covers: AC-02.1, AC-02.2, AC-02.3
  - Depends on: P2-T1
  - Work: Render today-specific completion buttons and persist toggle actions without duplicate records.
  - Verify: Automated toggle tests and a reload browser check show correct current-day state.

### Phase 3 — Calendar history and evidence

- [ ] **P3-T1 — Implement selected-habit calendar history**
  - Covers: AC-03.1, AC-03.2, AC-03.3
  - Depends on: P2-T2
  - Work: Add selected-habit calendar rendering, accessible month navigation, and distinct completed-date styling.
  - Verify: Automated calendar tests cover month lengths, leap-year February, navigation, and empty history.

- [ ] **P3-T2 — Add automated checks and perform the acceptance walkthrough**
  - Covers: AC-01.1–AC-04.2, NFR-01–NFR-03
  - Depends on: P3-T1
  - Work: Add a direct Node test command for pure application logic, document it, and execute the full browser acceptance walkthrough.
  - Verify: The automated command passes and the walkthrough records evidence for every acceptance criterion.

## Release and rollback considerations

- **Release:** The example is released with the repository as static files; no deployment or database migration is required.
- **Rollback:** Removing the example files reverts repository content only. Visitors' browser-local example data remains isolated and is never stored by the repository.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-09-06 | Initial draft | Derived from approved specification | All |
