---
type: Software Architecture
title: "Adaptive SDD architecture"
description: "Current plugin layout and responsibility boundaries."
status: stable
generated: {"by":"adaptive-sdd/0.4.0","at":"2026-09-06T21:04:26Z"}
verified: [{"by":"human:user","at":"2026-09-06T03:01:31Z"},{"by":"human:user","at":"2026-09-06T16:39:41Z"},{"by":"human:user","at":"2026-09-06T17:28:12Z"}]
sources: [{"id":"skill","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md","title":"Shared orchestrator"},{"id":"tests","resource":"../../plugins/adaptive-sdd/tests/test_adaptive_sdd.py","title":"Deterministic test suite"},{"id":"delivery-state","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/scripts/delivery_state.py","title":"Delivery state engine"},{"id":"installer","resource":"../../plugins/adaptive-sdd/scripts/install-project.ps1","title":"Project installer"},{"id":"installer-common","resource":"../../plugins/adaptive-sdd/scripts/install-common.ps1","title":"Safe installation mechanics"},{"id":"evaluations","resource":"../../plugins/adaptive-sdd/evals/evaluate.py","title":"Deterministic evaluation harness"},{"id":"cursor-manifest","resource":"../../plugins/adaptive-sdd/plugin.json","title":"Agent Plugin manifest"},{"id":"codex-manifest","resource":"../../plugins/adaptive-sdd/.codex-plugin/plugin.json","title":"Codex plugin manifest"},{"id":"habit-tracker-app","resource":"../../plugins/adaptive-sdd/examples/habit-tracker/app.js","title":"Daymark application"},{"id":"habit-tracker-tests","resource":"../../plugins/adaptive-sdd/examples/habit-tracker/app.test.mjs","title":"Daymark automated tests"}]
sdd: {"profile_version":1,"assumptions":[]}
---

# Architecture

## Components

- `skills/adaptive-sdd/SKILL.md` is the shared public orchestrator.
- `assets/`, `references/`, and `scripts/` provide shared templates, method rules, and deterministic mechanics.
- The root Agent Plugin manifest and `.codex-plugin/plugin.json` adapt discovery without forking behavior.
- Root `install-project.ps1` and `install-cursor-local.ps1` bootstrap scripts delegate to the versioned plugin installers, so clone-root commands stay stable for new repositories.
- `scripts/install-project.ps1` copies the shared skill into a target repository.
- `scripts/install-common.ps1` provides canonical destination checks, staged publication, and recoverable backups.
- `skills/adaptive-sdd/scripts/delivery_state.py` persists resumable feature state and applies evidence-backed verification and release gates.
- `skills/adaptive-sdd/scripts/doctor.py` reports local compatibility without mutating the project.
- `tests/` and `evals/` provide regression coverage and deterministic workflow safety scenarios.
- `examples/habit-tracker/` is a self-contained static application: `app.js` owns local state, date-key, storage, and rendering logic; `app.test.mjs` exercises its pure state and calendar functions with Node's built-in test runner.

## Relationships and flows

- Natural requests enter through the shared skill, which selects a specification tier or a Project Memory operation.
- TinySpec and LiteSpec are owned by Adaptive SDD; full Spec Kit is delegated to official upstream-installed workflows.
- Project Memory remains orthogonal to tier selection and records only durable implemented state with provenance.
- The Daymark example opens directly in a browser, stores data only in browser-local storage, and has no backend or build pipeline.
- Interaction mode and project profile are independent dimensions layered over the selected tier.
- Structural validators check artifacts; delivery state separately determines whether current implementation evidence satisfies approved outcomes.

## Constraints and invariants

- Artifact creation, tier promotion, implementation, and generated memory writes require explicit approval.
- Codex and Cursor use the same installed skill, assets, references, and Python scripts.
- Target repository knowledge stays in portable files rather than provider-specific storage.
- Installed content is staged before replacement, and unexpected destination content is never recursively removed.
- Delivery attribution is reviewable repository state, not authenticated identity or cryptographic proof.
