# Using Adaptive SDD

Start with a natural request:

```text
$adaptive-sdd Help me add CSV export to this application.
```

In Cursor, invoke the same skill as:

```text
/adaptive-sdd Help me add CSV export to this application.
```

Adaptive SDD inspects the repository, recommends a tier with rationale, and waits for confirmation. Discovery proceeds one focused question at a time.

When `.sdd/memory/` exists, Adaptive SDD reads its index first, loads only relevant concepts, and verifies consequential claims against the code before using them. Memory is context, not authority.

## TinySpec

TinySpec creates `.tinyspec/<feature>.md`. It combines intent, boundaries, requirements, implementation direction, and verification in one compact contract.

Use it when the change is bounded and reversible. Promote when separate stories, planning, or traceability become necessary.

## LiteSpec

LiteSpec creates three gated artifacts:

```text
.litespec/<feature>/spec.md
.litespec/<feature>/plan.md
.litespec/<feature>/tests.md
```

Each artifact requires explicit approval before the next is created. Implementation requires separate authorization after all three are approved.

## Full Spec Kit

Adaptive SDD explains why the full workflow is warranted and asks before installing it. Once installed, official `$speckit-*` skills own the full workflow. Adaptive SDD does not fork or override those skills.

## Useful direct validation

```text
python .agents/skills/adaptive-sdd/scripts/validate_tinyspec.py .tinyspec/my-feature.md
python .agents/skills/adaptive-sdd/scripts/validate_litespec.py .litespec/my-feature
```

Add `--approved` before implementation to require approved-or-later lifecycle states.

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
