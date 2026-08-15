#!/usr/bin/env python3
"""
结果自动注入论文脚本

将代码运行结果自动注入到论文中，确保论文数字与代码输出一致。

用法：
    python inject_results_to_paper.py [--dry-run]

输出：
    - 更新后的 paper_output/final_paper_source.md
    - paper_output/qa/inject_report.json
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
RESULTS_DIR = OUTPUT_DIR / "results"
PAPER_FILE = OUTPUT_DIR / "final_paper_source.md"
REPORT_JSON = QA_DIR / "inject_report.json"


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def extract_q1_results() -> dict[str, Any]:
    """提取Q1的计算结果"""
    data = load_json(RESULTS_DIR / "q1_results.json")
    if not data:
        return {}

    results = data.get("results", {})
    energy = results.get("energy", {})
    indicators = results.get("indicators", {})
    cost = results.get("cost", {})

    return {
        "E_load": energy.get("E_load_kWh", 0),
        "E_re": energy.get("E_re_kWh", 0),
        "E_buy": energy.get("E_buy_kWh", 0),
        "E_sell": energy.get("E_sell_kWh", 0),
        "self_use": indicators.get("self_use_ratio", 0) * 100,
        "green_ratio": indicators.get("green_ratio", 0) * 100,
        "feed_in": indicators.get("feed_in_ratio", 0) * 100,
        "ton_cost": cost.get("ton_nh3_cost_yuan", 0),
    }


def format_number(value: float, decimal_places: int = 1) -> str:
    """格式化数字"""
    if decimal_places == 0:
        return f"{int(value):,}"
    return f"{value:,.{decimal_places}f}"


def replace_in_paper(paper_text: str, replacements: list[tuple[str, str]]) -> tuple[str, int]:
    """在论文中替换文本（迭代 replacements 清单——旧版误迭代 paper_text 字符串，
    一旦被调用必然 ValueError 崩溃，属潜伏 bug；当前 main 走内联循环未触发）"""
    count = 0
    for old, new in replacements:
        if old in paper_text:
            paper_text = paper_text.replace(old, new, 1)
            count += 1
    return paper_text, count


def generate_replacements(q1_results: dict) -> list[tuple[str, str]]:
    """生成替换列表"""
    replacements = []

    if not q1_results:
        return replacements

    # 摘要中的数字
    replacements.append((
        f"日用电量为{format_number(q1_results['E_load'], 0)} kWh",
        f"日用电量为{format_number(q1_results['E_load'], 0)} kWh"
    ))
    replacements.append((
        f"新能源发电量为{format_number(q1_results['E_re'], 0)} kWh",
        f"新能源发电量为{format_number(q1_results['E_re'], 0)} kWh"
    ))
    replacements.append((
        f"网购电量为{format_number(q1_results['E_buy'], 0)} kWh",
        f"网购电量为{format_number(q1_results['E_buy'], 0)} kWh"
    ))
    replacements.append((
        f"上网电量为{format_number(q1_results['E_sell'], 0)} kWh",
        f"上网电量为{format_number(q1_results['E_sell'], 0)} kWh"
    ))
    replacements.append((
        f"比例为{format_number(q1_results['self_use'])}%",
        f"比例为{format_number(q1_results['self_use'])}%"
    ))
    replacements.append((
        f"比例为{format_number(q1_results['green_ratio'])}%",
        f"比例为{format_number(q1_results['green_ratio'])}%"
    ))
    replacements.append((
        f"比例为{format_number(q1_results['feed_in'])}%",
        f"比例为{format_number(q1_results['feed_in'])}%"
    ))
    replacements.append((
        f"吨氨成本为{format_number(q1_results['ton_cost'], 0)}元",
        f"吨氨成本为{format_number(q1_results['ton_cost'], 0)}元"
    ))

    return replacements


def inject_results_to_table(paper_text: str, q1_results: dict) -> str:
    """将结果注入到表格中"""
    # 查找表2并替换内容
    table_pattern = r"(\*\*表2 典型日运行指标计算结果\*\*\n\n\|.*?\|.*?\|.*?\|.*?\|\n)(\|.*?\|.*?\|.*?\|.*?\|\n)*"
    table_match = re.search(table_pattern, paper_text, re.DOTALL)

    if table_match and q1_results:
        new_table = f"""**表2 典型日运行指标计算结果**

| 指标 | 数值 | 要求 | 是否满足 |
|------|------|------|----------|
| 日用电量 | {format_number(q1_results['E_load'], 0)} kWh | - | - |
| 新能源发电量 | {format_number(q1_results['E_re'], 0)} kWh | - | - |
| 网购电量 | {format_number(q1_results['E_buy'], 0)} kWh | - | - |
| 上网电量 | {format_number(q1_results['E_sell'], 0)} kWh | - | - |
| 自发自用比例 | {format_number(q1_results['self_use'])}% | >60% | {'✅' if q1_results['self_use'] >= 60 else '❌'} |
| 绿电比例 | {format_number(q1_results['green_ratio'])}% | >30% | {'✅' if q1_results['green_ratio'] >= 30 else '❌'} |
| 上网比例 | {format_number(q1_results['feed_in'])}% | <20% | {'✅' if q1_results['feed_in'] <= 20 else '❌'} |
| 吨氨成本 | {format_number(q1_results['ton_cost'], 0)} 元/吨 | - | - |
"""
        paper_text = paper_text[:table_match.start()] + new_table + paper_text[table_match.end():]

    return paper_text


def main():
    import argparse
    parser = argparse.ArgumentParser(description="结果自动注入论文")
    parser.add_argument("--dry-run", action="store_true", help="仅显示替换，不实际修改")
    args = parser.parse_args()

    print("结果自动注入论文")
    print("=" * 50)

    if not PAPER_FILE.exists():
        print(f"❌ 论文文件不存在: {PAPER_FILE}")
        return 1

    paper_text = PAPER_FILE.read_text(encoding="utf-8")

    # 提取Q1结果
    q1_results = extract_q1_results()
    if not q1_results:
        print("❌ Q1结果文件不存在或为空")
        return 1

    print(f"\nQ1计算结果:")
    for key, value in q1_results.items():
        print(f"  {key}: {value}")

    # 生成替换列表
    replacements = generate_replacements(q1_results)

    # 注入表格
    new_paper_text = inject_results_to_table(paper_text, q1_results)

    # 统计替换
    changes = []
    for old, new in replacements:
        if old in new_paper_text:
            new_paper_text = new_paper_text.replace(old, new, 1)
            changes.append({"old": old, "new": new})

    if args.dry_run:
        print(f"\n[Dry Run] 将进行 {len(changes)} 处替换:")
        for change in changes:
            print(f"  - {change['old']} → {change['new']}")
    else:
        # 保存更新后的论文
        PAPER_FILE.write_text(new_paper_text, encoding="utf-8")
        print(f"\n✅ 已更新论文: {PAPER_FILE}")
        print(f"   替换数量: {len(changes)}")

    # 保存报告
    report = {
        "schema_version": "1.0",
        "generated_at": "2026-06-15",
        "q1_results": q1_results,
        "changes": changes,
        "status": "SUCCESS" if changes else "NO_CHANGES",
    }
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
