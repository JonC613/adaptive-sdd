"""Exercise reporting with real unittest events, without model calls."""
import importlib.util
import io
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('evaluate', Path(__file__).resolve().parents[1] / 'evals/evaluate.py')
evaluate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluate)


class EvaluationTests(unittest.TestCase):
    def run_fixture(self, case):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(case)
        return unittest.TextTestRunner(stream=io.StringIO(), resultclass=evaluate.ScenarioResult).run(suite)

    def test_exact_results_and_scenario_vs_unique_test_counts(self):
        class Fixture(unittest.TestCase):
            def test_pass(self):
                pass

            @unittest.skip('dependency unavailable')
            def test_skip(self):
                pass

            def test_fail(self):
                self.fail('actual failure')

        result = self.run_fixture(Fixture)
        scenarios = [{'id': name, 'test': Fixture(method).id()} for name, method in
                     [('pass', 'test_pass'), ('same-test', 'test_pass'), ('skip', 'test_skip'), ('fail', 'test_fail')]]
        scenarios.append({'id': 'missing', 'test': 'another.module.test_pass'})
        report = evaluate.build_report(scenarios, result)
        self.assertEqual(report['scenario_count'], 5)
        self.assertEqual(report['unique_test_count'], 4)
        self.assertEqual(report['suite_tests_run'], 3)
        self.assertEqual(report['scenario_counts'], {'passed': 2, 'failed': 1, 'skipped': 1, 'not_evaluated': 1})
        self.assertEqual(report['scenarios'][2]['reason'], 'dependency unavailable')
        self.assertFalse(report['passed'])
        self.assertEqual(report['measurements'], [])
        self.assertFalse(report['live_agent_evaluated'])

    def test_skipped_scenario_does_not_pass_even_when_suite_successful(self):
        class Fixture(unittest.TestCase):
            @unittest.skip('PowerShell missing')
            def test_install(self):
                pass

        result = self.run_fixture(Fixture)
        report = evaluate.build_report([{'id': 'install', 'test': Fixture('test_install').id()}], result)
        self.assertTrue(report['suite_successful'])
        self.assertFalse(report['passed'])
        self.assertEqual(report['scenarios'][0]['status'], 'skipped')

    def test_subtest_errors_and_expected_failures_are_not_passes(self):
        class Fixture(unittest.TestCase):
            def test_subtest(self):
                for value in [1, 2]:
                    with self.subTest(value=value):
                        self.assertEqual(value, 1)

            def test_error(self):
                raise ValueError('fixture error')

            @unittest.expectedFailure
            def test_expected(self):
                self.fail('known failure')

            @unittest.expectedFailure
            def test_unexpected(self):
                pass

        result = self.run_fixture(Fixture)
        expected = {'test_subtest': 'failed', 'test_error': 'failed', 'test_expected': 'skipped', 'test_unexpected': 'failed'}
        for method, status in expected.items():
            self.assertEqual(result.outcomes[Fixture(method).id()]['status'], status)

    def test_setup_class_failure_leaves_scenario_not_evaluated(self):
        class Fixture(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                raise RuntimeError('setup failed')

            def test_never_runs(self):
                pass

        result = self.run_fixture(Fixture)
        report = evaluate.build_report([{'id': 'setup', 'test': Fixture('test_never_runs').id()}], result)
        self.assertFalse(report['passed'])
        self.assertEqual(report['scenarios'][0]['status'], 'not_evaluated')

    def test_skipped_subtest_does_not_become_parent_success(self):
        class Fixture(unittest.TestCase):
            def test_partial(self):
                with self.subTest(dependency='missing'):
                    self.skipTest('dependency unavailable')
                with self.subTest(dependency='available'):
                    self.assertTrue(True)

            def test_failure_then_skip(self):
                with self.subTest(case='failure'):
                    self.fail('failure must remain visible')
                with self.subTest(case='skip'):
                    self.skipTest('skip must not hide failure')

        result = self.run_fixture(Fixture)
        self.assertEqual(result.outcomes[Fixture('test_partial').id()]['status'], 'skipped')
        self.assertEqual(result.outcomes[Fixture('test_failure_then_skip').id()]['status'], 'failed')
