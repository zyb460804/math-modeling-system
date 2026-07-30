#!/usr/bin/env python3
"""
参数自动修复器
题目为准：代码参数 ≠ 题目要求 → 自动修正代码

用法:
    python parameter_auto_fixer.py --errors path/to/errors.json
    python parameter_auto_fixer.py --check-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CODE_DIR = ROOT / "paper_output" / "code"
QA_DIR = ROOT / "paper_output" / "qa"
REPORT_JSON = QA_DIR / "parameter_consistency_report.json"


def load_parameter_report() -> dict:
    """加载参数一致性检查报告"""
    if REPORT_JSON.exists():
        return json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    return {"issues": []}


def fix_code_parameter(code_file: Path, param_name: str, expected_value: float, actual_value: float) -> bool:
    """修正代码中的参数值"""
    if not code_file.exists():
        return False

    code = code_file.read_text(encoding="utf-8")
    original_code = code

    # 构建匹配模式：PARAM_NAME = actual_value
    # 支持整数和浮点数
    actual_str = str(actual_value)
    expected_str = str(expected_value)

    # 如果是整数，也尝试匹配不带小数点的形式
    if actual_value == int(actual_value):
        actual_str = rf"(?:{actual_value}|{int(actual_value)}(?:\.0)?)"
    else:
        actual_str = re.escape(str(actual_value))

    # 替换模式
    pattern = rf"({re.escape(param_name)}\s*=\s*){actual_str}"
    replacement = rf"\g<1>{expected_str}"

    new_code = re.sub(pattern, replacement, code)

    if new_code != original_code:
        code_file.write_text(new_code, encoding="utf-8")
        print(f"    [OK] {code_file.name}: {param_name} = {actual_value} -> {expected_value}")
        return True

    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="参数自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--check-all", action="store_true", help="检查并修复所有参数不一致")
    args = parser.parse_args()

    print("[*] 参数一致性修复")

    # 加载报告
    report = load_parameter_report()
    issues = report.get("issues", [])

    if not issues:
        # 尝试从错误文件加载
        if args.errors:
            error_data = json.loads(Path(args.errors).read_text(encoding="utf-8"))
            issues = error_data.get("errors", [])

    if not issues:
        print("[OK] 未发现参数不一致")
        sys.exit(0)

    print(f"[!] 发现 {len(issues)} 个参数不一致")

    # 查找代码文件
    code_files = list(CODE_DIR.rglob("*.py"))
    if not code_files:
        print("[!] 未找到代码文件")
        sys.exit(1)

    # 解析不一致并修正
    fixed_count = 0
    for issue in issues:
        if isinstance(issue, str):
            # 解析错误信息
            # 格式: "Q1: P_ALKEL 代码=20.0, 题目=10.0, 偏差=100.0%"
            match = re.search(r"(Q\d+):\s*(\w+)\s*代码=([\d.]+),\s*题目=([\d.]+)", issue)
            if match:
                question = match.group(1)
                param_name = match.group(2)
                actual_value = float(match.group(3))
                expected_value = float(match.group(4))

                # 查找对应的代码文件
                for code_file in code_files:
                    if question.lower() in code_file.stem.lower() or "q" + question[1:] in code_file.stem.lower():
                        if fix_code_parameter(code_file, param_name, expected_value, actual_value):
                            fixed_count += 1
                            break

        elif isinstance(issue, dict):
            # 结构化错误
            question = issue.get("question", "")
            param_name = issue.get("param", "")
            actual_value = issue.get("actual")
            expected_value = issue.get("expected")

            if actual_value is not None and expected_value is not None:
                for code_file in code_files:
                    if question.lower() in code_file.stem.lower():
                        if fix_code_parameter(code_file, param_name, float(expected_value), float(actual_value)):
                            fixed_count += 1
                            break

    print(f"\n[=] 修正结果: {fixed_count}/{len(issues)} 个参数")
    sys.exit(0 if fixed_count > 0 else 1)


if __name__ == "__main__":
    main()
