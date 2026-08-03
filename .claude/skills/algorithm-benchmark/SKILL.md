---
name: algorithm-benchmark
description: "算法基准测试：比较不同算法的性能、精度、速度。参考 szilard/benchm-ml 设计。触发词：算法基准测试、benchmark、比较算法性能、算法对比、精度速度对比、算法选型对比、多模型对比。"
---

# 算法基准测试（Algorithm Benchmark）

> **版本**: v1.0 | **更新**: 2026-06-21
> **来源**: 参考 szilard/benchm-ml 设计

---

## 设计理念

算法基准测试用于比较不同算法的性能，帮助选择最适合特定问题的算法。本skill提供：
- 评价类算法基准测试
- 预测类算法基准测试
- 优化类算法基准测试
- 分类类算法基准测试

---

## 基准测试清单

### 1. 评价类算法

| 算法 | 适用场景 | 指标 |
|------|---------|------|
| TOPSIS | 多指标评价 | 综合得分 |
| AHP | 层次分析 | 一致性比率 |
| 熵权法 | 客观赋权 | 权重 |
| 灰色关联 | 小样本评价 | 关联度 |
| 模糊综合评价 | 不确定性评价 | 隶属度 |

### 2. 预测类算法

| 算法 | 适用场景 | 指标 |
|------|---------|------|
| ARIMA | 时序预测 | RMSE, MAE |
| LSTM | 复杂时序 | RMSE, MAE |
| 灰色预测 | 小样本预测 | 后验差比 |
| 回归分析 | 线性关系 | R², RMSE |
| 随机森林 | 非线性关系 | RMSE, MAE |

### 3. 优化类算法

| 算法 | 适用场景 | 指标 |
|------|---------|------|
| 线性规划 | 线性约束 | 目标函数值 |
| 整数规划 | 离散变量 | 目标函数值 |
| 遗传算法 | 复杂优化 | 收敛代数 |
| 粒子群优化 | 连续优化 | 收敛速度 |
| 模拟退火 | 全局优化 | 解质量 |

---

## 基准测试脚本

### 评价类算法基准测试

```python
# .claude/skills/algorithm-benchmark/scripts/benchmark_evaluation.py

import time
import numpy as np
import pandas as pd
from typing import Any

def benchmark_topsis(data: np.ndarray, weights: np.ndarray) -> dict:
    """TOPSIS算法基准测试"""
    start_time = time.time()

    # 标准化
    norm_data = data / np.sqrt(np.sum(data**2, axis=0))

    # 加权
    weighted_data = norm_data * weights

    # 理想解和负理想解
    ideal = np.max(weighted_data, axis=0)
    negative_ideal = np.min(weighted_data, axis=0)

    # 距离
    d_pos = np.sqrt(np.sum((weighted_data - ideal)**2, axis=1))
    d_neg = np.sqrt(np.sum((weighted_data - negative_ideal)**2, axis=1))

    # 综合得分
    scores = d_neg / (d_pos + d_neg)

    elapsed = time.time() - start_time

    return {
        "algorithm": "TOPSIS",
        "scores": scores.tolist(),
        "ranking": np.argsort(-scores).tolist(),
        "time_seconds": elapsed
    }


def benchmark_ahp(comparison_matrix: np.ndarray) -> dict:
    """AHP算法基准测试"""
    start_time = time.time()

    n = comparison_matrix.shape[0]

    # 计算权重
    eigenvalues, eigenvectors = np.linalg.eig(comparison_matrix)
    max_idx = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, max_idx].real
    weights = weights / weights.sum()

    # 一致性检验
    lambda_max = eigenvalues[max_idx].real
    CI = (lambda_max - n) / (n - 1)
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]
    CR = CI / RI[n-1] if n <= 9 else CI

    elapsed = time.time() - start_time

    return {
        "algorithm": "AHP",
        "weights": weights.tolist(),
        "consistency_ratio": CR,
        "is_consistent": CR < 0.1,
        "time_seconds": elapsed
    }


def benchmark_entropy(data: np.ndarray) -> dict:
    """熵权法基准测试"""
    start_time = time.time()

    # 标准化
    norm_data = data / data.sum(axis=0)

    # 计算熵值
    k = 1 / np.log(len(data))
    entropy = -k * np.sum(norm_data * np.log(norm_data + 1e-10), axis=0)

    # 计算权重
    weights = (1 - entropy) / (1 - entropy).sum()

    elapsed = time.time() - start_time

    return {
        "algorithm": "Entropy",
        "weights": weights.tolist(),
        "entropy_values": entropy.tolist(),
        "time_seconds": elapsed
    }


def run_benchmark(data: np.ndarray, algorithms: list = None) -> dict:
    """运行基准测试"""
    if algorithms is None:
        algorithms = ["topsis", "entropy"]

    results = {}

    if "topsis" in algorithms:
        weights = np.ones(data.shape[1]) / data.shape[1]
        results["topsis"] = benchmark_topsis(data, weights)

    if "entropy" in algorithms:
        results["entropy"] = benchmark_entropy(data)

    return {
        "data_shape": data.shape,
        "algorithms": algorithms,
        "results": results
    }
```

---

## 使用方式

> 说明：上方 TOPSIS/AHP/熵权代码块为**参考实现**，供复制进赛题专用代码使用。
> 实际脚本 `scripts/benchmark_evaluation.py` 做的是**监督学习模型基准测试**：
> 对 CSV 数据集运行 6 个 sklearn 常用模型的 K 折交叉验证（分类：LogisticRegression/
> DecisionTree/RandomForest/GradientBoosting/KNN/SVM；回归：LinearRegression/Ridge/
> DecisionTree/RandomForest/GradientBoosting/KNN），输出指标 + 训练耗时排名表。

```bash
# 分类任务基准测试（5 折 CV，指标 accuracy + f1_macro）
python .claude/skills/algorithm-benchmark/scripts/benchmark_evaluation.py \
  --data paper_output/data_cleaned/data.csv \
  --target label --task classification \
  --output paper_output/results/benchmark_report.json

# 回归任务基准测试（指标 RMSE + R2）
python .claude/skills/algorithm-benchmark/scripts/benchmark_evaluation.py \
  --data paper_output/data_cleaned/data.csv \
  --target y --task regression \
  --output paper_output/results/benchmark_report.json
```

可选参数：`--cv 5`（折数，样本/类别不足时自动降低）、`--seed 42`。
非数值特征自动 one-hot，缺失值中位数填充，Pipeline 内统一标准化。

---

## 输出格式

```json
{
  "data": "paper_output/data_cleaned/data.csv",
  "task": "classification",
  "target": "label",
  "n_samples": 120,
  "n_features": 5,
  "cv_folds": 5,
  "primary_metric": "f1_macro",
  "results": [
    {
      "model": "RandomForest",
      "rank": 1,
      "accuracy_mean": 0.875, "accuracy_std": 0.0527,
      "f1_macro_mean": 0.8724, "f1_macro_std": 0.0552,
      "fit_time_mean_s": 0.1467
    }
  ]
}
```

---

## 版本历史

- v1.0.0 (2026-06-21): 初始版本，参考 szilard/benchm-ml 设计