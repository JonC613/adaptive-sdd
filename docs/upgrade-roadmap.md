# Adaptive SDD upgrade execution

Approved in conversation: phased roadmap, Collaborative default for new projects,
and explicit implementation authorization. Existing project defaults are unchanged.
This record is a work tracker, not evidence that the roadmap is delivered.

| Release | Priority | Work | Status |
|---|---|---|---|
| 1 | P0 | Installer safety; structural validator correctness; memory drift; regressions | Implemented locally |
| 2 | P1 | Feature state; evidence; verification; fingerprint-bound approvals; legacy compatibility | Implemented locally |
| 3 | P1 | Interaction modes; grouped approval; authority boundaries; resume; memory integration | Implemented locally |
| 4 | P2 | Optional project profiles and representative examples | Implemented locally; broader pilots pending |
| 5 | P2 | Workflow evaluations; doctor; compatibility; distribution readiness | Partial: deterministic local checks implemented; live compatibility and owner license decision pending |

Release 1 must be verified independently before later changes. No release, remote
push, installation into another project, paid API call, or license selection is
authorized by this execution record. A license choice remains an owner decision.
Existing uncommitted changes belong to the user and must be preserved.

Implementation, local verification, and the approved Project Memory update are
complete. Git reconciliation and release evidence remain post-commit operations.

## Verification policy

Structural validation is not delivery verification. Local tests do not establish
cross-platform CI success. Mocked installer commands do not establish live Spec Kit
compatibility. Missing evidence remains missing rather than inferred from status.
