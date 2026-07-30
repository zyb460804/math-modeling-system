#!/usr/bin/env python3
"""
引用自动修复器
检测断链引用、格式错误 → 自动修正引用格式

用法:
    python citation_auto_fixer.py --errors path/to/errors.json
    python citation_auto_fixer.py --paper paper_output/final_paper_source.md
    python citation_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"
REFS_DIR = ROOT / "paper_output" / "references"


def find_citation_issues(paper_text: str) -> list:
    """查找引用问题"""
    issues = []

    # 1. 查找 [数字] 格式的引用
    citations = re.findall(r"\[(\d+)\]", paper_text)
    citation_nums = sorted(set(int(c) for c in citations))

    # 2. 检查引用是否连续（跳号）
    if citation_nums:
        expected = list(range(1, max(citation_nums) + 1))
        missing = set(expected) - set(citation_nums)
        if missing:
            issues.append({
                "type": "missing_citation",
                "description": f"引用跳号: 缺少 {sorted(missing)}",
                "missing": sorted(missing),
            })

    # 3. 检查重复引用编号
    from collections import Counter
    citation_counts = Counter(int(c) for c in citations)
    duplicates = {k: v for k, v in citation_counts.items() if v > 1}
    if duplicates:
        issues.append({
            "type": "duplicate_citation",
            "description": f"重复引用编号: {duplicates}",
            "duplicates": duplicates,
        })

    # 4. 检查引用格式（中英文混用）
    # 国赛格式: [1] 作者. 标题[文献类型]. 出版信息, 年份.
    # 美赛格式: [1] Author. Title. Publisher, Year.
    cn_refs = re.findall(r"\[[\d]+\]\s*[一-鿿]", paper_text)
    en_refs = re.findall(r"\[[\d]+\]\s*[A-Z]", paper_text)
    if cn_refs and en_refs:
        issues.append({
            "type": "mixed_format",
            "description": f"中英文引用格式混用: {len(cn_refs)} 中文, {len(en_refs)} 英文",
        })

    # 5. 检查正文中的引用是否在参考文献列表中出现
    ref_section = re.findall(r"#+\s*(?:参考文献|References|Bibliography)(.*?)(?:#|\Z)", paper_text, re.DOTALL)
    if ref_section:
        ref_list = ref_section[0]
        ref_nums_in_list = set(int(m) for m in re.findall(r"\[(\d+)\]", ref_list))
        ref_nums_in_text = set(int(m) for m in citations)
        orphaned = ref_nums_in_text - ref_nums_in_list
        if orphaned:
            issues.append({
                "type": "orphaned_citation",
                "description": f"正文引用但参考文献列表中缺失: {sorted(orphaned)}",
                "orphaned": sorted(orphaned),
            })

    # 6. 检查空引用
    empty_refs = re.findall(r"\[\s*\]", paper_text)
    if empty_refs:
        issues.append({
            "type": "empty_citation",
            "description": f"空引用: {len(empty_refs)} 处",
        })

    return issues


def fix_citations(paper_text: str, issues: list) -> tuple:
    """修正引用问题"""
    fixed_count = 0

    for issue in issues:
        if issue["type"] == "missing_citation":
            # 重新编号引用（跳号修复）
            citations = re.findall(r"\[(\d+)\]", paper_text)
            old_nums = sorted(set(int(c) for c in citations))
            new_nums = list(range(1, len(old_nums) + 1))
            num_map = dict(zip(old_nums, new_nums))

            def replace_citation(m):
                old_num = int(m.group(1))
                new_num = num_map.get(old_num, old_num)
                return f"[{new_num}]"

            paper_text = re.sub(r"\[(\d+)\]", replace_citation, paper_text)
            fixed_count += 1
            print(f"    [>] 重新编号引用: {len(old_nums)} 个")

        elif issue["type"] == "empty_citation":
            # 移除空引用
            paper_text = re.sub(r"\[\s*\]", "", paper_text)
            fixed_count += 1
            print(f"    [>] 移除空引用")

        elif issue["type"] == "mixed_format":
            # 提示但不自动修正（需要人工判断用哪种格式）
            print(f"    [!] 中英文引用混用，需人工确认格式")

        elif issue["type"] == "orphaned_citation":
            # 提示但不自动修正（需要补充参考文献）
            print(f"    [!] 正文引用缺失参考文献条目，需人工补充")

    return paper_text, fixed_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description="引用自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    parser.add_argument("--fix-all", action="store_true", help="修复所有引用问题")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"[!] 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")

    print("[*] 引用一致性检查")

    # 统计引用
    citations = re.findall(r"\[(\d+)\]", paper_text)
    print(f"    引用总数: {len(citations)}")
    print(f"    引用编号: {len(set(citations))} 个唯一编号")

    # 查找问题
    issues = find_citation_issues(paper_text)

    if not issues:
        print("[OK] 引用检查通过")
        sys.exit(0)

    print(f"\n[!] 发现 {len(issues)} 个引用问题:")
    for issue in issues:
        print(f"    - {issue['description']}")

    if args.fix_all or args.errors:
        fixed_text, fixed_count = fix_citations(paper_text, issues)
        if fixed_count > 0:
            paper_path.write_text(fixed_text, encoding="utf-8")
            print(f"\n[OK] 已修正 {fixed_count} 类引用问题")
        else:
            print(f"\n[!] 无法自动修正，需人工处理")
            sys.exit(1)
    else:
        print("\n使用 --fix-all 自动修正")
        sys.exit(1)


if __name__ == "__main__":
    main()
