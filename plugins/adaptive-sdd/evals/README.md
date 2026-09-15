# Evaluating Adaptive-SDD

## Deterministic regression report

```text
python plugins/adaptive-sdd/evals/evaluate.py --json
```

The evaluator runs the Python suite with `unittest` and records runner events by exact, fully qualified test ID. It does not parse console names or call a model. JSON goes to stdout; the test log goes to stderr.

Each scenario is **passed**, **failed**, **skipped**, or **not_evaluated**. Missing tests and tests prevented from running by class setup errors are not evaluated. Dependency skips and expected failures do not count as passing scenarios. Failed subtests, errors, and unexpected successes are failures. A fixture's class setup failure also makes the overall suite unsuccessful.

`scenario_count` counts configured scenarios. `unique_test_count` counts distinct referenced tests, including missing ones. `suite_tests_run` reports the runner's execution count; suite outcome entries can also include setup/teardown errors. Several scenarios can reference one regression test; they are not independent experiments. `passed` requires a successful suite and every configured scenario passing. Exit status is nonzero when that condition is not met, including a skipped configured scenario.

Schema version 2 replaces the old inferred `metrics` object with per-scenario records and an empty `measurements` list. `checks` in scenarios.json describes the intent of a regression, not a measured rate. `live_agent_evaluated` remains false. The Python suite and this reporter have their own [regression tests](../tests/test_evaluation.py).

The installer backup scenario runs real PowerShell file operations in temporary directories when PowerShell is available. The separate combined-installer test deliberately substitutes `uv` and `specify`; that is a control-flow fixture, not a live upstream installation.

## Optional live-agent evaluation protocol — not yet run

Provider calls require explicit opt-in and a cost budget. No paid calls are made by the deterministic evaluator or CI. No benchmark result is claimed.

1. Build a versioned, sanitized request set spanning small fixes, multiple user journeys, ambiguous requirements, external integrations, and consequential migrations. Keep development prompts separate from a held-out set.
2. Have two reviewers independently label acceptable tiers (including reasonable alternatives), genuinely blocking ambiguities, required outcomes, and the checks needed for completion. Resolve disagreement and retain the rubric.
3. Run a pinned model/tool configuration in isolated repositories with a fixed time/token budget and repeat count. Record model version, prompt/skill commit, fixtures, tool access, transcripts, actual commands, costs, failures, and incomplete runs.
4. Compare Adaptive-SDD with a stated baseline under the same conditions, such as the same agent without this guidance. Do not equate different fixture difficulty or budgets with workflow improvement.
5. Score the following from transcripts and independently observed artifacts and execution:

| Measurement | Numerator / denominator | Ground truth |
|---|---|---|
| Tier selection | Recommendations within the acceptable tier set / runs with a scored recommendation | Predeclared tier rubric; report missing recommendations separately |
| Unnecessary clarification | Questions reviewers judge answerable from supplied context or irrelevant to an in-scope decision / all clarification questions | Blinded transcript review; also report per-run counts, including zero-question runs |
| Missed requirements | Required outcomes absent or incorrect / all required outcomes assessed | Per-outcome implementation inspection and independent checks |
| Verification accuracy | Unsupported completion claims / all completion claims assessed; also report missed failures and true/false positives/negatives | Independently run checks against the exact claimed artifact snapshot |

6. Publish raw counts, denominators, skipped/unscorable/incomplete runs and reasons, reviewer agreement, uncertainty intervals, and repeat variability. Report zero only when an actual measured numerator is zero; use not evaluated when no measurement exists.

These measurements would evaluate behavior on that request set. They would not by themselves establish workplace productivity or production reliability.
