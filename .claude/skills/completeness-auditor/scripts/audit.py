#!/usr/bin/env python3
"""
完整性审计脚本

检查所有审查文件、审计报告、代码审查是否存在且质量达标。

用法：
    python audit.py [--question QUESTION] [--verbose]

输出：
    - 控制台报告
    - paper_output/qa/completeness_audit_report.json
    - paper_output/qa/completeness_audit_report.md
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 配置 UTF-8 输出
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 路径配置
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
REPORT_JSON = QA_DIR / "completeness_audit_report.json"
REPORT_MD = QA_DIR / "completeness_audit_report.md"

# 必须存在的文件清单
CRITICAL_ARTIFACTS = [
    # 计划产物
    ("step1/problem_analysis.json", "CRITICAL", "题意分析"),
    ("plan/model_route.json", "CRITICAL", "模型路线"),

    # 论文产物
    ("final_paper_source.md", "CRITICAL", "论文源稿"),
    ("final_paper.docx", "CRITICAL", "Word文档"),

    # QA产物
    ("qa/evidence_gate_report.json", "CRITICAL", "证据门禁报告"),
]

HIGH_ARTIFACTS = [
    # 计划产物
    ("plan/rubric_alignment.json", "HIGH", "评分对齐"),
    ("plan/data_plan.json", "HIGH", "数据计划"),
    ("plan/visualization_plan.json", "HIGH", "图表计划"),
    ("plan/symbol_table.md", "HIGH", "符号表"),
    ("plan/paper_outline.json", "HIGH", "论文大纲"),

    # 索引文件
    ("figure_index.json", "HIGH", "图表索引"),
    ("tables/table_index.json", "HIGH", "表格索引"),

    # QA产物
    ("qa/consistency_audit_report.json", "HIGH", "一致性审计报告"),
    ("qa/format_check_report.json", "HIGH", "格式检查报告"),
]

# 每个子问题必须存在的产物
PER_QUESTION_CRITICAL = [
    ("methods/{q}/{q_lower}_final_method_explanation.md", "CRITICAL", "最终方法解释"),
    ("results/{q}/reports/{q_lower}_final_result_analysis.md", "CRITICAL", "最终结果分析"),
    ("results/{q}/reports/frozen_numbers.json", "CRITICAL", "冻结数字"),
]

PER_QUESTION_HIGH = [
    ("robustness/{q}/{q_lower}_robustness_report.md", "HIGH", "鲁棒性报告"),
    ("results/{q}/reports/{q_lower}_solution_package_for_writer.md", "HIGH", "解决方案包"),
]

# 代码审查文件
CODE_REVIEW_PATTERNS = [
    ("code/{q}/reviews/{q_lower}_python_review.md", "CRITICAL", "Python代码审查"),
    ("code/matlab/{q}/reviews/{q_lower}_matlab_review.md", "CRITICAL", "Matlab代码审查"),
]

# 同一产物的候选路径（旧布局/新布局兼容）：命中任一即算存在
# table_index.json 历史上登记为根路径，实际产物在 tables/ 下 → 路径错位误报（B-①）
ARTIFACT_FALLBACKS = {
    "tables/table_index.json": ["table_index.json"],
    "table_index.json": ["tables/table_index.json"],
    "figure_index.json": ["figures/figure_index.json"],
    "figures/figure_index.json": ["figure_index.json"],
}


def resolve_artifact(rel_path: str) -> Path:
    """按主路径+候选路径解析产物，任一存在即返回该路径；全缺失时返回主路径（用于报告）"""
    for cand in [rel_path] + ARTIFACT_FALLBACKS.get(rel_path, []):
        p = OUTPUT_DIR / cand
        if p.exists():
            return p
    return OUTPUT_DIR / rel_path


def load_json(path: Path) -> Any:
    """加载 JSON 文件"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}


def get_question_dirs() -> list[str]:
    """获取所有子问题目录"""
    questions = []
    results_dir = OUTPUT_DIR / "results"
    if results_dir.exists():
        for item in results_dir.iterdir():
            if item.is_dir() and item.name.startswith("Q"):
                questions.append(item.name)
    return sorted(questions)


def check_file_exists(path: Path) -> dict:
    """检查文件是否存在并获取元信息"""
    if not path.exists():
        return {"exists": False}

    stat = path.stat()
    return {
        "exists": True,
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_empty": stat.st_size == 0
    }


def check_code_review_quality(review_path: Path) -> dict:
    """检查代码审查文件质量"""
    if not review_path.exists():
        return {"exists": False, "quality": "N/A"}

    content = review_path.read_text(encoding="utf-8")

    # 统计检查项数量
    # 假设每个检查项以数字开头或以"检查"开头
    check_patterns = [
        r'^\d+[\.\)]\s*',  # 1. 或 1)
        r'^[-*]\s+',  # - 或 *
        r'检查\d+[：:]',  # 检查1：
        r'##\s+检查',  # ## 检查
    ]

    check_count = 0
    for pattern in check_patterns:
        import re
        matches = re.findall(pattern, content, re.MULTILINE)
        check_count += len(matches)

    # 检查是否有file:line引用
    has_file_ref = bool(re.search(r'\w+\.\w+:\d+', content))

    # 检查是否有结论
    has_conclusion = "结论" in content or "总结" in content or "PASS" in content or "FAIL" in content

    return {
        "exists": True,
        "check_items": check_count,
        "has_file_line_refs": has_file_ref,
        "has_conclusion": has_conclusion,
        "quality": "PASS" if check_count >= 5 and has_file_ref else "WARN" if check_count >= 3 else "FAIL"
    }


def check_audit_report_status(report_path: Path) -> dict:
    """检查审计报告状态"""
    if not report_path.exists():
        return {"exists": False, "status": "MISSING"}

    data = load_json(report_path)
    if not data or "__error__" in data:
        return {"exists": True, "status": "ERROR", "error": data.get("__error__", "Unknown")}

    return {
        "exists": True,
        "status": data.get("status", "UNKNOWN"),
        "score": data.get("score", 0)
    }


def check_frozen_numbers_freshness(q: str) -> dict:
    """检查frozen_numbers.json的时效性"""
    frozen_path = OUTPUT_DIR / "results" / q / "reports" / "frozen_numbers.json"
    if not frozen_path.exists():
        return {"exists": False, "is_fresh": False}

    data = load_json(frozen_path)
    if not data or "__error__" in data:
        return {"exists": True, "is_fresh": False, "error": data.get("__error__")}

    frozen_at = data.get("frozen_at")
    if not frozen_at:
        return {"exists": True, "is_fresh": False, "reason": "No frozen_at timestamp"}

    # 检查源文件是否比frozen更新
    code_source_files = data.get("code_source_files", [])
    frozen_time = datetime.fromisoformat(frozen_at.replace("Z", "+00:00"))

    for source in code_source_files:
        source_path = Path(source.get("path", ""))
        if source_path.exists():
            # aware/naive 统一（第一轮 M-9）：frozen_at 带 tz（如 Z 结尾）而 mtime 为
            # naive 本地时间时直接比较会 TypeError——按 frozen 的 tz 感知化 mtime
            if frozen_time.tzinfo is not None:
                source_mtime = datetime.fromtimestamp(source_path.stat().st_mtime, tz=frozen_time.tzinfo)
            else:
                source_mtime = datetime.fromtimestamp(source_path.stat().st_mtime)
            if source_mtime > frozen_time:
                return {
                    "exists": True,
                    "is_fresh": False,
                    "reason": f"Source file {source_path} modified after freeze"
                }

    return {"exists": True, "is_fresh": True}


def run_audit(questions: list[str], verbose: bool = False) -> dict:
    """执行完整性审计"""
    result = {
        "audit_type": "completeness",
        "audit_time": datetime.now().isoformat(),
        "status": "PASS",
        "score": 100,
        "checks": {
            "global_artifacts": {"status": "PASS", "details": []},
            "code_reviews": {"status": "PASS", "details": []},
            "audit_reports": {"status": "PASS", "details": []},
            "per_question": {"status": "PASS", "details": {}}
        },
        "failures": [],
        "warnings": []
    }

    total_expected = 0
    total_found = 0

    # 1. 检查全局产物
    print("\n[1/5] 检查全局产物...")
    for artifact, severity, description in CRITICAL_ARTIFACTS + HIGH_ARTIFACTS:
        total_expected += 1
        artifact_path = resolve_artifact(artifact)
        info = check_file_exists(artifact_path)

        if info["exists"] and not info.get("is_empty"):
            total_found += 1
            result["checks"]["global_artifacts"]["details"].append({
                "path": artifact,
                "resolved": str(artifact_path.relative_to(OUTPUT_DIR)) if str(artifact_path).startswith(str(OUTPUT_DIR)) else artifact,
                "status": "OK",
                "severity": severity,
                "description": description
            })
        else:
            # 0 字节产物与缺失同罪（B-②：is_empty 旧来只算不用，空壳文件被当 OK）
            if info["exists"]:
                issue_type = "empty_artifact"
                status_label = "EMPTY"
            else:
                issue_type = "missing_critical" if severity == "CRITICAL" else "missing_high"
                status_label = "MISSING"

            if severity == "CRITICAL":
                result["status"] = "FAIL"
                result["failures"].append({
                    "type": issue_type,
                    "severity": severity,
                    "artifact": artifact,
                    "description": description + ("（文件存在但为 0 字节空壳）" if info["exists"] else "")
                })
            else:
                result["warnings"].append({
                    "type": issue_type,
                    "severity": severity,
                    "artifact": artifact,
                    "description": description + ("（文件存在但为 0 字节空壳）" if info["exists"] else "")
                })

            result["checks"]["global_artifacts"]["details"].append({
                "path": artifact,
                "status": status_label,
                "severity": severity,
                "description": description
            })

    if verbose:
        print(f"  全局产物: {total_found}/{total_expected}")

    # 2. 检查审计报告
    print("\n[2/5] 检查审计报告...")
    audit_reports = [
        ("qa/consistency_audit_report.json", "一致性审计"),
        ("qa/evidence_gate_report.json", "证据门禁"),
        ("qa/format_check_report.json", "格式检查")
    ]

    for report_path, description in audit_reports:
        full_path = OUTPUT_DIR / report_path
        status = check_audit_report_status(full_path)

        result["checks"]["audit_reports"]["details"].append({
            "path": report_path,
            "description": description,
            **status
        })

        if not status["exists"]:
            result["warnings"].append({
                "type": "missing_audit_report",
                "severity": "HIGH",
                "artifact": report_path,
                "description": description
            })
        elif status.get("status") not in ["PASS", "WARN"]:
            result["warnings"].append({
                "type": "audit_not_passed",
                "severity": "HIGH",
                "artifact": report_path,
                "status": status.get("status"),
                "description": description
            })

    # 3. 检查代码审查
    print("\n[3/5] 检查代码审查...")
    for q in questions:
        q_lower = q.lower()
        q_details = []

        for pattern, severity, description in CODE_REVIEW_PATTERNS:
            review_path = OUTPUT_DIR / pattern.format(q=q, q_lower=q_lower)
            quality = check_code_review_quality(review_path)

            q_details.append({
                "path": str(review_path.relative_to(OUTPUT_DIR)),
                "description": description,
                **quality
            })

            if quality["exists"]:
                if quality["quality"] == "FAIL":
                    result["warnings"].append({
                        "type": "review_quality_low",
                        "severity": "HIGH",
                        "artifact": str(review_path.relative_to(OUTPUT_DIR)),
                        "check_items": quality.get("check_items", 0),
                        "suggestion": "代码审查需要≥5项具体检查，并引用file:line"
                    })
            # 不强制要求Matlab审查存在，除非目录存在

        result["checks"]["code_reviews"]["details"].extend(q_details)

    # 4. 检查每个子问题的产物
    print("\n[4/5] 检查子问题产物...")
    if not questions:
        # 扁平布局（results/ 无 Q* 子目录）：per-question 产物检查整体未执行。
        # 旧实现静默跳过 → 空壳 per-question 也显示 PASS；至少 WARN 让空档可见（B-④）。
        result["warnings"].append({
            "type": "per_question_skipped",
            "severity": "HIGH",
            "artifact": "results/Q*/",
            "description": "results/ 下无 Q* 子目录（扁平布局），per-question 产物检查未执行；"
                           "如需逐问核验请建立 results/Q1..Qn/ 结构，或用 --question 逐个指定"
        })
        result["checks"]["per_question"]["status"] = "WARN"
    for q in questions:
        q_lower = q.lower()
        q_result = {
            "critical": {"expected": 0, "found": 0, "missing": []},
            "high": {"expected": 0, "found": 0, "missing": []}
        }

        # 检查关键产物
        for pattern, severity, description in PER_QUESTION_CRITICAL:
            total_expected += 1
            q_result["critical"]["expected"] += 1

            artifact_path = OUTPUT_DIR / pattern.format(q=q, q_lower=q_lower)
            info = check_file_exists(artifact_path)

            if info["exists"] and not info.get("is_empty"):
                total_found += 1
                q_result["critical"]["found"] += 1
            else:
                empty_note = "（0 字节空壳）" if info["exists"] else ""
                q_result["critical"]["missing"].append({
                    "path": pattern.format(q=q, q_lower=q_lower),
                    "description": description + empty_note
                })
                result["failures"].append({
                    "type": "empty_artifact" if info["exists"] else "missing_critical",
                    "severity": severity,
                    "artifact": pattern.format(q=q, q_lower=q_lower),
                    "description": f"{q}: {description}{empty_note}"
                })

        # 检查高优先级产物
        for pattern, severity, description in PER_QUESTION_HIGH:
            total_expected += 1
            q_result["high"]["expected"] += 1

            artifact_path = OUTPUT_DIR / pattern.format(q=q, q_lower=q_lower)
            info = check_file_exists(artifact_path)

            if info["exists"] and not info.get("is_empty"):
                total_found += 1
                q_result["high"]["found"] += 1
            else:
                empty_note = "（0 字节空壳）" if info["exists"] else ""
                q_result["high"]["missing"].append({
                    "path": pattern.format(q=q, q_lower=q_lower),
                    "description": description + empty_note
                })
                result["warnings"].append({
                    "type": "empty_artifact" if info["exists"] else "missing_high",
                    "severity": severity,
                    "artifact": pattern.format(q=q, q_lower=q_lower),
                    "description": f"{q}: {description}{empty_note}"
                })

        # 检查frozen_numbers时效性
        frozen_status = check_frozen_numbers_freshness(q)
        q_result["frozen_numbers"] = frozen_status

        if frozen_status["exists"] and not frozen_status["is_fresh"]:
            result["warnings"].append({
                "type": "frozen_stale",
                "severity": "HIGH",
                "artifact": f"results/{q}/reports/frozen_numbers.json",
                "reason": frozen_status.get("reason", "Unknown"),
                "suggestion": "重新运行 solution-package-builder 更新冻结数字"
            })

        result["checks"]["per_question"]["details"][q] = q_result

        if verbose:
            critical_pct = q_result["critical"]["found"] / max(q_result["critical"]["expected"], 1) * 100
            high_pct = q_result["high"]["found"] / max(q_result["high"]["expected"], 1) * 100
            print(f"  {q}: Critical {critical_pct:.0f}%, High {high_pct:.0f}%")

    # 5. 计算总体得分
    print("\n[5/5] 计算总体得分...")
    if total_expected > 0:
        result["score"] = int(total_found / total_expected * 100)

    # 更新总体状态
    if result["failures"]:
        result["status"] = "FAIL"
        result["checks"]["global_artifacts"]["status"] = "FAIL"
    elif result["warnings"]:
        result["status"] = "WARN"

    return result


def save_report(report: dict):
    """保存审计报告"""
    QA_DIR.mkdir(parents=True, exist_ok=True)

    # 保存JSON
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 保存Markdown
    md_content = generate_markdown_report(report)
    REPORT_MD.write_text(md_content, encoding="utf-8")

    print(f"\n审计报告已保存:")
    print(f"  JSON: {REPORT_JSON}")
    print(f"  Markdown: {REPORT_MD}")


def generate_markdown_report(report: dict) -> str:
    """生成Markdown格式的报告"""
    lines = []
    lines.append("# 完整性审计报告")
    lines.append("")
    lines.append(f"**审计时间**: {report['audit_time']}")
    lines.append(f"**审计状态**: {'✅ PASS' if report['status'] == 'PASS' else '⚠️ WARN' if report['status'] == 'WARN' else '❌ FAIL'}")
    lines.append(f"**综合得分**: {report['score']}/100")
    lines.append("")

    # 审计摘要
    lines.append("## 审计摘要")
    lines.append("")
    lines.append("| 维度 | 状态 | 详情 |")
    lines.append("|------|------|------|")

    checks = report.get("checks", {})
    for check_name, check_data in checks.items():
        status_icon = "✅" if check_data.get("status") == "PASS" else "⚠️" if check_data.get("status") == "WARN" else "❌"

        if check_name == "global_artifacts":
            total = len(check_data.get("details", []))
            found = sum(1 for d in check_data.get("details", []) if d.get("status") == "OK")
            detail = f"{found}/{total} 完整"
        elif check_name == "code_reviews":
            total = len(check_data.get("details", []))
            found = sum(1 for d in check_data.get("details", []) if d.get("exists"))
            detail = f"{found}/{total} 存在"
        elif check_name == "audit_reports":
            total = len(check_data.get("details", []))
            passed = sum(1 for d in check_data.get("details", []) if d.get("status") in ["PASS", "WARN"])
            detail = f"{passed}/{total} 通过"
        elif check_name == "per_question":
            q_details = check_data.get("details", {})
            total_critical = sum(q["critical"]["expected"] for q in q_details.values())
            found_critical = sum(q["critical"]["found"] for q in q_details.values())
            detail = f"Critical: {found_critical}/{total_critical}"
        else:
            detail = check_data.get("status", "N/A")

        lines.append(f"| {check_name} | {status_icon} {check_data.get('status', 'N/A')} | {detail} |")

    lines.append("")

    # 缺失文件 / 状态异常（B-③：存在但内容 FAIL 的报告不再混进"缺失"清单渲染）
    failures = report.get("failures", [])
    warnings = report.get("warnings", [])
    # 属于"文件不在/为空"的类型；其余（audit_not_passed/frozen_stale/...）是"存在但未达标"
    MISSING_TYPES = {"missing_critical", "missing_high", "missing_audit_report", "empty_artifact"}
    missing_warnings = [w for w in warnings if w.get("type") in MISSING_TYPES]
    status_warnings = [w for w in warnings if w.get("type") not in MISSING_TYPES]

    if failures or missing_warnings:
        lines.append("## 缺失 / 空文件")
        lines.append("")

        if failures:
            lines.append("### ❌ 必须补齐")
            lines.append("")
            for i, failure in enumerate(failures, 1):
                lines.append(f"{i}. **{failure.get('artifact', 'Unknown')}** [{failure.get('severity', 'CRITICAL')}]")
                lines.append(f"   - 用途: {failure.get('description', '')}")
                if "suggestion" in failure:
                    lines.append(f"   - 生成方式: {failure['suggestion']}")
                lines.append("")

        if missing_warnings:
            lines.append("### ⚠️ 建议补齐")
            lines.append("")
            for i, warning in enumerate(missing_warnings, 1):
                lines.append(f"{i}. **{warning.get('artifact', 'Unknown')}** [{warning.get('severity', 'HIGH')}]")
                lines.append(f"   - 用途: {warning.get('description', '')}")
                if "suggestion" in warning:
                    lines.append(f"   - 生成方式: {warning['suggestion']}")
                lines.append("")

    if status_warnings:
        lines.append("## 状态异常（文件存在但内容未通过）")
        lines.append("")
        for i, warning in enumerate(status_warnings, 1):
            status_extra = f"（状态: {warning['status']}）" if warning.get("status") else ""
            lines.append(f"{i}. **{warning.get('artifact', 'Unknown')}** [{warning.get('severity', 'HIGH')}] {status_extra}")
            lines.append(f"   - 说明: {warning.get('description', '')}")
            if "reason" in warning:
                lines.append(f"   - 原因: {warning['reason']}")
            if "suggestion" in warning:
                lines.append(f"   - 建议: {warning['suggestion']}")
            lines.append("")

    # 代码审查质量
    code_reviews = checks.get("code_reviews", {}).get("details", [])
    if code_reviews:
        lines.append("## 代码审查质量")
        lines.append("")
        lines.append("| 文件 | 检查项数 | file:ref | 质量 |")
        lines.append("|------|---------|----------|------|")

        for review in code_reviews:
            if review.get("exists"):
                check_items = review.get("check_items", 0)
                has_ref = "✅" if review.get("has_file_line_refs") else "❌"
                quality = review.get("quality", "N/A")
                lines.append(f"| {review.get('path', '')} | {check_items}项 | {has_ref} | {quality} |")

        lines.append("")

    # 子问题产物详情
    per_question = checks.get("per_question", {}).get("details", {})
    if per_question:
        lines.append("## 子问题产物详情")
        lines.append("")

        for q, q_data in per_question.items():
            lines.append(f"### {q}")
            lines.append("")

            critical = q_data.get("critical", {})
            lines.append(f"- **关键产物**: {critical.get('found', 0)}/{critical.get('expected', 0)}")

            if critical.get("missing"):
                for item in critical["missing"]:
                    lines.append(f"  - ❌ {item.get('path', '')}: {item.get('description', '')}")

            high = q_data.get("high", {})
            lines.append(f"- **高优先级**: {high.get('found', 0)}/{high.get('expected', 0)}")

            if high.get("missing"):
                for item in high["missing"]:
                    lines.append(f"  - ⚠️ {item.get('path', '')}: {item.get('description', '')}")

            frozen = q_data.get("frozen_numbers", {})
            if frozen.get("exists"):
                fresh_icon = "✅" if frozen.get("is_fresh") else "⚠️"
                lines.append(f"- **frozen_numbers**: {fresh_icon} {'时效' if frozen.get('is_fresh') else '过时'}")

            lines.append("")

    # 下一步
    lines.append("## 下一步")
    lines.append("")
    if report["status"] == "PASS":
        lines.append("- ✅ 完整性审计通过")
        lines.append("- 进入 quality-assurance-auditor")
    elif report["status"] == "WARN":
        lines.append("- ⚠️ 有警告需要关注")
        lines.append("- 建议补齐缺失文件后重新审计")
    else:
        lines.append("- ❌ 审计失败，必须补齐缺失文件")
        lines.append("- 修复后重新运行完整性审计")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="完整性审计脚本")
    parser.add_argument("--question", type=str, help="指定子问题（如Q1）")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    print("=" * 60)
    print("完整性审计开始")
    print("=" * 60)

    # 获取子问题列表
    if args.question:
        questions = [args.question]
    else:
        questions = get_question_dirs()

    if not questions:
        print("⚠️ 未找到子问题目录")
        questions = []

    print(f"子问题: {', '.join(questions) if questions else '无'}")

    # 执行审计
    report = run_audit(questions, args.verbose)

    # 保存报告
    save_report(report)

    # 输出摘要
    print("\n" + "=" * 60)
    print("审计完成")
    print("=" * 60)
    print(f"状态: {report['status']}")
    print(f"得分: {report['score']}/100")
    print(f"失败项: {len(report['failures'])}")
    print(f"警告项: {len(report['warnings'])}")

    # 返回退出码
    if report["status"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()