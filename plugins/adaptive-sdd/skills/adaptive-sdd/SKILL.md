---
name: adaptive-sdd
description: Guide adaptive specification-driven development and portable Project Memory across TinySpec, LiteSpec, and official GitHub Spec Kit. Use when the user invokes `$adaptive-sdd`, asks which specification depth fits a change, wants one-question-at-a-time discovery, needs TinySpec or LiteSpec artifacts, wants to initialize, update, refresh, inspect, or verify a living repository memory, wants to promote an existing specification to a deeper tier, or asks to install and use full Spec Kit.
---

# Adaptive SDD

Select the smallest specification tier that creates sufficient shared understanding. A request to build or fix authorizes routine planning, implementation, relevant tests, and maintenance of affected existing documentation within that scope. Reuse authorization already given; do not ask again at each stage. A request only to plan, review, or explain does not authorize implementation.

For implemented work, read [references/delivery-evidence.md](references/delivery-evidence.md).
Read [references/interaction-modes.md](references/interaction-modes.md) when choosing
or resuming collaboration behavior. Collaborative is the default, including when resuming older projects unless the user requested guided checkpoints. Read
[references/project-profiles.md](references/project-profiles.md) when the work is not
a conventional application feature or needs specialized evidence.

## Orient before writing

1. Resolve the repository, feature, and desired outcome.
2. When `.sdd/memory/index.md` exists, read it first and load only relevant Project Memory concepts. Treat them as context, verify consequential claims against current code, and report contradictions or potential staleness.
3. Inspect the codebase read-only: architecture, relevant behavior, tests, dependencies, conventions, and deployment surfaces.
4. Read [references/tier-selection.md](references/tier-selection.md).
5. Recommend TinySpec, LiteSpec, or full Spec Kit with a project-specific rationale.
6. Proceed with the appropriate tier within the requested scope. Ask before adding tooling or materially expanding the work unless already authorized.
7. Tell the user before external research. Prefer primary sources for unstable, regulated, unfamiliar, or high-risk facts.

Do not use a numerical complexity score. Do not infer implementation permission from approval of a specification.

## Maintain Project Memory

Read [references/project-memory.md](references/project-memory.md) whenever the user asks to initialize, inspect, update, refresh, or verify living repository memory, or when completed implementation may have changed durable repository knowledge.

Use one shared workflow for Codex and Cursor. `$adaptive-sdd` and `/adaptive-sdd` are invocation differences only; never store provider-specific state in the memory bundle.

- **Initialize memory:** when requested, inspect the repository, use `scripts/project_memory.py scaffold`, write the smallest useful concepts with sources or explicit assumptions, and verify once. Refuse overwrite. Do not claim human review unless it occurred.
- **Status memory:** run `scripts/project_memory.py status --project <root>` read-only and explain current, potential drift, or limited-confidence results without claiming drift proves factual error.
- **Verify memory:** run `scripts/project_memory.py verify --project <root>` read-only. Separate failures from freshness and optional-link warnings.
- **Update memory:** maintain affected existing memory as part of the requested implementation. Record only durable current-state changes and provenance, update `log.md`, and verify once after the batch. Do not copy complete specifications or claim human review.
- **Refresh memory:** when requested, inspect changes since the recorded commit and apply supported corrections or record a no-op. Reconcile the inspected commit after relevant validation; ask only about consequential unresolved contradictions.

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

Fill the artifact and proceed to implementation when the user's request authorizes it. For planning-only work, leave it in `review`. `approved` records intent covered by the user's authorization, not a claim that the user reviewed generated text. Validate the completed artifact once; repeat only after relevant structural changes or failures.

Use TinySpec only while behavior, boundaries, implementation direction, and verification remain clear in one concise artifact.

## Run LiteSpec

Read [references/litespec-method.md](references/litespec-method.md). Prepare three related artifacts as one planning batch:

```text
.litespec/<feature>/
├── spec.md
├── plan.md
└── tests.md
```

Use `scripts/scaffold_litespec.py` to create spec, plan, and tests in dependency order without intermediate approvals. Validate the completed package once. Use `--guided` on the scaffolder only when the user requested individual artifact checkpoints.

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

## Complete authorized work

1. Determine authorization from the current request and prior conversation. Ask only when implementation is not already authorized or a consequential decision cannot be inferred.
2. Set approved artifacts to `implementing`.
3. Execute approved tasks in dependency order.
4. Run relevant checks at meaningful milestones and before handoff. Reuse passing results while their tested behavior and dependencies remain unchanged. Repeat affected checks for relevant changes, failures, or unresolved concerns; do not rerun suites for status requests or unrelated documentation edits.
5. Report actual outcomes and test evidence. Structural validation is not delivery evidence. Use delivery-state tracking when requested or already active; it is optional for ordinary work. Its strict `verify` and `release` claims still require their recorded evidence.
6. Update affected existing Project Memory within scope, batching edits and validation.
7. Set artifacts to `done` when completion criteria are met. Do not invent test results or human verification.

Handle routine implementation decisions and compatible amendments within existing authorization. Update affected artifacts together. Pause only for consequential unresolved choices, material scope or risk expansion, or actions outside existing authority. Do not turn an in-scope amendment into another approval cycle.

## Report clearly

Lead with the outcome. Surface validation failures or decisions requiring user action; keep routine bookkeeping quiet. At handoff, summarize changes, relevant checks, and limitations without requiring acknowledgment to finish.
