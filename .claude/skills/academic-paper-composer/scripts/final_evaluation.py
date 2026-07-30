#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全文最终评价（final_evaluation.py）

对完整论文 Markdown 做机械可测维度的打分（每维 10 分，共 40 分）：
  1. 结构齐全度：摘要/引言/结论/参考文献 + 主体章节数量
  2. 字数达标：对照 --min-words / --max-words 区间
  3. 图表表格计数：图片、图题、表格数量及"图N/表N"引用-定义匹配
  4. 引用完整性：参考文献条目数、文内引用 [n] 与文献表的对应关系

输出 JSON 评分（--json 指定路径，默认打印到 stdout）+ 控制台摘要。
通过线：≥32/40（80%）。

注意：SKILL.md 的 7 维定性评价（论证质量/原创性/方法严谨性等）由 agent 按
references/writing_standards.md 评估，本脚本只覆盖可离线机械检查的 4 个维度。
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

CJK_RE = re.compile(r"[㐀-䶿一-鿿]")
EN_WORD_RE = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*")
FENCE_RE = re.compile(r"```.*?```", re.S)
MATH_BLOCK_RE = re.compile(r"\$\$.*?\$\$", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
FIG_CAP_RE = re.compile(r"^\s*(?:图\s*(\d+)|Figure\s+(\d+))[.:：\s]", re.M)
TAB_CAP_RE = re.compile(r"^\s*(?:表\s*(\d+)|Table\s+(\d+))[.:：\s]", re.M)
FIG_REF_RE = re.compile(r"图\s*(\d+)|Figure\s+(\d+)")
TAB_REF_RE = re.compile(r"表\s*(\d+)|Table\s+(\d+)")
NUM_CITE_RE = re.compile(r"\[(\d{1,3})(?:[-–,]\s*(\d{1,3}))?\]")

REQUIRED_SECTIONS = {
    "摘要": r"摘\s*要|abstract",
    "引言/问题重述": r"引言|绪论|问题重述|introduction",
    "结论": r"结论|总结|conclusion",
    "参考文献": r"参考文献|references|bibliography",
}


def count_words(text):
    """中文按字计、英文按词计的混合字数统计。"""
    text = FENCE_RE.sub(" ", text)
    text = MATH_BLOCK_RE.sub(" ", text)
    return len(CJK_RE.findall(text)) + len(EN_WORD_RE.findall(text))


def num_set(matches):
    out = set()
    for m in matches:
        g = next((x for x in m.groups() if x), None)
        if g:
            out.add(int(g))
    return out


def eval_structure(text):
    headings = [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(text)]
    titles = " | ".join(t for _, t in headings).lower()
    found, missing = [], []
    for name, pat in REQUIRED_SECTIONS.items():
        if re.search(pat, titles, re.I) or re.search(r"^\s*\*{0,2}(" + pat + r")\*{0,2}\s*$", text, re.I | re.M):
            found.append(name)
        else:
            missing.append(name)
    top = [t for d, t in headings if d <= 2]
    body_chapters = max(0, len(top) - len(found))
    score = 2.0 * len(found)
    score += 2.0 if body_chapters >= 3 else (1.0 if body_chapters >= 1 else 0.0)
    score = min(10.0, score)
    detail = {"found_sections": found, "missing_sections": missing,
              "top_level_headings": len(top), "body_chapters_estimate": body_chapters}
    summary = (f"必备节 {len(found)}/4" + (f"（缺：{'、'.join(missing)}）" if missing else "")
               + f"，主体章节约 {body_chapters} 章")
    return score, summary, detail


def eval_word_count(text, min_words, max_words):
    n = count_words(text)
    if min_words <= n <= max_words:
        score = 10.0
    elif n < min_words:
        score = round(10.0 * n / min_words, 1) if min_words else 0.0
    else:
        over = (n - max_words) / max_words
        score = max(6.0, round(10.0 - 10.0 * over, 1))
    summary = f"全文 {n} 字（达标区间 {min_words}-{max_words}）"
    return min(10.0, max(0.0, score)), summary, {"count": n, "min": min_words, "max": max_words}


def eval_figures_tables(text):
    images = len(IMAGE_RE.findall(text))
    fig_caps = num_set(FIG_CAP_RE.finditer(text))
    tab_caps = num_set(TAB_CAP_RE.finditer(text))
    md_tables = len(re.findall(r"^\s*\|.*\|\s*$\n^\s*\|[\s:|-]+\|\s*$", text, re.M))
    figures = max(images, len(fig_caps))
    tables = max(md_tables, len(tab_caps))
    fig_refs = num_set(FIG_REF_RE.finditer(text)) - fig_caps
    tab_refs = num_set(TAB_REF_RE.finditer(text)) - tab_caps
    dangling = []
    if fig_caps and fig_refs - fig_caps:
        dangling.append(f"图引用无定义：{sorted(fig_refs - fig_caps)}")
    if tab_caps and tab_refs - tab_caps:
        dangling.append(f"表引用无定义：{sorted(tab_refs - tab_caps)}")
    score = min(6.0, 2.0 * figures) + min(4.0, 2.0 * tables)
    score = max(0.0, score - 2.0 * len(dangling))
    summary = f"图 {figures} 幅、表 {tables} 张" + ("；" + "；".join(dangling) if dangling else "")
    detail = {"figures": figures, "tables": tables, "images": images,
              "fig_captions": sorted(fig_caps), "tab_captions": sorted(tab_caps),
              "dangling_refs": dangling}
    return min(10.0, score), summary, detail


def eval_citations(text):
    m = re.search(r"^#{1,3}\s*.*(参考文献|references|bibliography).*$", text, re.I | re.M)
    if not m:
        return 0.0, "未找到参考文献节", {"entries": 0, "in_text": 0, "broken": []}
    ref_block = text[m.end():]
    nxt = re.search(r"^#{1,3}\s+", ref_block, re.M)
    if nxt:
        ref_block = ref_block[:nxt.start()]
    entry_nums = {int(x) for x in re.findall(r"^\s*\[?(\d{1,3})[\].、.]\s+\S", ref_block, re.M)}
    entries = len(entry_nums) or len([l for l in ref_block.splitlines() if l.strip()])
    body = text[:m.start()]
    cited = set()
    for a, b in NUM_CITE_RE.findall(body):
        if b and abs(int(b) - int(a)) <= 50:
            cited.update(range(min(int(a), int(b)), max(int(a), int(b)) + 1))
        else:
            cited.add(int(a))
    broken = sorted(cited - entry_nums) if entry_nums else []
    score = 4.0 if entries else 0.0
    score += min(3.0, 0.3 * entries)
    if cited:
        score += 3.0 * (1 - len(broken) / len(cited))
    summary = (f"参考文献 {entries} 条，文内引用 {len(cited)} 处"
               + (f"；断链引用：{broken}" if broken else ""))
    detail = {"entries": entries, "in_text": len(cited), "broken": broken}
    return min(10.0, round(score, 1)), summary, detail


def build_parser():
    parser = argparse.ArgumentParser(
        prog="final_evaluation.py",
        description="全文最终评价：结构齐全度/字数达标/图表表格计数/引用完整性 4 维打分（各 10 分，共 40 分，通过线 32）。",
        epilog="示例：python final_evaluation.py --paper final_paper.md --min-words 5000 --max-words 12000 --json final_eval.json")
    parser.add_argument("--paper", required=True, help="全文 Markdown 文件路径")
    parser.add_argument("--min-words", type=int, default=5000, help="字数达标下限（默认 5000）")
    parser.add_argument("--max-words", type=int, default=12000, help="字数达标上限（默认 12000）")
    parser.add_argument("--json", dest="json_out", default=None,
                        help="可选：JSON 评分输出路径；不填则将 JSON 打印到 stdout")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.min_words <= 0 or args.max_words < args.min_words:
        print("[错误] --min-words/--max-words 区间非法", file=sys.stderr)
        return 2
    path = Path(args.paper)
    if not path.is_file():
        print(f"[错误] 论文文件不存在：{path}", file=sys.stderr)
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"[错误] 无法读取 {path}：{exc}", file=sys.stderr)
        return 2

    dims = [
        ("structure", "结构齐全度", *eval_structure(text)),
        ("word_count", "字数达标", *eval_word_count(text, args.min_words, args.max_words)),
        ("figures_tables", "图表表格", *eval_figures_tables(text)),
        ("citations", "引用完整性", *eval_citations(text)),
    ]
    total = round(sum(d[2] for d in dims), 1)
    passed = total >= 32.0
    report = {
        "paper": str(path),
        "total": total,
        "max_total": 40,
        "pass_threshold": 32,
        "passed": passed,
        "dimensions": {key: {"name": name, "score": score, "max": 10,
                             "summary": summary, "detail": detail}
                       for key, name, score, summary, detail in dims},
        "note": "本脚本仅覆盖机械可测 4 维；论证质量/原创性/方法严谨性等 7 维定性评价由 agent 按 references/writing_standards.md 评估。",
    }

    print("=" * 60)
    print(f"全文最终评价：{path}")
    print("=" * 60)
    for _, name, score, summary, _ in dims:
        print(f"  {name}：{score}/10 —— {summary}")
    print("-" * 60)
    print(f"总分：{total}/40（通过线 32）→ {'PASS' if passed else 'FAIL'}")
    print("说明：定性 7 维（论证/原创性/方法等）由 agent 评估，不在本脚本范围内。")

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        try:
            Path(args.json_out).write_text(payload, encoding="utf-8")
            print(f"JSON 评分已写入：{args.json_out}")
        except OSError as exc:
            print(f"[错误] JSON 写入失败：{exc}", file=sys.stderr)
            return 2
    else:
        print(payload)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
