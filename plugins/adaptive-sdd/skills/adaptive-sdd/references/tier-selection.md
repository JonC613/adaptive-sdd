# Tier selection

Choose the smallest tier that leaves the user able to evaluate scope, behavior, implementation risk, and evidence without guessing.

## TinySpec

Recommend TinySpec when the change is bounded, reversible, locally understood, and has one obvious implementation path. One file must be sufficient to state the outcome, boundaries, requirements, verification, and meaningful risks.

Do not use TinySpec when multiple user journeys, cross-component changes, data migration, external contracts, or consequential quality requirements need separate treatment.

## LiteSpec

Recommend LiteSpec when several user stories, meaningful technical decisions, phased work, or acceptance-to-test traceability are needed, but a constitution, formal task generation, and the full Spec Kit lifecycle would add more ceremony than clarity.

### Application integration signals

Recommend LiteSpec for a new or materially expanded application that accepts external content, persists user data, or is deployed as a service. Capture only the applicable decisions before approval:

- **Untrusted inputs:** accepted source types, validation, size and time limits, malformed-content behavior, and user-visible recovery.
- **Remote retrieval:** allowed URL policy, redirect handling, server-side request protections, source attribution, and parser fallback behavior.
- **Files and documents:** supported formats, extraction limits, storage location and retention, cleanup, and behavior when extraction is incomplete.
- **Data and access:** ownership, authentication or access assumptions, persistence boundaries, deletion/export needs, and privacy-sensitive fields.
- **Deployment and operations:** required environment configuration, availability/failure behavior, observability, and rollback or safe-disable plan.
- **Evidence:** fixtures for valid and hostile inputs, integration coverage for source-to-review-to-save flows, and manual deployment checks where automation is unsuitable.

These signals do not automatically require full Spec Kit. Escalate only when the integration is security-sensitive, regulated, irreversible, or coordinated across teams.

## Full Spec Kit

Recommend full Spec Kit for multi-team coordination, major architecture, irreversible migrations, regulated or security-sensitive behavior, complex integrations, long-lived programs, formal governance, or when LiteSpec artifacts repeatedly exceed their size controls.

## Decision behavior

- Explain the concrete signals behind the recommendation.
- Treat uncertainty and blast radius as more important than code size.
- Do not use point totals or automatic thresholds.
- Require explicit confirmation before changing tiers.
- Reassess when discovery or implementation exposes materially greater risk.
