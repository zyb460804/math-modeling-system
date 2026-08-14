#!/usr/bin/env python3
"""数字一致性检查脚本（v4.9 qa_config 驱动版）

检查论文中的关键数字是否与代码实际输出一致。
防止论文编造数字或使用错误版本的代码输出。

期望数字字段外置到赛题配置 paper_output/plan/qa_config.json 的 number_consistency 段
（schema 示例见 .claude/skills/quality-assurance-auditor/references/qa_config.example.json）：
- pattern：论文侧正则（第 1 个捕获组为数字）；
- json_path：代码侧取值路径（点号分隔，相对 paper_output/results/{qi}_results.json）；
- scale：换算系数（如比率 0-1 折算成百分比时为 100），缺省 1；无 json_path 的条目只提取不比对。

该段缺失/为空时输出 SKIP（退出码 0，与 check_parameter_consistency 的 SKIP 口径一致），
绝不输出 PASS。配置存在但论文引用了某关键数字、而代码结果文件或对应字段缺失时，
记 CODE_SOURCE_MISSING 不一致（fail-closed，收口换题恒绿漏洞 CR-1/G-03 复现 A）。
配置的关键数字在论文中一个都没匹配到时，状态降为 WARNING（"没检查到"不等于"一致"）。

用法：
    python check_number_consistency.py [--paper PAPER_PATH] [--config CONFIG_PATH]

输出：
    - 控制台报告
    - paper_output/qa/number_consistency_report.json
    - paper_output/qa/number_consistency_report.md
"""

import argparse
import json
import re
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
RESULTS_DIR = OUTPUT_DIR / "results"
PAPER_FILE = OUTPUT_DIR / "final_paper_source.md"
REPORT_JSON = QA_DIR / "number_consistency_report.json"
REPORT_MD = QA_DIR / "number_consistency_report.md"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "plan" / "qa_config.json"
EXAMPLE_CONFIG_HINT = ".claude/skills/quality-assurance-auditor/references/qa_config.example.json"

REQUIRED_SECTION = "number_consistency"

# 容差配置（与赛题无关，保留在脚本内）
TOLERANCE = {
    "absolute": 0.05,      # 绝对容差：5%
    "percentage": 0.10,    # 百分比容差：10个百分点
    "cost": 0.15,          # 成本容差：15%
}


def load_qa_config(config_path: Path) -> tuple:
    """读取赛题配置。返回 (config, skip_reason)；skip_reason 非空表示应 SKIP。

    与 check_parameter_consistency.py 保持同一口径：文件缺失→SKIP；
    文件损坏（非法 JSON）→ 显式报错退出 1（fail-closed）。
    """
    if not config_path.exists():
        return None, (f"未找到赛题配置 {config_path}（新赛题需先生成，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"错误：赛题配置 {config_path} 读取/解析失败：{exc}")
        raise SystemExit(1)
    if REQUIRED_SECTION not in config:
        return None, (f"赛题配置 {config_path} 缺少段 [{REQUIRED_SECTION}]（新赛题需先补齐，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    return config, ""


def number_sections(config: dict) -> dict[str, dict]:
    """取 number_consistency 段（跳过 _ 开头的注释键，值必须是 dict）。"""
    raw = config.get(REQUIRED_SECTION)
    if not isinstance(raw, dict):
        return {}
    sections: dict[str, dict] = {}
    for qid, patterns in raw.items():
        if str(qid).startswith("_") or not isinstance(patterns, dict):
            continue
        sections[qid] = {
            key: spec for key, spec in patterns.items()
            if not str(key).startswith("_") and isinstance(spec, dict)
        }
    return sections


def write_skip_reports(reason: str) -> None:
    """配置缺失时写 SKIP 状态报告（绝不写 PASS）。"""
    payload = {
        "schema_version": "1.1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "SKIP",
        "reason": reason,
    }
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join(["# 数字一致性检查报告", "", "- 状态: `SKIP`", f"- 原因: {reason}", ""]),
        encoding="utf-8",
    )


def load_json(path: Path) -> Any:
    """加载 JSON 文件"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}


def lookup_json_path(data: Any, dotted_path: str) -> Any:
    """按点号分隔路径取嵌套值，任一层缺失返回 None。"""
    current = data
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def extract_numbers_from_paper(text: str, question_id: str, patterns: dict) -> dict[str, float]:
    """从论文中提取关键数字（pattern 第 1 个捕获组）"""
    results = {}
    for key, spec in patterns.items():
        pattern = str(spec.get("pattern") or "")
        if not pattern:
            continue
        matches = re.findall(pattern, text)
        if matches:
            try:
                value = matches[0].replace(",", "")
                results[key] = float(value)
            except ValueError:
                pass
    return results


def extract_numbers_from_code(question_id: str, patterns: dict) -> tuple[dict[str, float], bool]:
    """从代码结果 JSON 提取关键数字（json_path + scale）。

    返回 (values, file_exists)。file_exists=False 表示结果文件缺失或不可解析，
    供 compare_numbers 区分"字段缺失"与"结果文件缺失"两种无来源情形。
    """
    values: dict[str, float] = {}
    result_file = RESULTS_DIR / f"{question_id.lower()}_results.json"
    if not result_file.exists():
        return values, False
    data = load_json(result_file)
    if not isinstance(data, dict) or "__error__" in data:
        return values, False
    for key, spec in patterns.items():
        dotted = str(spec.get("json_path") or "").strip()
        if not dotted:
            continue
        raw = lookup_json_path(data, dotted)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            continue
        values[key] = raw * float(spec.get("scale", 1.0))
    return values, True


def compare_numbers(paper_values: dict, code_values: dict, question_id: str,
                    code_file_exists: bool) -> list[dict]:
    """比较论文和代码中的数字。

    论文侧匹配到、代码侧无对应值时记 CODE_SOURCE_MISSING（fail-closed）：
    旧版在此静默跳过——论文捏造数字 + 结果文件缺失照样"✅ 数字一致"（G-03 复现 A）。
    """
    discrepancies = []
    for key, paper_val in paper_values.items():
        code_val = code_values.get(key)
        if code_val is None:
            missing_kind = "代码结果文件缺失" if not code_file_exists else "代码侧字段缺失"
            discrepancies.append({
                "question_id": question_id,
                "key": key,
                "paper_value": paper_val,
                "code_value": None,
                "diff_percent": missing_kind,
                "status": "CODE_SOURCE_MISSING",
            })
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


def generate_report(sections: dict, all_discrepancies: list[dict],
                    unmatched_notes: list[str], matched_count: int) -> dict:
    """生成检查报告。

    有不一致 → FAIL；无不一致但配置的数字一个都没匹配到 → WARNING（不给假绿灯 PASS）。
    """
    total_configured = sum(len(patterns) for patterns in sections.values())
    if all_discrepancies:
        status = "FAIL"
    elif unmatched_notes:
        status = "WARNING"
    else:
        status = "PASS"
    return {
        "schema_version": "1.1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_configured": total_configured,
        "matched": matched_count,
        "passed": matched_count - len(all_discrepancies),
        "failed": len(all_discrepancies),
        "unmatched_notes": unmatched_notes,
        "discrepancies": all_discrepancies,
        "status": status,
    }


def write_markdown_report(report: dict) -> str:
    """生成 Markdown 格式的报告"""
    lines = [
        "# 数字一致性检查报告",
        "",
        f"- 状态: `{report['status']}`",
        f"- 配置检查项: {report['total_configured']}",
        f"- 实际比对: {report['matched']}",
        f"- 通过: {report['passed']}",
        f"- 失败: {report['failed']}",
        "",
    ]

    if report.get("unmatched_notes"):
        lines.append("## 未匹配项（配置了但论文中没出现，未产生实际比对）")
        lines.append("")
        for note in report["unmatched_notes"]:
            lines.append(f"- {note}")
        lines.append("")

    if report["discrepancies"]:
        lines.append("## 不一致项")
        lines.append("")
        lines.append("| 问题 | 指标 | 论文值 | 代码值 | 差异 |")
        lines.append("|------|------|--------|--------|------|")

        for d in report["discrepancies"]:
            lines.append(
                f"| {d['question_id']} | {d['key']} | {d['paper_value']} "
                f"| {d['code_value']} | {d['diff_percent']} |"
            )

        lines.append("")
        lines.append("## 修复建议")
        lines.append("")
        lines.append("1. 以代码实际输出为准修改论文数字（或修正代码后重跑）")
        lines.append("2. CODE_SOURCE_MISSING 项：论文引用了 qa_config 声明的关键数字，"
                     "但代码结果文件/字段缺失——补跑代码或修正 number_consistency 配置")
        lines.append("3. 重新运行代码确保结果正确")
    elif not report.get("unmatched_notes"):
        lines.append("## 结果")
        lines.append("")
        lines.append(f"✅ 所有关键数字与代码输出一致（比对 {report['matched']} 个）。")

    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="数字一致性检查：对照赛题配置 qa_config.json 的 number_consistency 段核对论文数字与代码结果"
    )
    parser.add_argument("--paper", type=str, default=str(PAPER_FILE), help="论文文件路径")
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH),
                        help=f"赛题配置 JSON 路径（默认 {DEFAULT_CONFIG_PATH}）")
    parser.add_argument("--fix", action="store_true", help="自动修复（暂不支持，传入即报错退出）")
    args = parser.parse_args(argv)

    # M-9：原版静默收下 --fix 再什么都不做，改为显式报错（rc=2），避免"以为修了"
    if args.fix:
        parser.error("--fix 自动修复暂不支持：请以代码实际输出为准修正论文数字后重跑本检查")

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"❌ 论文文件不存在: {paper_path}")
        return 1
    try:
        # utf-8-sig：兼容带 BOM 的源稿；损坏编码显式 FAIL（不写报告）
        paper_text = paper_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"❌ 无法读取论文文件 {paper_path}：{exc}")
        return 1

    print("数字一致性检查")
    print("=" * 50)

    cfg, skip_reason = load_qa_config(Path(args.config))
    if skip_reason:
        print(f"SKIP（qa_config 未配置 number_consistency）：{skip_reason}")
        write_skip_reports(skip_reason)
        return 0

    sections = number_sections(cfg)
    if not sections:
        reason = (f"赛题配置 {REQUIRED_SECTION} 段为空（新赛题需按本题关键数字补齐，"
                  f"格式参考 {EXAMPLE_CONFIG_HINT}）")
        print(f"SKIP（qa_config 未配置 number_consistency）：{reason}")
        write_skip_reports(reason)
        return 0

    # 检查每个问题
    all_discrepancies = []
    unmatched_notes = []
    matched_count = 0
    for qid, patterns in sections.items():
        print(f"\n检查 {qid}（配置 {len(patterns)} 个关键数字）...")

        paper_numbers = extract_numbers_from_paper(paper_text, qid, patterns)
        print(f"  论文数字: {paper_numbers}")

        code_numbers, code_file_exists = extract_numbers_from_code(qid, patterns)
        suffix = "" if code_file_exists else "（结果文件缺失）"
        print(f"  代码数字: {code_numbers}{suffix}")

        discrepancies = compare_numbers(paper_numbers, code_numbers, qid, code_file_exists)
        all_discrepancies.extend(discrepancies)
        matched_count += len(paper_numbers)

        if not paper_numbers:
            unmatched_notes.append(
                f"{qid}: 配置的 {len(patterns)} 个关键数字在论文中均未匹配到"
                f"（模式过期或论文未引用，未产生实际比对）"
            )
            print("  ⚠️ 论文侧 0 个数字匹配配置模式，本问未产生实际比对")
        elif discrepancies:
            print(f"  ❌ 发现 {len(discrepancies)} 个不一致项")
            for d in discrepancies:
                print(f"    - {d['key']}: 论文={d['paper_value']}, 代码={d['code_value']}, 差异={d['diff_percent']}")
        else:
            print(f"  ✅ 数字一致（比对 {len(paper_numbers)} 个）")

    # 生成报告
    report = generate_report(sections, all_discrepancies, unmatched_notes, matched_count)

    # 保存报告
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(write_markdown_report(report), encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"检查完成: {report['status']}")
    print(f"配置检查项: {report['total_configured']}")
    print(f"实际比对: {report['matched']}")
    print(f"通过: {report['passed']}")
    print(f"失败: {report['failed']}")
    if unmatched_notes:
        print(f"未匹配: {len(unmatched_notes)} 问（详见报告）")
    print(f"报告: {REPORT_MD}")

    return 0 if report["status"] in ("PASS", "WARNING") else 1


if __name__ == "__main__":
    sys.exit(main())
