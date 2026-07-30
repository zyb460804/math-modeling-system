#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AI 失败模式检查器（离线启发式版）。

对论文 Markdown 做 7 类 AI 失败模式扫描，每类输出 PASS/FAIL 与证据行号：
  1. 占位符/TODO 残留
  2. 可疑编造标记（"数据来源：略"、示例年份连号等）
  3. 文内引用断链（[n] 引用与参考文献列表不匹配）
  4. 数字自相矛盾（同一主体+同一指标多处不同值的粗检）
  5. AI 套话（基于 anti-ai-detection-guide.md 禁用词表）
  6. 空洞章节（正文 <100 字的叶子节）
  7. 图表引用悬空（引用了没有题注/图片定义的图/表编号）

语义级检查（幻觉、方法适用性、结论合理性）无法离线判定，由 agent 按 SKILL.md 清单完成。
数字与代码结果的交叉验证由 quality-assurance-auditor/scripts/check_number_consistency.py 负责。
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_GUIDE = os.path.normpath(os.path.join(
    SCRIPT_DIR, "..", "..", "paper-formal-writer", "references", "anti-ai-detection-guide.md"))

MODE_NAMES = {
    1: "占位符/TODO残留", 2: "可疑编造标记", 3: "文内引用断链",
    4: "数字自相矛盾", 5: "AI套话(禁用词表)", 6: "空洞章节(<100字)",
    7: "图表引用悬空",
}

PLACEHOLDER_PATTERNS = [
    (re.compile(r"\bTODO\b|\bFIXME\b|\bTBD\b", re.I), "TODO/FIXME/TBD 残留"),
    (re.compile(r"待(补充|填写|完善|插入|确定)"), "『待补充』类占位"),
    (re.compile(r"占位符?"), "『占位』标记"),
    (re.compile(r"此处(省略|待)"), "『此处省略/待』标记"),
    (re.compile(r"[（(]略[)）]"), "（略）占位"),
    (re.compile(r"_{4,}|＿{3,}"), "下划线填空占位"),
    (re.compile(r"\?{3,}|？{3,}"), "问号占位"),
    (re.compile(r"\bXXX+\b"), "XXX 占位"),
]

FAB_PATTERNS = [
    (re.compile(r"数据来源[：:]\s*(略|暂无|待定|不详|无)"), "数据来源缺失标记", "FAIL"),
    (re.compile(r"示例数据|虚构数据|杜撰|编造"), "示例/虚构数据标记", "FAIL"),
    (re.compile(r"数据仅供参考|数据为示意|示意数据"), "示意数据标记", "FAIL"),
]
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
CITE_RE = re.compile(r"(?<!!)\[([\d,，、\-\s]+)\]")
REF_DEF_RE = re.compile(r"^\s*\[?(\d{1,3})[\]\.、．]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)")
METRIC_RE = re.compile(
    r"(?:([一-龥A-Za-z0-9_\-]{1,12})\s*的\s*)?"
    r"(准确率|精确率|精度|召回率|F1\s*分数|F1\s*值|F1|RMSE|MAE|MAPE|AUC|R2|R²|误差率|拟合优度)"
    r"\s*(?:为|达到|达|是|约为|约|=|：|:)\s*([0-9]+(?:\.[0-9]+)?)\s*(%|％)?")
FIG_DEF_RE = re.compile(r"^\s*(?:>+\s*)?(?:\*\*)?\s*图\s*([0-9]+(?:[.\-][0-9]+)?)")
TBL_DEF_RE = re.compile(r"^\s*(?:>+\s*)?(?:\*\*)?\s*表\s*([0-9]+(?:[.\-][0-9]+)?)")
IMG_ALT_FIG_RE = re.compile(r"!\[[^\]]*?图\s*([0-9]+(?:[.\-][0-9]+)?)[^\]]*?\]")
FIG_REF_RE = re.compile(r"图\s*([0-9]+(?:[.\-][0-9]+)?)")
TBL_REF_RE = re.compile(r"(?<!附)表\s*([0-9]+(?:[.\-][0-9]+)?)")

GUIDE_SKIP_WORDS = ("禁用", "禁止", "替换", "过度使用", "问题", "建议", "正确",
                    "频率", "AI 特征", "修复", "表现", "应使用")
PHRASE_ALLOWANCE = {"此外": 2, "moreover": 1, "furthermore": 1,
                    "a wide range of": 1, "关键的": 1, "核心的": 1}
BUILTIN_PHRASES = ["标志着", "奠定了坚实基础", "发挥了重要作用", "具有重要意义",
                   "突破性的", "令人震撼的", "不仅…而且…", "深入探讨", "此外",
                   "研究表明", "众所周知", "前景广阔", "值得注意的是"]


def issue(line_no, text, note):
    return {"line": line_no, "text": text.strip()[:120], "note": note}


def check_placeholders(lines):
    issues = []
    for i, ln in enumerate(lines, 1):
        for pat, note in PLACEHOLDER_PATTERNS:
            if pat.search(ln):
                issues.append(issue(i, ln, note))
                break
    return ("FAIL" if issues else "PASS"), issues


def check_fabrication(lines):
    issues, hard = [], 0
    for i, ln in enumerate(lines, 1):
        for pat, note, sev in FAB_PATTERNS:
            if pat.search(ln):
                issues.append(issue(i, ln, note))
                hard += 1
                break
        years = [int(m.group()) for m in YEAR_RE.finditer(ln)]
        run = best = 1
        for a, b in zip(years, years[1:]):
            run = run + 1 if b == a + 1 else 1
            best = max(best, run)
        if best >= 5:
            issues.append(issue(i, ln, f"疑似示例连号年份（连续 {best} 年，请确认为真实数据）[WARN]"))
    return ("FAIL" if hard else "PASS"), issues


def _parse_cite_nums(content):
    nums = set()
    for part in re.split(r"[,，、]", content):
        part = part.strip()
        m = re.match(r"^(\d{1,3})\s*-\s*(\d{1,3})$", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < b - a <= 50:
                nums.update(range(a, b + 1))
        elif re.match(r"^\d{1,3}$", part):
            nums.add(int(part))
    return nums


def check_citations(lines):
    ref_start = None
    for i, ln in enumerate(lines):
        if HEADING_RE.match(ln) and re.search(r"参考文献|References", ln, re.I):
            ref_start = i
            break
    cited, defined, issues = {}, set(), []
    body_end = ref_start if ref_start is not None else len(lines)
    for i, ln in enumerate(lines[:body_end], 1):
        for m in CITE_RE.finditer(ln):
            for n in _parse_cite_nums(m.group(1)):
                cited.setdefault(n, i)
    if ref_start is not None:
        for ln in lines[ref_start + 1:]:
            m = REF_DEF_RE.match(ln)
            if m:
                defined.add(int(m.group(1)))
    if not cited:
        return "PASS", [issue(0, "", "正文未检出 [n] 数字引用，跳过")]
    if ref_start is None:
        return "FAIL", [issue(ln_no, f"[{n}]", "正文有引用但未找到参考文献章节")
                        for n, ln_no in sorted(cited.items())][:10]
    dangling = sorted(set(cited) - defined)
    for n in dangling:
        issues.append(issue(cited[n], f"[{n}]", f"引用 [{n}] 在参考文献中无对应条目"))
    for n in sorted(defined - set(cited)):
        issues.append(issue(0, f"[{n}]", f"参考文献 [{n}] 未被正文引用 [WARN]"))
    return ("FAIL" if dangling else "PASS"), issues


def check_number_conflicts(lines):
    groups = {}
    for i, ln in enumerate(lines, 1):
        for m in METRIC_RE.finditer(ln):
            subj = (m.group(1) or "").strip()
            metric = re.sub(r"\s", "", m.group(2)).upper().replace("R²", "R2")
            metric = {"F1分数": "F1", "F1值": "F1"}.get(metric, metric)
            unit = "%" if m.group(4) else ""
            groups.setdefault((subj, metric, unit), []).append((m.group(3), i, ln))
    issues = []
    for (subj, metric, unit), vals in groups.items():
        distinct = {v for v, _, _ in vals}
        if len(distinct) > 1:
            label = f"{subj + '的' if subj else ''}{metric}"
            for v, i, ln in vals:
                issues.append(issue(i, ln, f"『{label}』出现多个不同值: {sorted(distinct)}"))
    return ("FAIL" if issues else "PASS"), issues


def load_banned_phrases(guide_path):
    phrases = []
    try:
        with open(guide_path, encoding="utf-8") as f:
            raw = f.read().splitlines()
    except OSError:
        return list(BUILTIN_PHRASES), False
    for ln in raw:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        cell = cells[0] if cells else ""
        if not cell or set(cell) <= set("-: ") or "❌" in cell or "✅" in cell:
            continue
        if any(w in cell for w in GUIDE_SKIP_WORDS):
            continue
        cell = re.sub(r"（[^）]*）", "", cell).strip()
        for part in re.split(r"\s*/\s*", cell):
            part = part.strip()
            if 2 <= len(part) <= 24 and part not in phrases:
                phrases.append(part)
    return (phrases if phrases else list(BUILTIN_PHRASES)), bool(phrases)


def check_ai_phrases(lines, guide_path, threshold):
    phrases, from_guide = load_banned_phrases(guide_path)
    issues, total = [], 0
    for phrase in phrases:
        pat = re.escape(phrase).replace(re.escape("…"), ".{0,12}").replace(r"\.\.\.", ".{0,20}")
        try:
            rx = re.compile(pat, re.IGNORECASE)
        except re.error:
            continue
        hits, count = [], 0
        for i, ln in enumerate(lines, 1):
            n = len(rx.findall(ln))
            if n:
                hits.append((i, ln))
                count += n
        allowed = PHRASE_ALLOWANCE.get(phrase, 0)
        if count > allowed:
            total += count - allowed
            for i, ln in hits[:3]:
                issues.append(issue(i, ln, f"禁用词『{phrase}』共 {count} 次(允许 {allowed})"))
    src = "词表来源: anti-ai-detection-guide.md" if from_guide else "词表来源: 内置兜底(指南未解析)"
    issues.insert(0, issue(0, "", f"{src}, 共 {len(phrases)} 条, 超限命中 {total} 处"))
    return ("FAIL" if total >= threshold else "PASS"), issues


def check_empty_sections(lines):
    heads = [(i, len(m.group(1)), m.group(2).strip())
             for i, ln in enumerate(lines) if (m := HEADING_RE.match(ln))]
    issues = []
    skip = re.compile(r"参考文献|附录|目录|References|Appendix", re.I)
    for idx, (pos, level, title) in enumerate(heads):
        nxt = heads[idx + 1] if idx + 1 < len(heads) else None
        if nxt and nxt[1] > level:
            continue  # 有子节的父标题不算空洞
        if skip.search(title):
            continue
        end = nxt[0] if nxt else len(lines)
        body = re.sub(r"\s", "", "".join(lines[pos + 1:end]))
        if len(body) < 100:
            issues.append(issue(pos + 1, lines[pos], f"节『{title}』正文仅 {len(body)} 字"))
    return ("FAIL" if issues else "PASS"), issues


def check_figure_refs(lines):
    fig_defs, tbl_defs, fig_refs, tbl_refs = set(), set(), {}, {}
    for i, ln in enumerate(lines, 1):
        for m in IMG_ALT_FIG_RE.finditer(ln):
            fig_defs.add(m.group(1))
        if FIG_DEF_RE.match(ln):
            fig_defs.add(FIG_DEF_RE.match(ln).group(1))
            continue
        if TBL_DEF_RE.match(ln):
            tbl_defs.add(TBL_DEF_RE.match(ln).group(1))
            continue
        for m in FIG_REF_RE.finditer(ln):
            fig_refs.setdefault(m.group(1), i)
        for m in TBL_REF_RE.finditer(ln):
            tbl_refs.setdefault(m.group(1), i)
    issues = []
    if not fig_defs and not tbl_defs and (fig_refs or tbl_refs):
        issues.append(issue(0, "", "全文未检出任何图/表题注定义（若图表在排版阶段插入可忽略）[WARN]"))
    for n in sorted(set(fig_refs) - fig_defs, key=str):
        issues.append(issue(fig_refs[n], f"图{n}", f"引用了图 {n} 但未找到题注/图片定义"))
    for n in sorted(set(tbl_refs) - tbl_defs, key=str):
        issues.append(issue(tbl_refs[n], f"表{n}", f"引用了表 {n} 但未找到题注定义"))
    dangling = [x for x in issues if "[WARN]" not in x["note"]]
    return ("FAIL" if dangling else "PASS"), issues


def main():
    parser = argparse.ArgumentParser(
        description="AI 失败模式检查：对论文 Markdown 做 7 类离线启发式扫描，"
                    "每类输出 PASS/FAIL 与证据行号。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--paper", required=True, help="论文 Markdown 文件路径")
    parser.add_argument("--source", default=None,
                        help="结果证据目录（可选，仅记录存在性；数字交叉验证请用 check_number_consistency.py）")
    parser.add_argument("--output", default=None, help="JSON 报告输出路径（可选）")
    parser.add_argument("--guide", default=DEFAULT_GUIDE, help="禁用词表指南路径")
    parser.add_argument("--banned-threshold", type=int, default=5,
                        help="AI 套话超限命中达到该数即判 FAIL")
    args = parser.parse_args()

    try:
        with open(args.paper, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as exc:
        print(f"[ERROR] 无法读取论文文件: {exc}", file=sys.stderr)
        return 2

    results = []
    checks = [
        (1, lambda: check_placeholders(lines)),
        (2, lambda: check_fabrication(lines)),
        (3, lambda: check_citations(lines)),
        (4, lambda: check_number_conflicts(lines)),
        (5, lambda: check_ai_phrases(lines, args.guide, args.banned_threshold)),
        (6, lambda: check_empty_sections(lines)),
        (7, lambda: check_figure_refs(lines)),
    ]
    for mode_id, fn in checks:
        try:
            status, issues = fn()
        except Exception as exc:  # 单模式失败不中断整体
            status, issues = "FAIL", [issue(0, "", f"检查执行异常: {exc}")]
        results.append({"mode": mode_id, "name": MODE_NAMES[mode_id],
                        "status": status, "issues": issues})

    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    print(f"== AI 失败模式检查: {os.path.basename(args.paper)} ==")
    for r in results:
        real = [x for x in r["issues"] if x["line"] > 0]
        print(f"[{r['status']}] mode{r['mode']} {r['name']}: {len(real)} 处证据")
        for x in r["issues"][:5]:
            loc = f"L{x['line']}" if x["line"] > 0 else "-"
            print(f"    {loc}: {x['note']}" + (f" | {x['text'][:60]}" if x["text"] else ""))
    print(f"总结: {n_fail}/7 个模式 FAIL -> {'FAIL' if n_fail else 'PASS'}")

    report = {"paper": args.paper, "modes": results,
              "summary": {"fail_modes": n_fail,
                          "status": "FAIL" if n_fail else "PASS"},
              "note": "语义级检查(幻觉/方法适用性/结论合理性)由 agent 按 SKILL.md 清单完成"}
    if args.source:
        exists = os.path.isdir(args.source)
        report["source_dir"] = {"path": args.source, "exists": exists,
                                "n_files": len(os.listdir(args.source)) if exists else 0}
    if args.output:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"报告已写入: {args.output}")
        except OSError as exc:
            print(f"[ERROR] 报告写入失败: {exc}", file=sys.stderr)
            return 2
    return 1 if n_fail else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
