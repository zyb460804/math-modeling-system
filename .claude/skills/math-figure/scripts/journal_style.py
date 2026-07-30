#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SciencePlots 期刊风样式助手 — 一行让 matplotlib 出 IEEE/Nature/Science 期刊风图表。

融合自 garrettj404/SciencePlots（~5k★）。数模论文图表"看起来专不专业"直接影响
评委第一印象；SciencePlots 提供各期刊/学术风格的预设样式。

内置样式：
  - ieee / nature / science / science_nature
  - notebook / grid / high-vis / bright / vibrant / muted / retro
  - 中文支持：cn（自动用 SimHei/SimSun，不乱码）

用法（两种）：
  1. CLI 调用（生成样式名清单 + 示例图）：
     python journal_style.py list
     python journal_style.py demo --style nature --out paper_output/figures/style_demo.png
  2. 在绘图脚本里直接用：
     import scienceplots  # 注册样式
     import matplotlib.pyplot as plt
     plt.style.use(["science", "ieee", "no-latex"])  # 组合多个
"""
from __future__ import annotations

import argparse
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# 推荐样式组合（按数模场景）
RECOMMENDED = {
    "通用学术": ["science", "no-latex"],
    "IEEE 风": ["science", "ieee", "no-latex"],
    "Nature 风": ["science", "nature", "no-latex"],
    "中文论文": ["science", "no-latex", "cn"],  # cn 解决中文乱码
    "高对比": ["science", "high-vis", "no-latex"],
    "答辩高亮": ["science", "vibrant", "no-latex"],
}


def cmd_list() -> int:
    try:
        import scienceplots  # type: ignore  # noqa: F401
        import matplotlib.pyplot as plt
    except ImportError:
        print("[style] 未安装。pip install SciencePlots", file=sys.stderr)
        return 2
    available = sorted(plt.style.available)
    print("[style] 可用样式：")
    for s in available:
        print(f"  {s}")
    print("\n[style] 数模推荐组合：")
    for name, combo in RECOMMENDED.items():
        print(f"  {name:<8} → plt.style.use({combo})")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    try:
        import scienceplots  # type: ignore  # noqa: F401
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[style] 未安装。pip install SciencePlots matplotlib numpy", file=sys.stderr)
        return 2
    combo = RECOMMENDED.get(args.style) or [args.style]
    plt.style.use(combo)
    fig, ax = plt.subplots(figsize=(5, 3.2))
    x = np.linspace(0, 5, 200)
    for k in [1, 2, 3]:
        ax.plot(x, np.sin(k * x), label=f"y=sin({k}x)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Style: {args.style}")
    ax.legend(title="系列")
    fig.tight_layout()
    out = args.out
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[style] 示例图 → {out}  (样式: {combo})")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="SciencePlots 期刊风样式助手")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("list", help="列出可用样式 + 数模推荐组合")
    sd = sub.add_parser("demo", help="生成示例图")
    sd.add_argument("--style", default="通用学术", choices=list(RECOMMENDED.keys()))
    sd.add_argument("--out", default="paper_output/figures/style_demo.png")
    args = p.parse_args()
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "demo":
        return cmd_demo(args)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())