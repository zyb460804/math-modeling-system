#!/usr/bin/env python3
"""PostToolUse hook: log non-zero exit codes from Bash commands.

Informational only -- never blocks.

Exit codes:
  0 = always (informational hook)
"""
import sys
import json


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    result = data.get("tool_result", {})
    exit_code = result.get("exitCode", 0)

    # Defensive: ensure int comparison
    try:
        exit_code = int(exit_code)
    except (ValueError, TypeError):
        exit_code = 0

    if exit_code != 0:
        print(f"[Hook] Bash exit code: {exit_code}")

    sys.exit(0)


if __name__ == "__main__":
    main()