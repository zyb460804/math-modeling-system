#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PreToolUse hook：git 提交前密钥拦截。

仅在 Bash 命令包含 "git commit" 时触发扫描，其余 Bash 命令直接放行（零开销）。
扫描逻辑委托给 consistency-auditor/scripts/security_check.py（密钥/路径/注入防护）。
发现密钥 → 退出码 2（阻止提交，stderr 展示给用户）。

融合自 AutoMCM-Pro 的"密钥提交拦截"机制，接入方式遵循本项目 hooks 惯例
（与 protect_outputs.py / check_python.py 同级）。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# 项目根 = .../数学建模（__file__ 在 .claude/hooks/ 下，parents[2]=项目根）
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCANNER = PROJECT_ROOT / ".claude" / "skills" / "consistency-auditor" / "scripts" / "security_check.py"
# 兜底：用工作目录相对路径
SCANNER_FALLBACK = Path("e:/数学建模/.claude/skills/consistency-auditor/scripts/security_check.py")


def _is_git_commit(command: str) -> bool:
    """判断 Bash 命令是否为 git commit（含 git commit -m / --amend 等）。"""
    if not command:
        return False
    # 容忍中间参数；排除 git commit-tree 等
    tokens = command.strip().split()
    if len(tokens) >= 2 and tokens[0] == "git" and tokens[1] == "commit":
        return True
    # 形如 "git add . && git commit -m ..."
    return " git commit" in (" " + command) or command.startswith("git commit")


def main() -> int:
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw:
        return 0  # 非 PreToolUse 调用，放行
    try:
        payload = json.loads(raw)
    except Exception:
        return 0  # 非 JSON，放行（不阻断正常工作）

    command = ""
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, dict):
        command = str(tool_input.get("command", ""))

    if not _is_git_commit(command):
        return 0  # 非 git commit，零开销放行

    # 是 git commit → 跑密钥扫描
    scanner = SCANNER if SCANNER.exists() else SCANNER_FALLBACK
    if not scanner.exists():
        return 0  # 扫描器缺失，不阻断
    try:
        proc = subprocess.run(
            [sys.executable, str(scanner), "all"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60, cwd=str(PROJECT_ROOT),
        )
    except Exception as e:
        # 扫描器异常不阻断提交（避免误伤），仅警告
        sys.stderr.write(f"[precommit-secret-guard] 扫描器异常，跳过: {e}\n")
        return 0

    if proc.returncode != 0:
        sys.stderr.write("[precommit-secret-guard] ✗ 检测到密钥/安全问题，已阻止 git commit：\n")
        sys.stderr.write(proc.stdout + proc.stderr)
        sys.stderr.write("\n请改用环境变量，从文件移除密钥后重新提交。\n")
        return 2  # 退出码 2 = 阻断，stderr 展示给用户
    return 0


if __name__ == "__main__":
    sys.exit(main())