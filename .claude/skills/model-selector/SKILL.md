---
name: model-selector
description: "输入题型关键词，输出推荐模型+算法+风险评估+代码模板路径+PoC验证。基于 outputs/method_matching.md 和 outputs/model_selection_quick_table.md 智能路由。每个候选方法必须附带≤30行PoC代码在真实数据上运行。"
disable-model-invocation: true
---

# Model Selector — 智能选模助手（含PoC验证）

> **此 skill 是 `/analyze` 统一入口的内部调度工具。** 用户说"选模""推荐模型"等均由 `/analyze` 统一接收后分派。本 skill 保留独立触发词仅用于向后兼容。

> **v3.6 更新**：引入PoC验证门禁（Gate G2），每个候选方法必须附带≤30行PoC代码在真实数据上运行并产出具体结果。

## 设计理念

> "Teams often discover only near the deadline that a method they had counted on does not run on the real data, when it is too late to switch."

本skill的核心改进：
- 每个候选方法必须有**≤30行PoC代码**
- PoC必须在**真实清洗数据**上运行
- PoC必须产出**具体数值结果**
- PoC失败的方法标记**[REJECTED]**并归档

## 触发词

`选模` `推荐模型` `用什么算法` `模型选择` `建模路线`

## 工作流

### Step 1: 解析输入

从用户描述中提取：
- **题型**：评价 / 预测 / 优化 / 分类 / 聚类 / 图论 / 仿真 / 综合
- **数据特征**：表格 / 时序 / 网络 / 空间 / 文本，数据量大小
- **约束条件**：是否有实时性要求、可解释性要求、精度要求

### Step 2: 查询知识库

读取以下文件匹配最佳方案：
1. `outputs/method_matching.md` — 方法匹配表（11类任务×模型×算法×风险）
2. `outputs/model_selection_quick_table.md` — 快速选型表
3. `outputs/problem_type_taxonomy.md` — 题型分类学
4. `outputs/algorithm_templates.md` — 算法模板库

#### 扩展参考文档（按需加载）

以下文档来自 GitHub 社区集成（zhnnky329/Lupynow），按工作流阶段按需读取，**不要预加载全部文件**：

| 文档 | 路径 | 加载时机 | 用途 |
|------|------|---------|------|
| 95+场景决策矩阵 | `references/model-selection-matrix.md` | **Step 2 匹配场景特征时**：当题型/数据特征/约束条件组合在 `method_matching.md` 中无法精确匹配时加载 | 95+种场景×推荐模型×算法×风险的完整决策矩阵，覆盖长尾场景 |
| 12型问题分解法 | `references/problem-decomposition.md` | **Step 1 解析输入后**：当问题包含多个子问题或题型为"综合"时加载 | 12种标准问题分解模式，帮助将复杂赛题拆解为可独立建模的子问题 |
| 端到端Playbook | `references/playbooks/` | **Step 5 输出推荐后**：当用户要求"完整示例"或需要展示端到端流程时按题型加载 | 12个题型的端到端Playbook（从审题到代码到论文），每个playbook覆盖一种典型竞赛题型 |
| HMML 分层方法库 | `references/hmml/` | **Step 2 匹配方法时**：当需要按问题领域分层检索建模方法节点时加载 | NeurIPS 2025 MM-Agent，5 domain/18 subdomain/97 method 三层结构，与 model-selection-matrix 互补 |
| HMML 选模算法指南 | `references/hmml-retrieval-guide.md` | **Step 2 匹配方法时**：需要理解 actor-critic 自顶向下选模流程时加载 | MethodScorer 逐层打分 + top_k 检索方法论 |

**路由规则**：
- 场景匹配优先查 `model-selection-matrix.md`，其次查 `method_matching.md`
- 综合题型必须先用 `problem-decomposition.md` 拆解，再逐子问题选模
- Playbook 仅在用户明确要求示例或需要端到端参考时加载，按题型名匹配文件名（如 `playbooks/evaluation.md`、`playbooks/prediction.md`）

### Step 3: 生成候选方法（2-4个）

为每个子问题生成2-4个候选方法，每个方法必须包含：

```markdown
## 候选方法 A: [方法名称]

### 基本信息
- **模型类型**: [评价/预测/优化/...]
- **算法**: [具体算法名]
- **优势**: [简述]
- **风险**: [低/中/高]
- **代码模板**: [路径]

### PoC代码（≤30行）

```python
# [方法名称] PoC验证
# 文件: paper_output/methods/{Q}/poc/{method}_poc.py

import pandas as pd
import numpy as np
from pathlib import Path

# 加载真实清洗数据
data_path = Path("paper_output/data_cleaned/cleaned_data.csv")
data = pd.read_csv(data_path)

# [核心算法实现，≤30行]
# ...

# 输出具体结果
print(f"结果: {result}")
print(f"指标: {metric}")
```

### 预期输出
- **结果类型**: [数值/排名/分类/...]
- **关键指标**: [指标名] = [预期范围]
```

### Step 4: PoC验证（Gate G2 ★）

**这是关键门禁**：每个候选方法的PoC必须在真实数据上运行成功。

```bash
# 运行PoC验证
python paper_output/methods/{Q}/poc/{method}_poc.py
```

**验证标准**:
- ✅ **PASS**: 代码运行成功，产出具体数值结果
- ❌ **FAIL**: 代码运行失败或无具体输出

**PoC失败的处理**:
- 标记为 `[REJECTED]`
- 记录失败原因
- 自动归档到 `paper_output/archived/{Q}/{method}_REJECTED/`

### Step 5: 输出推荐

```markdown
## 选模推荐

### 题型判断
- 主题型：[X]
- 辅助题型：[Y]

### 候选方法（Gate G2 验证结果）

| 排名 | 模型 | 算法 | PoC状态 | 关键指标 | 风险 | 代码模板 |
|------|------|------|---------|----------|------|----------|
| 1 | ... | ... | ✅ PASS | [指标]=[值] | 低 | ... |
| 2 | ... | ... | ✅ PASS | [指标]=[值] | 中 | ... |
| 3 | ... | ... | ❌ FAIL | - | - | [REJECTED] |

### PoC失败方法
- **[方法名]**: [失败原因]

### 组合建议
- 主模型：[X] — [理由]
- 辅助模型：[Y] — [理由]
- 验证方法：[Z]

### 风险预警
- [从 model_specific_pitfalls.md 提取]

### 下一步（Gate G2.5：用户决策）
- **必须由用户选择最终方法并填写理由**
- 运行 `decision-logger` 记录决策
- 然后运行 `/algorithm-runner [推荐算法名]` 执行完整代码
```

## Gate G2: PoC验证门禁

### 验证规则

| 检查项 | 规则 | 严重度 |
|--------|------|--------|
| PoC文件存在 | 每个候选方法必须有PoC文件 | CRITICAL |
| PoC可运行 | PoC代码必须能成功运行 | CRITICAL |
| 有具体输出 | PoC必须产出具体数值结果 | CRITICAL |
| 使用真实数据 | PoC必须使用清洗后的真实数据 | HIGH |
| 代码行数≤30 | PoC代码不超过30行 | MEDIUM |

### PoC模板

```python
#!/usr/bin/env python3
"""
[方法名称] PoC验证
文件: paper_output/methods/{Q}/poc/{method}_poc.py
用途: 在真实数据上验证方法可行性，产出具体结果
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# ===== 配置 =====
Q_ID = "{Q}"  # 子问题编号
METHOD_NAME = "{method}"  # 方法名称
DATA_PATH = Path(f"paper_output/data_cleaned/cleaned_data.csv")
OUTPUT_PATH = Path(f"paper_output/methods/{Q_ID}/poc/{METHOD_NAME}_poc_result.json")

# ===== 加载数据 =====
print(f"加载数据: {DATA_PATH}")
data = pd.read_csv(DATA_PATH)
print(f"数据形状: {data.shape}")

# ===== 核心算法（≤20行） =====
# 在这里实现算法的核心逻辑
# ...

# ===== 输出结果 =====
result = {
    "method": METHOD_NAME,
    "question": Q_ID,
    "status": "SUCCESS",
    "metrics": {
        "main_metric": float(main_value),
        "secondary_metric": float(secondary_value)
    },
    "data_shape": list(data.shape)
}

# 保存结果
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"结果已保存: {OUTPUT_PATH}")
print(f"主要指标: {result['metrics']}")
```

## Gate G2.5: 用户决策门禁

**PoC验证完成后，必须由用户做出最终选择**：

1. 展示所有候选方法的PoC结果
2. 用户选择最终方法
3. 用户填写选择理由（≥50字）
4. 记录到 `decision-logger`

**关键规则**:
- AI不能代替用户做选择
- 理由不能为空或过于简短
- 理由必须包含具体的数据/问题特征分析

## REJECTED方法自动归档

当PoC验证失败时，自动执行：

```python
def archive_rejected_method(question_id: str, method_name: str, reason: str):
    """将淘汰方法归档"""
    src = f"paper_output/methods/{question_id}/{method_name}"
    dst = f"paper_output/archived/{question_id}/{method_name}_REJECTED"

    # 创建归档目录
    Path(dst).mkdir(parents=True, exist_ok=True)

    # 移动PoC文件
    poc_src = f"{src}/poc/{method_name}_poc.py"
    poc_dst = f"{dst}/{method_name}_poc.py"
    if Path(poc_src).exists():
        Path(poc_src).rename(poc_dst)

    # 记录归档原因
    with open(f"{dst}/rejection_reason.md", "w", encoding="utf-8") as f:
        f.write(f"# 方法淘汰记录\n\n")
        f.write(f"**方法**: {method_name}\n")
        f.write(f"**子问题**: {question_id}\n")
        f.write(f"**淘汰时间**: {datetime.now().isoformat()}\n")
        f.write(f"**淘汰原因**: {reason}\n")
```

## 输出目录结构

```
paper_output/
├── methods/
│   └── {Q}/
│       ├── {Q}_method_candidates.md    # 候选方法列表
│       └── poc/
│           ├── method_a_poc.py         # 方法A的PoC
│           ├── method_a_poc_result.json # 方法A的PoC结果
│           ├── method_b_poc.py         # 方法B的PoC
│           └── method_b_poc_result.json # 方法B的PoC结果
├── archived/
│   └── {Q}/
│       └── method_c_REJECTED/          # 淘汰方法归档
│           ├── method_c_poc.py
│           └── rejection_reason.md
└── qa/
    └── decision_log.json               # 用户决策日志
```

## 与其他skill的关系

```
                    ┌─────────────────────┐
                    │ problem-doc-model-   │
                    │ selector             │
                    └──────────┬──────────┘
                               │ 题意分析
                               ▼
                    ┌─────────────────────┐
                    │   model-selector     │ ← 你在这里
                    │   (含PoC验证)        │
                    └──────────┬──────────┘
                               │ 候选方法 + PoC结果
                               ▼
                    ┌─────────────────────┐
                    │   decision-logger    │ ← Gate G2.5
                    │   (用户决策)         │
                    └──────────┬──────────┘
                               │ 用户选择
                               ▼
                    ┌─────────────────────┐
                    │ model-code-generator │
                    │ (完整代码)           │
                    └─────────────────────┘
```

## 约束

- 不编造算法，只推荐知识库中已有的方案
- 明确标注每个推荐的风险等级（低/中/高）
- 如果题型不确定，给出 2-3 种可能的题型判断
- **每个候选方法必须有PoC代码**
- **PoC必须在真实数据上运行**
- **PoC失败的方法必须标记[REJECTED]并归档**
- **最终选择必须由用户做出并记录理由**

## 版本历史

- v1.0.0: 初始版本，基础选模推荐
- v2.0.0: 添加PoC验证门禁（Gate G2）
- v2.1.0: 添加用户决策门禁（Gate G2.5）
- v2.2.0: 添加REJECTED自动归档机制