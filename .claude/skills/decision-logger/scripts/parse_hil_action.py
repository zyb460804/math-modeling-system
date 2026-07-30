#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解析 human_intervention.md 中的 HIL 动作标记，返回结构化决策。

融合自 jihe520/MathModelAgent 的 HIL 6 动作机制。
被 pipeline_manager.py 的 check-approval 扩展调用，或独立运行。

动作：confirm/edit/regenerate/ask/skip/abort
用法：
  python parse_hil_action.py                    # 读默认 human_intervention.md
  python parse_hil_action.py --file <path>      # 指定文件
输出（stdout）：一行 JSON，如：
  {"action":"confirm","arg":""}
  {"action":"edit","arg":"把摘要第2段改为..."}
  {"action":"pending"}                          # 无标记
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

DEFAULT_FILE = Path("paper_output/state/human_intervention.md")

# 动作优先级（文件中出现多个标记时，取优先级最高的）
# abort > skip > regenerate > edit > ask > confirm
ACTIONS = [
    ("abort", re.compile(r"\[ABORT\](.*)")),
    ("skip", re.compile(r"\[SKIP\](.*)")),
    ("regenerate", re.compile(r"\[REGENERATE\](.*)")),
    ("rework", re.compile(r"\[REWORK\](.*)")),     # 兼容旧标记
    ("edit", re.compile(r"\[EDIT\](.*)")),
    ("ask", re.compile(r"\[ASK\](.*)")),
    ("confirm", re.compile(r"\[APPROVED\](.*)")),
]

# 排除 advance 后的配对形式（[APPROVED — stage @ time]）
LEGIT_PAIRED = re.compile(r"\[(APPROVED|REWORK)\s+—\s+\S+\s+@\s+[^\]]+\]")


def parse(text: str) -> dict:
    cleaned = LEGIT_PAIRED.sub("", text)
    for action, pat in ACTIONS:
        m = pat.search(cleaned)
        if m:
            return {"action": action, "arg": m.group(1).strip()}
    return {"action": "pending", "arg": ""}


def main() -> int:
    p = argparse.ArgumentParser(description="解析 HIL 6 动作标记")
    p.add_argument("--file", default=str(DEFAULT_FILE))
    args = p.parse_args()
    f = Path(args.file)
    if not f.exists():
        print(json.dumps({"action": "pending", "arg": ""}, ensure_ascii=False))
        return 0
    result = parse(f.read_text(encoding="utf-8", errors="ignore"))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())