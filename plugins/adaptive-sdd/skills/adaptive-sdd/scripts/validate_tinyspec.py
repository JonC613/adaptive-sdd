#!/usr/bin/env python3
"""Validate TinySpec metadata, required sections, and requirement IDs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from validate_litespec import Validation, parse_frontmatter, finish


REQUIRED_SECTIONS = ("Summary", "Scope", "Requirements", "Implementation outline", "Verification", "Done when", "Amendment history")
ALLOWED_STATUSES = {"draft", "review", "approved", "implementing", "done"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--approved", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = args.artifact.resolve()
    validation = Validation()
    validation.json_output = args.json
    if not path.is_file():
        validation.errors.append(f"FILE_MISSING: artifact does not exist: {path}")
        finish(validation)
    metadata, text = parse_frontmatter(path, validation)
    errors = validation.errors

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
        finish(validation)
    finish(validation, len(requirement_ids), 1)


if __name__ == "__main__":
    main()
