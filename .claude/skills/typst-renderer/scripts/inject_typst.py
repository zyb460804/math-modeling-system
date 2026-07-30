#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Markdown → Typst 注入 + 编译（带重试）。

融合自 jihe520/MathModelAgent 的 Typst 交付链路。
流程：选模板 → 复制到工作区 → md 转 typst 内联 → 编译 PDF（失败重试 3 次）

用法：
  python inject_typst.py                                  # 默认：source=final_paper_source.md, 模板自动选
  python inject_typst.py --source paper_output/final_paper_source.md
  python inject_typst.py --template zh/cumcm --lang zh
  python inject_typst.py --compile-only                   # 仅编译已有 main.typ
退出码：0=成功  1=编译失败  2=typst CLI 未安装
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

TEMPLATES_ROOT = Path("e:/数学建模/resources/15_Typst模板")
WORK_DIR = Path("paper_output/typst")
SOURCE_MD = Path("paper_output/final_paper_source.md")
PROBLEM_ANALYSIS = Path("paper_output/step1/problem_analysis.json")
OUT_PDF = Path("paper_output/final_paper.pdf")
MAX_COMPILE_RETRY = 3

COMPETITION_TO_TEMPLATE = {
    "CUMCM": ("zh", "cumcm"), "国赛": ("zh", "cumcm"),
    "MCM": ("en", "mcm"), "ICM": ("en", "mcm"), "美赛": ("en", "mcm"),
    "APMCM": ("zh", "apmcm"), "亚太": ("zh", "apmcm"),
    "华数杯": ("zh", "huashubei"), "华为杯": ("zh", "huaweibei"),
    "电工杯": ("zh", "diangongbei"), "五一": ("zh", "wuyibei"),
}


# ── Markdown → Typst 语法转换 ─────────────────────────────────
def latex_math_to_typst(tex: str) -> str:
    """把 LaTeX 数学命令转成 Typst 数学语法（$...$ 内部内容）。
    - \\frac{A}{B} → (A)/(B)；\\sqrt{X} → sqrt(X)
    - \\cos \\sin \\theta \\alpha … → 去反斜杠（Typst 用 cos/sin/theta/alpha）
    - \\cdot → dot.op；\\times → times；\\leq → <=；\\geq → >=；\\neq → !=
    """
    import re as _re
    s = tex
    s = _re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
    s = _re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = _re.sub(r"\\text\{([^{}]*)\}", r'"\1"', s)  # \text{cover} → "cover"
    s = s.replace(r"\cdot", " dot.op ").replace(r"\times", " times ")
    s = s.replace(r"\leq", " <= ").replace(r"\geq", " >= ").replace(r"\neq", " != ")
    s = s.replace(r"\le", " <= ").replace(r"\ge", " >= ")
    # 剩余 \<字母序列> 去反斜杠并加空格分隔（\cos\theta → cos theta，避免连成 costheta）
    s = _re.sub(r"\\([A-Za-z]+)", r"\1 ", s)
    s = _re.sub(r"\s+", " ", s)  # 折叠多空格
    return s


def _convert_math_spans(line: str) -> str:
    """转换一行中的 $...$ 数学内容（块公式已处理，这里处理行内与块内残余）。"""
    import re as _re
    return _re.sub(r"\$([^$]+)\$", lambda m: "$" + latex_math_to_typst(m.group(1)) + "$", line)


def md_to_typst(md: str) -> str:
    """把 Markdown 转成 Typst 语法。"""
    lines = md.split("\n")
    out: list[str] = []
    in_block_math = False
    for line in lines:
        # 块公式 $$...$$
        if line.strip().startswith("$$"):
            content = line.strip().strip("$").strip()
            if content:
                out.append(f"$ {latex_math_to_typst(content)} $")
            else:
                in_block_math = not in_block_math
                out.append("$" if in_block_math else " $")
            continue
        if in_block_math:
            out.append(latex_math_to_typst(line))
            continue
        # 行内公式转换（$...$）
        line = _convert_math_spans(line)
        # 标题
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append("=" * level + " " + m.group(2).strip())
            continue
        # 图片 ![alt](path)
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if m:
            alt, path = m.group(1), m.group(2)
            out.append(f'#figure(image("{path}"), caption: [{alt}])')
            continue
        # 粗体 **x** → *x*
        line = re.sub(r"\*\*([^*]+)\*\*", r"*\1*", line)
        out.append(line)
    return "\n".join(out)


def detect_template(args) -> tuple[str, str]:
    if args.template and args.lang:
        return args.lang, args.template
    if args.template:
        return "zh", args.template
    # 从 problem_analysis.json 自动选
    try:
        pa = json.loads(PROBLEM_ANALYSIS.read_text(encoding="utf-8"))
        comp = str(pa.get("competition") or pa.get("contest") or "").upper()
        for key, (lang, tpl) in COMPETITION_TO_TEMPLATE.items():
            if key.upper() in comp:
                return lang, tpl
    except Exception:
        pass
    return "zh", "default"


def build_main_typ(lang: str, template: str, body_typ: str, title: str) -> None:
    """复制模板目录到工作区，生成内联 body 的 main.typ。"""
    tpl_dir = TEMPLATES_ROOT / lang / template
    if not tpl_dir.exists():
        # 兜底 default
        tpl_dir = TEMPLATES_ROOT / lang / "default"
    if not tpl_dir.exists():
        sys.exit(f"[typst] 模板不存在: {TEMPLATES_ROOT}/{lang}/{template}")
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    shutil.copytree(tpl_dir, WORK_DIR)

    # 读模板 main.typ，只删除 sections/ 的 #include（保留 references.typ 等其它 include，
    # 避免截断 references-cn 等含 include 的函数体），然后把 body 注入到第一个 sections include 处
    main_typ = (tpl_dir / "main.typ").read_text(encoding="utf-8", errors="ignore")
    import re as _re
    sections_inc = _re.compile(r'^#include\("sections/[^"]+"\)\s*$', _re.MULTILINE)
    first_pos = sections_inc.search(main_typ)
    if first_pos:
        head = main_typ[: first_pos.start()]
        tail = sections_inc.sub("", main_typ[first_pos.start():])  # 去 sections include，留尾部 references/appendix
    else:
        head, tail = main_typ, ""
    head = head.replace("[论文标题]", title).replace('"[论文标题]"', f'"{title}"')

    new_main = (
        head.rstrip()
        + "\n\n// ===== 以下为 final_paper_source.md 注入内容 =====\n\n"
        + body_typ
        + "\n\n// ===== 以下为模板尾部（references/appendix 等）=====\n"
        + tail.strip()
        + "\n"
    )
    (WORK_DIR / "main.typ").write_text(new_main, encoding="utf-8")


def compile_pdf() -> int:
    """编译 main.typ → PDF，失败重试 MAX_COMPILE_RETRY 次。"""
    if not shutil.which("typst"):
        print("[typst] ✗ typst CLI 未安装。安装：winget install --id Typst.Typst")
        return 2
    # 用绝对路径，避免 cwd + 相对路径双重解析
    main_abs = str((WORK_DIR / "main.typ").resolve())
    out_abs = str(OUT_PDF.resolve())
    for attempt in range(1, MAX_COMPILE_RETRY + 1):
        print(f"[typst] 编译尝试 {attempt}/{MAX_COMPILE_RETRY}…")
        proc = subprocess.run(
            ["typst", "compile", main_abs, out_abs, "--root", str(WORK_DIR.resolve())],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(WORK_DIR.resolve()),
        )
        if proc.returncode == 0:
            print(f"[typst] ✓ 编译成功 → {OUT_PDF}")
            return 0
        print(f"[typst] 编译失败：\n{proc.stderr or proc.stdout}")
        # 简单自动修正常见错误（下轮重试）
        main_typ = (WORK_DIR / "main.typ").read_text(encoding="utf-8", errors="ignore")
        fixed = main_typ
        # 修未配对的 $（奇数个）
        if fixed.count("$") % 2 != 0:
            fixed += "\n$"
        (WORK_DIR / "main.typ").write_text(fixed, encoding="utf-8")
    print(f"[typst] ✗ {MAX_COMPILE_RETRY} 次重试均失败")
    return 1


def main() -> int:
    p = argparse.ArgumentParser(description="Typst 注入 + 编译")
    p.add_argument("--source", default=str(SOURCE_MD))
    p.add_argument("--template", default=None, help="如 cumcm/mcm/default")
    p.add_argument("--lang", default=None, choices=["zh", "en"])
    p.add_argument("--compile-only", action="store_true")
    p.add_argument("--title", default="数学建模论文")
    args = p.parse_args()

    if not args.compile_only:
        if not Path(args.source).exists():
            sys.exit(f"[typst] 源 md 不存在: {args.source}")
        lang, template = detect_template(args)
        print(f"[typst] 模板: {lang}/{template}")
        md = Path(args.source).read_text(encoding="utf-8", errors="ignore")
        body = md_to_typst(md)
        build_main_typ(lang, template, body, args.title)
        print(f"[typst] 已生成 {WORK_DIR / 'main.typ'}")

    return compile_pdf()


if __name__ == "__main__":
    sys.exit(main())