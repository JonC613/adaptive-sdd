"""Regression checks for the upgrade audit. All mutations use isolated fixtures."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/adaptive-sdd/scripts'
EXAMPLE = ROOT / 'examples/simple-kanban/lite/simple-kanban'
PWSH = shutil.which('pwsh')


class ReliabilityTests(unittest.TestCase):
    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True)

    def fixture(self, folder):
        return Path(shutil.copytree(EXAMPLE, Path(folder) / 'simple-kanban'))

    def test_validator_negative_cases(self):
        cases = [
            ('spec.md', 'owner: user', 'owner:', 'STRUCTURE_INVALID'),
            ('spec.md', 'owner: user', 'owner: user\nowner: other', 'META_DUPLICATE'),
            ('spec.md', 'created: 2026-08-15', 'created: 2026-99-99', 'STRUCTURE_INVALID'),
            ('spec.md', '## Problem', '## Removed', 'SECTION_MISSING'),
            ('plan.md', 'Depends on: None', 'Depends on: P999-T999', 'TASK_DEPENDENCY'),
            ('plan.md', 'Depends on: None', 'Depends on: P1-T2', 'TASK_CYCLE'),
            ('tests.md', '| AC-01.1 | T-01 |', '| AC-01.1 | NO_TEST |', 'TRACE_EMPTY'),
            ('tests.md', '| AC-01.1 | T-01 |', '| AC-01.1 | T-02 |', 'TRACE_MISMATCH'),
        ]
        for name, before, after, code in cases:
            with self.subTest(code=code, after=after), tempfile.TemporaryDirectory() as folder:
                feature = self.fixture(folder)
                path = feature / name
                original = path.read_text(encoding='utf-8')
                self.assertIn(before, original)
                path.write_text(original.replace(before, after), encoding='utf-8')
                result = self.run_script('validate_litespec.py', feature, '--approved', '--json')
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report['kind'], 'structural')
                self.assertIn(code, {item['code'] for item in report['diagnostics']})

    def test_success_is_only_structural(self):
        result = self.run_script('validate_litespec.py', EXAMPLE, '--approved')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('delivery not verified', result.stdout)

    def test_tiny_dates_and_quotes(self):
        with tempfile.TemporaryDirectory() as folder:
            self.run_script('scaffold_tinyspec.py', '--project', folder, '--feature', 'test', '--title', 'Test')
            path = Path(folder) / '.tinyspec/test.md'
            text = path.read_text(encoding='utf-8')
            path.write_text(text.replace('artifact: tiny', 'artifact: "tiny"'), encoding='utf-8')
            self.assertEqual(self.run_script('validate_tinyspec.py', path, '--json').returncode, 0)
            path.write_text(text.replace('version: 0.1', 'version: nonsense'), encoding='utf-8')
            self.assertEqual(self.run_script('validate_tinyspec.py', path, '--json').returncode, 1)

    def test_memory_local_and_specification_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            def git(*args):
                return subprocess.run(['git', '-C', folder, *args], check=True, capture_output=True, text=True)
            git('init')
            git('config', 'user.name', 'Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            (project / 'code.txt').write_text('initial', encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'fixture')
            self.assertEqual(self.run_script('project_memory.py', 'scaffold', '--project', folder).returncode, 0)
            (project / 'code.txt').write_text('staged', encoding='utf-8')
            git('add', 'code.txt')
            (project / 'code.txt').write_text('unstaged', encoding='utf-8')
            (project / 'specs').mkdir()
            (project / 'specs/api.md').write_text('contract change', encoding='utf-8')
            result = self.run_script('project_memory.py', 'status', '--project', folder)
            for label in ('staged', 'unstaged', 'untracked'):
                self.assertIn(f'({label})', result.stdout)
            self.assertNotIn('PASS:', result.stdout)
            git('add', '.')
            git('commit', '-m', 'changes')
            result = self.run_script('project_memory.py', 'status', '--project', folder)
            self.assertIn('2 durable path(s)', result.stdout)

    @unittest.skipUnless(PWSH, 'PowerShell 7 required')
    def test_installer_backup_and_unsafe_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'adaptive-sdd'
            script = ROOT / 'scripts/install-cursor-local.ps1'
            def run(*args):
                return subprocess.run([PWSH, '-NoProfile', '-File', str(script), *map(str, args)], capture_output=True, text=True)
            self.assertEqual(run('-Destination', destination).returncode, 0)
            previous = (destination / 'plugin.json').read_bytes()
            self.assertEqual(run('-Destination', destination, '-Force').returncode, 0)
            backups = list(Path(folder).glob('.adaptive-sdd-backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'plugin.json').read_bytes(), previous)
            result = run('-Destination', folder, '-Force')
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(destination.exists())
            (destination / 'unrelated.txt').write_text('keep', encoding='utf-8')
            self.assertNotEqual(run('-Destination', destination, '-Force').returncode, 0)
            self.assertEqual((destination / 'unrelated.txt').read_text(), 'keep')

    @unittest.skipUnless(PWSH, 'PowerShell 7 required')
    def test_installer_allows_linked_ancestor_but_rejects_linked_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            real_parent = root / 'real-parent'
            linked_parent = root / 'linked-parent'
            real_parent.mkdir()
            try:
                os.symlink(real_parent, linked_parent, target_is_directory=True)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f'directory symlinks unavailable: {error}')

            script = ROOT / 'scripts/install-cursor-local.ps1'
            destination = linked_parent / 'adaptive-sdd'
            result = subprocess.run(
                [PWSH, '-NoProfile', '-File', str(script), '-Destination', str(destination)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((real_parent / 'adaptive-sdd/plugin.json').is_file())

            linked_destination = root / 'adaptive-sdd'
            os.symlink(real_parent / 'adaptive-sdd', linked_destination, target_is_directory=True)
            result = subprocess.run(
                [PWSH, '-NoProfile', '-File', str(script), '-Destination', str(linked_destination), '-Force'],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('file or link', result.stdout + result.stderr)

    @unittest.skipUnless(PWSH, 'PowerShell 7 required')
    def test_combined_installer_checks_clean_tree_before_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            subprocess.run(['git', '-C', folder, 'init'], check=True, capture_output=True)
            script = str(ROOT / 'scripts/install-project.ps1').replace("'", "''")
            target = folder.replace("'", "''")
            # Functions deliberately shadow external tools; no network or global install.
            command = f"function uv {{ $global:LASTEXITCODE=0 }}; function specify {{ $global:LASTEXITCODE=0 }}; & '{script}' -Target '{target}' -InstallSpecKit"
            result = subprocess.run([PWSH, '-NoProfile', '-Command', command], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((Path(folder) / '.agents/skills/adaptive-sdd/SKILL.md').is_file())

    @unittest.skipUnless(PWSH, 'PowerShell 7 required')
    def test_installer_whatif_does_not_create_target(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'adaptive-sdd'
            result = subprocess.run([PWSH, '-NoProfile', '-File', str(ROOT / 'scripts/install-cursor-local.ps1'), '-Destination', str(destination), '-WhatIf'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(destination.exists())
