---
feature: <feature-slug>
artifact: plan
status: draft
owner: <owner>
version: 0.1
created: YYYY-MM-DD
updated: YYYY-MM-DD
spec_version: <approved-spec-version>
---

# Implementation Plan: <Feature name>

## Technical approach

<Describe the smallest coherent implementation strategy in one to three short paragraphs.>

## Key decisions

### KD-01 — <Decision title>

- **Choice:** <Selected approach>
- **Rationale:** <Why this fits the approved requirements and codebase>
- **Alternatives considered:** <Only credible alternatives>
- **Consequences:** <Tradeoffs, constraints, or follow-on effects>

## Impacted areas

| Area | Expected change | Related IDs |
|---|---|---|
| `<path, module, service, schema, or contract>` | <Impact> | US-01, AC-01.1 |

<!-- Include only when technical detail materially removes ambiguity. -->
## Technical detail

### Data model, interface, or state transition

<Add the minimum useful schema, interface, state transition, or diagram. Remove this section when unnecessary.>

<!-- Include only when meaningful risks were discovered. -->
## Risks and mitigations

| Risk | Impact | Mitigation | Evidence or trigger |
|---|---|---|---|
| <Risk> | <Impact> | <Mitigation> | <How it will be detected> |

## Implementation phases

### Phase 1 — <Verifiable outcome>

- [ ] **P1-T1 — <Task outcome>**
  - Covers: US-01, AC-01.1
  - Depends on: None
  - Work: <Bounded implementation actions>
  - Verify: <Specific evidence that completes the task>

- [ ] **P1-T2 — <Task outcome>**
  - Covers: AC-01.2
  - Depends on: P1-T1
  - Work: <Bounded implementation actions>
  - Verify: <Specific evidence that completes the task>

### Phase 2 — <Verifiable outcome>

- [ ] **P2-T1 — <Task outcome>**
  - Covers: <IDs>
  - Depends on: <Task IDs or None>
  - Work: <Bounded implementation actions>
  - Verify: <Specific evidence>

<!-- Include when deployed state or external consumers make release behavior relevant. -->
## Release and rollback considerations

- **Release:** <Relevant rollout sequence or compatibility condition>
- **Rollback:** <Safe reversal or recovery approach>

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | YYYY-MM-DD | Initial draft | Derived from approved specification | All |
