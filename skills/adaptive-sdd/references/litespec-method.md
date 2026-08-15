# LiteSpec method reference

## Contents

1. Tier contract
2. Artifact contracts
3. Writing rules
4. Metadata and lifecycle
5. Priority and versioning
6. Quality checks
7. Research foundations

## 1. Tier contract

LiteSpec occupies the middle tier between TinySpec and full Spec Kit:

| Tier | Artifacts | Use |
|---|---:|---|
| TinySpec | 1 | Behavior and implementation path are already clear |
| LiteSpec | 3 | TinySpec no longer creates enough shared understanding |
| Full Spec Kit | Full workflow | LiteSpec becomes insufficient |

Do not use mandatory scores or automatic thresholds. Explain a project-specific rationale and get user confirmation before changing tiers.

## 2. Artifact contracts

### `spec.md`

Answer: **What must be true, for whom, and why?**

Required core:

- Summary
- Problem
- Desired outcome
- Current-release and deferred requirements
- User stories with rationale, acceptance criteria, and edge cases
- Non-functional requirements
- Codebase context
- Assumptions and open questions
- Amendment history

Conditional sections:

- Goals, non-goals, and constraints when boundaries are ambiguous.
- Inline research findings when external facts are required.
- Detailed quality categories only when relevant.

Story form:

```markdown
### US-01 — <behavioral title>

**Story:** As a <role>, I want <capability>, so that <value>.
**Rationale:** <why it matters>

**Acceptance criteria:**
- **AC-01.1:** <observable result>
- **AC-01.2:** Given <context>, when <event>, then <outcome>.

**Edge cases:**
- <boundary or failure behavior>
```

### `plan.md`

Answer: **How will approved intent be implemented safely?**

Required core:

- Technical approach
- Key decisions and rationale
- Impacted areas
- Implementation phases
- Tasks with dependencies, linked IDs, and verification
- Amendment history

Conditional sections:

- Interfaces, data models, state transitions, migrations, or diagrams only when they remove ambiguity.
- Risks and mitigations only when meaningful risks exist.
- Release and rollback notes only when deployed state or external consumers are affected.

Task form:

```markdown
- [ ] **P1-T1 — <task outcome>**
  - Covers: US-01, AC-01.1
  - Depends on: None
  - Work: <bounded actions>
  - Verify: <completion evidence>
```

Use independently verifiable tasks for risky work. Routine work may remain grouped.

### `tests.md`

Answer: **What evidence proves approved behavior works?**

Required core:

- Strategy
- Acceptance traceability
- Critical user flows
- Failure and recovery cases
- Automated checks
- Manual exceptions
- Test data and setup
- Completion criteria
- Amendment history

Test form:

```markdown
### T-01 — <behavior>

- Covers: AC-01.1
- Level: unit | component | integration | end-to-end
- Setup: <state>
- Action: <trigger>
- Expected: <observable result>
```

Every current-release acceptance criterion maps to automated evidence. Permit a manual exception only with a specific automation limitation, repeatable method, and expected evidence.

## 3. Writing rules

### User stories

- Express stakeholder value, not UI inventory or technical components.
- Keep one independently understandable behavior per story.
- Include rationale and relevant edge cases.
- Use stable `US-<sequence>` IDs.

### Acceptance criteria

- Use stable `AC-<story>.<sequence>` IDs.
- Describe observable outcomes, not internals.
- Prefer one behavioral assertion per criterion.
- Use a concise checklist by default.
- Use Given/When/Then for meaningful preconditions, branching, or recovery.
- Avoid speculative permutations.

### Codebase context

- Inspect architecture, conventions, relevant behavior, tests, dependencies, and deployment surfaces.
- Summarize only facts that constrain or inform the feature.
- Do not reproduce general repository documentation.

### Size controls

- Keep summary, problem, outcome, and approach to one to three short paragraphs each.
- Include only acceptance conditions needed to accept a story.
- Record only decisions a future implementer could reasonably revisit.
- Make every phase produce a demonstrable or verifiable outcome.
- Map IDs in traceability tables rather than repeating requirements.
- If sections repeatedly exceed these bounds, reassess the tier with the user.

## 4. Metadata and lifecycle

Each artifact starts with:

```yaml
---
feature: feature-slug
artifact: spec
status: draft
owner: user
version: 0.1
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Lifecycle:

```text
draft → review → approved → implementing → done
```

Each artifact has its own status. Never infer approval from silence or approval of another artifact.

## 5. Priority and versioning

Use two requirement priorities:

- **Current release:** required for approved implementation.
- **Deferred:** retained but excluded from current tasks and required tests.

Compatible approved amendments increment `1.0` to `1.1`. Scope invalidation triggers a recommendation to review under full Spec Kit. Record version, date, change, reason, and affected IDs in each changed artifact.

## 6. Quality checks

### Specification

- Stories express value.
- Current-release stories have stable IDs, rationale, acceptance criteria, and relevant edge cases.
- Acceptance criteria are observable and testable.
- Deferred work is separate.
- Non-functional requirements are measurable or explicitly absent.
- High-impact questions are resolved.
- Codebase claims come from inspection.

### Plan

- Tasks map to approved intent.
- Dependencies and verification are explicit.
- Technical detail removes real ambiguity.
- Decisions include rationale and consequences.
- Deferred work is not implemented accidentally.

### Tests

- Every acceptance criterion maps to evidence.
- Critical flows and relevant failure paths are covered.
- Tests are placed at the lowest practical level.
- Manual exceptions include rationale, method, and evidence.
- Completion criteria are objective.

### Cross-artifact

- IDs are unique and stable.
- Links resolve in both directions.
- Versions and statuses are coherent.
- Amendments appear in all affected artifacts.
- No requirement, task, or test is orphaned.

## 7. Research foundations

LiteSpec adapts established practices without reproducing their full ceremony:

- GitHub Spec Kit: phased Markdown artifacts and approval gates — https://github.github.com/spec-kit/ and https://github.github.com/spec-kit/reference/workflows.html
- Agile Alliance user stories: value increments and evolving detail — https://agilealliance.org/glossary/user-stories/
- Cucumber Gherkin: observable examples and Given/When/Then — https://cucumber.io/docs/gherkin/reference/
- Requirements traceability: linking requirements through design, development, and tests — https://www.digitalpolicy.gov.hk/en/our_work/digital_infrastructure/methodology/system_development/doc/G61a_Effective_SAnD_Guide_Appendix_A_v1_2.pdf
- Lightweight decision records: context, decisions, and consequences in source control — https://ddt.beta.education.gov.uk/guides/architecture-documentation
- Test Pyramid: prefer the lowest practical test layer and a balanced portfolio — https://martinfowler.com/bliki/TestPyramid.html
- Semantic Versioning: meaning-bearing version increments, adapted here to specification amendments — https://semver.org/
