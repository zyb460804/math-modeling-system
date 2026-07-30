#!/usr/bin/env python3
"""PostToolUse hook: auto-format .py files with black.

Only runs black if the edited file ends with .py.
Uses subprocess timeout to prevent hanging.

Exit codes:
  0 = success or skipped (non-.py file / black not installed)
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

    if not file_path.endswith(".py"):
        sys.exit(0)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "black", "--quiet", "--line-length", "100", file_path],
            timeout=30,
            capture_output=True,
            text=True,
        )
        # black exit code 0 = formatted, 1 = error, 123 = internal error
        if result.returncode not in (0, 1):
            print(f"[Hook] black exited with code {result.returncode}", file=sys.stderr)
    except FileNotFoundError:
        pass  # black not installed, skip silently
    except subprocess.TimeoutExpired:
        print(f"[Hook] black timed out for {file_path}", file=sys.stderr)
    except Exception:
        pass  # fail silently

    sys.exit(0)


if __name__ == "__main__":
    main()