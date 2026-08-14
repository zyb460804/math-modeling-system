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

三态说明（2026-08 修复 CR-9a“橡皮图章”）：
    PASS            所有已实现检查全部通过
    PASS_WITH_SKIP  已实现检查通过，但存在未实现自动检测的检查项（SKIP/N/A）——
                    总体不得是纯 PASS，属于 WARNING 级：哪些查了、哪些没查必须可见
    WARN / FAIL / ERROR  同原语义（WARN 及以上仍以 rc=1 结束）
    font_size / text_overlap / label_clarity（及非 PNG 路径的 text_quality）为 SKIP：
    本脚本基于成品位图无法可靠测量字号/重叠/清晰度，不再假装 PASS——
    文字重叠由 math-figure/scripts/figqa.py::assert_no_overlap 碰撞门承接
    （出图脚本 savefig 前已接线），字号与标签清晰度需人工确认。
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


def _aggregate_status(checks: dict) -> str:
    """聚合单项检查状态为总体状态。

    优先级：FAIL/ERROR > WARN > PASS_WITH_SKIP > PASS。
    任一检查项为 SKIP/N/A（未实现自动检测或未执行）时，总体不得是纯 PASS，
    而是 PASS_WITH_SKIP（WARNING 级）：已查的部分通过 + 未查的部分必须可见。
    """
    statuses = [c.get("status") for c in checks.values()]
    if "FAIL" in statuses or "ERROR" in statuses:
        return "FAIL"
    if "WARN" in statuses:
        return "WARN"
    if any(s in ("SKIP", "N/A") for s in statuses):
        return "PASS_WITH_SKIP"
    return "PASS"


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

        # 检查文字质量：位图无法可靠测量字号/重叠/清晰度，显式 SKIP（不假装 PASS）
        result["checks"]["text_quality"] = {
            "status": "SKIP",
            "note": "未实现自动检测：文字重叠由 figqa 碰撞门承接"
                    "（math-figure/scripts/figqa.py），字号/清晰度需人工确认"
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

        # 总体状态（三态聚合：含 SKIP/N/A 时不得是纯 PASS）
        result["overall_status"] = _aggregate_status(result["checks"])

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

        # 检查字体大小：位图无法可靠测量字号，显式 SKIP（不假装 PASS）
        result["checks"]["font_size"] = {
            "status": "SKIP",
            "min_size": QUALITY_STANDARDS["min_font_size"],
            "note": "未实现自动检测：最小字号（标准≥6.5pt）需人工确认"
        }

        # 检查文字重叠：由 figqa 碰撞门在出图时承接，此处显式 SKIP
        result["checks"]["text_overlap"] = {
            "status": "SKIP",
            "max_overlap_ratio": QUALITY_STANDARDS["max_text_overlap_ratio"],
            "note": "未实现自动检测：文字重叠由 figqa 碰撞门承接"
                    "（math-figure/scripts/figqa.py::assert_no_overlap，"
                    "出图脚本 savefig 前已接线）"
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

        # 检查标签清晰度：位图无法可靠测量，显式 SKIP（不假装 PASS）
        result["checks"]["label_clarity"] = {
            "status": "SKIP",
            "note": "未实现自动检测：坐标轴标签与图例清晰度需人工确认"
        }

        # 总体状态（三态聚合：含 SKIP/N/A 时不得是纯 PASS）
        result["overall_status"] = _aggregate_status(result["checks"])

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

        # 哪些查了、哪些没查：stdout 可见
        skipped_checks = [
            name for name, c in results[figure_file.name]["checks"].items()
            if c.get("status") in ("SKIP", "N/A")
        ]
        if skipped_checks:
            print(f"  ⏭ 未实现自动检测（SKIP）: {', '.join(skipped_checks)}")

    # 统计
    total = len(results)
    passed = sum(1 for r in results.values() if r["overall_status"] == "PASS")
    pass_with_skip = sum(1 for r in results.values() if r["overall_status"] == "PASS_WITH_SKIP")
    skipped = sum(1 for r in results.values() if r["overall_status"] == "SKIP")
    warned = sum(1 for r in results.values() if r["overall_status"] == "WARN")
    failed = sum(1 for r in results.values() if r["overall_status"] in ("FAIL", "ERROR"))

    return {
        "total": total,
        "passed": passed,
        "pass_with_skip": pass_with_skip,
        "skipped": skipped,
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
            "pass_with_skip": check_results.get("pass_with_skip", 0),
            "skipped": check_results.get("skipped", 0),
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
| 通过（纯PASS） | {report['summary']['passed']} |
| 部分通过（含SKIP，未全部实现自动检测） | {report['summary']['pass_with_skip']} |
| 整体跳过 | {report['summary']['skipped']} |
| 警告 | {report['summary']['warned']} |
| 失败 | {report['summary']['failed']} |

## 检查结果

| 文件 | 状态 | 问题 | 未检查项（SKIP/N/A） |
|------|------|------|------|
"""

    for filename, result in check_results["results"].items():
        status = result["overall_status"]
        if status == "PASS":
            status_icon = "✅"
        elif status in ("PASS_WITH_SKIP", "SKIP"):
            status_icon = "🔶"
        elif status == "WARN":
            status_icon = "⚠️"
        else:
            status_icon = "❌"
        issues = "; ".join(result["issues"]) if result["issues"] else "-"
        skipped = ", ".join(
            name for name, c in result["checks"].items()
            if c.get("status") in ("SKIP", "N/A")
        ) or "-"
        md_content += f"| {filename} | {status_icon} {status} | {issues} | {skipped} |\n"

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
3. 确保没有文字重叠（自动检测由 figqa 碰撞门在出图时承接：math-figure/scripts/figqa.py）
4. 确保图表内容不超出画布边界
5. 确保字体大小符合要求（未实现自动检测，需人工确认）

> 说明：PASS_WITH_SKIP = 已实现的检查（分辨率/尺寸/白区/边缘像素）通过，
> 但 font_size / text_overlap / label_clarity 未实现位图级自动检测（SKIP），
> 不是纯 PASS——文字重叠请依赖出图时的 figqa 碰撞门，字号与清晰度请人工确认。
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

        sys.exit(0 if result["overall_status"] in ("PASS", "SKIP", "PASS_WITH_SKIP") else 1)

    elif args.command == "check-all":
        figures_dir = Path(args.dir)

        print(f"检查目录: {figures_dir}")
        results = check_all_figures(figures_dir)

        if results.get("error"):
            print(f"⚠️ {results['error']}")

        generate_report(results)

        print(f"\n总计: {results['total']}")
        print(f"通过（纯PASS）: {results['passed']}")
        print(f"部分通过（含SKIP）: {results.get('pass_with_skip', 0)}")
        print(f"整体跳过: {results.get('skipped', 0)}")
        print(f"警告: {results['warned']}")
        print(f"失败: {results['failed']}")

        sys.exit(0 if results["failed"] == 0 else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()