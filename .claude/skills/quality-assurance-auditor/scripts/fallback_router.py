#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""L2 Fallback Hand Off 路由器：主方法失败时切换到备用方案。

融合自 jihe520/MathModelAgent 四层容错的 L2 层（Fallback Hand Off）。
与 L1（auto_detect_and_fix.py 重试）、L3（Shadow 降级）、L4（pipeline rework 人介入）
配合，构成完整 4 层容错（见 references/four_layer_fault_tolerance.md）。

用法：
  # 查看某类方法的备用链
  python fallback_router.py list optimization
  # 取下一个备用方案（消费式：记录到 fallback_log，返回下一方法）
  python fallback_router.py next --category optimization --failed "NSGA-II" --reason "种群退化"
  # 查看历史 fallback 记录
  python fallback_router.py log
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

ROUTES_FILE = Path(__file__).parent / "fallback_routes.json"
LOG_FILE = Path("paper_output/qa/fallback_log.json")


def load_routes() -> dict:
    return json.loads(ROUTES_FILE.read_text(encoding="utf-8"))


def load_log() -> dict:
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"events": []}


def append_log(entry: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = load_log()
    log["events"].append(entry)
    log["updated_at"] = datetime.now().isoformat(timespec="seconds")
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_list(args: argparse.Namespace) -> int:
    routes = load_routes()["routes"]
    if args.category:
        cat = routes.get(args.category)
        if not cat:
            print(f"[router] 未知类别: {args.category}。可选: {', '.join(routes)}")
            return 1
        print(f"\n[{args.category}] {cat['description']}\n")
        for i, step in enumerate(cat["chain"], 1):
            print(f"  {i}. {step['method']}")
            print(f"     模板: {step['template']}")
            print(f"     触发: {step['when']}\n")
    else:
        print("\n可用 fallback 类别：\n")
        for cat, info in routes.items():
            chain = " → ".join(s["method"] for s in info["chain"])
            print(f"  {cat:<16} {info['description']}")
            print(f"  {'':16} 链: {chain}\n")
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    routes = load_routes()["routes"]
    cat = routes.get(args.category)
    if not cat:
        print(f"[router] 未知类别: {args.category}")
        return 1

    chain = cat["chain"]
    # 找到 failed 在链中的位置，返回下一个
    methods = [s["method"] for s in chain]
    if args.failed not in methods:
        print(f"[router] 主方法 '{args.failed}' 不在 {args.category} 链中，返回链首。")
        next_step = chain[0]
        idx = 0
    else:
        idx = methods.index(args.failed)
        if idx + 1 >= len(chain):
            # L2 耗尽 → 提示进入 L3/L4
            append_log({
                "at": datetime.now().isoformat(timespec="seconds"),
                "category": args.category,
                "failed": args.failed,
                "reason": args.reason,
                "result": "L2_EXHAUSTED",
                "advice": "L2 备用链耗尽，进入 L3 Shadow 降级 或 L4 pipeline rework 人介入",
            })
            print(f"[router] ✗ {args.category} 的 L2 备用链已耗尽（{args.failed} 是最后手段）。")
            print(f"[router] → 进入 L3 Evaluator Shadow Mode（降级交付 + 标注不确定）")
            print(f"[router]   或 L4：python pipeline_manager.py rework <stage> --feedback 'L2 耗尽'")
            return 2
        next_step = chain[idx + 1]

    append_log({
        "at": datetime.now().isoformat(timespec="seconds"),
        "category": args.category,
        "failed": args.failed,
        "reason": args.reason,
        "result": "FALLBACK",
        "next_method": next_step["method"],
        "next_template": next_step["template"],
    })
    print(f"[router] L2 Fallback：{args.failed} → {next_step['method']}")
    print(f"  触发原因: {args.reason}")
    print(f"  适用场景: {next_step['when']}")
    print(f"  代码模板: {next_step['template']}")
    print(f"  记录: {LOG_FILE}")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    log = load_log()
    events = log.get("events", [])
    if not events:
        print("[router] 无 fallback 记录")
        return 0
    print(f"\nFallback 历史（{len(events)} 条）:\n")
    for e in events[-20:]:
        if e["result"] == "FALLBACK":
            print(f"  {e['at'][:19]}  {e['category']:<14} {e['failed']} → {e['next_method']}")
            print(f"  {'':20}原因: {e['reason']}")
        else:
            print(f"  {e['at'][:19]}  {e['category']:<14} {e['result']}  ({e['failed']})")
            print(f"  {'':20}{e.get('advice', '')}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="L2 Fallback Hand Off 路由器")
    sub = p.add_subparsers(dest="cmd")
    pl = sub.add_parser("list", help="列出备用链")
    pl.add_argument("category", nargs="?", default=None)
    pn = sub.add_parser("next", help="取下一个备用方案")
    pn.add_argument("--category", required=True)
    pn.add_argument("--failed", required=True, help="失败的主方法名")
    pn.add_argument("--reason", default="", help="失败原因")
    sub.add_parser("log", help="查看 fallback 历史")
    args = p.parse_args()
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "next":
        return cmd_next(args)
    if args.cmd == "log":
        return cmd_log(args)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())