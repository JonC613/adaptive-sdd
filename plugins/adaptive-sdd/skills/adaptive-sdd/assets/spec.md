---
feature: <feature-slug>
artifact: spec
status: draft
owner: <owner>
version: 0.1
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Specification: <Feature name>

## Summary

<Describe the feature and its value in one short paragraph.>

## Problem

<Describe the current limitation or unmet need without prescribing implementation.>

## Desired outcome

<Describe what successful delivery changes for users or stakeholders.>

<!-- Include the next section when boundaries are ambiguous or scope drift is plausible. -->
## Boundaries

### Goals

- <Goal>

### Non-goals

- <Explicit exclusion>

### Constraints

- <Technical, business, regulatory, schedule, or compatibility constraint>

## Requirements

### Current release

- **R-01:** <Required behavior or capability>

### Deferred

- **D-01:** <Explicitly deferred capability and, when useful, why>

## User stories

### US-01 — <Behavioral title>

**Story:** As a <role>, I want <capability>, so that <value>.

**Rationale:** <Explain why this story matters.>

**Acceptance criteria:**

- **AC-01.1:** <Observable, verifiable outcome.>
- **AC-01.2:** Given <context>, when <event>, then <outcome>.

**Edge cases:**

- <Boundary, invalid input, failure, empty state, or recovery behavior>

## Non-functional requirements

<!-- Include measurable expectations only. Use "None identified" when genuinely absent. -->

- **NFR-01 — <Quality>:** <Measurable accessibility, performance, security, privacy, reliability, or compatibility expectation>

## Codebase context

<Summarize architecture, conventions, tests, dependencies, and relevant implementation surfaces discovered through repository assessment. Do not reproduce general repository documentation.>

<!-- Add sourced findings beside the affected requirement when external research is necessary. -->
## Assumptions and open questions

### Assumptions

- **A-01:** <Low-risk assumption and its impact if false>

### Open questions

- None.

<!-- High-impact open questions must be resolved before approval. -->
## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | YYYY-MM-DD | Initial draft | Initial discovery | All |
