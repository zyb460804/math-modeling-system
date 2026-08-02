#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G4.10 图片嵌入门 — 论文 Word 是否真的嵌入了图片（v4.7）

背景：2026-08 实测 2023 国赛 B 题踩坑——final_paper_source.md 里只写了
"见图 4"等纯文字引用，没用 markdown 图片语法 ![](path)，pandoc 转 Word 后
0 张图。而 check_paper_format.py 只在 figure_index.json 存在时才检查图片数，
若 figure_index.json 缺失或后建，该门禁会跳过，导致"无图 Word"漏检。

本门禁独立检查，不依赖 figure_index.json：
  1. 论文 Markdown 源稿里的 ![](path) 语法数 = N_md
  2. Word 文件里 word/media/* 内嵌图片数 = N_docx
  3. 判定：
     - N_md > 0 且 N_docx == 0  → FAIL（CRITICAL，pandoc 路径错或语法错）
     - N_md == 0 且 N_docx == 0  → FAIL（CRITICAL，论文 0 图）
     - N_md > N_docx             → WARN（部分图丢失）
     - N_md == N_docx > 0        → PASS

用法：
    python image_embed_check.py                              # 默认 paper_output/
    python image_embed_check.py --paper-dir C:/xxx/作品目录
    python image_embed_check.py --paper-dir paper_output --md final_paper_source.md --docx final_paper.docx

退出码：0 = PASS；1 = FAIL；2 = WARN（仅警告，不阻断）。
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Markdown 图片语法：![alt](path "title") 或 ![alt](path)
# 不匹配代码块里的 [文字](文字) 等无关链接（要求 ! 前缀）
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")


def count_md_images(md_path: Path) -> tuple[int, list[str]]:
    """统计 Markdown 文件中的图片引用数。返回 (数量, 路径列表)。"""
    if not md_path.exists():
        return -1, []
    text = md_path.read_text(encoding="utf-8", errors="replace")
    # 去除代码块（```...```）里的内容，避免误判
    text = re.sub(r"```[\s\S]*?```", "", text)
    matches = MD_IMAGE_RE.findall(text)
    paths = []
    for m in matches:
        # 提取括号里的路径
        m_path = re.search(r"\]\(([^)\s]+)", m)
        if m_path:
            paths.append(m_path.group(1))
    return len(matches), paths


def count_docx_images(docx_path: Path) -> tuple[int, list[str]]:
    """统计 Word 文件中实际嵌入的图片数。返回 (数量, 媒体文件名列表)。

    内嵌图片在 docx zip 的 word/media/ 目录下。
    """
    if not docx_path.exists():
        return -1, []
    try:
        with zipfile.ZipFile(docx_path) as z:
            media = [n for n in z.namelist() if n.startswith("word/media/")]
            return len(media), media
    except (zipfile.BadZipFile, OSError) as e:
        print(f"[ERROR] 无法读取 docx: {e}", file=sys.stderr)
        return -1, []


def check(paper_dir: Path, md_name: str, docx_name: str) -> tuple[str, list[str], list[str]]:
    """返回 (status, failures, warnings)。status ∈ {'PASS','FAIL','WARN'}。"""
    failures: list[str] = []
    warnings: list[str] = []

    md_path = paper_dir / md_name
    docx_path = paper_dir / docx_name

    # 兼容：若指定名字找不到，自动扫描 paper_dir 下的 .md 和 .docx
    if not md_path.exists():
        mds = sorted(paper_dir.glob("*.md"))
        mds = [m for m in mds if "source" in m.name or "paper" in m.name or "final" in m.name]
        if mds:
            md_path = mds[0]
    if not docx_path.exists():
        docxs = sorted(paper_dir.glob("*.docx"))
        docxs = [d for d in docxs if "final" in d.name or "paper" in d.name]
        if docxs:
            docx_path = docxs[0]

    n_md, md_paths = count_md_images(md_path)
    n_docx, docx_media = count_docx_images(docx_path)

    print(f"  Markdown 源稿: {md_path.name if md_path.exists() else '(未找到)'}")
    print(f"    ![](path) 语法数 N_md = {n_md}")
    if md_paths:
        for p in md_paths[:5]:
            print(f"      - {p}")
        if len(md_paths) > 5:
            print(f"      ... 共 {len(md_paths)} 个")
    print(f"  Word 文件: {docx_path.name if docx_path.exists() else '(未找到)'}")
    print(f"    内嵌图片数 N_docx = {n_docx}")

    # 判定逻辑
    if n_md < 0 and n_docx < 0:
        failures.append(f"未找到 Markdown 源稿（{md_name}）和 Word 文件（{docx_name}）")
    elif n_md < 0:
        failures.append(f"未找到 Markdown 源稿：{md_path}")
    elif n_docx < 0:
        failures.append(f"Word 文件无法读取或不是合法 docx：{docx_path}")
    elif n_md > 0 and n_docx == 0:
        failures.append(
            f"CRITICAL：Markdown 有 {n_md} 个图片引用 ![](path)，但 Word 中 0 张内嵌图片。"
            f"常见原因：① pandoc 运行目录无法解析图片相对路径；② Markdown 用了'见图N'纯文字而非 ![](path) 语法。"
            f"修复：cd {paper_dir} && pandoc {md_path.name} -o {docx_path.name} --resource-path=."
        )
    elif n_md == 0 and n_docx == 0:
        failures.append(
            "CRITICAL：论文 Markdown 与 Word 均无图片。正式论文不可能 0 图——"
            "请在正文对应位置添加 ![图N 标题](figures/xxx.png) 语法。"
        )
    elif n_md > n_docx:
        warnings.append(
            f"WARN：Markdown 有 {n_md} 个图片引用，但 Word 仅嵌入 {n_docx} 张，"
            f"可能有 {n_md - n_docx} 张图片路径错误或文件缺失。"
        )
    elif n_md == 0 and n_docx > 0:
        # Word 有图但 md 源稿没有 ![](path)——可能是直接用 python-docx 写入的图
        warnings.append(f"WARN：Word 有 {n_docx} 张图但 Markdown 源稿无 ![](path) 语法（可能是程序直接写入）")
    else:
        # n_md >= 0 and n_docx > 0 and n_md <= n_docx
        print(f"  ✅ Word 内嵌 {n_docx} 张图，Markdown 引用 {n_md} 个，一致。")

    if failures:
        return "FAIL", failures, warnings
    if warnings:
        return "WARN", [], warnings
    return "PASS", [], warnings


def main() -> int:
    ap = argparse.ArgumentParser(description="G4.10 图片嵌入门：检查论文 Word 是否真的嵌入了图片")
    ap.add_argument("--paper-dir", type=Path, default=Path("paper_output"), help="作品目录（默认 paper_output/）")
    ap.add_argument("--md", default="final_paper_source.md", help="Markdown 源稿文件名")
    ap.add_argument("--docx", default="final_paper.docx", help="Word 文件名")
    args = ap.parse_args()

    print("=" * 60)
    print("G4.10 图片嵌入门 — 论文 Word 是否真的嵌入了图片")
    print("=" * 60)

    status, failures, warnings = check(args.paper_dir, args.md, args.docx)

    print("\n" + "=" * 60)
    if status == "PASS":
        print("✅ PASS — 图片嵌入正常")
        rc = 0
    elif status == "WARN":
        print("⚠️  WARN — 有警告但不阻断：")
        for w in warnings:
            print(f"  - {w}")
        rc = 2
    else:
        print("❌ FAIL — 图片嵌入异常，必须修复：")
        for f in failures:
            print(f"  - {f}")
        for w in warnings:
            print(f"  - (附加) {w}")
        rc = 1
    print("=" * 60)

    # 写报告
    report = {
        "gate": "G4.10",
        "status": status,
        "paper_dir": str(args.paper_dir),
        "failures": failures,
        "warnings": warnings,
    }
    report_path = args.paper_dir / "qa" / "image_embed_check_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json_module_dumps(report), encoding="utf-8"
    )
    print(f"报告：{report_path}")
    return rc


def json_module_dumps(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    sys.exit(main())
