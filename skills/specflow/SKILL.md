---
name: specflow
description: Guide adaptive specification-driven development across TinySpec, LiteSpec, and official GitHub Spec Kit. Use when the user invokes `$specflow`, asks which specification depth fits a change, wants one-question-at-a-time discovery, needs TinySpec or LiteSpec artifacts, wants to promote an existing specification to a deeper tier, or asks to install and use full Spec Kit with Codex.
---

# SpecFlow

Use one orchestrator to select and guide the smallest specification tier that creates sufficient shared understanding. Preserve user control through explicit tier, artifact, and implementation approvals.

## Orient before writing

1. Resolve the repository, feature, and desired outcome.
2. Inspect the codebase read-only: architecture, relevant behavior, tests, dependencies, conventions, and deployment surfaces.
3. Read [references/tier-selection.md](references/tier-selection.md).
4. Recommend TinySpec, LiteSpec, or full Spec Kit with a project-specific rationale.
5. Ask for tier confirmation before creating artifacts or installing tooling.
6. Tell the user before external research. Prefer primary sources for unstable, regulated, unfamiliar, or high-risk facts.

Do not use a numerical complexity score. Do not infer implementation permission from approval of a specification.

## Conduct discovery

- Ask one focused question at a time.
- Adapt the next question to the previous answer.
- Offer two or three mutually exclusive choices when useful and permit a custom answer.
- Resolve user value, current scope, exclusions, observable acceptance, relevant quality expectations, constraints, and consequential unknowns.
- Record low-risk assumptions; resolve high-impact unknowns before approval.

## Run TinySpec

Read [references/tinyspec-method.md](references/tinyspec-method.md). Create exactly one `.tinyspec/<feature>.md` using `assets/tinyspec.md` or:

```text
python <skill-dir>/scripts/scaffold_tinyspec.py --project <root> --feature <slug> --title "<title>"
```

Fill the artifact, set it to `review`, validate it, and request approval. After approval, set `status: approved` and offer implementation separately.

Use TinySpec only while behavior, boundaries, implementation direction, and verification remain clear in one concise artifact.

## Run LiteSpec

Read [references/litespec-method.md](references/litespec-method.md). Create three approval-gated artifacts in order:

```text
.litespec/<feature>/
├── spec.md
├── plan.md
└── tests.md
```

Use `scripts/scaffold_litespec.py` and `scripts/validate_litespec.py`. Never create `plan.md` before specification approval or `tests.md` before plan approval.

## Run full Spec Kit

Read [references/speckit-adapter.md](references/speckit-adapter.md). Use only the official `github/spec-kit` distribution. Confirm installation because it changes project tooling and creates `.specify/`, `specs/`, and Codex skills.

After installation, hand control to the official `$speckit-*` skills. Do not reproduce or silently override upstream Spec Kit workflows.

## Promote safely

Read [references/migration-rules.md](references/migration-rules.md).

- Promote TinySpec to LiteSpec when one file no longer captures sufficient behavioral or test detail.
- Promote LiteSpec to full Spec Kit when coordination, architecture, governance, migrations, or risk exceed LiteSpec's three-artifact contract.
- Preserve the source artifacts and provenance.
- Ask follow-up questions for missing information; never manufacture approval, user stories, acceptance criteria, or architectural decisions.
- Do not automatically downgrade active work. A completed feature may receive a read-only summary.

## Implement through explicit approval

1. Wait for explicit implementation authorization.
2. Set approved artifacts to `implementing`.
3. Execute approved tasks in dependency order.
4. Run agreed tests and tier validation.
5. Set artifacts to `done` only when their completion criteria are satisfied.

When requirements change, pause affected work, explain the smallest coherent amendment, request approval, update every affected artifact, increment the minor version, and revalidate.

## Report clearly

Lead with the current outcome or decision. At each gate, state what changed, what remains unresolved, and what the next approval permits. End with artifact paths, statuses, validation evidence, and the next authorized action.
