from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "adaptive-sdd"


class AdaptiveSDDTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SKILL / "scripts" / name), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def run_memory(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_script("project_memory.py", *args, "--project", str(project))

    def init_repository(self, folder: str) -> Path:
        project = Path(folder)
        (project / "README.md").write_text("# Fixture\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(project), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(project), "config", "user.name", "Adaptive SDD Tests"], check=True)
        subprocess.run(["git", "-C", str(project), "config", "user.email", "tests@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(project), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(project), "commit", "-q", "-m", "fixture"], check=True)
        return project

    def test_plugin_manifest_points_to_skills(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "adaptive-sdd")
        self.assertEqual(manifest["version"], "0.4.0")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_cursor_agent_plugin_manifest(self) -> None:
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], "adaptive-sdd")
        self.assertEqual(manifest["version"], "0.4.0")
        self.assertTrue((ROOT / "skills" / "adaptive-sdd" / "SKILL.md").is_file())

    def test_root_bootstrap_scripts_delegate_to_plugin_installers(self) -> None:
        marketplace_root = ROOT.parents[1]
        for name, implementation in (
            ("install-project.ps1", "plugins/adaptive-sdd/scripts/install-project.ps1"),
            ("install-cursor-local.ps1", "plugins/adaptive-sdd/scripts/install-cursor-local.ps1"),
        ):
            with self.subTest(name=name):
                script = marketplace_root / name
                self.assertTrue(script.is_file())
                self.assertIn(implementation, script.read_text(encoding="utf-8").replace("\\", "/"))

    def test_project_installer_and_litespec_cover_activation_and_external_inputs(self) -> None:
        installer = (ROOT / "scripts" / "install-project.ps1").read_text(encoding="utf-8")
        tier_selection = (SKILL / "references" / "tier-selection.md").read_text(encoding="utf-8")
        litespec = (SKILL / "references" / "litespec-method.md").read_text(encoding="utf-8")
        spec_template = (SKILL / "assets" / "spec.md").read_text(encoding="utf-8")
        tests_template = (SKILL / "assets" / "tests.md").read_text(encoding="utf-8")

        self.assertIn("Activation required", installer)
        self.assertIn("Existing tasks may not discover skills", installer)
        self.assertIn("Application integration signals", tier_selection)
        for text in (tier_selection, litespec, spec_template, tests_template):
            self.assertIn("remote", text.lower())
            self.assertIn("external", text.lower())

    def test_tinyspec_scaffold_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            created = self.run_script(
                "scaffold_tinyspec.py", "--project", folder, "--feature", "export-csv", "--title", "Export CSV"
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            artifact = Path(folder) / ".tinyspec" / "export-csv.md"
            self.assertTrue(artifact.is_file())
            validation = self.run_script("validate_tinyspec.py", str(artifact))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_tinyspec_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            args = ("--project", folder, "--feature", "export-csv", "--title", "Export CSV")
            self.assertEqual(self.run_script("scaffold_tinyspec.py", *args).returncode, 0)
            second = self.run_script("scaffold_tinyspec.py", *args)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("refusing to overwrite", second.stderr.lower())

    def test_litespec_example_validates(self) -> None:
        result = self.run_script("validate_litespec.py", str(ROOT / "examples" / "simple-kanban" / "lite" / "simple-kanban"), "--approved")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_memory_scaffold_status_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            created = self.run_memory(project, "scaffold", "--title", "Fixture", "--verified-by", "human:owner")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            memory = project / ".sdd" / "memory"
            self.assertEqual(
                {path.name for path in memory.iterdir()},
                {"index.md", "project.md", "architecture.md", "log.md"},
            )
            state = json.loads((project / ".sdd" / "memory-state.json").read_text(encoding="utf-8"))
            head = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            self.assertEqual(state["last_reconciled_commit"], head)
            validation = self.run_memory(project, "verify")
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("PASS:", validation.stdout)
            status = self.run_memory(project, "status")
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("reconciled with HEAD", status.stdout)

    def test_project_memory_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            before = (project / ".sdd" / "memory" / "project.md").read_text(encoding="utf-8")
            second = self.run_memory(project, "scaffold")
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("refusing to overwrite", second.stderr.lower())
            self.assertEqual((project / ".sdd" / "memory" / "project.md").read_text(encoding="utf-8"), before)

    def test_project_memory_reports_drift_and_reconciles_forward(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            (project / "change.txt").write_text("material change\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(project), "add", "change.txt"], check=True)
            subprocess.run(["git", "-C", str(project), "commit", "-q", "-m", "change"], check=True)
            head = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            stale = self.run_memory(project, "verify")
            self.assertEqual(stale.returncode, 0, stale.stdout + stale.stderr)
            self.assertIn("WARN:", stale.stdout)
            reconciled = self.run_memory(project, "reconcile", "--commit", head)
            self.assertEqual(reconciled.returncode, 0, reconciled.stdout + reconciled.stderr)
            current = self.run_memory(project, "verify")
            self.assertEqual(current.returncode, 0, current.stdout + current.stderr)
            self.assertIn("PASS:", current.stdout)

    def test_project_memory_ignores_its_own_commit_for_drift(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            subprocess.run(["git", "-C", str(project), "add", ".sdd"], check=True)
            subprocess.run(["git", "-C", str(project), "commit", "-q", "-m", "add memory"], check=True)
            validation = self.run_memory(project, "verify")
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("PASS:", validation.stdout)
            status = self.run_memory(project, "status")
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("Only excluded memory artifacts", status.stdout)

    def test_project_memory_validation_rejects_broken_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            concept = project / ".sdd" / "memory" / "project.md"
            text = concept.read_text(encoding="utf-8").replace("../../README.md", "../../missing.md")
            concept.write_text(text, encoding="utf-8")
            validation = self.run_memory(project, "verify")
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("missing source", validation.stdout)
            self.assertIn("FAIL:", validation.stdout)

    def test_project_memory_non_git_repository_has_limited_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            (project / "README.md").write_text("# Fixture\n", encoding="utf-8")
            created = self.run_memory(project, "scaffold")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            validation = self.run_memory(project, "verify")
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("Git history unavailable", validation.stdout)

    def test_project_memory_shallow_checkout_has_limited_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            state_path = project / ".sdd" / "memory-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["last_reconciled_commit"] = "0" * 40
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            head = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            (project / ".git" / "shallow").write_text(head + "\n", encoding="ascii")

            validation = self.run_memory(project, "verify")
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("outside this shallow checkout", validation.stdout)
            self.assertIn("WARN:", validation.stdout)

    def test_project_memory_preserves_unknown_concept_fields(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            concept = project / ".sdd" / "memory" / "project.md"
            text = concept.read_text(encoding="utf-8").replace("status: draft\n", "status: draft\nextension: {\"keep\":true}\n")
            concept.write_text(text, encoding="utf-8")
            before = concept.read_text(encoding="utf-8")
            head = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            result = self.run_memory(project, "reconcile", "--commit", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(concept.read_text(encoding="utf-8"), before)

    def test_project_memory_validator_distinguishes_optional_links_and_required_state(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            concept = project / ".sdd" / "memory" / "project.md"
            concept.write_text(
                concept.read_text(encoding="utf-8") + "\nSee [future knowledge](future.md).\n",
                encoding="utf-8",
            )
            optional = self.run_memory(project, "verify")
            self.assertEqual(optional.returncode, 0, optional.stdout + optional.stderr)
            self.assertIn("broken link", optional.stdout)
            state_path = project / ".sdd" / "memory-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["profile_version"] = 999
            state_path.write_text(json.dumps(state), encoding="utf-8")
            required = self.run_memory(project, "verify")
            self.assertNotEqual(required.returncode, 0)
            self.assertIn("profile_version", required.stdout)

    def test_project_memory_reconciliation_cannot_move_backward(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            project = self.init_repository(folder)
            first = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            self.assertEqual(self.run_memory(project, "scaffold").returncode, 0)
            (project / "later.txt").write_text("later\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(project), "add", "later.txt"], check=True)
            subprocess.run(["git", "-C", str(project), "commit", "-q", "-m", "later"], check=True)
            later = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
            ).stdout.strip()
            self.assertEqual(self.run_memory(project, "reconcile", "--commit", later).returncode, 0)
            backward = self.run_memory(project, "reconcile", "--commit", first)
            self.assertNotEqual(backward.returncode, 0)
            self.assertIn("cannot move backward", backward.stderr)

    def test_project_memory_workflow_contract_requires_review_and_supports_all_sources(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        reference = (SKILL / "references" / "project-memory.md").read_text(encoding="utf-8")
        for operation in ("Initialize memory", "Status memory", "Verify memory", "Update memory", "Refresh memory"):
            self.assertIn(operation, skill)
        self.assertIn("Rejection changes nothing", skill)
        self.assertIn("reviewed no-op", skill)
        self.assertIn("Verify consequential claims", reference)
        for source in ("TinySpec", "LiteSpec", "Spec Kit", "Repository-only work"):
            self.assertIn(source, reference)
        for path in (SKILL / "assets" / "memory").iterdir():
            content = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("codex", content)
            self.assertNotIn("cursor", content)

    def test_project_memory_is_one_shared_agent_neutral_capability(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        reference = (SKILL / "references" / "project-memory.md").read_text(encoding="utf-8")
        self.assertIn("Maintain Project Memory", skill)
        self.assertIn("one shared workflow for Codex and Cursor", skill)
        self.assertIn("TinySpec", reference)
        self.assertIn("LiteSpec", reference)
        self.assertIn("Spec Kit", reference)
        self.assertFalse((ROOT / "skills" / "project-memory").exists())

    def test_project_memory_examples_validate(self) -> None:
        projects = (ROOT.parents[1], ROOT / "examples" / "simple-kanban")
        for project in projects:
            with self.subTest(project=project):
                result = self.run_memory(project, "verify")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Project Memory validation", result.stdout)


if __name__ == "__main__":
    unittest.main()
