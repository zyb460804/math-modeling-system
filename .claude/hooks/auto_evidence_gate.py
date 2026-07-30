#!/usr/bin/env python3
"""PostToolUse hook: auto-run evidence gate when key files change.

Triggers when these files are written:
  - paper_output/results/*.json
  - paper_output/plan/model_route.json
  - paper_output/tables/table_index.json
  - paper_output/figures/figure_index.json

Runs evidence_gate.py --mode quickstart in background.

Exit codes:
  0 = always (informational, never blocks)
"""
import sys
import json
import subprocess
import os
import re


TRIGGER_PATTERNS = [
    r"paper_output/results/.+\.json$",
    r"paper_output/plan/model_route\.json$",
    r"paper_output/tables/table_index\.json$",
    r"paper_output/figures/figure_index\.json$",
]

GATE_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(__file__),
    "..", "skills", "quality-assurance-auditor", "scripts", "evidence_gate.py"
))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    fp = file_path.replace("\\", "/")

    # Check if file matches any trigger pattern
    triggered = any(re.search(pat, fp) for pat in TRIGGER_PATTERNS)
    if not triggered:
        sys.exit(0)

    # Check if gate script exists
    if not os.path.isfile(GATE_SCRIPT):
        sys.exit(0)

    # Run in background (non-blocking)
    try:
        subprocess.Popen(
            [sys.executable, GATE_SCRIPT, "--mode", "quickstart"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        print("[Hook] Evidence gate triggered (background)")
    except Exception as e:
        print(f"[Hook] Evidence gate launch failed: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()