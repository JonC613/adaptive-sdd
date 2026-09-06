#!/usr/bin/env python3
"""Validate LiteSpec metadata, ordering, IDs, and acceptance traceability."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path


ARTIFACTS = ("spec", "plan", "tests")
REQUIRED_METADATA = {"feature", "artifact", "status", "owner", "version", "created", "updated"}
ALLOWED_STATUSES = {"draft", "review", "approved", "implementing", "done"}
APPROVED_STATUSES = {"approved", "implementing", "done"}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.json_output = False

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def parse_frontmatter(path: Path, validation: Validation) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        validation.errors.append(f"{path.name}: missing YAML front matter")
        return {}, text
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        validation.errors.append(f"{path.name}: unclosed YAML front matter")
        return {}, text
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        validation.require(key.strip() not in metadata, f"META_DUPLICATE: {path.name}: duplicate metadata: {key.strip()}")
        metadata[key.strip()] = value.strip().strip('"\'')
    missing = sorted(key for key in REQUIRED_METADATA if not metadata.get(key))
    validation.require(not missing, f"{path.name}: missing metadata: {', '.join(missing)}")
    for field in ("created", "updated"):
        if field in metadata:
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata[field]):
                    raise ValueError()
                date.fromisoformat(metadata[field])
            except ValueError:
                validation.errors.append(f"{path.name}: {field} must be YYYY-MM-DD")
    validation.require(metadata.get("status") in ALLOWED_STATUSES, f"{path.name}: invalid status")
    validation.require(bool(re.fullmatch(r"\d+\.\d+", metadata.get("version", ""))), f"{path.name}: version must be major.minor")
    return metadata, text


def check_graph(text: str, acceptance: set[str], validation: Validation) -> None:
    blocks = re.split(r"(?m)^- \[[ xX]\] \*\*(P\d+-T\d+)\s+—", text)
    graph: dict[str, set[str]] = {}
    covered: set[str] = set()
    for i in range(1, len(blocks), 2):
        task, body = blocks[i], blocks[i + 1].split("\n## ")[0]
        dep = re.search(r"(?m)^\s*- Depends on:\s*([^\n]+)", body)
        validation.require(dep is not None, f"TASK_DEPENDENCY: {task}: missing Depends on")
        graph[task] = set(re.findall(r"P\d+-T\d+", dep[1])) if dep else set()
        if dep:
            validation.require(bool(graph[task]) or dep[1].strip() == "None", f"TASK_DEPENDENCY: {task}: expected task IDs or None")
        cover = re.search(r"(?m)^\s*- Covers:\s*([^\n]+)", body)
        validation.require(cover is not None, f"TASK_COVERAGE: {task}: missing Covers")
        if cover:
            ids = set(re.findall(r"AC-\d{2}\.\d+", cover[1]))
            validation.require(ids <= acceptance, f"TASK_COVERAGE: {task}: unknown acceptance IDs")
            covered.update(ids)
        for field in ("Work", "Verify"):
            validation.require(re.search(rf"(?m)^\s*- {field}:\s*\S", body) is not None, f"TASK_FIELD: {task}: missing {field}")
    validation.require(covered == acceptance, "TASK_COVERAGE: task Covers fields must cover every acceptance criterion")
    for task, dependencies in graph.items():
        validation.require(dependencies <= graph.keys(), f"TASK_DEPENDENCY: {task}: unknown dependency")
    pending = dict(graph)
    while pending:
        ready = {task for task, deps in pending.items() if not deps}
        if not ready:
            validation.require(False, "TASK_CYCLE: dependencies contain a cycle or unresolved reference")
            break
        pending = {task: deps - ready for task, deps in pending.items() if task not in ready}


REQUIRED_SECTIONS = {
    "spec": ("Summary", "Problem", "Desired outcome", "Requirements", "User stories", "Non-functional requirements", "Codebase context", "Assumptions and open questions", "Amendment history"),
    "plan": ("Technical approach", "Key decisions", "Impacted areas", "Implementation phases", "Amendment history"),
    "tests": ("Strategy", "Acceptance traceability", "Critical user flows", "Failure and recovery cases", "Manual exceptions", "Test data and setup", "Completion criteria", "Amendment history"),
}


def unique_ids(pattern: str, text: str, label: str, validation: Validation) -> set[str]:
    values = re.findall(pattern, text, flags=re.MULTILINE)
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    validation.require(not duplicates, f"Duplicate {label} IDs: {', '.join(duplicates)}")
    return set(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_dir", type=Path)
    parser.add_argument("--approved", action="store_true", help="Require all artifacts and approved-or-later status")
    parser.add_argument("--json", action="store_true", help="Emit structural diagnostics as JSON; does not verify delivery")
    args = parser.parse_args()

    feature_dir = args.feature_dir.resolve()
    validation = Validation()
    validation.json_output = args.json
    validation.require(feature_dir.is_dir(), f"Feature directory does not exist: {feature_dir}")
    if not feature_dir.is_dir():
        finish(validation)

    paths = {name: feature_dir / f"{name}.md" for name in ARTIFACTS}
    existing = {name: path for name, path in paths.items() if path.is_file()}
    validation.require("spec" in existing, "spec.md is required")
    if "plan" in existing:
        validation.require("spec" in existing, "plan.md requires spec.md")
    if "tests" in existing:
        validation.require("plan" in existing, "tests.md requires plan.md")
    if args.approved:
        validation.require(set(existing) == set(ARTIFACTS), "--approved requires spec.md, plan.md, and tests.md")

    metadata: dict[str, dict[str, str]] = {}
    content: dict[str, str] = {}
    for name, path in existing.items():
        metadata[name], content[name] = parse_frontmatter(path, validation)
        for section in REQUIRED_SECTIONS[name]:
            validation.require(re.search(rf"(?mi)^## {re.escape(section)}\s*$", content[name]) is not None, f"SECTION_MISSING: {path.name}: {section}")
        validation.require(metadata[name].get("artifact") == name, f"{path.name}: artifact metadata must be {name}")
        validation.require(metadata[name].get("feature") == feature_dir.name, f"{path.name}: feature must match directory name")
        if args.approved:
            validation.require(metadata[name].get("status") in APPROVED_STATUSES, f"{path.name}: explicit approval is required")
            validation.require(not re.search(r"<(?:feature|Feature|owner|approved-)", content[name]), f"{path.name}: unresolved template placeholder")

    if "plan" in metadata and "spec" in metadata:
        validation.require(metadata["plan"].get("spec_version") == metadata["spec"].get("version"), "plan.md spec_version does not match spec.md")
    if "tests" in metadata and "plan" in metadata and "spec" in metadata:
        validation.require(metadata["tests"].get("spec_version") == metadata["spec"].get("version"), "tests.md spec_version does not match spec.md")
        validation.require(metadata["tests"].get("plan_version") == metadata["plan"].get("version"), "tests.md plan_version does not match plan.md")

    acceptance_ids: set[str] = set()
    if "spec" in content:
        story_ids = unique_ids(r"^###\s+(US-\d{2})\b", content["spec"], "story", validation)
        acceptance_ids = unique_ids(r"\*\*(AC-\d{2}\.\d+):\*\*", content["spec"], "acceptance", validation)
        validation.require(bool(story_ids), "spec.md has no user story IDs")
        validation.require(bool(acceptance_ids), "spec.md has no acceptance criterion IDs")
        for acceptance_id in acceptance_ids:
            story_id = f"US-{acceptance_id[3:5]}"
            validation.require(story_id in story_ids, f"{acceptance_id} has no matching {story_id}")

    if "plan" in content:
        check_graph(content["plan"], acceptance_ids, validation)
        task_ids = unique_ids(r"\*\*(P\d+-T\d+)\s+—", content["plan"], "task", validation)
        validation.require(bool(task_ids), "plan.md has no task IDs")
        for acceptance_id in sorted(acceptance_ids):
            validation.require(acceptance_id in content["plan"], f"plan.md does not reference {acceptance_id}")

    if "tests" in content:
        test_ids = unique_ids(r"^###\s+([TM]-\d{2})\b", content["tests"], "test", validation)
        parts = re.split(r"(?m)^###\s+([TM]-\d{2})\b", content["tests"])
        coverage = {}
        for i in range(1, len(parts), 2):
            fields = re.findall(r"(?m)^\s*- Covers:\s*([^\n]+)", parts[i + 1].split("\n## ")[0])
            coverage[parts[i]] = set(re.findall(r"AC-\d{2}\.\d+", " ".join(fields)))
        trace_rows = re.findall(r"^\|\s*(AC-\d{2}\.\d+)\s*\|\s*([^|]+)\|", content["tests"], flags=re.MULTILINE)
        trace_acceptance = [row[0] for row in trace_rows]
        duplicate_trace = sorted(value for value, count in Counter(trace_acceptance).items() if count > 1)
        validation.require(not duplicate_trace, f"Duplicate traceability rows: {', '.join(duplicate_trace)}")
        validation.require(set(trace_acceptance) == acceptance_ids, "tests.md traceability rows must exactly match spec.md acceptance IDs")
        referenced_tests = {value for _, cell in trace_rows for value in re.findall(r"[TM]-\d{2}", cell)}
        for ac, cell in trace_rows:
            refs = re.findall(r"[TM]-\d{2}", cell)
            validation.require(bool(refs), f"TRACE_EMPTY: {ac}: expected test or manual exception IDs")
            for ref in refs:
                validation.require(ac in coverage.get(ref, set()), f"TRACE_MISMATCH: {ac}: {ref} does not cover this criterion")
        for test_id in sorted(referenced_tests):
            validation.require(test_id in test_ids, f"Traceability references missing test {test_id}")
        for acceptance_id in sorted(acceptance_ids):
            validation.require(re.search(rf"Covers:\s*[^\n]*\b{re.escape(acceptance_id)}\b", content["tests"]) is not None, f"No test case covers {acceptance_id}")

    finish(validation, len(acceptance_ids), len(existing))


def finish(validation: Validation, acceptance_count: int = 0, artifact_count: int = 0) -> None:
    if validation.json_output:
        print(json.dumps({"schema_version": 1, "kind": "structural", "valid": not validation.errors,
                          "diagnostics": [{"code": e.split(":", 1)[0] if re.match(r"^[A-Z_]+:", e) else "STRUCTURE_INVALID", "message": e} for e in validation.errors],
                          "artifact_count": artifact_count, "acceptance_count": acceptance_count}))
        raise SystemExit(1 if validation.errors else 0)
    if validation.errors:
        for error in validation.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: structural validation of {artifact_count} artifact(s) and {acceptance_count} acceptance criteria; delivery not verified")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
