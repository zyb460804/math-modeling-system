#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""安全检查：密钥扫描 + 路径遍历防护 + 环境变量泄露检测 + Markdown 注入防护。

融合自 AutoMCM-Pro/scripts/security_check.py（RealSeaberry/AutoMCM-Pro, 144★）。
适配要点：
  - 工作区改为 paper_output/（对齐本项目输出约定）
  - 新增 markdown 子命令：检测非审批文件中伪造的控制标记——半角 [APPROVED] 与全角
    【APPROVED】/【REWORK】等两套形态都抓（与 pipeline_manager.APPROVED_MARKS 口径对齐，
    round2 B7）；绑定形态 [APPROVED S5]/【REWORK S6_paper_writing】一并扫描（与
    pipeline_manager._APPROVED_BOUND_RE 消费口径对齐，round3 P1-10）；豁免仅限固定
    相对路径 paper_output/state/human_intervention.md（round3 P0-3 收窄：旧口径按
    文件名全局豁免，任意目录同名文件是注入盲区）
  - 大文件（>2MB）不再整文件跳过：截断扫描前 2MB + notes 注明 scanned_truncated
    （余量未扫，staged 摘要集中 ⚠ 列出）——旧口径 size>2MB → continue，尾部藏钥
    可整文件逃逸入库（round3 P0-2）；二进制嗅探（前 8KB 含 NUL）保留

退出码：0=通过  1=发现安全问题  2=跳过（不适用）

用法：
  python security_check.py path  --paths ./paper_output/code/x.py
  python security_check.py env   --vars OPENAI_API_KEY ANTHROPIC_API_KEY
  python security_check.py scan  --files paper_output/code/model.py
  python security_check.py staged          # 扫描 git 暂存区全部文件（pre-commit 用）
  python security_check.py markdown --file paper_output/state/human_intervention.md  # 该固定路径豁免，返回通过
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

# 绑定形态（round3 P1-10）：消费端 pipeline_manager._APPROVED_BOUND_RE /
# _REWORK_BOUND_RE 认 [APPROVED S5] / 【APPROVED S5_evidence_gate】（分隔含
# 空格/制表/全角空格，独占一行）——此前扫描端只认裸标记，“消费端认、扫描端
# 不扫”的错位使语料里伪造绑定形态完全隐身。扫描侧 token 放宽为任意非空白、
# 非括号字符序列（消费词表 [A-Za-z0-9_\-.]+ 的超集）：非豁免文件里任何绑定
# 形态都值得报警，宁多报不漏报。MANUAL_SPEC 无绑定形态消费，不纳入（对齐
# 消费端）。
_BOUND_SEP = r"[ \t　]+"
_BOUND_TOKEN = r"[^\s\[\]【】]+"
_CONTROL_BOUND_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(rf"\[APPROVED{_BOUND_SEP}{_BOUND_TOKEN}\]"), "[APPROVED <token>]"),
    (re.compile(rf"【APPROVED{_BOUND_SEP}{_BOUND_TOKEN}】"), "【APPROVED <token>】"),
    (re.compile(rf"\[REWORK{_BOUND_SEP}{_BOUND_TOKEN}\]"), "[REWORK <token>]"),
    (re.compile(rf"【REWORK{_BOUND_SEP}{_BOUND_TOKEN}】"), "【REWORK <token>】"),
]

# 人工审批文件豁免（round3 P0-3 收窄）：仅固定相对路径
# paper_output/state/human_intervention.md 豁免——pipeline_manager.HUMAN_FILE
# （STATE_DIR = paper_output/state）只消费这一处，是用户合法填写审批标记的唯一
# 场所，扫描它必然误报。旧口径按文件名（fpath.name）全局豁免，任意目录同名文件
# （如 crawled_data/human_intervention.md）都是注入盲区（round3 B6 实测得手）；
# 收窄后其余目录同名文件照扫。
_HUMAN_APPROVAL_RELPATH = Path("state") / "human_intervention.md"


def _is_human_approval_file(fpath: Path) -> bool:
    """fpath 是否恰为 WORKSPACE 下的 state/human_intervention.md。

    normcase 消除 Windows 大小写/斜杠差异；不在 paper_output/state/ 精确位置的
    同名文件一律不豁免。与 pipeline_manager 的相对路径消费约定一致（cwd=项目根）。
    """
    fp = Path(os.path.normcase(str(fpath.resolve())))
    ws = Path(os.path.normcase(str(WORKSPACE.resolve())))
    try:
        rel = fp.relative_to(ws)
    except ValueError:
        return False
    return rel == _HUMAN_APPROVAL_RELPATH


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
# 大文件/二进制处理（round3 P0-2：>2MB 整文件跳过 → 尾部藏钥可入库）：
#   - >2MB：不再整文件跳过——读前 _MAX_SCAN_BYTES 扫描，notes 注明
#     scanned_truncated（前 2MB 已扫，余 N MB 未扫）。藏尾部的密钥仍可能
#     逃过截断，这里选择诚实披露未扫字节范围而非假装全覆盖；staged 模式
#     在摘要行集中列出截断文件（⚠ 行），供人工复核；
#   - 前 8KB 含 NUL 字节：判定为二进制，跳过并注明 skipped_binary——
#     xlsx/pkl/mat/docx 等 zip/序列化格式不再整读入内存，防止 precommit
#     hook 的 60s 超时 → fail-open 放大面（二进制字节流 errors=ignore 解码
#     后也可能碰巧拼出疑似凭据形态，豁免同时收敛误报）。
_MAX_SCAN_BYTES = 2 * 1024 * 1024
_BINARY_SNIFF_BYTES = 8 * 1024


def _fmt_unscanned(nbytes: int) -> str:
    """未扫余量人性化（第四轮修复 LOW）：<0.1MB 时以字节显示。

    旧版恒用 MB 一位小数——35B/542B 级余量被格式化成"余 0.0MB"，掩盖
    "其实只差几百字节就全覆盖"的事实；<0.1MB 改显字节，≥0.1MB 仍显 MB。
    """
    if nbytes < 0.1 * 1048576:
        return f"{nbytes}B"
    return f"{nbytes / 1048576:.1f}MB"


def scan_files_for_secrets(
    files: list[str], notes: list[str] | None = None
) -> tuple[bool, list[str]]:
    """扫描硬编码密钥。

    大文件（>2MB）截断扫描：只读前 _MAX_SCAN_BYTES，notes 注明 scanned_truncated
    （前 2MB 已扫，余量按字节/MB 显示）；二进制（前 8KB 含 NUL）跳过并注明 skipped_binary。
    """
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
        truncated = size > _MAX_SCAN_BYTES
        try:
            with fpath.open("rb") as fh:
                head = fh.read(_BINARY_SNIFF_BYTES)
                if b"\x00" in head:
                    if notes is not None:
                        notes.append(f"skipped_binary: {fpath}（前 8KB 含 NUL 字节）")
                    continue
                # 小文件整读；大文件只读到 2MB 上限（截断扫描，round3 P0-2）
                if truncated:
                    body = head + fh.read(_MAX_SCAN_BYTES - len(head))
                else:
                    body = head + fh.read()
        except OSError:
            continue
        text = body.decode("utf-8", errors="ignore")
        if truncated and notes is not None:
            unscanned = max(0, size - len(body))
            # 第四轮修复 LOW：①补"窗口末端约 1KB 属模式匹配盲区"——截断边界处被
            # 切开的密钥两头都不完整，任何单侧模式都匹配不上（跨界漏报）；
            # ②余量 <0.1MB 时按字节显示（"余 0.0MB"会掩盖 35B/542B 级余量）
            notes.append(
                f"scanned_truncated: {fpath}（前 {len(body) / 1048576:.1f}MB 已扫，"
                f"余 {_fmt_unscanned(unscanned)} 未扫——窗口末端约 1KB 属模式匹配盲区"
                f"（跨界密钥可能漏报），藏尾部的密钥仍可能逃过，需人工复核）"
            )
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
    n_trunc = sum(1 for n in notes if n.startswith("scanned_truncated"))
    n_bin = sum(1 for n in notes if n.startswith("skipped_binary"))
    parts: list[str] = []
    if n_trunc:
        parts.append(f"{n_trunc} 个大文件仅截断扫描前 2MB（尾部未覆盖，名单见 ⚠ 行）")
    if n_bin:
        parts.append(f"跳过 {n_bin} 个二进制")
    suffix = ("，" + "，".join(parts)) if parts else ""
    print(f"  （暂存区 {len(names)} 个文件已扫描{suffix}）")
    # 截断文件集中醒目列出（round3 P0-2 审计可见性）：藏尾部的密钥仍可能逃过
    # 截断，至少让“哪些文件没扫全、各余多少”一眼可见，供人工复核。
    if n_trunc:
        print("    ⚠ 以下文件只扫了前 2MB，尾部未覆盖（密钥若藏尾部仍可能逃过）：")
        for n in notes:
            if n.startswith("scanned_truncated"):
                print(f"      ⚠ {n}")
    for n in notes:
        if not n.startswith("scanned_truncated"):
            print(f"    · {n}")
    return passed, issues


# ── 检查 5：Markdown 注入防护 ───────────────────────────────────
def _strip_teaching_mentions(text: str) -> str:
    """去掉反引号内的控制标记（教学性提及豁免，单行内配对）。

    反引号 span（`...`，不含换行）内含任一裸标记或绑定形态标记即整段移除，
    否则原样保留——与旧版逐标记 `` `...marker...` `` 移除语义等价，扩展到
    绑定形态（round3 P1-10）。
    """

    def _drop_if_marker(span: re.Match) -> str:
        s = span.group(0)
        for marker in _CONTROL_MARKERS:
            if marker in s:
                return ""
        for pat, _label in _CONTROL_BOUND_PATTERNS:
            if pat.search(s):
                return ""
        return s

    return re.sub(r"`[^`\n]*`", _drop_if_marker, text)


def check_markdown_injection(file: str) -> tuple[bool, list[str]]:
    """检测非审批文件中是否存在未配对的控制标记（半角/全角/绑定形态都抓）。

    pipeline_manager 行级消费 human_intervention.md 里的裸标记与绑定形态
    [APPROVED <stage>] / 【APPROVED <stage>】（_APPROVED_BOUND_RE 等）；同样
    的标记若出现在语料/论文/爬取数据等其它文件中，视为注入风险（伪造批准
    可能经拼接/引用流入状态链）。绑定形态此前“消费端认、扫描端不扫”
    （round3 P1-10），语料里伪造 [APPROVED S5] 对本扫描完全隐身。

    豁免（不视为注入，与消费端口径一致）：
      - paper_output/state/human_intervention.md（固定相对路径，round3 P0-3
        收窄：旧口径按文件名全局豁免，任意目录同名文件是注入盲区）；
      - 配对历史形式 [APPROVED — stage @ time]（全角括号同样豁免）；
      - 反引号内的标记（`[APPROVED]`、`[APPROVED S5]` 等为教学性提及；
        限定单行内配对，防跨行反引号把正文的真标记一并吞掉）。
    """
    fpath = Path(file)
    if not fpath.exists():
        return True, []
    if _is_human_approval_file(fpath):
        print(
            f"  （{fpath} 为人工审批文件（paper_output/state/ 固定路径），"
            "控制标记是用户合法输入，豁免注入扫描）"
        )
        return True, []
    text = fpath.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []
    # 去掉配对历史形式（半角 [] 与全角 【】 都认）
    legit = re.compile(r"[\[【](?:APPROVED|REWORK)\s+—\s+\S+\s+@\s+[^\]】]+[\]】]")
    remaining = legit.sub("", text)
    # 去掉反引号内的标记（教学性提及豁免；裸形态与绑定形态统一处理）
    remaining = _strip_teaching_mentions(remaining)
    for marker in _CONTROL_MARKERS:
        idx = remaining.find(marker)
        if idx >= 0:
            lineno = remaining[:idx].count("\n") + 1
            issues.append(f"{fpath}:{lineno}: 疑似伪造控制标记 {marker}（未配对）")
    for pat, _label in _CONTROL_BOUND_PATTERNS:
        for m in pat.finditer(remaining):
            lineno = remaining[: m.start()].count("\n") + 1
            issues.append(
                f"{fpath}:{lineno}: 疑似伪造控制标记 {m.group(0)}（绑定形态，未配对）"
            )
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

    pm = sub.add_parser(
        "markdown", help="Markdown 注入防护（仅 paper_output/state/human_intervention.md 豁免）"
    )
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