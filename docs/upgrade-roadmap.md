# Project status

Current manifest version: **0.4.1**. See the [changelog](../CHANGELOG.md) for released-version history and unreleased changes. This status describes repository contents; it is not a record of deployment or live-agent performance.

| Area | Implemented evidence | Remaining work |
|---|---|---|
| Installer safety | [Guarded installers](../plugins/adaptive-sdd/scripts/) and temporary-directory integration tests | Fresh live Spec Kit and marketplace checks |
| Specification validation | TinySpec/LiteSpec validators and [negative cases](../plugins/adaptive-sdd/tests/test_reliability.py) | Broader real-project format feedback |
| Delivery state | Optional approvals, evidence, snapshots, and [strict verification regressions](../plugins/adaptive-sdd/tests/test_delivery_state.py) | Evidence attribution remains a stated claim |
| Shared workflow | [Codex/Cursor guidance](../plugins/adaptive-sdd/skills/adaptive-sdd/SKILL.md), interaction modes, and portable Project Memory | Broader usability evidence |
| Profiles and examples | Six [profile examples](../plugins/adaptive-sdd/examples/profiles/) and runnable [Daymark](../plugins/adaptive-sdd/examples/habit-tracker/) | Additional representative projects |
| Evaluation | Explicit [deterministic scenario results](../plugins/adaptive-sdd/evals/) | Optional live-agent evaluation; no measurements yet |
| CI and presentation | Python, JavaScript, browser, and repository checks; [case study](case-study.md) and [demo](demo.md) | Review actual CI runs for each proposed release |
| Distribution | Versioned manifests and installation guidance | Owner license decision and release checklist |

No deployment, productivity, or production-maturity conclusion is recorded.

## Verification policy

Structural validation is not delivery verification. Local tests do not establish cross-platform CI success. Mocked installer commands do not establish live Spec Kit compatibility. Missing evidence remains missing. Use the [release-readiness checklist](release-readiness.md) to collect evidence before any future release.
