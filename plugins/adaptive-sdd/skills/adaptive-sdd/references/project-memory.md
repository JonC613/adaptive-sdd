# Project Memory profile

Project Memory is the repository-lifecycle layer shared by TinySpec, LiteSpec, and official Spec Kit. Specifications remain point-in-time records. Memory describes the durable current state that implemented changes leave behind.

## Portable bundle

Store the first profile version as:

```text
.sdd/
├── memory/
│   ├── index.md
│   ├── project.md
│   ├── architecture.md
│   └── log.md
└── memory-state.json
```

`.sdd/memory/` is an Open Knowledge Format (OKF) v0.2 bundle. `memory-state.json` is Adaptive SDD operational state and is not part of the OKF bundle. Use standard Markdown links and forward slashes in stored paths.

Project Memory must remain useful without Codex or Cursor. Do not store conversation history, model-specific state, secrets, or required provider-specific fields.

## Concept profile

Use these initial concept types:

- `Software Repository` for `project.md`.
- `Software Architecture` for `architecture.md`.

Every concept requires `type`, `title`, `description`, `status`, `generated`, and `sdd`. Use OKF `sources` for material claims and `verified` only after the named actor actually reviewed the current content.

Adaptive SDD emits top-level scalars and JSON-compatible inline maps or lists in YAML frontmatter. JSON values are valid YAML and keep deterministic parsing dependency-free. Preserve unknown fields when content is not being replaced.

```yaml
---
type: Software Repository
title: Example
description: Current overview of the Example repository.
status: stable
generated: {"by":"adaptive-sdd/0.4.0","at":"2026-08-22T18:00:00Z"}
verified: [{"by":"human:owner","at":"2026-08-22T18:05:00Z"}]
sources: [{"id":"readme","resource":"../../README.md","title":"Repository README"}]
sdd: {"profile_version":1,"assumptions":[]}
---
```

Use `draft`, `stable`, or `deprecated` for OKF status. A draft or an entry in `sdd.assumptions` must make uncertainty visible. Never turn agent generation into `human:` verification without explicit approval.

## Evidence and trust

Treat code, tests, configuration, approved specifications, and Git commits as evidence. Link existing authoritative documentation rather than copying it. An unavailable or conflicting source is a review item, not permission to invent an answer.

- `generated.by` identifies the producer, normally `adaptive-sdd/<version>`.
- `verified` records actual review events. Human verification uses `human:<id>`.
- `sources[].resource` points to a URL, a bundle concept, or a repository-relative artifact.
- Commit drift is a freshness signal. It does not prove that a concept is false.

## Specification provenance

Capture only implemented, durable repository state. Do not copy requirement lists, task lists, or test matrices into memory.

- TinySpec: link `.tinyspec/<feature>.md`, its version, implementation, tests, and commits.
- LiteSpec: link its `spec.md`, `plan.md`, and `tests.md` versions plus implementation evidence.
- Spec Kit: link the native `specs/<feature>/` package read-only. Never modify `.specify/`, `specs/`, or installed `speckit-*` resources through memory maintenance.
- Repository-only work: cite Git, code, and tests and record `tier: none`.

For promotion, preserve the earlier artifacts as `promoted_from` provenance and use the tier that governed implementation as the primary source. One implemented capability has one current memory representation, not one copy per tier.

## Operations

### Initialize

1. Inspect the repository and existing documentation read-only.
2. Draft the smallest useful `project.md` and `architecture.md` content.
3. Cite sources or mark assumptions.
4. Proceed under the initialization request; ask only about consequential unresolved choices.
5. Scaffold and write the content, verify once, and record the inspected Git commit without claiming human review.

A proposal-only request leaves the repository unchanged. Refuse to overwrite existing memory.

### Status and verify

Run the portable script. Report `PASS`, `WARN`, or `FAIL`. Drift, shallow history, unavailable Git, and broken optional links warn. Malformed required metadata, required evidence, state, or declared Git references fail.

Freshness includes staged, unstaged, and relevant untracked paths. Specification
changes are review signals too. Only `.sdd/memory/` and `.sdd/memory-state.json`
are excluded by default to avoid self-generated drift. Optional `.sdd/config.json`
may contain `"memory_exclude": ["build/"]`; a trailing slash means a directory
prefix, otherwise an entry is an exact repository-relative path. Exclusions reduce
coverage and must be chosen deliberately. Drift never proves factual error.

### Update after SDD work

Before marking implemented specifications done, assess whether the work changed repository purpose, capabilities, component boundaries, flows, public contracts, durable decisions, or constraints. Update affected existing concepts and provenance within the implementation request, add a log entry, verify the batch once, and reconcile the inspected commit. No separate approval is needed; do not claim human verification.

### Refresh external work

Compare `last_reconciled_commit` with `HEAD`, inspect the changed code and evidence, and apply supported corrections or record a no-op under the refresh request. Reconcile after relevant validation. Ask only about consequential unresolved contradictions. Inspection-only requests remain read-only.

## Orientation

Read `index.md` first and load only concepts relevant to the requested change. Treat memory as contextual evidence, not authority. Verify consequential claims against current code before using them in tier selection or specifications. Report contradictions instead of repeating them.
