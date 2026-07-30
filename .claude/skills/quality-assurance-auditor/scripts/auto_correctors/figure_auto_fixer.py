#!/usr/bin/env python3
"""
图表质量自动修复器
render_check.py 检测到 DPI<150 / 字体<6.5pt / 重叠>5% → 自动调整参数重新渲染

用法:
    python figure_auto_fixer.py --errors path/to/errors.json
    python figure_auto_fixer.py --figure paper_output/figures/xxx.png
    python figure_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FIGURES_DIR = ROOT / "paper_output" / "figures"
QA_DIR = ROOT / "paper_output" / "qa"
REPORT_JSON = QA_DIR / "render_check_report.json"

# 质量标准
STANDARDS = {
    "min_font_size": 6.5,
    "min_resolution": 150,
    "min_width": 800,
    "min_height": 600,
    "max_text_overlap_ratio": 0.05,
}


def load_render_report() -> dict:
    """加载渲染检查报告"""
    if REPORT_JSON.exists():
        return json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    return {"figures": []}


def find_figure_source(figure_path: Path) -> Path:
    """查找图表的源代码文件"""
    # 常见源代码位置
    code_dir = ROOT / "paper_output" / "code" / "visualization"
    if code_dir.exists():
        # 根据图表文件名猜测源代码
        stem = figure_path.stem
        # 尝试匹配: q1_xxx.py, plot_xxx.py, xxx_viz.py
        for pattern in [f"*{stem}*.py", f"*{stem[:5]}*.py", "q*.py", "plot_*.py"]:
            matches = list(code_dir.glob(pattern))
            if matches:
                return matches[0]

    # 查找 math-figure 生成脚本
    math_fig_dir = ROOT / ".claude" / "skills" / "math-figure" / "scripts"
    if math_fig_dir.exists():
        for script in math_fig_dir.glob("*.py"):
            if script.name not in ("__init__.py", "render_check.py"):
                return script

    return None


def fix_figure_params(figure_path: Path, issues: list) -> bool:
    """修正图表参数并重新渲染"""
    source = find_figure_source(figure_path)
    if not source or not source.exists():
        print(f"    [!] 找不到源代码: {figure_path.name}")
        return False

    code = source.read_text(encoding="utf-8")
    original_code = code

    for issue in issues:
        issue_lower = issue.lower()

        # 修复 DPI 过低
        if "dpi" in issue_lower or "resolution" in issue_lower:
            # 替换 DPI 参数
            code = re.sub(
                r"dpi\s*=\s*\d+",
                "dpi=200",
                code,
            )
            def _replace_dpi(m):
                old = m.group(0)
                match = re.search(r'dpi=(\d+)', old)
                if match:
                    return old.replace("dpi=" + match.group(1), "dpi=200")
                return old
            code = re.sub(
                r"savefig\([^)]*dpi\s*=\s*\d+",
                _replace_dpi,
                code,
            )
            print("    [>] DPI -> 200")

        # 修复字体过小
        if "font" in issue_lower or "fontsize" in issue_lower:
            # 增大字体
            code = re.sub(
                r"fontsize\s*=\s*(\d+)",
                lambda m: f"fontsize={max(int(m.group(1)), 10)}",
                code,
            )
            code = re.sub(
                r"font_size\s*=\s*(\d+)",
                lambda m: f"font_size={max(int(m.group(1)), 10)}",
                code,
            )
            # 设置全局字体大小
            if "plt.rcParams" not in code and "rcParams" not in code:
                import_line = "import matplotlib.pyplot as plt\n"
                rc_line = 'plt.rcParams["font.size"] = 12\nplt.rcParams["axes.titlesize"] = 14\nplt.rcParams["axes.labelsize"] = 12\n'
                code = code.replace(import_line, import_line + rc_line)
            print(f"    [>] font_size -> >=10")

        # 修复画布过小
        if "width" in issue_lower or "height" in issue_lower or "size" in issue_lower:
            code = re.sub(
                r"figsize\s*=\s*\(([^)]+)\)",
                lambda m: f"figsize=({max(float(m.group(1).split(',')[0]), 10)}, {max(float(m.group(1).split(',')[1].strip()), 7)})",
                code,
            )
            print(f"    [>] figsize -> >=(10,7)")

        # 修复文字重叠
        if "overlap" in issue_lower:
            # 添加 tight_layout
            if "tight_layout" not in code:
                code = code.replace("plt.show()", "plt.tight_layout()\nplt.show()")
                code = code.replace("plt.savefig(", "plt.tight_layout()\nplt.savefig(")
            # 增加子图间距
            code = re.sub(
                r"subplots\(figsize=([^)]+)\)",
                r"subplots(figsize=\1)",
                code,
            )
            print(f"    [>] tight_layout added")

    # 写回源代码
    if code != original_code:
        source.write_text(code, encoding="utf-8")
        print(f"    [OK] 源代码已修正: {source.name}")

        # 尝试重新运行渲染
        try:
            import subprocess
            result = subprocess.run(
                ["python", str(source)],
                capture_output=True,
                timeout=60,
                cwd=str(ROOT),
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                print(f"    [OK] 重新渲染成功: {figure_path.name}")
                return True
            else:
                print(f"    [!] 重新渲染失败")
                return False
        except Exception as e:
            print(f"    [!] 渲染异常: {e}")
            return False

    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="图表质量自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--figure", help="直接指定要修复的图表文件")
    parser.add_argument("--fix-all", action="store_true", help="修复所有不达标图表")
    args = parser.parse_args()

    report = load_render_report()
    figures = report.get("figures", [])

    if args.figure:
        # 修复单个图表
        fig_path = Path(args.figure)
        issues = [f.get("issues", []) for f in figures if f.get("file") == str(fig_path)]
        issues = issues[0] if issues else ["manual fix"]
        success = fix_figure_params(fig_path, issues)
        sys.exit(0 if success else 1)

    elif args.errors or args.fix_all:
        # 从报告中提取不达标的图表
        failed_figures = []
        for fig in figures:
            if fig.get("overall_status") in ("FAIL", "WARN"):
                failed_figures.append({
                    "path": Path(fig["file"]),
                    "issues": fig.get("issues", []),
                })

        if not failed_figures:
            print("[OK] 所有图表质量达标")
            sys.exit(0)

        print(f"[!] {len(failed_figures)} 个图表不达标")
        success_count = 0
        for fig in failed_figures:
            print(f"  修复: {fig['path'].name}")
            if fix_figure_params(fig["path"], fig["issues"]):
                success_count += 1

        print(f"\n[=] 修复结果: {success_count}/{len(failed_figures)}")
        sys.exit(0 if success_count > 0 else 1)

    else:
        print("请指定 --figure, --errors 或 --fix-all")
        sys.exit(1)


if __name__ == "__main__":
    main()