#!/usr/bin/env python3
"""
一致性审计脚本

检查论文数字、文件名、符号与frozen_numbers.json和代码输出的交叉一致性。

用法：
    python audit.py [--paper PAPER_PATH] [--strict] [--tolerance TOLERANCE]

输出：
    - 控制台报告
    - paper_output/qa/consistency_audit_report.json
    - paper_output/qa/consistency_audit_report.md
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
SYMBOL_TABLE = OUTPUT_DIR / "plan" / "symbol_table.md"
REPORT_JSON = QA_DIR / "consistency_audit_report.json"
REPORT_MD = QA_DIR / "consistency_audit_report.md"

# 默认容差
DEFAULT_TOLERANCE = {
    "number": 0.05,      # 5% 数字容差
    "percentage": 0.10,  # 10% 百分比容差
}


def load_json(path: Path) -> Any:
    """加载 JSON 文件"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}


def load_frozen_numbers() -> dict:
    """加载所有frozen_numbers.json"""
    frozen = {}
    if not RESULTS_DIR.exists():
        return frozen

    for q_dir in RESULTS_DIR.iterdir():
        if q_dir.is_dir() and q_dir.name.startswith("Q"):
            frozen_file = q_dir / "reports" / "frozen_numbers.json"
            if frozen_file.exists():
                data = load_json(frozen_file)
                if data and "__error__" not in data:
                    frozen[q_dir.name] = data
    return frozen


def load_symbol_table() -> dict:
    """加载符号表"""
    if not SYMBOL_TABLE.exists():
        return {}

    content = SYMBOL_TABLE.read_text(encoding="utf-8")
    symbols = {}

    # 解析符号表（假设Markdown表格格式）
    # | 符号 | 含义 | 类型 | 子问题 |
    pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
    for match in re.finditer(pattern, content):
        symbol, meaning, sym_type, question = match.groups()
        symbol = symbol.strip()
        if symbol and symbol != "符号" and not symbol.startswith("-"):
            symbols[symbol] = {
                "meaning": meaning.strip(),
                "type": sym_type.strip(),
                "question": question.strip()
            }
    return symbols


def extract_numbers_from_paper(text: str) -> list[dict]:
    """从论文中提取所有数字"""
    numbers = []

    # 匹配各种数字格式
    patterns = [
        # 普通数字：123, 123.45, 1,234
        r'(?<![a-zA-Z])(\d[\d,]*\.?\d*)(?![a-zA-Z])',
        # 百分比：12.3%
        r'(\d+\.?\d*)\s*%',
        # 科学计数法：1.23e-4
        r'(\d+\.?\d*)\s*[eE]\s*[-+]?\d+',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            value_str = match.group(1).replace(",", "")
            try:
                value = float(value_str)
                # 获取上下文
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].replace("\n", " ")

                numbers.append({
                    "value": value,
                    "raw": match.group(0),
                    "position": match.start(),
                    "context": context
                })
            except ValueError:
                continue

    return numbers


def extract_file_references(text: str) -> list[dict]:
    """从论文中提取文件引用"""
    references = []

    # 匹配图表引用
    patterns = [
        (r'见图\s*(\d+)', "figure"),
        (r'如图\s*(\d+)', "figure"),
        (r'图\s*(\d+)', "figure"),
        (r'见表\s*(\d+)', "table"),
        (r'如表\s*(\d+)', "table"),
        (r'表\s*(\d+)', "table"),
    ]

    for pattern, ref_type in patterns:
        for match in re.finditer(pattern, text):
            ref_num = match.group(1)
            references.append({
                "type": ref_type,
                "number": int(ref_num),
                "raw": match.group(0),
                "position": match.start()
            })

    return references


def extract_symbols_from_paper(text: str) -> list[dict]:
    """从论文中提取数学符号"""
    symbols = []

    # 匹配LaTeX数学符号
    patterns = [
        # $...$ 行内公式
        r'\$([^$]+)\$',
        # $$...$$ 行间公式
        r'\$\$([^$]+)\$\$',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            formula = match.group(1)

            # 提取单字符符号（希腊字母、拉丁字母）
            symbol_pattern = r'\\([a-zA-Z]+)|([a-zA-Z])'
            for sym_match in re.finditer(symbol_pattern, formula):
                symbol = sym_match.group(1) or sym_match.group(2)
                if symbol and len(symbol) <= 3:  # 过滤掉长命令
                    symbols.append({
                        "symbol": symbol,
                        "formula": formula,
                        "position": match.start()
                    })

    return symbols


def check_number_consistency(paper_numbers: list[dict], frozen: dict, tolerance: float) -> dict:
    """检查数字一致性"""
    result = {
        "status": "PASS",
        "total": len(paper_numbers),
        "matched": 0,
        "mismatched": 0,
        "missing": 0,
        "details": []
    }

    # 从frozen中提取所有数字
    frozen_values = {}
    for q_id, q_data in frozen.items():
        if "claims" in q_data:
            for claim in q_data["claims"]:
                key = f"{q_id}_{claim.get('id', '')}"
                frozen_values[key] = {
                    "value": claim.get("value"),
                    "label": claim.get("label", ""),
                    "source": claim.get("source_file", "")
                }

    # 检查论文中的数字是否有对应的frozen值
    # 注意：不是所有数字都需要在frozen中，只检查关键结果数字
    for paper_num in paper_numbers[:50]:  # 限制检查数量
        value = paper_num["value"]

        # 跳过小数字（可能是编号、页码等）
        if value < 1 or value > 1000000:
            continue

        # 在frozen中查找匹配
        matched = False
        for frozen_key, frozen_data in frozen_values.items():
            frozen_value = frozen_data["value"]
            if frozen_value is None:
                continue

            # 计算差异
            if frozen_value != 0:
                diff_ratio = abs(value - frozen_value) / abs(frozen_value)
            else:
                diff_ratio = abs(value - frozen_value)

            if diff_ratio <= tolerance:
                matched = True
                result["matched"] += 1
                break

        if not matched:
            # 可能是新数字或不在frozen中的数字，记录为warning
            result["details"].append({
                "type": "number_not_frozen",
                "value": value,
                "context": paper_num["context"][:100]
            })

    return result


def check_file_references(references: list[dict], output_dir: Path) -> dict:
    """检查文件引用一致性"""
    result = {
        "status": "PASS",
        "total": len(references),
        "found": 0,
        "missing": 0,
        "details": []
    }

    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"

    for ref in references:
        ref_type = ref["type"]
        ref_num = ref["number"]

        # 检查文件是否存在
        found = False
        if ref_type == "figure":
            # 搜索可能的文件名模式
            patterns = [
                f"figure_{ref_num}.*",
                f"fig_{ref_num}.*",
                f"fig{ref_num}.*",
                f"图{ref_num}.*",
            ]
            for pattern in patterns:
                if figures_dir.exists():
                    matches = list(figures_dir.glob(pattern))
                    if matches:
                        found = True
                        break
        elif ref_type == "table":
            patterns = [
                f"table_{ref_num}.*",
                f"tab_{ref_num}.*",
                f"tab{ref_num}.*",
                f"表{ref_num}.*",
            ]
            for pattern in patterns:
                if tables_dir.exists():
                    matches = list(tables_dir.glob(pattern))
                    if matches:
                        found = True
                        break

        if found:
            result["found"] += 1
        else:
            result["missing"] += 1
            result["details"].append({
                "type": "file_missing",
                "reference": ref["raw"],
                "expected_location": f"figures/ 或 tables/"
            })

    if result["missing"] > 0:
        result["status"] = "FAIL"

    return result


def check_symbol_consistency(paper_symbols: list[dict], symbol_table: dict) -> dict:
    """检查符号一致性"""
    result = {
        "status": "PASS",
        "total": len(set(s["symbol"] for s in paper_symbols)),
        "consistent": 0,
        "conflicts": 0,
        "details": []
    }

    # 统计每个符号的使用位置
    symbol_usage = {}
    for sym in paper_symbols:
        symbol = sym["symbol"]
        if symbol not in symbol_usage:
            symbol_usage[symbol] = []
        symbol_usage[symbol].append(sym["position"])

    # 检查符号是否在symbol_table中定义
    for symbol, positions in symbol_usage.items():
        if symbol in symbol_table:
            result["consistent"] += 1
        else:
            # 符号未在symbol_table中定义
            result["conflicts"] += 1
            result["details"].append({
                "type": "undefined_symbol",
                "symbol": symbol,
                "usage_count": len(positions),
                "first_position": positions[0]
            })

    if result["conflicts"] > 0:
        result["status"] = "WARN"

    return result


def check_code_output_consistency(frozen: dict, output_dir: Path) -> dict:
    """检查代码输出一致性"""
    result = {
        "status": "PASS",
        "total": 0,
        "matched": 0,
        "mismatched": 0,
        "details": []
    }

    # 检查每个frozen claim的source_file是否存在
    for q_id, q_data in frozen.items():
        if "claims" not in q_data:
            continue

        for claim in q_data["claims"]:
            result["total"] += 1

            source_file = claim.get("source_file")
            if source_file:
                source_path = output_dir / source_file
                if source_path.exists():
                    result["matched"] += 1
                else:
                    result["mismatched"] += 1
                    result["details"].append({
                        "type": "source_file_missing",
                        "claim_id": claim.get("id"),
                        "source_file": source_file
                    })

    if result["mismatched"] > 0:
        result["status"] = "FAIL"

    return result


def generate_report(checks: dict, output_dir: Path) -> dict:
    """生成审计报告"""
    # 计算总体状态
    has_fail = any(c.get("status") == "FAIL" for c in checks.values())
    has_warn = any(c.get("status") == "WARN" for c in checks.values())

    if has_fail:
        status = "FAIL"
    elif has_warn:
        status = "WARN"
    else:
        status = "PASS"

    # 计算得分
    total_checks = sum(c.get("total", 0) for c in checks.values())
    passed_checks = sum(c.get("matched", 0) + c.get("found", 0) + c.get("consistent", 0) for c in checks.values())
    score = int(passed_checks / max(total_checks, 1) * 100)

    # 收集failures和warnings
    failures = []
    warnings = []

    for check_name, check_data in checks.items():
        if check_data.get("status") == "FAIL":
            for detail in check_data.get("details", []):
                failures.append({
                    "check": check_name,
                    "severity": "CRITICAL",
                    **detail
                })
        elif check_data.get("status") == "WARN":
            for detail in check_data.get("details", []):
                warnings.append({
                    "check": check_name,
                    "severity": "HIGH",
                    **detail
                })

    report = {
        "audit_type": "consistency",
        "audit_time": datetime.now().isoformat(),
        "status": status,
        "score": score,
        "checks": checks,
        "failures": failures,
        "warnings": warnings
    }

    return report


def save_report(report: dict, output_dir: Path):
    """保存审计报告"""
    qa_dir = output_dir / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)

    # 保存JSON
    report_json = qa_dir / "consistency_audit_report.json"
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 保存Markdown
    report_md = qa_dir / "consistency_audit_report.md"
    md_content = generate_markdown_report(report)
    report_md.write_text(md_content, encoding="utf-8")

    print(f"审计报告已保存:")
    print(f"  JSON: {report_json}")
    print(f"  Markdown: {report_md}")


def generate_markdown_report(report: dict) -> str:
    """生成Markdown格式的报告"""
    lines = []
    lines.append("# 一致性审计报告")
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

        if check_name == "number_consistency":
            detail = f"{check_data.get('matched', 0)}/{check_data.get('total', 0)} 匹配"
        elif check_name == "file_reference":
            detail = f"{check_data.get('found', 0)}/{check_data.get('total', 0)} 存在"
        elif check_name == "symbol_consistency":
            detail = f"{check_data.get('consistent', 0)}/{check_data.get('total', 0)} 一致"
        elif check_name == "code_output":
            detail = f"{check_data.get('matched', 0)}/{check_data.get('total', 0)} 匹配"
        else:
            detail = check_data.get("status", "N/A")

        lines.append(f"| {check_name} | {status_icon} {check_data.get('status', 'N/A')} | {detail} |")

    lines.append("")

    # 发现的问题
    failures = report.get("failures", [])
    warnings = report.get("warnings", [])

    if failures or warnings:
        lines.append("## 发现的问题")
        lines.append("")

        if failures:
            lines.append("### ❌ 必须修复")
            lines.append("")
            for i, failure in enumerate(failures, 1):
                lines.append(f"{i}. **{failure.get('type', 'Unknown')}** [{failure.get('severity', 'CRITICAL')}]")
                if "symbol" in failure:
                    lines.append(f"   - 符号: {failure['symbol']}")
                if "reference" in failure:
                    lines.append(f"   - 引用: {failure['reference']}")
                if "value" in failure:
                    lines.append(f"   - 数值: {failure['value']}")
                lines.append("")

        if warnings:
            lines.append("### ⚠️ 建议修复")
            lines.append("")
            for i, warning in enumerate(warnings, 1):
                lines.append(f"{i}. **{warning.get('type', 'Unknown')}** [{warning.get('severity', 'HIGH')}]")
                if "symbol" in warning:
                    lines.append(f"   - 符号: {warning['symbol']}")
                if "usage_count" in warning:
                    lines.append(f"   - 使用次数: {warning['usage_count']}")
                lines.append("")

    # 下一步
    lines.append("## 下一步")
    lines.append("")
    if report["status"] == "PASS":
        lines.append("- ✅ 一致性审计通过")
        lines.append("- 进入 completeness-auditor")
    elif report["status"] == "WARN":
        lines.append("- ⚠️ 有警告需要关注")
        lines.append("- 建议修复后重新审计")
    else:
        lines.append("- ❌ 审计失败，必须修复")
        lines.append("- 修复后重新运行一致性审计")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="一致性审计脚本")
    parser.add_argument("--paper", type=str, default=str(PAPER_FILE),
                        help="论文文件路径")
    parser.add_argument("--strict", action="store_true",
                        help="严格模式（不容差）")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE["number"],
                        help="数字容差（默认0.05）")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    output_dir = OUTPUT_DIR
    tolerance = 0 if args.strict else args.tolerance

    print("=" * 60)
    print("一致性审计开始")
    print("=" * 60)

    # 检查论文文件
    if not paper_path.exists():
        print(f"❌ 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")
    print(f"✅ 加载论文: {paper_path}")

    # 加载frozen_numbers
    frozen = load_frozen_numbers()
    print(f"✅ 加载frozen_numbers: {len(frozen)}个子问题")

    # 加载symbol_table
    symbol_table = load_symbol_table()
    print(f"✅ 加载symbol_table: {len(symbol_table)}个符号")

    # 提取论文中的数字
    paper_numbers = extract_numbers_from_paper(paper_text)
    print(f"✅ 提取论文数字: {len(paper_numbers)}个")

    # 提取文件引用
    file_references = extract_file_references(paper_text)
    print(f"✅ 提取文件引用: {len(file_references)}个")

    # 提取符号
    paper_symbols = extract_symbols_from_paper(paper_text)
    print(f"✅ 提取数学符号: {len(paper_symbols)}个")

    # 执行检查
    print("\n" + "-" * 40)
    print("执行检查...")
    print("-" * 40)

    checks = {}

    # 1. 数字一致性检查
    print("\n[1/4] 检查数字一致性...")
    checks["number_consistency"] = check_number_consistency(paper_numbers, frozen, tolerance)
    print(f"  状态: {checks['number_consistency']['status']}")

    # 2. 文件引用检查
    print("\n[2/4] 检查文件引用...")
    checks["file_reference"] = check_file_references(file_references, output_dir)
    print(f"  状态: {checks['file_reference']['status']}")

    # 3. 符号一致性检查
    print("\n[3/4] 检查符号一致性...")
    checks["symbol_consistency"] = check_symbol_consistency(paper_symbols, symbol_table)
    print(f"  状态: {checks['symbol_consistency']['status']}")

    # 4. 代码输出一致性检查
    print("\n[4/4] 检查代码输出...")
    checks["code_output"] = check_code_output_consistency(frozen, output_dir)
    print(f"  状态: {checks['code_output']['status']}")

    # 生成报告
    print("\n" + "-" * 40)
    print("生成报告...")
    print("-" * 40)

    report = generate_report(checks, output_dir)
    save_report(report, output_dir)

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