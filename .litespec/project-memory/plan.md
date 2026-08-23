---
feature: project-memory
artifact: plan
status: implementing
owner: user
version: 0.1
created: 2026-08-22
updated: 2026-08-22
spec_version: 0.1
---

# Implementation Plan: Project Memory

## Technical approach

Implement Project Memory inside the existing `adaptive-sdd` skill rather than adding another public skill. A pinned OKF v0.2 profile, Markdown assets, one reference guide, and a standard-library Python CLI will form the portable core. Codex and Cursor will invoke the same skill and scripts; their manifests remain discovery adapters only.

Separate deterministic mechanics from knowledge judgment. The CLI will scaffold, inspect Git state, validate artifacts, and record an approved reconciliation point. The shared skill will inspect code and specifications read-only, propose human-readable content or patches in conversation, and write them only after explicit approval. This keeps rejected proposals from mutating the repository while avoiding model or provider dependencies in the stored format and validator.

## Key decisions

### KD-01 — Use an Adaptive SDD profile of OKF v0.2

- **Choice:** Store the living document as an OKF v0.2 bundle in `.sdd/memory/` and version Adaptive SDD extensions independently.
- **Rationale:** OKF supplies portable concepts, sources, trust, lifecycle, indexes, and logs without prescribing the repository workflow that Adaptive SDD must add.
- **Alternatives considered:** A proprietary Markdown schema or a service-backed memory database.
- **Consequences:** The implementation must pin and validate the supported OKF version, preserve unknown fields, and provide an explicit future migration path.

### KD-02 — Keep one public Adaptive SDD skill

- **Choice:** Add Project Memory operations, references, assets, and scripts to `adaptive-sdd`; do not add a public memory skill in the MVP.
- **Rationale:** One orchestrator avoids overlapping invocation choices and already has portable Codex and Cursor discovery paths.
- **Alternatives considered:** Separate Codex and Cursor skills or an independent `project-memory` skill.
- **Consequences:** `SKILL.md` must route memory requests clearly, and a future standalone skill must reuse the same core rather than fork it.

### KD-03 — Propose knowledge before repository writes

- **Choice:** Agents inspect and present proposed memory content or patches before calling deterministic write/state operations after approval.
- **Rationale:** Knowledge synthesis is judgment-heavy, while repository mutation and validation should remain explicit and testable.
- **Alternatives considered:** Automatically regenerate memory on every commit or maintain proposal files inside the target repository.
- **Consequences:** The workflow requires an approval turn, but rejected proposals leave repository files and reconciliation state unchanged.

### KD-04 — Treat commit drift as a freshness signal

- **Choice:** Record a last reconciled commit outside the OKF bundle and report later commits as potential staleness rather than proof of incorrect content.
- **Rationale:** Many commits do not change durable repository knowledge, and a living document should not create noisy mandatory edits.
- **Alternatives considered:** Fail validation after every commit or use timestamps alone.
- **Consequences:** A reviewed no-op refresh may advance reconciliation state, while missing or shallow Git history produces limited-confidence output.

### KD-05 — Use a dependency-free generated frontmatter subset

- **Choice:** Generate OKF frontmatter using top-level scalars and JSON-compatible inline values, which are valid YAML and can be parsed with the Python standard library; tolerate preserved unknown fields that the tool does not rewrite.
- **Rationale:** Installed project skills currently run without dependency installation, and adding a YAML package would weaken portability.
- **Alternatives considered:** Require PyYAML or implement a complete YAML parser.
- **Consequences:** The Project Memory profile documents its emitted subset. Validation is strict for profile-owned fields and graceful for valid extensions outside that subset.

## Impacted areas

| Area | Expected change | Related IDs |
|---|---|---|
| `plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md` | Route initialization, status, update, refresh, verification, orientation, and completion behavior | US-01, US-03, AC-04.4 |
| `plugins/adaptive-sdd/skills/adaptive-sdd/references/project-memory.md` | Define OKF profile, evidence, trust, tier provenance, approvals, and reconciliation rules | US-02, US-03, US-04 |
| `plugins/adaptive-sdd/skills/adaptive-sdd/assets/memory/` | Provide minimal OKF index, project, architecture, log, and state templates | AC-01.1, AC-02.3 |
| `plugins/adaptive-sdd/skills/adaptive-sdd/scripts/project_memory.py` | Provide scaffold, status, verify, and approved reconciliation-state mechanics | US-01, US-04 |
| `plugins/adaptive-sdd/tests/test_adaptive_sdd.py` | Cover scaffolding, safety, validation, Git drift, tier provenance, and compatibility | AC-01.1 through AC-04.4 |
| `plugins/adaptive-sdd/examples/simple-kanban/` | Demonstrate a portable living memory and an update after a specified change | US-01, US-02, US-03 |
| `plugins/adaptive-sdd/docs/` and plugin README | Document concepts, commands, agent-neutral use, tier integration, and limitations | AC-02.4, AC-04.1 |

## Technical detail

### Repository data model

```text
.sdd/
├── memory/
│   ├── index.md          # OKF bundle index and version
│   ├── project.md        # Software Repository concept
│   ├── architecture.md   # Software Architecture concept
│   └── log.md            # OKF chronological update log
└── memory-state.json     # Adaptive SDD reconciliation state
```

Initial state shape:

```json
{
  "schema_version": 1,
  "okf_version": "0.2",
  "profile_version": 1,
  "last_reconciled_commit": null,
  "last_reconciled_at": null
}
```

### Portable CLI boundary

```text
project_memory.py scaffold --project <root>
project_memory.py status --project <root>
project_memory.py verify --project <root>
project_memory.py reconcile --project <root> --commit COMMIT_SHA
```

`scaffold` creates only approved baseline files and refuses an existing `.sdd/memory/`. `status` and `verify` are read-only. `reconcile` changes only the state file after the agent has applied an approved memory patch and validation succeeds. Agent-facing phrases such as `initialize memory` and `refresh memory` remain semantic operations in the shared skill, not separate provider APIs.

### Lifecycle

```text
absent → proposed → approved/current → potentially stale → proposed patch
   └──────── rejected/no change ◄──────────────────────────────┘
                                      approved + verified → current
```

The `proposed` state exists in the interaction, not as an unapproved repository artifact. OKF `generated`, `verified`, `status`, and `sources` describe concept trust and provenance; `memory-state.json` records only tool/profile versions and reconciliation state.

## Risks and mitigations

| Risk | Impact | Mitigation | Evidence or trigger |
|---|---|---|---|
| Generated prose invents intent or overstates architecture | Future work is grounded in false knowledge | Require repository sources, distinguish assumptions, require approval, and recheck consequential claims during orientation | Claim lacks a resolvable source or conflicts with inspected code |
| Memory becomes noisy or duplicates specifications | Contributors stop maintaining or reading it | Capture only durable current state and link to authoritative detail | Refresh repeatedly copies requirements, tasks, or test matrices |
| Codex and Cursor behavior diverges | Repository knowledge becomes tool-dependent | Use one skill and CLI; add cross-agent artifact compatibility tests | Equivalent operations produce different committed structures |
| OKF changes after v0.2 | Existing bundles or validators drift | Pin OKF and profile versions; document migration boundaries | Bundle declares an unsupported version |
| Dependency-free YAML handling rejects valid external syntax | Interoperability is narrower than OKF | Constrain only Adaptive SDD-emitted syntax, preserve unknown content, and report unsupported validation depth without rewriting | External concept uses nested syntax outside the profile subset |
| Large memory consumes agent context | Orientation becomes slower and less focused | Use `index.md`, minimal initial concepts, and relevant-concept loading | Agents load every concept for unrelated work |

## Implementation phases

### Phase 1 — Portable profile and artifacts

- [x] **P1-T1 — Define the Project Memory profile**
  - Covers: AC-01.2, AC-02.3, AC-02.4, AC-04.4
  - Depends on: None
  - Work: Add the OKF/profile reference covering concept types, portable paths, source evidence, generated and verified trust, SDD tier provenance, promotion, unknown-field preservation, and relevant-memory orientation.
  - Verify: Reference examples are valid under the documented profile and contain no required provider-specific fields.

- [x] **P1-T2 — Add minimal memory assets**
  - Covers: AC-01.1, AC-01.2, AC-01.4
  - Depends on: P1-T1
  - Work: Add templates for the bundle index, project concept, architecture concept, update log, and separate state file with pinned format/profile versions.
  - Verify: Rendering the assets produces the exact MVP structure with valid OKF metadata and repository-relative evidence placeholders.

### Phase 2 — Deterministic portable core

- [x] **P2-T1 — Implement safe scaffolding and status**
  - Covers: AC-01.1, AC-01.3, AC-01.4, AC-03.2, AC-04.3
  - Depends on: P1-T2
  - Work: Implement standard-library CLI commands that scaffold only after approval, refuse overwrite, record Git state when available, and report commit drift or unavailable history without declaring memory incorrect.
  - Verify: Temporary Git and non-Git repositories demonstrate successful initialization, overwrite refusal, unchanged rejection path, current status, drift warning, and limited-confidence status.

- [x] **P2-T2 — Implement validation and approved reconciliation**
  - Covers: AC-03.3, AC-03.4, AC-03.5, AC-04.1, AC-04.2, AC-04.3
  - Depends on: P2-T1
  - Work: Validate required OKF/profile metadata, concepts, evidence, links, spec paths, Git commits, and state; update the reconciliation point only after an approved patch or reviewed no-op passes validation.
  - Verify: Deterministic fixtures produce distinct pass, warning, and failure results, and failed validation never advances state.

### Phase 3 — Shared agent workflow and SDD provenance

- [x] **P3-T1 — Integrate memory commands and orientation into the shared skill**
  - Covers: AC-02.1, AC-02.4, AC-04.4
  - Depends on: P2-T2
  - Work: Add `initialize memory`, `status memory`, `update memory`, `refresh memory`, and `verify memory` routing plus progressive, evidence-checking memory reads during normal Adaptive SDD orientation.
  - Verify: Codex-style and Cursor-style invocations resolve to the same documented workflow, scripts, assets, and stored semantics.

- [x] **P3-T2 — Implement approval-gated update and refresh behavior**
  - Covers: AC-03.1, AC-03.2, AC-03.3, AC-03.4, AC-03.5
  - Depends on: P3-T1
  - Work: Define read-only change inspection, materiality assessment, conversational patch review, accepted patch application, logging, validation, rejected update behavior, and reviewed no-op reconciliation.
  - Verify: A material change produces an evidence-backed patch; an immaterial change produces a reviewable no-op; rejection and failure leave files and state unchanged.

- [x] **P3-T3 — Integrate every specification tier**
  - Covers: AC-03.1
  - Depends on: P3-T2
  - Work: Add provenance rules for TinySpec, LiteSpec, official Spec Kit, promoted features, and repository-only changes while preserving source artifacts and upstream ownership.
  - Verify: Fixtures for each source type resolve to the correct primary source and provenance chain without copying complete specifications or modifying Spec Kit-owned files.

### Phase 4 — Compatibility evidence and dogfooding

- [ ] **P4-T1 — Add cross-platform and cross-agent tests**
  - Covers: AC-02.1, AC-02.2, AC-02.3
  - Depends on: P3-T3
  - Work: Extend deterministic tests and CI coverage for portable paths, Python 3.11+, equivalent shared operations, round trips between agent invocation forms, overwrite safety, and preservation of unknown extensions.
  - Verify: The same memory fixture initializes under one invocation form, refreshes under the other, and validates identically on the supported OS matrix.

- [x] **P4-T2 — Dogfood and document the lifecycle**
  - Covers: AC-01.1, AC-01.2, AC-02.4, AC-03.4, AC-04.1, AC-04.4
  - Depends on: P4-T1
  - Work: Add a Simple Kanban memory example, initialize an evidence-backed memory for Adaptive SDD itself, exercise one approved update, and document installation-neutral use, tiers, trust, staleness, limitations, and recovery.
  - Verify: Both example bundles validate, the Adaptive SDD memory helps orient a subsequent change, and documentation contains no claim that installation silently creates memory.

## Release and rollback considerations

- **Release:** Ship Project Memory as an opt-in capability of the existing plugin. Run the complete test suite, validate the dogfood and Kanban bundles, confirm both manifests still resolve the same shared skill, and document the pinned OKF/profile versions.
- **Rollback:** Because installation does not create memory automatically, the capability can be removed from a later plugin release without altering target repositories. Existing `.sdd/memory/` bundles remain readable OKF Markdown; users may retain them and run the version of the validator that supports their declared profile.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-08-22 | Initial draft | Derived from approved specification 0.1 | All |
