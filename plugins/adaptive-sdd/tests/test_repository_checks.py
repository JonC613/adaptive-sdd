import importlib.util
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('check_repository', REPO / 'scripts/check_repository.py')
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)


class RepositoryCheckTests(unittest.TestCase):
    def test_local_links_include_html_and_ignore_external_urls_and_code_examples(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'present.md').write_text('# Present\n')
            (root / 'README.md').write_text('''[exists](present.md#unchecked-anchor)
[missing](absent.md)
[external](https://example.invalid/unavailable)
```text
[example](not-a-real-path.md)
```
''')
            (root / 'index.html').write_text('<a href="present.md">Present</a><img src="missing.png">')
            count, errors = checks.check_links(root)
            self.assertEqual(count, 4)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any('absent.md' in error for error in errors))
            self.assertTrue(any('missing.png' in error for error in errors))

    def test_distribution_versions_and_paths_are_consistent(self):
        self.assertEqual(checks.check_packaging(REPO), [])
