---
feature: simple-kanban
artifact: tests
status: done
owner: user
version: 1.1
created: 2026-08-15
updated: 2026-08-15
spec_version: 1.1
plan_version: 1.1
---

# Test Plan: Simple Kanban

## Strategy

Use component-level interaction tests for task creation, movement, editing, deletion, dialog behavior, and local-storage synchronization. These checks are faster and more focused than repeating every branch through a deployed browser. Retain a small server-render test for page metadata and initial product structure, plus a production build check for the vinext deployment boundary.

Use one narrow end-to-end smoke flow only if the component environment cannot prove native drag data transfer or the deployed static Markdown route. Responsive visual quality remains a documented manual exception; semantic accessibility and keyboard behavior should be automated.

## Acceptance traceability

| Acceptance criterion | Test IDs | Method | Status |
|---|---|---|---|
| AC-01.1 | T-01 | Automated | Passed |
| AC-01.2 | T-02 | Automated | Passed |
| AC-02.1 | T-03 | Automated | Passed |
| AC-02.2 | T-04 | Automated | Passed |
| AC-03.1 | T-05 | Automated | Passed |
| AC-03.2 | T-06 | Automated | Passed |
| AC-03.3 | T-07 | Automated | Passed |
| AC-04.1 | T-08 | Automated | Passed |
| AC-04.2 | T-09 | Automated | Passed |
| AC-05.1 | T-10 | Automated | Passed |
| AC-05.2 | T-11 | Automated | Passed |
| AC-05.3 | T-15 | Automated | Passed |

## Critical user flows

### T-01 — Create a task

- Covers: AC-01.1
- Level: component
- Setup: Render an empty board with available browser storage.
- Action: Enter `Prepare release` and submit.
- Expected: One To Do card appears at the top, the count becomes one, and the input clears.

### T-03 — Move a task between columns

- Covers: AC-02.1
- Level: component
- Setup: Render one task in To Do with a controllable data-transfer object.
- Action: Drag and drop the task onto In Progress.
- Expected: The task appears once in In Progress and both counts update.

### T-05 — Edit a title inline

- Covers: AC-03.1
- Level: component
- Setup: Render a task named `Draft notes`.
- Action: Save `Publish notes` with Enter, then begin another edit and cancel with Escape.
- Expected: The first edit persists and the cancelled edit restores `Publish notes`.

### T-08 — Restore the working board

- Covers: AC-04.1
- Level: component
- Setup: Seed storage with tasks in all three states, including an edited title.
- Action: Render the app as a fresh session.
- Expected: Titles, states, and counts match the stored board without an initial destructive write.

### T-10 — Read and close the Docs library

- Covers: AC-05.1
- Level: component
- Setup: Render the board.
- Action: Open Docs, select a document, and close it separately through Escape, the close control, and the backdrop.
- Expected: The labeled library loads the complete document and each close path dismisses it without changing tasks.

### T-11 — Open raw documentation

- Covers: AC-05.2
- Level: integration
- Setup: Build the production application.
- Action: Request every manifest path and inspect each selected document's raw link target.
- Expected: Each route returns its Markdown asset and the link points to the selected file.

### T-15 — Verify the complete document inventory

- Covers: AC-05.3, R-07
- Level: integration
- Setup: Read the document manifest, canonical sources, and `public/docs/` tree.
- Action: Compare the nine expected entries and compare every published copy byte-for-byte with its canonical source.
- Expected: All nine categorized documents are present, uniquely linked, and current.

## Failure and recovery cases

### T-02 — Reject empty capture

- Covers: AC-01.2
- Level: component
- Setup: Render an empty board.
- Action: Enter spaces only and attempt submission.
- Expected: No task is created and the submit control remains unavailable.

### T-04 — Show and clear a valid drop target

- Covers: AC-02.2
- Level: component
- Setup: Render one draggable task.
- Action: Enter a target column during drag, then leave or complete the drop.
- Expected: Target styling appears only during the valid drag state and is cleared afterward.

### T-06 — Confirm individual deletion

- Covers: AC-03.2
- Level: component
- Setup: Render one named task and stub confirmation.
- Action: Cancel one deletion attempt, then confirm a second.
- Expected: Cancel preserves the task; confirm removes exactly that task.

### T-07 — Clear Done safely

- Covers: AC-03.3
- Level: component
- Setup: Render tasks across all columns and stub confirmation.
- Action: Cancel and then confirm Clear done.
- Expected: Cancel preserves all tasks; confirm removes only Done tasks; the control becomes disabled.

### T-09 — Recover from invalid storage

- Covers: AC-04.2
- Level: component
- Setup: Make storage return invalid JSON and separately throw on read or write.
- Action: Render and use the board.
- Expected: The app presents an empty usable board and supports in-session task actions without crashing.

## Quality checks

### T-12 — Keyboard and semantic accessibility

- Covers: NFR-01
- Level: component
- Setup: Render populated board and specification dialog states.
- Action: Run automated accessibility checks and operate forms, editing, confirmations, and dialog controls by keyboard.
- Expected: No serious automated violations occur; labeled controls and visible focus support the defined keyboard flows.

### T-13 — Local-only data behavior

- Covers: NFR-03, NFR-04
- Level: component
- Setup: Spy on network access and storage operations.
- Action: Create, edit, move, and delete tasks with successful and failing storage.
- Expected: No task payload is transmitted, and storage failure does not break the session.

### T-14 — Reduced motion

- Covers: NFR-05
- Level: static
- Setup: Inspect the compiled stylesheet.
- Action: Locate the reduced-motion media query.
- Expected: Nonessential transitions are disabled under the preference.

## Manual exceptions

### M-01 — Responsive visual composition

- Covers: NFR-02
- Automation limitation: Layout rules can be asserted automatically, but readable composition and absence of awkward clipping remain visual judgments.
- Method: Review the board and specification dialog at representative narrow and desktop widths with empty and populated columns.
- Expected evidence: Review record confirming single-column mobile layout, no horizontal page scrolling, readable dialog content, and usable controls.

### M-02 — Touch drag compatibility

- Covers: A-02
- Automation limitation: Native drag behavior depends on the actual browser and input device.
- Method: Attempt task movement on each agreed touch-device/browser target.
- Expected evidence: Compatibility record. Any failure triggers a proposed interaction amendment before declaring broad touch support.

## Test data and setup

- Empty storage.
- Valid stored tasks in each status.
- Invalid JSON and storage operations that throw.
- Titles containing leading or trailing whitespace and the 120-character boundary.
- Stubbed confirmation responses for cancel and confirm paths.
- A controllable drag data-transfer object.
- Representative narrow and desktop viewport widths for M-01.

## Completion criteria

- [x] Every current-release acceptance criterion maps to passing automated evidence.
- [x] T-01 through T-15 pass at their specified levels.
- [x] M-01 and M-02 remain recorded manual exceptions; no additional device targets were agreed for this release.
- [x] The production build succeeds.
- [x] All nine public Markdown copies match their canonical source documents byte-for-byte.
- [x] No unresolved failure blocks an approved story or non-functional requirement.

## Release evidence

- `validate_litespec.py --approved`: passed for all three version 1.1 artifacts and 12 acceptance criteria.
- `npm test`: production build passed; server render, CRUD contract presence, nine-document inventory, and canonical-copy checks passed.
- `npm run lint`: passed after excluding generated deployment archives under `work/`.
- M-01 and M-02 remain explicit manual checks because no browser or touch-device review was requested for this release.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 1.0 | 2026-08-15 | Initial worked-example test plan | Derived from LiteSpec example versions 1.0 | All |
| 1.1 | 2026-08-15 | Add Docs library inventory, raw-file, and canonical-copy coverage | Verify approved specification amendment 1.1 | R-06, R-07, US-05, AC-05.1–AC-05.3 |
