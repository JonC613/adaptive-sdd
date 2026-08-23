---
feature: project-memory
artifact: spec
status: implementing
owner: user
version: 0.1
created: 2026-08-22
updated: 2026-08-22
---

# Specification: Project Memory

## Summary

Add a repository-owned, living memory that describes the codebase as it exists today and evolves with material repository changes. Point-in-time TinySpec, LiteSpec, and Spec Kit artifacts continue to explain individual changes; Project Memory carries their durable outcomes forward for people and agents throughout the repository lifecycle.

## Problem

Adaptive SDD preserves the intent, plan, and evidence for individual changes, but a new contributor or agent must still reconstruct the repository's current purpose and architecture from code, historical specifications, and scattered documentation. Those sources can become difficult to navigate as the repository evolves, and a summary without evidence or reconciliation state can silently become inaccurate.

## Desired outcome

A repository can contain a concise, human-readable and agent-readable knowledge bundle that explains its current purpose and architecture, cites code and specifications as evidence, reports when it may be stale, and can be initialized, updated, refreshed, and verified through the same portable workflow in Codex and Cursor.

## Boundaries

### Goals

- Maintain a concise current-state description of the repository in version control.
- Use Open Knowledge Format (OKF) v0.2 as the portable knowledge envelope.
- Provide deterministic, cross-platform operations for scaffolding, status, and validation.
- Integrate durable outcomes from TinySpec, LiteSpec, full Spec Kit, and ordinary Git changes.
- Preserve human control over generated knowledge through review before writes.

### Non-goals

- Replace source code, tests, specifications, API schemas, or existing authoritative documentation.
- Store conversation history, personal preferences, secrets, or model-specific memory.
- Automatically rewrite memory on every commit.
- Provide vector search, embeddings, a remote knowledge service, or cross-repository memory.
- Generate architecture diagrams, enforce memory freshness in CI, or install Git hooks in the first release.
- Modify official Spec Kit-owned `.specify/`, `specs/`, or installed `speckit-*` workflows.

### Constraints

- The same committed memory bundle must work without conversion in Codex, Cursor, and ordinary text or Git tooling.
- Core behavior must not depend on MCP, proprietary agent APIs, or vendor-specific conversation storage.
- Generated claims must remain distinguishable from human-reviewed claims.
- Existing TinySpec, LiteSpec, Spec Kit adapter, installer, and validation behavior must remain compatible.

## Requirements

### Current release

- **R-01:** Store Project Memory as an OKF v0.2-compatible bundle under `.sdd/memory/`, with Adaptive SDD operational state stored separately under `.sdd/`.
- **R-02:** Provide a portable initialization operation that inspects a repository and proposes a minimal project overview and architecture description with evidence.
- **R-03:** Provide a status operation that reports the last reconciled Git commit, current `HEAD`, and whether reconciliation may be required without claiming that commit drift alone makes the memory incorrect.
- **R-04:** Provide an update operation that proposes durable current-state changes after approved SDD implementation work and links them to the governing specification, code, tests, and commits.
- **R-05:** Provide a refresh operation that examines changes since the last reconciliation point and proposes additions, corrections, or deprecations for work completed outside Adaptive SDD.
- **R-06:** Require explicit review before generated repository knowledge is written or marked human-reviewed.
- **R-07:** Provide deterministic validation of the OKF structure, Adaptive SDD profile, evidence paths, specification references, Git references, internal links, and reconciliation state.
- **R-08:** Treat TinySpec, LiteSpec, full Spec Kit, and repository-only changes as valid provenance sources without copying their complete artifacts into memory.
- **R-09:** Preserve the provenance chain when a feature is promoted between SDD tiers and use the tier that governed implementation as its primary specification source.
- **R-10:** Read relevant, verified Project Memory during Adaptive SDD repository orientation while checking consequential claims against current repository evidence.
- **R-11:** Use one shared skill, templates, profile, and script implementation for Codex and Cursor; agent-specific manifests may provide discovery but must not change memory semantics.
- **R-12:** Keep memory useful without an installed agent: a person or generic agent must be able to navigate it as standard Markdown, follow its evidence links, and run deterministic validation separately.

### Deferred

- **D-01:** Optional warning or enforcement policies for CI.
- **D-02:** Optional Git hooks or scheduled reconciliation.
- **D-03:** Component-level concept directories, dedicated decision records, operational playbooks, known-issue concepts, and richer change concepts.
- **D-04:** Search indexes, embeddings, graph visualization, and remote knowledge serving.
- **D-05:** Cross-repository memory aggregation and synchronization.
- **D-06:** Automated architecture diagram generation.

## User stories

### US-01 — Establish repository memory

**Story:** As a repository maintainer, I want to initialize a living description from an existing codebase, so that contributors and agents have a reviewed starting point for understanding it.

**Rationale:** A useful lifecycle memory needs an evidence-backed baseline before it can track later changes.

**Acceptance criteria:**

- **AC-01.1:** Given a repository without Project Memory, initialization proposes `.sdd/memory/index.md`, `project.md`, `architecture.md`, `log.md`, and separate reconciliation state without overwriting existing content.
- **AC-01.2:** Every material generated claim identifies repository evidence or is explicitly marked as an assumption requiring review.
- **AC-01.3:** Rejecting the proposal leaves the target repository unchanged.
- **AC-01.4:** Approving the proposal records its generation and verification metadata and the current Git commit when Git is available.

**Edge cases:**

- Existing authoritative documentation is linked rather than unnecessarily duplicated.
- A non-Git directory can retain readable memory, while Git-based reconciliation reports itself unavailable.
- Partial or conflicting evidence is surfaced for review instead of resolved by invention.

### US-02 — Consume memory across tools

**Story:** As a contributor using Codex, Cursor, or ordinary repository tools, I want the same memory to remain readable and actionable, so that project knowledge is not locked to one agent.

**Rationale:** Repository memory should outlive individual tools, models, and installations.

**Acceptance criteria:**

- **AC-02.1:** A memory bundle created through the Codex workflow can be read, refreshed, and verified through the Cursor workflow without migration, and the reverse is also true.
- **AC-02.2:** Core deterministic commands produce equivalent artifacts and validation results on supported Windows, macOS, and Linux environments.
- **AC-02.3:** Memory artifacts contain no required Codex- or Cursor-specific fields and use portable repository-relative paths.
- **AC-02.4:** A reader without Adaptive SDD can navigate the bundle using standard Markdown links and distinguish generated, machine-verified, and human-reviewed content from OKF metadata.

**Edge cases:**

- Optional capabilities unavailable in one agent degrade without changing the stored format.
- Unknown OKF extensions remain preserved rather than causing destructive rewrites.

### US-03 — Keep memory aligned with repository changes

**Story:** As a repository maintainer, I want material code changes to produce reviewable memory updates, so that the current description evolves without becoming an untrusted automatic narrative.

**Rationale:** A living document is valuable only if its update loop is practical, traceable, and resistant to silent drift.

**Acceptance criteria:**

- **AC-03.1:** After approved SDD implementation, the update workflow proposes only durable changes to current repository knowledge and cites the governing artifacts and implementation evidence.
- **AC-03.2:** Refresh compares the recorded reconciliation point with current Git history and identifies potentially affected memory concepts for review.
- **AC-03.3:** No proposed update changes files or advances reconciliation state before approval.
- **AC-03.4:** After approval, the workflow applies the accepted patch, records a log entry, updates reconciliation state, and validates the result.
- **AC-03.5:** When no material repository knowledge changed, refresh can complete as a reviewed no-op while advancing reconciliation state.

**Edge cases:**

- Planned but unimplemented behavior is not represented as a current capability.
- Deleted or renamed evidence is reported rather than silently discarded.
- A rejected or failed update preserves the previous reconciliation point.

### US-04 — Trust and verify repository knowledge

**Story:** As a memory consumer, I want to see where claims came from and whether the bundle is current, so that I can judge what to trust before acting on it.

**Rationale:** Generated documentation without provenance, trust signals, or freshness information can mislead future work.

**Acceptance criteria:**

- **AC-04.1:** Validation distinguishes valid and reconciled memory, valid but potentially stale memory, and malformed or materially broken memory.
- **AC-04.2:** Validation detects unsupported profile versions, invalid metadata, missing required concepts, broken required evidence, invalid specification references, and invalid Git commits.
- **AC-04.3:** Commit drift produces a staleness warning rather than an assertion that memory is factually wrong.
- **AC-04.4:** Adaptive SDD treats memory as contextual evidence and verifies consequential claims against the codebase before using them in a new specification.

**Edge cases:**

- Unavailable Git history or shallow clones produce an explicit limited-confidence result.
- Broken optional knowledge links remain distinguishable from broken required evidence.

## Non-functional requirements

- **NFR-01 — Portability:** Core deterministic scripts must support Python 3.11 or newer on Windows, macOS, and Linux without requiring a model-provider SDK.
- **NFR-02 — Interoperability:** Project Memory concepts must conform to pinned OKF v0.2 rules, while Adaptive SDD extensions use a separately versioned profile and preserve unknown fields.
- **NFR-03 — Safety:** Scaffolding must refuse to overwrite an existing bundle, and rejected or failed proposals must not mutate memory or reconciliation state.
- **NFR-04 — Auditability:** Every accepted generated update must be visible as ordinary version-controlled file changes and identify its producer, time, sources, and verification state.
- **NFR-05 — Maintainability:** Codex and Cursor must share one implementation; platform adapters may not fork core behavior.
- **NFR-06 — Context efficiency:** The root index must support progressive disclosure so an agent can identify relevant concepts without loading the entire bundle.

## Codebase context

Adaptive SDD is distributed as one shared skill under `plugins/adaptive-sdd/skills/adaptive-sdd/`, with Markdown assets and references plus portable Python scaffold and validation scripts. The project installer copies that shared skill into `.agents/skills/adaptive-sdd`, which the existing documentation identifies as discoverable by Codex and Cursor. Cursor uses the root Agent Plugin manifest, while Codex uses `.codex-plugin/plugin.json`; these provide suitable discovery adapters around a shared implementation.

TinySpec and LiteSpec already use repository-owned Markdown artifacts, explicit lifecycle gates, stable identifiers, and deterministic Python validators. The Spec Kit adapter deliberately leaves `.specify/`, `specs/`, and installed upstream skills under official Spec Kit ownership. Project Memory must extend the shared Adaptive SDD orientation and completion workflow without changing those ownership boundaries or automatically creating memory during project installation.

## Assumptions and open questions

### Assumptions

- **A-01:** Human-readable repository documentation is the primary product; agent consumption is an equally supported use rather than a reason to introduce proprietary storage.
- **A-02:** OKF v0.2 is pinned for the first release, and future OKF compatibility can evolve independently from the Adaptive SDD Project Memory profile.
- **A-03:** Explicit initialization and refresh commands are sufficient for the MVP; continuous hooks and CI enforcement remain deferred.
- **A-04:** Git is the normal reconciliation mechanism, but basic reading, initialization, and validation remain useful when Git metadata is unavailable.
- **A-05:** The MVP starts with a single project overview and architecture concept; finer-grained concepts are added only after dogfooding demonstrates a need.

### Open questions

- None.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | 2026-08-22 | Initial draft | Consolidated approved discovery for portable Project Memory | All |
