#!/usr/bin/env python3
"""Run deterministic workflow safety scenarios and emit a compact report."""
import argparse, json, subprocess, sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser(); p.add_argument('--plugin', type=Path, default=Path(__file__).resolve().parents[1]); p.add_argument('--json', action='store_true'); args = p.parse_args()
    root = args.plugin.resolve(); config = json.loads((root / 'evals/scenarios.json').read_text())
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(root / 'tests'), '-v'], capture_output=True, text=True)
    missing = [s['test'] for s in config['deterministic'] if s['test'] not in result.stderr and s['test'] not in result.stdout]
    passed = result.returncode == 0 and not missing
    report = {'schema_version':1, 'passed':passed, 'scenario_count':len(config['deterministic']), 'missing_tests':missing,
              'metrics':{s['metric']: 0 if passed else None for s in config['deterministic']},
              'live_agent_evaluated':False, 'limitations':['deterministic fixtures do not establish live-agent or upstream integration performance']}
    if args.json: print(json.dumps(report, indent=2))
    else:
        print(('PASS' if passed else 'FAIL') + f": {len(config['deterministic'])} deterministic workflow scenarios")
        for limitation in report['limitations']: print(f"LIMITATION: {limitation}")
        if missing: print('MISSING: ' + ', '.join(missing))
    raise SystemExit(0 if passed else 1)
if __name__ == '__main__': main()
