# Contributing

Keep the shared workflow provider-neutral and dependency-light. Add a deterministic regression for safety or validation changes. Do not describe structural checks, mocks, or unrun CI as execution evidence. Preserve compatibility fixtures unless a documented migration replaces them.

## Local checks

From the repository root, with Python 3.11+, Git, and Node 22.14.0:

```text
python -m unittest discover -s plugins/adaptive-sdd/tests -v
python plugins/adaptive-sdd/evals/evaluate.py --json
python plugins/adaptive-sdd/skills/adaptive-sdd/scripts/doctor.py --plugin plugins/adaptive-sdd
python scripts/check_repository.py
npm test
npm ci
npx playwright install chromium
npm run test:e2e
```

The evaluator reruns the Python suite to produce exact per-scenario results. For routine iteration, run the relevant tests first and use the evaluator when a scenario report is needed. Skipped configured scenarios make that report incomplete and return a nonzero exit status; inspect reasons rather than assuming failure of product behavior.

Doctor reports the actual host. Its behavioral tests mock available/missing dependencies and supported/unsupported Python. Installer tests use real PowerShell file operations in isolated temporary directories when available; dependency or symlink limitations are explicit skips. `test_combined_installer_checks_clean_tree_before_copy` mocks `uv` and `specify` and does not prove live Spec Kit compatibility. A real upstream install is a separate release-readiness check.

The browser suite uses Windows screenshot baselines. CI selects Windows Server 2022, pinned Node 22.14.0 and Playwright 1.63.0's bundled Chromium. Hosted runner images still receive updates, so font/rendering changes require investigation. Other OS baselines have not been established. See [browser QA](docs/qa/daymark-e2e.md) for reproduction and baseline review.

CI runs Python on Linux/macOS/Windows with Python 3.11 and 3.13, Node unit tests on Linux, browser tests on Windows, and offline repository link/packaging checks. Reports/traces/failure screenshots are uploaded by the browser job. Local Markdown targets are checked; external URLs and anchors are not checked by the offline script.

## Changes and releases

Use a feature branch. Pull requests default to the `origin` repository; verify the head and base repository/branch before creating one. Keep releases separate from routine fixes. Record unreleased changes in the changelog without bumping manifests speculatively.

Adaptive SDD is licensed under [Apache License 2.0](LICENSE). By submitting a
contribution, you license that contribution under Apache-2.0 unless you state
different terms in writing before it is accepted. See the
[release checklist](docs/release-readiness.md).
