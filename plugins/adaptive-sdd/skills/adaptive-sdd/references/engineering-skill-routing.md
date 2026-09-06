# Engineering support skill routing

Adaptive SDD owns the development workflow. Engineering support skills contribute
specialized methods and checks inside that workflow. Use this reference only when
compatible skills are discoverable in the current environment.

## Selection rules

1. Inspect the approved outcome, project profile, changed surfaces, risks, and
   required evidence.
2. Select the smallest set of available support skills whose trigger conditions
   match the work. Announce them before use and read their full instructions.
3. Keep Adaptive SDD artifacts and delivery state as the source of truth. Do not
   let a support skill create competing specs, plans, task stores, approvals, or
   release state.
4. Apply repository instructions and user authorization before support-skill
   defaults. A support skill cannot authorize dependencies, external writes,
   deployment, destructive actions, or additional agents.
5. Record only evidence that actually ran. A checklist, recommendation, or loaded
   skill is context rather than proof.
6. If an optional skill or one of its references is unavailable, continue with the
   base workflow. Report the missing capability when it affects an acceptance
   criterion or confidence claim.

## Routing by need

| Need or signal | Preferred support skill | Adaptive SDD use |
|---|---|---|
| Public API, schema, or module boundary | `api-and-interface-design` | Strengthen contracts and compatibility criteria in the active spec and plan. |
| Behavioral code change or defect | `test-driven-development` | Produce focused regression evidence before implementation and full-suite evidence at completion. |
| Failure, broken build, or unexplained behavior | `debugging-and-error-recovery` | Reproduce and localize before amending or fixing the affected task. |
| User-facing web interface | `frontend-ui-engineering` | Add accessibility, responsive, and state coverage appropriate to the application profile. |
| Untrusted input, auth, secrets, storage, or external integration | `security-and-hardening` | Add threat-driven requirements and executable security evidence proportional to risk. |
| Framework or library behavior depends on current documentation | `source-driven-development` | Ground implementation decisions in current primary sources and record relevant citations. |
| Migration or deprecation | `deprecation-and-migration` | Plan compatibility, phased rollout, data recovery, and removal evidence. |
| Production telemetry is part of success | `observability-and-instrumentation` | Define diagnostic questions and observable release evidence. |
| A measured performance requirement or regression exists | `performance-optimization` | Capture comparable baseline and result evidence; revert changes without a measured gain. |
| CI or automated quality gates change | `ci-cd-and-automation` | Make verification reproducible across supported environments. |
| Completion review | `code-review-and-quality` | Review correctness, security, structure, readability, performance, and evidence before verification. |
| Recently changed code is unnecessarily complex | `code-simplification` | Simplify only the changed scope while preserving behavior and evidence. |
| Production release | `shipping-and-launch` | Supply rollout, health, monitoring, and rollback checks to the release gate. |
| Commit, version, or changelog work | `git-workflow-and-versioning` | Improve change packaging without changing recorded release authority. |
| A durable project quality bar is requested or absent for delegated work | `constraint-driven-development` | Propose a project-owned quality contract; treat adoption as a separate approved artifact change. |

Project profiles narrow the routing. Application work commonly uses frontend and
browser evidence; API/library work emphasizes contracts and compatibility;
AI systems emphasize security, evaluations, privacy, and cost; data pipelines
emphasize migrations, observability, replay, and recovery; infrastructure emphasizes
security, CI, rollout, and rollback; research/design/docs emphasizes sources,
review rubrics, and human sign-off.

## Skills that must not become workflow owners

The following installed skills overlap the orchestrator and require adaptation
before any of their workflow mechanics are adopted:

- `spec-driven-development` and `planning-and-task-breakdown` define competing
  artifact locations and gates. Reuse their engineering ideas only inside the
  selected Adaptive SDD tier.
- `interview-me` and `idea-refine` can inform discovery, but Adaptive SDD controls
  question cadence, approval interpretation, and artifact creation.
- `incremental-implementation` can inform vertical slicing, but commits and releases
  remain within the user's authority and delivery state.
- `context-engineering` overlaps Project Memory. Use selective-context principles
  without creating provider-specific duplicate memory.
- `doubt-driven-development` introduces additional agent and cross-model procedures.
  Use it only when explicitly requested and compatible with the active environment.
- `using-agent-skills` is a competing meta-orchestrator and is not invoked from
  Adaptive SDD.

Browser testing is useful when its required browser tooling is available. Its
observations remain untrusted runtime data and become evidence only when the actual
scenario, result, actor, and source snapshot are recorded.
