# PoC Validation Gate（PoC 验证门禁）

> **用途**：定义候选方法的 PoC（Proof of Concept）验证标准，作为 Gate G2 的核心检查机制。
> **来源**：MathModeling-skills/CLAUDE.md + design-principles.md
> **版本**：v1.0
> **核心原则**：每个候选方法必须有 <= 30 行的 PoC 在真实数据上运行，产出可行性数字。没有 PoC 就不叫验证。

---

## 1. PoC 要求总览

### 什么是 PoC

PoC（Proof of Concept）是一个极简的代码片段，用于验证某个候选方法在真实数据上是否可行。它不是完整的实现，而是"这条路能不能走通"的快速验证。

### 为什么需要 PoC

> "Without a baseline, claims like 'better,' 'more accurate,' or 'more stable' are usually unsupported."
> — design-principles.md

同理，没有 PoC 的方法选择是"纸上谈兵"。PoC 的作用是：
- 在投入大量编码时间前验证方法可行性
- 产出具体的可行性数字，支撑 G2.5 人类决策
- 及早发现方法的致命缺陷，避免后期返工
- 为备选方案的切换提供数据依据

---

## 2. PoC 验证标准

### 核心要求

| 要求 | 标准 | 严重度 |
|------|------|--------|
| **代码行数** | <= 30 行（不含 import 和注释） | MEDIUM |
| **可行性数字** | 必须产出一个具体的数值结果 | CRITICAL |
| **真实数据** | 必须使用 `workspace/data_clean/` 中的清洗后数据 | HIGH |
| **可运行** | 代码必须能成功执行，无报错 | CRITICAL |
| **输出到文件** | 结果写入文件（而非仅打印到控制台） | HIGH |

### 可行性数字（Feasibility Number）

可行性数字是 PoC 的核心产出。它不是一个最终结果，而是一个"这条路走得通"的信号。

**合格的可行性数字**：
- 一个具体的数值（如 RMSE = 0.045, 准确率 = 82.3%）
- 一个排序结果（如 6 个城市的 TOPSIS 排名）
- 一个收敛信号（如迭代 50 步后损失下降到 0.01 以下）
- 一个相关性系数（如灰色关联度 r = 0.87）

**不合格的可行性数字**：
- "模型可以运行"（无数值）
- "效果不错"（无量化）
- "比基线好"（无数值对比）
- 空输出

### 30 行限制的计算方式

```python
# 不计入行数的部分：
# - import 语句
# - 空行
# - 纯注释行

# 计入行数的部分：
# - 数据加载和预处理代码
# - 模型核心逻辑
# - 结果输出代码

# 示例计数：
import numpy as np              # 不计入
import pandas as pd             # 不计入
                               # 不计入（空行）
# 加载数据                     # 不计入（注释）
df = pd.read_csv('data.csv')   # 计入 (1)
X = df.drop('target', axis=1)  # 计入 (2)
y = df['target']               # 计入 (3)
                               # 不计入（空行）
# 熵权计算                     # 不计入（注释）
def entropy_weight(X):         # 计入 (4)
    ...                        # 计入 (5-10)
                               # 不计入（空行）
# TOPSIS 排序                  # 不计入（注释）
def topsis(X, weights):        # 计入 (11)
    ...                        # 计入 (12-20)
                               # 不计入（空行）
# 输出结果                     # 不计入（注释）
result = topsis(X, weights)    # 计入 (21)
print(f'排名: {result}')       # 计入 (22)
np.savetxt('poc_result.csv',   # 计入 (23)
           result, delimiter=',')
# 总计：23 行（合格，<= 30）
```

---

## 3. PoC 文件规范

### 文件命名

```
methods/Qx/poc/<method_name>_poc.py
```

示例：
```
methods/Q1/poc/entropy_topsis_poc.py
methods/Q1/poc/ahp_topsis_poc.py
methods/Q2/poc/arima_poc.py
methods/Q2/poc/lstm_poc.py
```

### 文件结构

```python
"""
PoC: [方法名称] 验证
子问题: Qx
目的: 验证 [方法] 在 [数据] 上的可行性
"""
import numpy as np
import pandas as pd

# === 数据加载（不计入行数） ===
data = pd.read_csv('workspace/data_clean/Q1_data.csv')
X = data.drop('target', axis=1).values
y = data['target'].values

# === 核心方法实现（计入行数）===
# [方法核心逻辑，<= 30 行]

# === 结果输出（计入行数）===
result = [...]  # 可行性数字
np.savetxt('methods/Q1/poc/entropy_topsis_poc_result.txt',
           result, fmt='%.4f', header='feasibility_number')
print(f'PoC 可行性数字: {result[0]:.4f}')
```

### 结果文件

```
methods/Qx/poc/<method_name>_poc_result.txt
```

内容格式：
```
# PoC Result: [方法名称]
# Date: [运行时间]
# Data: [使用的数据文件]
# Feasibility Number: [数值]
[具体数值数据]
```

---

## 4. 失败 PoC 的处理

### 标记与归档

当 PoC 失败时（运行报错 / 无数值输出 / 结果不合理）：

1. **标记**：在方法候选文件中将该方法标记为 `[REJECTED]`

```markdown
## 候选方法列表

### M1: AHP-TOPSIS [REJECTED]
- PoC 文件: methods/Q1/poc/ahp_topsis_poc.py
- 失败原因: AHP 判断矩阵不一致，CR = 0.15 > 0.10
- 失败时间: 2026-06-21T10:30:00+08:00
```

2. **归档**：将 PoC 脚本、输出、相关图表移动到归档目录

```
workspace/archived/Q1/ahp_topsis_REJECTED_round1/
├── ahp_topsis_poc.py
├── ahp_topsis_poc_result.txt
└── error_log.txt
```

3. **记录**：在迭代日志中添加一条记录

```markdown
## methods/Q1/q1_method_iteration_log.md

### Round 1
- [REJECTED] AHP-TOPSIS: 判断矩阵一致性检验失败 (CR = 0.15)
- [CANDIDATE] Entropy-TOPSIS: PoC 通过，可行性数字 = 0.0342
- [CANDIDATE] CRITIC-TOPSIS: PoC 通过，可行性数字 = 0.0367
```

### 归档规则

- **主代码树永远干净**：`code/Qx/` 和 `methods/Qx/poc/` 中只保留 `[CANDIDATE]` 和 `[CHOSEN]` 方法
- **REJECTED 方法全部归档**：移至 `workspace/archived/Qx/<method>_REJECTED_roundN/`
- **保留失败原因**：归档目录中必须包含 `error_log.txt` 或在迭代日志中记录失败原因
- **不丢弃代码**：归档不是删除，未来可能需要参考失败尝试

### 触发切换条件

当以下情况发生时，触发备选方案评估：

| 触发条件 | 操作 |
|---------|------|
| 所有候选方法的 PoC 均 REJECTED | 回退到 G1，重新审视子问题拆解 |
| 首选方法 PoC 失败 | 启用备选方案，继续验证 |
| PoC 结果与预期严重不符 | 建模手评估是否调整方法方向 |
| 数据质量问题导致 PoC 失败 | 回退到 data-auditor-cleaner |

---

## 5. 与 method-selector skill 的集成

### 工作流程

```
method-selector 生成候选方法池
  ↓
为每个候选方法生成 PoC 脚本（<= 30 行）
  ↓
运行 PoC，收集可行性数字
  ↓
标记通过/失败，更新候选状态
  ↓
产出：methods/Qx/qx_method_candidates.md（含 PoC 结果）
  ↓
进入 G2 检查
```

### method-selector 的输出要求

method-selector skill 在生成候选方法时，必须为每个候选方法同时产出：

1. **方法描述**：方法名称、原理简介、适用条件
2. **PoC 脚本**：`methods/Qx/poc/<method>_poc.py`（<= 30 行）
3. **预期可行性数字**：预期结果的范围或目标值
4. **备选方案**：如果 PoC 失败，使用什么替代

### 候选方法文件格式

```markdown
# methods/Q1/q1_method_candidates.md

## 子问题 Q1: [描述]

### M1: Entropy-TOPSIS [CANDIDATE]
- **原理**: 熵权法确定客观权重 + TOPSIS 排序
- **适用条件**: 数据量适中，指标间无强共线性
- **PoC 文件**: methods/Q1/poc/entropy_topsis_poc.py (28 行)
- **可行性数字**: RMSE = 0.0342
- **PoC 状态**: PASS
- **备选方案**: M2 (CRITIC-TOPSIS)

### M2: CRITIC-TOPSIS [CANDIDATE]
- **原理**: CRITIC 法确定权重 + TOPSIS 排序
- **适用条件**: 指标间有对比强度和冲突性
- **PoC 文件**: methods/Q1/poc/critic_topsis_poc.py (25 行)
- **可行性数字**: RMSE = 0.0367
- **PoC 状态**: PASS
- **备选方案**: M3 (AHP-TOPSIS)

### M3: AHP-TOPSIS [REJECTED]
- **原理**: 层次分析法确定主观权重 + TOPSIS 排序
- **PoC 文件**: methods/Q1/poc/ahp_topsis_poc.py → workspace/archived/Q1/ahp_topsis_REJECTED_round1/
- **失败原因**: 判断矩阵一致性检验失败 (CR = 0.15 > 0.10)
- **PoC 状态**: REJECTED
```

---

## 6. Gate G2 检查清单

当 orchestrator 评估 Gate G2 时，按以下清单逐项检查：

### 对每个子问题 Qx

- [ ] `methods/Qx/qx_method_candidates.md` 存在
- [ ] 每个 `[CANDIDATE]` 方法有对应的 PoC 文件
- [ ] PoC 文件代码行数 <= 30（不含 import/注释/空行）
- [ ] PoC 文件使用 `workspace/data_clean/` 中的真实数据
- [ ] PoC 文件能成功运行，无报错
- [ ] PoC 产出可行性数字（写入结果文件）
- [ ] 可行性数字是具体数值（非空/非定性描述）
- [ ] `[REJECTED]` 方法已归档到 `workspace/archived/`
- [ ] 迭代日志 `methods/Qx/qx_method_iteration_log.md` 已更新

### 全局检查

- [ ] 所有子问题的 G2 均通过
- [ ] 至少每个子问题有 2 个 `[CANDIDATE]` 方法（不全是 REJECTED）
- [ ] 主代码树中无 `[REJECTED]` 方法残留

### 通过条件

所有子问题的所有检查项均通过 → G2 PASS

### 失败处理

任一检查项失败 → G2 FAIL → 回退到 method-selector skill 补充 PoC

---

## 7. PoC 最佳实践

### 做什么

- **先跑通再优化**：PoC 的目标是验证可行性，不是写出优雅代码
- **用真实数据**：模拟数据可能掩盖真实问题（缺失值、异常值、数据分布）
- **输出到文件**：便于后续检查和决策记录
- **记录失败原因**：为未来的备选方案提供参考
- **保留中间结果**：方便调试和复现

### 不做什么

- **不要超过 30 行**：如果需要更多代码，说明方法过于复杂，考虑简化
- **不要做完整实现**：PoC 是"能不能跑通"，不是"跑得好不好"
- **不要跳过数据预处理**：真实数据的脏数据会暴露方法的脆弱点
- **不要只看一个指标**：至少输出一个核心指标 + 一个辅助指标
- **不要在 PoC 中调参**：PoC 用默认参数，调参留给正式实现

### 常见失败模式

| 失败模式 | 表现 | 处理 |
|---------|------|------|
| 数据不匹配 | 方法要求的数据格式与实际不符 | 检查数据预处理，或更换方法 |
| 计算超时 | 方法在给定数据量下无法在合理时间内完成 | 简化方法或减小数据规模 |
| 数值不稳定 | 结果在不同随机种子下差异巨大 | 检查方法的数值稳定性 |
| 依赖缺失 | 需要的库未安装或版本不兼容 | 确认环境依赖 |
| 内存溢出 | 数据量超出方法的内存限制 | 简化方法或分批处理 |