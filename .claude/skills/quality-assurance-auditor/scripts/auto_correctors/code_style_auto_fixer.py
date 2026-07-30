#!/usr/bin/env python3
"""
代码风格自动修复器
检测 PEP8/格式问题 → 自动格式化

用法:
    python code_style_auto_fixer.py --errors path/to/errors.json
    python code_style_auto_fixer.py --file paper_output/code/modeling/q1_model.py
    python code_style_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CODE_DIR = ROOT / "paper_output" / "code"


def fix_code_style(code: str) -> tuple:
    """修正代码风格问题"""
    fixes = []
    lines = code.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        original = line

        # 1. 移除行尾空格
        line = line.rstrip()

        # 2. 修正缩进（确保使用4空格）
        if line and not line.startswith("#"):
            # 将 tab 替换为 4 空格
            line = line.replace("\t", "    ")

        # 3. 修正运算符周围空格
        # 赋值运算符
        line = re.sub(r"(\w)\s*=\s*(\w)", r"\1 = \2", line)
        # 比较运算符
        line = re.sub(r"(\w)\s*==\s*(\w)", r"\1 == \2", line)
        line = re.sub(r"(\w)\s*!=\s*(\w)", r"\1 != \2", line)
        line = re.sub(r"(\w)\s*>=\s*(\w)", r"\1 >= \2", line)
        line = re.sub(r"(\w)\s*<=\s*(\w)", r"\1 <= \2", line)
        # 但不要修改 f-string 和注释中的内容
        if 'f"' not in line and "f'" not in line and "#" not in line:
            # 算术运算符
            line = re.sub(r"(\w)\s*\+\s*(\w)", r"\1 + \2", line)
            line = re.sub(r"(\w)\s*-\s*(\w)", r"\1 - \2", line)
            line = re.sub(r"(\w)\s*\*\s*(\w)", r"\1 * \2", line)

        # 4. 修正逗号后空格
        line = re.sub(r",(\S)", r", \1", line)

        # 5. 修正冒号后空格（字典/切片）
        line = re.sub(r":(\S)", r": \1", line)

        # 6. 修正括号内空格
        # 不要修改函数调用中的括号

        # 7. 修正注释格式
        if "#" in line:
            code_part, comment_part = line.split("#", 1)
            # 确保 # 前有空格
            if code_part and not code_part.endswith(" "):
                line = code_part + " #" + comment_part
            # 确保 # 后有空格
            if comment_part and not comment_part.startswith(" "):
                line = code_part + " #" + comment_part.lstrip()

        if line != original:
            fixes.append(i + 1)

        fixed_lines.append(line)

    # 8. 移除文件末尾多余空行
    while fixed_lines and fixed_lines[-1] == "":
        fixed_lines.pop()

    # 9. 确保文件以空行结尾
    fixed_lines.append("")

    return "\n".join(fixed_lines), fixes


def fix_imports(code: str) -> tuple:
    """修正导入语句"""
    fixes = []
    lines = code.split("\n")

    # 分离导入语句和其他代码
    imports = []
    other_lines = []
    in_imports = True

    for line in lines:
        stripped = line.strip()
        if in_imports and (stripped.startswith("import ") or stripped.startswith("from ")):
            imports.append(stripped)
        else:
            if in_imports and stripped:
                in_imports = False
            other_lines.append(line)

    if not imports:
        return code, fixes

    # 按类型分组
    stdlib_imports = []
    third_party_imports = []
    local_imports = []

    stdlib_modules = {
        "os", "sys", "json", "re", "math", "random", "datetime", "pathlib",
        "collections", "itertools", "functools", "typing", "abc", "copy",
        "argparse", "subprocess", "threading", "multiprocessing", "io",
    }

    for imp in imports:
        module = imp.split()[1].split(".")[0]
        if module in stdlib_modules:
            stdlib_imports.append(imp)
        elif imp.startswith("from .") or imp.startswith("import ."):
            local_imports.append(imp)
        else:
            third_party_imports.append(imp)

    # 排序
    stdlib_imports.sort()
    third_party_imports.sort()
    local_imports.sort()

    # 重新组合
    sorted_imports = []
    if stdlib_imports:
        sorted_imports.extend(stdlib_imports)
        sorted_imports.append("")
    if third_party_imports:
        sorted_imports.extend(third_party_imports)
        sorted_imports.append("")
    if local_imports:
        sorted_imports.extend(local_imports)
        sorted_imports.append("")

    new_code = "\n".join(sorted_imports) + "\n" + "\n".join(other_lines)

    if new_code != code:
        fixes.append("imports_sorted")

    return new_code, fixes


def fix_code_file(file_path: Path) -> bool:
    """修复单个代码文件"""
    if not file_path.exists():
        print(f"    [!] 文件不存在: {file_path}")
        return False

    code = file_path.read_text(encoding="utf-8")
    original_code = code

    # 修正风格
    code, style_fixes = fix_code_style(code)

    # 修正导入
    code, import_fixes = fix_imports(code)

    total_fixes = len(style_fixes) + len(import_fixes)

    if total_fixes > 0:
        file_path.write_text(code, encoding="utf-8")
        print(f"    [OK] {file_path.name}: {len(style_fixes)} 行风格修正, {len(import_fixes)} 处导入修正")
        return True
    else:
        print(f"    [OK] {file_path.name}: 无需修正")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="代码风格自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--file", help="直接指定要修复的代码文件")
    parser.add_argument("--fix-all", action="store_true", help="修复所有代码文件")
    args = parser.parse_args()

    if args.file:
        file_path = Path(args.file)
        success = fix_code_file(file_path)
        sys.exit(0 if success else 1)

    elif args.errors or args.fix_all:
        code_files = list(CODE_DIR.rglob("*.py"))
        if not code_files:
            print("[!] 未找到代码文件")
            sys.exit(1)

        print(f"[*] 代码风格检查 ({len(code_files)} 个文件)")
        success_count = 0
        for code_file in code_files:
            if fix_code_file(code_file):
                success_count += 1

        print(f"\n[=] 修正结果: {success_count}/{len(code_files)} 个文件")
        sys.exit(0 if success_count > 0 else 1)

    else:
        print("请指定 --file, --errors 或 --fix-all")
        sys.exit(1)


if __name__ == "__main__":
    main()
