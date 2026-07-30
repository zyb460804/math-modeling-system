#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all_citations.py — 论文引用完整性双向检查（citation-tracer skill）

功能：
  1. 从论文（.md / .tex / .txt / .docx）提取文内引用标记：[1] 数字式、\\cite{key} 式、（作者, 年份）式
  2. 提取参考文献列表：论文内“参考文献/References”节，或 --references 指定的 .bib / 文本文件
  3. 双向匹配检查：文内引了但列表没有（断链）/ 列表有但文内未引 / 列表编号断档
  4. --online 时调用 CrossRef API（query.bibliographic）核验条目真实性，
     超时 10s，网络失败自动降级为离线并在报告中明示

退出码：0=无问题  1=发现引用问题  2=运行错误
"""
import argparse
import json
import os
import re
import sys
import zipfile
from html import unescape

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF_HEADING_RE = re.compile(
    r'^\s{0,3}(?:#{1,6}\s*)?(?:\\section\*?\{)?(?:\d+[.、]?\s*)?'
    r'(参考文献|References|Bibliography|REFERENCES)\}?\s*$', re.M)
NUMERIC_CITE_RE = re.compile(r'\[(\d{1,3}(?:\s*[-–—,，]\s*\d{1,3})*)\]')
LATEX_CITE_RE = re.compile(
    r'\\(?:cite|citep|citet|parencite|footcite|autocite)\*?(?:\[[^\]]*\])?\{([^}]+)\}')
AUTHOR_YEAR_RE = re.compile(r'[（(]([^（）()\d]{1,40}?)[,，]\s*((?:19|20)\d{2})[a-z]?[）)]')
REF_LINE_NUM_RE = re.compile(r'^\s*(?:[\[［](\d{1,3})[\]］]|(\d{1,3})[.、])\s*(\S.*)$')
BIBITEM_RE = re.compile(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}')
BIB_ENTRY_RE = re.compile(r'@(\w+)\s*\{\s*([^,\s]+)\s*,')
MAX_CITE_NUM = 200
CROSSREF_URL = "https://api.crossref.org/works"
MATCH_THRESHOLD = 0.55


def read_text_file(path):
    """按 utf-8 / utf-8-sig / gbk 依次尝试读取文本。"""
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def read_docx_text(path):
    """从 .docx 提取纯文本（仅 stdlib：zipfile + 正则去标签）。"""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = xml.replace("</w:p>", "\n").replace("<w:tab/>", "\t")
    return unescape(re.sub(r"<[^>]+>", "", xml))


def load_paper(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return read_docx_text(path)
    return read_text_file(path)


def expand_numeric_token(token):
    """把 '1-3,5' 展开为 [1,2,3,5]；异常范围直接跳过。"""
    nums = []
    for part in re.split(r"[,，]", token):
        part = part.strip()
        m = re.match(r"^(\d{1,3})\s*[-–—]\s*(\d{1,3})$", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < a <= b <= MAX_CITE_NUM and b - a <= 50:
                nums.extend(range(a, b + 1))
        elif part.isdigit() and 0 < int(part) <= MAX_CITE_NUM:
            nums.append(int(part))
    return nums


def split_reference_section(text):
    """返回 (正文, 参考文献节文本)。找不到标题则返回 (text, '')。"""
    matches = list(REF_HEADING_RE.finditer(text))
    if not matches:
        return text, ""
    m = matches[-1]
    return text[:m.start()], text[m.end():]


def parse_numbered_refs(refs_text):
    """解析编号型参考文献列表，支持 [1]/1. 两种编号与续行。"""
    entries, current = [], None
    for line in refs_text.splitlines():
        if not line.strip():
            current = None
            continue
        m = REF_LINE_NUM_RE.match(line)
        if m:
            num = int(m.group(1) or m.group(2))
            current = {"number": num, "key": None, "text": m.group(3).strip()}
            entries.append(current)
        elif current is not None:
            current["text"] += " " + line.strip()
    return entries


def parse_bib_file(path):
    """解析 .bib：返回 [{key, text}]，text 为 title+author+year 拼接。"""
    text = read_text_file(path)
    entries = []
    for m in BIB_ENTRY_RE.finditer(text):
        seg = text[m.end():m.end() + 1500]
        fields = dict(re.findall(r'(\w+)\s*=\s*[{"]([^}"]*)[}"]', seg))
        desc = ". ".join(v for k, v in fields.items()
                         if k.lower() in ("author", "title", "journal", "year") and v)
        entries.append({"number": None, "key": m.group(2), "text": desc or m.group(2)})
    return entries


def parse_bibitems(text):
    """解析 LaTeX thebibliography 的 \\bibitem 条目。"""
    entries = []
    items = list(BIBITEM_RE.finditer(text))
    for i, m in enumerate(items):
        end = items[i + 1].start() if i + 1 < len(items) else min(len(text), m.end() + 800)
        body = re.sub(r"\s+", " ", text[m.end():end]).strip()
        entries.append({"number": i + 1, "key": m.group(1), "text": body[:300]})
    return entries


def extract_in_text(body):
    """提取三类文内引用。数字式排除疑似非引用（>MAX_CITE_NUM 已在展开时过滤）。"""
    numeric = sorted({n for m in NUMERIC_CITE_RE.finditer(body)
                      for n in expand_numeric_token(m.group(1))})
    latex_keys = sorted({k.strip() for m in LATEX_CITE_RE.finditer(body)
                         for k in m.group(1).split(",") if k.strip()})
    author_year = sorted({(m.group(1).strip(), m.group(2))
                          for m in AUTHOR_YEAR_RE.finditer(body)})
    return numeric, latex_keys, author_year


def check_numeric(cited, refs, issues):
    listed = {e["number"] for e in refs if e["number"]}
    for n in sorted(set(cited) - listed):
        issues.append({"type": "cited_not_listed",
                       "detail": f"文内引用 [{n}] 在参考文献列表中不存在（断链）"})
    for n in sorted(listed - set(cited)):
        issues.append({"type": "listed_not_cited",
                       "detail": f"参考文献 [{n}] 未在正文中被引用"})
    if listed:
        gaps = sorted(set(range(1, max(listed) + 1)) - listed)
        for n in gaps:
            issues.append({"type": "numbering_gap",
                           "detail": f"参考文献列表编号断档：缺 [{n}]"})


def check_latex(cited_keys, refs, issues):
    listed = {e["key"] for e in refs if e["key"]}
    if not listed:
        issues.append({"type": "no_ref_keys",
                       "detail": "检测到 \\cite 引用，但参考文献无 key（需 --references 提供 .bib 或使用 \\bibitem）"})
        return
    for k in sorted(set(cited_keys) - listed):
        issues.append({"type": "cited_not_listed", "detail": f"\\cite{{{k}}} 在参考文献中不存在（断链）"})
    for k in sorted(listed - set(cited_keys)):
        issues.append({"type": "listed_not_cited", "detail": f"参考文献条目 {k} 未在正文中被引用"})


def check_author_year(pairs, refs, issues):
    for author, year in pairs:
        surname = re.split(r"[\s,，等&]|et\s+al", author)[0].strip()
        hit = any(surname and surname in e["text"] and year in e["text"] for e in refs)
        if not hit:
            issues.append({"type": "cited_not_listed",
                           "detail": f"文内引用（{author}, {year}）未在参考文献中找到匹配条目"})


def similarity(a, b):
    """标记化重叠率：a 的 token 有多少出现在 b 中。"""
    ta = {t for t in re.findall(r"[\w\u4e00-\u9fff]+", a.lower()) if len(t) > 1}
    if not ta:
        return 0.0
    tb = b.lower()
    return sum(1 for t in ta if t in tb) / len(ta)


def online_verify(refs, timeout, max_n):
    """CrossRef 逐条核验；网络异常立即整体降级为离线并明示。"""
    try:
        import requests
    except ImportError:
        return {"status": "degraded", "error": "requests 未安装，已降级为离线检查", "results": []}
    results = []
    for e in refs[:max_n]:
        query = e["text"][:300]
        try:
            r = requests.get(CROSSREF_URL,
                             params={"query.bibliographic": query, "rows": 3},
                             headers={"User-Agent": "citation-tracer/1.0"},
                             timeout=timeout)
            r.raise_for_status()
            items = r.json().get("message", {}).get("items", [])
        except Exception as exc:
            return {"status": "degraded",
                    "error": f"CrossRef 请求失败（{type(exc).__name__}: {exc}），已降级为离线检查",
                    "results": results}
        best, best_score = None, 0.0
        for it in items:
            title = (it.get("title") or [""])[0]
            score = similarity(title, e["text"])
            if score > best_score:
                best, best_score = it, score
        results.append({
            "ref": e["number"] if e["number"] is not None else e["key"],
            "status": "verified" if best_score >= MATCH_THRESHOLD else "unverified",
            "matched_title": (best.get("title") or [""])[0] if best else None,
            "doi": best.get("DOI") if best else None,
            "score": round(best_score, 2)})
    note = None
    if len(refs) > max_n:
        note = f"仅核验前 {max_n} 条（共 {len(refs)} 条，可用 --max-online 调整）"
    return {"status": "ok", "note": note, "results": results}


def build_report(args):
    text = load_paper(args.paper)
    body, refs_text = split_reference_section(text)
    if args.references:
        refs = (parse_bib_file(args.references)
                if args.references.lower().endswith(".bib")
                else parse_numbered_refs(read_text_file(args.references)))
    elif "\\bibitem" in text:
        refs = parse_bibitems(text)
        body = text[:text.find("\\bibitem")]
    else:
        refs = parse_numbered_refs(refs_text)
    numeric, latex_keys, author_year = extract_in_text(body)
    issues = []
    if numeric:
        mode = "numeric"
        check_numeric(numeric, refs, issues)
    elif latex_keys:
        mode = "latex"
        check_latex(latex_keys, refs, issues)
    elif author_year:
        mode = "author_year"
        check_author_year(author_year, refs, issues)
    else:
        mode = "none"
        issues.append({"type": "no_citation_found", "detail": "正文中未检测到任何文内引用标记"})
    if not refs:
        issues.append({"type": "no_reference_list",
                       "detail": "未找到参考文献列表（论文内无“参考文献/References”节，且未指定 --references）"})
    online = online_verify(refs, args.timeout, args.max_online) if args.online else None
    return {
        "paper": args.paper, "mode": mode,
        "in_text": {"numeric": numeric, "latex_keys": latex_keys,
                    "author_year": [list(p) for p in author_year]},
        "references": refs, "issues": issues,
        "summary": {"total_in_text": len(numeric) + len(latex_keys) + len(author_year),
                    "total_references": len(refs), "issue_count": len(issues)},
        "online": online}


def print_report(report):
    print("=" * 60)
    print("引用完整性检查报告")
    print(f"  论文: {report['paper']}")
    print(f"  引用模式: {report['mode']}  文内引用 {report['summary']['total_in_text']} 处"
          f"  参考文献 {report['summary']['total_references']} 条")
    issues = report["issues"]
    if issues:
        print(f"\n发现 {len(issues)} 个问题：")
        for i, it in enumerate(issues, 1):
            print(f"  {i}. [{it['type']}] {it['detail']}")
    else:
        print("\n未发现引用完整性问题。")
    online = report.get("online")
    if online:
        print(f"\n在线核验（CrossRef）: {online['status']}")
        if online["status"] == "degraded":
            print(f"  ⚠ {online['error']}")
        for r in online.get("results", []):
            mark = "✓" if r["status"] == "verified" else "?"
            print(f"  {mark} 条目 {r['ref']}: {r['status']} score={r['score']}"
                  + (f" DOI={r['doi']}" if r.get("doi") else ""))
        if online.get("note"):
            print(f"  注: {online['note']}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="论文引用完整性双向检查：文内引用 vs 参考文献列表（断链/未引用/编号断档），"
                    "--online 可选调用 CrossRef 核验条目真实性（失败自动降级为离线）")
    parser.add_argument("--paper", required=True, help="论文文件路径（.md / .tex / .txt / .docx）")
    parser.add_argument("--references", help="可选：参考文献文件（.bib 或编号文本）；缺省从论文内提取“参考文献”节")
    parser.add_argument("--output", help="可选：JSON 报告输出路径")
    parser.add_argument("--online", action="store_true", help="调用 CrossRef API 核验条目真实性（需联网）")
    parser.add_argument("--timeout", type=float, default=10.0, help="在线请求超时秒数（默认 10）")
    parser.add_argument("--max-online", type=int, default=20, help="在线核验条目数上限（默认 20）")
    args = parser.parse_args()
    if not os.path.isfile(args.paper):
        print(f"错误: 论文文件不存在: {args.paper}", file=sys.stderr)
        return 2
    if args.references and not os.path.isfile(args.references):
        print(f"错误: 参考文献文件不存在: {args.references}", file=sys.stderr)
        return 2
    try:
        report = build_report(args)
    except (OSError, zipfile.BadZipFile) as exc:
        print(f"错误: 读取/解析失败: {exc}", file=sys.stderr)
        return 2
    print_report(report)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已写入: {args.output}")
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
