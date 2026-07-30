#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""优秀论文语料 → Markdown 转换器（为 award-paper-rag 建 RAG 索引）。

把 resources/02_优秀论文/ 下的 PDF/docx 批量转为 Markdown，
并从目录结构解析 year/problem/competition/award 生成 papers.csv。

断点续传：已转换的跳过。.doc（旧格式）需 Word，标记跳过。

用法：
  python corpus_converter.py                    # 转换全部
  python corpus_converter.py --limit 20         # 只转前 20 个（测试）
  python corpus_converter.py --root <dir>       # 指定语料根
输出：
  data/papers/*.md
  data/papers.csv   (id, year, problem, competition, award, path)
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path("e:/数学建模/resources/02_优秀论文")
DATA_DIR = Path("e:/数学建模/.claude/skills/award-paper-rag/data")
PAPERS_DIR = DATA_DIR / "papers"
CSV_FILE = DATA_DIR / "papers.csv"

# 默认语料根（多根）：02_优秀论文 + 09_竞赛资料下的论文子目录 + 05_我的作品
DEFAULT_ROOTS = [
    "e:/数学建模/resources/02_优秀论文",
    "e:/数学建模/resources/09_竞赛资料/2026电工杯竞赛助攻资料/2007~2022年电工杯数学建模竞赛优秀论文",
    "e:/数学建模/resources/09_竞赛资料/MathorCup_C题案例包/论文",
    "e:/数学建模/resources/09_竞赛资料/五一C题",
    "e:/数学建模/05_我的作品",
]

YEAR_RE = re.compile(r"(20[0-2]\d|199\d)")  # 1990-2029，排除文件名中的随机数字
PROBLEM_RE = re.compile(r"([A-Fa-f])\s*[题问]", re.UNICODE)
# 文件名非法字符（含路径分隔符 / \，"MCM/ICM" 会误建目录）
_FILENAME_UNSAFE = re.compile(r'[\\/:"*?<>|]+')


def _safe_id(raw: str) -> str:
    """净化 doc_id 为安全文件名（去路径分隔符等）。

    注意：截断到 80 字符后必须再 strip 一次，否则截断点恰好在空格处
    会导致文件名末尾残留空格（Windows/POSIX 表现不一，且与 CSV 不一致）。
    """
    return _FILENAME_UNSAFE.sub("_", raw).strip("_ ")[:80].rstrip("_ ")


COMPETITION_KEYWORDS = {
    "CUMCM": ["国赛", "CUMCM", "全国大学生"],
    "MCM/ICM": ["MCM", "ICM", "美赛", "O奖", "COMAP"],
    "APMCM": ["APMCM", "亚太"],
    "MathorCup": ["MathorCup", "数学建模挑战赛"],
    "华为杯": ["华为杯", "研究生"],
    "华数杯": ["华数杯"],
    "深圳杯": ["深圳杯"],
    "电工杯": ["电工杯"],
    "五一赛": ["五一", "五一建模", "五一赛"],
}


def detect_competition(path: str) -> str:
    for comp, keywords in COMPETITION_KEYWORDS.items():
        if any(k in path for k in keywords):
            return comp
    return "未知"


def parse_meta(pdf_path: Path) -> dict:
    """从路径解析 year/problem/competition/award。"""
    s = str(pdf_path)
    year_m = YEAR_RE.search(pdf_path.name) or YEAR_RE.search(s)
    year = year_m.group(1) if year_m else ""
    prob_m = PROBLEM_RE.search(pdf_path.name) or PROBLEM_RE.search(s)
    problem = prob_m.group(1).upper() if prob_m else ""
    competition = detect_competition(s)
    award = "O奖" if ("O奖" in s or "Outstanding" in s) else ("优秀" if "优秀" in s else "")
    return {"year": year, "problem": problem, "competition": competition, "award": award}


def pdf_to_md(pdf_path: Path) -> str:
    """pdfplumber 提取文本 → 简易 md。"""
    try:
        import pdfplumber
    except ImportError:
        return f"[转换失败：缺 pdfplumber] {pdf_path.name}"
    parts: list[str] = [f"# {pdf_path.stem}\n"]
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                txt = page.extract_text() or ""
                if txt.strip():
                    parts.append(f"\n## 第 {i} 页\n\n{txt}\n")
    except Exception as e:
        parts.append(f"\n[PDF 解析异常: {e}]\n")
    return "\n".join(parts)


def docx_to_md(docx_path: Path) -> str:
    """python-docx 提取段落 → md。"""
    try:
        import docx
    except ImportError:
        return f"[转换失败：缺 python-docx] {docx_path.name}"
    parts: list[str] = [f"# {docx_path.stem}\n"]
    try:
        doc = docx.Document(str(docx_path))
        for para in doc.paragraphs:
            t = para.text.strip()
            if t:
                style = (para.style.name or "").lower()
                if "heading 1" in style:
                    parts.append(f"\n# {t}\n")
                elif "heading" in style:
                    parts.append(f"\n## {t}\n")
                else:
                    parts.append(t + "\n")
    except Exception as e:
        parts.append(f"\n[docx 解析异常: {e}]\n")
    return "\n".join(parts)


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="优秀论文 → md 批量转换")
    p.add_argument("--roots", nargs="*", default=None, help="覆盖默认语料根列表")
    p.add_argument("--limit", type=int, default=0, help="只转前 N 个（0=全部）")
    args = p.parse_args()

    roots = [Path(r) for r in (args.roots or DEFAULT_ROOTS)]
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    targets: list[Path] = []
    missing: list[str] = []
    for root in roots:
        if not root.exists():
            missing.append(str(root))
            continue
        for ext in ("*.pdf", "*.docx"):
            targets.extend(root.rglob(ext))
    targets = sorted(set(targets))
    if missing:
        print(f"[convert] 跳过不存在的根: {missing}")
    if not targets:
        print("[convert] 未找到任何 PDF/docx")
        return 1
    if args.limit:
        targets = targets[: args.limit]

    print(f"[convert] 扫描 {len(roots)} 个语料根，待转换 {len(targets)} 个文件 → {PAPERS_DIR}")
    rows: list[dict] = []
    ok = skip = fail = 0
    for i, src in enumerate(targets, 1):
        meta = parse_meta(src)
        doc_id = _safe_id(f"{meta['year']}_{meta['competition']}_{meta['problem']}_{src.stem}")
        out = PAPERS_DIR / f"{doc_id}.md"
        if out.exists() and out.stat().st_size > 50:
            skip += 1
            rows.append({
                "doc_id": doc_id,
                "year": int(meta["year"] or 0),
                "problem": meta["problem"],
                "problem_id": meta["problem"],
                "competition": meta["competition"],
                "award": meta["award"],
                "path": str(out.relative_to(DATA_DIR.parent)).replace("\\", "/"),
            })
            continue
        try:
            md = pdf_to_md(src) if src.suffix.lower() == ".pdf" else docx_to_md(src)
            out.write_text(md, encoding="utf-8")
            ok += 1
            rows.append({
                "doc_id": doc_id,
                "year": int(meta["year"] or 0),
                "problem": meta["problem"],
                "problem_id": meta["problem"],
                "competition": meta["competition"],
                "award": meta["award"],
                "path": str(out.relative_to(DATA_DIR.parent)).replace("\\", "/"),
            })
        except Exception as e:
            fail += 1
            print(f"  FAIL {src.name}: {e}", flush=True)
        if i % 20 == 0:
            print(f"  {i}/{len(targets)}  ok={ok} skip={skip} fail={fail}", flush=True)

    # 写 papers.csv
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CSV_FILE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id", "year", "problem", "problem_id", "competition", "award", "path"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"\n[convert] DONE  ok={ok} skip={skip} fail={fail}  → {CSV_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())