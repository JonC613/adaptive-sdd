# Migration rules

## TinySpec to LiteSpec

Preserve the approved TinySpec unchanged. Seed a draft LiteSpec specification with its summary, scope, requirements, constraints, verification conditions, and a provenance link. Ask for missing user stories, acceptance criteria, edge cases, and non-functional requirements. Then follow normal LiteSpec approval gates.

## LiteSpec to Spec Kit

Preserve the LiteSpec package unchanged. Install official Spec Kit only after approval. Carry forward:

- Product intent, scope, stories, and acceptance criteria from `spec.md`
- Decisions, risks, dependencies, and phases from `plan.md`
- Acceptance mappings and evidence obligations from `tests.md`

Record the LiteSpec feature, version, and path as provenance. Let official Spec Kit commands produce their native artifacts; do not fabricate command output.

## Compatibility

- Keep stable IDs where the target format permits them.
- Never mark promoted artifacts approved automatically.
- Never delete the source tier during promotion.
- Treat a changed core outcome as a new approval cycle, not a mechanical conversion.
