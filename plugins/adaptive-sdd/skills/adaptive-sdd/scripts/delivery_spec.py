"""Read supported specification formats without executing document content.

Strict delivery uses definitions, never incidental mentions of IDs. The existing
validators remain useful independently for draft document validation.
"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


def prose(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)", "", text)


def section(text, name):
    match = re.search(rf"(?mi)^## {re.escape(name)}\s*$", text)
    return re.split(r"(?m)^## ", text[match.end():], maxsplit=1)[0] if match else ""


def meaningful(body):
    body = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', body)
    return bool(re.search(r"\w", body)) and not re.search(
        r"<[^>]+>|\[(?:NEEDS CLARIFICATION|specific |initial state|action|expected outcome|Measurable |Describe |Explain )[^]]*\]|^\s*(?:TODO|TBD)\b|^\s*\[[^]]+\]\s*$", body
    )


def inspect_spec(project, artifacts, tier):
    """Return criterion IDs, optional task IDs, and actionable blocking diagnostics."""
    issues, definitions, tasks = [], [], []
    paths = [project / item for item in artifacts]

    def validate(script, target):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name(script)), str(target), '--json'],
            capture_output=True, text=True, encoding='utf-8',
        )
        if result.returncode:
            try:
                issues.extend(item['message'] for item in json.loads(result.stdout)['diagnostics'])
            except (ValueError, KeyError):
                issues.append(f"document validation failed: {target.name}: {result.stderr.strip()}")

    def read(path):
        try:
            return prose(path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError) as exc:
            issues.append(f"cannot read specification {path.name}: {exc}")
            return ''

    if tier == 'tiny' and len(paths) == 1 and paths[0].is_file():
        text = read(paths[0])
        requirements = section(text, 'Requirements')
        if text.startswith('---'):
            validate('validate_tinyspec.py', paths[0])
            definitions = re.findall(r"(?m)^\s*- \*\*(R-\d{2}):\*\*([^\n]*)", requirements)
            lines = [line for line in requirements.splitlines() if re.match(r'^\s*[-+*] ', line)]
            if len(lines) != len(definitions):
                issues.append('unrecognized TinySpec requirement: use - **R-01:** observable outcome')
        elif re.search(r'(?m)^# TinySpec:', text):
            # Historical repository example: numbered requirements, no metadata.
            for heading in ('What', 'Requirements', 'Plan', 'Done When'):
                if not section(text, heading).strip():
                    issues.append(f'legacy TinySpec missing section: {heading}')
            numbered = re.findall(r'(?m)^\s*(\d+)\.([^\n]*)', requirements)
            definitions = [(f'R-{int(number):02}', body) for number, body in numbered]
            if any(line.strip() and not re.match(r'^\s*\d+\.', line) for line in requirements.splitlines()):
                issues.append('unrecognized legacy requirement: use one numbered outcome per line')
        else:
            issues.append('unsupported TinySpec structure: use the TinySpec scaffold or documented legacy format')
    elif tier in ('lite', 'speckit'):
        if len(paths) == 1 and paths[0].is_dir():
            directory = paths[0]
        elif paths and len({p.parent for p in paths}) == 1:
            directory = paths[0].parent
            required = {'spec.md', 'plan.md', 'tests.md'} if tier == 'lite' else {'spec.md', 'plan.md', 'tasks.md'}
            if {p.name for p in paths} != required:
                issues.append(f'{tier} strict delivery must approve all artifacts: {", ".join(sorted(required))}')
        else:
            directory = None
            issues.append(f'unsupported {tier} layout: supply one feature directory')
        if directory:
            names = ('spec', 'plan', 'tests') if tier == 'lite' else ('spec', 'plan', 'tasks')
            texts = {name: read(directory / f'{name}.md') for name in names}
            text = texts['spec']
            if tier == 'lite':
                validate('validate_litespec.py', directory)
                definitions = re.findall(r'(?m)^\s*- \*\*(AC-\d{2}\.\d+):\*\*([^\n]*)', text)
                # A malformed definition must not disappear while another passes.
                mentions = re.findall(r'(?m)^\s*[-+*] .*?\b(AC-\d+\.\d+)\b', text)
                if Counter(mentions) != Counter(key for key, _ in definitions):
                    issues.append('unrecognized acceptance criterion: use - **AC-01.1:** observable outcome')
                tasks = re.findall(r'(?m)^- \[[ xX]\] \*\*(P\d+-T\d+)\s+—', texts['plan'])
            else:
                for heading in ('User Scenarios & Testing', 'Requirements', 'Success Criteria'):
                    if not re.search(rf'(?m)^## {re.escape(heading)}(?:\s|$)', text):
                        issues.append(f'Spec Kit spec.md missing section: {heading}')
                definitions = re.findall(r'(?m)^\s*- \*\*((?:FR|SC)-\d{3})\*\*:[ \t]*([^\n]*)', text)
                mentions = re.findall(r'(?m)^\s*[-+*] .*?\b((?:FR|SC)-\d+)\b', text)
                if Counter(mentions) != Counter(key for key, _ in definitions):
                    issues.append('unrecognized Spec Kit outcome: use - **FR-001**: or - **SC-001**: followed by an observable outcome')
                for prefix in ('FR-', 'SC-'):
                    if not any(key.startswith(prefix) for key, _ in definitions):
                        issues.append(f'Spec Kit requires meaningful {prefix} definitions in spec.md')
                stories = re.split(r'(?m)^### User Story (\d+)\s+[^\n]+', text)
                if len(stories) == 1:
                    issues.append('Spec Kit requires User Story N headings with Acceptance Scenarios')
                for i in range(1, len(stories), 2):
                    body = stories[i + 1].split('\n## ')[0]
                    acceptance = body.split('**Acceptance Scenarios**:', 1)
                    scenario_text = re.split(r'(?m)^### |^---\s*$', acceptance[1], maxsplit=1)[0] if len(acceptance) == 2 else ''
                    scenarios = re.findall(r'(?m)^\s*(\d+)\.([^\n]*)', scenario_text)
                    if any(line.strip() and not re.match(r'^\s*\d+\.', line) for line in scenario_text.splitlines()):
                        issues.append(f'Spec Kit User Story {stories[i]}: unrecognized scenario; use numbered Given/When/Then outcomes')
                    if not scenarios:
                        issues.append(f'Spec Kit User Story {stories[i]} has no numbered Acceptance Scenarios')
                    for number, outcome in scenarios:
                        parts = re.fullmatch(r'\s*\*\*Given\*\*(.+?)\*\*When\*\*(.+?)\*\*Then\*\*(.+)', outcome)
                        if not parts or not all(meaningful(part) for part in parts.groups()):
                            issues.append(f'Spec Kit scenario {stories[i]}.{number}: expected concrete Given/When/Then conditions')
                        definitions.append((f'US{stories[i]}-AC{number}', outcome))
                tasks = re.findall(r'(?m)^- \[[ xX]\] (T\d{3})\b[^\n]+', texts['tasks'])
                if len(re.findall(r'(?m)^- \[[ xX]\]', texts['tasks'])) != len(tasks):
                    issues.append('unrecognized Spec Kit task: use - [ ] T001 followed by work to perform')
                if not tasks:
                    issues.append('Spec Kit tasks.md requires checkbox tasks with T001-style IDs')
                if not re.search(r'(?m)^# .+\S', texts['plan']):
                    issues.append('Spec Kit plan.md requires a nonempty plan with a title')
    else:
        issues.append(f'unsupported {tier} artifact structure; use the documented tier layout')

    for key, body in definitions:
        if not meaningful(body):
            issues.append(f'{key}: empty or unresolved criterion; write a concrete observable outcome')
    duplicates = [key for key, count in Counter(key for key, _ in definitions).items() if count > 1]
    if duplicates:
        issues.append('duplicate criterion IDs: ' + ', '.join(duplicates))
    if len(tasks) != len(set(tasks)):
        issues.append('duplicate task IDs')
    criteria = sorted({key for key, body in definitions if meaningful(body)})
    if not criteria:
        issues.append('no meaningful acceptance criteria discovered; define TinySpec R-XX, LiteSpec AC-XX.N, or supported Spec Kit scenarios and FR/SC outcomes')
    return criteria, sorted(set(tasks)), issues
