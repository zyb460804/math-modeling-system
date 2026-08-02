# -*- coding: utf-8 -*-
"""样例论文离线质量评价脚本（academic-paper-strategist）。

对样例论文目录中的每篇论文（.md/.txt）统计可离线计量的质量信号：
- 字数（中文字符 + 英文单词）
- 章节结构（标题数量、层级深度、是否含摘要）
- 图表/公式密度（每千字）
- 参考文献数量

输出排序评价表（控制台 + JSON）。JSON 中的 median 字段可作为
gap_analysis.py 的基线输入。

注意：相关性评分、时间分布、作者多样性等依赖检索元数据的维度
无法离线计量，由 agent 在检索阶段人工评估（见 SKILL.md）。
"""

import argparse
import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt"}

# 用于排序的启发式打分权重（满分 100，仅供相对排序参考）
SCORE_TARGETS = {
    "word_count": (8000, 30),        # 达到 8000 字得满 30 分
    "section_count": (6, 15),        # 6 个二级章节得满 15 分
    "reference_count": (30, 25),     # 30 条参考文献得满 25 分
    "figure_density": (2.0, 10),     # 每千字 2 图得满 10 分
    "formula_density": (3.0, 10),    # 每千字 3 式得满 10 分
}
ABSTRACT_BONUS = 10                  # 含摘要加 10 分

REF_HEADING_RE = re.compile(
    r"^\s{0,3}(#{1,6}\s*)?(references?|bibliography|参考文献|引用文献)\s*$",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
FIGURE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)|<img\b", re.IGNORECASE)
FIGURE_CAPTION_RE = re.compile(r"^\s*(图|表|Figure|Fig\.?|Table)\s*\d", re.IGNORECASE)
ENV_FORMULA_RE = re.compile(r"\\begin\{(equation|align|gather|eqnarray|multline)\*?\}")
BLOCK_FORMULA_RE = re.compile(r"\$\$.+?\$\$", re.DOTALL)
INLINE_FORMULA_RE = re.compile(r"(?<!\$)\$(?!\$)[^$\n]+?\$(?!\$)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
REF_ENTRY_RE = re.compile(r"^\s*(\[\d+\]|\d+[.、)]|[-*+]\s|\[[A-Za-z])")


def read_text(path):
    """读取文本文件，优先 UTF-8，失败时回退 GBK。"""
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def count_words(text):
    """字数 = 中文字符数 + 英文单词数。"""
    return len(CJK_RE.findall(text)) + len(LATIN_WORD_RE.findall(text))


def count_references(lines):
    """定位参考文献章节并统计条目数；无该章节时回退统计 [n] 引用标记。"""
    ref_start = None
    for i, line in enumerate(lines):
        if REF_HEADING_RE.match(line.strip()):
            ref_start = i + 1
    if ref_start is None:
        markers = set(re.findall(r"\[(\d{1,3})\]", "\n".join(lines)))
        return len(markers)
    count = 0
    for line in lines[ref_start:]:
        stripped = line.strip()
        if not stripped:
            continue
        if HEADING_RE.match(stripped):
            break
        if REF_ENTRY_RE.match(stripped) or len(stripped) >= 20:
            count += 1
    return count


def analyze_paper(path):
    """对单篇论文计算全部离线指标，返回 dict。"""
    text = read_text(path)
    lines = text.splitlines()

    word_count = count_words(text)
    per_kilo = (word_count / 1000.0) if word_count > 0 else 1.0

    headings = [m for m in (HEADING_RE.match(l) for l in lines) if m]
    heading_count = len(headings)
    heading_max_depth = max((len(m.group(1)) for m in headings), default=0)
    section_count = sum(1 for m in headings if len(m.group(1)) == 2)

    lowered = text.lower()
    has_abstract = ("摘要" in text) or ("abstract" in lowered)

    figure_count = len(FIGURE_RE.findall(text)) + sum(
        1 for l in lines if FIGURE_CAPTION_RE.match(l)
    )
    text_no_block = BLOCK_FORMULA_RE.sub(" ", text)
    formula_count = (
        len(BLOCK_FORMULA_RE.findall(text))
        + len(ENV_FORMULA_RE.findall(text))
        + len(INLINE_FORMULA_RE.findall(text_no_block))
    )
    reference_count = count_references(lines)

    return {
        "word_count": word_count,
        "heading_count": heading_count,
        "heading_max_depth": heading_max_depth,
        "section_count": section_count,
        "has_abstract": has_abstract,
        "figure_count": figure_count,
        "figure_density": round(figure_count / per_kilo, 2),
        "formula_count": formula_count,
        "formula_density": round(formula_count / per_kilo, 2),
        "reference_count": reference_count,
    }


def heuristic_score(metrics):
    """启发式质量分（0-100），仅用于样例间相对排序。"""
    score = 0.0
    for key, (target, weight) in SCORE_TARGETS.items():
        value = metrics.get(key, 0)
        score += min(value / target, 1.0) * weight
    if metrics.get("has_abstract"):
        score += ABSTRACT_BONUS
    return round(score, 1)


def median_of(papers, key):
    values = [p["metrics"][key] for p in papers]
    if isinstance(values[0], bool):
        return sum(values) >= len(values) / 2.0
    return round(statistics.median(values), 2)


def build_report(samples_dir, papers):
    median_keys = [
        "word_count", "section_count", "heading_max_depth",
        "figure_density", "formula_density", "reference_count", "has_abstract",
    ]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "samples_dir": str(samples_dir),
        "paper_count": len(papers),
        "papers": papers,
        "median": {k: median_of(papers, k) for k in median_keys},
        "median_score": round(statistics.median(p["score"] for p in papers), 1),
        "note": "score 为离线启发式分，仅供样例间相对排序；"
                "相关性/时间分布/作者多样性由 agent 结合检索元数据评估。",
    }


def print_table(report):
    print(f"\n样例论文评价表（{report['paper_count']} 篇，按启发式分降序）")
    print("-" * 96)
    header = (f"{'排名':<4}{'文件':<32}{'字数':>8}{'章节':>6}{'图/千字':>9}"
              f"{'式/千字':>9}{'文献':>6}{'摘要':>6}{'得分':>8}")
    print(header)
    print("-" * 96)
    for rank, p in enumerate(report["papers"], 1):
        m = p["metrics"]
        name = p["file"] if len(p["file"]) <= 30 else p["file"][:27] + "..."
        print(f"{rank:<4}{name:<32}{m['word_count']:>8}{m['section_count']:>6}"
              f"{m['figure_density']:>9}{m['formula_density']:>9}"
              f"{m['reference_count']:>6}{'有' if m['has_abstract'] else '无':>6}"
              f"{p['score']:>8}")
    print("-" * 96)
    med = report["median"]
    print(f"中位数: 字数={med['word_count']} 章节={med['section_count']} "
          f"图密度={med['figure_density']} 式密度={med['formula_density']} "
          f"文献={med['reference_count']} 分数={report['median_score']}")


def main():
    parser = argparse.ArgumentParser(
        description="样例论文离线质量评价：统计字数/章节结构/图表公式密度/"
                    "参考文献数，输出排序评价表（JSON+控制台）。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--samples-dir", required=True,
                        help="样例论文目录（扫描其中的 .md/.txt 文件）")
    parser.add_argument("--output", default="sample_evaluation.json",
                        help="评价结果 JSON 输出路径（可作为 gap_analysis.py 的 --baseline）")
    args = parser.parse_args()

    samples_dir = Path(args.samples_dir)
    if not samples_dir.is_dir():
        print(f"错误：样例目录不存在或不是目录：{samples_dir}", file=sys.stderr)
        return 2

    files = sorted(
        f for f in samples_dir.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_SUFFIXES
    )
    if not files:
        print(f"错误：目录中未找到 .md/.txt 样例论文：{samples_dir}", file=sys.stderr)
        return 2

    papers = []
    for f in files:
        try:
            metrics = analyze_paper(f)
        except OSError as exc:
            print(f"警告：读取失败，跳过 {f}：{exc}", file=sys.stderr)
            continue
        papers.append({
            "file": f.name,
            "path": str(f),
            "metrics": metrics,
            "score": heuristic_score(metrics),
        })
    if not papers:
        print("错误：所有样例文件均读取失败。", file=sys.stderr)
        return 2

    papers.sort(key=lambda p: p["score"], reverse=True)
    report = build_report(samples_dir, papers)

    output = Path(args.output)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"错误：无法写入输出文件 {output}：{exc}", file=sys.stderr)
        return 2

    print_table(report)
    print(f"\nJSON 报告已写入：{output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
