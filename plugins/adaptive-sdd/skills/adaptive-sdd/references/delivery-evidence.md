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
