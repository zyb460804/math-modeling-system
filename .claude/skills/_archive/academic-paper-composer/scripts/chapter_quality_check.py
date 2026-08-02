#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章节质量检查（chapter_quality_check.py）

对单个章节 Markdown 文件做机械可测的质量检查，输出分项 PASS/WARN/FAIL 报告：
  1. 字数（对照 --target-words 目标，±10% 内 PASS，±20% 内 WARN，超出 FAIL）
  2. 结构完整性（标题存在、层级不跳级、无空小节）
  3. 公式/图表引用存在性（正文引用"图N/表N/式(N)"是否在本章有对应定义；图片路径是否存在）
  4. 占位符残留（TODO/待补/placeholder/{{...}} 等，一律 FAIL）
  5. 段落均衡（超长段、碎段占比、长度离散度）

注意：论证质量、引用文献质量等 5 维定性评分由 agent 按
references/writing_standards.md 人工评估，本脚本只负责机械检查部分。
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

CJK_RE = re.compile(r"[㐀-䶿一-鿿]")
EN_WORD_RE = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*")
FENCE_RE = re.compile(r"```.*?```", re.S)
MATH_BLOCK_RE = re.compile(r"\$\$.*?\$\$", re.S)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)[^)]*\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

PLACEHOLDER_PATTERNS = [
    (r"\bTODO\b", "TODO"),
    (r"\bTBD\b", "TBD"),
    (r"\bFIXME\b", "FIXME"),
    (r"\bXXX\b", "XXX"),
    (r"\{\{[^}]*\}\}", "{{模板占位}}"),
    (r"\[待[补填写完成善]*\]|【待[补填写完成善]*】", "[待补]"),
    (r"待补充|待填写|待完善|此处省略|内容略", "待补充类"),
    (r"lorem\s+ipsum", "lorem ipsum"),
    (r"\[placeholder\]|\bplaceholder\b", "placeholder"),
    (r"\[插入[^\]]*\]|【插入[^】]*】", "[插入…]"),
]

FIG_REF_RE = re.compile(r"图\s*(\d+)|Figure\s+(\d+)|Fig\.\s*(\d+)")
TAB_REF_RE = re.compile(r"表\s*(\d+)|Table\s+(\d+)")
EQ_REF_RE = re.compile(r"式\s*[（(]\s*(\d+)\s*[）)]|Eq(?:uation)?\.?\s*[（(]?(\d+)[）)]?")
FIG_DEF_RE = re.compile(r"^\s*(?:!\[|图\s*\d+[：:\s]|Figure\s+\d+[.:：\s])", re.M)
EQ_DEF_RE = re.compile(r"\$\$|\\begin\{(?:equation|align|eqnarray)")


def count_words(text):
    """中文按字计、英文按词计的混合字数统计。"""
    text = FENCE_RE.sub(" ", text)
    text = MATH_BLOCK_RE.sub(" ", text)
    cjk = len(CJK_RE.findall(text))
    en = len(EN_WORD_RE.findall(text))
    return cjk + en


def first_group(match):
    return next((g for g in match.groups() if g), None)


def check_word_count(text, target):
    n = count_words(text)
    if target is None:
        status = "PASS" if n >= 200 else "WARN"
        detail = f"实际 {n} 字（未指定 --target-words，仅提示；<200 字视为 WARN）"
        return status, detail, {"count": n, "target": None}
    dev = abs(n - target) / target if target else 0
    if dev <= 0.10:
        status = "PASS"
    elif dev <= 0.20:
        status = "WARN"
    else:
        status = "FAIL"
    detail = f"实际 {n} 字 / 目标 {target} 字，偏差 {dev:.0%}（±10% PASS，±20% WARN）"
    return status, detail, {"count": n, "target": target, "deviation": round(dev, 3)}


def check_structure(lines):
    headings = []
    for i, line in enumerate(lines, 1):
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    issues = []
    if not headings:
        return "FAIL", "未找到任何 Markdown 标题（#）", {"headings": 0, "issues": ["无标题"]}
    for (l1, d1, _), (l2, d2, t2) in zip(headings, headings[1:]):
        if d2 > d1 + 1:
            issues.append(f"第 {l2} 行标题「{t2}」层级跳跃（{d1}级→{d2}级）")
    for idx, (ln, _, title) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        body = "".join(lines[ln:end])
        if count_words(body) == 0 and idx + 1 < len(headings) and headings[idx + 1][1] <= headings[idx][1]:
            issues.append(f"第 {ln} 行小节「{title}」内容为空")
    status = "PASS" if not issues else ("WARN" if all("跳跃" in s for s in issues) else "FAIL")
    detail = f"共 {len(headings)} 个标题" + ("；" + "；".join(issues) if issues else "，层级与内容正常")
    return status, detail, {"headings": len(headings), "issues": issues}


def check_references_exist(text, base_dir):
    issues, warns = [], []
    fig_refs = {first_group(m) for m in FIG_REF_RE.finditer(text)}
    tab_refs = {first_group(m) for m in TAB_REF_RE.finditer(text)}
    eq_refs = {first_group(m) for m in EQ_REF_RE.finditer(text)}
    has_fig_def = bool(FIG_DEF_RE.search(text))
    has_table_def = any(l.lstrip().startswith("|") for l in text.splitlines()) or bool(
        re.search(r"^\s*表\s*\d+[：:\s]", text, re.M))
    has_eq_def = bool(EQ_DEF_RE.search(text)) or "$" in text
    if fig_refs and not has_fig_def:
        warns.append(f"正文引用了图 {sorted(fig_refs)} 但本章未见图片/图题定义（可能在其他章节）")
    if tab_refs and not has_table_def:
        warns.append(f"正文引用了表 {sorted(tab_refs)} 但本章未见表格/表题定义（可能在其他章节）")
    if eq_refs and not has_eq_def:
        warns.append(f"正文引用了式 {sorted(eq_refs)} 但本章未见公式定义（可能在其他章节）")
    for path in IMAGE_RE.findall(text):
        if path.startswith(("http://", "https://", "data:")):
            continue
        if not (base_dir / path).exists() and not Path(path).exists():
            issues.append(f"图片路径不存在：{path}")
    if issues:
        status = "FAIL"
    elif warns:
        status = "WARN"
    else:
        status = "PASS"
    stats = {"fig_refs": len(fig_refs), "tab_refs": len(tab_refs), "eq_refs": len(eq_refs),
             "missing_images": issues, "warnings": warns}
    detail = (f"引用统计：图 {len(fig_refs)}、表 {len(tab_refs)}、式 {len(eq_refs)}"
              + ("；" + "；".join(issues + warns) if issues + warns else "，均有对应定义"))
    return status, detail, stats


def check_placeholders(lines):
    hits = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for pat, label in PLACEHOLDER_PATTERNS:
            if re.search(pat, line, re.I):
                hits.append(f"第 {i} 行：{label}")
                break
    status = "PASS" if not hits else "FAIL"
    detail = "无占位符残留" if not hits else "发现占位符：" + "；".join(hits[:10]) + (
        f"（共 {len(hits)} 处）" if len(hits) > 10 else "")
    return status, detail, {"hits": hits}


def check_paragraph_balance(text):
    body = FENCE_RE.sub("", text)
    body = MATH_BLOCK_RE.sub("", body)
    paras = []
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or HEADING_RE.match(block) or block.startswith(("|", "![", ">")):
            continue
        paras.append(count_words(block))
    if not paras:
        return "WARN", "未找到正文段落", {"paragraphs": 0}
    long_paras = sum(1 for p in paras if p > 800)
    tiny_ratio = sum(1 for p in paras if p < 40) / len(paras)
    med = statistics.median(paras)
    spread = (max(paras) / med) if med else 0
    issues = []
    if long_paras:
        issues.append(f"{long_paras} 个超长段（>800 字）")
    if len(paras) >= 5 and tiny_ratio > 0.4:
        issues.append(f"碎段占比 {tiny_ratio:.0%}（<40 字段落过多）")
    if med and spread > 8:
        issues.append(f"段落长度离散（最长/中位 = {spread:.1f}）")
    status = "PASS" if not issues else "WARN"
    detail = (f"段落 {len(paras)} 个，中位 {med:.0f} 字，最长 {max(paras)} 字"
              + ("；" + "；".join(issues) if issues else "，分布均衡"))
    return status, detail, {"paragraphs": len(paras), "median": med, "max": max(paras), "issues": issues}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="chapter_quality_check.py",
        description="章节质量检查：字数/结构/图表公式引用/占位符/段落均衡，输出分项 PASS/WARN/FAIL。",
        epilog="示例：python chapter_quality_check.py --chapter ch1.md --target-words 1500 --json report.json")
    parser.add_argument("--chapter", required=True, help="章节 Markdown 文件路径")
    parser.add_argument("--target-words", type=int, default=None, help="该章目标字数（来自大纲），不填则只统计")
    parser.add_argument("--json", dest="json_out", default=None, help="可选：把检查结果另存为 JSON 文件")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    path = Path(args.chapter)
    if not path.is_file():
        print(f"[错误] 章节文件不存在：{path}", file=sys.stderr)
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"[错误] 无法读取 {path}：{exc}", file=sys.stderr)
        return 2
    lines = text.splitlines(keepends=True)

    checks = [
        ("字数", *check_word_count(text, args.target_words)),
        ("结构完整性", *check_structure(lines)),
        ("图表/公式引用", *check_references_exist(text, path.parent)),
        ("占位符残留", *check_placeholders(text.splitlines())),
        ("段落均衡", *check_paragraph_balance(text)),
    ]

    print("=" * 60)
    print(f"章节质量检查：{path}")
    print("=" * 60)
    results = []
    for name, status, detail, stats in checks:
        print(f"[{status}] {name}：{detail}")
        results.append({"item": name, "status": status, "detail": detail, "stats": stats})
    statuses = [r["status"] for r in results]
    overall = "FAIL" if "FAIL" in statuses else ("WARN" if "WARN" in statuses else "PASS")
    print("-" * 60)
    print(f"总体结论：{overall}")
    print("说明：论证/引用文献等 5 维定性评分由 agent 按 references/writing_standards.md 评估。")

    if args.json_out:
        report = {"chapter": str(path), "overall": overall, "checks": results}
        try:
            Path(args.json_out).write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"JSON 报告已写入：{args.json_out}")
        except OSError as exc:
            print(f"[错误] JSON 报告写入失败：{exc}", file=sys.stderr)
            return 2
    return 0 if overall != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
