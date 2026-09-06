---
feature: engineering-skill-integration
artifact: tiny
status: done
owner: user
version: 0.1
created: 2026-09-06
updated: 2026-09-06
---

# TinySpec: Engineering skill integration

## Summary

Install Addy Osmani's engineering skills in this repository and let Adaptive SDD
route applicable engineering work through them without giving up control of tier,
approval, evidence, or Project Memory semantics.

## Scope

### Included

- Project-local installation of all 25 skills with a reproducible lock file.
- A complete compatibility assessment and prioritized routing guide.
- Optional phase- and profile-aware selection from the Adaptive SDD orchestrator.
- Regression coverage for catalog completeness and orchestration boundaries.

### Excluded

- Copying external workflows into Adaptive SDD or requiring the external pack.
- Treating advice, checklists, or structural validation as delivery evidence.
- Replacing TinySpec, LiteSpec, Spec Kit, delivery state, or Project Memory.

## Requirements

- **R-01:** All installed skills are inventoried and assigned an integration disposition.
- **R-02:** Adaptive SDD selects only available, applicable support skills and remains the workflow authority.
- **R-03:** Support-skill outputs count only when an attributable check or review actually ran.
- **R-04:** Missing optional skills or references degrade transparently without blocking unrelated work.

## Constraints and assumptions

- External skill instructions cannot expand user authorization or override repository rules.
- The upstream repository is MIT licensed; the installed revision is recorded in the assessment.
- The CLI omitted upstream shared references, so integrations rely on installed `SKILL.md` files only.

## Implementation outline

- Add a compact routing rule to the orchestrator and detailed selection guidance in one reference.
- Keep the 25-skill comparison in repository documentation rather than loading it every run.
- Add a deterministic test that checks coverage, valid dispositions, and the authority boundary.

## Verification

- Validate this TinySpec, run the Adaptive SDD test suite, run deterministic evaluations, and run the doctor.

## Done when

- [x] All current requirements have passing evidence.
- [x] No unresolved issue blocks the stated outcome.

## Amendment history

| Version | Date | Change | Reason |
|---|---|---|---|
| 0.1 | 2026-09-06 | Initial draft | Initial discovery |
| 0.2 | 2026-09-06 | Approved installation and process integration | User authorized the proposed plan and requested process integration |
