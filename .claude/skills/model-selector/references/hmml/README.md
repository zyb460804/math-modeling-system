# HMML — Hierarchical Mathematical Modeling Library

> 来源：[usail-hkust/LLM-MM-Agent](https://github.com/usail-hkust/LLM-MM-Agent)（NeurIPS 2025）
> 落地版本：v4.6 融合（只做加法，不改骨架）

## 这是什么

HMML（分层数学建模方法库）是 MM-Agent 论文配套的方法知识树，将数学建模常用方法组织为 **Domain → Subdomain → Method** 的分层结构，每个节点附带 `<modeling_method>` / `<core_idea>` / `<application>` 三段式描述。

### 数据规模

| 层级 | 数量 | 说明 |
|------|------|------|
| Domain（领域） | **5** | 运筹学、优化方法、机器学习、预测、评价方法 |
| Level-2 节点（子领域/类别） | **18** | 部分为 Subdomain（含子类别），部分为直接 Category（直接挂 Method 叶子） |
| Method 叶子节点 | **97** | 每个节点含方法名 + 建模思路 + 核心思想 + 应用场景描述 |

> 注：部分分支存在第 4 层 Category（如 Programming Theory → Linear Programming → LP/IP/MIP），整体呈不规则多叉树。

### 五大领域一览

| # | Domain | Level-2 节点数 | Method 数 |
|---|--------|---------------|-----------|
| 1 | Operations Research（运筹学） | 3 | 25 |
| 2 | Optimization Methods（优化方法） | 5 | 23 |
| 3 | Machine Learning（机器学习） | 5 | 22 |
| 4 | Prediction（预测） | 2 | 12 |
| 5 | Evaluation Methods（评价方法） | 3 | 15 |

## 文件清单

| 文件 | 说明 |
|------|------|
| `HMML.json` | 结构化方法树（原样复制自 MM-Agent，未修改任何内容） |
| `HMML.md` | 人类可读的 Markdown 版方法树（原样复制，323 行） |
| `README.md` | 本文件 |

## 如何在选模时使用

### 检索流程（自顶向下逐层下钻）

```
1. 确定问题领域（Domain）
   ↓  读题 → 判断属于运筹/优化/ML/预测/评价中的哪个（或哪几个）
2. 下钻到子领域（Subdomain / Category）
   ↓  在 Domain 内按问题特征缩小范围
3. 选择具体方法（Method 叶子）
   ↓  查看 <core_idea> 和 <application> 判断适用性
4. 产出候选方法清单
   →  交给 model-selector Step 3（生成候选方法 + PoC 验证）
```

### 两种检索方式

1. **人工查阅**：直接读 `HMML.md`，按 Markdown 标题层级（`##` → `###` → `####` → `-`）逐层浏览。
2. **算法检索**：参照 `../hmml-retrieval-guide.md` 中的 MethodScorer 算法，对每个节点按问题描述打分，取 top-k 方法。MM-Agent 原始实现支持 embedding 相似度和 LLM 批判两种打分模式。

## 与 model-selection-matrix.md 的互补关系

| 维度 | `model-selection-matrix.md` | HMML |
|------|----------------------------|------|
| **组织方式** | 场景 → 算法直查（扁平矩阵） | 问题 → 领域 → 方法（分层树） |
| **检索路径** | 根据场景特征直接定位推荐模型 | 先定 Domain，再逐层下钻 |
| **信息粒度** | 每行 = 场景 + 候选A vs 候选B + 风险 + 决策依据 | 每节点 = 建模思路 + 核心思想 + 应用场景 |
| **适用场景** | 已知问题特征，需要快速匹配算法 | 需要理解方法体系全貌，或需要方法级描述来辅助判断 |
| **批判机制** | 冲突裁决规则（题目特征/规模/用户背景优先级） | 可选 LLM 批判打分（actor-critic） |

**协同用法**：先用 `model-selection-matrix.md` 快速定位候选算法，再用 HMML 的方法节点描述（`<core_idea>` / `<application>`）加深理解、辅助 PoC 设计；或先用 HMML 确定领域方向，再用 matrix 精确匹配具体场景。

## 与 analyze skill 的衔接

```
/analyze（统一审题选模入口）
  ├─ 题型判断 + 模型路线  ← analyze 的核心能力
  ├─ HMML 方法节点检索     ← 本库提供方法级知识
  │    └─ 输出：候选方法 + 建模思路 + 应用场景
  └─ model-selection-matrix ← 场景级精确匹配
       └─ 输出：场景 → 推荐算法 + 风险
```

`/analyze` 做顶层题型判断和路线规划，HMML 在 Step 2（匹配方法）阶段提供方法节点级的分层检索和描述，两者互补不冲突。
