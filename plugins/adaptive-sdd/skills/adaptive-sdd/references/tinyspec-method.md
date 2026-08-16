# TinySpec method

TinySpec is a one-file contract for small, clear changes.

## Artifact contract

Store one artifact at `.tinyspec/<feature>.md`. Keep it concise and include:

- Summary and desired outcome
- Current scope and explicit exclusions
- Observable requirements
- Relevant constraints and assumptions
- Implementation outline
- Verification and completion conditions
- Amendment history

Use stable `R-*` requirement IDs when there is more than one requirement. Avoid full user-story ceremony unless it materially improves clarity; move to LiteSpec when stories and traceability become necessary.

## Lifecycle

Use `draft → review → approved → implementing → done`. Approval of the artifact does not authorize implementation.

## Size control

Prefer one to three short paragraphs and compact lists. If the artifact needs multiple detailed journeys, a separate implementation plan, or an acceptance traceability matrix, recommend LiteSpec.

## Validation

Run `validate_tinyspec.py`. Validation checks structure and metadata but never grants approval.
