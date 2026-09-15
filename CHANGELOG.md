# Changelog

## Unreleased

- Reject empty, malformed, and unsupported strict delivery criteria; preserve task-free TinySpec and recognize the documented legacy and Spec Kit formats.
- Recheck discovered criteria, current evidence, and evidence-source fingerprints; a later failure supersedes an earlier pass. Old evidence lacking a source fingerprint must be rerun and recorded.
- Replace inferred evaluation metrics with exact per-scenario unittest outcomes and document an optional, unrun live-agent protocol.
- Correct unsupported-Python diagnostics and test dependency availability independently of the host.
- Add JavaScript, Windows Chromium, and repository checks to CI; pin browser tooling and disable implicit snapshot updates.
- Lead documentation with the product and runnable example; add an ongoing-pilot case study, demo script, and release checklist.

## 0.4.1 - 2026-09-06

- Add the Daymark runnable habit-tracker example with a QA-oriented Playwright suite and committed visual baselines.
- Keep examples, browser-test tooling, QA documentation, and development dependencies repository-local; Codex and Cursor installations continue to ship only the shared Adaptive SDD skill.

## 0.4.0 - 2026-09-05

- Harden installation with preflight checks, staged copies, and recoverable backups.
- Strengthen structural validation and add machine-readable diagnostics.
- Detect committed and working-tree Project Memory drift.
- Add resumable delivery state, fingerprint-bound approvals, evidence gates, and release references.
- Add interaction modes, optional project profiles, local diagnostics, and deterministic workflow evaluations.

Compatibility: existing specifications and memory remain readable and are not
automatically migrated. Historical `done` artifacts are not inferred to be verified.
Live marketplace and Spec Kit compatibility require separate integration checks.
