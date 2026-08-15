#!/usr/bin/env python3
"""Validate TinySpec metadata, required sections, and requirement IDs."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


REQUIRED_SECTIONS = ("Summary", "Scope", "Requirements", "Implementation outline", "Verification", "Done when", "Amendment history")
ALLOWED_STATUSES = {"draft", "review", "approved", "implementing", "done"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--approved", action="store_true")
    args = parser.parse_args()
    path = args.artifact.resolve()
    if not path.is_file():
        raise SystemExit(f"ERROR: artifact does not exist: {path}")

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        errors.append("missing YAML front matter")
        metadata = {}
    else:
        metadata = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    for key in ("feature", "artifact", "status", "owner", "version", "created", "updated"):
        if not metadata.get(key):
            errors.append(f"missing metadata: {key}")
    if metadata.get("artifact") != "tiny":
        errors.append("artifact metadata must be tiny")
    if metadata.get("status") not in ALLOWED_STATUSES:
        errors.append("invalid status")
    if args.approved and metadata.get("status") not in {"approved", "implementing", "done"}:
        errors.append("explicit approval is required")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^## {re.escape(section)}\s*$", text, flags=re.MULTILINE | re.IGNORECASE):
            errors.append(f"missing section: {section}")

    requirement_ids = re.findall(r"\*\*(R-\d{2}):\*\*", text)
    duplicates = [value for value, count in Counter(requirement_ids).items() if count > 1]
    if not requirement_ids:
        errors.append("no requirement IDs")
    if duplicates:
        errors.append(f"duplicate requirement IDs: {', '.join(sorted(duplicates))}")
    if args.approved and re.search(r"<[^>]+>", text):
        errors.append("unresolved template placeholder")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"OK: validated TinySpec with {len(requirement_ids)} requirement(s)")


if __name__ == "__main__":
    main()
