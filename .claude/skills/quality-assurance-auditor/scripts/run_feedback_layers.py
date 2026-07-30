#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_feedback_layers.py — v4.1 四层反馈机制的机械预检查器（L1/L2）

设计：
- 脚本只做**机械检查**（结构/存在性/数字一致性/证据分位对比）。
- 5 维 rubric 评分与 diff 精修留给 agent-critic（读本脚本产出的 report 后评判）。
- 默认 advisory：永远写报告、永不抛异常、永不改调用方退出码（除非 --strict 见 blocker）。
- 接入点：code_factory.py（--stage code）/ run_and_verify.py（--stage result）/ 手动。

用法：
    python run_feedback_layers.py --stage code
    python run_feedback_layers.py --stage result
    python run_feedback_layers.py --stage all
    python run_feedback_layers.py --stage all --strict   # 出 blocker 返回 1
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    return Path.cwd().resolve()


def _load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _safe_call(func):
    """装饰器：任何子检查异常都不冒泡，记为 internal_error。"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            return {"check": func.__name__, "severity": "info",
                    "concern": f"internal_error: {type(e).__name__}: {e}"}
    wrapper.__name__ = func.__name__
    return wrapper


# ---------------- L1: 阶段级机械检查 ----------------

@_safe_call
def l1_code(root: Path) -> dict[str, Any]:
    """代码阶段：每个 q*_model.py 存在、可编译、有 main。"""
    code_dir = root / "paper_output" / "code" / "modeling"
    findings: list[dict] = []
    py_files = sorted(code_dir.glob("q*_model.py")) if code_dir.exists() else []
    if not py_files:
        findings.append({"severity": "medium", "where": "paper_output/code/modeling/",
                         "concern": "未找到 q*_model.py", "fix": "先运行 code_factory.py"})
    for py in py_files:
        try:
            import py_compile
            py_compile.compile(str(py), doraise=True)
        except Exception as e:  # noqa: BLE001
            findings.append({"severity": "high", "where": str(py.relative_to(root)),
                             "concern": f"语法错误: {e}", "fix": "修复语法后重跑"})
        src = py.read_text(encoding="utf-8", errors="ignore")
        if "def main" not in src:
            findings.append({"severity": "medium", "where": py.name,
                             "concern": "缺 main()，run_and_verify 可能无法调用", "fix": "补 def main()"})
    return {"stage": "L1-code", "checked": len(py_files), "findings": findings}


@_safe_call
def l1_result(root: Path) -> dict[str, Any]:
    """结果阶段：results/*.json 合法 + 证据指标（图/表/公式计数 vs empirical by_topic）。"""
    results_dir = root / "paper_output" / "results"
    findings: list[dict] = []
    evidence = {"figure_count": 0, "table_count": 0, "formula_count": 0}

    fig_dir = root / "paper_output" / "figures"
    if fig_dir.exists():
        evidence["figure_count"] = len(list(fig_dir.glob("*.png")) + list(fig_dir.glob("*.svg")))
    tbl_dir = root / "paper_output" / "tables"
    if tbl_dir.exists():
        evidence["table_count"] = len(list(tbl_dir.glob("*.csv")))
    src = root / "paper_output" / "final_paper_source.md"
    if src.exists():
        text = src.read_text(encoding="utf-8", errors="ignore")
        evidence["formula_count"] = len(re.findall(r"\$\$|\\\\begin\{equation\}", text))

    # empirical 分位对比（仅 CUMCM，异常提示）
    emp = _load_json(root / "outputs" / "empirical.json")
    pa = _load_json(root / "paper_output" / "step1" / "problem_analysis.json")
    topic = None
    if isinstance(pa, dict):
        topic = pa.get("topic") or (pa.get("questions", [{}])[0].get("id", "")[:1] or None)
    if isinstance(emp, dict) and topic and topic.upper() in emp.get("by_topic", {}):
        bt = emp["by_topic"][topic.upper()]
        fig_p25 = bt.get("figure_count", {}).get("p25")
        if fig_p25 is not None and evidence["figure_count"] < fig_p25:
            findings.append({
                "severity": "medium",
                "where": f"figures/ (题型 {topic})",
                "concern": f"图表 {evidence['figure_count']} < 该题型 p25={fig_p25}（empirical 异常提示，非硬阈值）",
                "fix": f"建议至少补到 {fig_p25} 张（p50={bt.get('figure_count', {}).get('p50')}）",
            })

    if results_dir.exists():
        for jf in results_dir.glob("*.json"):
            if _load_json(jf) is None:
                findings.append({"severity": "high", "where": str(jf.name),
                                 "concern": "JSON 解析失败", "fix": "重新生成结果文件"})

    return {"stage": "L1-result", "evidence_metrics": evidence, "findings": findings}


# ---------------- L2: 跨阶段一致性 ----------------

@_safe_call
def l2_backtrack(root: Path) -> dict[str, Any]:
    """跨阶段：task_type 一致性 + frozen_numbers 存在性 + 结果/路线对齐。"""
    findings: list[dict] = []
    pa = _load_json(root / "paper_output" / "step1" / "problem_analysis.json")
    mr = _load_json(root / "paper_output" / "results" / "model_route.json") \
        or _load_json(root / "paper_output" / "plan" / "model_route.json")

    pa_tt = _extract_task_type(pa)
    mr_tt = _extract_task_type(mr)
    if pa_tt and mr_tt and pa_tt != mr_tt:
        findings.append({"severity": "high", "from": "problem_analysis", "to": "model_route",
                         "concern": f"task_type 漂移: {pa_tt} → {mr_tt}",
                         "fix": "统一 task_type（影响 dim_weights 加权）"})

    frozen = root / "paper_output" / "qa" / "frozen_numbers.json"
    src = root / "paper_output" / "final_paper_source.md"
    if frozen.exists() and src.exists():
        fn = _load_json(frozen) or {}
        nums = {str(k): str(v) for k, v in fn.items() if not str(k).startswith("_")}
        text = src.read_text(encoding="utf-8", errors="ignore")
        for k, v in list(nums.items())[:20]:
            if v not in text:
                findings.append({"severity": "medium", "from": "frozen_numbers", "to": "paper",
                                 "concern": f"冻结值 {k}={v} 未在正文出现",
                                 "fix": "确认正文数字与 frozen_numbers 一致"})

    if isinstance(mr, dict) and isinstance(pa, dict):
        pa_q = {q.get("id") for q in pa.get("questions", []) if isinstance(q, dict)}
        mr_q = {q.get("id") for q in mr.get("questions", []) if isinstance(q, dict)}
        if pa_q and mr_q and pa_q != mr_q:
            missing = pa_q - mr_q
            if missing:
                findings.append({"severity": "high", "from": "problem_analysis", "to": "model_route",
                                 "concern": f"子问题覆盖缺失: {missing}",
                                 "fix": "model_route 须覆盖所有子问题"})

    return {"stage": "L2-backtrack", "findings": findings}


def _extract_task_type(doc: Any) -> str | None:
    if not isinstance(doc, dict):
        return None
    return doc.get("task_type") or doc.get("topic_type")


# ---------------- 编排 ----------------

def run(stage: str, root: Path) -> dict[str, Any]:
    stages = ["code", "result", "l2"] if stage == "all" else [stage]
    report: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(),
        "stage_requested": stage,
        "mode": "advisory",
        "layers": {},
    }
    if "code" in stages:
        report["layers"]["L1"] = l1_code(root)
    if "result" in stages:
        report["layers"]["L1_result"] = l1_result(root)
    if stage in ("l2", "all") or "result" in stages:
        report["layers"]["L2"] = l2_backtrack(root)

    blockers = sum(1 for layer in report["layers"].values()
                   if isinstance(layer, dict)
                   for f in layer.get("findings", [])
                   if isinstance(f, dict) and f.get("severity") == "high")
    report["blockers"] = blockers
    report["status"] = "FAIL" if blockers else "PASS"

    out = root / "paper_output" / "qa" / "feedback_layer_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="v4.1 feedback layer mechanical pre-checker")
    parser.add_argument("--stage", default="all",
                        choices=["code", "result", "l2", "all"])
    parser.add_argument("--strict", action="store_true",
                        help="出现 high-severity blocker 时返回 1（默认 advisory 返回 0）")
    args = parser.parse_args()

    root = get_project_root()
    report = run(args.stage, root)
    print(f"[feedback-layer] stage={args.stage} status={report['status']} "
          f"blockers={report['blockers']} → paper_output/qa/feedback_layer_report.json")
    if args.strict and report["blockers"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
