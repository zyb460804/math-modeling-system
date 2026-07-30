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
  python freshness_check.py check
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
    """聚合一个目录下所有文件的 SHA-256（排序后拼接哈希）。"""
    if not d.exists():
        return ""
    files = sorted([f for f in d.rglob("*") if f.is_file()])
    h = hashlib.sha256()
    for f in files:
        rel = str(f.relative_to(d)).replace("\\", "/")
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(_hash_file(f).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def compute_source_hash() -> dict:
    """计算所有源的哈希指纹。"""
    parts: dict[str, str] = {}
    for src in SOURCE_GLOBS:
        if src.exists() and src.is_dir():
            parts[src.name] = _hash_dir(src)
        elif src.exists() and src.is_file():
            parts[src.name] = _hash_file(src)
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
    snap = compute_source_hash()
    data["source_hash"] = snap["source_hash"]
    data["source_hash_parts"] = snap["parts"]
    data["source_hash_at"] = snap["computed_at"]
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[fresh] 已为 {report.name} 记录 source_hash = {snap['source_hash'][:12]}…")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    current = compute_source_hash()
    print(f"[fresh] 当前源指纹: {current['source_hash'][:12]}…\n")

    reports = [Path(args.report)] if args.report else sorted(QA_DIR.glob("*.json")) if QA_DIR.exists() else []
    if not reports:
        print("[fresh] 无报告可比对")
        return 0

    stale: list[str] = []
    fresh: list[str] = []
    no_hash: list[str] = []
    for r in reports:
        try:
            data = json.loads(r.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict) or "source_hash" not in data:
            no_hash.append(r.name)
            continue
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

    print(f"\n[fresh] FRESH={len(fresh)} STALE={len(stale)} NO_HASH={len(no_hash)}")
    return 0 if not stale else 1


def main() -> int:
    p = argparse.ArgumentParser(description="SHA-256 新鲜度校验")
    sub = p.add_subparsers(dest="cmd")
    pr = sub.add_parser("record", help="为报告写入 source_hash")
    pr.add_argument("report")
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