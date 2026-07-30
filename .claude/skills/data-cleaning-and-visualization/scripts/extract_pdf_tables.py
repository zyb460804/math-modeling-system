#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PDF 表格提取（Camelot）— 把赛题附件里的数据表一键转 CSV/Excel。

融合自 atlanhq/camelot（3716★）。数模赛题 PDF 常含附表（成分表、负荷数据、
参数表等），人工抠表易错且慢；Camelot 自动识别表格结构输出 DataFrame。

两种模式：
  - lattice  ：带网格线的表格（精确，依赖 ghostscript）
  - stream   ：无网格线表格（依赖文字对齐推断）

用法：
  python extract_pdf_tables.py --pdf problem_files/赛题.pdf
  python extract_pdf_tables.py --pdf 赛题.pdf --pages 1-5 --mode lattice
  python extract_pdf_tables.py --pdf 赛题.pdf --out paper_output/code/data/
产出：每页每表一个 CSV + 一个汇总 Excel + tables_index.json
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


def main() -> int:
    p = argparse.ArgumentParser(description="PDF 表格提取（Camelot）")
    p.add_argument("--pdf", required=True, help="PDF 文件路径")
    p.add_argument("--pages", default="all", help="页码，如 1-5 或 all（默认 all）")
    p.add_argument("--mode", default="lattice", choices=["lattice", "stream"],
                   help="lattice=带网格线表格；stream=无网格线（默认 lattice）")
    p.add_argument("--out", default="paper_output/code/data", help="输出目录")
    args = p.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"[extract] PDF 不存在: {pdf_path}")

    try:
        import camelot  # type: ignore
    except ImportError:
        print(
            "[extract] 未安装 camelot。安装：\n"
            "  pip install camelot-py[cv]\n"
            "  另需 Ghostscript（lattice 模式）：winget install Ghostscript.Ghostscript\n"
            "  或 base 版：pip install camelot-py（仍需 ghostscript）",
            file=sys.stderr,
        )
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[extract] {pdf_path.name} | mode={args.mode} | pages={args.pages}")
    tables = camelot.read_pdf(str(pdf_path), pages=args.pages, flavor=args.mode)
    print(f"[extract] 识别到 {len(tables)} 个表格")

    index: list[dict] = []
    for i, t in enumerate(tables):
        df = t.df
        csv_path = out_dir / f"table_{i + 1}_p{t.page}_acc{t.accuracy:.2f}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        index.append({
            "table": i + 1,
            "page": int(t.page),
            "rows": int(df.shape[0]),
            "cols": int(df.shape[1]),
            "accuracy": round(float(t.accuracy), 3),
            "parsing_report": t.parsing_report,
            "csv": str(csv_path).replace("\\", "/"),
            "preview": df.head(3).to_dict("records"),
        })
        print(f"  表 {i + 1}（第 {t.page} 页，{df.shape[0]}×{df.shape[1]}，精度 {t.accuracy:.2f}）→ {csv_path.name}")

    # 汇总 Excel
    try:
        xlsx_path = out_dir / "tables_summary.xlsx"
        with __import__("pandas").ExcelWriter(xlsx_path) as writer:
            for i, t in enumerate(tables):
                t.df.to_excel(writer, sheet_name=f"table_{i + 1}", index=False)
        print(f"[extract] 汇总 Excel → {xlsx_path}")
    except Exception as e:
        print(f"[extract] Excel 汇总跳过: {e}")

    index_path = out_dir / "tables_index.json"
    index_path.write_text(
        json.dumps({"pdf": str(pdf_path), "mode": args.mode, "count": len(tables), "tables": index},
                   ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"[extract] 索引 → {index_path}")
    return 0 if tables else 1


if __name__ == "__main__":
    sys.exit(main())