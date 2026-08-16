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
