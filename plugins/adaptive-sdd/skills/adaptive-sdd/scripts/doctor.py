#!/usr/bin/env python3
"""Read-only Adaptive SDD installation and compatibility diagnostics."""
import argparse, json, re, shutil, subprocess
from pathlib import Path

def main():
    p = argparse.ArgumentParser(); p.add_argument('--plugin', type=Path, default=Path(__file__).resolve().parents[3]); p.add_argument('--json', action='store_true'); args = p.parse_args()
    root = args.plugin.resolve(); checks = []
    def add(code, ok, message): checks.append({'code': code, 'ok': bool(ok), 'message': message})
    manifests = [root / 'plugin.json', root / '.codex-plugin/plugin.json']
    versions = []
    for path in manifests:
        try: versions.append(json.loads(path.read_text(encoding='utf-8'))['version']); add('MANIFEST', True, f'{path.name} readable')
        except Exception as exc: add('MANIFEST', False, f'{path}: {exc}')
    add('VERSION_SYNC', len(set(versions)) == 1 and bool(versions), f'manifest versions: {versions}')
    add('PYTHON', True, 'running on supported Python' if __import__('sys').version_info >= (3,11) else 'Python 3.11+ required')
    add('GIT', shutil.which('git') is not None, 'Git available' if shutil.which('git') else 'Git unavailable')
    add('POWERSHELL', shutil.which('pwsh') is not None, 'PowerShell 7 available' if shutil.which('pwsh') else 'PowerShell 7 unavailable')
    for name in ('validate_litespec.py','validate_tinyspec.py','project_memory.py','delivery_state.py'):
        add('SCRIPT', (root / 'skills/adaptive-sdd/scripts' / name).is_file(), name)
    installer = (root / 'scripts/install-project.ps1').read_text(encoding='utf-8')
    pin = re.search(r'SpecKitVersion = "([^"]+)"', installer)
    add('SPECKIT_PIN', bool(pin), f'pinned {pin.group(1)}; live compatibility not tested' if pin else 'pin missing')
    ok = all(c['ok'] for c in checks)
    if args.json: print(json.dumps({'schema_version':1,'ok':ok,'checks':checks}, indent=2))
    else:
        for check in checks: print(('PASS' if check['ok'] else 'FAIL') + f" [{check['code']}] {check['message']}")
        print('INFO Live Spec Kit and marketplace compatibility require separate integration checks.')
    raise SystemExit(0 if ok else 1)
if __name__ == '__main__': main()
