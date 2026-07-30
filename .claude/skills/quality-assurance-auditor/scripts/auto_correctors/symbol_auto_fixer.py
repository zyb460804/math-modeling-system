#!/usr/bin/env python3
"""
符号表自动修复器
检测符号重复/不一致 → 自动解决冲突

用法:
    python symbol_auto_fixer.py --errors path/to/errors.json
    python symbol_auto_fixer.py --paper paper_output/final_paper_source.md
    python symbol_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[5]
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"
SYMBOL_TABLE = ROOT / "paper_output" / "plan" / "symbol_table.md"


def extract_symbols(paper_text: str) -> dict:
    """提取论文中的数学符号"""
    symbols = {}

    # 1. 提取 LaTeX 数学符号
    # 行内公式中的符号
    inline_formulas = re.findall(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", paper_text)
    for formula in inline_formulas:
        # 提取单字母变量（排除常见命令）
        vars_in_formula = re.findall(r"(?<![a-zA-Z\\])([a-zA-Z])(?![a-zA-Z])", formula)
        for var in vars_in_formula:
            if var not in ("d", "e", "i", "n", "x", "y", "z"):  # 排除常用符号
                symbols[var] = symbols.get(var, 0) + 1

    # 2. 提取定义的符号（如 "其中，x 表示..."）
    definitions = re.findall(r"其中[，,]\s*(?:，|，)?\s*([a-zA-Z])\s*(?:为|表示|是|代表)", paper_text)
    for defn in definitions:
        symbols[defn] = symbols.get(defn, 0) + 1

    # 3. 提取希腊字母
    greek = re.findall(r"\\(alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega)", paper_text)
    for g in greek:
        symbols[f"\\{g}"] = symbols.get(f"\\{g}", 0) + 1

    return symbols


def find_symbol_conflicts(paper_text: str) -> list:
    """查找符号冲突"""
    conflicts = []

    # 1. 查找同一符号在不同上下文中表示不同含义
    # 检查 "x" 是否在多处被定义
    x_definitions = re.findall(r"([a-zA-Z])\s*(?:为|表示|是|代表)\s*(.{2,20}?)(?:[，,。.；;])", paper_text)
    symbol_defs = {}
    for sym, meaning in x_definitions:
        if sym in symbol_defs:
            if meaning.strip() != symbol_defs[sym].strip():
                conflicts.append({
                    "type": "multiple_definitions",
                    "symbol": sym,
                    "definitions": [symbol_defs[sym], meaning.strip()],
                    "description": f"符号 '{sym}' 有多个不同定义",
                })
        else:
            symbol_defs[sym] = meaning.strip()

    # 2. 查找未定义就使用的符号
    used_symbols = extract_symbols(paper_text)
    defined_symbols = set(sym for sym, _ in x_definitions)

    # 排除常见符号
    common_symbols = {"x", "y", "z", "t", "n", "i", "j", "k", "a", "b", "c", "d", "e", "f", "g", "h", "p", "q", "r", "s", "m", "u", "v", "w"}
    undefined = set(used_symbols.keys()) - defined_symbols - common_symbols

    if undefined:
        conflicts.append({
            "type": "undefined_symbols",
            "symbols": list(undefined)[:10],
            "description": f"以下符号可能未定义: {list(undefined)[:10]}",
        })

    # 3. 查找符号表文件中的冲突
    if SYMBOL_TABLE.exists():
        table_text = SYMBOL_TABLE.read_text(encoding="utf-8")
        table_symbols = re.findall(r"\|\s*([a-zA-Z\\]+)\s*\|", table_text)
        table_counts = Counter(table_symbols)
        duplicates = {k: v for k, v in table_counts.items() if v > 1}
        if duplicates:
            conflicts.append({
                "type": "table_duplicates",
                "duplicates": duplicates,
                "description": f"符号表中有重复定义: {duplicates}",
            })

    return conflicts


def fix_symbol_conflicts(paper_text: str, conflicts: list) -> tuple:
    """修正符号冲突"""
    fixed_count = 0

    for conflict in conflicts:
        if conflict["type"] == "multiple_definitions":
            # 为不同定义添加下标区分
            sym = conflict["symbol"]
            for i, defn in enumerate(conflict["definitions"]):
                old_pattern = f"{sym} 为{defn}"
                new_pattern = f"{sym}_{i+1} 为{defn}"
                if old_pattern in paper_text:
                    paper_text = paper_text.replace(old_pattern, new_pattern, 1)
                    fixed_count += 1
                    print(f"    [>] 符号 '{sym}' 添加下标: {sym}_{i+1}")

        elif conflict["type"] == "undefined_symbols":
            # 提示但不自动修正
            print(f"    [!] 未定义符号需人工补充: {conflict['symbols'][:5]}")

        elif conflict["type"] == "table_duplicates":
            # 提示但不自动修正
            print(f"    [!] 符号表重复需人工处理: {list(conflict['duplicates'].keys())[:5]}")

    return paper_text, fixed_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description="符号表自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    parser.add_argument("--fix-all", action="store_true", help="修复所有符号冲突")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"[!] 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")

    print("[*] 符号表一致性检查")

    # 提取符号
    symbols = extract_symbols(paper_text)
    print(f"    发现符号: {len(symbols)} 个")

    # 查找冲突
    conflicts = find_symbol_conflicts(paper_text)

    if not conflicts:
        print("[OK] 符号检查通过")
        sys.exit(0)

    print(f"\n[!] 发现 {len(conflicts)} 个符号冲突:")
    for conflict in conflicts:
        print(f"    - {conflict['description']}")

    if args.fix_all or args.errors:
        print(f"\n[#] 自动修正...")
        fixed_text, fixed_count = fix_symbol_conflicts(paper_text, conflicts)

        if fixed_count > 0:
            paper_path.write_text(fixed_text, encoding="utf-8")
            print(f"\n[OK] 已修正 {fixed_count} 个符号冲突")
        else:
            print(f"\n[!] 无法自动修正，需人工处理")
            sys.exit(1)
    else:
        print("\n使用 --fix-all 自动修正")
        sys.exit(1)


if __name__ == "__main__":
    main()
