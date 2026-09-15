# Case study: proportionate specification for AI-assisted development

## Problem and contribution

AI-generated code can look complete while missing behavior, edge cases, or evidence. At the other extreme, applying a full planning lifecycle to every small change creates overhead that discourages consistent use.

I created Adaptive-SDD to make specification depth a deliberate engineering decision. I built TinySpec and LiteSpec guidance, a shared Codex/Cursor workflow, an adapter to official GitHub Spec Kit, structural validators, guarded installers, portable Project Memory, and optional delivery-state tracking. The upstream Spec Kit workflow remains separately maintained.

## Decisions and tradeoffs

- **Use the smallest adequate tier.** Scope, uncertainty, and the consequences of a mistake drive the recommendation. Agent judgment keeps the workflow adaptable, but its consistency needs evaluation; there is no numeric classifier or measured selection accuracy.
- **Keep specifications portable.** Markdown and a shared skill make requirements inspectable across tools. Deterministic validators support a defined syntax rather than interpreting arbitrary prose.
- **Separate intent, evidence, and execution.** Approval records intent; validators check structure; the optional delivery gate checks recorded evidence against the current files. It cannot prove that a reported command actually ran. Strict snapshots favor detecting stale evidence, at the cost of requiring checks to be repeated after unrelated file changes.
- **Keep lightweight work lightweight.** TinySpec does not need task IDs. Strict tracking is opt-in. Larger changes gain traceability without forcing every project through the full upstream lifecycle.
- **Maintain upstream boundaries.** A version pin makes the Spec Kit dependency explicit. Mocked command tests are useful for installer control flow but do not replace live integration checks.

## Example: Daymark

The request is a habit tracker with daily check-ins, calendar history, and browser-local persistence. Its multiple user journeys fit LiteSpec.

| Step | Repository evidence |
|---|---|
| Define behavior | [Specification](../.litespec/habit-tracker-example/spec.md): adding a habit (`AC-01.1`), saving progress across reloads (`AC-04.1`) |
| Plan implementation | [Plan](../.litespec/habit-tracker-example/plan.md): state operations, storage, daily list, calendar, and checks |
| Build | [Application code](../plugins/adaptive-sdd/examples/habit-tracker/app.js): state functions and browser UI |
| Check | [Node tests](../plugins/adaptive-sdd/examples/habit-tracker/app.test.mjs), [Playwright scenarios](../tests/e2e/daymark.spec.mjs), and [manual test plan](../.litespec/habit-tracker-example/tests.md) |

The browser example can be opened locally without a server. Automated checks exercise behavior; Markdown traceability alone is not evidence that every requirement passed. The [demo script](demo.md) shows how to inspect and run the example.

A correctness review also exposed an empty-set bug: a heading-only specification could be approved and marked verified because there were no criteria to fail. The gate now validates the supported structure, requires meaningful criteria, and checks current passing evidence for each discovered criterion. [Regression coverage](../plugins/adaptive-sdd/tests/test_delivery_state.py) includes empty criteria, valid minimal formats, missing and stale evidence, and a later failure superseding a pass.

## Current limits

The repository does not establish deployment, measured productivity gains, or production maturity. Employer, customer, and proprietary project details are intentionally absent.

## What this demonstrates

The repository demonstrates workflow design for AI-assisted development, provider-neutral guidance, executable validation, traceability, regression testing, and a clear distinction between recorded claims and observed execution. It also demonstrates a willingness to test failure paths and constrain claims when evidence is missing.

It does not yet establish live-agent tier-selection accuracy, reduced clarification overhead, fewer missed requirements, productivity gains, broad marketplace compatibility, or readiness for regulated production use. The [evaluation protocol](../plugins/adaptive-sdd/evals/README.md) describes how those questions could be tested. Licensing and fresh upstream compatibility evidence remain on the [release checklist](release-readiness.md).
