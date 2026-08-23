---
type: Software Repository
title: "Adaptive SDD"
description: "Portable, approval-gated specification workflows and living repository memory."
status: draft
generated: {"by":"adaptive-sdd/0.3.0","at":"2026-08-22T12:00:00Z"}
sources: [{"id":"marketplace-readme","resource":"../../README.md","title":"Marketplace README"},{"id":"plugin-readme","resource":"../../plugins/adaptive-sdd/README.md","title":"Adaptive SDD README"},{"id":"skill","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md","title":"Shared Adaptive SDD skill"}]
sdd: {"profile_version":1,"assumptions":["Initial dogfood content awaits repository-owner review."]}
---

# Adaptive SDD

## Purpose

Help repositories use the least specification ceremony that still makes behavior, implementation risk, and verification clear, while maintaining an optional portable description of the codebase over its lifecycle.

## Current capabilities

- Guides TinySpec, LiteSpec, and official GitHub Spec Kit through explicit approval gates.
- Installs one shared skill for Codex and Cursor discovery.
- Scaffolds and validates TinySpec and LiteSpec artifacts deterministically.
- Provides OKF-compatible Project Memory scaffolding, status, validation, and reconciliation mechanics.

## Boundaries

- Official Spec Kit remains upstream-owned.
- Installing Adaptive SDD does not automatically create specifications or Project Memory in a target repository.
- Agent-produced knowledge requires review before it is marked human-verified.
