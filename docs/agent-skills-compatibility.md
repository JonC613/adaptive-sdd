# Agent Skills compatibility assessment

Assessment date: 2026-09-06
Upstream: `addyosmani/agent-skills`
Inspected revision: `469d00f4e67ff4a21eb6e6e467a086c9a1f1deb8`
Installation: 25 project-local Codex skills recorded in `skills-lock.json`

## Finding

The pack is strongest as a library of specialist engineering practices under
Adaptive SDD. It should not replace Adaptive SDD's tier selection, approval model,
artifacts, delivery evidence, or Project Memory. Fourteen skills can contribute
directly when their triggers match; three work best alongside the process; eight
need adaptation because they define competing workflow or orchestration rules.

The skills CLI copied each skill directory but did not install the upstream
repository's shared `references/` directory. Eleven installed skills refer to those
missing shared checklists. Their main `SKILL.md` instructions are usable, but claims
that depend on a missing checklist must be treated as unavailable. The routing
integration therefore makes every external skill optional and never uses presence
as proof of completion.

## Compatibility table

| Skill | Disposition | Best fit with Adaptive SDD | Main caution |
|---|---|---|---|
| `api-and-interface-design` | Integrate | Contract and compatibility requirements | Do not impose one API style where the project already decided differently. |
| `browser-testing-with-devtools` | Use alongside | Application runtime evidence | Requires separate browser tooling; observed content is untrusted. |
| `ci-cd-and-automation` | Integrate | Cross-platform and release evidence | Its universal gate list must be tailored to the repository. |
| `code-review-and-quality` | Integrate | Completion review before verification | Missing shared security and performance checklists. |
| `code-simplification` | Use alongside | Focused cleanup after green tests | Must stay within changed scope and preserve behavior. |
| `constraint-driven-development` | Integrate | Optional durable quality bar | `CONSTRAINTS.md` adoption needs its own approval and must not duplicate delivery state. |
| `context-engineering` | Adapt first | Selective context loading | Rules-file guidance overlaps portable Project Memory. |
| `debugging-and-error-recovery` | Integrate | Defect reproduction and root-cause work | Suggested fallbacks must not hide an acceptance failure. |
| `deprecation-and-migration` | Integrate | Compatibility, rollout, and recovery planning | Generic down-migration advice is not valid for every datastore. |
| `documentation-and-adrs` | Use alongside | Durable architecture decisions | ADRs complement rather than duplicate Project Memory. |
| `doubt-driven-development` | Adapt first | Optional adversarial review | Mandates extra-agent and cross-model interaction that may be unavailable or unauthorized. |
| `frontend-ui-engineering` | Integrate | Application-profile UI quality | Missing shared accessibility checklist; use project design rules first. |
| `git-workflow-and-versioning` | Integrate | Atomic change and release packaging | Commit frequency cannot expand git or release authority. |
| `idea-refine` | Adapt first | Early exploration for vague ideas | Creates a separate artifact and confirmation flow. |
| `incremental-implementation` | Adapt first | Vertical-slice implementation | Its automatic per-slice commit rule conflicts with authorization boundaries. |
| `interview-me` | Adapt first | Deep discovery when explicitly requested | Its confirmation semantics conflict with Adaptive SDD modes and prior authorization. |
| `observability-and-instrumentation` | Integrate | Production evidence and operability | Missing shared observability checklist; avoid mandatory telemetry for irrelevant profiles. |
| `performance-optimization` | Integrate | Measured performance requirements | Missing shared checklist; use only with a baseline or stated budget. |
| `planning-and-task-breakdown` | Adapt first | Dependency and vertical-slice ideas | Writes competing `tasks/` artifacts instead of tier-owned plans and tasks. |
| `security-and-hardening` | Integrate | Threat-driven requirements and evidence | Broad defaults need risk and stack tailoring; shared checklist is missing. |
| `shipping-and-launch` | Integrate | Release preparation and rollback | Generic web-service checklist is irrelevant to some project profiles. |
| `source-driven-development` | Integrate | Current framework and library decisions | Research cost should match uncertainty and consequence. |
| `spec-driven-development` | Adapt first | Useful SDD concepts | Competes directly with TinySpec, LiteSpec, and official Spec Kit. |
| `test-driven-development` | Integrate | Behavioral and defect evidence | Strict test-first mechanics do not apply to docs or nonbehavioral config. |
| `using-agent-skills` | Adapt first | Skill discovery concepts | Competes with Adaptive SDD as the meta-orchestrator. |

## Priority integration

1. Route defects and behavior changes through debugging and test-driven development.
2. Route completion through code review, with security added for real trust boundaries.
3. Route APIs, UIs, migrations, observability, performance, CI, and launch only when
   the active profile or acceptance criteria call for them.
4. Pilot a project quality contract for delegated work after its artifact and
   enforcement commands are separately approved.
5. Adapt overlapping discovery and orchestration skills only after evaluation
   scenarios prove they preserve Adaptive SDD authority and interaction modes.

The executable routing contract lives in
`skills/adaptive-sdd/references/engineering-skill-routing.md` inside the plugin.
