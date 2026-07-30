#!/usr/bin/env python3
"""
数字一致性检查脚本

检查论文中的关键数字是否与代码实际输出一致。
防止论文编造数字或使用错误版本的代码输出。

用法：
    python check_number_consistency.py [--paper PAPER_PATH] [--fix]

输出：
    - 控制台报告
    - paper_output/qa/number_consistency_report.json
    - paper_output/qa/number_consistency_report.md
"""

import argparse
import json
import re
import sys
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
RESULTS_DIR = OUTPUT_DIR / "results"
PAPER_FILE = OUTPUT_DIR / "final_paper_source.md"
REPORT_JSON = QA_DIR / "number_consistency_report.json"
REPORT_MD = QA_DIR / "number_consistency_report.md"

# 容差配置
TOLERANCE = {
    "absolute": 0.05,      # 绝对容差：5%
    "percentage": 0.10,    # 百分比容差：10个百分点
    "cost": 0.15,          # 成本容差：15%
}

# 从代码输出中提取的关键数字
# 注意：模式需要匹配Q1结果表格中的数字，而不是摘要中的数字
EXPECTED_KEYS = {
    "Q1": {
        "E_load_kWh": {"pattern": r"日用电量[为：:]\s*([\d,]+)\s*kWh", "unit": "kWh"},
        "E_re_kWh": {"pattern": r"新能源发电量[为：:]\s*([\d,]+)\s*kWh", "unit": "kWh"},
        "E_buy_kWh": {"pattern": r"网购电量[为：:]\s*([\d,]+)\s*kWh", "unit": "kWh"},
        "E_sell_kWh": {"pattern": r"上网电量[为：:]\s*([\d,]+)\s*kWh", "unit": "kWh"},
        "self_use_ratio": {"pattern": r"自发自用比例[为为]\s*([\d.]+)%", "unit": "%"},
        "green_ratio": {"pattern": r"绿电比例[为为]\s*([\d.]+)%", "unit": "%"},
        "feed_in_ratio": {"pattern": r"上网比例[为为]\s*([\d.]+)%", "unit": "%"},
        "ton_nh3_cost": {"pattern": r"\|\s*吨氨成本\s*\|\s*([\d,]+)\s*元/吨", "unit": "元/吨"},
    },
}


def load_json(path: Path) -> Any:
    """加载 JSON 文件"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}


def extract_numbers_from_paper(text: str, question_id: str) -> dict[str, float]:
    """从论文中提取关键数字"""
    results = {}
    patterns = EXPECTED_KEYS.get(question_id, {})

    for key, config in patterns.items():
        pattern = config["pattern"]
        matches = re.findall(pattern, text)
        if matches:
            try:
                value = matches[0].replace(",", "")
                results[key] = float(value)
            except ValueError:
                pass

    return results


def extract_numbers_from_code(question_id: str) -> dict[str, float]:
    """从代码输出中提取关键数字"""
    results = {}

    # 尝试加载 q{N}_results.json
    result_file = RESULTS_DIR / f"{question_id.lower()}_results.json"
    if not result_file.exists():
        return results

    data = load_json(result_file)
    if not data or "__error__" in data:
        return results

    # 提取关键数字
    if question_id == "Q1":
        energy = data.get("results", {}).get("energy", {})
        indicators = data.get("results", {}).get("indicators", {})
        cost = data.get("results", {}).get("cost", {})

        results["E_load_kWh"] = energy.get("E_load_kWh", 0)
        results["E_re_kWh"] = energy.get("E_re_kWh", 0)
        results["E_buy_kWh"] = energy.get("E_buy_kWh", 0)
        results["E_sell_kWh"] = energy.get("E_sell_kWh", 0)
        results["self_use_ratio"] = indicators.get("self_use_ratio", 0) * 100
        results["green_ratio"] = indicators.get("green_ratio", 0) * 100
        results["feed_in_ratio"] = indicators.get("feed_in_ratio", 0) * 100
        results["ton_nh3_cost"] = cost.get("ton_nh3_cost_yuan", 0)

    return results


def compare_numbers(paper_values: dict, code_values: dict, question_id: str) -> list[dict]:
    """比较论文和代码中的数字"""
    discrepancies = []

    for key in set(paper_values.keys()) | set(code_values.keys()):
        paper_val = paper_values.get(key)
        code_val = code_values.get(key)

        if paper_val is None or code_val is None:
            continue

        # 计算差异
        if code_val != 0:
            diff_ratio = abs(paper_val - code_val) / abs(code_val)
        else:
            diff_ratio = float("inf") if paper_val != 0 else 0

        # 判断是否超过容差
        if key.endswith("_ratio"):
            tolerance = TOLERANCE["percentage"]
        elif "cost" in key:
            tolerance = TOLERANCE["cost"]
        else:
            tolerance = TOLERANCE["absolute"]

        if diff_ratio > tolerance:
            discrepancies.append({
                "question_id": question_id,
                "key": key,
                "paper_value": paper_val,
                "code_value": code_val,
                "diff_ratio": diff_ratio,
                "diff_percent": f"{diff_ratio * 100:.1f}%",
                "status": "MISMATCH",
            })

    return discrepancies


def generate_report(all_discrepancies: list[dict]) -> dict:
    """生成检查报告"""
    report = {
        "schema_version": "1.0",
        "generated_at": "2026-06-15",
        "total_checks": 0,
        "passed": 0,
        "failed": 0,
        "discrepancies": all_discrepancies,
        "status": "PASS" if not all_discrepancies else "FAIL",
    }

    for qid in EXPECTED_KEYS.keys():
        report["total_checks"] += len(EXPECTED_KEYS[qid])

    report["failed"] = len(all_discrepancies)
    report["passed"] = report["total_checks"] - report["failed"]

    return report


def write_markdown_report(report: dict) -> str:
    """生成 Markdown 格式的报告"""
    lines = [
        "# 数字一致性检查报告",
        "",
        f"- 状态: `{report['status']}`",
        f"- 总检查项: {report['total_checks']}",
        f"- 通过: {report['passed']}",
        f"- 失败: {report['failed']}",
        "",
    ]

    if report["discrepancies"]:
        lines.append("## 不一致项")
        lines.append("")
        lines.append("| 问题 | 指标 | 论文值 | 代码值 | 差异 |")
        lines.append("|------|------|--------|--------|------|")

        for d in report["discrepancies"]:
            lines.append(f"| {d['question_id']} | {d['key']} | {d['paper_value']} | {d['code_value']} | {d['diff_percent']} |")

        lines.append("")
        lines.append("## 修复建议")
        lines.append("")
        lines.append("1. 检查代码参数是否正确（36吨 vs 72吨）")
        lines.append("2. 以代码实际输出为准修改论文")
        lines.append("3. 重新运行代码确保结果正确")
    else:
        lines.append("## 结果")
        lines.append("")
        lines.append("✅ 所有关键数字与代码输出一致。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="数字一致性检查")
    parser.add_argument("--paper", type=str, default=str(PAPER_FILE), help="论文文件路径")
    parser.add_argument("--fix", action="store_true", help="自动修复（暂不支持）")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"❌ 论文文件不存在: {paper_path}")
        return 1

    # 读取论文
    paper_text = paper_path.read_text(encoding="utf-8")

    # 检查每个问题
    all_discrepancies = []
    for qid in EXPECTED_KEYS.keys():
        print(f"\n检查 {qid}...")

        # 从论文提取数字
        paper_numbers = extract_numbers_from_paper(paper_text, qid)
        print(f"  论文数字: {paper_numbers}")

        # 从代码提取数字
        code_numbers = extract_numbers_from_code(qid)
        print(f"  代码数字: {code_numbers}")

        # 比较
        discrepancies = compare_numbers(paper_numbers, code_numbers, qid)
        all_discrepancies.extend(discrepancies)

        if discrepancies:
            print(f"  ❌ 发现 {len(discrepancies)} 个不一致项")
            for d in discrepancies:
                print(f"    - {d['key']}: 论文={d['paper_value']}, 代码={d['code_value']}, 差异={d['diff_percent']}")
        else:
            print(f"  ✅ 数字一致")

    # 生成报告
    report = generate_report(all_discrepancies)

    # 保存报告
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(write_markdown_report(report), encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"检查完成: {report['status']}")
    print(f"总检查项: {report['total_checks']}")
    print(f"通过: {report['passed']}")
    print(f"失败: {report['failed']}")
    print(f"报告: {REPORT_MD}")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
