# Interaction modes

Specification tier controls documentation depth. Interaction mode controls how the
agent collaborates; it never lowers evidence requirements.

- **Guided (only when requested):** pause at each meaningful artifact and explain decisions. Best for new
  users, high-learning contexts, or close oversight.
- **Collaborative:** default for new state. Group related planning decisions into a
  review package. A build/fix request authorizes routine planning, implementation,
  checks, and affected existing documentation without separate sign-offs. Pause for consequential unknowns, material scope/risk changes, access,
  cost, destructive work, or deployment outside the recorded authority.
- **Delegated:** only after explicit opt-in and bounded allowed/excluded work. Proceed
  within that boundary; the same pause conditions still apply.

Use Collaborative behavior for legacy projects too unless guided checkpoints were requested. `Continue` means perform the next permitted action; it does not expand scope.
When resuming, report the active feature, lifecycle, blockers, stale approvals or
evidence, and next permitted action. Ask the user to select when multiple active
features are plausible.

Maintain affected existing memory within the implementation request without separate approval. Never infer human verification from a grouped approval.

Validate the completed planning batch once. Run relevant implementation checks at
meaningful milestones and handoff. Repeat affected checks only for relevant changes,
failures, or unresolved concerns; status requests and unrelated edits do not trigger
another validation cycle. Summarize results at handoff and surface actionable failures.
