#!/usr/bin/env python3
"""Create one LiteSpec artifact while enforcing approval-gate order."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


ALLOWED_READY_STATUSES = {"approved", "implementing", "done"}
ARTIFACTS = ("spec", "plan", "tests")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        fail(f"Required artifact does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"Missing YAML front matter: {path}")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        fail(f"Unclosed YAML front matter: {path}")
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def require_approved(path: Path) -> dict[str, str]:
    metadata = frontmatter(path)
    if metadata.get("status") not in ALLOWED_READY_STATUSES:
        fail(f"{path.name} must be approved before creating the next artifact")
    if not metadata.get("version"):
        fail(f"{path.name} has no version")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--feature", required=True, help="Lowercase feature slug")
    parser.add_argument("--title", required=True, help="Human-readable feature name")
    parser.add_argument("--artifact", required=True, choices=ARTIFACTS)
    parser.add_argument("--owner", default="user")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.feature):
        fail("Feature must use lowercase letters, digits, and single hyphens")

    project = args.project.resolve()
    feature_dir = project / ".litespec" / args.feature
    destination = feature_dir / f"{args.artifact}.md"
    if destination.exists():
        fail(f"Refusing to overwrite existing artifact: {destination}")

    spec_meta: dict[str, str] = {}
    plan_meta: dict[str, str] = {}
    if args.artifact in {"plan", "tests"}:
        spec_meta = require_approved(feature_dir / "spec.md")
    if args.artifact == "tests":
        plan_meta = require_approved(feature_dir / "plan.md")

    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "assets" / f"{args.artifact}.md"
    if not template.is_file():
        fail(f"Missing bundled template: {template}")

    today = date.today().isoformat()
    output = template.read_text(encoding="utf-8")
    replacements = {
        "<feature-slug>": args.feature,
        "<Feature name>": args.title,
        "<owner>": args.owner,
        "YYYY-MM-DD": today,
        "<approved-spec-version>": spec_meta.get("version", "<approved-spec-version>"),
        "<approved-plan-version>": plan_meta.get("version", "<approved-plan-version>"),
    }
    for old, new in replacements.items():
        output = output.replace(old, new)

    feature_dir.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8", newline="\n")
    print(destination)


if __name__ == "__main__":
    main()
