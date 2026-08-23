---
feature: project-memory
artifact: tests
status: done
owner: user
version: 0.1
created: 2026-08-22
updated: 2026-08-22
spec_version: 0.1
plan_version: 0.1
---

# Test Plan: Project Memory

## Strategy

Use standard-library unit and integration tests with temporary Git and non-Git repositories for deterministic behavior, plus contract fixtures for agent-guided workflows. Exercise the same scripts and assets that are installed into target repositories. Run portability checks on Windows, macOS, and Linux with Python 3.11 or newer; keep provider sessions outside the automated core by testing Codex- and Cursor-style invocation routing against the same shared implementation.

Test at the lowest practical level: parsing and validation rules as units, filesystem and Git safety as temporary-repository integrations, and initialization/update/refresh as end-to-end workflow fixtures. Dogfooding supplies qualitative evidence for usefulness, but every current-release acceptance criterion has automated evidence.

## Acceptance traceability

| Acceptance criterion | Test IDs | Method | Status |
|---|---|---|---|
| AC-01.1 | T-01 | Automated integration | Passing |
| AC-01.2 | T-02 | Automated contract | Passing |
| AC-01.3 | T-03 | Automated integration | Passing |
| AC-01.4 | T-01 | Automated integration | Passing |
| AC-02.1 | T-04 | Automated end-to-end | Passing |
| AC-02.2 | T-05 | Automated CI matrix | Passing |
| AC-02.3 | T-06 | Automated contract | Passing |
| AC-02.4 | T-06 | Automated contract | Passing |
| AC-03.1 | T-07 | Automated contract | Passing |
| AC-03.2 | T-08 | Automated integration | Passing |
| AC-03.3 | T-09 | Automated integration | Passing |
| AC-03.4 | T-10 | Automated end-to-end | Passing |
| AC-03.5 | T-10 | Automated end-to-end | Passing |
| AC-04.1 | T-11 | Automated integration | Passing |
| AC-04.2 | T-12 | Automated parameterized | Passing |
| AC-04.3 | T-13 | Automated integration | Passing |
| AC-04.4 | T-14 | Automated contract | Passing |

## Critical user flows

### T-01 — Initialize an evidence-ready memory bundle

- Covers: AC-01.1, AC-01.4
- Level: integration
- Setup: Temporary clean Git repository at a known commit with no `.sdd/memory/`; render an approved baseline from bundled assets.
- Action: Run the portable scaffold and approved reconciliation operations.
- Expected: The four MVP Markdown files and separate state file exist, declare the pinned OKF/profile versions, record generation and verification fields, and contain the repository commit in state.

### T-02 — Require evidence or an explicit assumption

- Covers: AC-01.2
- Level: component
- Setup: Profile fixtures containing sourced claims, explicit assumptions, and an unsupported unsourced material claim.
- Action: Run Project Memory validation on each fixture.
- Expected: Sourced claims and declared assumptions pass their profile rules; the unsupported material claim produces an actionable validation failure.

### T-04 — Round-trip one bundle through both agent invocation forms

- Covers: AC-02.1
- Level: end-to-end
- Setup: One shared installed skill fixture with Codex-style and Cursor-style command routing and a temporary repository.
- Action: Initialize through the Codex form, refresh through the Cursor form, verify through the standalone CLI, then repeat with the invocation forms reversed.
- Expected: Both directions use the same scripts and assets, require no migration, and produce equivalent committed artifact structures and validation results.

### T-05 — Run the portable core across supported systems

- Covers: AC-02.2
- Level: integration
- Setup: CI jobs for Windows, macOS, and Linux using the supported Python versions and portable repository fixtures.
- Action: Run scaffolding, status, verification, reconciliation, and the complete test suite.
- Expected: Commands and fixtures behave equivalently with no model-provider SDK, shell-specific path, or platform-only dependency.

### T-06 — Consume agent-neutral OKF artifacts

- Covers: AC-02.3, AC-02.4
- Level: component
- Setup: Generated bundle with standard Markdown links, OKF trust metadata, portable paths, and an unknown extension field.
- Action: Parse and validate the bundle with the standalone CLI and inspect all required profile fields.
- Expected: No required field names Codex or Cursor, links are navigable without the skill, trust tiers can be derived, paths use portable notation, and the unknown field survives any supported round trip.

### T-07 — Record durable outcomes from every source tier

- Covers: AC-03.1
- Level: component
- Setup: Change fixtures for TinySpec, LiteSpec, official Spec Kit, a promoted feature, and a repository-only change, each with code and test evidence.
- Action: Apply the documented materiality and provenance mapping to each proposed update.
- Expected: Each proposal cites its governing artifacts and implementation evidence, promotion retains its provenance chain, the implementation-governing tier is primary, no full specification is copied, and Spec Kit-owned files remain unchanged.

### T-08 — Identify memory affected by later commits

- Covers: AC-03.2
- Level: integration
- Setup: Git repository with reconciled memory followed by material, immaterial, renamed, and deleted evidence changes.
- Action: Run status and the read-only refresh inspection contract from the recorded commit to `HEAD`.
- Expected: Commit range and potentially affected concepts are reported; renamed or deleted evidence is surfaced; no factual conclusion or repository mutation occurs during inspection.

### T-10 — Apply an approved patch or reviewed no-op

- Covers: AC-03.4, AC-03.5
- Level: end-to-end
- Setup: Two temporary repositories with potentially stale memory: one requiring a material patch and one containing only an immaterial code change.
- Action: Apply an approved evidence-backed patch in the first; approve a no-op refresh in the second; validate and reconcile both.
- Expected: The first updates concepts and `log.md`; both advance state to the approved `HEAD` only after successful validation and finish with current status.

### T-11 — Report usable trust and freshness states

- Covers: AC-04.1
- Level: integration
- Setup: Valid/current, valid/potentially-stale, and malformed/broken memory fixtures.
- Action: Run verification and status.
- Expected: Results are distinctly reported as pass, warning, and failure with stable exit behavior suitable for local use and future CI integration.

### T-14 — Verify memory before using it in orientation

- Covers: AC-04.4
- Level: component
- Setup: Orientation fixtures containing a relevant verified claim, an irrelevant concept, and a relevant claim contradicted by current code.
- Action: Run the shared skill's documented orientation routing and evidence checks.
- Expected: Only relevant memory is selected; the supported claim is usable context; the contradiction is reported and not repeated as specification fact.

## Failure and recovery cases

### T-03 — Reject initialization and refuse overwrite

- Covers: AC-01.3
- Level: integration
- Setup: Hash the contents and Git status of one repository before a rejected proposal and another repository with an existing memory bundle.
- Action: Reject the first proposal and attempt to scaffold the second.
- Expected: Both repositories retain their original hashes and reconciliation state; overwrite refusal returns an actionable error.

### T-09 — Preserve state before approval or after failure

- Covers: AC-03.3
- Level: integration
- Setup: Repository with a recorded reconciliation commit, an unapproved proposed patch, and a second approved patch that fails validation.
- Action: Attempt reconciliation before approval and after the failing patch.
- Expected: Neither attempt advances state or modifies the last accepted memory; diagnostics identify the missing approval or validation failure.

### T-12 — Detect malformed and broken memory

- Covers: AC-04.2
- Level: unit
- Setup: Parameterized fixtures with unsupported profile versions, invalid timestamps/status/trust metadata, missing required concepts, broken required evidence, missing specification paths, invalid Git commits, broken optional links, and unknown preserved fields.
- Action: Run verification for each fixture.
- Expected: Material defects fail with field/path-specific diagnostics, broken optional links warn distinctly, and preserved unknown fields do not cause rejection.

### T-13 — Handle drift and unavailable Git honestly

- Covers: AC-04.3
- Level: integration
- Setup: A current repository, a repository several commits past reconciliation, a shallow clone missing the recorded commit, and a non-Git directory.
- Action: Run status and verification.
- Expected: Current memory passes, ordinary drift warns without asserting factual error, and shallow or unavailable history reports limited confidence rather than inventing lineage.

## Automated checks

```text
python -m unittest discover -s plugins/adaptive-sdd/tests
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/validate_litespec.py .litespec/project-memory --approved
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/project_memory.py verify --project <fixture>
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/project_memory.py status --project <fixture>
```

The CI matrix will run the applicable standard-library suite on Windows, macOS, and Linux. Existing TinySpec, LiteSpec, manifest, and example checks remain regression requirements.

## Manual exceptions

None. Qualitative dogfooding observations supplement but do not replace automated acceptance evidence.

## Test data and setup

- Temporary repositories with explicit user identity, deterministic commits, renames, deletions, shallow-history simulation, and clean teardown.
- Non-Git directories for graceful-degradation coverage.
- OKF/profile fixtures for current, stale, malformed, extended, generated-only, machine-confirmed, and human-reviewed concepts.
- TinySpec, LiteSpec, Spec Kit, promoted-feature, and repository-only provenance fixtures.
- Shared installed-skill fixture with both documented invocation forms resolving to the same resources.
- Paths containing spaces and platform separators to expose portability defects.
- No network, external account, model-provider SDK, or live Codex/Cursor session is required for deterministic tests.

## Completion criteria

- [x] Every current-release acceptance criterion maps to passing automated evidence.
- [x] Critical initialization, cross-agent round-trip, refresh, approval, and orientation flows pass their local and contract checks.
- [x] Rejection, overwrite, malformed data, broken evidence, Git drift, and non-Git recovery cases pass; shallow history uses the same limited-confidence path.
- [x] The supported OS/Python matrix passes with portable artifact output.
- [x] Existing TinySpec, LiteSpec, Spec Kit adapter, manifest, installer, and example tests pass.
- [x] The complete LiteSpec package validates with `--approved`.
- [x] No unresolved local failure blocks an approved story or non-functional requirement.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-08-22 | Initial draft | Derived from approved specification 0.1 and plan 0.1 | All |
