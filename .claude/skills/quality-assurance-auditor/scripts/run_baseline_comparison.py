#!/usr/bin/env python3
"""基准对照自动化脚本（v4.5 参数外置版）

运行基准方案（不优化）并与优化方案对比，展示优化的价值。

数据文件名与全部模型参数外置到赛题配置 paper_output/plan/qa_config.json，
schema 示例见 .claude/skills/quality-assurance-auditor/references/qa_config.example.json
（示例参数属于旧赛题「绿电直连型合成氨」）。配置或所需段缺失时输出 SKIP
（退出码 0），绝不输出 PASS。模型结构（分时电价 + 电解槽/合成氨调度）为该类
园区问题定制，换赛题除重写配置外还需评估模型函数是否适用。

用法：
    python run_baseline_comparison.py [--config 配置路径]

输出：
    - paper_output/results/baseline_comparison.json
    - paper_output/qa/baseline_comparison_report.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
RESULTS_DIR = OUTPUT_DIR / "results"
DATA_DIR = OUTPUT_DIR / "data_cleaned"
REPORT_JSON = RESULTS_DIR / "baseline_comparison.json"
REPORT_MD = QA_DIR / "baseline_comparison_report.md"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "plan" / "qa_config.json"
EXAMPLE_CONFIG_HINT = ".claude/skills/quality-assurance-auditor/references/qa_config.example.json"

REQUIRED_SECTIONS = ["data_files", "model_params", "price_periods", "om_coeffs", "production"]


def load_qa_config(config_path: Path, required_sections: list) -> tuple:
    """读取赛题配置。返回 (config, skip_reason)；skip_reason 非空表示应 SKIP。"""
    if not config_path.exists():
        return None, (f"未找到赛题配置 {config_path}（新赛题需先生成，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"错误：赛题配置 {config_path} 读取/解析失败：{exc}")
        raise SystemExit(1)
    missing = [s for s in required_sections if s not in config]
    if missing:
        return None, (f"赛题配置 {config_path} 缺少段 {missing}（新赛题需先补齐，"
                      f"格式参考 {EXAMPLE_CONFIG_HINT}）")
    return config, ""


def write_skip_reports(reason: str) -> None:
    """配置缺失时写 SKIP 状态报告（绝不写 PASS）。"""
    payload = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "SKIP",
        "reason": reason,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(
        "\n".join(["# 基准对照分析报告", "", "- 状态: `SKIP`", f"- 原因: {reason}", ""]),
        encoding="utf-8",
    )


def make_price_fn(params: dict, periods: dict):
    """按配置的分时段构造电价函数：peak/normal 命中则取对应电价，否则谷价。"""
    def in_any(h, ranges):
        return any(lo <= h < hi for lo, hi in ranges)

    def get_price(h):
        if in_any(h, periods.get("peak", [])):
            return params["PEAK_PRICE"]
        if in_any(h, periods.get("normal", [])):
            return params["NORMAL_PRICE"]
        return params["VALLEY_PRICE"]

    return get_price


def load_curves(cfg: dict) -> tuple:
    """按配置加载清洗后的负荷/风光标幺曲线。"""
    data_files = cfg["data_files"]
    columns = cfg.get("columns", {})
    for key in ("load_curve", "renewable_curve"):
        if key not in data_files:
            print(f"错误：赛题配置 data_files 段缺少 {key}")
            raise SystemExit(1)
    load_path = DATA_DIR / data_files["load_curve"]
    re_path = DATA_DIR / data_files["renewable_curve"]
    for p in (load_path, re_path):
        if not p.exists():
            print(f"错误：配置声明的数据文件不存在：{p}")
            raise SystemExit(1)
    load_df = pd.read_csv(load_path)
    re_df = pd.read_csv(re_path)
    load_pu = load_df.iloc[:, int(columns.get("load", 1))].values
    wind_pu = re_df.iloc[:, int(columns.get("wind", 1))].values
    solar_pu = re_df.iloc[:, int(columns.get("solar", 2))].values
    if min(len(load_pu), len(wind_pu), len(solar_pu)) < 24:
        print("错误：数据曲线不足 24 个时段，无法进行 24h 对照")
        raise SystemExit(1)
    return load_pu, wind_pu, solar_pu


def compute_om(params: dict, om: dict, P_wind, P_solar) -> float:
    """运维成本 = 风/光按发电量 + 电解槽/合成氨按装机×24h。"""
    return (om["wind"] * float(np.sum(P_wind)) * 1000
            + om["solar"] * float(np.sum(P_solar)) * 1000
            + (om["alkel"] * params["P_ALKEL"] + om["pemel"] * params["P_PEMEL"]
               + om["nh3"] * params["P_NH3"]) * 1000 * 24)


def run_baseline_24h(curves, params, get_price, om_coeffs, production):
    """基准方案：24小时满负荷运行"""
    load_pu, wind_pu, solar_pu = curves
    P_load = load_pu * params["P_LOAD_PEAK"]
    P_wind = wind_pu * params["P_WIND"]
    P_solar = solar_pu * params["P_SOLAR"]
    P_re = P_wind + P_solar

    P_elec = params["P_ALKEL"] + params["P_PEMEL"]
    P_ammonia = params["P_NH3"]
    P_total_load = P_load + P_elec + P_ammonia

    P_balance = P_re - P_total_load
    P_buy = np.maximum(-P_balance, 0)
    P_sell = np.maximum(P_balance, 0)

    E_load = float(np.sum(P_total_load) * 1000)
    E_re = float(np.sum(P_re) * 1000)
    E_buy = float(np.sum(P_buy) * 1000)
    E_sell = float(np.sum(P_sell) * 1000)

    self_use = (E_load - E_sell - E_buy) / E_re if E_re > 0 else 0
    green_ratio = (E_re - E_sell) / E_load if E_load > 0 else 0
    feed_in = E_sell / E_re if E_re > 0 else 0

    buy_cost = sum(float(P_buy[h] * 1000 * get_price(h)) for h in range(24))
    sell_income = float(np.sum(P_sell) * 1000 * params["FEED_IN_PRICE"])
    daily_cost = buy_cost - sell_income + compute_om(params, om_coeffs, P_wind, P_solar)
    nh3_daily = float(production["nh3_daily_ton"])
    ton_cost = daily_cost / nh3_daily

    return {
        "scenario": "24h_full_load",
        "description": "24小时满负荷运行（基准方案）",
        "E_load": E_load,
        "E_re": E_re,
        "E_buy": E_buy,
        "E_sell": E_sell,
        "self_use_ratio": self_use,
        "green_ratio": green_ratio,
        "feed_in_ratio": feed_in,
        "ton_nh3_cost": ton_cost,
        "nh3_daily": nh3_daily,
        "utilization": 1.0,
    }


def run_optimized(curves, params, get_price, om_coeffs, production):
    """优化方案：根据边际成本选择生产时段"""
    load_pu, wind_pu, solar_pu = curves
    P_load = load_pu * params["P_LOAD_PEAK"]
    P_wind = wind_pu * params["P_WIND"]
    P_solar = solar_pu * params["P_SOLAR"]
    P_re = P_wind + P_solar

    P_prod = params["P_ALKEL"] + params["P_PEMEL"] + params["P_NH3"]
    opt_hours = int(production["optimized_hours"])
    nh3_daily = float(production["nh3_daily_ton"])

    # 计算各时段的边际成本
    marginal_costs = []
    for h in range(24):
        # 不生产时的成本
        P_balance_nprod = P_re[h] - P_load[h]
        cost_nprod = (max(-P_balance_nprod, 0) * 1000 * get_price(h)
                      - max(P_balance_nprod, 0) * 1000 * params["FEED_IN_PRICE"])
        # 生产时的成本
        P_balance_prod = P_re[h] - (P_load[h] + P_prod)
        cost_prod = (max(-P_balance_prod, 0) * 1000 * get_price(h)
                     - max(P_balance_prod, 0) * 1000 * params["FEED_IN_PRICE"])
        marginal_costs.append((h, cost_prod - cost_nprod))

    # 选择边际成本最低的 opt_hours 小时生产
    marginal_costs.sort(key=lambda x: x[1])
    production_hours = set(h for h, _ in marginal_costs[:opt_hours])

    # 计算优化方案的结果
    E_load = E_re = E_buy = E_sell = 0
    total_cost = 0
    for h in range(24):
        P_total = P_load[h] + (P_prod if h in production_hours else 0)
        P_balance = P_re[h] - P_total
        buy = max(-P_balance, 0)
        sell = max(P_balance, 0)
        E_load += P_total * 1000
        E_re += P_re[h] * 1000
        E_buy += buy * 1000
        E_sell += sell * 1000
        total_cost += buy * 1000 * get_price(h) - sell * 1000 * params["FEED_IN_PRICE"]

    total_cost += compute_om(params, om_coeffs, P_wind, P_solar)

    self_use = (E_load - E_sell - E_buy) / E_re if E_re > 0 else 0
    green_ratio = (E_re - E_sell) / E_load if E_load > 0 else 0
    feed_in = E_sell / E_re if E_re > 0 else 0

    return {
        "scenario": "optimized",
        "description": f"优化调度方案（{opt_hours}小时生产）",
        "E_load": E_load,
        "E_re": E_re,
        "E_buy": E_buy,
        "E_sell": E_sell,
        "self_use_ratio": self_use,
        "green_ratio": green_ratio,
        "feed_in_ratio": feed_in,
        "ton_nh3_cost": total_cost / nh3_daily,
        "nh3_daily": nh3_daily,
        "utilization": opt_hours / 24,
        "production_hours": sorted(production_hours),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="基准对照自动化：读取赛题配置 qa_config.json，运行基准方案与优化方案并对比"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH),
                        help="赛题配置 JSON 路径（默认 paper_output/plan/qa_config.json）")
    args = parser.parse_args(argv)

    print("基准对照自动化")
    print("=" * 50)

    cfg, skip_reason = load_qa_config(Path(args.config), REQUIRED_SECTIONS)
    if skip_reason:
        print(f"SKIP：{skip_reason}")
        write_skip_reports(skip_reason)
        return 0

    params = cfg["model_params"]
    get_price = make_price_fn(params, cfg["price_periods"])
    om_coeffs = cfg["om_coeffs"]
    production = cfg["production"]
    curves = load_curves(cfg)

    print("\n运行基准方案（24小时满负荷）...")
    baseline = run_baseline_24h(curves, params, get_price, om_coeffs, production)
    print(f"  吨氨成本: {baseline['ton_nh3_cost']:.0f}元/吨")
    print(f"  自发自用: {baseline['self_use_ratio']:.1%}")
    print(f"  绿电比例: {baseline['green_ratio']:.1%}")

    print("\n运行优化方案...")
    optimized = run_optimized(curves, params, get_price, om_coeffs, production)
    print(f"  吨氨成本: {optimized['ton_nh3_cost']:.0f}元/吨")
    print(f"  自发自用: {optimized['self_use_ratio']:.1%}")
    print(f"  绿电比例: {optimized['green_ratio']:.1%}")
    print(f"  生产时段: {optimized['production_hours']}")

    cost_improvement = (baseline['ton_nh3_cost'] - optimized['ton_nh3_cost']) / baseline['ton_nh3_cost']
    self_use_improvement = optimized['self_use_ratio'] - baseline['self_use_ratio']
    green_improvement = optimized['green_ratio'] - baseline['green_ratio']
    feed_in_improvement = baseline['feed_in_ratio'] - optimized['feed_in_ratio']

    print("\n改善幅度:")
    print(f"  吨氨成本: {cost_improvement:+.1%}")
    print(f"  自发自用: {self_use_improvement:+.1%}")
    print(f"  绿电比例: {green_improvement:+.1%}")
    print(f"  上网比例: {feed_in_improvement:+.1%}")

    comparison = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "DONE",
        "config_path": str(args.config),
        "baseline": baseline,
        "optimized": optimized,
        "improvement": {
            "ton_nh3_cost": cost_improvement,
            "self_use_ratio": self_use_improvement,
            "green_ratio": green_improvement,
            "feed_in_ratio": feed_in_improvement,
        },
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(comparison, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 基准对照分析报告",
        "",
        "## 方案对比",
        "",
        "| 指标 | 基准方案(24h满产) | 优化方案 | 改善幅度 |",
        "|------|-----------------|---------|---------|",
        f"| 吨氨成本 | {baseline['ton_nh3_cost']:.0f}元/吨 | {optimized['ton_nh3_cost']:.0f}元/吨 | {cost_improvement:+.1%} |",
        f"| 自发自用比例 | {baseline['self_use_ratio']:.1%} | {optimized['self_use_ratio']:.1%} | {self_use_improvement:+.1%} |",
        f"| 绿电比例 | {baseline['green_ratio']:.1%} | {optimized['green_ratio']:.1%} | {green_improvement:+.1%} |",
        f"| 上网比例 | {baseline['feed_in_ratio']:.1%} | {optimized['feed_in_ratio']:.1%} | {feed_in_improvement:+.1%} |",
        f"| 设备利用率 | 100% | {optimized['utilization']:.0%} | - |",
        "",
        "## 优化方案详情",
        "",
        f"生产时段: {optimized['production_hours']}",
        "",
        "## 结论",
        "",
        f"优化调度可降低吨氨成本{cost_improvement:.1%}，提高自发自用比例{self_use_improvement:.1%}。",
    ]
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{'=' * 50}")
    print("分析完成")
    print(f"结果: {REPORT_JSON}")
    print(f"报告: {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
