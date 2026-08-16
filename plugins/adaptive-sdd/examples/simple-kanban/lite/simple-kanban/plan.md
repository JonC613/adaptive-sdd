---
feature: simple-kanban
artifact: plan
status: done
owner: user
version: 1.1
created: 2026-08-15
updated: 2026-08-15
spec_version: 1.1
---

# Implementation Plan: Simple Kanban

## Technical approach

Keep Simple Kanban as a client-side React page within the existing vinext application. Represent each task with a stable ID, title, status, and creation time. Maintain the active board in React state and synchronize it to browser local storage only after initial restoration completes.

Render the three fixed columns from shared metadata, derive per-column task groups from state, and update task status through native drag-and-drop events. Keep a document manifest in the client and open an accessible Docs library that fetches published Markdown copies on demand.

## Key decisions

### KD-01 — Browser-local persistence

- **Choice:** Store tasks as versioned JSON in `localStorage`.
- **Rationale:** R-05 and NFR-03 explicitly require device-local state without accounts or a backend.
- **Alternatives considered:** IndexedDB; hosted database.
- **Consequences:** The implementation remains small, but tasks do not synchronize and may be lost when browser data is cleared.

### KD-02 — Native drag and drop

- **Choice:** Use the browser drag-and-drop API for inter-column movement.
- **Rationale:** It satisfies R-03 without adding a dependency and matches the approved interaction constraint.
- **Alternatives considered:** Pointer-event drag implementation; drag library; move buttons.
- **Consequences:** Desktop pointer support is simple, but touch behavior requires explicit compatibility verification and keyboard movement remains deferred.

### KD-03 — Embedded documentation library

- **Choice:** Render a categorized document navigator and complete Markdown reader in a modal, with each canonical document copied to a stable public path.
- **Rationale:** R-06, R-07, AC-05.1, AC-05.2, and AC-05.3 require one discoverable surface for all nine documents while retaining raw-file access.
- **Alternatives considered:** A second application route; a single specification summary; raw Markdown links only.
- **Consequences:** Published copies must be checked against their canonical sources before release.

## Impacted areas

| Area | Expected change | Related IDs |
|---|---|---|
| `app/page.tsx` | Task state, CRUD, drag and drop, persistence, document manifest, and Docs library | US-01–US-05, AC-05.1, AC-05.2, AC-05.3 |
| `app/globals.css` | Board, card, focus, dialog, responsive, and reduced-motion styles | NFR-01, NFR-02, NFR-05 |
| `public/docs/` | Nine deployable Markdown copies | R-07, AC-05.2, AC-05.3 |
| `tests/rendered-html.test.mjs` | Server-shell, feature-presence, and canonical-copy checks | AC-05.1, AC-05.2, AC-05.3 |
| Behavioral test surface | Automated interaction and storage tests | AC-01.1–AC-04.2 |

## Risks and mitigations

| Risk | Impact | Mitigation | Evidence or trigger |
|---|---|---|---|
| Native drag behavior varies on touch devices | Users may see a responsive board but be unable to move cards | Verify agreed browser/device targets; propose a pointer or explicit-move amendment if required | Compatibility test cannot complete a move |
| Canonical and published documentation drift | A public file may become stale | Copy all nine documents during the amendment and compare each pair in the test suite | Any public copy differs from its canonical source |
| Early persistence write | Stored tasks could be replaced by the initial empty state | Gate writes behind a restoration-ready flag | Reload test loses seeded tasks |

## Implementation phases

### Phase 1 — Reliable local task model

- [x] **P1-T1 — Implement restoration-safe task state**
  - Covers: US-04, AC-04.1, AC-04.2, NFR-03, NFR-04
  - Depends on: None
  - Work: Define the task model, safe read helper, readiness flag, and guarded persistence effect.
  - Verify: Storage restoration, invalid-data fallback, and in-session behavior pass automated tests.

- [x] **P1-T2 — Implement task capture**
  - Covers: US-01, AC-01.1, AC-01.2
  - Depends on: P1-T1
  - Work: Add the To Do form, input normalization, stable IDs, length limit, and empty state transition.
  - Verify: Valid and whitespace-only creation cases pass.

### Phase 2 — Board workflow and maintenance

- [x] **P2-T1 — Implement inter-column movement**
  - Covers: US-02, AC-02.1, AC-02.2
  - Depends on: P1-T1
  - Work: Add draggable cards, droppable columns, target styling, state updates, and count derivation.
  - Verify: Movement, same-column drops, empty targets, and counts pass automated interaction tests.

- [x] **P2-T2 — Implement editing and destructive actions**
  - Covers: US-03, AC-03.1, AC-03.2, AC-03.3
  - Depends on: P1-T1
  - Work: Add inline edit lifecycle, individual deletion confirmation, and confirmed clearing of Done.
  - Verify: Save, cancel, invalid edit, delete cancel/confirm, and clear-done cases pass.

### Phase 3 — Documentation transparency and quality

- [x] **P3-T1 — Add the in-app Docs library**
  - Covers: US-05, AC-05.1, AC-05.2, AC-05.3, R-06, R-07, NFR-01
  - Depends on: P1-T2, P2-T1, P2-T2
  - Work: Add the categorized manifest, document navigation, loading and error states, complete Markdown reader, close paths, and raw Markdown links.
  - Verify: Library interaction, inventory, and static-asset consistency tests pass.

- [x] **P3-T2 — Complete responsive and accessibility behavior**
  - Covers: NFR-01, NFR-02, NFR-05
  - Depends on: P3-T1
  - Work: Add responsive breakpoints, semantic labels, focus visibility, and reduced-motion handling.
  - Verify: Automated accessibility checks pass and the documented responsive manual exception has evidence.

- [x] **P3-T3 — Run cross-artifact and production validation**
  - Covers: All current-release IDs
  - Depends on: P3-T2
  - Work: Run the build, test suite, traceability audit, and specification-copy consistency check.
  - Verify: Every completion criterion in `tests.md` is satisfied with no orphan IDs.

## Release and rollback considerations

- **Release:** Publish only after the production build and current-release evidence pass. Existing browser data must remain readable under the unchanged storage key.
- **Rollback:** Redeploy the previous site version. Because the data schema is unchanged and browser-local, no server data rollback is required.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 1.0 | 2026-08-15 | Initial worked-example plan | Derived from LiteSpec example version 1.0 | All |
| 1.1 | 2026-08-15 | Plan the nine-document in-app library and canonical-copy validation | Implement approved specification amendment 1.1 | R-06, R-07, US-05, AC-05.1–AC-05.3 |
