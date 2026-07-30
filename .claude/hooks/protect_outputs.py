#!/usr/bin/env python3
"""PreToolUse hook: block writes to protected directories.

Protected paths:
  - outputs/ (except INDEX.md)
  - .claude/ (all files)
  - resources/ (all files)

Exit codes:
  0 = allow (path not protected)
  2 = block (path is protected)
"""
import sys
import json
import os

# Project root: two levels up from hooks/
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # fail-open on parse error

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Normalize to relative path from project root
    fp = file_path.replace("\\", "/")
    if os.path.isabs(file_path):
        try:
            fp = os.path.relpath(os.path.normpath(file_path), PROJECT_ROOT).replace("\\", "/")
        except ValueError:
            # Different drive letters on Windows
            pass

    # Protected prefixes with optional exceptions
    rules = [
        ("outputs/", ["INDEX.md"]),      # block outputs/ except INDEX.md
        (".claude/", []),                 # block all .claude/ writes
        ("resources/", []),               # block all resources/ writes
    ]

    for prefix, exceptions in rules:
        if not fp.startswith(prefix):
            continue
        # Check if the file matches any exception
        basename = os.path.basename(fp)
        if basename in exceptions:
            sys.exit(0)  # allow exception
        sys.exit(2)  # block

    sys.exit(0)  # allow


if __name__ == "__main__":
    main()