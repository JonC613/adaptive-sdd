#!/usr/bin/env python3
"""Scaffold, inspect, validate, and reconcile Adaptive SDD Project Memory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


OKF_VERSION = "0.2"
PROFILE_VERSION = 1
SCHEMA_VERSION = 1
PRODUCER = "adaptive-sdd/0.3.0"
REQUIRED_MEMORY_FILES = ("index.md", "project.md", "architecture.md", "log.md")
CONCEPT_TYPES = {
    "project.md": "Software Repository",
    "architecture.md": "Software Architecture",
}
ACTOR_PATTERN = re.compile(r"^(?:human:|process:|[^/\s]+/)[^\s]+$")
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def git(project: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(project), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None


def git_head(project: Path) -> str | None:
    result = git(project, "rev-parse", "HEAD")
    if result is None or result.returncode != 0:
        return None
    return result.stdout.strip() or None


def commit_exists(project: Path, commit: str) -> bool:
    result = git(project, "cat-file", "-e", f"{commit}^{{commit}}")
    return result is not None and result.returncode == 0


def is_ancestor(project: Path, earlier: str, later: str) -> bool:
    result = git(project, "merge-base", "--is-ancestor", earlier, later)
    return result is not None and result.returncode == 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(str(exc)) from exc
    if not isinstance(value, dict):
        raise ValueError("root value must be an object")
    return value


def parse_value(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return ""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw.strip("'\"")


def frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("unclosed YAML frontmatter") from exc
    values: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace() or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        values[key.strip()] = parse_value(raw)
    return values, "\n".join(lines[end + 1 :])


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def level(self) -> str:
        if self.errors:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"

    def emit(self) -> None:
        for message in self.errors:
            print(f"ERROR: {message}")
        for message in self.warnings:
            print(f"WARN: {message}")
        print(f"{self.level}: Project Memory validation")


def validate_actor(value: Any, label: str, report: Report) -> None:
    if not isinstance(value, str) or not ACTOR_PATTERN.fullmatch(value):
        report.error(f"{label} must use an OKF actor identifier")


def resolve_resource(project: Path, bundle: Path, document: Path, resource: str) -> Path | None:
    parsed = urlparse(resource)
    if parsed.scheme:
        return None
    if resource.startswith("/"):
        target = bundle / resource.lstrip("/")
    else:
        target = document.parent / resource
    resolved = target.resolve()
    try:
        resolved.relative_to(project)
    except ValueError:
        return Path("__outside_project__")
    return resolved


def validate_links(project: Path, bundle: Path, document: Path, body: str, report: Report, required: bool) -> None:
    for raw_target in LINK_PATTERN.findall(body):
        target_text = raw_target.split("#", 1)[0].strip()
        if not target_text or urlparse(target_text).scheme:
            continue
        target = resolve_resource(project, bundle, document, target_text)
        if target == Path("__outside_project__"):
            report.error(f"{document.name}: link escapes repository: {raw_target}")
        elif target is not None and not target.exists():
            message = f"{document.name}: broken link: {raw_target}"
            report.error(message) if required else report.warn(message)


def validate_concept(project: Path, bundle: Path, path: Path, report: Report) -> None:
    try:
        meta, body = frontmatter(path)
    except (OSError, ValueError) as exc:
        report.error(f"{path.name}: {exc}")
        return
    expected_type = CONCEPT_TYPES[path.name]
    if meta.get("type") != expected_type:
        report.error(f"{path.name}: type must be {expected_type!r}")
    for key in ("title", "description"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            report.error(f"{path.name}: {key} is required")
    if meta.get("status", "stable") not in {"draft", "stable", "deprecated"}:
        report.error(f"{path.name}: invalid OKF status")

    generated = meta.get("generated")
    if not isinstance(generated, dict):
        report.error(f"{path.name}: generated must be an inline object")
    else:
        validate_actor(generated.get("by"), f"{path.name}: generated.by", report)
        if not parse_time(generated.get("at")):
            report.error(f"{path.name}: generated.at must be an ISO 8601 timestamp with offset")

    verified = meta.get("verified")
    if verified is not None:
        entries = verified if isinstance(verified, list) else [verified]
        if not entries or not all(isinstance(entry, dict) for entry in entries):
            report.error(f"{path.name}: verified must be an object or non-empty list of objects")
        else:
            for index, entry in enumerate(entries):
                validate_actor(entry.get("by"), f"{path.name}: verified[{index}].by", report)
                if not parse_time(entry.get("at")):
                    report.error(f"{path.name}: verified[{index}].at must be an ISO 8601 timestamp with offset")

    sdd = meta.get("sdd")
    if not isinstance(sdd, dict) or sdd.get("profile_version") != PROFILE_VERSION:
        report.error(f"{path.name}: sdd.profile_version must be {PROFILE_VERSION}")
    sources = meta.get("sources")
    if not isinstance(sources, list) or not sources:
        report.error(f"{path.name}: at least one source is required")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict) or not isinstance(source.get("resource"), str):
                report.error(f"{path.name}: sources[{index}].resource is required")
                continue
            target = resolve_resource(project, bundle, path, source["resource"])
            if target == Path("__outside_project__"):
                report.error(f"{path.name}: source escapes repository: {source['resource']}")
            elif target is not None and not target.exists():
                report.error(f"{path.name}: missing source: {source['resource']}")
    validate_links(project, bundle, path, body, report, required=False)


def collect_report(project: Path) -> Report:
    report = Report()
    bundle = project / ".sdd" / "memory"
    state_path = project / ".sdd" / "memory-state.json"
    if not bundle.is_dir():
        report.error("missing .sdd/memory directory")
        return report
    for name in REQUIRED_MEMORY_FILES:
        if not (bundle / name).is_file():
            report.error(f"missing .sdd/memory/{name}")
    index = bundle / "index.md"
    if index.is_file():
        try:
            meta, body = frontmatter(index)
            if str(meta.get("okf_version")) != OKF_VERSION:
                report.error(f"index.md: okf_version must be {OKF_VERSION}")
            validate_links(project, bundle, index, body, report, required=True)
        except (OSError, ValueError) as exc:
            report.error(f"index.md: {exc}")
    for name in CONCEPT_TYPES:
        path = bundle / name
        if path.is_file():
            validate_concept(project, bundle, path, report)
    log_path = bundle / "log.md"
    if log_path.is_file():
        log_text = log_path.read_text(encoding="utf-8")
        if not log_text.startswith("# Project Memory Update Log"):
            report.error("log.md: missing update-log heading")
        for heading in re.findall(r"^##\s+(.+)$", log_text, flags=re.MULTILINE):
            try:
                datetime.strptime(heading, "%Y-%m-%d")
            except ValueError:
                report.error(f"log.md: date heading must be YYYY-MM-DD: {heading}")
        validate_links(project, bundle, log_path, log_text, report, required=False)

    state: dict[str, Any] | None = None
    if not state_path.is_file():
        report.error("missing .sdd/memory-state.json")
    else:
        try:
            state = load_json(state_path)
        except ValueError as exc:
            report.error(f"memory-state.json: {exc}")
    if state is not None:
        expected = {
            "schema_version": SCHEMA_VERSION,
            "okf_version": OKF_VERSION,
            "profile_version": PROFILE_VERSION,
        }
        for key, value in expected.items():
            if state.get(key) != value:
                report.error(f"memory-state.json: {key} must be {value!r}")
        reconciled = state.get("last_reconciled_commit")
        reconciled_at = state.get("last_reconciled_at")
        if reconciled_at is not None and not parse_time(reconciled_at):
            report.error("memory-state.json: last_reconciled_at must be null or an ISO 8601 timestamp with offset")
        head = git_head(project)
        if head is None:
            report.warn("Git history unavailable; reconciliation confidence is limited")
        elif reconciled is None:
            report.warn("No reconciled Git commit is recorded")
        elif not isinstance(reconciled, str) or not commit_exists(project, reconciled):
            report.error("memory-state.json: last_reconciled_commit is not available in this Git history")
        elif reconciled != head:
            report.warn(f"Memory may be stale: reconciled {reconciled[:12]}, HEAD {head[:12]}")
    return report


def asset_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "memory"


def render_asset(name: str, replacements: dict[str, str]) -> str:
    path = asset_dir() / name
    if not path.is_file():
        fail(f"Bundled memory asset is missing: {path}")
    output = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        output = output.replace(f"{{{{{old}}}}}", new)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", output)
    if unresolved:
        fail(f"Unresolved asset placeholders in {name}: {', '.join(sorted(set(unresolved)))}")
    return output


def command_scaffold(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    if not project.is_dir():
        fail(f"Project does not exist: {project}")
    sdd = project / ".sdd"
    bundle = sdd / "memory"
    state_path = sdd / "memory-state.json"
    if bundle.exists() or state_path.exists():
        fail("Project Memory already exists; refusing to overwrite")
    if args.verified_by and not ACTOR_PATTERN.fullmatch(args.verified_by):
        fail("--verified-by must use an OKF actor identifier such as human:owner")

    generated_at = now_utc()
    head = git_head(project)
    source = "../../README.md" if (project / "README.md").is_file() else "../.."
    sources = json.dumps(
        [{"id": "repository", "resource": source, "title": "Repository evidence"}],
        separators=(",", ":"),
    )
    generated = json.dumps({"by": PRODUCER, "at": generated_at}, separators=(",", ":"))
    verified_line = ""
    if args.verified_by:
        verified = json.dumps([{"by": args.verified_by, "at": generated_at}], separators=(",", ":"))
        verified_line = f"verified: {verified}\n"
    title = args.title or project.name
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    replacements = {
        "PROJECT_TITLE": safe_title,
        "GENERATED": generated,
        "GENERATED_AT": generated_at,
        "VERIFIED_LINE": verified_line,
        "SOURCES": sources,
        "DATE": generated_at[:10],
        "COMMIT": json.dumps(head),
    }

    sdd.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".memory-", dir=sdd))
    try:
        staged_bundle = temporary / "memory"
        staged_bundle.mkdir()
        for name in REQUIRED_MEMORY_FILES:
            (staged_bundle / name).write_text(render_asset(name, replacements), encoding="utf-8", newline="\n")
        staged_state = temporary / "memory-state.json"
        staged_state.write_text(render_asset("state.json", replacements), encoding="utf-8", newline="\n")
        staged_bundle.replace(bundle)
        staged_state.replace(state_path)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    print(bundle)


def command_status(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    state_path = project / ".sdd" / "memory-state.json"
    if not state_path.is_file():
        fail("Project Memory state does not exist")
    try:
        state = load_json(state_path)
    except ValueError as exc:
        fail(f"Invalid Project Memory state: {exc}")
    head = git_head(project)
    reconciled = state.get("last_reconciled_commit")
    print(f"Profile: {state.get('profile_version')}")
    print(f"Last reconciled: {reconciled or 'none'}")
    print(f"HEAD: {head or 'unavailable'}")
    if head is None:
        print("WARN: Git history unavailable; reconciliation confidence is limited")
    elif reconciled == head:
        print("PASS: Project Memory is reconciled with HEAD")
    else:
        print("WARN: Project Memory may require reconciliation")


def command_verify(args: argparse.Namespace) -> None:
    report = collect_report(args.project.resolve())
    report.emit()
    raise SystemExit(1 if report.errors else 0)


def command_reconcile(args: argparse.Namespace) -> None:
    project = args.project.resolve()
    state_path = project / ".sdd" / "memory-state.json"
    if not state_path.is_file():
        fail("Project Memory state does not exist")
    if not commit_exists(project, args.commit):
        fail(f"Commit is not available in this repository: {args.commit}")
    head = git_head(project)
    if head is None or not is_ancestor(project, args.commit, head):
        fail("Reconciliation commit must be reachable from current HEAD")
    try:
        state = load_json(state_path)
    except ValueError as exc:
        fail(f"Invalid Project Memory state: {exc}")
    previous = state.get("last_reconciled_commit")
    if isinstance(previous, str) and commit_exists(project, previous) and not is_ancestor(project, previous, args.commit):
        fail("Reconciliation cannot move backward or to an unrelated commit")
    report = collect_report(project)
    if report.errors:
        report.emit()
        fail("Project Memory must validate before reconciliation")
    state["last_reconciled_commit"] = args.commit
    state["last_reconciled_at"] = now_utc()
    temporary = state_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(state_path)
    print(f"Reconciled Project Memory at {args.commit}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold = subparsers.add_parser("scaffold", help="Create an approved minimal Project Memory bundle")
    scaffold.add_argument("--project", type=Path, default=Path.cwd())
    scaffold.add_argument("--title")
    scaffold.add_argument("--verified-by")
    scaffold.set_defaults(handler=command_scaffold)

    status = subparsers.add_parser("status", help="Report reconciliation state without changing files")
    status.add_argument("--project", type=Path, default=Path.cwd())
    status.set_defaults(handler=command_status)

    verify = subparsers.add_parser("verify", help="Validate Project Memory and its evidence")
    verify.add_argument("--project", type=Path, default=Path.cwd())
    verify.set_defaults(handler=command_verify)

    reconcile = subparsers.add_parser("reconcile", help="Record an approved, validated reconciliation commit")
    reconcile.add_argument("--project", type=Path, default=Path.cwd())
    reconcile.add_argument("--commit", required=True)
    reconcile.set_defaults(handler=command_reconcile)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
