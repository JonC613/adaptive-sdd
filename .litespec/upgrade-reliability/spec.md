---
feature: upgrade-reliability
artifact: spec
status: done
owner: user
version: 0.2
created: 2026-09-05
updated: 2026-09-05
---

# Specification: Upgrade reliability

## Summary
Implement Release 1 of the user-approved upgrade roadmap.

## Problem
Installation can replace unsafe destinations, validators accept invalid mappings,
and commit-only memory freshness misses local changes.

## Desired outcome
Users get safe installation and truthful, actionable structural diagnostics.

## Requirements
### Current release
- **R-01:** Harden installation, validation, and freshness without migrating projects.
### Deferred
- Delivery evidence, interaction modes, profiles, and distribution are later releases.

## User stories
### US-01 — Trust repository maintenance
**Story:** As a maintainer, I want checks and installers to fail safely.
**Rationale:** Safety and honest diagnostics underpin later delivery verification.
**Acceptance criteria:**
- **AC-01.1:** Installers preflight before writes, reject unsafe destinations, and preserve replacements in backups.
- **AC-01.2:** Structural validators reject invalid metadata, dependencies, and traceability with stable diagnostics and optional JSON output.
- **AC-01.3:** Memory reports committed and working-tree drift without claiming factual error or ignoring specifications by default.
- **AC-01.4:** Isolated negative regression tests pass alongside existing supported fixtures.
**Edge cases:** Missing tools, failed copy, duplicate keys, cycles, stale memory, non-Git and shallow repositories.
Platform-managed symlink ancestors are allowed, while the installation destination itself must not be a link.

## Non-functional requirements
- No network or paid API calls in default regression tests.
- Existing installed artifacts are not automatically rewritten.

## Codebase context
Shared Python scripts and PowerShell installers serve both agent integrations.

## Assumptions and open questions
- User authorized the roadmap and implementation together; this slice records its bounded requirements.
- Full upstream installation is not transactional; report any external initialization failure explicitly.

## Amendment history
| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-09-05 | Initial slice | Approved upgrade roadmap | All |
| 0.2 | 2026-09-05 | Clarify safe handling of linked path ancestors | macOS CI exposed `/var` as a normal platform symlink | AC-01.1, AC-01.4 |
