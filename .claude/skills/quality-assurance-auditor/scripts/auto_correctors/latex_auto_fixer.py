#!/usr/bin/env python3
"""
LaTeX 公式自动修复器
render_formulas.py 检测到语法错误 → 自动修正常见 LaTeX 错误

用法:
    python latex_auto_fixer.py --errors path/to/errors.json
    python latex_auto_fixer.py --paper paper_output/final_paper_source.md
    python latex_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

from _project_root import ProjectRootNotFoundError, find_project_root

# M-13（未收口 #9）锚定统一：parents[5] 硬编码层级 → 文件位置上溯定位项目根。
# 旧形态病灶：脚本被复制到其它深度（沙箱）时 parents[5] 会指向沙箱外或
# 真实树，造成"空沙箱却扫到/写到真实树"；新形态找不到项目根时启动即报错退出。
try:
    ROOT = find_project_root()
except ProjectRootNotFoundError as exc:
    print(f"[ANCHOR FAILED] {exc}", file=sys.stderr)
    raise SystemExit(2)
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"
FORMULA_INDEX = ROOT / "paper_output" / "tables" / "formula_index.json"

# 常见 LaTeX 错误模式 → 修复策略
LATEX_FIXES = [
    {
        "name": "未闭合的大括号",
        "pattern": r"\{[^}]*$",
        "fix": lambda m: m.group(0) + "}",
        "scope": "formula",
    },
    {
        "name": "未闭合的括号",
        "pattern": r"\\left\([^)]*$",
        "fix": lambda m: m.group(0) + "\\right)",
        "scope": "formula",
    },
    {
        "name": "未转义的下划线",
        "pattern": r"(?<!\\)_\{",
        "fix": lambda m: "\\_{" if "_" in m.group(0) else m.group(0),
        "scope": "formula",
    },
    {
        "name": "双反斜杠缺失",
        "pattern": r"\\\\begin\{[^}]+\}[^$]*[^\\]\\$",
        "fix": lambda m: m.group(0),
        "scope": "formula",
    },
    {
        "name": "空公式",
        "pattern": r"\$\$\s*\$\$",
        "fix": lambda m: "",
        "scope": "inline",
    },
    {
        "name": "嵌套数学模式",
        "pattern": r"\$\$.*?\$.*?\$\$",
        "fix": lambda m: m.group(0).replace("$", ""),
        "scope": "formula",
    },
]


def fix_latex_formula(latex: str) -> tuple:
    """修正单个 LaTeX 公式，返回 (fixed_latex, fixes_applied)"""
    fixes_applied = []
    fixed = latex

    # 1. 修复未闭合的大括号
    open_braces = fixed.count("{") - fixed.count("}")
    if open_braces > 0:
        fixed += "}" * open_braces
        fixes_applied.append(f"补全 {open_braces} 个大括号")

    # 2. 修复未闭合的 \left( ... \right)
    left_count = len(re.findall(r"\\left\s*[\(\[\{]", fixed))
    right_count = len(re.findall(r"\\right\s*[\)\]\}]", fixed))
    if left_count > right_count:
        # 推断右括号类型
        last_left = re.findall(r"\\left\s*([\(\[\{])", fixed)
        if last_left:
            bracket_map = {"(": ")", "[": "]", "{": "}"}
            missing = left_count - right_count
            fixed += "\\right" + bracket_map.get(last_left[-1], ")") * missing
            fixes_applied.append(f"补全 {missing} 个 \\right 括号")

    # 3. 修复常见的命令拼写错误
    typo_fixes = [
        ("\\\\alhpa", "\\\\alpha"),
        ("\\\\belta", "\\\\beta"),
        ("\\\\gama", "\\\\gamma"),
        ("\\\\lamda", "\\\\lambda"),
    ]
    for typo, correct in typo_fixes:
        if re.search(typo, fixed, re.IGNORECASE):
            fixed = re.sub(typo, correct, fixed, flags=re.IGNORECASE)
            fixes_applied.append(f"修正命令拼写")

    # 4. 修复 \frac 缺少参数
    fixed = re.sub(r"\\frac\s*(?!\{)", "\\frac{", fixed, count=1)
    if "\\frac{" in fixed and fixed.count("\\frac{") > fixed.count("}{"):
        # 可能缺少第二个参数
        pass

    # 5. 修复空格问题
    # 数字和字母之间需要空格
    fixed = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", fixed)
    # 但不要在命令中添加空格
    fixed = re.sub(r"(\\[a-zA-Z]+)\s+(\{)", r"\1\2", fixed)

    # 6. 修复常见的环境缺失
    if "\\begin{" in fixed and "\\end{" not in fixed:
        env_match = re.search(r"\\begin\{(\w+)\}", fixed)
        if env_match:
            env = env_match.group(1)
            fixed += f"\\end{{{env}}}"
            fixes_applied.append(f"补全 \\end{{{env}}}")

    return fixed, fixes_applied


def fix_paper_formulas(paper_text: str) -> tuple:
    """修正论文中的所有公式，返回 (fixed_text, total_fixes)"""
    total_fixes = 0

    # 提取并修正行间公式
    def fix_display(match):
        nonlocal total_fixes
        formula = match.group(1).strip()
        fixed, fixes = fix_latex_formula(formula)
        if fixes:
            total_fixes += len(fixes)
            print(f"    [>] 公式修正: {fixes}")
        return f"$$\n{fixed}\n$$"

    paper_text = re.sub(r"\$\$(.*?)\$\$", fix_display, paper_text, flags=re.DOTALL)

    # 提取并修正行内公式
    def fix_inline(match):
        nonlocal total_fixes
        formula = match.group(1).strip()
        fixed, fixes = fix_latex_formula(formula)
        if fixes:
            total_fixes += len(fixes)
        return f"${fixed}$"

    paper_text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", fix_inline, paper_text)

    return paper_text, total_fixes


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LaTeX 公式自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    parser.add_argument("--fix-all", action="store_true", help="修复所有公式")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"[!] 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")

    # 统计公式数量
    display_formulas = len(re.findall(r"\$\$.*?\$\$", paper_text, re.DOTALL))
    inline_formulas = len(re.findall(r"(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)", paper_text))
    print(f"[*] LaTeX 公式检查")
    print(f"    行间公式: {display_formulas}")
    print(f"    行内公式: {inline_formulas}")

    # 修正公式
    fixed_text, total_fixes = fix_paper_formulas(paper_text)

    if total_fixes > 0:
        paper_path.write_text(fixed_text, encoding="utf-8")
        print(f"[OK] 已修正 {total_fixes} 处公式问题")
    else:
        print("[OK] 公式检查通过，无需修正")

    sys.exit(0)


if __name__ == "__main__":
    main()