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

    def test_plugin_manifest_points_to_skills(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "adaptive-sdd")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_cursor_agent_plugin_manifest(self) -> None:
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], "adaptive-sdd")
        self.assertEqual(manifest["version"], "0.2.0")
        self.assertTrue((ROOT / "skills" / "adaptive-sdd" / "SKILL.md").is_file())

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


if __name__ == "__main__":
    unittest.main()
