#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""特征工程标准预处理 CLI。

按 SKILL.md 流程执行：缺失值处理 -> 异常值处理(可选 IQR 裁剪) -> 类别编码 -> 缩放。
输出清洗后 CSV + 处理报告 JSON。--target 指定的列不参与裁剪/编码/缩放（目标缺失的行直接删除）。
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd


def handle_missing(df, strategy, target, report):
    info = {"strategy": strategy, "filled": {}, "dropped_rows": 0}
    if target and target in df.columns:
        before = len(df)
        df = df.dropna(subset=[target])
        info["dropped_rows_target_na"] = before - len(df)
    if strategy == "drop":
        before = len(df)
        df = df.dropna()
        info["dropped_rows"] = before - len(df)
    else:
        num_cols = [c for c in df.select_dtypes(include=[np.number]).columns
                    if c != target]
        for col in num_cols:
            n_na = int(df[col].isna().sum())
            if n_na:
                fill = df[col].mean() if strategy == "mean" else df[col].median()
                df[col] = df[col].fillna(fill)
                info["filled"][col] = {"n": n_na, "value": round(float(fill), 6)}
        cat_cols = [c for c in df.columns
                    if c not in num_cols and c != target and df[c].isna().any()]
        for col in cat_cols:
            n_na = int(df[col].isna().sum())
            mode = df[col].mode()
            fill = mode.iloc[0] if not mode.empty else "unknown"
            df[col] = df[col].fillna(fill)
            info["filled"][col] = {"n": n_na, "value": str(fill), "method": "mode"}
    report["missing"] = info
    return df.reset_index(drop=True)


def handle_outliers_iqr(df, target, report):
    info = {"method": "iqr_clip", "clipped": {}}
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns
                if c != target]
    for col in num_cols:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr <= 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((df[col] < lower) | (df[col] > upper)).sum())
        if n_out:
            df[col] = df[col].clip(lower, upper)
            info["clipped"][col] = {"n": n_out,
                                    "lower": round(float(lower), 6),
                                    "upper": round(float(upper), 6)}
    report["outlier_iqr"] = info
    return df


def encode_categorical(df, method, target, report):
    cat_cols = [c for c in df.columns
                if c != target and (pd.api.types.is_string_dtype(df[c])
                                    or isinstance(df[c].dtype, pd.CategoricalDtype)
                                    or df[c].dtype == object)]
    info = {"method": method, "columns": cat_cols}
    if not cat_cols:
        report["encoding"] = info
        return df
    if method == "onehot":
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)
        info["new_columns"] = [c for c in df.columns
                               if any(c.startswith(f"{cc}_") for cc in cat_cols)]
    else:  # label
        mappings = {}
        for col in cat_cols:
            codes, uniques = pd.factorize(df[col].astype(str))
            df[col] = codes
            mappings[col] = {str(v): i for i, v in enumerate(uniques[:20])}
            if len(uniques) > 20:
                mappings[col]["..."] = f"共 {len(uniques)} 类，报告仅列前 20"
        info["mappings"] = mappings
    report["encoding"] = info
    return df


def scale_numeric(df, method, num_cols, target, report):
    cols = [c for c in num_cols if c != target and c in df.columns]
    info = {"method": method, "columns": cols}
    if method == "none" or not cols:
        report["scaling"] = info
        return df
    for col in cols:
        series = df[col].astype(float)
        if method == "standard":
            std = series.std(ddof=0)
            df[col] = 0.0 if std == 0 else (series - series.mean()) / std
        else:  # minmax
            rng = series.max() - series.min()
            df[col] = 0.0 if rng == 0 else (series - series.min()) / rng
    report["scaling"] = info
    return df


def main():
    parser = argparse.ArgumentParser(
        description="特征工程标准预处理：缺失值 -> 异常值(IQR 可选) -> 类别编码 -> 缩放，"
                    "输出清洗后 CSV + 处理报告 JSON。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input", required=True, help="输入 CSV 文件路径")
    parser.add_argument("--output", required=True, help="输出 CSV 文件路径")
    parser.add_argument("--target", default=None,
                        help="目标列名（可选；该列不参与裁剪/编码/缩放）")
    parser.add_argument("--missing", default="median",
                        choices=["mean", "median", "drop"], help="缺失值策略")
    parser.add_argument("--encode", default="onehot",
                        choices=["onehot", "label"], help="类别编码方式")
    parser.add_argument("--scale", default="none",
                        choices=["standard", "minmax", "none"], help="数值缩放方式")
    parser.add_argument("--outlier-iqr", action="store_true",
                        help="启用 IQR 异常值裁剪（Q1-1.5IQR ~ Q3+1.5IQR）")
    parser.add_argument("--report", default=None,
                        help="处理报告 JSON 路径（默认 <output>.report.json）")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        print(f"[ERROR] 无法读取输入文件: {exc}", file=sys.stderr)
        return 2
    if df.empty:
        print("[ERROR] 输入数据为空", file=sys.stderr)
        return 2
    if args.target and args.target not in df.columns:
        print(f"[ERROR] 目标列 '{args.target}' 不在数据列中: {list(df.columns)}",
              file=sys.stderr)
        return 2

    report = {"input": args.input, "output": args.output, "target": args.target,
              "shape_before": list(df.shape)}
    original_num_cols = [c for c in df.select_dtypes(include=[np.number]).columns]

    df = handle_missing(df, args.missing, args.target, report)
    if df.empty:
        print("[ERROR] 缺失值处理后数据为空（drop 策略删光了所有行）", file=sys.stderr)
        return 2
    if args.outlier_iqr:
        df = handle_outliers_iqr(df, args.target, report)
    else:
        report["outlier_iqr"] = {"method": "disabled"}
    df = encode_categorical(df, args.encode, args.target, report)
    df = scale_numeric(df, args.scale, original_num_cols, args.target, report)
    report["shape_after"] = list(df.shape)

    try:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        os.makedirs(out_dir, exist_ok=True)
        df.to_csv(args.output, index=False, encoding="utf-8-sig")
    except OSError as exc:
        print(f"[ERROR] 输出 CSV 写入失败: {exc}", file=sys.stderr)
        return 2

    report_path = args.report or f"{args.output}.report.json"
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"[ERROR] 报告写入失败: {exc}", file=sys.stderr)
        return 2

    print(f"预处理完成: {report['shape_before']} -> {report['shape_after']}")
    print(f"  缺失值策略={args.missing}, IQR裁剪={'开' if args.outlier_iqr else '关'}, "
          f"编码={args.encode}, 缩放={args.scale}")
    print(f"  输出 CSV: {args.output}")
    print(f"  处理报告: {report_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
