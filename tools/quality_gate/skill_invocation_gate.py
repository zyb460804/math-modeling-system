#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G5 Skill 调用强制门 — 检查必调 skill 是否真调过（v4.8）

背景：docs/agent_workflow_standard.md 要求 Agent 必须调 humanizer-zh-academic、
/review、/defense 等 skill，但原门禁只查数字/格式/图片，不查"调没调 skill"。
Agent 可凭直觉走捷径跳过 skill。本门禁通过检查 skill 产出文件，强制 Agent 必须调。

设计：
- 每个"必调 skill"对应一个产出文件（Agent 调 skill 后写到指定位置）
- 门禁检查文件存在性 + 基本质量（非空、有关键字段）
- 不通过 → FAIL + 给出"怎么调"的修复指引
- "建议调 skill" → WARN（不阻断提交，但提示覆盖率低）

用法：
    python skill_invocation_gate.py
    python skill_invocation_gate.py --paper-dir paper_output

退出码：0=PASS；1=FAIL（有必调 skill 未调）；2=WARN（建议 skill 未调）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ====== 必调 skill 清单（FAIL 级，未调则阻断提交）======
# 每个阶段至少 1 个门禁，确保"每个环节都调用了 skill 或知识库"
REQUIRED_SKILLS = [
    {
        "gate": "G5.1",
        "stage": "阶段0 任务启动",
        "skill": "knowledge_checkpoint（知识资产查阅）",
        "expected_file": "plan/knowledge_checkpoint.md",
        "check": "contains_all",
        "keywords": ["INDEX.md", "method_matching", "scoring_rubric", "phrase_bank", "section-architecture"],
        "how_to_fix": "读 outputs/INDEX.md + method_matching.md + scoring_rubric.md + phrase_bank.md + section-architecture.md，在 knowledge_checkpoint.md 声明已查阅并列关键收获",
    },
    {
        "gate": "G5.2",
        "stage": "阶段1 选模",
        "skill": "model-selector（选模对照）",
        "expected_file": "plan/model_selection_check.md",
        "check": "size",
        "min_size": 500,
        "how_to_fix": "查 outputs/method_matching.md + model-selection-matrix.md + HMML，写 model_selection_check.md 记录：①本题属于哪类 ②对照表推荐什么 ③最终选什么模型 ④为什么",
    },
    {
        "gate": "G5.3",
        "stage": "阶段2 代码复用",
        "skill": "resources/04_代码模板 + 10_算法cookbook",
        "expected_file": "plan/code_reuse_check.md",
        "check": "size",
        "min_size": 300,
        "how_to_fix": "查 resources/04_代码模板/ + resources/10_算法cookbook/，写 code_reuse_check.md 记录：①看了哪些模板 ②哪些可复用 ③哪些需自写 ④为什么",
    },
    {
        "gate": "G5.4",
        "stage": "阶段3 写作对照",
        "skill": "section-architecture + evidence-pyramid + scoring_rubric",
        "expected_file": "plan/writing_alignment_check.md",
        "check": "contains_all",
        "keywords": ["摘要", "六要素", "引言", "五要素", "证据"],
        "how_to_fix": "对照 section-architecture.md（摘要六要素 context/gap/approach/result/implication/boundary + 引言五要素）+ evidence-pyramid.md + scoring_rubric.md，写 writing_alignment_check.md 记录对齐情况",
    },
    {
        "gate": "G5.5",
        "stage": "阶段4 降AI味",
        "skill": "humanizer-zh-academic（降 AI 味）",
        "expected_file": "qa/humanizer_report.json",
        "check": "json_score",
        "json_path": ["score"],
        "min_value": 40,
        "max_value": 60,
        "how_to_fix": "调 humanizer-zh-academic skill（Skill 工具）对 final_paper_source.md 做 14 种 AI 模式扫描+60 分制评分，产出 humanizer_report.json（含 score 字段）",
    },
    {
        "gate": "G5.6",
        "stage": "阶段5 独立评审",
        "skill": "paper-reviewer agent（独立评审）",
        "expected_file": "qa/paper_reviewer_report.md",
        "check": "size",
        "min_size": 3000,
        "how_to_fix": "调 paper-reviewer agent（Task 工具，subagent_type=paper-reviewer）对论文做 9 维度评审，产出报告",
    },
    {
        "gate": "G5.7",
        "stage": "阶段5.5 AI失败检查",
        "skill": "ai-failure-checker（AI 失败模式检查）",
        "expected_file": "qa/ai_failure_check_report.json",
        "check": "json_count",
        "json_path": ["blocking"],
        "max_count": 0,
        "how_to_fix": "调 ai-failure-checker skill 做 7-mode blocking checklist（编造/幻觉/逻辑错误等），产出报告（blocking 数=0）",
    },
    {
        "gate": "G5.8",
        "stage": "阶段5.5 引用验证",
        "skill": "citation-tracer（引用验证）",
        "expected_file": "qa/citation_trace_report.md",
        "check": "size",
        "min_size": 200,
        "how_to_fix": "调 citation-tracer skill 验证论文引用的真实性",
    },
    {
        "gate": "G5.9",
        "stage": "阶段6 答辩",
        "skill": "defense（答辩材料）",
        "expected_file": "qa/defense_qa_bank.md",
        "check": "headings",
        "min_headings": 10,
        "how_to_fix": "调 /defense skill（Skill 工具）生成 ≥10 类问答+30 条追问链",
    },
]

# ====== 建议调 skill 清单（WARN 级，不阻断但提示覆盖率低）======
RECOMMENDED_SKILLS = [
    {"skill": "paper-polisher（12点检查）", "expected_file": "qa/paper_polisher_report.md"},
    {"skill": "style-calibration（风格校准）", "expected_file": "qa/style_calibration_report.md"},
    {"skill": "robustness-checker（稳健性）", "expected_file": "qa/robustness_check_report.md"},
    {"skill": "symbol-table-builder（符号表）", "expected_file": "plan/symbol_table_auto.md"},
    {"skill": "award-paper-rag mmqa retrieve（O奖检索）", "expected_file": "qa/award_paper_rag_results.md"},
    {"skill": "blind-panel（3座盲评，冲奖模式）", "expected_file": "qa/blind_panel_report.md"},
]


def check_one(item: dict, paper_dir: Path) -> tuple[str, str]:
    """返回 (status, detail)。status ∈ {'PASS','FAIL','WARN'}。"""
    fpath = paper_dir / item["expected_file"]
    if not fpath.exists():
        return "FAIL", f"产出文件不存在：{item['expected_file']}"

    check = item["check"]
    if check == "size":
        size = fpath.stat().st_size
        if size < item["min_size"]:
            return "FAIL", f"文件过小：{size} < {item['min_size']} 字节（疑似空壳/占位）"
        return "PASS", f"{size} 字节"
    if check == "json_score":
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            val = data
            for key in item["json_path"]:
                val = val[key]
            if val < item["min_value"]:
                return "FAIL", f"score={val} < {item['min_value']}（AI 味过重，需进一步降）"
            return "PASS", f"score={val}/{item['max_value']}"
        except Exception as e:
            return "FAIL", f"JSON 解析失败或缺少字段 {item['json_path']}：{e}"
    if check == "headings":
        text = fpath.read_text(encoding="utf-8")
        n = text.count("\n## ")
        if n < item["min_headings"]:
            return "FAIL", f"标题数 {n} < {item['min_headings']}（内容不完整）"
        return "PASS", f"{n} 个问答标题"
    if check == "json_count":
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            val = data
            for key in item["json_path"]:
                val = val[key]
            if isinstance(val, list) and len(val) > item["max_count"]:
                return "FAIL", f"blocking 数 {len(val)} > {item['max_count']}：{val[:3]}"
            return "PASS", f"blocking={len(val) if isinstance(val, list) else val}"
        except Exception as e:
            return "FAIL", f"JSON 解析失败：{e}"
    if check == "contains_all":
        text = fpath.read_text(encoding="utf-8")
        missing = [k for k in item["keywords"] if k not in text]
        if missing:
            return "FAIL", f"未声明查阅：{missing}"
        return "PASS", f"已声明查阅 {len(item['keywords'])} 项资产"
    return "FAIL", f"未知检查类型：{check}"


def main() -> int:
    ap = argparse.ArgumentParser(description="G5 Skill 调用强制门：检查必调 skill 是否真调过")
    ap.add_argument("--paper-dir", type=Path, default=Path("paper_output"))
    args = ap.parse_args()
    paper_dir = args.paper_dir.resolve()

    print("=" * 60)
    print("G5 Skill 调用强制门 — 检查必调 skill 产出文件")
    print("=" * 60)
    print(f"作品目录：{paper_dir}\n")

    n_pass = n_fail = 0
    results = []
    print("【必调 skill（FAIL 级）】")
    for item in REQUIRED_SKILLS:
        status, detail = check_one(item, paper_dir)
        mark = "✅" if status == "PASS" else "❌"
        print(f"  {mark} {item['gate']} {item['skill']}")
        print(f"      {detail}")
        if status == "FAIL":
            print(f"      修复：{item['how_to_fix']}")
            n_fail += 1
        else:
            n_pass += 1
        results.append({"gate": item["gate"], "skill": item["skill"], "status": status, "detail": detail})

    n_warn = 0
    print("\n【建议调 skill（WARN 级）】")
    for item in RECOMMENDED_SKILLS:
        fpath = paper_dir / item["expected_file"]
        if fpath.exists():
            print(f"  ✅ {item['skill']}")
            n_pass += 1
            results.append({"gate": "REC", "skill": item["skill"], "status": "PASS", "detail": str(fpath.stat().st_size)})
        else:
            print(f"  ⚠️  {item['skill']}（未调）→ {item['expected_file']}")
            n_warn += 1
            results.append({"gate": "REC", "skill": item["skill"], "status": "WARN", "detail": "未调"})

    total_required = len(REQUIRED_SKILLS)
    total_recommended = len(RECOMMENDED_SKILLS)
    coverage = (n_pass / (total_required + total_recommended)) * 100

    print("\n" + "=" * 60)
    print(f"必调：{n_pass}/{total_required + n_warn} PASS（其中必调 {total_required - n_fail}/{total_required}）")
    print(f"建议：{total_recommended - n_warn}/{total_recommended} 已调")
    print(f"总覆盖率：{coverage:.0f}%")
    if n_fail > 0:
        print(f"\n❌ FAIL — {n_fail} 个必调 skill 未调或产出不合格，不得提交")
        rc = 1
    elif n_warn > 0:
        print(f"\n⚠️  WARN — 必调全过，但 {n_warn} 个建议 skill 未调（覆盖率偏低）")
        rc = 2
    else:
        print(f"\n✅ PASS — 全部 skill 调用完备，覆盖率 100%")
        rc = 0
    print("=" * 60)

    report = {
        "gate": "G5_SKILL_INVOCATION",
        "status": "FAIL" if n_fail > 0 else ("WARN" if n_warn > 0 else "PASS"),
        "coverage_pct": round(coverage, 1),
        "n_required_pass": total_required - n_fail,
        "n_required_total": total_required,
        "n_recommended_pass": total_recommended - n_warn,
        "n_recommended_total": total_recommended,
        "details": results,
    }
    report_path = paper_dir / "qa" / "skill_invocation_gate_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"报告：{report_path}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
