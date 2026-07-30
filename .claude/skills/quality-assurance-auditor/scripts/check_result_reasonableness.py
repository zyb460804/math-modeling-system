#!/usr/bin/env python3
"""结果合理性检查脚本（v4.5 参数外置版）

检查代码输出的结果是否在合理范围内，防止代码 bug 导致不合理的结果。

合理范围外置到赛题配置 paper_output/plan/qa_config.json 的 reasonable_ranges 段
（可选 green_constraints / green_constraints_apply_to 段），schema 示例见
.claude/skills/quality-assurance-auditor/references/qa_config.example.json
（示例参数属于旧赛题「绿电直连型合成氨」）。配置或所需段缺失时输出 SKIP
（退出码 0）。结果文件缺失不再静默通过：部分缺失→WARNING，全部缺失→FAIL。

用法：
    python check_result_reasonableness.py [--config 配置路径]

输出：
    - 控制台报告
    - paper_output/qa/result_reasonableness_report.json
    - paper_output/qa/result_reasonableness_report.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
RESULTS_DIR = OUTPUT_DIR / "results"
REPORT_JSON = QA_DIR / "result_reasonableness_report.json"
REPORT_MD = QA_DIR / "result_reasonableness_report.md"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "plan" / "qa_config.json"
EXAMPLE_CONFIG_HINT = ".claude/skills/quality-assurance-auditor/references/qa_config.example.json"

REQUIRED_SECTIONS = ["reasonable_ranges"]


def load_qa_config(config_path: Path, required_sections: list) -> tuple:
    """读取赛题配置。返回 (config, skip_reason)；skip_reason 非空表示应 SKIP。"""
    if not config_path.exists():
        return None, (f"未找到赛题配置 {config_path}（新赛题需先生成，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"错误：赛题配置 {config_path} 读取/解析失败：{exc}")
        raise SystemExit(1)
    missing = [s for s in required_sections if s not in config]
    if missing:
        return None, (f"赛题配置 {config_path} 缺少段 {missing}（新赛题需先补齐，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    return config, ""


def write_skip_reports(reason: str) -> None:
    """配置缺失时写 SKIP 状态报告（绝不写 PASS）。"""
    payload = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "SKIP",
        "reason": reason,
    }
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join(["# 结果合理性检查报告", "", "- 状态: `SKIP`", f"- 原因: {reason}", ""]),
        encoding="utf-8",
    )


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def extract_indicators(data: dict) -> dict:
    """从结果文件中提取指标"""
    indicators = {}
    results = data.get("results", {})
    if isinstance(results, dict):
        for section in ("indicators", "cost", "energy"):
            sub = results.get(section, {})
            if isinstance(sub, dict):
                indicators.update(sub)
    for key, value in data.items():
        if isinstance(value, (int, float)) and key not in indicators:
            indicators[key] = value
    return indicators


def parse_range_spec(question_id: str, param: str, spec: Any) -> tuple:
    """解析 [min, max, 说明] 格式的范围配置"""
    try:
        min_val, max_val, desc = spec
        return float(min_val), float(max_val), str(desc)
    except (TypeError, ValueError) as exc:
        print(f"错误：reasonable_ranges.{question_id}.{param} 格式应为 [min, max, 说明]：{exc}")
        raise SystemExit(1)


def parse_constraint_spec(param: str, spec: Any) -> tuple:
    """解析 [阈值, 运算符, 说明] 格式的约束配置"""
    try:
        threshold, operator, desc = spec
        if operator not in (">=", "<="):
            raise ValueError(f"运算符必须是 >= 或 <=，实际为 {operator}")
        return float(threshold), str(operator), str(desc)
    except (TypeError, ValueError) as exc:
        print(f"错误：green_constraints.{param} 格式应为 [阈值, '>='或'<=', 说明]：{exc}")
        raise SystemExit(1)


def check_constraint(value: float, threshold: float, operator: str) -> bool:
    if operator == ">=":
        return value >= threshold
    if operator == "<=":
        return value <= threshold
    return False


def check_reasonableness(question_id: str, indicators: dict, ranges: dict,
                         green_constraints: dict, apply_green: bool) -> list:
    """检查结果合理性"""
    issues = []

    # 检查合理范围
    for param, spec in ranges.items():
        if str(param).startswith("_"):
            continue
        min_val, max_val, desc = parse_range_spec(question_id, param, spec)
        value = indicators.get(param)
        if value is not None and not (min_val <= value <= max_val):
            issues.append({
                "question_id": question_id,
                "param": param,
                "value": value,
                "range": f"[{min_val}, {max_val}]",
                "description": desc,
                "severity": "WARNING",
                "status": "OUT_OF_RANGE",
            })

    # 检查绿电类指标约束（按配置 green_constraints_apply_to 指定的问题）
    if apply_green:
        for param, spec in green_constraints.items():
            if str(param).startswith("_"):
                continue
            threshold, operator, desc = parse_constraint_spec(param, spec)
            value = indicators.get(param)
            if value is None:
                continue
            if value > 1:  # 百分比转小数
                value = value / 100
            if not check_constraint(value, threshold, operator):
                issues.append({
                    "question_id": question_id,
                    "param": param,
                    "value": value,
                    "constraint": f"{operator} {threshold}",
                    "description": desc,
                    "severity": "INFO",
                    "status": "CONSTRAINT_NOT_MET",
                })

    return issues


def generate_report(all_issues: list, missing_results: list,
                    total_questions: int) -> dict:
    """生成检查报告。结果文件全部缺失→FAIL；部分缺失→WARNING；不给假绿灯。"""
    report = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_questions": total_questions,
        "missing_results": missing_results,
        "warnings": 0,
        "info": 0,
        "issues": all_issues,
        "status": "PASS",
    }
    for issue in all_issues:
        if issue["severity"] == "WARNING":
            report["warnings"] += 1
        elif issue["severity"] == "INFO":
            report["info"] += 1
    if report["warnings"] > 0:
        report["status"] = "WARNING"
    if missing_results and len(missing_results) >= total_questions:
        report["status"] = "FAIL"  # 一个结果文件都没有，等于什么都没检查
    return report


def write_markdown_report(report: dict) -> str:
    """生成Markdown报告"""
    lines = [
        "# 结果合理性检查报告",
        "",
        f"- 状态: `{report['status']}`",
        f"- 警告: {report['warnings']}",
        f"- 信息: {report['info']}",
        f"- 缺失结果文件: {len(report['missing_results'])}/{report['total_questions']}",
        "",
    ]
    if report["status"] == "FAIL":
        lines.append("**所有问题的结果文件均缺失，本检查实际未验证任何结果，不能作为通过依据。**")
        lines.append("")
    if report["issues"]:
        lines.append("## 问题项")
        lines.append("")
        lines.append("| 问题 | 指标 | 值 | 约束/范围 | 说明 |")
        lines.append("|------|------|-----|----------|------|")
        for issue in report["issues"]:
            value = issue.get("value", "")
            if isinstance(value, float):
                value = f"{value:.2f}"
            constraint = issue.get("range", issue.get("constraint", ""))
            lines.append(f"| {issue['question_id']} | {issue['param']} | {value} | {constraint} | {issue['description']} |")
        lines.append("")
        lines.append("## 建议")
        lines.append("")
        lines.append("1. 检查代码逻辑是否正确实现了题目要求")
        lines.append("2. 检查参数设置是否与赛题配置一致")
        lines.append("3. 检查结果文件是否正确生成（paper_output/results/{qi}_results.json）")
    else:
        lines.append("## 结果")
        lines.append("")
        lines.append("✅ 已检查的结果均在合理范围内。")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="结果合理性检查：对照赛题配置 qa_config.json 的 reasonable_ranges 段检查模型结果"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH),
                        help="赛题配置 JSON 路径（默认 paper_output/plan/qa_config.json）")
    args = parser.parse_args(argv)

    print("结果合理性检查")
    print("=" * 50)

    cfg, skip_reason = load_qa_config(Path(args.config), REQUIRED_SECTIONS)
    if skip_reason:
        print(f"SKIP：{skip_reason}")
        write_skip_reports(skip_reason)
        return 0

    reasonable_ranges = {k: v for k, v in cfg["reasonable_ranges"].items()
                         if not str(k).startswith("_")}
    if not reasonable_ranges:
        reason = f"赛题配置 reasonable_ranges 段为空（新赛题需先补齐，格式参考 {EXAMPLE_CONFIG_HINT}）"
        print(f"SKIP：{reason}")
        write_skip_reports(reason)
        return 0
    green_constraints = {k: v for k, v in cfg.get("green_constraints", {}).items()
                         if not str(k).startswith("_")}
    green_apply_to = set(cfg.get("green_constraints_apply_to", []))

    all_issues = []
    missing_results = []
    for qid, ranges in reasonable_ranges.items():
        result_file = RESULTS_DIR / f"{qid.lower()}_results.json"
        print(f"\n检查 {qid}...")
        data = load_json(result_file)
        if not data:
            print(f"  ⚠️ 结果文件缺失或不可解析: {result_file}（不计为通过）")
            missing_results.append(qid)
            all_issues.append({
                "question_id": qid,
                "param": "(结果文件)",
                "value": "",
                "range": "",
                "description": f"结果文件缺失或不可解析: {result_file.name}",
                "severity": "WARNING",
                "status": "MISSING_RESULT_FILE",
            })
            continue

        indicators = extract_indicators(data)
        issues = check_reasonableness(qid, indicators, ranges,
                                      green_constraints, qid in green_apply_to)
        all_issues.extend(issues)
        if issues:
            print(f"  ⚠️ 发现 {len(issues)} 个问题")
            for issue in issues:
                print(f"    - {issue['param']}: {issue['value']} ({issue['status']})")
        else:
            print(f"  ✅ 结果合理")

    report = generate_report(all_issues, missing_results, len(reasonable_ranges))
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(write_markdown_report(report), encoding="utf-8")

    print(f"\n{'=' * 50}")
    print(f"检查完成: {report['status']}")
    print(f"报告: {REPORT_MD}")
    return 0 if report["status"] in ("PASS", "WARNING") else 1


if __name__ == "__main__":
    raise SystemExit(main())
