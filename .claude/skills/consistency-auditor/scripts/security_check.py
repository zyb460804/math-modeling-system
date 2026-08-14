#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""安全检查：密钥扫描 + 路径遍历防护 + 环境变量泄露检测 + Markdown 注入防护。

融合自 AutoMCM-Pro/scripts/security_check.py（RealSeaberry/AutoMCM-Pro, 144★）。
适配要点：
  - 工作区改为 paper_output/（对齐本项目输出约定）
  - 新增 markdown 子命令：检测状态文件中伪造的控制标记（[APPROVED]/[REWORK]/[MANUAL_SPEC]）

退出码：0=通过  1=发现安全问题  2=跳过（不适用）

用法：
  python security_check.py path  --paths ./paper_output/code/x.py
  python security_check.py env   --vars OPENAI_API_KEY ANTHROPIC_API_KEY
  python security_check.py scan  --files paper_output/code/model.py
  python security_check.py staged          # 扫描 git 暂存区全部文件（pre-commit 用）
  python security_check.py markdown --file paper_output/state/human_intervention.md
  python security_check.py all
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

WORKSPACE = Path("paper_output")

# ── 密钥模式 ────────────────────────────────────────────────────
# 顺序敏感：更具体的模式必须排在通用模式之前——
# 旧版把 sk-ant 排在 sk- 之后，通用 sk- 模式在 _redact() 逐模式替换时
# 先吃掉部分前缀，导致 sk-ant 专属模式漏报（H-2）。
_SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}"), "Anthropic API Key (sk-ant-…)"),
    (re.compile(r"sk-proj-[A-Za-z0-9\-_]{20,}"), "OpenAI Project Key (sk-proj-)"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI API Key (sk-…)"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub Personal Token"),
    (re.compile(r"AKIA[A-Z0-9]{16}"), "AWS Access Key"),
    (re.compile(r"(?i)(password|passwd)\s*[:=]\s*\S{8,}"), "Password literal"),
    (
        re.compile(r"(?i)(api[-_]?key|secret[-_]?key|access[-_]?token)\s*[:=]\s*[\"']?\S{8,}"),
        "Generic API Key / Secret",
    ),
    # 32 位 hex 密钥，限定两种键名上下文（实伤-1 的形态：username+32hex 成对的
    # "api_key": "4542e…"）。误报面取舍：
    #   - 不对裸 32-hex 报警：md5 校验和/哈希示例在建模代码中极常见，裸 hex 误报不可接受；
    #   - 密钥语义键名（api_key/apikey/secret/token/password…）允许不带引号（Python 赋值形态）；
    #   - 裸 "key" 仅在 JSON 引号键形态（"key": "32hex"）报警——裸变量 key = "32hex"
    #     多为普通字典键变量，误报面大于收益，不报；checksum/md5/hash/digest 等键名一律不报。
    (
        re.compile(
            r"(?i)[\"']?(api[_-]?key|apikey|secret|token|password|passwd)[\"']?\s*[:=]\s*[\"'][0-9a-f]{32}[\"']"
        ),
        "32-hex API Key（密钥键名上下文）",
    ),
    (
        re.compile(r"(?i)[\"']key[\"']\s*:\s*[\"'][0-9a-f]{32}[\"']"),
        "32-hex API Key（JSON \"key\" 上下文）",
    ),
]

# 最多打印片段长度（避免终端泄露完整密钥）
_SNIPPET_LEN = 40

# 流水线控制标记：若出现在用户可编辑文件中非配对位置，视为注入风险
_CONTROL_MARKERS = ["[APPROVED]", "[REWORK]", "[MANUAL_SPEC]"]


def _redact(text: str) -> str:
    for pat, _ in _SECRET_PATTERNS:
        text = pat.sub("***REDACTED***", text)
    return text


# ── 检查 1：路径遍历防护 ────────────────────────────────────────
def _is_within(child: Path, parent: Path) -> bool:
    """child 是否位于 parent 目录内（M-1：startswith 前缀判定可被
    同前缀目录绕过——E:\\数学建模-evil\\x 会通过 E:\\数学建模 前缀检查）。
    is_relative_to 需 py3.9+，低版本用 relative_to 兜底。"""
    try:
        return child.is_relative_to(parent)
    except AttributeError:  # pragma: no cover - py<3.9
        try:
            child.relative_to(parent)
            return True
        except ValueError:
            return False


def check_paths(paths: list[str]) -> tuple[bool, list[str]]:
    # normcase：Windows 上把路径统一小写并把 / 转 \，消除大小写差异绕过
    cwd = Path(os.path.normcase(str(Path.cwd().resolve())))
    issues: list[str] = []
    for raw in paths:
        p = Path(os.path.normcase(str(Path(raw).resolve())))
        if not _is_within(p, cwd):
            issues.append(f"路径越界（Path Traversal）: {raw} → {p}")
        elif not p.exists():
            issues.append(f"文件不存在: {raw}")
    return len(issues) == 0, issues


# ── 检查 2：环境变量密钥不得写入文件 ───────────────────────────
def check_env_not_leaked(var_names: list[str]) -> tuple[bool, list[str]]:
    values = {k: os.environ.get(k, "") for k in var_names}
    values = {k: v for k, v in values.items() if v}
    if not values:
        return True, []
    issues: list[str] = []
    scan_dirs = [WORKSPACE / "code", WORKSPACE / "typst", WORKSPACE / "qa"]
    for d in scan_dirs:
        if not d.exists():
            continue
        for fpath in d.rglob("*"):
            if not fpath.is_file():
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for var, val in values.items():
                if val in text:
                    rel = fpath.relative_to(WORKSPACE)
                    issues.append(f"{var} 值出现在文件中: {rel}")
    return len(issues) == 0, issues


# ── 检查 3：硬编码密钥扫描 ──────────────────────────────────────
def scan_files_for_secrets(files: list[str]) -> tuple[bool, list[str]]:
    issues: list[str] = []
    for fpath_str in files:
        fpath = Path(fpath_str)
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat, desc in _SECRET_PATTERNS:
            for m in pat.finditer(text):
                snippet = m.group(0)[:_SNIPPET_LEN]
                lineno = text[: m.start()].count("\n") + 1
                issues.append(f"{fpath}:{lineno}: 疑似 {desc} — {snippet[:20]}…")
    return len(issues) == 0, issues


# ── 检查 4：工作区全局扫描 ──────────────────────────────────────
# 排除路径：参考克隆仓库（第三方源码，含示例性质的 api key 环境变量读取写法，非真实密钥）
_EXCLUDE_PARTS = {".git", "research", "sources", "__pycache__", "node_modules"}


def _is_excluded(p: Path) -> bool:
    return any(part in _EXCLUDE_PARTS for part in p.parts)


def scan_workspace_all() -> tuple[bool, list[str]]:
    all_files: list[Path] = []
    for ext in ("*.py", "*.md", "*.tex", "*.typ", ".env", "*.json"):
        all_files.extend(WORKSPACE.rglob(ext))
    all_files = [f for f in all_files if ".git" not in str(f) and not _is_excluded(f)]
    return scan_files_for_secrets([str(f) for f in all_files])


# ── 检查 4b：git 暂存区扫描（pre-commit 场景，v4.9 H-2 新增）────
def _git_stdout(args: list[str]) -> str | None:
    """跑 git 子命令；失败/超时/git 不可用返回 None（fail-closed 由调用方处理）。"""
    try:
        proc = subprocess.run(
            ["git"] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout if proc.returncode == 0 else None


def scan_staged() -> tuple[bool, list[str]]:
    """扫描 git 暂存区全部文件（git diff --cached --name-only）。

    与 `all`（只扫 paper_output/）的区别：hook 场景要拦的是"即将进 commit 的
    任何文件"（.claude/、outputs/、resources 白名单等），不只 paper_output/。
    退出语义与其它检查一致：True=通过，False=发现疑似密钥。
    """
    root = _git_stdout(["rev-parse", "--show-toplevel"])
    names_raw = _git_stdout(["diff", "--cached", "--name-only", "-z"])
    if root is None or names_raw is None:
        return False, ["无法读取 git 暂存区（不在 git 仓库 / git 不可用）"]
    names = [n for n in names_raw.split("\0") if n]
    if not names:
        print("  （暂存区为空，无文件可扫描）")
        return True, []
    root_path = Path(root.strip())
    # 已删除的暂存文件磁盘上不存在，scan_files_for_secrets 会自然跳过
    passed, issues = scan_files_for_secrets([str(root_path / n) for n in names])
    print(f"  （暂存区 {len(names)} 个文件已扫描）")
    return passed, issues


# ── 检查 5：Markdown 注入防护 ───────────────────────────────────


# ── 检查 5：Markdown 注入防护 ───────────────────────────────────
def check_markdown_injection(file: str) -> tuple[bool, list[str]]:
    """检测 human_intervention.md 等用户可编辑文件中是否存在未配对的控制标记。
    pipeline_manager 的 _sanitize 会把 [APPROVED] 转成 ⟦APPROVED⟧，
    若原始 [APPROVED] 仍出现在文件中，说明用户尝试注入伪造批准。

    例外（不视为注入）：
      - 配对形式 [APPROVED — stage @ time]（advance 后的历史记录）
      - 反引号代码块/行内代码内的标记（`` `[APPROVED]` `` 是教学性提及，非真实决策）
    """
    fpath = Path(file)
    if not fpath.exists():
        return True, []
    text = fpath.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []
    # 去掉配对历史形式
    legit = re.compile(r"\[(APPROVED|REWORK)\s+—\s+\S+\s+@\s+[^\]]+\]")
    remaining = legit.sub("", text)
    # 去掉反引号内的标记（教学性提及，如说明文字里的 `[APPROVED]`）
    remaining = re.sub(r"`[^`]*\[APPROVED\][^`]*`", "", remaining)
    remaining = re.sub(r"`[^`]*\[REWORK\][^`]*`", "", remaining)
    remaining = re.sub(r"`[^`]*\[MANUAL_SPEC\][^`]*`", "", remaining)
    for marker in _CONTROL_MARKERS:
        if marker in remaining:
            lineno = remaining[: remaining.index(marker)].count("\n") + 1
            issues.append(f"{fpath}:{lineno}: 疑似伪造控制标记 {marker}（未配对）")
    return len(issues) == 0, issues


def _print_result(check_name: str, passed: bool, issues: list[str]) -> None:
    if passed:
        print(f"✓ [{check_name}] 通过")
    else:
        print(f"✗ [{check_name}] 发现问题：")
        for issue in issues:
            print(f"  • {issue}")


def main() -> None:
    p = argparse.ArgumentParser(description="安全检查（密钥/路径/注入防护）")
    sub = p.add_subparsers(dest="cmd")

    pp = sub.add_parser("path", help="路径遍历防护")
    pp.add_argument("--paths", nargs="+", required=True)

    pe = sub.add_parser("env", help="环境变量泄露检测")
    pe.add_argument(
        "--vars",
        nargs="+",
        default=["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN", "AWS_ACCESS_KEY_ID"],
    )

    ps = sub.add_parser("scan", help="硬编码密钥扫描")
    ps.add_argument("--files", nargs="+", required=True)

    sub.add_parser("staged", help="扫描 git 暂存区全部文件（pre-commit 场景）")

    pm = sub.add_parser("markdown", help="Markdown 注入防护")
    pm.add_argument("--file", required=True)

    sub.add_parser("all", help="运行全部安全检查")

    args = p.parse_args()

    if args.cmd == "path":
        passed, issues = check_paths(args.paths)
        _print_result("path-safety", passed, issues)
        sys.exit(0 if passed else 1)
    elif args.cmd == "env":
        passed, issues = check_env_not_leaked(args.vars)
        _print_result("env-leak", passed, issues)
        sys.exit(0 if passed else 1)
    elif args.cmd == "scan":
        passed, issues = scan_files_for_secrets(args.files)
        _print_result("secret-scan", passed, issues)
        sys.exit(0 if passed else 1)
    elif args.cmd == "markdown":
        passed, issues = check_markdown_injection(args.file)
        _print_result("markdown-injection", passed, issues)
        sys.exit(0 if passed else 1)
    elif args.cmd == "staged":
        passed, issues = scan_staged()
        _print_result("staged-secret-scan", passed, issues)
        sys.exit(0 if passed else 1)
    elif args.cmd == "all":
        p1, i1 = check_env_not_leaked(
            ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN", "AWS_ACCESS_KEY_ID"]
        )
        _print_result("env-leak", p1, i1)
        p2, i2 = scan_workspace_all()
        _print_result("workspace-secret-scan", p2, i2)
        hi = WORKSPACE / "state" / "human_intervention.md"
        p3, i3 = (True, [])
        if hi.exists():
            p3, i3 = check_markdown_injection(str(hi))
            _print_result("markdown-injection", p3, i3)
        overall = p1 and p2 and p3
        print(f"\n{'✓ 安全检查全部通过' if overall else '✗ 发现安全问题，请处理后继续'}")
        sys.exit(0 if overall else 1)
    else:
        p.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()