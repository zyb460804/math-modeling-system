#!/usr/bin/env python3
"""Stop hook: remind to update INDEX.md if outputs/ was modified.

Checks if any files in outputs/ were changed during the session.
If so, prints a reminder (advisory only, never blocks).

Exit codes:
  0 = always (advisory hook)
"""
import sys
import json
import os


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Check tool history for outputs/ modifications
    history = data.get("tool_history", [])
    outputs_modified = False

    for entry in history:
        tool = entry.get("tool", "")
        if tool not in ("Write", "Edit"):
            continue
        file_path = entry.get("tool_input", {}).get("file_path", "")
        fp = file_path.replace("\\", "/")
        if fp.startswith("outputs/") and not fp.endswith("INDEX.md"):
            outputs_modified = True
            break

    if outputs_modified:
        print("[Hook] outputs/ was modified this session -- consider running '建规则库' to update INDEX.md")

    sys.exit(0)


if __name__ == "__main__":
    main()