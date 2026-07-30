#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""算法基准测试：对 CSV 数据集运行多个 sklearn 常用模型的 K 折交叉验证。

- classification: LogisticRegression / DecisionTree / RandomForest /
  GradientBoosting / KNN / SVM，指标 accuracy + f1_macro
- regression: LinearRegression / Ridge / DecisionTree / RandomForest /
  GradientBoosting / KNN，指标 RMSE + R2

输出各模型指标与训练耗时排名表（控制台 + 可选 JSON）。
特征自动预处理：非数值列 one-hot，缺失值中位数填充，Pipeline 内统一标准化。
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd


def build_models(task):
    if task == "classification":
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import (RandomForestClassifier,
                                      GradientBoostingClassifier)
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC
        return {
            "LogisticRegression": LogisticRegression(max_iter=2000),
            "DecisionTree": DecisionTreeClassifier(random_state=42),
            "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
            "GradientBoosting": GradientBoostingClassifier(random_state=42),
            "KNN": KNeighborsClassifier(),
            "SVM": SVC(random_state=42),
        }
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import (RandomForestRegressor,
                                  GradientBoostingRegressor)
    from sklearn.neighbors import KNeighborsRegressor
    return {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(random_state=42),
        "DecisionTree": DecisionTreeRegressor(random_state=42),
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(random_state=42),
        "KNN": KNeighborsRegressor(),
    }


def prepare_features(df, target):
    x_raw = df.drop(columns=[target])
    x_enc = pd.get_dummies(x_raw, dtype=float)
    med = x_enc.median(numeric_only=True)
    x_enc = x_enc.fillna(med).fillna(0.0)
    return x_enc


def resolve_cv(task, y, requested):
    n = len(y)
    if task == "classification":
        min_class = int(y.value_counts().min())
        folds = min(requested, min_class)
        if folds < 2:
            raise ValueError(
                f"最小类别仅 {min_class} 个样本，无法做 {requested} 折分层交叉验证")
    else:
        folds = min(requested, n)
        if folds < 2:
            raise ValueError(f"样本量 {n} 过小，无法交叉验证")
    return folds


def run_benchmark(x_mat, y, task, folds, seed=42):
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import (cross_validate, StratifiedKFold, KFold)

    if task == "classification":
        scoring = {"accuracy": "accuracy", "f1_macro": "f1_macro"}
        splitter = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
        primary, higher_better = "f1_macro", True
    else:
        scoring = {"rmse": "neg_root_mean_squared_error", "r2": "r2"}
        splitter = KFold(n_splits=folds, shuffle=True, random_state=seed)
        primary, higher_better = "rmse", False

    rows = []
    for name, model in build_models(task).items():
        pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
        try:
            cv = cross_validate(pipe, x_mat, y, cv=splitter, scoring=scoring,
                                n_jobs=1, error_score="raise")
        except Exception as exc:
            rows.append({"model": name, "error": str(exc)[:200]})
            continue
        row = {"model": name,
               "fit_time_mean_s": round(float(np.mean(cv["fit_time"])), 4)}
        for key in scoring:
            vals = cv[f"test_{key}"]
            if key == "rmse":
                vals = -vals
            row[f"{key}_mean"] = round(float(np.mean(vals)), 4)
            row[f"{key}_std"] = round(float(np.std(vals)), 4)
        rows.append(row)

    ok = [r for r in rows if "error" not in r]
    ok.sort(key=lambda r: r[f"{primary}_mean"], reverse=higher_better)
    for rank, r in enumerate(ok, 1):
        r["rank"] = rank
    return ok + [r for r in rows if "error" in r], primary


def print_table(rows, task):
    if task == "classification":
        cols = ["rank", "model", "accuracy_mean", "accuracy_std",
                "f1_macro_mean", "f1_macro_std", "fit_time_mean_s"]
    else:
        cols = ["rank", "model", "rmse_mean", "rmse_std",
                "r2_mean", "r2_std", "fit_time_mean_s"]
    widths = [max(len(c), 6) for c in cols]
    widths[1] = max(widths[1], max((len(r["model"]) for r in rows), default=5))
    header = "  ".join(c.ljust(w) for c, w in zip(cols, widths))
    print(header)
    print("-" * len(header))
    for r in rows:
        if "error" in r:
            print(f"{'-'.ljust(widths[0])}  {r['model'].ljust(widths[1])}  运行失败: {r['error']}")
            continue
        cells = [str(r.get(c, "")) for c in cols]
        print("  ".join(c.ljust(w) for c, w in zip(cells, widths)))


def main():
    parser = argparse.ArgumentParser(
        description="算法基准测试：对 CSV 数据集运行 6 个 sklearn 常用模型的 K 折交叉验证，"
                    "输出指标 + 训练耗时排名表。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--data", required=True, help="输入 CSV 文件路径")
    parser.add_argument("--target", required=True, help="目标列名")
    parser.add_argument("--task", required=True,
                        choices=["classification", "regression"], help="任务类型")
    parser.add_argument("--cv", type=int, default=5, help="交叉验证折数")
    parser.add_argument("--output", default=None, help="JSON 报告输出路径（可选）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.data)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        print(f"[ERROR] 无法读取数据文件: {exc}", file=sys.stderr)
        return 2
    if args.target not in df.columns:
        print(f"[ERROR] 目标列 '{args.target}' 不在数据列中: {list(df.columns)}",
              file=sys.stderr)
        return 2

    df = df.dropna(subset=[args.target]).reset_index(drop=True)
    if len(df) < 10:
        print(f"[ERROR] 有效样本仅 {len(df)} 条，太少无法基准测试", file=sys.stderr)
        return 2
    y = df[args.target]
    if args.task == "regression" and not pd.api.types.is_numeric_dtype(y):
        print("[ERROR] regression 任务要求目标列为数值型", file=sys.stderr)
        return 2

    x_mat = prepare_features(df, args.target)
    try:
        folds = resolve_cv(args.task, y, args.cv)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    if folds != args.cv:
        print(f"[WARN] 折数从 {args.cv} 自动降为 {folds}（受样本/类别数限制）")

    print(f"== 基准测试: {os.path.basename(args.data)} | task={args.task} "
          f"| n={len(df)} | features={x_mat.shape[1]} | cv={folds} ==")
    rows, primary = run_benchmark(x_mat, y, args.task, folds, args.seed)
    print_table(rows, args.task)
    ok = [r for r in rows if "error" not in r]
    if ok:
        print(f"最优模型（按 {primary}）: {ok[0]['model']}")

    if args.output:
        report = {"data": args.data, "task": args.task, "target": args.target,
                  "n_samples": int(len(df)), "n_features": int(x_mat.shape[1]),
                  "cv_folds": folds, "primary_metric": primary, "results": rows}
        try:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"报告已写入: {args.output}")
        except OSError as exc:
            print(f"[ERROR] 报告写入失败: {exc}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
