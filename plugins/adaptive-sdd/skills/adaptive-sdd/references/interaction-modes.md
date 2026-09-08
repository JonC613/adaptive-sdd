# Interaction modes

Specification tier controls documentation depth. Interaction mode controls how the
agent collaborates; it never lowers evidence requirements.

- **Guided:** pause at each meaningful artifact and explain decisions. Best for new
  users, high-learning contexts, or close oversight.
- **Collaborative:** default for new state. Group related planning decisions into a
  review package. Implementation authorization remains separate unless explicitly
  included. Pause for consequential unknowns, material scope/risk changes, access,
  cost, destructive work, or deployment outside the recorded authority.
- **Delegated:** only after explicit opt-in and bounded allowed/excluded work. Proceed
  within that boundary; the same pause conditions still apply.

Legacy projects keep their existing interaction behavior until the user chooses a
mode. `Continue` means perform the next permitted action; it does not expand scope.
When resuming, report the active feature, lifecycle, blockers, stale approvals or
evidence, and next permitted action. Ask the user to select when multiple active
features are plausible.

Memory maintenance may be included in an explicit authorization boundary. Otherwise
propose it separately. Never infer human verification from a grouped approval.
