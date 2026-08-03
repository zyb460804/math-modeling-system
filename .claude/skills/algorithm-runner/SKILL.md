---
name: algorithm-runner
description: 一键运行算法模板：匹配算法名→适配数据→执行→输出结果JSON。扫描 resources/04_代码模板/ 自动执行。触发词：运行算法、执行代码、跑算法、algorithm runner、算法执行、跑模板、一键运行。
disable-model-invocation: true
---

# Algorithm Runner — 算法执行器

从 64+ 算法模板中匹配目标算法，适配数据并执行。

> **与 code skill 的区别**：本 skill 执行已有算法模板；`code` skill 从零生成新代码。如需从零写代码而非执行已有模板，走 `/code`。

## 触发词

`运行算法` `执行代码` `跑一下XX算法` `算法测试` `代码运行`

## 工作流

### Step 1: 匹配算法

根据用户输入的算法名，在以下目录中搜索：
- `resources/04_代码模板/14种国赛必备算法源代码/` — 14 种
- `resources/04_代码模板/50多种常用算法源代码/` — 50+ 种
- `resources/04_代码模板/2025国赛创新型算法源代码/` — 创新型
- `paper_output/code/` — 赛题专用代码

匹配策略：精确匹配 > 模糊匹配 > 同义词匹配

### Step 2: 适配数据

- 读取数据文件（CSV/Excel/JSON）
- 对比算法模板的数据格式要求
- 自动适配列名、数据类型、缺失值处理

### Step 3: 执行

```python
# 伪代码
subprocess.run(["python", algorithm_script, "--data", data_path, "--output", output_path])
```

### Step 4: 输出结果

```markdown
## 算法执行报告

### 算法信息
- 名称：[X]
- 来源：[模板路径]
- 语言：Python / Matlab

### 执行结果
- 状态：成功 / 失败
- 运行时间：X 秒
- 输出文件：[路径]

### 结果摘要
- [关键指标和数值]

### 下一步
- 运行 `/chart-recommender` 可视化结果
- 运行 `quality-assurance-auditor/scripts/check_result_reasonableness.py` 验证结果合理性（参考 `result-validation-rules.md` 规则集，v4.8 整合自 result-validator）
```

## 可用算法速查

| 类别 | 算法 |
|------|------|
| 评价 | TOPSIS, AHP, 熵权法, 模糊综合评价, DEA, 秩和比 |
| 预测 | ARIMA, 灰色预测, LSTM, Prophet, XGBoost, LightGBM |
| 优化 | 遗传算法, 粒子群, 模拟退火, NSGA-II, 线性规划, 整数规划 |
| 分类 | 随机森林, SVM, KNN, 逻辑回归, BP神经网络 |
| 聚类 | K-means, DBSCAN, 层次聚类, SOM |
| 图论 | Dijkstra, Floyd, 最小生成树, 网络流 |
| 仿真 | 蒙特卡洛, 排队论, 系统动力元, 元胞自动机 |