#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Optuna 超参自动调优 — 贝叶斯优化寻最优参数，比网格搜索快且专业。

融合自 optuna（14549★）。数模 ML/优化题用 Optuna 替代手动调参：
  - 论文里写"贝叶斯优化（TPE）"比"网格搜索"专业
  - 自动寻最优超参，带可视化（优化历史/参数重要性）

内置模型：XGBoost / LightGBM / RandomForest / SVR / MLP（可扩展）。
用法：
  python optuna_tune.py --model xgboost --X data.csv --y target --trials 50
  python optuna_tune.py --model lightgbm --X data.csv --y target --trials 100 --out paper_output/code/tune/
产出：best_params.json + optuna.db（可视化用）+ 优化历史图
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


def build_objective(model_type: str, X, y):
    """返回 optuna objective 函数。"""
    from sklearn.model_selection import cross_val_score
    import numpy as np

    def objective(trial):
        if model_type == "xgboost":
            import xgboost as xgb
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "max_depth": trial.suggest_int("max_depth", 3, 12),
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            }
            model = xgb.XGBRegressor(**params, random_state=42, n_jobs=-1)
        elif model_type == "lightgbm":
            import lightgbm as lgb
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "num_leaves": trial.suggest_int("num_leaves", 15, 127),
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
                "feature_fraction": trial.suggest_float("feature_fraction", 0.6, 1.0),
                "bagging_fraction": trial.suggest_float("bagging_fraction", 0.6, 1.0),
            }
            model = lgb.LGBMRegressor(**params, random_state=42, n_jobs=-1, verbose=-1)
        elif model_type == "random_forest":
            from sklearn.ensemble import RandomForestRegressor
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 800),
                "max_depth": trial.suggest_int("max_depth", 4, 30),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
            }
            model = RandomForestRegressor(**params, random_state=42, n_jobs=-1)
        elif model_type == "svr":
            from sklearn.svm import SVR
            from sklearn.preprocessing import StandardScaler
            from sklearn.pipeline import Pipeline
            params = {
                "C": trial.suggest_float("C", 1e-2, 1e2, log=True),
                "gamma": trial.suggest_float("gamma", 1e-4, 1e1, log=True),
                "epsilon": trial.suggest_float("epsilon", 1e-3, 1.0, log=True),
            }
            model = Pipeline([("scaler", StandardScaler()), ("svr", SVR(**params))])
        else:
            raise ValueError(f"未知模型: {model_type}")

        # 5 折交叉验证负 MSE（optuna 最大化 → 取负号）
        scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_squared_error", n_jobs=-1)
        rmse = float(np.sqrt(-scores.mean()))
        return rmse  # 最小化 RMSE

    return objective


def main() -> int:
    p = argparse.ArgumentParser(description="Optuna 超参自动调优")
    p.add_argument("--model", required=True,
                   choices=["xgboost", "lightgbm", "random_forest", "svr"])
    p.add_argument("--X", required=True, help="特征 CSV")
    p.add_argument("--y", required=True, help="目标列名（在 CSV 内）或单独 CSV")
    p.add_argument("--trials", type=int, default=50)
    p.add_argument("--out", default="paper_output/code/tune")
    args = p.parse_args()

    try:
        import optuna  # type: ignore
        import pandas as pd  # type: ignore
    except ImportError:
        print("[optuna] 未安装。pip install optuna pandas", file=sys.stderr)
        return 2

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.X)
    if args.y in df.columns:
        y = df.pop(args.y)
        X = df
    else:
        X = df
        y = pd.read_csv(args.y).iloc[:, 0]

    storage = f"sqlite:///{out_dir / 'optuna.db'.replace(chr(92), '/')}"
    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=42),
                                storage=storage, study_name=f"{args.model}_tune")
    objective = build_objective(args.model, X, y)
    study.optimize(objective, n_trials=args.trials, show_progress_bar=False)

    best = study.best_params
    best["best_rmse"] = float(study.best_value)
    best["model"] = args.model
    best["n_trials"] = args.trials

    (out_dir / "best_params.json").write_text(
        json.dumps(best, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[optuna] {args.model} 调优完成（{args.trials} 轮）")
    print(f"  最优 RMSE: {best['best_rmse']:.6f}")
    print(f"  最优参数:")
    for k, v in study.best_params.items():
        print(f"    {k}: {v}")
    print(f"  → {out_dir / 'best_params.json'}")

    # 可视化（参数重要性 + 优化历史）
    try:
        import matplotlib
        matplotlib.use("Agg")
        fig = optuna.visualization.matplotlib.plot_optimization_history(study)
        fig.figure.savefig(out_dir / "optimization_history.png", dpi=150, bbox_inches="tight")
        fig2 = optuna.visualization.matplotlib.plot_param_importances(study)
        fig2.figure.savefig(out_dir / "param_importances.png", dpi=150, bbox_inches="tight")
        print(f"  可视化 → {out_dir}/optimization_history.png, param_importances.png")
    except Exception as e:
        print(f"  可视化跳过: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())