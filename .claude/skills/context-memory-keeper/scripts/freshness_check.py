#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SHA-256 新鲜度校验：防止输入/代码/结果变化后继续使用旧报告。

融合自 yushui2022/MathModel-Skill（217★）的"防漂移"机制：
  用 SHA-256 防止输入、代码或结果变化后继续使用旧报告。
  报告（qa/*.json）必须记录其生成时所依据的源文件哈希；
  若源文件后续变化，该报告被标记为 STALE，必须重新生成。

工作流：
  record <report>   — 为报告计算并写入 source_hash 字段
  check             — 比对所有带 source_hash 的报告，输出 STALE 列表
  check <report>    — 检查单个报告

用法：
  python freshness_check.py record paper_output/qa/evidence_gate_report.json
  python freshness_check.py record paper_output/qa/verify_gate_report.json \
      --sources paper_output/code/verifications paper_output/code/modeling
  python freshness_check.py check

--sources（record 可选）：显式指定该报告依赖的源文件/目录（各门禁只绑定自己的
核心依赖，而非全量 SOURCE_GLOBS）。record 会把源清单写进报告的
source_hash_sources 字段，check 据此按报告各自重算——不带该字段的旧报告
仍按默认 SOURCE_GLOBS 比对（向后兼容）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

BASE = Path("paper_output")
QA_DIR = BASE / "qa"
CODE_DIR = BASE / "code"
PROBLEM_DIR = Path("problem_files")

# 哈希源：所有影响报告结论的输入
SOURCE_GLOBS = [
    PROBLEM_DIR,                          # 赛题与附件（只读）
    CODE_DIR / "data_processing",
    CODE_DIR / "modeling",
    CODE_DIR / "visualization",
]


def _hash_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _hash_dir(d: Path) -> str:
    """聚合一个目录下所有文件的 SHA-256（排序后拼接哈希）。

    排除 __pycache__ 与 .pyc/.pyc.py3k/.pyo：字节码随解释器/环境波动，
    与"源是否变化"无关，混入会造成假 STALE。
    """
    if not d.exists():
        return ""
    files = sorted([
        f for f in d.rglob("*")
        if f.is_file()
        and "__pycache__" not in f.parts
        and f.suffix not in (".pyc", ".pyo")
    ])
    h = hashlib.sha256()
    for f in files:
        rel = str(f.relative_to(d)).replace("\\", "/")
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(_hash_file(f).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def compute_source_hash(sources: list[Path] | None = None) -> dict:
    """计算源哈希指纹。sources 为空 → 默认 SOURCE_GLOBS（全量源，键=目录/文件名）；
    显式传入 → 只哈希指定路径（键=posix 路径串，record/check 两端同源派生，可比）。
    不存在的源跳过：record 后新增文件 / 删除文件都会改变 parts → 触发 STALE，
    这正是"依赖集变化=报告过期"的预期语义。
    """
    targets = [Path(s) for s in sources] if sources else list(SOURCE_GLOBS)
    parts: dict[str, str] = {}
    for src in targets:
        if src.is_dir():
            key = src.as_posix()
            parts[key] = _hash_dir(src)
        elif src.is_file():
            key = src.as_posix()
            parts[key] = _hash_file(src)
    merged = hashlib.sha256(
        "|".join(f"{k}={v}" for k, v in sorted(parts.items())).encode("utf-8")
    ).hexdigest()
    return {"source_hash": merged, "parts": parts, "computed_at": datetime.now().isoformat(timespec="seconds")}


def cmd_record(args: argparse.Namespace) -> int:
    report = Path(args.report)
    if not report.exists():
        print(f"[fresh] 报告不存在: {report}")
        return 1
    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[fresh] 报告解析失败: {e}")
        return 1
    if not isinstance(data, dict):
        data = {"payload": data}
    sources = [Path(s) for s in args.sources] if args.sources else None
    snap = compute_source_hash(sources)
    data["source_hash"] = snap["source_hash"]
    data["source_hash_parts"] = snap["parts"]
    data["source_hash_at"] = snap["computed_at"]
    if sources is not None:
        # check 端按报告各自的源清单重算，而非全量 SOURCE_GLOBS
        data["source_hash_sources"] = [s.as_posix() for s in sources]
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    scope = f"（自定义源 {len(snap['parts'])} 项）" if sources is not None else "（默认全量源）"
    print(f"[fresh] 已为 {report.name} 记录 source_hash = {snap['source_hash'][:12]}… {scope}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    default_snap: dict | None = None  # 惰性缓存：无自定义源的报告共用默认全量指纹

    def _default() -> dict:
        nonlocal default_snap
        if default_snap is None:
            default_snap = compute_source_hash()
        return default_snap

    print(f"[fresh] 默认源指纹: {_default()['source_hash'][:12]}…\n")

    reports = [Path(args.report)] if args.report else sorted(QA_DIR.glob("*.json")) if QA_DIR.exists() else []
    if not reports:
        print("[fresh] 无报告可比对")
        return 0

    stale: list[str] = []
    fresh: list[str] = []
    no_hash: list[str] = []
    unreadable: list[str] = []
    for r in reports:
        try:
            data = json.loads(r.read_text(encoding="utf-8"))
        except Exception as e:
            # fail-closed（显式指定报告时）：读不到 = 无法证明其新鲜，
            # 记入 stale 触发 rc=1——旧版静默 continue，"check <不存在的报告>"
            # 会以 FRESH=0 STALE=0 rc=0 假绿收场。全量扫描模式仅可见列出，不改变判定。
            if args.report:
                print(f"  ✗ UNREADABLE {r}  （无法读取/解析: {e}）")
                stale.append(r.name)
            else:
                unreadable.append(r.name)
            continue
        if not isinstance(data, dict) or "source_hash" not in data:
            no_hash.append(r.name)
            continue
        recorded_sources = data.get("source_hash_sources")
        if isinstance(recorded_sources, list) and recorded_sources:
            # record --sources 记录的报告：按它自己的源清单重算（门禁报告只绑定各自依赖）
            current = compute_source_hash([Path(s) for s in recorded_sources])
        else:
            current = _default()
        if data["source_hash"] != current["source_hash"]:
            stale.append(r.name)
        else:
            fresh.append(r.name)

    for n in fresh:
        print(f"  ✓ FRESH    {n}")
    for n in stale:
        print(f"  ✗ STALE    {n}  （源已变化，报告需重新生成）")
    for n in no_hash:
        print(f"  · NO_HASH  {n}  （无 source_hash 字段，用 record 命令补充）")
    for n in unreadable:
        print(f"  · UNREADABLE  {n}  （无法读取/解析，未能校验新鲜度）")

    print(f"\n[fresh] FRESH={len(fresh)} STALE={len(stale)} NO_HASH={len(no_hash)} UNREADABLE={len(unreadable)}")
    return 0 if not stale else 1


def main() -> int:
    p = argparse.ArgumentParser(description="SHA-256 新鲜度校验")
    sub = p.add_subparsers(dest="cmd")
    pr = sub.add_parser("record", help="为报告写入 source_hash")
    pr.add_argument("report")
    pr.add_argument("--sources", nargs="+", default=None, metavar="PATH",
                    help="该报告依赖的源文件/目录（默认全量 SOURCE_GLOBS）；写入 source_hash_sources 供 check 按报告重算")
    pc = sub.add_parser("check", help="比对报告新鲜度")
    pc.add_argument("report", nargs="?", default=None)
    args = p.parse_args()
    if args.cmd == "record":
        return cmd_record(args)
    if args.cmd == "check":
        return cmd_check(args)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())