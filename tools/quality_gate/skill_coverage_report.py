#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skill 适用覆盖率报告（v4.8）

读取 skill_applicability_matrix.json + problem_analysis.json，根据题型动态计算
"本题适用 skill 清单"，检查覆盖率。分母是"适用数"而非"总数 54"（v4.8 归档后），
真实反映浪费。

用法：
    python skill_coverage_report.py
    python skill_coverage_report.py --paper-dir paper_output --delivery word --mode standard

退出码：0（INFO 级，不阻断提交，仅报告覆盖率）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def detect_task_types(paper_dir: Path) -> list[str]:
    """从 problem_analysis.json 读取 task_type；若泛化则用关键词扫描题目文本补判。"""
    types = set()
    pa = paper_dir / "step1" / "problem_analysis.json"
    if pa.exists():
        try:
            data = json.loads(pa.read_text(encoding="utf-8"))
            for q in data.get("questions", []):
                tt = q.get("task_type", "")
                if tt and tt != "综合建模/统计分析":
                    # 从"综合建模/统计分析"等泛化值里提取信号
                    types.add(tt)
        except Exception:
            pass

    # 关键词扫描题目文本（从 problem_analysis.json 的 raw_text / problem_text_excerpt）
    scan_text = ""
    pa = paper_dir / "step1" / "problem_analysis.json"
    if pa.exists():
        try:
            data = json.loads(pa.read_text(encoding="utf-8"))
            scan_text += data.get("problem_text_excerpt", "")
            for q in data.get("questions", []):
                scan_text += q.get("raw_text", "") + q.get("summary", "")
        except Exception:
            pass
    # 也扫描 _pdf_text.txt（如果存在）
    pdf_text = paper_dir / "_pdf_text.txt"
    if pdf_text.exists():
        scan_text += pdf_text.read_text(encoding="utf-8", errors="replace")[:5000]

    if scan_text:
        signals_map = {
            "几何解析类": ["几何", "剖面", "坐标", "三角", "射线", "投影", "坡度", "角度", "夹角"],
            "优化类": ["最优", "最小", "最大", "调度", "配置", "路径", "规划", "最短", "设计一组"],
            "数据驱动类": ["附件", "数据集", "栅格", "表格数据", "测深数据", "单波束测量"],
            "评价类": ["排序", "打分", "优选", "多指标"],
            "预测类": ["预测", "趋势", "未来"],
            "图与网络类": ["最短路", "连通", "网络"],
            "机理分析类": ["微分方程", "传热", "扩散"],
        }
        for topic, keywords in signals_map.items():
            if sum(1 for k in keywords if k in scan_text) >= 2:
                types.add(topic)
    return sorted(types)


def compute_applicable(matrix: dict, task_types: list[str], delivery: str, mode: str) -> dict:
    """计算本题适用 skill 清单。返回 {applicable, excluded}。"""
    applicable = set(matrix["always_required"]["skills"])
    reason = {"always_required": "每题必用"}

    # by_topic
    for tt in task_types:
        # 模糊匹配（task_type 可能是"几何解析类"或"优化类+数据驱动类"）
        for key, val in matrix.get("by_topic", {}).items():
            if key.startswith("_"):
                continue
            if key in tt or any(k in tt for k in [key.replace("类", "")]):
                for s in val.get("skills", []):
                    applicable.add(s)
                    reason[s] = f"题型 {key} 适用"

    # by_delivery
    del_cfg = matrix.get("by_delivery", {}).get(delivery, {})
    for s in del_cfg.get("skills", []):
        applicable.add(s)
        reason[s] = f"交付方式 {delivery} 适用"

    # by_mode
    mode_cfg = matrix.get("by_mode", {}).get(mode, {})
    for s in mode_cfg.get("extra_skills", []):
        # 去掉括号说明
        s_clean = re.sub(r"[（(].*", "", s).strip()
        if s_clean:
            applicable.add(s_clean)
            reason[s_clean] = f"模式 {mode} 适用"

    # general_recommended（standard/championship 模式加）
    if mode in ("standard", "championship"):
        for s in matrix.get("general_recommended", {}).get("skills", []):
            s_clean = re.sub(r"[（(].*", "", s).strip()
            if s_clean:
                applicable.add(s_clean)
                reason[s_clean] = "通用建议"

    # 排除不适用（第四轮审查 F-5 修复）：矩阵 v4.8 改版后已无 not_applicable_domestic 键，
    # 旧排除逻辑读不到键恒返回空列表（死代码，排除静默失效）。现接现行 schema：
    #   rarely_applicable.skills = {name: reason}   特殊场景才用，不进覆盖率分母
    #   archived_skills.archived = {name: 去向}      v4.8 已归档，能力已抽到 references
    excluded = {}
    rare = matrix.get("rarely_applicable", {}).get("skills", {})
    if isinstance(rare, dict):
        for s in list(applicable):
            if s in rare:
                applicable.discard(s)
                excluded[s] = str(rare[s])
    archived = matrix.get("archived_skills", {}).get("archived", {})
    if isinstance(archived, dict):
        for s in list(applicable):
            if s in archived:
                applicable.discard(s)
                excluded[s] = f"v4.8 已归档：{archived[s]}"

    return {"applicable": sorted(applicable), "excluded": excluded, "reason": reason}


def check_skill_invoked(skill_name: str, paper_dir: Path) -> bool:
    """粗略判断 skill 是否被调用过——检查 qa/ 和 plan/ 下有无对应产出文件。"""
    qa = paper_dir / "qa"
    plan = paper_dir / "plan"
    candidates = []
    # 把 skill_name 转成可能的产出文件名片段
    short = skill_name.replace("-", "_").replace(" ", "_").lower()
    for d in [qa, plan]:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and short in f.name.lower():
                    return True
    # 特殊映射
    special = {
        "humanizer-zh-academic": ["humanizer_report.json"],
        "paper-reviewer": ["paper_reviewer_report.md"],
        "ai-failure-checker": ["ai_failure_check_report.json"],
        "citation-tracer": ["citation_trace_report.md"],
        "defense": ["defense_qa_bank.md"],
        "model-selector": ["model_selection_check.md", "model_route.json"],
        "robustness-checker": ["robustness_check_report.md"],
        "symbol-table-builder": ["symbol_table_auto.md", "symbol_table.md"],
        "award-paper-rag": ["award_paper_rag_results.md"],
        "paper-polisher": ["paper_polisher_report.md"],
        "style-calibration": ["style_calibration_report.md"],
        "blind-panel": ["blind_panel_report.md"],
        "math-figure": ["render_check_report.json", "figqa"],
    }
    for keyword in special.get(skill_name, []):
        for d in [qa, plan]:
            if d.exists():
                for f in d.rglob("*"):
                    if f.is_file() and keyword.lower() in str(f).lower():
                        return True
    return False


def check_knowledge_coverage(matrix: dict, paper_dir: Path) -> dict:
    """检查知识资产覆盖率。通过 knowledge_checkpoint.md 声明 + 对应产出文件判断。"""
    stages = matrix.get("knowledge_assets_by_stage", {})
    checkpoint = paper_dir / "plan" / "knowledge_checkpoint.md"
    checkpoint_text = checkpoint.read_text(encoding="utf-8", errors="replace") if checkpoint.exists() else ""

    # 也扫描 paper_output 下所有产出文件名，作为辅助判断
    produced_files = set()
    for d in [paper_dir / "plan", paper_dir / "qa"]:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file():
                    produced_files.add(f.name.lower())

    total = 0
    checked = 0
    details = {}
    for stage, assets in stages.items():
        if stage.startswith("_"):
            continue
        stage_checked = 0
        stage_total = 0
        for asset_path, desc in assets.items():
            stage_total += 1
            # 资产简称（用于在 checkpoint 里搜索）
            asset_short = asset_path.split("/")[-1].replace(".md", "").replace(".json", "").replace("/", "")
            # 判断是否查阅：① checkpoint 提及 ② 或有对应产出文件
            in_checkpoint = (
                asset_short.lower() in checkpoint_text.lower()
                or asset_path.lower() in checkpoint_text.lower()
            )
            # 检查对应的产出文件（粗映射）
            output_mapping = {
                "INDEX": ["knowledge_checkpoint.md"],
                "method_matching": ["model_selection_check.md"],
                "model-selection-matrix": ["model_selection_check.md"],
                "hmml": ["model_selection_check.md"],
                "04_代码模板": ["code_reuse_check.md"],
                "10_算法cookbook": ["code_reuse_check.md"],
                "writing_templates": ["writing_alignment_check.md"],
                "phrase_bank": ["writing_alignment_check.md"],
                "section-architecture": ["writing_alignment_check.md"],
                "evidence-pyramid": ["writing_alignment_check.md"],
                "scoring_rubric": ["paper_reviewer_report.md"],
                "anti-ai-detection-guide": ["humanizer_report.json"],
                "four-round-self-review": ["humanizer_report.json"],
            }
            has_output = False
            for key, files in output_mapping.items():
                if key.lower() in asset_path.lower():
                    if any(f in produced_files for f in files):
                        has_output = True
                        break

            if in_checkpoint or has_output:
                stage_checked += 1
                checked += 1
            stage_total_str = f"{stage_checked}/{stage_total}"
            details[stage] = {"checked": stage_checked, "total": stage_total}
        total += stage_total
    return {"checked": checked, "total": total, "by_stage": details}


def main() -> int:
    ap = argparse.ArgumentParser(description="Skill 适用覆盖率报告")
    ap.add_argument("--paper-dir", type=Path, default=Path("paper_output"))
    ap.add_argument("--delivery", default="word", choices=["word", "latex", "typst", "english_academic"])
    ap.add_argument("--mode", default="standard", choices=["fast", "standard", "championship"])
    args = ap.parse_args()
    paper_dir = args.paper_dir.resolve()
    here = Path(__file__).resolve().parent

    matrix_path = here / "skill_applicability_matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))

    task_types = detect_task_types(paper_dir)
    result = compute_applicable(matrix, task_types, args.delivery, args.mode)
    applicable = result["applicable"]
    excluded = result["excluded"]

    print("=" * 60)
    print("Skill 适用覆盖率报告")
    print("=" * 60)
    print(f"作品目录：{paper_dir}")
    print(f"题型判断：{task_types or '（未识别，按通用建议）'}")
    print(f"交付方式：{args.delivery}")
    print(f"运行模式：{args.mode}")
    print(f"\n本题适用 skill 清单（{len(applicable)} 个，已排除不适用的 {len(excluded)} 个）：")

    invoked = []
    not_invoked = []
    for s in applicable:
        ok = check_skill_invoked(s, paper_dir)
        mark = "✅" if ok else "❌"
        reason = result["reason"].get(s, "")
        print(f"  {mark} {s}  ({reason})")
        if ok:
            invoked.append(s)
        else:
            not_invoked.append(s)

    if excluded:
        print(f"\n不适用（不计入分母，非浪费）：")
        for s, why in excluded.items():
            print(f"  ⏭️  {s}  ({why})")

    coverage = len(invoked) / len(applicable) * 100 if applicable else 0
    print(f"\n{'=' * 60}")
    print(f"覆盖率：{len(invoked)}/{len(applicable)} = {coverage:.0f}%")
    print(f"  已调：{len(invoked)}")
    print(f"  适用但未调：{len(not_invoked)}")
    print(f"  不适用（排除）：{len(excluded)}")
    if coverage >= 80:
        print(f"  ✅ 覆盖率达标（≥80%），资产利用率良好")
    elif coverage >= 50:
        print(f"  ⚠️  覆盖率中等（50-80%），有 {len(not_invoked)} 个适用 skill 未调")
    else:
        print(f"  ❌ 覆盖率偏低（<50%），{len(not_invoked)} 个适用 skill 未调——资产浪费")
    print(f"{'=' * 60}")

    report = {
        "gate": "SKILL_COVERAGE_REPORT",
        "task_types": task_types,
        "delivery": args.delivery,
        "mode": args.mode,
        "applicable_count": len(applicable),
        "invoked_count": len(invoked),
        "not_invoked": not_invoked,
        "excluded": excluded,
        "coverage_pct": round(coverage, 1),
    }

    # ====== 知识资产覆盖率 ======
    print(f"\n{'=' * 60}")
    print("知识资产覆盖率（outputs/ + resources/ + references/）")
    print(f"{'=' * 60}")
    knowledge = check_knowledge_coverage(matrix, paper_dir)
    k_cov = knowledge["checked"] / knowledge["total"] * 100 if knowledge["total"] else 0
    print(f"\n按阶段：")
    for stage, info in knowledge["by_stage"].items():
        mark = "✅" if info["checked"] == info["total"] else ("⚠️" if info["checked"] > 0 else "❌")
        print(f"  {mark} {stage}: {info['checked']}/{info['total']}")
    print(f"\n知识资产覆盖率：{knowledge['checked']}/{knowledge['total']} = {k_cov:.0f}%")
    if k_cov >= 80:
        print(f"  ✅ 知识资产利用良好")
    elif k_cov >= 50:
        print(f"  ⚠️  知识资产利用中等，部分沉淀未被查阅")
    else:
        print(f"  ❌ 知识资产浪费严重——这些是项目核心价值，不查等于白搭")

    # 综合利用率
    overall = (coverage + k_cov) / 2
    print(f"\n{'=' * 60}")
    print(f"综合利用率（skill 覆盖率 {coverage:.0f}% + 知识资产覆盖率 {k_cov:.0f}%）= {overall:.0f}%")
    print(f"{'=' * 60}")

    report["knowledge_coverage"] = {
        "checked": knowledge["checked"],
        "total": knowledge["total"],
        "coverage_pct": round(k_cov, 1),
        "by_stage": knowledge["by_stage"],
    }
    report["overall_utilization_pct"] = round(overall, 1)
    report_path = paper_dir / "qa" / "skill_coverage_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"报告：{report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
