# Tier selection

Choose the smallest tier that leaves the user able to evaluate scope, behavior, implementation risk, and evidence without guessing.

## TinySpec

Recommend TinySpec when the change is bounded, reversible, locally understood, and has one obvious implementation path. One file must be sufficient to state the outcome, boundaries, requirements, verification, and meaningful risks.

Do not use TinySpec when multiple user journeys, cross-component changes, data migration, external contracts, or consequential quality requirements need separate treatment.

## LiteSpec

Recommend LiteSpec when several user stories, meaningful technical decisions, phased work, or acceptance-to-test traceability are needed, but a constitution, formal task generation, and the full Spec Kit lifecycle would add more ceremony than clarity.

## Full Spec Kit

Recommend full Spec Kit for multi-team coordination, major architecture, irreversible migrations, regulated or security-sensitive behavior, complex integrations, long-lived programs, formal governance, or when LiteSpec artifacts repeatedly exceed their size controls.

## Decision behavior

- Explain the concrete signals behind the recommendation.
- Treat uncertainty and blast radius as more important than code size.
- Do not use point totals or automatic thresholds.
- Require explicit confirmation before changing tiers.
- Reassess when discovery or implementation exposes materially greater risk.
