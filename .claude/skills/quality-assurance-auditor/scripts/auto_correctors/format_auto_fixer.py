#!/usr/bin/env python3
"""
格式自动修正器
检测论文格式问题 → 自动修正 → 重检

用法:
    python format_auto_fixer.py --errors path/to/errors.json
    python format_auto_fixer.py --paper paper_output/final_paper_source.md
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"


def check_and_fix_format(paper_text: str) -> tuple:
    """检查并修正格式问题，返回 (fixed_text, issues)"""
    issues = []
    fixed = paper_text

    # 1. 检查字数
    cn_chars = len(re.findall(r"[一-鿿]", fixed))
    en_words = len(re.findall(r"[a-zA-Z]+", fixed))
    total = cn_chars + en_words
    if total < 18000:
        issues.append(f"字数不足: {total} 字（要求 ≥18000）")

    # 2. 检查三级标题结构
    h1 = re.findall(r"^# .+", fixed, re.MULTILINE)
    h2 = re.findall(r"^## .+", fixed, re.MULTILINE)
    h3 = re.findall(r"^### .+", fixed, re.MULTILINE)
    if len(h3) < 3:
        issues.append(f"三级标题不足: {len(h3)} 个（要求 ≥3）")

    # 3. 检查图表引用
    fig_refs = re.findall(r"图\s*\d+", fixed)
    table_refs = re.findall(r"表\s*\d+", fixed)
    if not fig_refs and not table_refs:
        issues.append("未发现图表引用（图X/表X）")

    # 4. 修正常见格式问题

    # 4.1 修正多余空行（超过2个连续空行 → 2个）
    fixed = re.sub(r"\n{4,}", "\n\n\n", fixed)

    # 4.2 修正标题前后空行
    fixed = re.sub(r"\n\n\n(#+ )", r"\n\n\1", fixed)
    fixed = re.sub(r"(#+ .+)\n\n\n", r"\1\n\n", fixed)

    # 4.3 修正中英文标点混用
    # 英文逗号后无空格 → 添加空格
    fixed = re.sub(r",([^\s\d])", r", \1", fixed)
    # 中文句号后无空格（在中文语境中）
    fixed = re.sub(r"。([^\n\s])", r"。\1", fixed)

    # 4.4 修正公式格式
    # 独立公式应该前后有空行
    fixed = re.sub(r"([^\n])\n(\$\$)", r"\1\n\n\2", fixed)
    fixed = re.sub(r"(\$\$)\n([^\n])", r"\1\n\n\2", fixed)

    # 4.5 修正表格格式
    # Markdown 表格前后应有空行
    fixed = re.sub(r"([^\n])\n(\|)", r"\1\n\n\2", fixed)
    fixed = re.sub(r"(\|[^\n]+)\n([^\n|])", r"\1\n\n\2", fixed)

    # 4.6 修正引用格式
    # [1] 前应有空格
    fixed = re.sub(r"([^\s])\[([0-9]+)\]", r"\1 [\2]", fixed)

    # 4.7 修正图片引用格式
    # 图 1 → 图1（国赛规范）
    fixed = re.sub(r"图\s+(\d+)", r"图\1", fixed)
    fixed = re.sub(r"表\s+(\d+)", r"表\1", fixed)

    # 4.8 修正摘要格式
    # 摘要应以"摘要："开头
    if "摘要" in fixed and "摘要：" not in fixed and "摘要:" not in fixed:
        fixed = fixed.replace("# 摘要\n", "# 摘要\n\n摘要：", 1)

    return fixed, issues


def main():
    import argparse

    parser = argparse.ArgumentParser(description="格式自动修正器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")

    print("[*] 格式检查与修正")
    fixed_text, issues = check_and_fix_format(paper_text)

    # 保存修正后的文件
    if fixed_text != paper_text:
        paper_path.write_text(fixed_text, encoding="utf-8")
        print(f"[OK] 格式已修正: {paper_path}")

    if issues:
        print(f"\n[!] 发现 {len(issues)} 个格式问题:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("[OK] 格式检查通过")
        sys.exit(0)


if __name__ == "__main__":
    main()