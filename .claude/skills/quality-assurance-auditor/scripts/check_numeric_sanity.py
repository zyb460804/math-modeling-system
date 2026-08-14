#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数值合理性扫描：inf/nan/量级检查（通用，非侵入式）。

融合自 AutoMCM-Pro 五层质量门控中的"数值合理性"层：
  自动检查决策变量范围、目标值量级、有无 inf/nan，任一异常回退。

与 check_result_reasonableness.py（硬编码 Q1-Q4 指标范围）互补：
  本脚本递归扫描 paper_output/results/**/*.json（含子目录）所有数值字段，做通用 sanity 检查。

额外规则（2026-08 修复 M-8）：
  - JSON 解析失败：记 WARNING 级 issue（不再静默跳过），全部损坏也必须看得见；
  - 字符串化的 inf/nan（如 "Infinity"、"-inf"、"nan"）：记 CRITICAL issue
    （数值溢出/计算失败被当文本写出的同义症状）。

用法：
  python check_numeric_sanity.py [--results-dir PATH]
退出码：0=无 CRITICAL（可有 WARNING）  1=发现 inf/nan/极端量级（含字符串化形态）
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

RESULTS_DIR = Path("paper_output/results")
QA_DIR = Path("paper_output/qa")
REPORT_FILE = QA_DIR / "numeric_sanity_report.json"

# 量级阈值：超出此区间视为可疑（物理量极少跨越 1e-6 ~ 1e10）
MAGNITUDE_LO = 1e-9
MAGNITUDE_HI = 1e10
# 绝对值大于此视为极端量级（可能是单位错误或溢出）
EXTREME_HI = 1e15

# 字符串化 inf/nan 识别表（整串精确匹配：strip+lower 后比对，避免误伤叙述文本）
_STRING_INF_TOKENS = {"inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}
_STRING_NAN_TOKENS = {"nan"}


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def scan_value(path: str, value: Any, issues: list[dict]) -> None:
    """递归扫描一个值，数值则检查。"""
    if _is_number(value):
        v = float(value)
        field = {"path": path, "value": v}
        if math.isnan(v):
            issues.append({**field, "type": "NAN", "severity": "CRITICAL",
                           "msg": "NaN（数值计算崩溃，如 0/0 或 log(负数)）"})
        elif math.isinf(v):
            issues.append({**field, "type": "INF", "severity": "CRITICAL",
                           "msg": "Inf（数值溢出或除零未捕获）"})
        elif abs(v) > EXTREME_HI:
            issues.append({**field, "type": "EXTREME_MAGNITUDE", "severity": "CRITICAL",
                           "msg": f"极端量级 |{v:.3g}| > {EXTREME_HI:.0g}（疑似单位错误/溢出）"})
        elif 0 < abs(v) < MAGNITUDE_LO:
            issues.append({**field, "type": "TINY_VALUE", "severity": "WARNING",
                           "msg": f"极小值 |{v:.3g}| < {MAGNITUDE_LO:.0g}（疑似归一化残留/下溢）"})
        elif abs(v) > MAGNITUDE_HI:
            issues.append({**field, "type": "LARGE_MAGNITUDE", "severity": "WARNING",
                           "msg": f"大量级 |{v:.3g}| > {MAGNITUDE_HI:.0g}（确认单位/量纲）"})
    elif isinstance(value, str):
        # M-8: 字符串化的数字也要扫（"Infinity"/"nan" 等，整串精确匹配避免误伤普通文本）
        token = value.strip().lower()
        if token in _STRING_INF_TOKENS:
            issues.append({"path": path, "value": value.strip(),
                           "type": "STRING_INF", "severity": "CRITICAL",
                           "msg": f"字符串化 Inf（{value.strip()!r}）：数值溢出被当文本写出"})
        elif token in _STRING_NAN_TOKENS:
            issues.append({"path": path, "value": value.strip(),
                           "type": "STRING_NAN", "severity": "CRITICAL",
                           "msg": f"字符串化 NaN（{value.strip()!r}）：计算失败被当文本写出"})
    elif isinstance(value, dict):
        for k, sub in value.items():
            scan_value(f"{path}.{k}" if path else k, sub, issues)
    elif isinstance(value, list):
        for i, sub in enumerate(value):
            scan_value(f"{path}[{i}]", sub, issues)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_numeric_sanity.py",
        description=(
            "数值合理性扫描：递归扫描结果目录下所有 JSON 的数值字段，"
            "检查 inf/nan/极端量级（通用、非侵入式）。"
        ),
        epilog=(
            "零参数运行保持原行为：递归扫描 paper_output/results/**/*.json（含子目录），"
            "报告写入 paper_output/qa/numeric_sanity_report.json。"
            "退出码：0=无 CRITICAL，1=发现 inf/nan/极端量级。"
        ),
    )
    parser.add_argument(
        "--results-dir",
        default=str(RESULTS_DIR),
        metavar="PATH",
        help="结果 JSON 所在目录（默认: paper_output/results）",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        print(f"[skip] 结果目录不存在: {results_dir}")
        return 0
    json_files = sorted(results_dir.rglob("*.json"))  # M-8: 真递归，子目录不再逃逸
    if not json_files:
        print("[skip] 无结果 JSON")
        return 0

    print(f"[numeric-sanity] 扫描 {len(json_files)} 个结果文件…\n")
    all_issues: list[dict] = []
    for jf in json_files:
        rel = jf.relative_to(results_dir).as_posix()  # 递归后用相对路径区分子目录
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            # M-8: 文件损坏不可静默——记 WARNING issue，至少要看得见
            msg = f"JSON 解析失败: {e}"
            print(f"  ⚠ {rel}: {msg}")
            all_issues.append({
                "path": "<unparseable>",
                "type": "UNPARSEABLE_JSON",
                "severity": "WARNING",
                "msg": msg,
                "file": rel,
            })
            continue
        file_issues: list[dict] = []
        scan_value("", data, file_issues)
        for it in file_issues:
            it["file"] = rel
        all_issues.extend(file_issues)
        if file_issues:
            n_crit = sum(1 for x in file_issues if x["severity"] == "CRITICAL")
            print(f"  ✗ {rel}: {len(file_issues)} 问题 ({n_crit} CRITICAL)")
        else:
            print(f"  ✓ {rel}: 干净")

    n_crit = sum(1 for x in all_issues if x["severity"] == "CRITICAL")
    n_warn = sum(1 for x in all_issues if x["severity"] == "WARNING")
    status = "FAIL" if n_crit else ("WARNING" if n_warn else "PASS")
    print(f"\n{'═' * 48}")
    print(f"  NUMERIC SANITY: {status}  ({n_crit} CRITICAL / {n_warn} WARNING)")
    print(f"{'═' * 48}")
    for it in all_issues:
        mark = "✗" if it["severity"] == "CRITICAL" else "⚠"
        val = it.get("value")
        if isinstance(val, (int, float)):
            val_str = f" = {val:.4g}"
        elif val is not None:
            val_str = f" = {val!r}"
        else:
            val_str = ""  # UNPARSEABLE_JSON 等无值 issue
        line = f"  {mark} {it['file']}:{it['path']}{val_str}  [{it['type']}]"
        if it.get("msg"):
            line += f"  {it['msg']}"
        print(line)

    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(
            {"status": status, "critical": n_crit, "warning": n_warn, "issues": all_issues},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n[numeric-sanity] 报告: {REPORT_FILE}")
    return 0 if n_crit == 0 else 1


if __name__ == "__main__":
    sys.exit(main())