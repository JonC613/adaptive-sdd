import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/adaptive-sdd/scripts/delivery_state.py'
EXAMPLE = ROOT / 'examples/simple-kanban/lite/simple-kanban'


class DeliveryStateTests(unittest.TestCase):
    def execute(self, project, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--project', str(project), *args], capture_output=True, text=True)

    def project(self, folder):
        project = Path(folder); target = project / '.litespec/simple-kanban'
        shutil.copytree(EXAMPLE, target)
        subprocess.run(['git', '-C', str(project), 'init'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(project), 'config', 'user.name', 'Fixture'], check=True)
        subprocess.run(['git', '-C', str(project), 'config', 'user.email', 'fixture@example.invalid'], check=True)
        subprocess.run(['git', '-C', str(project), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(project), 'commit', '-m', 'fixture'], check=True, capture_output=True)
        return project, target

    def test_resumable_evidence_lifecycle_and_stale_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            project, artifacts = self.project(folder)
            self.assertEqual(self.execute(project, 'init', '--feature', 'simple-kanban', '--tier', 'lite').returncode, 0)
            state_path = project / '.sdd/features/simple-kanban/state.json'
            state = json.loads(state_path.read_text())
            self.assertEqual(state['interaction_mode'], 'collaborative')
            self.assertTrue(state['criteria']); self.assertTrue(state['tasks'])
            self.assertTrue(all(item.startswith('AC-') for item in state['criteria']))
            self.assertEqual(self.execute(project, 'verify', '--feature', 'simple-kanban').returncode, 1)
            self.assertEqual(self.execute(project, 'approve', '--feature', 'simple-kanban', '--by', 'human:owner', '--action', 'implementation', '--action', 'release').returncode, 0)
            for task in state['tasks']:
                self.assertEqual(self.execute(project, 'task', '--feature', 'simple-kanban', '--task', task['id'], '--status', 'done').returncode, 0)
            for criterion in state['criteria']:
                self.assertEqual(self.execute(project, 'evidence', '--feature', 'simple-kanban', '--criterion', criterion, '--method', 'automated', '--result', 'pass', '--source', '.litespec/simple-kanban/tests.md', '--by', 'process:fixture', '--command', 'fixture test', '--exit-code', '0').returncode, 0)
            verified = self.execute(project, 'verify', '--feature', 'simple-kanban')
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
            subprocess.run(['git', '-C', str(project), 'add', '.sdd/features'], check=True)
            subprocess.run(['git', '-C', str(project), 'commit', '-m', 'record delivery state'], check=True, capture_output=True)
            unchanged = json.loads(self.execute(project, 'status', '--feature', 'simple-kanban', '--json').stdout)
            self.assertEqual(unchanged['blockers'], [])
            self.assertEqual(self.execute(project, 'release', '--feature', 'simple-kanban', '--reference', 'fixture:v1').returncode, 0)
            spec = artifacts / 'spec.md'; spec.write_text(spec.read_text() + '\nchanged\n')
            status = self.execute(project, 'status', '--feature', 'simple-kanban', '--json')
            report = json.loads(status.stdout)
            self.assertEqual(report['status'], 'blocked')
            self.assertTrue(any('stale or unapproved' in item for item in report['blockers']))
            self.assertEqual(self.execute(project, 'release', '--feature', 'simple-kanban', '--reference', 'fixture:v2').returncode, 1)

    def test_authorization_and_manual_evidence_are_attributed(self):
        with tempfile.TemporaryDirectory() as folder:
            project, _ = self.project(folder)
            result = self.execute(project, 'init', '--feature', 'simple-kanban', '--tier', 'lite', '--mode', 'delegated', '--allow', 'implementation', '--exclude', 'deployment')
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads((project / '.sdd/features/simple-kanban/state.json').read_text())
            self.assertEqual(state['authorization'], {'allowed': ['implementation'], 'excluded': ['deployment']})

    def test_evidence_attribution_rules(self):
        with tempfile.TemporaryDirectory() as folder:
            project, _ = self.project(folder)
            self.execute(project, 'init', '--feature', 'simple-kanban', '--tier', 'lite')
            common = ('evidence', '--feature', 'simple-kanban', '--criterion', 'AC-01.1', '--result', 'pass', '--source', '.litespec/simple-kanban/tests.md')
            self.assertNotEqual(self.execute(project, *common, '--method', 'automated', '--by', 'process:fixture').returncode, 0)
            self.assertNotEqual(self.execute(project, *common, '--method', 'manual', '--by', 'process:fixture').returncode, 0)
