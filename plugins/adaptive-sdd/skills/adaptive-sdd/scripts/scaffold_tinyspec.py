#!/usr/bin/env python3
"""Create one TinySpec without overwriting existing work."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--feature", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--owner", default="user")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.feature):
        raise SystemExit("ERROR: feature must use lowercase letters, digits, and single hyphens")

    destination = args.project.resolve() / ".tinyspec" / f"{args.feature}.md"
    if destination.exists():
        raise SystemExit(f"ERROR: refusing to overwrite existing artifact: {destination}")

    template = Path(__file__).resolve().parent.parent / "assets" / "tinyspec.md"
    if not template.is_file():
        raise SystemExit(f"ERROR: missing bundled template: {template}")

    today = date.today().isoformat()
    output = template.read_text(encoding="utf-8")
    replacements = {
        "<feature-slug>": args.feature,
        "<Feature name>": args.title,
        "<owner>": args.owner,
        "YYYY-MM-DD": today,
    }
    for old, new in replacements.items():
        output = output.replace(old, new)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8", newline="\n")
    print(destination)


if __name__ == "__main__":
    main()
