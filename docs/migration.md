# Promotion and migration

Promotion deepens the contract without destroying the prior tier.

## TinySpec to LiteSpec

1. Preserve the approved `.tinyspec/<feature>.md`.
2. Create a draft `.litespec/<feature>/spec.md`.
3. Carry forward intent, scope, requirements, constraints, and verification.
4. Record the TinySpec path and version as provenance.
5. Ask for missing stories, acceptance criteria, edge cases, and quality requirements.
6. Continue through the normal LiteSpec approval gates.

## LiteSpec to Spec Kit

1. Preserve the complete `.litespec/<feature>/` package.
2. Confirm and install official Spec Kit.
3. Use the approved LiteSpec as source material for official specification commands.
4. Carry forward stable IDs where the target format permits.
5. Record the source feature path and versions.
6. Review and approve the new native artifacts normally.

## Downgrading

Do not downgrade active work automatically. A completed feature may receive a compact read-only summary, but the deeper artifacts remain the authoritative record.
