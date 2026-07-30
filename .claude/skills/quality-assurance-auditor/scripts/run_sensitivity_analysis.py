#!/usr/bin/env python3
"""灵敏度分析自动化脚本（v4.5 参数外置版）

自动运行不同参数扰动下的模型，生成灵敏度分析结果。

数据文件名、基准参数与扰动区间外置到赛题配置 paper_output/plan/qa_config.json，
schema 示例见 .claude/skills/quality-assurance-auditor/references/qa_config.example.json
（示例参数属于旧赛题「绿电直连型合成氨」）。配置或所需段缺失时输出 SKIP
（退出码 0），绝不输出 PASS。内置模型函数（分时电价 + 电解槽/合成氨负荷）
为该类园区问题定制，换赛题除重写配置外还需评估模型函数是否适用。

用法：
    python run_sensitivity_analysis.py [--config 配置路径]

输出：
    - paper_output/results/sensitivity_results.json
    - paper_output/qa/sensitivity_report.md
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
REPORT_JSON = RESULTS_DIR / "sensitivity_results.json"
REPORT_MD = QA_DIR / "sensitivity_report.md"
DEFAULT_CONFIG_PATH = OUTPUT_DIR / "plan" / "qa_config.json"
EXAMPLE_CONFIG_HINT = ".claude/skills/quality-assurance-auditor/references/qa_config.example.json"

REQUIRED_SECTIONS = ["data_files", "model_params", "price_periods", "om_coeffs",
                     "production", "sensitivity"]


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
        "\n".join(["# 灵敏度分析报告", "", "- 状态: `SKIP`", f"- 原因: {reason}", ""]),
        encoding="utf-8",
    )


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
        print("错误：数据曲线不足 24 个时段，无法进行 24h 模型计算")
        raise SystemExit(1)
    return load_pu, wind_pu, solar_pu


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


def run_q1_model(curves, params, periods, om, production):
    """运行 Q1 供电模型（参数全部来自配置）"""
    load_pu, wind_pu, solar_pu = curves
    P_load = load_pu * params["P_LOAD_PEAK"]
    P_wind = wind_pu * params["P_WIND"]
    P_solar = solar_pu * params["P_SOLAR"]
    P_re = P_wind + P_solar

    P_total_load = P_load + params["P_ALKEL"] + params["P_PEMEL"] + params["P_NH3"]

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

    get_price = make_price_fn(params, periods)
    buy_cost = sum(float(P_buy[h] * 1000 * get_price(h)) for h in range(24))
    sell_income = float(np.sum(P_sell) * 1000 * params["FEED_IN_PRICE"])
    om_cost = (om["wind"] * float(np.sum(P_wind)) * 1000
               + om["solar"] * float(np.sum(P_solar)) * 1000
               + (om["alkel"] * params["P_ALKEL"] + om["pemel"] * params["P_PEMEL"]
                  + om["nh3"] * params["P_NH3"]) * 1000 * 24)
    daily_cost = buy_cost - sell_income + om_cost
    ton_cost = daily_cost / float(production["nh3_daily_ton"])

    return {
        "E_load": E_load,
        "E_re": E_re,
        "E_buy": E_buy,
        "E_sell": E_sell,
        "self_use_ratio": self_use,
        "green_ratio": green_ratio,
        "feed_in_ratio": feed_in,
        "ton_nh3_cost": ton_cost,
    }


def run_sensitivity(curves, cfg: dict, param_name: str, variations: list) -> list:
    """对单个参数进行灵敏度分析"""
    base_params = cfg["model_params"]
    if param_name not in base_params:
        print(f"错误：sensitivity 段引用的参数 {param_name} 不在 model_params 中")
        raise SystemExit(1)
    results = []
    for var in variations:
        params = dict(base_params)
        params[param_name] = params[param_name] * (1 + var)
        result = run_q1_model(curves, params, cfg["price_periods"],
                              cfg["om_coeffs"], cfg["production"])
        result["variation"] = var
        result["param_value"] = params[param_name]
        results.append(result)
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="灵敏度分析自动化：读取赛题配置 qa_config.json，按扰动区间批量运行模型"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH),
                        help="赛题配置 JSON 路径（默认 paper_output/plan/qa_config.json）")
    args = parser.parse_args(argv)

    print("灵敏度分析自动化")
    print("=" * 50)

    cfg, skip_reason = load_qa_config(Path(args.config), REQUIRED_SECTIONS)
    if skip_reason:
        print(f"SKIP：{skip_reason}")
        write_skip_reports(skip_reason)
        return 0

    curves = load_curves(cfg)
    sensitivity_params = {k: v for k, v in cfg["sensitivity"].items()
                          if not k.startswith("_")}
    if not sensitivity_params:
        print(f"SKIP：赛题配置 sensitivity 段为空（新赛题需先补齐，格式参考 {EXAMPLE_CONFIG_HINT}）")
        write_skip_reports("sensitivity 段为空")
        return 0

    all_results = {}
    for param_name, variations in sensitivity_params.items():
        print(f"\n分析参数: {param_name}")
        results = run_sensitivity(curves, cfg, param_name, variations)
        all_results[param_name] = results
        for r in results:
            print(f"  变化{r['variation']:+.0%}: 吨氨成本={r['ton_nh3_cost']:.0f}元/吨, "
                  f"自发自用={r['self_use_ratio']:.1%}, 绿电={r['green_ratio']:.1%}")

    payload = {
        "schema_version": "1.1",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "DONE",
        "config_path": str(args.config),
        "results": all_results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 灵敏度分析报告",
        "",
        "## 基准参数",
        "",
        "| 参数 | 值 |",
        "|------|-----|",
    ]
    for k, v in cfg["model_params"].items():
        if not str(k).startswith("_"):
            lines.append(f"| {k} | {v} |")

    lines += ["", "## 灵敏度分析结果", ""]
    for param_name, results in all_results.items():
        lines.append(f"### {param_name}")
        lines.append("")
        lines.append("| 变化幅度 | 参数值 | 吨氨成本 | 自发自用比例 | 绿电比例 | 上网比例 |")
        lines.append("|---------|--------|---------|------------|---------|---------|")
        for r in results:
            lines.append(f"| {r['variation']:+.0%} | {r['param_value']:.2f} | {r['ton_nh3_cost']:.0f}元/吨 | "
                         f"{r['self_use_ratio']:.1%} | {r['green_ratio']:.1%} | {r['feed_in_ratio']:.1%} |")
        lines.append("")

    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{'=' * 50}")
    print("分析完成")
    print(f"结果: {REPORT_JSON}")
    print(f"报告: {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
