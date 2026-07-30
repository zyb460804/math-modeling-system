#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""LaTeX 论文编译（2 pass + 失败重试 3 次，解析错误行）。

融合自 AutoMCM-Pro/scripts/compile_pdf.py 的 LaTeX 编译重试机制。
默认跑 2 pass（处理 TOC/引用交叉引用），失败时解析 .log 错误行打印，最多重试 3 次。

用法：
  python compile_latex.py --tex paper_output/latex/main.tex
  python compile_latex.py --tex main.tex --engine xelatex --passes 2
退出码：0=成功  1=编译失败  2=latex 引擎未安装
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

MAX_RETRY = 3
DEFAULT_PASSES = 2


def parse_log_errors(log_file: Path) -> list[str]:
    """从 .log 提取错误行（! Error ... / line N）。"""
    if not log_file.exists():
        return []
    text = log_file.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []
    for m in re.finditer(r"^! (.+)$", text, re.MULTILINE):
        errors.append(m.group(1).strip())
    for m in re.finditer(r"l\.(\d+)\s*(.*)", text):
        errors.append(f"line {m.group(1)}: {m.group(2).strip()}")
    return errors[:10]


def compile_once(tex: Path, engine: str, out_dir: Path) -> tuple[bool, str]:
    """单次编译，返回 (成功, stderr/log 摘要)。"""
    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
           f"-output-directory={out_dir}", str(tex)]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace", cwd=str(tex.parent),
        )
    except FileNotFoundError:
        return False, f"{engine} 未安装"
    log_file = out_dir / (tex.stem + ".log")
    errs = parse_log_errors(log_file)
    if proc.returncode == 0 and not errs:
        return True, ""
    return False, "\n".join(errs) or (proc.stderr or proc.stdout)[-400:]


def main() -> int:
    p = argparse.ArgumentParser(description="LaTeX 编译（2 pass + 重试）")
    p.add_argument("--tex", required=True, help=".tex 文件路径")
    p.add_argument("--engine", default="xelatex", choices=["xelatex", "pdflatex", "latexmk"])
    p.add_argument("--passes", type=int, default=DEFAULT_PASSES)
    p.add_argument("--out-dir", default=None, help="输出目录（默认 .tex 同级 build/）")
    args = p.parse_args()

    tex = Path(args.tex).resolve()
    if not tex.exists():
        sys.exit(f"[latex] .tex 不存在: {tex}")
    out_dir = Path(args.out_dir) if args.out_dir else tex.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = args.engine
    if not shutil.which(engine):
        print(f"[latex] ✗ {engine} 未安装。可选：xelatex / pdflatex / latexmk（MiKTeX/TeX Live）")
        return 2

    pdf = out_dir / (tex.stem + ".pdf")
    last_err = ""
    for attempt in range(1, MAX_RETRY + 1):
        print(f"[latex] 第 {attempt}/{MAX_RETRY} 轮（每轮 {args.passes} pass）…")
        ok = True
        for ps in range(1, args.passes + 1):
            print(f"  pass {ps}/{args.passes}")
            ok, last_err = compile_once(tex, engine, out_dir)
            if not ok:
                break
        if ok and pdf.exists():
            print(f"[latex] ✓ 编译成功 → {pdf}")
            return 0
        print(f"[latex] 失败：\n{last_err}\n")
    print(f"[latex] ✗ {MAX_RETRY} 轮均失败。常见原因：缺图、包未装、公式语法错。")
    print(f"[latex] 完整日志：{out_dir / (tex.stem + '.log')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())