---
type: Software Architecture
title: "Adaptive SDD architecture"
description: "Current plugin layout and responsibility boundaries."
status: draft
generated: {"by":"adaptive-sdd/0.3.0","at":"2026-08-22T12:00:00Z"}
sources: [{"id":"skill","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md","title":"Shared orchestrator"},{"id":"tests","resource":"../../plugins/adaptive-sdd/tests/test_adaptive_sdd.py","title":"Deterministic test suite"},{"id":"installer","resource":"../../plugins/adaptive-sdd/scripts/install-project.ps1","title":"Project installer"},{"id":"cursor-manifest","resource":"../../plugins/adaptive-sdd/plugin.json","title":"Agent Plugin manifest"},{"id":"codex-manifest","resource":"../../plugins/adaptive-sdd/.codex-plugin/plugin.json","title":"Codex plugin manifest"}]
sdd: {"profile_version":1,"assumptions":["Initial dogfood content awaits repository-owner review."]}
---

# Architecture

## Components

- `skills/adaptive-sdd/SKILL.md` is the shared public orchestrator.
- `assets/`, `references/`, and `scripts/` provide shared templates, method rules, and deterministic mechanics.
- The root Agent Plugin manifest and `.codex-plugin/plugin.json` adapt discovery without forking behavior.
- `scripts/install-project.ps1` copies the shared skill into a target repository.
- `tests/` validates manifests, artifact gates, and Project Memory behavior.

## Relationships and flows

- Natural requests enter through the shared skill, which selects a specification tier or a Project Memory operation.
- TinySpec and LiteSpec are owned by Adaptive SDD; full Spec Kit is delegated to official upstream-installed workflows.
- Project Memory remains orthogonal to tier selection and records only durable implemented state with provenance.

## Constraints and invariants

- Artifact creation, tier promotion, implementation, and generated memory writes require explicit approval.
- Codex and Cursor use the same installed skill, assets, references, and Python scripts.
- Target repository knowledge stays in portable files rather than provider-specific storage.
