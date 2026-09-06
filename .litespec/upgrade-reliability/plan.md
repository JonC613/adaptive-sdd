---
feature: upgrade-reliability
artifact: plan
status: done
owner: user
version: 0.1
created: 2026-09-05
updated: 2026-09-05
spec_version: 0.1
---

# Implementation Plan: Upgrade reliability
## Technical approach
Harden the existing entrypoints in place, preserving their invocation and fixtures.
## Key decisions
Keep stdlib Python and PowerShell. Stage copies beside destinations and retain
backups; do not recursively delete an existing installation. Report structural
validity independently from delivery evidence.
## Impacted areas
Installers, validators, memory script, regression tests and documentation.
## Implementation phases
- [x] **P1-T1 — Safe installation**
  - Covers: AC-01.1
  - Depends on: None
  - Work: Preflight, canonical safety checks, staging and recoverable replacement.
  - Verify: Isolated PowerShell execution tests.
- [x] **P1-T2 — Structural validation**
  - Covers: AC-01.2
  - Depends on: None
  - Work: Metadata, graph, coverage checks and JSON diagnostics.
  - Verify: Negative fixtures and supported examples.
- [x] **P1-T3 — Freshness and regressions**
  - Covers: AC-01.3, AC-01.4
  - Depends on: P1-T1, P1-T2
  - Work: Working-tree detection, configurable exclusions, docs and tests.
  - Verify: Full local suite; report CI separately.
## Amendment history
| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-09-05 | Initial slice | Approved upgrade roadmap | All |
