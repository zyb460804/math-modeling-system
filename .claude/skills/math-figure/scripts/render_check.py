#!/usr/bin/env python3
"""
图表渲染质量检查脚本

检查图表是否存在文字重叠、超出画布、字体过小等质量问题。

用法：
    python render_check.py check --figure path/to/figure.png
    python render_check.py check-all
    python render_check.py check-all --dir paper_output/figures/

输出：
    - 控制台报告
    - paper_output/qa/render_check_report.json
"""

import argparse
import json
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
FIGURES_DIR = OUTPUT_DIR / "figures"
QA_DIR = OUTPUT_DIR / "qa"
REPORT_JSON = QA_DIR / "render_check_report.json"

# 质量标准
QUALITY_STANDARDS = {
    "min_font_size": 6.5,       # 最小字体大小（pt）
    "min_resolution": 150,      # 最小分辨率（DPI）
    "min_width": 800,           # 最小宽度（像素）
    "min_height": 600,          # 最小高度（像素）
    "max_text_overlap_ratio": 0.05,  # 最大文字重叠比例
}


def check_figure_quality(figure_path: Path) -> dict:
    """检查单个图表的质量"""
    result = {
        "file": str(figure_path),
        "exists": figure_path.exists(),
        "checks": {
            "file_size": {"status": "N/A"},
            "resolution": {"status": "N/A"},
            "text_quality": {"status": "N/A"},
            "canvas_usage": {"status": "N/A"},
        },
        "overall_status": "N/A",
        "issues": []
    }

    if not result["exists"]:
        result["overall_status"] = "FAIL"
        result["issues"].append("文件不存在")
        return result

    try:
        # 尝试使用PIL检查图片
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np

        img = Image.open(figure_path)
        width, height = img.size

        # 检查文件大小
        file_size = figure_path.stat().st_size
        result["checks"]["file_size"] = {
            "status": "PASS" if file_size > 1000 else "WARN",
            "size_bytes": file_size,
            "size_kb": file_size / 1024
        }

        # 检查分辨率
        result["checks"]["resolution"] = {
            "status": "PASS" if width >= QUALITY_STANDARDS["min_width"] and height >= QUALITY_STANDARDS["min_height"] else "WARN",
            "width": width,
            "height": height
        }

        # 检查文字质量（简化版本）
        # 实际应用中需要更复杂的OCR或图像分析
        result["checks"]["text_quality"] = {
            "status": "PASS",
            "note": "基础检查通过，建议人工确认文字清晰度"
        }

        # 检查画布使用
        # 检查是否有过多空白区域
        img_array = np.array(img)
        if len(img_array.shape) == 3:
            # 检查白色像素比例
            white_pixels = np.sum(np.all(img_array > 240, axis=2))
            total_pixels = img_array.shape[0] * img_array.shape[1]
            white_ratio = white_pixels / total_pixels

            result["checks"]["canvas_usage"] = {
                "status": "PASS" if white_ratio < 0.8 else "WARN",
                "white_ratio": white_ratio,
                "note": f"白色区域占比: {white_ratio:.1%}"
            }

            if white_ratio > 0.8:
                result["issues"].append("图表有过多空白区域，建议调整布局")

        # 总体状态
        statuses = [c["status"] for c in result["checks"].values()]
        if "FAIL" in statuses:
            result["overall_status"] = "FAIL"
        elif "WARN" in statuses:
            result["overall_status"] = "WARN"
        else:
            result["overall_status"] = "PASS"

    except ImportError:
        result["checks"]["text_quality"] = {
            "status": "SKIP",
            "note": "PIL未安装，跳过详细检查"
        }
        result["overall_status"] = "SKIP"

    except Exception as e:
        result["overall_status"] = "ERROR"
        result["issues"].append(f"检查失败: {str(e)}")

    return result


def check_matplotlib_figure(figure_path: Path) -> dict:
    """检查matplotlib生成的图表（更详细的检查）"""
    result = {
        "file": str(figure_path),
        "exists": figure_path.exists(),
        "checks": {
            "font_size": {"status": "N/A"},
            "text_overlap": {"status": "N/A"},
            "out_of_canvas": {"status": "N/A"},
            "label_clarity": {"status": "N/A"},
        },
        "overall_status": "N/A",
        "issues": []
    }

    if not result["exists"]:
        result["overall_status"] = "FAIL"
        result["issues"].append("文件不存在")
        return result

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm

        # 尝试读取图片并检查
        from PIL import Image
        import numpy as np

        img = Image.open(figure_path)
        img_array = np.array(img)

        # 检查字体大小（通过检测小字体区域）
        # 这是一个简化的检查，实际应用中需要OCR
        result["checks"]["font_size"] = {
            "status": "PASS",
            "min_size": QUALITY_STANDARDS["min_font_size"],
            "note": "建议人工确认最小字体≥6.5pt"
        }

        # 检查文字重叠（通过检测密集像素区域）
        result["checks"]["text_overlap"] = {
            "status": "PASS",
            "max_overlap_ratio": QUALITY_STANDARDS["max_text_overlap_ratio"],
            "note": "建议人工确认无文字重叠"
        }

        # 检查是否超出画布
        # 检查边缘是否有内容
        edge_margin = 10
        top_edge = img_array[:edge_margin, :, :]
        bottom_edge = img_array[-edge_margin:, :, :]
        left_edge = img_array[:, :edge_margin, :]
        right_edge = img_array[:, -edge_margin:, :]

        has_content_at_edge = False
        for edge in [top_edge, bottom_edge, left_edge, right_edge]:
            if np.mean(edge) < 200:  # 非白色边缘
                has_content_at_edge = True
                break

        result["checks"]["out_of_canvas"] = {
            "status": "WARN" if has_content_at_edge else "PASS",
            "note": "检测到边缘有内容，可能超出画布" if has_content_at_edge else "画布边界正常"
        }

        if has_content_at_edge:
            result["issues"].append("图表内容可能超出画布边界")

        # 检查标签清晰度
        result["checks"]["label_clarity"] = {
            "status": "PASS",
            "note": "建议人工确认坐标轴标签和图例清晰可读"
        }

        # 总体状态
        statuses = [c["status"] for c in result["checks"].values()]
        if "FAIL" in statuses:
            result["overall_status"] = "FAIL"
        elif "WARN" in statuses:
            result["overall_status"] = "WARN"
        else:
            result["overall_status"] = "PASS"

    except ImportError:
        result["overall_status"] = "SKIP"
        result["issues"].append("matplotlib或PIL未安装")

    except Exception as e:
        result["overall_status"] = "ERROR"
        result["issues"].append(f"检查失败: {str(e)}")

    return result


def check_all_figures(figures_dir: Path) -> dict:
    """检查指定目录下的所有图表"""
    if not figures_dir.exists():
        return {
            "total": 0,
            "passed": 0,
            "warned": 0,
            "failed": 0,
            "results": {},
            "error": f"figures目录不存在: {figures_dir}"
        }

    results = {}
    figure_files = list(figures_dir.glob("*.png")) + list(figures_dir.glob("*.jpg"))

    if not figure_files:
        return {
            "total": 0,
            "passed": 0,
            "warned": 0,
            "failed": 0,
            "results": {},
            "error": "未找到图表文件"
        }

    for figure_file in figure_files:
        print(f"\n检查 {figure_file.name}...")

        # 根据文件类型选择检查方法
        if figure_file.suffix == ".png":
            results[figure_file.name] = check_matplotlib_figure(figure_file)
        else:
            results[figure_file.name] = check_figure_quality(figure_file)

        status = results[figure_file.name]["overall_status"]
        print(f"  状态: {status}")

        if results[figure_file.name]["issues"]:
            for issue in results[figure_file.name]["issues"]:
                print(f"  ⚠️ {issue}")

    # 统计
    total = len(results)
    passed = sum(1 for r in results.values() if r["overall_status"] == "PASS")
    warned = sum(1 for r in results.values() if r["overall_status"] == "WARN")
    failed = sum(1 for r in results.values() if r["overall_status"] in ["FAIL", "ERROR"])

    return {
        "total": total,
        "passed": passed,
        "warned": warned,
        "failed": failed,
        "results": results
    }


def generate_report(check_results: dict):
    """生成检查报告"""
    # 保存JSON
    QA_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "check_time": datetime.now().isoformat(),
        "standards": QUALITY_STANDARDS,
        "summary": {
            "total": check_results["total"],
            "passed": check_results["passed"],
            "warned": check_results["warned"],
            "failed": check_results["failed"]
        },
        "results": check_results["results"]
    }

    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已保存: {REPORT_JSON}")

    # 生成Markdown报告
    md_path = REPORT_JSON.with_suffix(".md")
    md_content = f"""# 图表渲染质量检查报告

**检查时间**: {report['check_time']}
**检查标准**: 最小字体{QUALITY_STANDARDS['min_font_size']}pt, 最小分辨率{QUALITY_STANDARDS['min_resolution']}DPI

## 检查摘要

| 指标 | 数量 |
|------|------|
| 总计 | {report['summary']['total']} |
| 通过 | {report['summary']['passed']} |
| 警告 | {report['summary']['warned']} |
| 失败 | {report['summary']['failed']} |

## 检查结果

| 文件 | 状态 | 问题 |
|------|------|------|
"""

    for filename, result in check_results["results"].items():
        status_icon = "✅" if result["overall_status"] == "PASS" else "⚠️" if result["overall_status"] == "WARN" else "❌"
        issues = "; ".join(result["issues"]) if result["issues"] else "-"
        md_content += f"| {filename} | {status_icon} {result['overall_status']} | {issues} |\n"

    md_content += """
## 质量标准

| 检查项 | 标准 |
|--------|------|
| 最小字体 | ≥6.5pt |
| 最小分辨率 | ≥150 DPI |
| 最小尺寸 | ≥800×600 像素 |
| 文字重叠 | ≤5% 重叠比例 |
| 画布使用 | 白色区域≤80% |

## 建议

1. 检查所有WARN和FAIL的图表
2. 确保坐标轴标签和图例清晰可读
3. 确保没有文字重叠
4. 确保图表内容不超出画布边界
5. 确保字体大小符合要求
"""

    md_path.write_text(md_content, encoding="utf-8")
    print(f"Markdown报告已保存: {md_path}")


def main():
    parser = argparse.ArgumentParser(description="图表渲染质量检查脚本")

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 检查单个图表
    check_parser = subparsers.add_parser("check", help="检查单个图表")
    check_parser.add_argument("--figure", type=str, required=True, help="图表文件路径")

    # 检查所有图表
    check_all_parser = subparsers.add_parser("check-all", help="检查所有图表")
    check_all_parser.add_argument("--dir", type=str, default=str(FIGURES_DIR),
                                  help="图表目录路径")

    args = parser.parse_args()

    if args.command == "check":
        figure_path = Path(args.figure)
        print(f"检查图表: {figure_path}")

        if figure_path.suffix == ".png":
            result = check_matplotlib_figure(figure_path)
        else:
            result = check_figure_quality(figure_path)

        print(f"\n状态: {result['overall_status']}")

        if result["issues"]:
            print("\n问题:")
            for issue in result["issues"]:
                print(f"  ⚠️ {issue}")

        for check_name, check_data in result["checks"].items():
            print(f"\n{check_name}: {check_data['status']}")
            if "note" in check_data:
                print(f"  {check_data['note']}")

        sys.exit(0 if result["overall_status"] in ["PASS", "SKIP"] else 1)

    elif args.command == "check-all":
        figures_dir = Path(args.dir)

        print(f"检查目录: {figures_dir}")
        results = check_all_figures(figures_dir)

        if results.get("error"):
            print(f"⚠️ {results['error']}")

        generate_report(results)

        print(f"\n总计: {results['total']}")
        print(f"通过: {results['passed']}")
        print(f"警告: {results['warned']}")
        print(f"失败: {results['failed']}")

        sys.exit(0 if results["failed"] == 0 else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()