---
name: context-memory-keeper
description: "Manages persistent memory with 3-layer architecture (Working/Short-term/Long-term) and knowledge graph integration. Inspired by GBrain memory layer + Karpathy cross-referencing. 触发词：记忆架构、memory keeper、三层记忆、知识图谱、工作记忆、长期记忆、上下文记忆、记忆管理。"
---

# Context Memory Keeper v2.0

> **升级来源：** Garry Tan GBrain（记忆分层） + Karpathy LLM Wiki（交叉引用）
> **变更摘要：** 2 层 → 3 层记忆；增加知识图谱集成；增加实体追踪；增加交叉引用导航。

## 执行契约

- 上游输入：当前赛题约束、模型路线、数据源、图表路径、QA 结论、用户新增偏好、知识图谱实体。
- 必须输出：更新后的 `memoryskill.md`（3 层结构）；当短期工作台过长时，将旧任务摘要归档到 `memory_archive.md`；更新 `memory_entity_index.md` 中的实体追踪。
- 下游交接：其他 skill 在复杂任务开始前读取 `memoryskill.md`，避免遗忘当前模型路线、数据来源和用户要求。需要跨文件导航时查询 `outputs/knowledge_graph.md`。
- 推荐下一步：完成记忆更新后回到调用它的当前 skill；若目标是完整论文，回到 `paper-workflow-orchestrator` 判断后续阶段。
- 失败回退：若无法安全更新记忆文件，应在本轮回复中明确保留关键结论，并提示后续手动补写到记忆文件。

---

## 三层记忆架构

### Layer 1: 工作记忆（Working Memory）
- **文件：** `memoryskill.md` → `## 0. 工作记忆` 区块
- **生命周期：** 单次对话/单个子任务（~30 分钟自动衰减）
- **内容：** 当前正在处理的文件路径、临时变量、中间计算结果、正在调试的错误
- **容量上限：** 20 行，超出立即压缩
- **特点：** 频繁读写，每个 agent 调用都可能更新

### Layer 2: 短期任务台（Short-Term Workbench）
- **文件：** `memoryskill.md` → `## 2. 短期工作台` 区块
- **生命周期：** 单个赛题/竞赛周期（数天）
- **内容：** 当前赛题状态、模型路线、数据来源、QA 进度、图表清单、用户临时偏好
- **容量上限：** 80 行，阶段性完成 → 归档到 `memory_archive.md`
- **特点：** 阶段切换时更新，保持关键结论、丢弃过程日志

### Layer 3: 长期准则（Long-Term Principles）
- **文件：** `memoryskill.md` → `## 1. 长期准则` 区块
- **生命周期：** 跨赛题、跨赛季（永久/半永久）
- **内容：** 用户角色、全局约束、写作风格偏好、红线规则、评分标准锚点
- **容量上限：** 40 行，仅在用户明确要求时修改
- **特点：** 只读为主，稳定不变

### Layer 4（可选）: 实体追踪索引
- **文件：** `memory_entity_index.md`
- **生命周期：** 跨赛题积累
- **内容：** 历次竞赛用过的 MODEL/ALGORITHM/CODE/RESULT 实体，带双向引用
- **用途：** 快速查找"上次用过什么模型""哪个代码验证过"

---

## 文件结构

```
.claude/skills/context-memory-keeper/
├── SKILL.md                  ← 本文件（架构说明 + 使用规范）
├── memoryskill.md            ← 三层记忆主文件（活跃记忆）
├── memory_archive.md         ← 归档（已完成任务的详情）
└── memory_entity_index.md    ← 实体追踪索引（知识图谱的实例化）
```

---

## When to Invoke

### Read（读取记忆）
- 每次开始复杂任务前，读取 `memoryskill.md`
- 感到上下文模糊时（模型路线忘了、数据来源不清）
- 跨 skill 切换时，确认当前阶段

### Update（更新记忆）

| 层级 | 触发时机 | 操作 |
|------|----------|------|
| 工作记忆 | 每个子步骤完成 | 更新当前文件路径、临时变量 |
| 短期工作台 | 阶段完成（审题/建模/数据/代码/QA/写作） | 更新进度、关键结论 |
| 长期准则 | 用户修改全局规则/偏好 | 更新对应条目 |
| 实体索引 | 使用了新的 MODEL/ALGORITHM/CODE | 追加实体记录 |

### Archive（归档压缩）
- 当 `memoryskill.md` 超过 **100 行** 时，**必须**执行压缩
- 归档流程：
  1. 工作记忆 → 阶段完成后**直接清空**
  2. 短期工作台 → 已完成阶段的细节 → 剪切到 `memory_archive.md`
  3. 长期准则 → 一般不动
  4. 保留原则：用户红线 > 项目骨架 > 活跃阻塞项

---

## 压缩策略（Compression Policy）

### 触发条件
- `memoryskill.md` 总行数 > 100
- 或单个子任务结束

### 保留优先级
1. **P0 用户红线**：用户强烈要求的命令、偏好、禁止项
2. **P0 活跃阻塞**：正在阻碍当前任务的问题
3. **P1 项目骨架**：当前赛题的模型路线、数据来源、关键路径
4. **P2 阶段结论**：已完成阶段的核心结论（非过程日志）

### 丢弃/归档规则
- 过程性日志 → `memory_archive.md` 或直接删除
- 已完成任务的执行细节 → `memory_archive.md`
- 已失效的临时变量 → 直接删除
- 重复信息 → 保留最新版本，删除旧版

---

## 与知识图谱的集成

### 读取时
- 在 `outputs/knowledge_graph.md` 中查找当前赛题类型的建模路径
- 在 `memory_entity_index.md` 中查找历史用过的同类模型

### 写入时
- 使用了新的 MODEL/ALGORITHM → 更新 `memory_entity_index.md`
- 发现新的模型链/组合 → 建议更新 `outputs/knowledge_graph.md`
- 案例完成 → 触发 `outputs/case_feedback_loop.md` 回灌

### 交叉引用格式（Karpathy 风格）
在记忆文件中使用 `→` 标注引用关系：
```
- 当前模型: TOPSIS → 代码: resources/04_代码模板/14种国赛必备算法源代码/14种国赛必备算法Python源代码/评价类 - TOPSIS 法.py
- 评分标准: → outputs/scoring_rubric.md（100分制7维度）
- 避坑提醒: → outputs/algorithm_selection_red_flags.md#熵权法
```

---

## Usage Tips

- 保持 `memoryskill.md` 轻量（< 100 行），随时可快速读取
- 工作记忆要**极度精简**——只放当前正在处理的东西
- 短期工作台放**结论**，不放**过程**——"模型已选定为TOPSIS"而非"我们考虑了5个模型最后选了TOPSIS因为..."
- 长期准则要**稳定**——除非用户明确要求，否则不动
- 实体索引要**持续积累**——每次用到新模型/算法都记录，这是跨赛题复用的基础
- 归档是**自动触发**的动作——超 100 行就必须压缩，不要等到“感觉差不多了”

## 新增脚本（v4.2）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/freshness_check.py` | SHA-256 报告新鲜度校验——源（problem_files/code）变化后旧报告标记 STALE | "报告新鲜度" / "校验报告过期" |

融合自 yushui2022。`freshness_check.py record <报告>` 写入 source_hash，`freshness_check.py check` 比对所有报告。防止输入/代码变了还用旧结论。