#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_style.py — 风格偏差检测与修改建议（style-calibration skill）

输入 analyze_style.py 生成的 style_profile.json 与待校准草稿，逐段对比草稿与
画像的偏差（句长/标点密度/连接词/成语/中英文混排/句首重复），输出偏差报告
JSON 与逐条修改建议清单。

诚实说明：本脚本只做可离线计量的"偏差检测 + 建议"，不自动改写文本；
实际改写由 agent 按建议清单执行。

示例：
    python apply_style.py --profile paper_output/qa/style_profile.json \
        --draft paper_output/final_paper_source.md \
        --output paper_output/qa/style_deviation_report.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from analyze_style import (clean_text, read_text, sentence_starter,
                               split_paragraphs, split_sentences, text_metrics)
except ImportError as exc:
    sys.stderr.write(f"[错误] 无法导入同目录的 analyze_style.py: {exc}\n")
    sys.exit(2)

TOOL_VERSION = "apply_style.py v1.1"
HONESTY_NOTE = ("本报告为偏差检测与修改建议清单；脚本不自动改写文本，"
                "实际改写由 agent 按建议执行。")


def load_profile(path: str) -> dict:
    """读取画像 JSON，返回其中的 metrics 字典（兼容裸 metrics 结构）。"""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"[错误] 无法读取画像文件 {path}: {exc}")
    metrics = data.get("metrics", data)
    required = ("sentence_length", "punctuation_per_1000", "connective_per_1000",
                "english_ratio", "idiom_per_1000", "starters_top")
    missing = [k for k in required if k not in metrics]
    if missing:
        raise SystemExit(f"[错误] 画像缺少字段 {missing}，请先用 analyze_style.py 生成")
    return metrics


def _issue(metric: str, draft_value, profile_value, suggestion: str) -> dict:
    return {"metric": metric, "draft": draft_value,
            "profile": profile_value, "suggestion": suggestion}


def compare_metrics(m: dict, ref: dict, tol: float, scope: str) -> list:
    """通用指标对比（段落级与全文级共用），返回 issue 列表。"""
    issues = []
    mean_len = m["sentence_length"]["mean"]
    ref_mean = ref["sentence_length"]["mean"]
    ref_p90 = ref["sentence_length"]["p90"]
    if ref_mean > 0:
        dev = (mean_len - ref_mean) / ref_mean
        if dev > tol:
            issues.append(_issue(
                "平均句长", mean_len, ref_mean,
                f"{scope}平均句长 {mean_len} 字，高于画像均值 {ref_mean} 字"
                f"（P90={ref_p90}）：建议把超过 {ref_p90} 字的长句拆成 2-3 句"))
        elif dev < -tol:
            issues.append(_issue(
                "平均句长", mean_len, ref_mean,
                f"{scope}句子偏短碎（平均 {mean_len} 字，画像均值 {ref_mean} 字）："
                "建议合并相邻短句，或补充条件/原因等从句"))

    comma = m["punctuation_per_1000"]["逗号"]
    ref_comma = ref["punctuation_per_1000"]["逗号"]
    if comma - ref_comma > max(8.0, ref_comma * 0.5):
        issues.append(_issue(
            "逗号密度", comma, ref_comma,
            f"{scope}逗号密度 {comma}/千字，画像为 {ref_comma}/千字："
            "建议将部分逗号改为句号或分号断句，避免一逗到底"))
    elif ref_comma - comma > max(8.0, ref_comma * 0.5):
        issues.append(_issue(
            "逗号密度", comma, ref_comma,
            f"{scope}逗号密度 {comma}/千字，低于画像 {ref_comma}/千字："
            "可在长句中增加停顿，贴近既往行文节奏"))

    for key in ("分号", "破折号", "顿号"):
        value = m["punctuation_per_1000"][key]
        ref_value = ref["punctuation_per_1000"][key]
        if value - ref_value > max(4.0, ref_value):
            issues.append(_issue(
                f"{key}密度", value, ref_value,
                f"{scope}{key}密度 {value}/千字，明显高于画像 {ref_value}/千字："
                f"建议减少{key}，改用画像更常用的标点"))

    eng = m["english_ratio"]
    ref_eng = ref["english_ratio"]
    if abs(eng - ref_eng) > 0.08:
        direction = "高于" if eng > ref_eng else "低于"
        issues.append(_issue(
            "英文占比", eng, ref_eng,
            f"{scope}英文字符占比 {eng:.1%}，{direction}画像 {ref_eng:.1%}："
            "核对术语中英文写法是否与既往作品一致"))

    conn = m["connective_per_1000"]
    ref_conn = ref["connective_per_1000"]
    if conn - ref_conn > max(4.0, ref_conn * 0.6):
        issues.append(_issue(
            "连接词密度", conn, ref_conn,
            f"{scope}连接词密度 {conn}/千字，高于画像 {ref_conn}/千字："
            "删减机械的“因此/然而”类衔接，改用语义自然过渡"))
    elif ref_conn - conn > max(4.0, ref_conn * 0.6):
        top = "、".join(w for w, _ in ref.get("connectives_top", [])[:3]) or "因此、然而、此外"
        issues.append(_issue(
            "连接词密度", conn, ref_conn,
            f"{scope}衔接词偏少（{conn}/千字，画像 {ref_conn}/千字）："
            f"可参考画像常用连接词：{top}"))

    idiom = m["idiom_per_1000"]
    ref_idiom = ref["idiom_per_1000"]
    if idiom - ref_idiom > max(2.0, ref_idiom):
        issues.append(_issue(
            "成语密度", idiom, ref_idiom,
            f"{scope}成语密度 {idiom}/千字，高于画像 {ref_idiom}/千字："
            "有堆砌感，建议将部分成语替换为平实表达"))
    return issues


def check_paragraph(para: str, ref: dict, tol: float) -> list:
    """段落级检查：通用指标 + 句首重复。"""
    metrics = text_metrics(para, already_clean=True)
    if metrics is None:
        return []
    issues = compare_metrics(metrics, ref, tol, scope="本段")
    starters = Counter(sentence_starter(s) for s in split_sentences(para))
    for word, count in starters.items():
        if word and count >= 3:
            issues.append(_issue(
                "句首重复", f"「{word}」×{count}", "-",
                f"本段有 {count} 个句子以「{word}」开头：建议变换句首表达"))
    return issues


def check_document(doc_m: dict, ref: dict, tol: float) -> list:
    """全文级检查：通用指标 + 句首词重合度 + 画像习惯缺失。"""
    issues = compare_metrics(doc_m, ref, tol, scope="全文")
    prof_starters = [w for w, _c, _r in ref.get("starters_top", [])[:8]]
    draft_starters = [w for w, _c, _r in doc_m.get("starters_top", [])[:8]]
    if prof_starters:
        overlap = set(prof_starters) & set(draft_starters)
        if len(overlap) < 2:
            issues.append(_issue(
                "句首词重合度", "、".join(draft_starters[:5]) or "无",
                "、".join(prof_starters[:5]),
                "草稿高频句首词与画像重合度低：可适当采用画像常用句首词起句"))
    for key, threshold in (("分号", 2.0), ("破折号", 1.5)):
        ref_value = ref["punctuation_per_1000"][key]
        value = doc_m["punctuation_per_1000"][key]
        if ref_value >= threshold and value < ref_value * 0.25:
            issues.append(_issue(
                f"{key}习惯缺失", value, ref_value,
                f"画像常用{key}（{ref_value}/千字），草稿几乎未用（{value}/千字）："
                f"可在并列长句/补充说明处使用{key}"))
    ref_idiom = ref["idiom_per_1000"]
    if ref_idiom >= 0.8 and doc_m["idiom_per_1000"] < ref_idiom * 0.3:
        examples = "、".join(w for w, _c in ref.get("idioms_found", [])[:5])
        issues.append(_issue(
            "成语习惯缺失", doc_m["idiom_per_1000"], ref_idiom,
            f"画像常用四字成语（如：{examples or '无示例'}），草稿密度偏低："
            "可在总结/评述句酌情使用"))
    return issues


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="风格偏差检测：对比草稿与 style_profile.json 画像，逐段输出偏差"
                    "报告与修改建议清单（脚本不自动改写，改写由 agent 按建议执行）。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--profile", "--style", dest="profile", required=True,
                        help="analyze_style.py 生成的画像 JSON（--style 为兼容别名）")
    parser.add_argument("--draft", "--paper", dest="draft", required=True,
                        help="待校准草稿文件 .md/.txt（--paper 为兼容别名）")
    parser.add_argument("--output", "-o",
                        default="paper_output/qa/style_deviation_report.json",
                        help="偏差报告输出路径（JSON）")
    parser.add_argument("--tolerance", type=float, default=0.30,
                        help="句长等指标的相对偏差容忍度（0.30 = ±30%%）")
    parser.add_argument("--min-para-chars", type=int, default=40,
                        help="短于该字数的段落跳过逐段检查（仍计入全文统计）")
    return parser


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    ref = load_profile(args.profile)
    if not os.path.isfile(args.draft):
        raise SystemExit(f"[错误] 草稿文件不存在: {args.draft}")

    cleaned = clean_text(read_text(args.draft))
    doc_metrics = text_metrics(cleaned, already_clean=True)
    if doc_metrics is None:
        raise SystemExit("[错误] 草稿中未检测到有效正文")

    doc_issues = check_document(doc_metrics, ref, args.tolerance)
    paragraphs = split_paragraphs(cleaned)
    findings, checked = [], 0
    for idx, para in enumerate(paragraphs, start=1):
        if len(re.sub(r"\s+", "", para)) < args.min_para_chars:
            continue
        checked += 1
        issues = check_paragraph(para, ref, args.tolerance)
        if issues:
            findings.append({"paragraph_index": idx,
                             "preview": para[:40] + ("…" if len(para) > 40 else ""),
                             "issues": issues})

    flagged = len(findings)
    para_ratio = flagged / checked if checked else 0.0
    score = round(100 * (0.6 * (1 - min(1.0, para_ratio))
                         + 0.4 * max(0.0, 1 - len(doc_issues) / 6.0)))
    report = {
        "tool": TOOL_VERSION,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "profile": os.path.abspath(args.profile),
        "draft": os.path.abspath(args.draft),
        "note": HONESTY_NOTE,
        "summary": {
            "consistency_score": score,
            "score_note": "启发式一致性分（0-100）：60% 段落达标率 + 40% 全文指标达标率",
            "paragraphs_total": len(paragraphs),
            "paragraphs_checked": checked,
            "paragraphs_flagged": flagged,
            "document_issue_count": len(doc_issues),
        },
        "document_issues": doc_issues,
        "document_metrics": doc_metrics,
        "paragraph_findings": findings,
    }
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise SystemExit(f"[错误] 无法写入报告 {args.output}: {exc}")

    print(f"[完成] 偏差报告已写入: {args.output}")
    print(f"  一致性得分: {score}/100 | 检查段落: {checked}/{len(paragraphs)}"
          f" | 偏差段落: {flagged} | 全文级问题: {len(doc_issues)}")
    for issue in doc_issues[:3]:
        print(f"  [全文] {issue['suggestion']}")
    for finding in findings[:3]:
        first = finding["issues"][0]["suggestion"]
        print(f"  [段落{finding['paragraph_index']}] {first}")
    if len(doc_issues) > 3 or len(findings) > 3:
        print("  …更多建议见报告 JSON")
    print(f"[提示] {HONESTY_NOTE}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
