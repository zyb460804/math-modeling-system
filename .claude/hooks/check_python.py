#!/usr/bin/env python3
"""PostToolUse hook: Python syntax check on .py files.

Only runs py_compile if the edited file ends with .py.
Uses subprocess timeout to prevent hanging.

Exit codes:
  0 = success or skipped (non-.py file)
  1 = syntax error found
"""
import sys
import subprocess
import json
import os


def main():
    # Get file path from stdin JSON (Claude Code hook protocol)
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Only check .py files
    if not file_path.endswith(".py"):
        sys.exit(0)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            timeout=30,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[Hook] Python syntax error in {file_path}", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"[Hook] py_compile timed out for {file_path}", file=sys.stderr)
        sys.exit(0)  # don't block on timeout
    except Exception as e:
        print(f"[Hook] py_compile error: {e}", file=sys.stderr)
        sys.exit(0)  # don't block on unexpected errors

    sys.exit(0)


if __name__ == "__main__":
    main()