import contextlib, importlib.util, io, json, subprocess, sys, unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DistributionTests(unittest.TestCase):
    def test_profile_examples(self):
        expected = {'application.md','api-library.md','ai-system.md','data-pipeline.md','infrastructure.md','research-design-docs.md'}
        actual = {p.name for p in (ROOT / 'examples/profiles').glob('*.md')}
        self.assertEqual(actual, expected)
        for name in expected:
            text = (ROOT / 'examples/profiles' / name).read_text(encoding='utf-8')
            self.assertIn('Outcome:', text); self.assertIn('Evidence:', text)

    def test_doctor_machine_output(self):
        result = subprocess.run([sys.executable, str(ROOT / 'skills/adaptive-sdd/scripts/doctor.py'), '--plugin', str(ROOT), '--json'], capture_output=True, text=True)
        report = json.loads(result.stdout)
        self.assertEqual(report['ok'], all(c['ok'] for c in report['checks']))
        self.assertEqual(result.returncode, 0 if report['ok'] else 1)
        self.assertIn('0.4.1', next(c['message'] for c in report['checks'] if c['code'] == 'VERSION_SYNC'))

    def test_distribution_guidance_is_present(self):
        repo = ROOT.parents[1]
        for name in ('CHANGELOG.md','CONTRIBUTING.md','SECURITY.md'):
            self.assertTrue((repo / name).is_file())
        self.assertIn('security boundary', (ROOT / 'skills/adaptive-sdd/references/delivery-evidence.md').read_text().lower())

    def test_doctor_available_missing_and_unsupported_dependencies(self):
        spec = importlib.util.spec_from_file_location('doctor', ROOT / 'skills/adaptive-sdd/scripts/doctor.py')
        doctor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doctor)
        for version, available, expected in [((3, 11), True, True), ((3, 13), True, True),
                                              ((3, 10), True, False), ((3, 11), False, False)]:
            with self.subTest(version=version, available=available):
                output = io.StringIO()
                with patch.object(sys, 'argv', ['doctor', '--plugin', str(ROOT), '--json']), \
                     patch.object(doctor.sys, 'version_info', version), \
                     patch.object(doctor.shutil, 'which', return_value='/fixture/tool' if available else None), \
                     contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as exited:
                    doctor.main()
                report = json.loads(output.getvalue())
                self.assertEqual(report['ok'], expected)
                self.assertEqual(exited.exception.code, 0 if expected else 1)
                checks = {c['code']: c['ok'] for c in report['checks']}
                self.assertEqual(checks['PYTHON'], version >= (3, 11))
                self.assertEqual(checks['GIT'], available)
                self.assertEqual(checks['POWERSHELL'], available)
