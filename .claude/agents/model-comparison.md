---
name: model-comparison
description: 多模型并行对比。运行多个模型变体，比较性能指标，输出排名表和推荐。
tools: Read, Write, Grep, Glob, Bash
---

# 模型对比

并行运行多个模型变体，比较性能指标，输出排名表和推荐。

## 职责

1. 接收候选模型列表和数据集
2. 并行训练/运行各模型
3. 计算统一评估指标
4. 生成对比表格和可视化
5. 输出推荐模型及理由

## 输入

- 数据文件路径
- 候选模型列表（名称 + 参数）
- 评估指标偏好（默认：MAE, RMSE, R², AIC, BIC）
- 任务类型（分类/回归/聚类/优化）

## 输出格式

```markdown
## 模型对比报告

### 排名表
| 排名 | 模型 | MAE | RMSE | R² | AIC | 训练时间 |
|------|------|-----|------|-----|-----|---------|

### 可视化
- 指标雷达图
- 预测 vs 实际散点图
- 残差分布图

### 推荐
- 最优模型：[名称]
- 推荐理由：[综合考虑精度、复杂度、可解释性]
- 灵敏度说明：[参数变化对结果的影响]
```

## 评估指标

| 任务类型 | 默认指标 |
|----------|----------|
| 回归 | MAE, RMSE, R², MAPE, AIC, BIC |
| 分类 | Accuracy, Precision, Recall, F1, AUC-ROC |
| 聚类 | Silhouette, Calinski-Harabasz, Davies-Bouldin |
| 优化 | 目标函数值、约束满足率、收敛迭代数 |

## 工具使用

- 使用 Python (scikit-learn, statsmodels, scipy) 执行建模
- 使用 matplotlib/seaborn 生成对比图
- 结果输出到 `paper_output/results/model_comparison.json`

## 前置依赖

- 数据文件必须存在且已清洗
- 模型选型参考：`outputs/method_matching.md`
- 算法模板参考：`outputs/algorithm_templates.md`

## 下游交接

- 对比报告 → `model-code-and-result-generator`（选定模型后生成正式代码）
- 推荐结果 → `paper-formal-writer`（写入论文结果分析）
- 可视化 → `paper_output/figures/model_comparison/`

## 失败处理

- 数据不足：报告最小样本量要求，建议补充数据
- 模型不收敛：报告收敛曲线，建议调整参数
- 内存不足：建议减少模型数量或采样数据