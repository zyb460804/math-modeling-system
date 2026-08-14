#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PreToolUse hook：git 提交前密钥拦截。

仅在 Bash 命令为 git commit（token 化判定，兼容 `git -c a=b commit`、
`git commit --amend`、复合命令 `git add . && git commit -m x`）时触发扫描，
其余 Bash 命令直接放行（零开销）。
扫描逻辑委托给 consistency-auditor/scripts/security_check.py staged 子命令
（扫描 git 暂存区全部文件，而非只扫 paper_output/）。
发现密钥 → 退出码 2（阻止提交，stderr 展示给用户）。

融合自 AutoMCM-Pro 的"密钥提交拦截"机制，接入方式遵循本项目 hooks 惯例
（与 protect_outputs.py / check_python.py 同级）。
"""
from __future__ import annotations

import json
import os
import re
import shlex
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


def _segment_is_git_commit(segment: str) -> bool:
    """判定单个命令段（已去掉 && ; || | 复合拼接）是否为 `git commit`。

    token 化后判定：首 token 为 git/git.exe（含绝对路径形式），跳过 git
    全局选项及其取值（-c a=b / -C path / --git-dir=x / --no-pager 等）后，
    首个子命令 token 为 "commit" 即命中。这覆盖旧版漏掉的 `git -c a=b commit`，
    也自然覆盖 `git commit --amend`（--amend 是 commit 的选项，子命令仍为 commit）。

    已知边界（判定为非 commit，不拦截）：
      - `git commit-tree`（子命令是 commit-tree，非 commit；与旧版口径一致）
      - `git --work-tree x commit` 这类空格取值的全局长选项（解析为子命令 "x"）
      - `GIT_DIR=x git commit`（环境变量前缀，首 token 非 git）
    """
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:  # 引号不配对等，退化为空白切分
        tokens = segment.split()
    if not tokens:
        return False
    first = os.path.basename(tokens[0].replace("\\", "/").strip('"')).lower()
    if first not in ("git", "git.exe"):
        return False
    i = 1
    while i < len(tokens):
        t = tokens[i]
        if t == "--":  # git 自身无 -- 分隔符，保守不判
            return False
        if t in ("-c", "-C", "--exec-path") and i + 1 < len(tokens):
            i += 2  # 跳过选项 + 其取值
            continue
        if t.startswith("--") and "=" in t:
            i += 1  # --git-dir=x 等自带取值
            continue
        if t.startswith("-"):
            i += 1  # 无参 flag（--no-pager / --bare / --literal-pathspecs …）
            continue
        return t == "commit"  # 首个非选项 token 即子命令
    return False


def _is_git_commit(command: str) -> bool:
    """判断 Bash 命令是否含 git commit（含复合命令 `git add . && git commit -m x`）。"""
    if not command or not command.strip():
        return False
    segments = re.split(r"&&|\|\||;|\|", command)
    return any(_segment_is_git_commit(seg.strip()) for seg in segments)


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

    # 是 git commit → 跑密钥扫描（--staged：扫 git 暂存区全部文件，
    # 旧版 all 只扫 paper_output/，.claude/ 等目录的密钥会漏过）
    scanner = SCANNER if SCANNER.exists() else SCANNER_FALLBACK
    if not scanner.exists():
        return 0  # 扫描器缺失，不阻断
    # 解释器优先项目 .venv（本机全局 python 是坏 venv，见环境备忘），兜底 sys.executable
    venv_py = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    interpreter = str(venv_py) if venv_py.exists() else sys.executable
    try:
        proc = subprocess.run(
            [interpreter, str(scanner), "staged"],
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