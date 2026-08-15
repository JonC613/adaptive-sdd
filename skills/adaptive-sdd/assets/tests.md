---
feature: <feature-slug>
artifact: tests
status: draft
owner: <owner>
version: 0.1
created: YYYY-MM-DD
updated: YYYY-MM-DD
spec_version: <approved-spec-version>
plan_version: <approved-plan-version>
---

# Test Plan: <Feature name>

## Strategy

<Describe the smallest balanced set of unit, component, integration, or end-to-end checks that proves the critical behavior. Explain why the selected levels are sufficient.>

## Acceptance traceability

| Acceptance criterion | Test IDs | Method | Status |
|---|---|---|---|
| AC-01.1 | T-01 | Automated | Planned |
| AC-01.2 | T-02 | Automated | Planned |

Every current-release acceptance criterion must appear exactly once in this table and map to at least one test or documented manual exception.

## Critical user flows

### T-01 — <Successful behavior>

- Covers: AC-01.1
- Level: unit | component | integration | end-to-end
- Setup: <Required state, fixture, account, or environment>
- Action: <User or system trigger>
- Expected: <Observable result>

## Failure and recovery cases

### T-02 — <Failure or recovery behavior>

- Covers: AC-01.2
- Level: unit | component | integration | end-to-end
- Setup: <Required failure state or boundary>
- Action: <Trigger>
- Expected: <Safe failure, feedback, and recovery behavior>

## Manual exceptions

<!-- Remove the example and write "None" when all criteria are automated. -->

### M-01 — <Criterion or quality check>

- Covers: <Acceptance or NFR ID>
- Automation limitation: <Why reliable automation is unsuitable>
- Method: <Repeatable manual procedure>
- Expected evidence: <Screenshot, report, observation, or sign-off>

## Test data and setup

- <Fixture, browser state, service double, test account, environment variable, or cleanup requirement>

## Completion criteria

- [ ] Every current-release acceptance criterion maps to passing evidence.
- [ ] Critical user flows pass.
- [ ] Relevant failure and recovery cases pass.
- [ ] Manual exceptions, if any, have recorded evidence.
- [ ] No unresolved failure blocks an approved story or non-functional requirement.

## Amendment history

| Version | Date | Change | Reason | Affected IDs |
|---|---|---|---|---|
| 0.1 | YYYY-MM-DD | Initial draft | Derived from approved specification and plan | All |
