---
type: Software Architecture
title: "Adaptive SDD architecture"
description: "Current plugin layout and responsibility boundaries."
status: stable
generated: {"by":"adaptive-sdd/0.4.0","at":"2026-09-06T16:39:41Z"}
verified: [{"by":"human:user","at":"2026-09-06T03:01:31Z"},{"by":"human:user","at":"2026-09-06T16:39:41Z"}]
sources: [{"id":"skill","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md","title":"Shared orchestrator"},{"id":"tests","resource":"../../plugins/adaptive-sdd/tests/test_adaptive_sdd.py","title":"Deterministic test suite"},{"id":"delivery-state","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/scripts/delivery_state.py","title":"Delivery state engine"},{"id":"installer","resource":"../../plugins/adaptive-sdd/scripts/install-project.ps1","title":"Project installer"},{"id":"installer-common","resource":"../../plugins/adaptive-sdd/scripts/install-common.ps1","title":"Safe installation mechanics"},{"id":"evaluations","resource":"../../plugins/adaptive-sdd/evals/evaluate.py","title":"Deterministic evaluation harness"},{"id":"cursor-manifest","resource":"../../plugins/adaptive-sdd/plugin.json","title":"Agent Plugin manifest"},{"id":"codex-manifest","resource":"../../plugins/adaptive-sdd/.codex-plugin/plugin.json","title":"Codex plugin manifest"},{"id":"engineering-routing","resource":"../../plugins/adaptive-sdd/skills/adaptive-sdd/references/engineering-skill-routing.md","title":"Engineering skill routing"},{"id":"skills-lock","resource":"../../skills-lock.json","title":"Installed engineering skill lock"}]
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
- `skills/adaptive-sdd/references/engineering-skill-routing.md` maps project phase and profile needs to the smallest applicable optional support-skill set.
- `.agents/skills/` contains project-local engineering support skills, with `skills-lock.json` recording their reproducible source and content hashes.
- `tests/` and `evals/` provide regression coverage and deterministic workflow safety scenarios.

## Relationships and flows

- Natural requests enter through the shared skill, which selects a specification tier or a Project Memory operation.
- TinySpec and LiteSpec are owned by Adaptive SDD; full Spec Kit is delegated to official upstream-installed workflows.
- Project Memory remains orthogonal to tier selection and records only durable implemented state with provenance.
- Interaction mode and project profile are independent dimensions layered over the selected tier.
- When engineering support is useful, Adaptive SDD selects available skills for bounded advice, execution, or checks and then records attributable results through its own delivery-evidence model.
- Structural validators check artifacts; delivery state separately determines whether current implementation evidence satisfies approved outcomes.

## Constraints and invariants

- Artifact creation, tier promotion, implementation, and generated memory writes require explicit approval.
- Codex and Cursor use the same installed skill, assets, references, and Python scripts.
- Target repository knowledge stays in portable files rather than provider-specific storage.
- Installed content is staged before replacement, and unexpected destination content is never recursively removed.
- Delivery attribution is reviewable repository state, not authenticated identity or cryptographic proof.
- External skills remain optional and subordinate to Adaptive SDD's tier, approval, authorization, evidence, release, and Project Memory semantics.
