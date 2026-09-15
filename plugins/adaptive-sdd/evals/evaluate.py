#!/usr/bin/env python3
"""Report deterministic regression outcomes; no provider calls or inferred metrics."""
import argparse
from collections import Counter
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys
import unittest


class ScenarioResult(unittest.TextTestResult):
    """Capture runner events, including skips and failed subtests, by exact test ID."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = {}

    def startTest(self, test):
        super().startTest(test)
        self.outcomes[test.id()] = {"status": "not_evaluated", "reason": "test did not complete"}

    def addSuccess(self, test):
        super().addSuccess(test)
        if self.outcomes[test.id()]["status"] == "not_evaluated":
            self.outcomes[test.id()] = {"status": "passed"}

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.outcomes[test.id()] = {"status": "failed", "reason": str(err[1])}

    def addError(self, test, err):
        super().addError(test, err)
        self.outcomes[test.id()] = {"status": "failed", "reason": str(err[1])}

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        parent = getattr(test, 'test_case', test)
        if self.outcomes.get(parent.id(), {}).get('status') != 'failed':
            self.outcomes[parent.id()] = {"status": "skipped", "reason": reason}

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.outcomes[test.id()] = {"status": "skipped", "reason": "expected failure; does not establish a passing outcome"}

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.outcomes[test.id()] = {"status": "failed", "reason": "unexpected success"}

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.outcomes[test.id()] = {"status": "failed", "reason": str(err[1])}


def build_report(scenarios, result):
    rows = [{"id": s["id"], "test": s["test"], **result.outcomes.get(
        s["test"], {"status": "not_evaluated", "reason": "exact test ID was not run"}
    )} for s in scenarios]
    counts = Counter(row["status"] for row in rows)
    return {
        "schema_version": 2,
        "passed": bool(rows) and result.wasSuccessful() and all(row["status"] == "passed" for row in rows),
        "scenario_count": len(rows),
        "unique_test_count": len({s["test"] for s in scenarios}),
        "suite_tests_run": result.testsRun,
        "suite_successful": result.wasSuccessful(),
        "suite_counts": dict(Counter(row["status"] for row in result.outcomes.values())),
        "scenario_counts": {status: counts[status] for status in ("passed", "failed", "skipped", "not_evaluated")},
        "scenarios": rows,
        "measurements": [],
        "live_agent_evaluated": False,
        "limitations": ["Deterministic fixtures do not measure live-agent quality or upstream integration performance.",
                        "Multiple scenarios can reference one test; these are not independent trials."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    root = args.plugin.resolve()
    config = json.loads((root / 'evals/scenarios.json').read_text(encoding='utf-8'))
    suite = unittest.defaultTestLoader.discover(str(root / 'tests'))
    with redirect_stdout(sys.stderr):
        result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2, resultclass=ScenarioResult).run(suite)
    report = build_report(config['deterministic'], result)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['scenario_count']} scenarios / {report['unique_test_count']} unique referenced tests")
        for row in report['scenarios']:
            print(f"{row['status'].upper()}: {row['id']} ({row['test']})" + (f": {row['reason']}" if 'reason' in row else ''))
        print('No live-agent measurements; see evals/README.md.')
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
