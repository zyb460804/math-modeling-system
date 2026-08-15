#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G4.7 实物门（Artifact Gate）：检查最终交付物实物，防止"占位符论文/空结果文件/无代码"带病交付。

背景：2026-08 实测发现 B 题作品 final_paper.docx 表格实体为 0、result1/result2.xlsx 为空表头、
无代码、摘要与正文数字矛盾，而原证据门只查 paper_output 下的 JSON 索引，全部漏检。
本脚本对任意作品目录做客观实物检查，不依赖模型自觉。

用法：
    python paper_artifact_check.py --paper-dir <作品目录>
    python paper_artifact_check.py --paper-dir C:/Users/xxx/Desktop/测试

退出码：0 = 通过（无 failures）；1 = 有 failures（不得宣称可提交）。
报告：默认 <作品目录>/qa/artifact_check_report.json + .md（也可 --report 指定）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PLACEHOLDER_MARKERS = [
    "【待补", "待补充", "待补", "TODO", "TBD", "XXX", "占位",
    "（结果如下表所示）", "（数据待补）", "此处插入",
    "**表1", "**表 1", "**表2", "**表 2", "如下表所示：", "如下表所示:",
]

UNIT_RE = re.compile(r"\d+(?:\.\d+)?")


def docx_stats(path: Path) -> dict:
    """纯标准库解析 docx（zip+xml）：表格实体、图片数、段落文本。"""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    except Exception as exc:
        return {"error": str(exc), "tables": [], "drawings": 0, "paragraph_text": []}
    drawings = len(re.findall(r"<w:drawing[ />]", xml))  # [ />] 同时覆盖 <w:drawing/> 自闭合形态
    tables = []
    for m in re.finditer(r"<w:tbl>.*?</w:tbl>", xml, re.S):
        cells = re.findall(r"<w:tc>.*?</w:tc>", m.group(0), re.S)
        rows_txt = []
        for c in cells:
            txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", c, re.S))
            rows_txt.append(txt.strip())
        nonempty = [r for r in rows_txt if r]
        if nonempty:
            tables.append(nonempty)
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)).strip()
        if txt:
            paras.append(txt)
    return {"error": None, "tables": tables, "drawings": drawings, "paragraph_text": paras}


def xlsx_has_data(path: Path, min_values: int = 5, header_rows: int = 2, header_cols: int = 2) -> tuple[bool, str]:
    """纯标准库解析 xlsx 第一个 sheet，排除表头行/列后判断数据区是否有真实值。

    背景：2026-08 实测 result1.xlsx 有 15 个非空单元格但全部是表头（距离标签+中心水深70），
    原实现把表头当数据，漏检了"空结果文件"。header_rows/header_cols 默认排除前 2 行 2 列。"""
    try:
        with zipfile.ZipFile(path) as z:
            sheet_names = [n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)]
            if not sheet_names:
                return False, "未找到 worksheet"
            sheet = z.read(sheet_names[0]).decode("utf-8", errors="replace")
            shared = ""
            if "xl/sharedStrings.xml" in z.namelist():
                shared = z.read("xl/sharedStrings.xml").decode("utf-8", errors="replace")
        cells = re.findall(r'<c r="([A-Z]+\d+)"[^>]*?(?:t="(\w+)")?[^>]*>(?:<v>(.*?)</v>)?(?:<is>.*?</is>)?', sheet, re.S)
        values: list[str] = []
        for ref, t, v in cells:
            # 排除表头区：行 <= header_rows 或 列 <= header_cols
            m = re.match(r"([A-Z]+)(\d+)", ref)
            if not m:
                continue
            col = 0
            for ch in m.group(1):
                col = col * 26 + (ord(ch) - 64)
            row = int(m.group(2))
            if row <= header_rows or col <= header_cols:
                continue
            if not v:
                continue
            if t == "s" and shared:
                try:
                    idx = int(float(v))
                except ValueError:
                    continue
                sis = re.findall(r"<si>.*?</si>", shared, re.S)
                if 0 <= idx < len(sis):
                    txt = "".join(re.findall(r"<t[^>]*>(.*?)</t>", sis[idx], re.S))
                    values.append(txt)
            else:
                values.append(v)
        nonempty = [x for x in values if x.strip()]
        return len(nonempty) >= min_values, f"非空单元格 {len(nonempty)} 个（最少要求 {min_values}）"
    except Exception as exc:
        return False, f"解析失败: {exc}"


def check_artifacts(paper_dir: Path, require_table: bool = True, require_figures: bool = True) -> tuple[list[str], list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not paper_dir.exists():
        return [f"作品目录不存在: {paper_dir}"], [], []

    files = [f for f in paper_dir.rglob("*") if f.is_file()]
    # 归档/沙箱/缓存目录不参与终检（防占位 docx 触发假 FAIL；仅匹配目录段，不影响同名文件）
    files = [
        f for f in files
        if not any(
            p == "__pycache__" or p == ".git" or p.startswith(("_archive", "_fixtest"))
            for p in f.relative_to(paper_dir).parts[:-1]
        )
    ]
    docx_files = [f for f in files if f.suffix.lower() == ".docx" and "~$" not in f.name and "backup" not in f.name.lower()]
    top_docx = [f for f in docx_files if f.parent == paper_dir]
    deep_docx = [f for f in docx_files if f.parent != paper_dir]
    result_xlsx = [f for f in files if f.suffix.lower() == ".xlsx" and re.search(r"result", f.name, re.I)]
    all_xlsx = [f for f in files if f.suffix.lower() == ".xlsx"]
    code_files = [f for f in files if f.suffix.lower() in (".py", ".m", ".r", ".ipynb", ".java", ".jl")]
    fig_files = [f for f in files if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg", ".gif")]

    # 1) 论文 docx 实物（主交付物 = paper_dir 顶层 docx；顶层为空时回退子目录。
    #    顶层已有主交付物时，子目录 docx 仅登记不判定——归档/沙箱/其他赛题工作
    #    目录里的同名占位 docx 不再触发"表格实体数为 0"假 FAIL）
    def _rel(d: Path) -> str:
        try:
            return str(d.relative_to(paper_dir))
        except ValueError:
            return d.name

    if not docx_files:
        failures.append("未找到论文 docx 文件")
    else:
        for d in (top_docx if top_docx else deep_docx):
            st = docx_stats(d)
            if st["error"]:
                failures.append(f"{_rel(d)}: docx 解析失败 {st['error']}")
                continue
            n_tables = len(st["tables"])
            info.append(f"{_rel(d)}: 表格实体 {n_tables} 个 / 图片 {st['drawings']} 张 / 段落 {len(st['paragraph_text'])} 段")
            if require_table and n_tables == 0:
                failures.append(f"{_rel(d)}: 表格实体数为 0 —— 题面要求的结果表/符号表在正文中不存在（只有文字占位）")
            elif n_tables < 2:
                warnings.append(f"{_rel(d)}: 表格实体仅 {n_tables} 个，核对题面要求的表1/表2/符号说明表是否齐全")
            if st["drawings"] == 0:
                warnings.append(f"{_rel(d)}: 全文无图片（计算/几何类题目建议至少 2~4 张图，图为得分载体）")
            text = "\n".join(st["paragraph_text"])
            for marker in PLACEHOLDER_MARKERS:
                if marker in text:
                    warnings.append(f"{_rel(d)}: 发现模板/占位残留「{marker}」——最终稿不得保留")
            # 数字一致性线索：提取正文数字
            nums = UNIT_RE.findall(text)
            info.append(f"{_rel(d)}: 正文共提取 {len(nums)} 个数字")

        # 子目录 docx（顶层已有主交付物）：仅登记，不参与终检判定
        if top_docx:
            for d in deep_docx:
                st = docx_stats(d)
                tag = f"{_rel(d)}: 子目录文档（不参与终检判定）"
                if st["error"]:
                    info.append(f"{tag} 解析失败 {st['error']}")
                else:
                    info.append(f"{tag} 表格实体 {len(st['tables'])} 个 / 图片 {st['drawings']} 张 / 段落 {len(st['paragraph_text'])} 段")

    # 2) 结果 xlsx 非空
    if result_xlsx:
        for x in result_xlsx:
            ok, msg = xlsx_has_data(x)
            if ok:
                info.append(f"{x.name}: {msg}")
            else:
                failures.append(f"{x.name}: 结果文件为空或只有表头（{msg}）——题目要求结果保存到此文件")
    else:
        if all_xlsx:
            warnings.append("未找到 result*.xlsx 命名结果文件（若题目要求输出结果文件，需按题面命名）")
        else:
            warnings.append("作品目录无任何 xlsx 结果文件")

    # 3) 代码存在性（可复现）
    if not code_files:
        failures.append("作品目录无任何代码文件（.py/.m/.R 等）——不可复现，附录声称的代码无法核实")

    # 4) 图（P1-7 幽灵链收口配套：require_figures 场景无图 = FAIL 而非 warning——
    #    论文图是结果证据载体，索引/正文可伪造，磁盘无图实物即不可交付；
    #    确无图需求时用 --no-require-figures 显式豁免，不做静默降级）
    if require_figures and not fig_files:
        failures.append("作品目录无任何图片文件（require_figures 场景）——论文图是结果证据载体，无图实物即幽灵链风险；确无图需求请用 --no-require-figures 显式豁免")

    return failures, warnings, info


def main() -> int:
    ap = argparse.ArgumentParser(description="G4.7 实物门：检查论文/结果文件/代码实物是否齐全")
    ap.add_argument("--paper-dir", default="paper_output", help="作品目录（支持桌面等任意位置）")
    ap.add_argument("--report", default="", help="报告 json 路径（默认 <paper-dir>/qa/artifact_check_report.json）")
    ap.add_argument("--no-require-table", action="store_true", help="不强制表格实体存在")
    ap.add_argument("--no-require-figures", action="store_true", help="不强制图片存在")
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir)
    failures, warnings, info = check_artifacts(
        paper_dir, require_table=not args.no_require_table, require_figures=not args.no_require_figures
    )

    report = {
        "gate": "G4.7_ARTIFACT_GATE",
        "status": "FAIL" if failures else "PASS",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper_dir": str(paper_dir.resolve()),
        "failures": failures,
        "warnings": warnings,
        "info": info,
    }
    report_path = Path(args.report) if args.report else paper_dir / "qa" / "artifact_check_report.json"
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path = report_path.with_suffix(".md")
        md_lines = ["# G4.7 实物门报告", "", f"- 目录: `{report['paper_dir']}`", f"- 状态: `{report['status']}`", ""]
        if failures:
            md_lines.append("## Failures（阻断）")
            md_lines += [f"- {f}" for f in failures]
        if warnings:
            md_lines.append("## Warnings")
            md_lines += [f"- {w}" for w in warnings]
        md_lines += ["", "## Info", ""]
        md_lines += [f"- {i}" for i in info]
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"[artifact-gate] 报告写入失败: {exc}")

    print("═" * 56)
    print(f"  G4.7 实物门: {'✅ PASS' if not failures else '❌ FAIL'}")
    print("═" * 56)
    for i in info:
        print(f"  · {i}")
    for w in warnings:
        print(f"  ⚠ {w}")
    for f in failures:
        print(f"  ✗ {f}")
    print(f"  报告: {report_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

