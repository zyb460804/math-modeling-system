#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""公式/图表 OCR（Pix2Text）— 从赛题 PDF/图片提取公式为 LaTeX。

融合自 breezedeus/Pix2Text（3195★）。赛题 PDF 常把公式渲染成图片或矢量图，
人工抄录易错；Pix2Text 自动识别输出 LaTeX，可直接进论文。

能力：
  - 图片公式 → LaTeX（image2latex）
  - PDF 整页布局识别（含公式/表格/插图）→ Markdown
  - 截屏/剪贴板 → LaTeX

用法：
  python extract_formulas_ocr.py --img formula.png
  python extract_formulas_ocr.py --pdf problem_files/赛题.pdf --pages 1-3
产出：stdout 打印 LaTeX + 写入 paper_output/code/formulas_ocr.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass


def ocr_image(img_path: Path) -> str:
    from pix2text import Pix2Text  # type: ignore
    p2t = Pix2Text.from_config()
    result = p2t.recognize(str(img_path))
    # result 可能是 str / dict / Layout 对象
    if isinstance(result, str):
        return result
    if hasattr(result, "to_markdown"):
        return result.to_markdown("md")
    if isinstance(result, dict):
        return result.get("latex") or result.get("text") or str(result)
    return str(result)


def ocr_pdf(pdf_path: Path, pages: str) -> list[dict]:
    from pix2text import Pix2Text  # type: ignore
    p2t = Pix2Text.from_config()
    out: list[dict] = []
    for pg in _expand_pages(pages):
        try:
            result = p2t.recognize_page(str(pdf_path), page=pg)
            md = result.to_markdown("md") if hasattr(result, "to_markdown") else str(result)
            # 抽取公式块（$$...$ 或 $...$）
            formulas = _extract_latex(md)
            out.append({"page": pg, "markdown": md[:500], "formulas": formulas})
        except Exception as e:
            out.append({"page": pg, "error": str(e)[:200]})
    return out


def _expand_pages(pages: str) -> list[int]:
    if pages.lower() == "all":
        return []  # 调用方自行处理
    out: list[int] = []
    for part in pages.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def _extract_latex(md: str) -> list[str]:
    import re
    # 块公式 $$...$$ 与行内 $...$
    formulas = re.findall(r"\$\$([^$]+)\$\$", md)
    formulas += re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", md)
    return [f.strip() for f in formulas if f.strip()]


def main() -> int:
    p = argparse.ArgumentParser(description="公式 OCR（Pix2Text）")
    p.add_argument("--img", help="单张公式图片")
    p.add_argument("--pdf", help="PDF 文件")
    p.add_argument("--pages", default="1", help="PDF 页码（仅 --pdf 时）")
    args = p.parse_args()

    if not args.img and not args.pdf:
        p.print_help()
        return 2

    try:
        import pix2text  # type: ignore  # noqa: F401
    except ImportError:
        print(
            "[ocr] 未安装 pix2text。安装：\n"
            "  pip install pix2text\n"
            "  首次运行会下载模型（~数百 MB），设 HF_ENDPOINT=https://hf-mirror.com 加速",
            file=sys.stderr,
        )
        return 2

    results: dict = {}
    if args.img:
        img_path = Path(args.img)
        if not img_path.exists():
            sys.exit(f"[ocr] 图片不存在: {img_path}")
        latex = ocr_image(img_path)
        print(f"[ocr] LaTeX:\n{latex}\n")
        results = {"type": "image", "input": str(img_path), "latex": latex}
    else:
        pdf_path = Path(args.pdf)  # type: ignore
        if not pdf_path.exists():
            sys.exit(f"[ocr] PDF 不存在: {pdf_path}")
        pages_results = ocr_pdf(pdf_path, args.pages)
        print(f"[ocr] PDF {pdf_path.name} 共 {len(pages_results)} 页：\n")
        for pg in pages_results:
            print(f"=== 第 {pg['page']} 页 ===")
            if "error" in pg:
                print(f"  [错误] {pg['error']}")
            else:
                print(f"  公式数: {len(pg['formulas'])}")
                for f in pg["formulas"][:5]:
                    print(f"    ${f}$")
        results = {"type": "pdf", "input": str(pdf_path), "pages": pages_results}

    out_file = Path("paper_output/code/formulas_ocr.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[ocr] 明细 → {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())