---
name: adaptive-sdd
description: Guide adaptive specification-driven development and portable Project Memory across TinySpec, LiteSpec, and official GitHub Spec Kit. Use when the user invokes `$adaptive-sdd`, asks which specification depth fits a change, wants one-question-at-a-time discovery, needs TinySpec or LiteSpec artifacts, wants to initialize, update, refresh, inspect, or verify a living repository memory, wants to promote an existing specification to a deeper tier, or asks to install and use full Spec Kit.
---

# Adaptive SDD

Use one orchestrator to select and guide the smallest specification tier that creates sufficient shared understanding. Preserve user control through explicit tier, artifact, and implementation approvals.

## Orient before writing

1. Resolve the repository, feature, and desired outcome.
2. When `.sdd/memory/index.md` exists, read it first and load only relevant Project Memory concepts. Treat them as context, verify consequential claims against current code, and report contradictions or potential staleness.
3. Inspect the codebase read-only: architecture, relevant behavior, tests, dependencies, conventions, and deployment surfaces.
4. Read [references/tier-selection.md](references/tier-selection.md).
5. Recommend TinySpec, LiteSpec, or full Spec Kit with a project-specific rationale.
6. Ask for tier confirmation before creating artifacts or installing tooling.
7. Tell the user before external research. Prefer primary sources for unstable, regulated, unfamiliar, or high-risk facts.

Do not use a numerical complexity score. Do not infer implementation permission from approval of a specification.

## Maintain Project Memory

Read [references/project-memory.md](references/project-memory.md) whenever the user asks to initialize, inspect, update, refresh, or verify living repository memory, or when completed implementation may have changed durable repository knowledge.

Use one shared workflow for Codex and Cursor. `$adaptive-sdd` and `/adaptive-sdd` are invocation differences only; never store provider-specific state in the memory bundle.

- **Initialize memory:** inspect the repository read-only, draft the smallest useful project and architecture concepts with evidence or explicit assumptions, show the complete proposal, and wait for approval. After approval, use `scripts/project_memory.py scaffold`, apply the accepted content, verify it, and record the approved commit. Refuse overwrite.
- **Status memory:** run `scripts/project_memory.py status --project <root>` read-only and explain current, potential drift, or limited-confidence results without claiming drift proves factual error.
- **Verify memory:** run `scripts/project_memory.py verify --project <root>` read-only. Separate failures from freshness and optional-link warnings.
- **Update memory:** after approved SDD implementation, propose only durable current-state changes and tier provenance. Do not copy complete specifications. Apply after approval, update `log.md`, verify, then reconcile the approved commit.
- **Refresh memory:** inspect changes since the recorded commit, propose affected edits or a no-op, and wait for approval. Rejection changes nothing. A reviewed no-op may reconcile after validation.

Project Memory is not a fourth specification tier and does not change tier selection. TinySpec, LiteSpec, official Spec Kit, and repository-only changes may all provide provenance. Preserve promoted artifacts and never modify official Spec Kit-owned files through memory maintenance.

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
5. Assess whether the completed code changed durable Project Memory. If memory exists, propose the smallest evidence-backed update and obtain approval before applying it.
6. Set artifacts to `done` only when their completion criteria and any approved memory update are satisfied.

When requirements change, pause affected work, explain the smallest coherent amendment, request approval, update every affected artifact, increment the minor version, and revalidate.

## Report clearly

Lead with the current outcome or decision. At each gate, state what changed, what remains unresolved, and what the next approval permits. End with artifact paths, statuses, validation evidence, and the next authorized action.
