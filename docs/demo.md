# Five-minute demo script

This is a presenter script, not a recording. Run from a local clone. Prerequisites and the browser environment are in the [README](../README.md).

## 0:00 — State the problem

“Small changes need clear intent without a large planning process. Larger changes need explicit behavior, decisions, and evidence. Adaptive-SDD helps choose that depth.”

Show the three-tier table in the README. Explain that agent guidance recommends the tier; Python does not classify requests.

## 0:45 — Follow one request

Use: “Create a habit tracker with daily check-ins, calendar history, and local persistence.”

Open the [Daymark specification](../.litespec/habit-tracker-example/spec.md). Show `AC-01.1` and `AC-04.1`, then the [plan](../.litespec/habit-tracker-example/plan.md) and [test plan](../.litespec/habit-tracker-example/tests.md). Multiple user journeys and persistence decisions explain LiteSpec. For a smaller contrast, show the [one-file Kanban specification](../plugins/adaptive-sdd/examples/simple-kanban/tiny/simple-kanban.md).

## 1:45 — Exercise the implementation

Open `plugins/adaptive-sdd/examples/habit-tracker/index.html` locally. Add “Read a page”, mark it complete, view calendar history, and reload. Explain that data stays in this browser. This walkthrough observes those actions only; it is not full acceptance or accessibility testing.

## 2:45 — Run actual checks

After `npm ci` and `npx playwright install chromium`, on Windows:

```text
npm test
npm run test:e2e
```

Expect five Node tests and five browser tests. Show the HTML report at `playwright-report/index.html` after execution. On a failure, inspect the report rather than updating baselines. Do not describe this script's expected results as a completed run.

Then contrast document validation:

```text
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/validate_litespec.py .litespec/habit-tracker-example --json
```

“This checks structure and traceability, not whether the app works.”

## 4:00 — Demonstrate a verification failure

Run the isolated regression that creates a heading-only specification, initializes delivery state, records approval, and asserts that verification fails:

```text
python -m unittest discover -s plugins/adaptive-sdd/tests -p test_delivery_state.py -v
```

Open `test_empty_criteria_cannot_verify` in [the test source](../plugins/adaptive-sdd/tests/test_delivery_state.py). Show the expected diagnostic: `no meaningful acceptance criteria discovered`. The same suite exercises valid specifications, missing evidence, stale evidence, and the distinction between a recorded passing command and execution.

## 4:45 — Close with limits

“Strict tracking is optional. Deterministic tests do not measure how consistently a live agent chooses tiers or finds requirements. Those measurements and live upstream compatibility checks remain future work.”

Link the [case study](case-study.md), [evaluation protocol](../plugins/adaptive-sdd/evals/README.md), and [release checklist](release-readiness.md).
