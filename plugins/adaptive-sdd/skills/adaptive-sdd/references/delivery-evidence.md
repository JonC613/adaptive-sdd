# Delivery state and evidence

Specification approval states intent. Structural validation checks document shape.
Neither proves delivery. Delivery state is an optional strict audit: use it when requested or already active, not as a prerequisite for ordinary implementation. Otherwise report real checks and outcomes directly. To initialize state:

```text
python scripts/delivery_state.py --project <root> init --feature <slug> --tier lite
python scripts/delivery_state.py --project <root> approve --feature <slug> --by human:<id> --action implementation
python scripts/delivery_state.py --project <root> status --feature <slug>
```

State lives at `.sdd/features/<feature>/state.json`. It contains no conversation
history or secrets. It records the tier, interaction mode, authorization summary,
artifact fingerprints, tasks, evidence, blockers, lifecycle, and release reference.
It is an audit aid, not cryptographic identity or a security boundary.

Use `task` to record `pending`, `doing`, `done`, or `blocked`. Record evidence only
after the referenced check or review actually occurs. Evidence methods are
`automated`, `manual`, `experiment`, and `contract`; results are `pass` or `fail`.
Every record names its actor, repository-relative source, time, and source snapshot.
Automated evidence also requires a recorded command and exit code; the tool checks
their consistency with the stated result but does not execute the command. Manual
evidence requires a `human:` actor. Attribution is a claim, not identity verification.

`verify` is a completion gate. It requires current artifact approvals, completed
tasks, passing evidence for every acceptance criterion, and no explicit blockers.
`release` additionally requires that the current snapshot still matches verified
work, explicit release authorization (or delegated deployment authority), and records an external release reference. A changed artifact or worktree makes
earlier evidence stale; never silently refresh or manufacture it.

Existing `done` artifacts are legacy/unverified until state and evidence are added.
Do not rewrite them during initialization. Official Spec Kit files remain upstream
owned and are referenced read-only.

Record existing authorization without asking again. Use `--by process:<id>` for
artifacts recorded under a build/fix request; reserve human attribution for actual
human review. In-scope amendments can refresh artifact fingerprints under that
authority, but never refresh evidence unless its check actually ran. Batch final
artifact and memory edits before checks to avoid snapshot invalidation. Run `verify`
once after the completed batch; repeat after changes or failures. These strict
snapshot rules apply only to the audit, not to ordinary implementation.

## Supported strict delivery formats

The gate re-reads the approved artifacts on every status/verification check. An empty set of criteria is a blocker, never a vacuous success. `init` and `approve` may record an incomplete draft; use `status --json` to see what must be corrected before verification.

| Tier | Artifact layout | Required evidence keys | Tasks |
|---|---|---|---|
| Current TinySpec | One file with template metadata and required sections | `R-01` etc., defined as `- **R-01:** observable outcome` under Requirements | No task list required |
| Legacy TinySpec | `# TinySpec:` with What, Requirements, Plan, and Done When sections | Numbered Requirements become `R-01`, `R-02`, etc. in state only | Historical checkboxes are not imported as execution evidence |
| LiteSpec | One directory or all three files: spec.md, plan.md, tests.md; existing structural/traceability rules apply | Every `AC-XX.N` definition in spec.md; references in plans/tests are not definitions | `P1-T1` etc. from plan.md |
| Spec Kit | One feature directory containing spec.md, plan.md, tasks.md, or all three files | `FR-001`, `SC-001`, and numbered acceptance scenarios mapped to `US1-AC1` etc. | `T001` etc. from tasks.md |

The Spec Kit adapter recognizes the pinned v0.16.4 Markdown shape: User Scenarios & Testing, Requirements, Success Criteria, `### User Story N` headings, and numbered Given/When/Then acceptance scenarios. This is a bounded delivery adapter, not a complete validator for every upstream artifact or future version. Source formats: [specification template](https://github.com/github/spec-kit/blob/v0.16.4/templates/spec-template.md) and [task template](https://github.com/github/spec-kit/blob/v0.16.4/templates/tasks-template.md). Unsupported shapes require an explicit adapter update or use of the ordinary upstream workflow; do not silently translate them into an empty verified state.

Criterion definitions need nonempty outcome text without unresolved template placeholders. Duplicate IDs, malformed definitions, unrecognized structures, and missing required artifacts block strict verification. Comments and fenced examples do not count as criteria. Recognition cannot judge whether prose is sufficiently testable; the reviewer remains responsible for that judgment. LiteSpec's gate keys are acceptance criteria; ensure the specification's acceptance criteria cover all required outcomes, including relevant non-functional constraints.

The gate compares discovered IDs to state. If they differ, review the changed artifacts and record approval again. Approving documents does not refresh evidence. A latest failed record supersedes an earlier pass even at the same snapshot. Evidence sources are fingerprinted separately, including ignored report files, and must still exist unchanged.

Old state remains readable. Evidence recorded before source fingerprints were introduced cannot satisfy the strict gate: rerun/review the check and record fresh evidence. Historical `done` and checkbox marks never become passing evidence automatically.

Successful JSON verification states `kind: recorded_evidence_gate` and `executed_checks: false`. It means the recorded claims satisfy this gate, not that this command ran a test suite or proved real-world execution.

Git-backed snapshots cover tracked and nonignored untracked files, excluding feature-state files and the memory-state record. Ignored build/dependency files are not implementation inputs to this snapshot; evidence-source fingerprints separately cover the referenced report even if it is ignored. Reviewers must ensure all relevant implementation inputs are tracked.
