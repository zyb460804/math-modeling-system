#!/usr/bin/env python3
"""参数一致性检查脚本（v4.5 参数外置版）

检查代码中使用的参数是否与题目要求一致，防止代码使用错误参数。

期望参数外置到赛题配置 paper_output/plan/qa_config.json 的 expected_params 段
（schema 示例见 .claude/skills/quality-assurance-auditor/references/qa_config.example.json，
示例参数属于旧赛题「绿电直连型合成氨」）。配置或所需段缺失时输出 SKIP
（退出码 0），绝不输出 PASS。代码文件按约定 paper_output/code/modeling/{qi}_model.py 查找。

用法：
    python check_parameter_consistency.py [--config 配置路径]

输出：
    - 控制台报告
    - paper_output/qa/parameter_consistency_report.json
    - paper_output/qa/parameter_consistency_report.md
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
CODE_DIR = OUTPUT_DIR / "code" / "modeling"
REPORT_JSON = QA_DIR / "parameter_consistency_report.json"
REPORT_MD = QA_DIR / "parameter_consistency_report.md"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "plan" / "qa_config.json"
EXAMPLE_CONFIG_HINT = ".claude/skills/quality-assurance-auditor/references/qa_config.example.json"

REQUIRED_SECTIONS = ["expected_params"]
DEFAULT_TOLERANCE = 0.01  # 1%容差


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
        "\n".join(["# 参数一致性检查报告", "", "- 状态: `SKIP`", f"- 原因: {reason}", ""]),
        encoding="utf-8",
    )


def extract_params_from_code(code_text: str, param_names: list) -> dict:
    """从代码中提取参数值（按 NAME = 数值 的赋值模式）"""
    params = {}
    for param_name in param_names:
        pattern = re.escape(param_name) + r"\s*=\s*([\d.]+)"
        matches = re.findall(pattern, code_text)
        if matches:
            try:
                params[param_name] = float(matches[0])
            except ValueError:
                pass
    return params


def compare_params(extracted: dict, expected: dict, question_id: str,
                   tolerance: float) -> list:
    """比较提取的参数与期望参数"""
    discrepancies = []
    for param_name, expected_val in expected.items():
        if str(param_name).startswith("_"):
            continue
        extracted_val = extracted.get(param_name)
        if extracted_val is None:
            continue
        if abs(extracted_val - float(expected_val)) > tolerance:
            discrepancies.append({
                "question_id": question_id,
                "param": param_name,
                "expected": expected_val,
                "actual": extracted_val,
                "status": "MISMATCH",
            })
    return discrepancies


def check_code_file(filepath: Path, question_id: str, expected: dict,
                    tolerance: float) -> tuple:
    """检查单个代码文件的参数一致性。返回 (不一致列表, 文件是否存在)。"""
    if not filepath.exists():
        return [], False
    try:
        code_text = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"  错误：无法读取代码文件 {filepath}：{exc}")
        return [], False
    param_names = [k for k in expected if not str(k).startswith("_")]
    extracted = extract_params_from_code(code_text, param_names)
    return compare_params(extracted, expected, question_id, tolerance), True


def generate_report(expected_params: dict, all_discrepancies: list,
                    missing_files: list) -> dict:
    """生成检查报告。有不一致→FAIL；仅缺代码文件→WARNING（不给假绿灯 PASS）。"""
    if all_discrepancies:
        status = "FAIL"
    elif missing_files:
        status = "WARNING"
    else:
        status = "PASS"
    report = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_questions": len(expected_params),
        "passed": 0,
        "failed": 0,
        "missing_code_files": missing_files,
        "discrepancies": all_discrepancies,
        "status": status,
    }
    for qid in expected_params:
        if [d for d in all_discrepancies if d["question_id"] == qid]:
            report["failed"] += 1
        elif qid not in missing_files:
            report["passed"] += 1
    return report


def write_markdown_report(report: dict) -> str:
    """生成Markdown报告"""
    lines = [
        "# 参数一致性检查报告",
        "",
        f"- 状态: `{report['status']}`",
        f"- 检查问题数: {report['total_questions']}",
        f"- 通过: {report['passed']}",
        f"- 失败: {report['failed']}",
        f"- 缺少代码文件: {len(report['missing_code_files'])}",
        "",
    ]
    if report["missing_code_files"]:
        lines.append("## 缺少代码文件的问题")
        lines.append("")
        for qid in report["missing_code_files"]:
            lines.append(f"- {qid}: 未找到 paper_output/code/modeling/{qid.lower()}_model.py，该问未检查")
        lines.append("")
    if report["discrepancies"]:
        lines.append("## 不一致项")
        lines.append("")
        lines.append("| 问题 | 参数 | 期望值 | 实际值 |")
        lines.append("|------|------|--------|--------|")
        for d in report["discrepancies"]:
            lines.append(f"| {d['question_id']} | {d['param']} | {d['expected']} | {d['actual']} |")
        lines.append("")
        lines.append("## 修复建议")
        lines.append("")
        lines.append("1. 检查代码中的参数定义是否与题目要求一致")
        lines.append("2. 以赛题配置 qa_config.json 的 expected_params 段为准修正代码参数")
    elif not report["missing_code_files"]:
        lines.append("## 结果")
        lines.append("")
        lines.append("✅ 所有参数与题目要求一致。")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="参数一致性检查：对照赛题配置 qa_config.json 的 expected_params 段检查建模代码参数"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH),
                        help="赛题配置 JSON 路径（默认 paper_output/plan/qa_config.json）")
    args = parser.parse_args(argv)

    print("参数一致性检查")
    print("=" * 50)

    cfg, skip_reason = load_qa_config(Path(args.config), REQUIRED_SECTIONS)
    if skip_reason:
        print(f"SKIP：{skip_reason}")
        write_skip_reports(skip_reason)
        return 0

    expected_params = {k: v for k, v in cfg["expected_params"].items()
                       if not str(k).startswith("_")}
    if not expected_params:
        reason = f"赛题配置 expected_params 段为空（新赛题需先补齐，格式参考 {EXAMPLE_CONFIG_HINT}）"
        print(f"SKIP：{reason}")
        write_skip_reports(reason)
        return 0
    tolerance = float(cfg.get("param_tolerance", DEFAULT_TOLERANCE))

    all_discrepancies = []
    missing_files = []
    for qid, expected in expected_params.items():
        filepath = CODE_DIR / f"{qid.lower()}_model.py"
        print(f"\n检查 {qid} ({filepath.name})...")
        discrepancies, file_exists = check_code_file(filepath, qid, expected, tolerance)
        if not file_exists:
            print(f"  ⚠️ 代码文件不存在，跳过该问（不计为通过）")
            missing_files.append(qid)
            continue
        all_discrepancies.extend(discrepancies)
        if discrepancies:
            print(f"  ❌ 发现 {len(discrepancies)} 个参数不一致")
            for d in discrepancies:
                print(f"    - {d['param']}: 期望={d['expected']}, 实际={d['actual']}")
        else:
            print(f"  ✅ 参数一致")

    report = generate_report(expected_params, all_discrepancies, missing_files)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(write_markdown_report(report), encoding="utf-8")

    print(f"\n{'=' * 50}")
    print(f"检查完成: {report['status']}")
    print(f"报告: {REPORT_MD}")
    return 0 if report["status"] in ("PASS", "WARNING") else 1


if __name__ == "__main__":
    raise SystemExit(main())
