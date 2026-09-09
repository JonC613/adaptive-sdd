# Using Adaptive SDD

## Delivery status versus document status

TinySpec and LiteSpec validators establish structure only. For an optional strict delivery audit (requested or already active),
initialize `.sdd/features/<feature>/state.json` with `delivery_state.py`, record
fingerprint-bound approval, update tasks, attach real evidence, and run `verify`.
Only `release --reference <external-reference>` may advance verified work to released.
Legacy `done` artifacts are not automatically treated as verified.

## Interaction mode and project profile

New delivery state defaults to Collaborative mode. Guided adds review pauses;
Delegated requires an explicit allowed/excluded boundary. Choose project profiles
independently: application, API/library, AI system, data pipeline, infrastructure,
or research/design/documentation. Profiles add relevant questions and evidence,
not mandatory ceremony.

## Diagnostics and evaluations

Run `python skills/adaptive-sdd/scripts/doctor.py --plugin <plugin-root>` for local,
read-only diagnostics. Run `python evals/evaluate.py --plugin <plugin-root>` for the
deterministic safety scenarios. Neither command claims live marketplace, Spec Kit,
or paid-agent compatibility.

Start with a natural request:

```text
$adaptive-sdd Help me add CSV export to this application.
```

In Cursor, invoke the same skill as:

```text
/adaptive-sdd Help me add CSV export to this application.
```

Adaptive SDD inspects the repository, selects a tier with rationale, and proceeds within the requested scope. Ask focused questions only when consequential information is missing.

When `.sdd/memory/` exists, Adaptive SDD reads its index first, loads only relevant concepts, and verifies consequential claims against the code before using them. Memory is context, not authority.

## TinySpec

TinySpec creates `.tinyspec/<feature>.md`. It combines intent, boundaries, requirements, implementation direction, and verification in one compact contract.

Use it when the change is bounded and reversible. Promote when separate stories, planning, or traceability become necessary.

## LiteSpec

LiteSpec prepares three related artifacts as one batch:

```text
.litespec/<feature>/spec.md
.litespec/<feature>/plan.md
.litespec/<feature>/tests.md
```

A build/fix request authorizes routine planning, implementation, checks, and affected existing documentation. No separate sign-offs are required. Planning-only work remains planning-only. Use scaffolder `--guided` for user-requested artifact checkpoints.

Validate the completed planning batch once and run relevant tests at meaningful milestones and handoff. Repeat affected checks only when relevant changes, failures, or unresolved concerns justify it. Surface actionable failures and summarize results at handoff.

## Full Spec Kit

Adaptive SDD explains why the full workflow is warranted and asks before installing it. Once installed, official `$speckit-*` skills own the full workflow. Adaptive SDD does not fork or override those skills.

## Useful direct validation

```text
python .agents/skills/adaptive-sdd/scripts/validate_tinyspec.py .tinyspec/my-feature.md
python .agents/skills/adaptive-sdd/scripts/validate_litespec.py .litespec/my-feature
```

Optional `--approved` requires approved-or-later lifecycle states; it does not require another user approval.

## Project Memory

Project Memory preserves the current repository understanding across changes while specifications retain point-in-time intent and evidence. It uses an OKF v0.2 Markdown bundle plus separate reconciliation state.

```text
$adaptive-sdd initialize memory
$adaptive-sdd status memory
$adaptive-sdd update memory
$adaptive-sdd refresh memory
$adaptive-sdd verify memory
```

In Cursor, replace `$adaptive-sdd` with `/adaptive-sdd`. Both forms use the same skill and Python scripts.

- `initialize` inspects the code and proposes the first project and architecture concepts before writing.
- `status` reports the recorded commit and current `HEAD` read-only.
- `update` proposes durable memory changes after SDD implementation.
- `refresh` examines work completed outside Adaptive SDD and proposes edits or a reviewed no-op.
- `verify` checks the bundle, sources, links, Git references, and reconciliation state.

Direct deterministic checks are also available:

```text
python .agents/skills/adaptive-sdd/scripts/project_memory.py status --project .
python .agents/skills/adaptive-sdd/scripts/project_memory.py verify --project .
```

Commit drift is a warning that memory may need review; it is not proof that the documentation is wrong. Generated content is never marked human-reviewed without explicit approval.
