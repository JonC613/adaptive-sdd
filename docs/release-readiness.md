# Release-readiness checklist

No release is published by this checklist. Current manifests remain **0.4.1**; pending changes belong under **Unreleased** until a release is intentionally prepared.

## Evidence to collect for a release candidate

- [ ] Review the candidate commit and actual [CI run](https://github.com/JonC613/adaptive-sdd/actions/workflows/test.yml): Python matrix, JavaScript, Windows Chromium, and repository checks.
- [ ] Record test counts, failures, skips, OS/runtime versions, and the commit tested. Do not copy expected outcomes as results.
- [ ] Review Playwright report and any trace/screenshot failures. Never regenerate baselines just to pass CI; intentional changes need image review on the documented Windows environment.
- [ ] Run the deterministic evaluator; inspect each scenario's status and the unique-test count. There are no live-agent measurements unless a separately approved evaluation ran.
- [ ] Run doctor on each intended installation environment. A missing dependency should produce a failed diagnostic; a skipped integration test supplies no compatibility evidence.
- [ ] Exercise a real shared-skill installation in a disposable target and verify discovery in fresh Codex and Cursor tasks.
- [ ] Separately run the pinned Spec Kit installation in a disposable clean repository; record `specify version`, expected generated files, and the actual commands/results. Mocked `uv`/`specify` tests do not fulfill this item.
- [ ] Review supported delivery formats and migration notes. Old evidence without a source fingerprint requires a fresh check and recording; do not fabricate a migration pass.
- [ ] Run `python scripts/check_repository.py` for local documentation targets and packaging/version consistency. External links and hosted services require separate review.
- [x] Owner selected Apache-2.0; root [LICENSE](../LICENSE) and [NOTICE](../NOTICE) record the grant and attribution.
- [ ] When authorized to prepare a version, synchronize both plugin manifests, changelog, README, and version assertions; review marketplace layout and installed payload.
- [ ] Keep evidence limitations accurate; exclude employer, customer, and proprietary details.
- [ ] Obtain explicit release authorization after the above evidence is reviewable.

## Remaining application-readiness considerations

The portfolio can show implementation and test evidence today. Live agent-quality measurements, fresh marketplace activation checks, and live Spec Kit installation evidence remain outstanding. No adoption, productivity gain, or production maturity is established.
