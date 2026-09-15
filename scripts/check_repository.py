#!/usr/bin/env python3
"""Offline checks for local documentation targets and distribution consistency.

Does not check external availability, Markdown anchors, or live installation.
"""
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', 'node_modules', '__pycache__', '.venv', 'playwright-report', 'test-results'}


def local_target(source, raw, root):
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc or not parsed.path or '<' in raw:
        return None
    return (root / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/')
            else source.parent / unquote(parsed.path)).resolve()


def check_links(root):
    errors = []
    count = 0
    for directory, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in EXCLUDED]
        for name in files:
            source = Path(directory) / name
            if source.suffix not in {'.md', '.html'}:
                continue
            text = source.read_text(encoding='utf-8-sig')
            if source.suffix == '.md':
                text = re.sub(r'(?ms)^```.*?^```[^\n]*', '', text)
                links = re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text)
                links += re.findall(r'(?m)^\[[^]]+\]:\s*(\S+)', text)
                links = [link.strip().split(' "', 1)[0].strip('<>') for link in links]
            else:
                links = re.findall(r'(?:href|src)=["\']([^"\']+)', text)
            for raw in links:
                target = local_target(source, raw, root)
                if target is None:
                    continue
                count += 1
                if not target.exists():
                    errors.append(f'{source.relative_to(root)}: missing target: {raw}')
    return count, errors


def check_packaging(root):
    plugin = root / 'plugins/adaptive-sdd'
    manifests = [json.loads((plugin / name).read_text(encoding='utf-8'))
                 for name in ('plugin.json', '.codex-plugin/plugin.json')]
    errors = []
    version = manifests[0]['version']
    if any(m['version'] != version or m['name'] != 'adaptive-sdd' for m in manifests):
        errors.append('plugin manifests must agree on name and version')
    if not (plugin / manifests[1]['skills'] / 'adaptive-sdd/SKILL.md').is_file():
        errors.append('Codex manifest skill path does not resolve')
    marketplace = json.loads((root / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    entries = [item for item in marketplace['plugins'] if item['name'] == 'adaptive-sdd']
    if len(entries) != 1 or (root / entries[0]['source']['path']).resolve() != plugin.resolve():
        errors.append('marketplace source must resolve to the plugin directory')
    if not re.search(rf'^## {re.escape(version)}\s+-', (root / 'CHANGELOG.md').read_text(), re.M):
        errors.append('manifest version is missing from changelog')
    if f'**{version}**' not in (root / 'README.md').read_text(encoding='utf-8-sig'):
        errors.append('README must state the current manifest version')
    package = json.loads((root / 'package.json').read_text())
    lock = json.loads((root / 'package-lock.json').read_text())
    dependency = package['devDependencies']['@playwright/test']
    if dependency != lock['packages']['']['devDependencies']['@playwright/test'] or dependency != lock['packages']['node_modules/@playwright/test']['version']:
        errors.append('Playwright must be exactly pinned consistently with the lockfile')
    return errors


def main():
    count, errors = check_links(ROOT)
    errors.extend(check_packaging(ROOT))
    for error in errors:
        print(f'ERROR: {error}')
    print(f'{count} local documentation targets checked; {len(errors)} errors. External URLs and anchors not checked.')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
