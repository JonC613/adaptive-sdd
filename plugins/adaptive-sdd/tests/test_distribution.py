import json, re, subprocess, sys, unittest
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
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout); self.assertTrue(report['ok'])
        self.assertIn('0.4.0', next(c['message'] for c in report['checks'] if c['code'] == 'VERSION_SYNC'))

    def test_distribution_guidance_is_present(self):
        repo = ROOT.parents[1]
        for name in ('CHANGELOG.md','CONTRIBUTING.md','SECURITY.md'):
            self.assertTrue((repo / name).is_file())
        self.assertIn('security boundary', (ROOT / 'skills/adaptive-sdd/references/delivery-evidence.md').read_text().lower())

    def test_engineering_skill_routing_covers_installed_catalog(self):
        repo = ROOT.parents[1]
        routing = (ROOT / 'skills/adaptive-sdd/references/engineering-skill-routing.md').read_text(encoding='utf-8')
        assessment = (repo / 'docs/agent-skills-compatibility.md').read_text(encoding='utf-8')
        skill = (ROOT / 'skills/adaptive-sdd/SKILL.md').read_text(encoding='utf-8')
        lock = json.loads((repo / 'skills-lock.json').read_text(encoding='utf-8'))
        rows = re.findall(r'^\| `([^`]+)` \| (Integrate|Use alongside|Adapt first|Skip) \|', assessment, re.MULTILINE)
        dispositions = {name: disposition for name, disposition in rows}

        self.assertEqual(set(dispositions), set(lock['skills']))
        self.assertEqual(len(dispositions), 25)
        self.assertIn('engineering-skill-routing.md', skill)
        self.assertIn('Adaptive SDD owns the development workflow', routing)
        self.assertIn('cannot authorize', routing)
        self.assertIn('Record only evidence that actually ran', routing)
