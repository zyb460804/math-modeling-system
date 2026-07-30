#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SHAP 模型可解释性 — 特征重要性 + 依赖图 + 单样本解释。

融合自 shapash（3247★）+ shap（标准库）。数模 ML 题（尤其 C 题预测/分类）评委
最看重"可解释性"——光给预测不够，要说明"为啥"。SHAP 输出：
  - 全局特征重要性条形图（哪个特征对模型影响最大）
  - 蜂群图（每个样本的特征贡献分布）
  - 依赖图（某特征值如何影响预测）
  - 单样本 waterfall（这条预测是怎么来的）

支持：XGBoost / LightGBM / RandomForest / sklearn 大部分模型。

用法：
  python shap_explain.py --model model.pkl --X data.csv --out paper_output/figures/shap/
  python shap_explain.py --model model.pkl --X data.csv --feature "温度" --kind dependence
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
    p = argparse.ArgumentParser(description="SHAP 模型可解释性")
    p.add_argument("--model", required=True, help="训练好的模型（.pkl）或路径")
    p.add_argument("--X", required=True, help="特征数据 CSV（用于计算 SHAP）")
    p.add_argument("--feature", default=None, help="dependence 图的特征名")
    p.add_argument("--kind", default="summary",
                   choices=["summary", "dependence", "waterfall", "all"],
                   help="summary=蜂群+条形；dependence=单特征依赖；waterfall=单样本")
    p.add_argument("--out", default="paper_output/figures/shap")
    p.add_argument("--sample-index", type=int, default=0, help="waterfall 用第几条样本")
    args = p.parse_args()

    try:
        import shap  # type: ignore
        import pandas as pd  # type: ignore
    except ImportError:
        print(
            "[shap] 未安装。pip install shap pandas matplotlib",
            file=sys.stderr,
        )
        return 2
    import pickle
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 可选 SciencePlots 期刊风
    try:
        import scienceplots  # type: ignore  # noqa: F401
        plt.style.use(["science", "no-latex"])
    except Exception:
        pass

    with open(args.model, "rb") as f:
        model = pickle.load(f)
    X = pd.read_csv(args.X)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 选 explainer：树模型用 TreeExplainer（快且精确），其它用 Kernel/Gradient
    explainer = None
    try:
        explainer = shap.TreeExplainer(model)
    except Exception:
        try:
            explainer = shap.GradientExplainer(model, X)
        except Exception:
            explainer = shap.LinearExplainer(model, X)
    shap_values = explainer.shap_values(X)

    # 多分类取第一类（二分类正类）
    if isinstance(shap_values, list):
        sv_arr = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    else:
        sv_arr = shap_values

    produced: list[str] = []

    def _save(fig, name):
        path = out_dir / name
        fig.savefig(path, dpi=200, bbox_inches="tight")
        produced.append(str(path).replace("\\", "/"))

    if args.kind in ("summary", "all"):
        # 条形图（全局重要性）
        fig, ax = plt.subplots(figsize=(6, max(3, 0.4 * X.shape[1])))
        shap.summary_plot(sv_arr, X, plot_type="bar", show=False, color=False)
        _save(plt.gcf(), "shap_importance_bar.png")
        plt.close()
        # 蜂群图
        shap.summary_plot(sv_arr, X, show=False)
        _save(plt.gcf(), "shap_beeswarm.png")
        plt.close()

    if args.kind in ("dependence", "all") and args.feature:
        shap.dependence_plot(args.feature, sv_arr, X, show=False)
        _save(plt.gcf(), f"shap_dependence_{args.feature}.png")
        plt.close()

    if args.kind in ("waterfall", "all"):
        try:
            sv_exp = explainer(X)
            if isinstance(sv_exp, list):
                sv_exp = sv_exp[1] if len(sv_exp) > 1 else sv_exp[0]
            shap.plots.waterfall(sv_exp[args.sample_index], show=False)
            _save(plt.gcf(), f"shap_waterfall_sample{args.sample_index}.png")
            plt.close()
        except Exception as e:
            print(f"[shap] waterfall 跳过: {e}")

    # 全局重要性 JSON（写进论文用）
    import numpy as np
    mean_abs = np.abs(sv_arr).mean(axis=0) if sv_arr.ndim > 1 else np.abs(sv_arr)
    importance = sorted(
        [{"feature": str(c), "mean_abs_shap": float(m)}
         for c, m in zip(X.columns, mean_abs)],
        key=lambda x: x["mean_abs_shap"], reverse=True,
    )
    (out_dir / "shap_importance.json").write_text(
        json.dumps(importance, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[shap] 产出 {len(produced)} 图：")
    for pth in produced:
        print(f"  {pth}")
    print(f"[shap] 特征重要性 Top5：")
    for it in importance[:5]:
        print(f"  {it['feature']:<20} {it['mean_abs_shap']:.4f}")
    print(f"[shap] JSON → {out_dir / 'shap_importance.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())