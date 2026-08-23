---
type: Software Architecture
title: "Simple Kanban example architecture"
description: "Artifact layout and provenance relationships in the Simple Kanban example."
status: stable
generated: {"by":"adaptive-sdd/0.3.0","at":"2026-08-22T12:00:00Z"}
verified: [{"by":"process:adaptive-sdd-tests","at":"2026-08-22T12:00:00Z"}]
sources: [{"id":"readme","resource":"../../README.md","title":"Example README"},{"id":"lite-plan","resource":"../../lite/simple-kanban/plan.md","title":"LiteSpec plan"},{"id":"lite-tests","resource":"../../lite/simple-kanban/tests.md","title":"LiteSpec tests"}]
sdd: {"profile_version":1,"assumptions":[]}
---

# Architecture

## Components

- `tiny/` contains the single-file representation.
- `lite/simple-kanban/` contains the three approval-gated LiteSpec artifacts.

## Relationships and flows

- Both tiers describe the same feature at different depths.
- Project Memory summarizes the durable example layout and links to the point-in-time artifacts for detail.

## Constraints and invariants

- Source specifications remain unchanged when referenced by memory.
