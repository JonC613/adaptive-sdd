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


class StrictVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.artifact = self.project / 'tiny.md'
        self.state_path = self.project / '.sdd/features/example/state.json'

    def run_command(self, command, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), '--project', str(self.project),
                                 command, '--feature', 'example', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def initialize(self, tier='tiny', artifact='tiny.md'):
        self.run_command('init', '--tier', tier, '--artifact', artifact)
        self.run_command('approve', '--by', 'process:fixture', '--action', 'implementation')
        return json.loads(self.state_path.read_text())

    def modern_tiny(self):
        text = (ROOT / 'skills/adaptive-sdd/assets/tinyspec.md').read_text(encoding='utf-8')
        replacements = {'<feature-slug>': 'example', '<owner>': 'fixture', 'YYYY-MM-DD': '2026-09-14',
                        '<Observable requirement>': 'The save button persists the current title.'}
        for before, after in replacements.items():
            text = text.replace(before, after)
        # Fill remaining scaffold prose; strict criteria must never be placeholders.
        import re
        self.artifact.write_text(re.sub(r'<[^>]+>', 'Save a title locally.', text), encoding='utf-8')

    def evidence(self, criterion, result='pass', source='tiny.md'):
        self.run_command('evidence', '--criterion', criterion, '--method', 'automated',
                         '--result', result, '--source', source, '--by', 'process:fixture',
                         '--command', 'fixture-only recorded assertion', '--exit-code', '0' if result == 'pass' else '1')

    def verify(self, expected):
        return json.loads(self.run_command('verify', '--json', expected=expected).stdout)

    def test_empty_criteria_cannot_verify(self):
        self.artifact.write_text('# Specification\nA heading and sentence.\n')
        state = self.initialize()
        self.assertEqual(state['criteria'], [])
        report = self.verify(1)
        self.assertFalse(report['verified'])
        self.assertTrue(any('no meaningful acceptance criteria' in item for item in report['blockers']))
        self.assertTrue(any('unsupported TinySpec' in item for item in report['blockers']))

    def test_minimal_tiny_requires_evidence_but_no_tasks(self):
        self.modern_tiny()
        state = self.initialize()
        self.assertEqual(state['criteria'], ['R-01'])
        self.assertEqual(state['tasks'], [])
        self.assertIn('missing current passing evidence: R-01', self.verify(1)['blockers'])
        self.evidence('R-01')
        report = self.verify(0)
        self.assertTrue(report['verified'])
        self.assertFalse(report['executed_checks'])

    def test_legacy_tiny_example_remains_read_only_and_requires_each_outcome(self):
        original = (ROOT / 'examples/simple-kanban/tiny/simple-kanban.md').read_bytes()
        self.artifact.write_bytes(original)
        state = self.initialize()
        self.assertEqual(len(state['criteria']), 9)
        for criterion in state['criteria'][:-1]:
            self.evidence(criterion)
        self.assertIn('missing current passing evidence: R-09', self.verify(1)['blockers'])
        self.evidence('R-09')
        self.verify(0)
        self.assertEqual(self.artifact.read_bytes(), original)

    def test_changed_worktree_and_reapproved_artifacts_do_not_refresh_evidence(self):
        self.modern_tiny()
        self.initialize()
        self.evidence('R-01')
        self.verify(0)
        (self.project / 'implementation.txt').write_text('changed implementation')
        self.assertIn('missing current passing evidence: R-01', self.verify(1)['blockers'])
        self.evidence('R-01')
        self.verify(0)
        self.artifact.write_text(self.artifact.read_text() + '\nAmended scope.\n')
        self.run_command('approve', '--by', 'process:fixture')
        self.assertIn('missing current passing evidence: R-01', self.verify(1)['blockers'])

    def test_latest_failure_overrides_earlier_pass_at_same_snapshot(self):
        self.modern_tiny()
        self.initialize()
        self.evidence('R-01')
        self.evidence('R-01', result='fail')
        self.verify(1)
        self.evidence('R-01')
        self.verify(0)

    def test_ignored_evidence_source_is_bound_to_its_contents(self):
        self.modern_tiny()
        subprocess.run(['git', '-C', str(self.project), 'init'], check=True, capture_output=True)
        (self.project / '.gitignore').write_text('report.txt\n')
        report = self.project / 'report.txt'
        report.write_text('fixture pass')
        self.initialize()
        self.evidence('R-01', source='report.txt')
        self.verify(0)
        report.write_text('changed report')
        self.assertTrue(any('changed evidence source' in item for item in self.verify(1)['blockers']))
        report.unlink()
        self.verify(1)

    def test_missing_criteria_in_old_state_cannot_bypass_discovery(self):
        self.modern_tiny()
        self.initialize()
        state = json.loads(self.state_path.read_text())
        state['criteria'] = []
        self.state_path.write_text(json.dumps(state))
        report = self.verify(1)
        self.assertTrue(any('differ from recorded state' in item for item in report['blockers']))
        self.assertIn('missing current passing evidence: R-01', report['blockers'])

    def test_placeholder_or_malformed_criterion_blocks_despite_one_valid_outcome(self):
        for extra in ('- **R-02:** <Observable requirement>', '- **R-02:**', '- R-02: Save another title.',
                      '+ **R-02:** Save another title.', '* **R-02:** Save another title.'):
            with self.subTest(extra=extra):
                self.modern_tiny()
                self.artifact.write_text(self.artifact.read_text().replace('## Constraints and assumptions', extra + '\n\n## Constraints and assumptions'))
                self.initialize()
                self.evidence('R-01')
                self.verify(1)
                self.state_path.unlink()

    def test_ids_in_comments_or_code_are_not_criteria(self):
        self.modern_tiny()
        text = self.artifact.read_text().replace('- **R-01:** The save button persists the current title.',
            '<!-- - **R-01:** Comment example. -->\n```markdown\n- **R-02:** Code example.\n```')
        self.artifact.write_text(text)
        self.assertEqual(self.initialize()['criteria'], [])
        self.verify(1)

    def test_supported_speckit_format_requires_scenarios_requirements_and_outcomes(self):
        feature = self.project / 'specs/example'
        feature.mkdir(parents=True)
        (feature / 'spec.md').write_text('''# Feature Specification: Save title
## User Scenarios & Testing *(mandatory)*
### User Story 1 - Save title (Priority: P1)
**Independent Test**: Save a title and reload.
**Acceptance Scenarios**:
1. **Given** a title, **When** saved, **Then** reload retains it.
## Requirements *(mandatory)*
### Functional Requirements
- **FR-001**: System MUST persist the title.
## Success Criteria *(mandatory)*
### Measurable Outcomes
- **SC-001**: The saved title survives every reload in the fixture.
''')
        (feature / 'plan.md').write_text('# Implementation Plan: Save title\nUse local storage.\n')
        (feature / 'tasks.md').write_text('# Tasks\n- [ ] T001 Implement title persistence.\n')
        state = self.initialize('speckit', 'specs/example')
        self.assertEqual(state['criteria'], ['FR-001', 'SC-001', 'US1-AC1'])
        self.assertEqual([t['id'] for t in state['tasks']], ['T001'])
        self.run_command('task', '--task', 'T001', '--status', 'done')
        for criterion in state['criteria']:
            self.evidence(criterion, source='specs/example/spec.md')
        self.verify(0)
        (feature / 'spec.md').write_text('# Unsupported specification\nNo criteria.\n')
        self.run_command('approve', '--by', 'process:fixture')
        self.verify(1)

    def test_lite_cannot_approve_only_spec_and_ignore_other_artifacts(self):
        shutil.copytree(EXAMPLE, self.project / 'simple-kanban')
        self.initialize('lite', 'simple-kanban/spec.md')
        self.assertTrue(any('approve all artifacts' in item for item in self.verify(1)['blockers']))

    def test_minimal_lite_one_story_one_task_and_one_test(self):
        feature = self.project / 'example'
        feature.mkdir()
        sections = {
            'spec': ['Summary', 'Problem', 'Desired outcome', 'Requirements', 'User stories',
                     'Non-functional requirements', 'Codebase context', 'Assumptions and open questions', 'Amendment history'],
            'plan': ['Technical approach', 'Key decisions', 'Impacted areas', 'Implementation phases', 'Amendment history'],
            'tests': ['Strategy', 'Acceptance traceability', 'Critical user flows', 'Failure and recovery cases',
                      'Manual exceptions', 'Test data and setup', 'Completion criteria', 'Amendment history'],
        }
        bodies = {
            'Requirements': '- **R-01:** Save a title locally.',
            'User stories': '### US-01 — Save title\n- **AC-01.1:** Reload retains the saved title.',
            'Implementation phases': '- [ ] **P1-T1 — Save title**\n  - Depends on: None\n  - Covers: AC-01.1\n  - Work: Save the title.\n  - Verify: Reload retains it.',
            'Acceptance traceability': '| AC-01.1 | T-01 |',
            'Critical user flows': '### T-01 — Reload\n- Covers: AC-01.1\n- Expected: The title survives reload.',
        }
        for name, headings in sections.items():
            metadata = f'---\nfeature: example\nartifact: {name}\nstatus: draft\nowner: fixture\nversion: 0.1\ncreated: 2026-09-14\nupdated: 2026-09-14\n'
            if name != 'spec':
                metadata += 'spec_version: 0.1\n'
            if name == 'tests':
                metadata += 'plan_version: 0.1\n'
            text = metadata + f'---\n# {name}\n'
            for heading in headings:
                text += f'\n## {heading}\n\n' + bodies.get(heading, 'One local title-persistence change; no additional scope.') + '\n'
            (feature / f'{name}.md').write_text(text, encoding='utf-8')
        state = self.initialize('lite', 'example')
        self.assertEqual(state['criteria'], ['AC-01.1'])
        self.assertIn('missing current passing evidence: AC-01.1', self.verify(1)['blockers'])
        self.evidence('AC-01.1', source='example/tests.md')
        self.assertIn('unfinished task: P1-T1', self.verify(1)['blockers'])
        self.run_command('task', '--task', 'P1-T1', '--status', 'done')
        self.verify(0)

    def test_old_evidence_without_source_fingerprint_requires_new_record(self):
        self.modern_tiny()
        self.initialize()
        self.evidence('R-01')
        state = json.loads(self.state_path.read_text())
        del state['evidence'][0]['source_fingerprint']
        self.state_path.write_text(json.dumps(state))
        self.verify(1)
        self.evidence('R-01')
        self.verify(0)
