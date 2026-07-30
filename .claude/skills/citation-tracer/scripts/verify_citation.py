#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_citation.py — 单条引用验证（citation-tracer skill）

功能：
  1. --citation "引用文本"：离线做 GB/T 7714 关键要素格式检查（作者/题名/年份，
     文献类型标识与来源作为提示项）
  2. --doi "10.xxxx/xxx"：离线校验 DOI 格式；--online 时查 CrossRef 确认真实存在
  3. --online：调用 CrossRef API 核验引用真实性（query.bibliographic 模糊匹配），
     超时 10s，网络失败自动降级为离线并在报告中明示

退出码：0=通过  1=发现问题  2=运行错误
"""
import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CROSSREF_WORKS = "https://api.crossref.org/works"
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
TYPE_RE = re.compile(r"\[(J|M|C|D|R|S|P|N|A|G|Z|(?:J|M|C|D|EB|DB)/OL)\]")
MATCH_THRESHOLD = 0.55


def check_gbt7714(citation):
    """离线 GB/T 7714 关键要素检查：作者/题名/年份必查，类型标识/来源为提示。"""
    elements, missing, hints = {}, [], []
    segs = [s.strip() for s in re.split(r"[.．]\s*", citation) if s.strip()]
    author = segs[0] if segs else ""
    is_author_ok = bool(author) and len(author) <= 80 and not author[0].isdigit()
    elements["author"] = author if is_author_ok else None
    if not is_author_ok:
        missing.append("作者（应位于条目起始，以句点结束）")
    title_seg = segs[1] if len(segs) > 1 else ""
    title = TYPE_RE.sub("", title_seg).strip()
    elements["title"] = title or None
    if not title:
        missing.append("题名（作者后第二段）")
    year_m = YEAR_RE.search(citation)
    elements["year"] = year_m.group(0) if year_m else None
    if not year_m:
        missing.append("年份（四位数字）")
    type_m = TYPE_RE.search(citation)
    elements["type_code"] = type_m.group(0) if type_m else None
    if not type_m:
        hints.append("建议补充文献类型标识（如 [J]/[M]/[C]/[EB/OL]）")
    source = ". ".join(segs[2:]) if len(segs) > 2 else ""
    elements["source"] = source or None
    if not source:
        hints.append("建议补充来源信息（期刊名/出版社，卷期页码）")
    return {"citation": citation, "elements": elements,
            "missing": missing, "hints": hints,
            "format_ok": not missing}


def check_doi_format(doi):
    ok = bool(DOI_RE.match(doi))
    return {"doi": doi, "format_ok": ok,
            "missing": [] if ok else ["DOI 格式不合法（应形如 10.xxxx/后缀）"],
            "hints": []}


def similarity(a, b):
    """标记化重叠率：a 的 token 有多少出现在 b 中。"""
    ta = {t for t in re.findall(r"[\w一-鿿]+", a.lower()) if len(t) > 1}
    if not ta:
        return 0.0
    tb = b.lower()
    return sum(1 for t in ta if t in tb) / len(ta)


def crossref_by_doi(doi, timeout):
    import requests
    r = requests.get(f"{CROSSREF_WORKS}/{doi}",
                     headers={"User-Agent": "citation-tracer/1.0"}, timeout=timeout)
    if r.status_code == 404:
        return {"status": "unverified", "error": "CrossRef 未收录该 DOI"}
    r.raise_for_status()
    msg = r.json().get("message", {})
    return {"status": "verified",
            "title": (msg.get("title") or [""])[0],
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip()
                        for a in msg.get("author", [])],
            "year": (msg.get("published", {}).get("date-parts", [[None]]) or [[None]])[0][0],
            "journal": (msg.get("container-title") or [""])[0],
            "doi": doi}


def crossref_by_text(citation, timeout):
    import requests
    r = requests.get(CROSSREF_WORKS,
                     params={"query.bibliographic": citation[:300], "rows": 3},
                     headers={"User-Agent": "citation-tracer/1.0"}, timeout=timeout)
    r.raise_for_status()
    items = r.json().get("message", {}).get("items", [])
    best, best_score = None, 0.0
    for it in items:
        score = similarity((it.get("title") or [""])[0], citation)
        if score > best_score:
            best, best_score = it, score
    if best is None or best_score < MATCH_THRESHOLD:
        return {"status": "unverified",
                "error": f"CrossRef 无高置信匹配（最高相似度 {best_score:.2f}）",
                "score": round(best_score, 2)}
    return {"status": "verified",
            "title": (best.get("title") or [""])[0],
            "doi": best.get("DOI"),
            "year": (best.get("published", {}).get("date-parts", [[None]]) or [[None]])[0][0],
            "journal": (best.get("container-title") or [""])[0],
            "score": round(best_score, 2)}


def online_verify(args):
    """在线核验；任何网络异常降级为离线并明示。"""
    try:
        if args.doi:
            return crossref_by_doi(args.doi, args.timeout)
        return crossref_by_text(args.citation, args.timeout)
    except ImportError:
        return {"status": "degraded", "error": "requests 未安装，已降级为离线检查"}
    except Exception as exc:
        return {"status": "degraded",
                "error": f"CrossRef 请求失败（{type(exc).__name__}: {exc}），已降级为离线检查"}


def print_report(report):
    print("=" * 60)
    print("单条引用验证报告")
    offline = report["offline"]
    if "citation" in offline:
        print(f"  引用: {offline['citation'][:80]}")
        print(f"  离线格式检查（GB/T 7714 关键要素）: {'通过' if offline['format_ok'] else '不通过'}")
        for k, label in (("author", "作者"), ("title", "题名"), ("year", "年份"),
                         ("type_code", "类型标识"), ("source", "来源")):
            v = offline["elements"].get(k)
            print(f"    {label}: {v if v else '（缺失）'}")
    else:
        print(f"  DOI: {offline['doi']}  格式: {'合法' if offline['format_ok'] else '不合法'}")
    for m in offline["missing"]:
        print(f"  ✗ 缺失: {m}")
    for h in offline["hints"]:
        print(f"  ! 提示: {h}")
    online = report.get("online")
    if online:
        print(f"\n在线核验（CrossRef）: {online['status']}")
        if online["status"] == "verified":
            print(f"  题名: {online.get('title', '')}")
            if online.get("doi"):
                print(f"  DOI: {online['doi']}")
            if online.get("year"):
                print(f"  年份: {online['year']}")
            if online.get("journal"):
                print(f"  来源: {online['journal']}")
            if online.get("score") is not None:
                print(f"  相似度: {online['score']}")
        else:
            print(f"  ⚠ {online.get('error', '')}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="验证单条引用：离线 GB/T 7714 格式合规检查（作者/题名/年份），"
                    "--doi 校验 DOI，--online 可选调用 CrossRef 核验真实性（失败自动降级为离线）")
    parser.add_argument("--citation", help='引用文本，如 "张三, 李四. 题名[J]. 期刊名, 2024, 12(3): 1-10."')
    parser.add_argument("--doi", help='DOI，如 "10.1234/example"')
    parser.add_argument("--online", action="store_true", help="调用 CrossRef API 核验真实性（需联网）")
    parser.add_argument("--output", help="可选：JSON 报告输出路径")
    parser.add_argument("--timeout", type=float, default=10.0, help="在线请求超时秒数（默认 10）")
    args = parser.parse_args()
    if not args.citation and not args.doi:
        parser.error("必须提供 --citation 或 --doi 至少一个")
    offline = check_doi_format(args.doi) if args.doi else check_gbt7714(args.citation)
    online = online_verify(args) if args.online else None
    report = {"offline": offline, "online": online}
    print_report(report)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已写入: {args.output}")
    has_issue = (not offline["format_ok"]) or (online is not None
                                               and online.get("status") == "unverified")
    return 1 if has_issue else 0


if __name__ == "__main__":
    sys.exit(main())
