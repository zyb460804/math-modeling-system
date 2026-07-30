#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""akshare 宏观/金融/行业数据获取 — 国赛 C 题刚需。

融合自 akshare（~10k★，中文金融/宏观经济数据库）。C 题常需 GDP/CPI/股价/行业产量
等宏观或行业数据，手动翻统计局费时；akshare 一行拉取。

覆盖：宏观经济（GDP/CPI/PMI/货币）、股票/基金/期货、行业产量、汇率、利率、
      人口、能源、进出口等。

用法：
  python akshare_fetch.py --list macro            # 列出宏观类可用接口
  python akshare_fetch.py --fetch macro_china_gdp --out paper_output/code/data/
  python akshare_fetch.py --fetch stock_zh_a_hist --kwargs '{"symbol":"000001","period":"daily","start_date":"20230101","end_date":"20240101"}'
产出：CSV + 元数据 JSON
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

# 常用接口分类（方便 --list 查找）
INTERFACE_CATEGORIES = {
    "macro": "宏观经济（GDP/CPI/PMI/货币/利率/汇率/进出口/人口/能源）",
    "stock": "股票（A股/港股/美股/历史行情/财务）",
    "fund": "基金/ETF",
    "futures": "期货/期权",
    "bond": "债券/国债收益率",
    "industry": "行业（产量/产销率/价格指数）",
    "currency": "外汇/汇率",
}


def list_interfaces(category: str) -> int:
    try:
        import akshare as ak  # type: ignore
    except ImportError:
        print("[akshare] 未安装。pip install akshare", file=sys.stderr)
        return 2
    if category == "all":
        print("[akshare] 可用类别：")
        for k, v in INTERFACE_CATEGORIES.items():
            print(f"  {k:<10} {v}")
        return 0
    # 列出该类别常见接口（按名称前缀过滤）
    funcs = [f for f in dir(ak) if f.startswith(f"{category}_") and callable(getattr(ak, f))]
    print(f"[akshare] {category} 类接口（{len(funcs)} 个），前 30：")
    for f in funcs[:30]:
        print(f"  {f}")
    if len(funcs) > 30:
        print(f"  ... 共 {len(funcs)} 个，完整列表见 https://akshare.akfamily.xyz/")
    return 0


def fetch(name: str, kwargs_json: str, out_dir: Path) -> int:
    try:
        import akshare as ak  # type: ignore
        import pandas as pd  # type: ignore
    except ImportError:
        print("[akshare] 未安装。pip install akshare pandas", file=sys.stderr)
        return 2

    func = getattr(ak, name, None)
    if func is None:
        print(f"[akshare] 接口不存在: {name}（用 --list <category> 查可用）", file=sys.stderr)
        return 1

    kwargs = {}
    if kwargs_json:
        try:
            kwargs = json.loads(kwargs_json)
        except json.JSONDecodeError as e:
            print(f"[akshare] --kwargs JSON 解析失败: {e}", file=sys.stderr)
            return 1

    print(f"[akshare] 调 {name}({kwargs})…")
    try:
        df = func(**kwargs)
    except Exception as e:
        print(f"[akshare] 调用失败: {e}", file=sys.stderr)
        return 1

    if df is None or len(df) == 0:
        print(f"[akshare] 返回空数据")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    meta = {
        "interface": name,
        "kwargs": kwargs,
        "rows": int(len(df)),
        "cols": list(df.columns) if hasattr(df, "columns") else [],
        "csv": str(csv_path).replace("\\", "/"),
        "preview": df.head(3).to_dict("records") if hasattr(df, "head") else [],
    }
    (out_dir / f"{name}_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(f"[akshare] {len(df)} 行 × {len(df.columns)} 列 → {csv_path}")
    print(f"[akshare] 元数据 → {out_dir / (name + '_meta.json')}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="akshare 宏观/金融数据获取")
    p.add_argument("--list", default=None, dest="list_cat",
                   help="列出接口类别（macro/stock/fund/futures/bond/industry/currency/all）")
    p.add_argument("--fetch", default=None, help="接口名，如 macro_china_gdp")
    p.add_argument("--kwargs", default=None, help="接口参数 JSON，如 {\"symbol\":\"000001\"}")
    p.add_argument("--out", default="paper_output/code/data")
    args = p.parse_args()

    if args.list_cat:
        return list_interfaces(args.list_cat)
    if args.fetch:
        return fetch(args.fetch, args.kwargs, Path(args.out))
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
