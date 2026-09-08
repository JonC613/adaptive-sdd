# Optional project profiles

Profiles add relevant discovery and evidence expectations to the generic outcome,
constraints, implementation, and verification core. They do not create separate
workflows, automatically choose a tier, or require irrelevant template sections.
Inspect the repository, recommend one or more profiles, and confirm consequential
choices.

| Profile | Discover | Evidence examples |
|---|---|---|
| application | user flows, accessibility, responsive and failure behavior | component, accessibility and end-to-end checks |
| api-library | contracts, compatibility, consumers and versioning | contract, integration, property and compatibility tests |
| ai-system | quality threshold, evaluation data, cost, privacy and safety | pinned eval fixtures, rubric, cost and refusal reports |
| data-pipeline | lineage, quality, idempotency, backfill and recovery | data-quality assertions, replay and recovery checks |
| infrastructure | blast radius, security, rollout and rollback | change preview, policy scan, deployment and rollback evidence |
| research-design-docs | audience, sources, uncertainty, usability and review | reproducible experiment, citations, review rubric and sign-off |

Mixed projects may combine profiles. A profile is supported only when its worked
example and workflow evaluation pass; otherwise describe it as experimental.
User-story phrasing is optional outside stakeholder-facing behavior. Stable outcomes
and observable criteria remain required.
