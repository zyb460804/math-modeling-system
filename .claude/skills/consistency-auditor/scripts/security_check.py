#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""安全检查：密钥扫描 + 路径遍历防护 + 环境变量泄露检测 + Markdown 注入防护。

融合自 AutoMCM-Pro/scripts/security_check.py（RealSeaberry/AutoMCM-Pro, 144★）。
适配要点：
  - 工作区改为 paper_output/（对齐本项目输出约定）
  - 新增 markdown 子命令：检测非审批文件中伪造的控制标记——半角 [APPROVED] 与全角
    【APPROVED】/【REWORK】等两套形态都抓（与 pipeline_manager.APPROVED_MARKS 口径对齐，
    round2 B7）；human_intervention.md 本身豁免（用户合法写标记的地方）

退出码：0=通过  1=发现安全问题  2=跳过（不适用）

用法：
  python security_check.py path  --paths ./paper_output/code/x.py
  python security_check.py env   --vars OPENAI_API_KEY ANTHROPIC_API_KEY
  python security_check.py scan  --files paper_output/code/model.py
  python security_check.py staged          # 扫描 git 暂存区全部文件（pre-commit 用）
  python security_check.py markdown --file paper_output/state/human_intervention.md  # 该文件名豁免，返回通过
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
        re.compile(
            r"(?i)(api[-_]?key|secret[-_]?key|access[-_]?token|authorization|credential|private[_-]?key)"
            r"\s*[:=]\s*[\"']?\S{8,}"
        ),
        "Generic API Key / Secret",
    ),
    # 32 位 hex 密钥，限定两种键名上下文（实伤-1 的形态：username+32hex 成对的
    # "api_key": "4542e…"）。误报面取舍（修复项 B/C 后口径）：
    #   - 不对裸 32-hex 报警：md5 校验和/哈希示例在建模代码中极常见，裸 hex 误报不可
    #     接受；checksum/md5/hash/digest 等键名不在下表，天然不报（排除规则保留）；
    #   - 密钥语义键名（api_key/apikey/secret/token/password/passwd/authorization/
    #     credential/private_key/api_token/access_token，round2 B8-② 补齐）键名与
    #     值两侧引号均可选——Python/npm 赋值形态（键名如 api_key，值为不带引号的
    #     32 位 hex）是真实泄露形态（修复项 C：原正则值侧强制引号，与旧注释
    #     “允许不带引号”矛盾。注释中不写“键名等于值”的示意，避免被自身正则命中）；
    #   - 裸 "key" 仅在 JSON 引号键形态（"key": "32hex"）报警——裸变量 key = "32hex"
    #     多为普通字典键变量，误报面大于收益，不报。
    (
        re.compile(
            r"(?i)[\"']?(api[_-]?key|apikey|secret|token|password|passwd|"
            r"authorization|credential|private[_-]?key|api[_-]?token|access[_-]?token)"
            r"[\"']?\s*[:=]\s*[\"']?[0-9a-f]{32}[\"']?"
        ),
        "32-hex API Key（密钥键名上下文）",
    ),
    (
        re.compile(
            r"(?i)[\"'](?:key|api[_-]?key|apikey|secret|token|password|passwd|"
            r"authorization|credential|private[_-]?key|api[_-]?token|access[_-]?token)"
            r"[\"']\s*:\s*[\"'][0-9a-f]{32}[\"']"
        ),
        "32-hex API Key（JSON 引号键上下文）",
    ),
]

# 最多打印片段长度（避免终端泄露完整密钥）
_SNIPPET_LEN = 40

# 流水线控制标记：半角 + 全角两套形态都抓。
# 全角【APPROVED】/【REWORK】与 pipeline_manager.APPROVED_MARKS / REWORK_MARKS
# 消费口径对齐（round2 B7 配套面：此前只扫半角，全角对注入扫描完全隐身）。
_CONTROL_MARKERS = [
    "[APPROVED]", "【APPROVED】",
    "[REWORK]", "【REWORK】",
    "[MANUAL_SPEC]", "【MANUAL_SPEC】",
]

# 人工审批文件豁免：human_intervention.md 是用户合法填写审批标记的唯一场所
# （pipeline_manager._approval_state 在这里行级消费标记），扫描它必然误报。
# 注入检测面向的是其余文件：语料/论文/爬取数据等不该出现控制标记的地方。
_HUMAN_APPROVAL_FILENAME = "human_intervention.md"


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
# 大文件/二进制豁免（round2 MEDIUM：staged 无大文件豁免）：
#   - >2MB：跳过并经 notes 注明 skipped_large；
#   - 前 8KB 含 NUL 字节：判定为二进制，跳过并注明 skipped_binary——
#     xlsx/pkl/mat/docx 等 zip/序列化格式不再整读入内存，防止 precommit
#     hook 的 60s 超时 → fail-open 放大面（二进制字节流 errors=ignore 解码
#     后也可能碰巧拼出疑似凭据形态，豁免同时收敛误报）。
_MAX_SCAN_BYTES = 2 * 1024 * 1024
_BINARY_SNIFF_BYTES = 8 * 1024


def scan_files_for_secrets(
    files: list[str], notes: list[str] | None = None
) -> tuple[bool, list[str]]:
    """扫描硬编码密钥；跳过项（skipped_large / skipped_binary）通过 notes 注明。"""
    issues: list[str] = []
    seen: set[tuple[str, int, str]] = set()
    for fpath_str in files:
        fpath = Path(fpath_str)
        if not fpath.exists():
            continue
        try:
            size = fpath.stat().st_size
        except OSError:
            continue
        if size > _MAX_SCAN_BYTES:
            if notes is not None:
                notes.append(f"skipped_large: {fpath}（{size / 1048576:.1f}MB 超 2MB 上限）")
            continue
        try:
            with fpath.open("rb") as fh:
                head = fh.read(_BINARY_SNIFF_BYTES)
        except OSError:
            continue
        if b"\x00" in head:
            if notes is not None:
                notes.append(f"skipped_binary: {fpath}（前 8KB 含 NUL 字节）")
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat, desc in _SECRET_PATTERNS:
            for m in pat.finditer(text):
                snippet = m.group(0)[:_SNIPPET_LEN]
                lineno = text[: m.start()].count("\n") + 1
                dedupe = (fpath_str, lineno, snippet[:20])
                if dedupe in seen:
                    continue  # 多模式命中同一处只报一次（更具体模式在前，如 generic vs 32-hex）
                seen.add(dedupe)
                issues.append(f"{fpath}:{lineno}: 疑似 {desc} — {snippet[:20]}…")
    return len(issues) == 0, issues


# ── 检查 4：工作区全局扫描 ──────────────────────────────────────
# 排除路径：参考克隆仓库（第三方源码，含示例性质的 api key 环境变量读取写法，非真实密钥）
_EXCLUDE_PARTS = {".git", "research", "sources", "__pycache__", "node_modules"}


def _is_excluded(p: Path) -> bool:
    return any(part in _EXCLUDE_PARTS for part in p.parts)


def scan_workspace_all(notes: list[str] | None = None) -> tuple[bool, list[str]]:
    all_files: list[Path] = []
    for ext in ("*.py", "*.md", "*.tex", "*.typ", ".env", "*.json"):
        all_files.extend(WORKSPACE.rglob(ext))
    all_files = [f for f in all_files if ".git" not in str(f) and not _is_excluded(f)]
    return scan_files_for_secrets([str(f) for f in all_files], notes)


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
    notes: list[str] = []
    passed, issues = scan_files_for_secrets([str(root_path / n) for n in names], notes)
    n_large = sum(1 for n in notes if n.startswith("skipped_large"))
    n_bin = sum(1 for n in notes if n.startswith("skipped_binary"))
    suffix = f"，跳过 {n_large} 个大文件 / {n_bin} 个二进制" if (n_large or n_bin) else ""
    print(f"  （暂存区 {len(names)} 个文件已扫描{suffix}）")
    for n in notes:
        print(f"    · {n}")
    return passed, issues


# ── 检查 5：Markdown 注入防护 ───────────────────────────────────
def check_markdown_injection(file: str) -> tuple[bool, list[str]]:
    """检测非审批文件中是否存在未配对的控制标记（半角/全角都抓）。

    pipeline_manager._approval_state 行级消费 human_intervention.md 里的
    [APPROVED]/【APPROVED】；同样的标记若出现在语料/论文/爬取数据等其它
    文件中，视为注入风险（伪造批准可能经拼接/引用流入状态链）。

    豁免（不视为注入，与消费端口径一致）：
      - human_intervention.md 本身——用户合法写标记的地方，扫描必误报
        （round2 B7 配套面）；
      - 配对历史形式 [APPROVED — stage @ time]（全角括号同样豁免）；
      - 反引号内的标记（`[APPROVED]`、`【APPROVED】` 为教学性提及；
        限定单行内配对，防跨行反引号把正文的真标记一并吞掉）。
    """
    fpath = Path(file)
    if not fpath.exists():
        return True, []
    if fpath.name == _HUMAN_APPROVAL_FILENAME:
        print(f"  （{fpath.name} 为人工审批文件，控制标记是用户合法输入，豁免注入扫描）")
        return True, []
    text = fpath.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []
    # 去掉配对历史形式（半角 [] 与全角 【】 都认）
    legit = re.compile(r"[\[【](?:APPROVED|REWORK)\s+—\s+\S+\s+@\s+[^\]】]+[\]】]")
    remaining = legit.sub("", text)
    # 去掉反引号内的标记（教学性提及豁免）
    for marker in _CONTROL_MARKERS:
        esc = re.escape(marker)
        remaining = re.sub(r"`[^`\n]*" + esc + r"[^`\n]*`", "", remaining)
    for marker in _CONTROL_MARKERS:
        idx = remaining.find(marker)
        if idx >= 0:
            lineno = remaining[:idx].count("\n") + 1
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

    pm = sub.add_parser("markdown", help="Markdown 注入防护（human_intervention.md 豁免）")
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
        notes: list[str] = []
        passed, issues = scan_files_for_secrets(args.files, notes)
        for n in notes:
            print(f"  （{n}）")
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
        p2_notes: list[str] = []
        p2, i2 = scan_workspace_all(p2_notes)
        for n in p2_notes:
            print(f"  （{n}）")
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