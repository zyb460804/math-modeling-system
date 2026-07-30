#!/usr/bin/env python3
"""
代码自动修复器
检测代码运行错误 → 分析错误类型 → 自动修正 → 返回修正后的代码

用法:
    python code_auto_fixer.py --errors path/to/errors.json
    python code_auto_fixer.py --file paper_output/code/modeling/q1_model.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CODE_DIR = ROOT / "paper_output" / "code"

# 常见错误模式 → 修复策略
ERROR_PATTERNS = [
    {
        "pattern": r"ModuleNotFoundError: No module named '(\w+)'",
        "fix_type": "import",
        "description": "缺少模块导入",
    },
    {
        "pattern": r"NameError: name '(\w+)' is not defined",
        "fix_type": "undefined_var",
        "description": "变量未定义",
    },
    {
        "pattern": r"FileNotFoundError.*No such file.*['\"](.+?)['\"]",
        "fix_type": "file_path",
        "description": "文件路径错误",
    },
    {
        "pattern": r"KeyError: '(.+?)'",
        "fix_type": "key_error",
        "description": "字典键不存在",
    },
    {
        "pattern": r"IndexError: list index out of range",
        "fix_type": "index_error",
        "description": "列表索引越界",
    },
    {
        "pattern": r"TypeError.*missing \d+ required positional argument",
        "fix_type": "arg_error",
        "description": "函数参数缺失",
    },
    {
        "pattern": r"ValueError.*could not convert string to float",
        "fix_type": "type_convert",
        "description": "类型转换失败",
    },
    {
        "pattern": r"UnicodeDecodeError",
        "fix_type": "encoding",
        "description": "编码错误",
    },
    {
        "pattern": r"PermissionError",
        "fix_type": "permission",
        "description": "权限错误",
    },
    {
        "pattern": r"ZeroDivisionError",
        "fix_type": "division_zero",
        "description": "除零错误",
    },
]


def analyze_error(error_text: str) -> list:
    """分析错误文本，返回匹配的错误类型"""
    matches = []
    for pattern_info in ERROR_PATTERNS:
        if re.search(pattern_info["pattern"], error_text, re.IGNORECASE):
            matches.append(pattern_info)
    return matches


def fix_import_error(code: str, error_text: str) -> str:
    """修复缺少模块导入"""
    match = re.search(r"ModuleNotFoundError: No module named '(\w+)'", error_text)
    if not match:
        return code
    module = match.group(1)

    # 常见模块映射
    module_map = {
        "sklearn": "scikit-learn",
        "cv2": "opencv-python",
        "PIL": "Pillow",
        "np": "numpy",
        "pd": "pandas",
        "plt": "matplotlib",
        "sns": "seaborn",
        "scipy": "scipy",
        "torch": "torch",
        "tensorflow": "tensorflow",
        "keras": "keras",
        "xgboost": "xgboost",
        "lightgbm": "lightgbm",
        "pgmpy": "pgmpy",
        "pywt": "PyWavelets",
        "SALib": "SALib",
    }

    # 检查是否已在导入语句中
    if f"import {module}" in code or f"from {module}" in code:
        return code

    # 添加导入语句
    import_line = f"import {module}"
    if module in ["np", "pd", "plt", "sns"]:
        alias_map = {"np": "numpy", "pd": "pandas", "plt": "matplotlib", "sns": "seaborn"}
        import_line = f"import {alias_map[module]} as {module}"

    # 在文件头部添加
    lines = code.split("\n")
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            insert_pos = i + 1
    lines.insert(insert_pos, import_line)
    return "\n".join(lines)


def fix_file_path(code: str, error_text: str) -> str:
    """修复文件路径错误"""
    match = re.search(r"FileNotFoundError.*No such file.*['\"](.+?)['\"]", error_text)
    if not match:
        return code
    bad_path = match.group(1)

    # 替换硬编码路径为相对路径或参数化
    # 常见模式: D:\xxx, C:\xxx, /home/xxx
    code = re.sub(
        r"""['\"]([A-Z]:\\\\[^'\"]+|/home/[^'\"]+)['\"]""",
        '# TODO: 替换为正确的数据文件路径\n    "data.csv"',
        code,
    )
    return code


def fix_encoding(code: str, error_text: str) -> str:
    """修复编码错误"""
    # 在文件读取处添加 encoding 参数
    code = code.replace("open(", "open(")
    # 替换常见的无编码读取
    code = re.sub(
        r"open\(([^)]+)\)",
        r"open(\1, encoding='utf-8')",
        code,
    )
    # 修复已有 encoding 的重复添加
    code = code.replace("encoding='utf-8', encoding='utf-8'", "encoding='utf-8'")
    return code


def fix_division_zero(code: str, error_text: str) -> str:
    """修复除零错误"""
    # 在除法操作前添加安全检查
    # 查找可能的除法操作
    lines = code.split("\n")
    fixed_lines = []
    for line in lines:
        if "/" in line and "=" in line and "import" not in line and "#" not in line.split("=")[0]:
            # 添加安全除法
            if "np.divide" not in line and "safe_div" not in line:
                line = line.replace("/", "/ (1e-10 + ", 1)  # 简单安全除法
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def fix_code_file(file_path: Path, errors: list) -> bool:
    """修复单个代码文件"""
    if not file_path.exists():
        print(f"    文件不存在: {file_path}")
        return False

    code = file_path.read_text(encoding="utf-8")
    original_code = code
    error_text = "\n".join(errors)

    # 分析错误类型
    matches = analyze_error(error_text)

    for match in matches:
        fix_type = match["fix_type"]
        print(f"    修复类型: {match['description']}")

        if fix_type == "import":
            code = fix_import_error(code, error_text)
        elif fix_type == "file_path":
            code = fix_file_path(code, error_text)
        elif fix_type == "encoding":
            code = fix_encoding(code, error_text)
        elif fix_type == "division_zero":
            code = fix_division_zero(code, error_text)

    # 写回文件
    if code != original_code:
        file_path.write_text(code, encoding="utf-8")
        print(f"    [OK] 已修复: {file_path.name}")
        return True
    else:
        print(f"    [!] 无法自动修复: {file_path.name}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="代码自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--file", help="直接指定要修复的代码文件")
    args = parser.parse_args()

    if args.file:
        file_path = Path(args.file)
        errors = ["手动指定修复"]
        success = fix_code_file(file_path, errors)
    elif args.errors:
        error_data = json.loads(Path(args.errors).read_text(encoding="utf-8"))
        errors = error_data.get("errors", [])
        stage = error_data.get("stage", "code")

        # 查找需要修复的代码文件
        code_files = list(CODE_DIR.rglob("*.py"))
        if not code_files:
            print("未找到代码文件")
            sys.exit(1)

        success = False
        for code_file in code_files:
            # 检查错误是否与该文件相关
            if any(code_file.name in err or str(code_file.stem) in err for err in errors):
                if fix_code_file(code_file, errors):
                    success = True

        if not success:
            # 尝试修复所有代码文件
            for code_file in code_files:
                if fix_code_file(code_file, errors):
                    success = True
    else:
        print("请指定 --errors 或 --file")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()