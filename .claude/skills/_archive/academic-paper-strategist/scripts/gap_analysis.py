# -*- coding: utf-8 -*-
"""当前论文 vs 样例基线的差距分析脚本（academic-paper-strategist）。

输入：
- --paper     当前论文（.md/.txt）
- --baseline  evaluate_samples.py 输出的评价 JSON（取其 median 作基线）

对字数/章节结构/图表公式密度/参考文献数逐维度对比样例中位数，
输出差距分析报告（控制台 + 可选 JSON）：低于中位数的维度 + 改进建议。

注意：研究空白（research gap）的证据充分性（每个 gap ≥3 条引用等）
属于语义判断，由 agent 依据 references/quality_standards.md 评估；
本脚本只负责可离线计量的结构性差距。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_samples import analyze_paper, heuristic_score  # noqa: E402

# (维度键, 中文名, 低于基线时的建议)
DIMENSIONS = [
    ("word_count", "字数",
     "正文篇幅低于样例中位数，优先扩充主体章节的论证与结果分析。"),
    ("section_count", "二级章节数",
     "章节划分少于样例惯例，考虑将长章节拆分或补齐方法/讨论等标准章节。"),
    ("heading_max_depth", "标题层级深度",
     "层级偏浅，样例普遍使用三级标题组织论证，建议细化小节结构。"),
    ("figure_density", "图表密度(每千字)",
     "图表少于样例水平，为关键结果/流程补充图或表以增强证据展示。"),
    ("formula_density", "公式密度(每千字)",
     "公式化表达少于样例水平，将核心模型/定义用公式显式给出。"),
    ("reference_count", "参考文献数",
     "参考文献少于样例中位数，补充关键文献（对照 Literature_Review_Report）。"),
]


def load_baseline(path):
    """读取 evaluate_samples.py 生成的基线 JSON，返回 median 字典。"""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"错误：无法读取基线文件 {path}：{exc}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"错误：基线文件不是合法 JSON：{path}（{exc}）")
    median = data.get("median")
    if not isinstance(median, dict):
        raise SystemExit(
            "错误：基线 JSON 缺少 median 字段，"
            "请先用 evaluate_samples.py 生成基线。")
    return data, median


def compare(metrics, median):
    """逐维度对比，返回 (对比列表, 低于基线的维度列表)。"""
    rows, gaps = [], []
    for key, label, advice in DIMENSIONS:
        base = median.get(key)
        if base is None:
            continue
        value = metrics.get(key, 0)
        ratio = round(value / base, 2) if base else None
        below = value < base
        row = {
            "dimension": key, "label": label,
            "paper": value, "baseline_median": base,
            "ratio": ratio, "below_median": below,
        }
        if below:
            row["advice"] = advice
            gaps.append(row)
        rows.append(row)

    if median.get("has_abstract") and not metrics.get("has_abstract"):
        row = {
            "dimension": "has_abstract", "label": "摘要",
            "paper": False, "baseline_median": True,
            "ratio": None, "below_median": True,
            "advice": "样例论文普遍含摘要，当前论文缺失，需补写摘要。",
        }
        rows.append(row)
        gaps.append(row)
    return rows, gaps


def print_report(report):
    print(f"\n差距分析：{report['paper']}")
    print(f"基线：{report['baseline']}（{report.get('baseline_papers', '?')} 篇样例中位数）")
    print("-" * 78)
    print(f"{'维度':<14}{'当前':>10}{'样例中位':>10}{'比值':>8}  结论")
    print("-" * 78)
    for r in report["comparison"]:
        paper_v = "有" if r["paper"] is True else ("无" if r["paper"] is False else r["paper"])
        base_v = "有" if r["baseline_median"] is True else (
            "无" if r["baseline_median"] is False else r["baseline_median"])
        ratio = "-" if r["ratio"] is None else r["ratio"]
        verdict = "低于中位数" if r["below_median"] else "达标"
        print(f"{r['label']:<14}{paper_v!s:>10}{base_v!s:>10}{ratio!s:>8}  {verdict}")
    print("-" * 78)

    gaps = report["gaps"]
    if not gaps:
        print("结论：所有可计量维度均不低于样例中位数。")
    else:
        print(f"结论：{len(gaps)} 个维度低于样例中位数，建议：")
        for i, g in enumerate(gaps, 1):
            print(f"  {i}. [{g['label']}] {g['advice']}")
    print(f"\n启发式分：当前论文 {report['paper_score']} / 样例中位 "
          f"{report.get('baseline_median_score', '-')}")


def main():
    parser = argparse.ArgumentParser(
        description="差距分析：将当前论文与样例评价基线（evaluate_samples.py 的"
                    "输出 JSON）逐维度对比，报告低于样例中位数的维度并给出建议。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--paper", required=True,
                        help="当前论文文件（.md/.txt）")
    parser.add_argument("--baseline", required=True,
                        help="样例评价基线 JSON（evaluate_samples.py 的输出）")
    parser.add_argument("--output", default=None,
                        help="差距分析报告 JSON 输出路径（默认只打印到控制台）")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.is_file():
        print(f"错误：论文文件不存在：{paper_path}", file=sys.stderr)
        return 2

    baseline_data, median = load_baseline(args.baseline)
    try:
        metrics = analyze_paper(paper_path)
    except OSError as exc:
        print(f"错误：读取论文失败 {paper_path}：{exc}", file=sys.stderr)
        return 2

    rows, gaps = compare(metrics, median)
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper": str(paper_path),
        "baseline": str(args.baseline),
        "baseline_papers": baseline_data.get("paper_count"),
        "paper_metrics": metrics,
        "paper_score": heuristic_score(metrics),
        "baseline_median_score": baseline_data.get("median_score"),
        "comparison": rows,
        "gaps": gaps,
        "note": "仅覆盖可离线计量维度；研究空白证据充分性由 agent 依据 "
                "references/quality_standards.md 评估。",
    }

    print_report(report)

    if args.output:
        output = Path(args.output)
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding="utf-8")
        except OSError as exc:
            print(f"错误：无法写入输出文件 {output}：{exc}", file=sys.stderr)
            return 2
        print(f"JSON 报告已写入：{output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
