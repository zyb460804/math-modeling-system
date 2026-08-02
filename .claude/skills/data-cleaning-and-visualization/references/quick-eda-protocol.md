# 快速 EDA 协议（Quick Exploratory Data Analysis）

> **来源**：从 `csv-data-summarizer` v2.1.0（已归档）抽取核心方法论，整合进 data-cleaning-and-visualization。
> **用途**：拿到 CSV/Excel 数据后的**第一步**——立即自动分析，不问用户"你想干什么"。
> **配合**：`data-cleaning-and-visualization` skill 的数据清洗主流程。

---

## 核心原则

> **"THE USER WANTS A FULL ANALYSIS RIGHT AWAY - JUST DO IT."**

拿到数据文件后，**立即自动执行**完整 EDA，不问用户"你想分析什么"。这是 csv-data-summarizer 最独特的行为模式。

---

## 触发条件

| 场景 | 是否触发快速 EDA |
|------|----------------|
| 用户上传/放入 CSV/Excel 到 `problem_files/` | ✅ 立即执行 |
| 用户说"看看这个数据" | ✅ 立即执行 |
| 用户说"分析 XXX"（具体分析目标） | ❌ 走定向分析，不做全量 EDA |
| 已有 `data_plan.json` | ❌ 走正式数据清洗流程 |

---

## 快速 EDA 自动分析步骤（8 步）

### Step 1: 数据概览

```
- 文件名 / 文件大小 / 行数 / 列数
- 数据类型推断（数值/类别/日期/文本）
- 内存占用
```

### Step 2: 统计摘要

```
数值列：count / mean / std / min / 25% / 50% / 75% / max
类别列：count / unique / top / freq
日期列：范围 / 间隔 / 频率
```

### Step 3: 缺失值分析

```
每列缺失数量 + 缺失率
缺失模式判断（完全随机/条件随机/非随机）
可视化：缺失值热力图（msno matrix）
```

### Step 4: 数据分布

```
数值列：直方图 + KDE + 正态性检验
类别列：柱状图 + 频率表
可视化：分布网格图（每列一个子图）
```

### Step 5: 异常值检测

```
IQR 法：超出 [Q1-1.5*IQR, Q3+1.5*IQR] 的点
Z-score 法：|Z| > 3 的点
可视化：箱线图网格
```

### Step 6: 相关性分析

```
Pearson 相关系数矩阵
Spearman 秩相关（非线性关系）
可视化：相关性热力图 + 聚类
高相关对（|r| > 0.8）列出
```

### Step 7: 数据质量报告

```
- 重复行数量
- 常量列（std=0，无信息）
- 高基数类别列（unique > 50，可能是 ID）
- 混合类型列（数字+文本混合）
- 潜在数据质量问题清单
```

### Step 8: 建模建议

```
基于数据特征自动推断：
- 适合的题型（分类/回归/聚类/时序）
- 推荐的预处理步骤
- 潜在的特征工程方向
- 建议的验证策略
```

---

## 自动化脚本

```bash
python .claude/skills/data-cleaning-and-visualization/scripts/quick_eda.py \
  --input problem_files/data.csv \
  --output paper_output/step1/eda_report/
```

**产出**：

```
paper_output/step1/eda_report/
├── overview.json           ← Step 1-3 概览/统计/缺失
├── distributions/          ← Step 4 分布图
├── correlations/           ← Step 6 相关性图
├── quality_report.json     ← Step 7 质量报告
├── modeling_suggestions.md ← Step 8 建模建议
└── eda_summary.md          ← 全量 EDA 摘要（人类可读）
```

---

## 自适应分析

根据数据特征**智能调整**分析重点：

| 数据特征 | 自动加强 |
|---------|---------|
| 时序列（有日期列） | 趋势分解 + 季节性 + 平稳性检验 |
| 地理数据（有经纬度） | 空间分布图 + 地理聚类 |
| 高维数据（列 > 50） | 降维（PCA/t-SNE）+ 特征筛选 |
| 类别失衡 | 类别分布 + 重采样建议 |
| 多表关联 | 关联键检测 + JOIN 建议 |

---

## 与正式数据清洗流程的关系

```
数据进入 problem_files/
        │
        ▼
快速 EDA（本协议）         ← 立即自动执行，产出概览
        │
        ▼
data_plan.json（正式清洗计划）  ← 基于 EDA 结果制定
        │
        ▼
正式数据清洗（data-cleaning-and-visualization 主流程）
```

**关键区别**：
- 快速 EDA = **只读**，不改数据，只看数据长什么样
- 正式清洗 = **改数据**，处理缺失/异常/编码/缩放

---

## 禁止行为

- ❌ 问用户"你想分析什么"（直接全量分析）
- ❌ 只做统计摘要不做可视化（图比表更直观）
- ❌ 跳过建模建议（EDA 的价值在于指导后续建模）
- ❌ EDA 过程中修改原始数据（只读原则）
- ❌ EDA 结果不放 `paper_output/step1/eda_report/`（后续步骤找不到）