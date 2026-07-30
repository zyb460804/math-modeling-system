#!/usr/bin/env python3
"""
数字自动修正器
检测论文中的数字与 frozen_numbers.json 不一致 → 自动修正论文中的数字

用法:
    python number_auto_fixer.py --errors path/to/errors.json
    python number_auto_fixer.py --paper paper_output/final_paper_source.md
    python number_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"
PAPER_DOCX = ROOT / "paper_output" / "final_paper.docx"
FROZEN_FILE = ROOT / "paper_output" / "frozen_numbers.json"
RESULTS_DIR = ROOT / "paper_output" / "results"


def load_frozen_numbers() -> dict:
    """加载冻结数字"""
    if FROZEN_FILE.exists():
        return json.loads(FROZEN_FILE.read_text(encoding="utf-8"))
    return {}


def load_result_numbers() -> dict:
    """从结果文件中提取数字"""
    numbers = {}
    for json_file in RESULTS_DIR.glob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            _extract_numbers_recursive(data, str(json_file.stem), numbers)
        except Exception:
            pass
    return numbers


def _extract_numbers_recursive(data, prefix: str, numbers: dict):
    """递归提取 JSON 中的数字"""
    if isinstance(data, dict):
        for k, v in data.items():
            _extract_numbers_recursive(v, f"{prefix}.{k}", numbers)
    elif isinstance(data, (int, float)):
        numbers[prefix] = data
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _extract_numbers_recursive(item, f"{prefix}[{i}]", numbers)


def find_number_inconsistencies(paper_text: str, frozen: dict, results: dict) -> list:
    """查找论文中的数字不一致"""
    inconsistencies = []

    # 从冻结数字中查找
    if "numbers" in frozen:
        for entry in frozen["numbers"]:
            value = entry.get("value")
            context = entry.get("context", "")
            if value is not None and context:
                # 在论文中搜索该上下文附近的数字
                pattern = re.escape(context[:20])
                matches = list(re.finditer(pattern, paper_text))
                for match in matches:
                    # 在上下文附近查找数字
                    start = max(0, match.start() - 50)
                    end = min(len(paper_text), match.end() + 50)
                    surrounding = paper_text[start:end]
                    numbers_in_text = re.findall(r"[\d]+\.?\d*", surrounding)
                    for num_str in numbers_in_text:
                        try:
                            num_val = float(num_str)
                            if abs(num_val - float(value)) > 0.01 * abs(float(value)):
                                inconsistencies.append({
                                    "type": "frozen_mismatch",
                                    "expected": value,
                                    "found": num_str,
                                    "context": context,
                                    "position": paper_text.find(num_str, match.start()),
                                })
                        except ValueError:
                            pass

    # 从结果文件中查找
    for key, value in results.items():
        if isinstance(value, (int, float)):
            # 在论文中搜索该值
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            if value_str in paper_text:
                continue  # 一致
            # 搜索近似值
            pattern = rf"\b{int(value)}\b" if isinstance(value, int) else rf"\b{value:.2f}\b"
            if not re.search(pattern, paper_text):
                # 可能是论文中写错了
                inconsistencies.append({
                    "type": "result_mismatch",
                    "expected": value,
                    "found": None,
                    "context": key,
                    "position": None,
                })

    return inconsistencies


def parse_consistency_errors(errors: list) -> list:
    """解析一致性审计的错误信息"""
    inconsistencies = []
    for error in errors:
        if isinstance(error, str):
            # 格式: "Q1 feed_in_ratio: 论文=33.3, 代码=6.741293367448395, 偏差=394.0%"
            match = re.search(r"(Q\d+)\s+(\w+):\s*论文=([\d.]+),\s*代码=([\d.]+)", error)
            if match:
                inconsistencies.append({
                    "type": "consistency_mismatch",
                    "question": match.group(1),
                    "param": match.group(2),
                    "found": match.group(3),
                    "expected": match.group(4),
                    "context": match.group(2),  # 用参数名作为上下文
                })
    return inconsistencies


def fix_paper_numbers(paper_text: str, inconsistencies: list) -> tuple:
    """修正论文中的数字，返回 (fixed_text, fixed_count)"""
    fixed_count = 0

    for item in inconsistencies:
        expected = item.get("expected")
        found = item.get("found")

        if expected is None or found is None:
            continue

        # 转换为数字
        try:
            expected_num = float(expected)
            found_num = float(found)
        except ValueError:
            continue

        # 格式化期望值（保留合理精度）
        if expected_num == int(expected_num):
            expected_str = str(int(expected_num))
        else:
            expected_str = f"{expected_num:.2f}".rstrip('0').rstrip('.')

        # 在论文中搜索并替换
        # 搜索格式：found_num 或 found_num%
        found_patterns = [
            re.escape(found),
            re.escape(found) + r"%",
        ]

        for pattern in found_patterns:
            matches = list(re.finditer(pattern, paper_text))
            for match in matches:
                pos = match.start()
                # 检查上下文是否匹配参数名
                context_start = max(0, pos - 100)
                context_end = min(len(paper_text), pos + 100)
                context = paper_text[context_start:context_end]

                # 如果上下文中有参数名，或者直接替换
                if item.get("param", "") in context or item.get("type") == "consistency_mismatch":
                    old_text = paper_text
                    paper_text = paper_text[:pos] + expected_str + paper_text[pos + len(found):]

                    # 如果原来是百分比格式，保持
                    if "%" in old_text[pos:pos + len(found) + 5] and "%" not in expected_str:
                        paper_text = paper_text[:pos + len(expected_str)] + "%" + paper_text[pos + len(expected_str):]

                    if paper_text != old_text:
                        fixed_count += 1
                        print(f"    [>] 论文修正: {found} -> {expected_str} (参数: {item.get('param', 'unknown')})")
                    break  # 每个不一致只修正一次

    return paper_text, fixed_count


def fix_from_consistency_report(paper_text: str, errors: list) -> tuple:
    """从一致性审计报告修正论文数字"""
    inconsistencies = parse_consistency_errors(errors)
    if not inconsistencies:
        return paper_text, 0
    return fix_paper_numbers(paper_text, inconsistencies)

    print(f"    共修正 {fixed_count} 处数字")
    return paper_text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="数字自动修正器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    parser.add_argument("--fix-all", action="store_true", help="修正所有不一致")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"[!] 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")
    frozen = load_frozen_numbers()
    results = load_result_numbers()

    total_fixed = 0

    # 1. 从一致性审计错误中修正（论文数字 → 代码结果）
    if args.errors:
        error_data = json.loads(Path(args.errors).read_text(encoding="utf-8"))
        errors = error_data.get("errors", [])
        consistency_errors = [e for e in errors if isinstance(e, str) and "论文=" in e and "代码=" in e]
        if consistency_errors:
            print(f"[*] 从一致性审计修正 ({len(consistency_errors)} 项)")
            paper_text, fixed = fix_from_consistency_report(paper_text, consistency_errors)
            total_fixed += fixed

    # 2. 从冻结数字中修正
    inconsistencies = find_number_inconsistencies(paper_text, frozen, results)
    if inconsistencies:
        print(f"[*] 从冻结数字修正 ({len(inconsistencies)} 项)")
        paper_text, fixed = fix_paper_numbers(paper_text, inconsistencies)
        total_fixed += fixed

    if total_fixed > 0:
        paper_path.write_text(paper_text, encoding="utf-8")
        print(f"[OK] 已修正 {total_fixed} 处数字")
    else:
        print("[OK] 数字一致性检查通过，无需修正")

    sys.exit(0 if total_fixed > 0 else 1)


if __name__ == "__main__":
    main()