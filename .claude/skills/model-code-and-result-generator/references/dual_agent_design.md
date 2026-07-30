# 双 Agent 协同设计：推导 ↔ 编码 解耦

> 融合自 `Hyde-yd/MathModeling-AI-Agent`（6★，双 Agent 协同系统）。
> 源设计：Agent1 负责赛题分析、论文框架、LaTeX 公式推导；Agent2 负责模型优选、Python 代码自动生成。
> 本项目当前是单 orchestrator 串行，本文档评估解耦为双轨并行的可行性与落点。

## 为什么考虑解耦

当前 `paper-workflow-orchestrator` 串行调度 problem-doc-model-selector → model-code-and-result-generator → paper-formal-writer。
对于**多子问题**赛题（如 4 问的 C 题），串行会让推导与编码互相阻塞：
- 问题二的推导必须等问题一编码完成
- 但问题二的数学推导其实不依赖问题一的代码

解耦后：推导轨（Agent-D）和编码轨（Agent-C）可按子问题粒度并行。

## 双轨职责

### Agent-D（Derivation 推导轨）
- 赛题分析、假设设定、变量定义
- **数学模型推导**（公式、约束、目标函数）→ 输出 `paper_output/plan/derivation_Q{n}.md`
- LaTeX 公式编排（配合 latex-renderer / typst-renderer）
- 灵敏度分析的理论设计
- **不写代码**，只产出数学规格（类似 AutoMCM-Pro MANUAL 模式的 SPEC）

### Agent-C（Coding 编码轨）
- 接收 Agent-D 的数学规格 → 选具体算法 → 生成 Python/MATLAB 代码
- 运行代码、生成结果契约 `results/Q{n}.json`
- **强制自证**（G4.6：每个模型配 verify_*.py）
- 数值合理性检查（check_numeric_sanity）

## 并行调度（用 pipeline_manager.py 并行阶段）

```
S2_modeling_route (approved)
        │
        ├─→ parallel-start: derivation_Q1  derivation_Q2  derivation_Q3  derivation_Q4
        │       (Agent-D ×4 并行推导)
        │
        ├─→ 每个 derivation_Qn approved 后，立即 start coding_Qn (Agent-C)
        │       (推导完成一个，编码启动一个，流水线并行)
        │
        └─→ parallel-all-done: coding_Q1 coding_Q2 coding_Q3 coding_Q4
                → S5_evidence_gate
```

## 交付契约（两轨交接）

Agent-D → Agent-C 通过 `derivation_Q{n}.md` 交接，格式对齐 AutoMCM-Pro 的 MANUAL_SPEC：

```markdown
## [MANUAL_SPEC] 问题 n
- 模型类型: 非线性规划
- 决策变量: x1(产量), x2(配比), ...
- 目标函数: min f(x) = ...   （LaTeX）
- 约束条件:
  - g1(x) ≤ 0
  - g2(x) = 0
- 求解方法建议: scipy.optimize.minimize, method='SLSQP'
- 期望输出: 最优解 x*, 最优值 f*, 灵敏度 ∂f/∂x_i
```

Agent-C 必须按此规格实现，不自行改模型结构（对齐 AutoMCM-Pro MANUAL 模式约束）。

## 与 4 层容错的配合

- Agent-C 编码失败（L1 重试 3 轮未过）→ 可回退到 Agent-D 重新推导（L2 Fallback Hand Off 的跨轨版本）
- Agent-D 推导有误 → Agent-C 的 verify_*.py 会捕获物理不合理 → 反向触发 Agent-D 修正

## 落点（不新建 agent，用现有 skill 编排）

本项目不需要新建独立进程；用 `pipeline_manager.py` 的并行阶段 + `paper-workflow-orchestrator` 的子问题分支即可实现：
- `problem-doc-model-selector` 承担 Agent-D 的分析部分
- `model-code-and-result-generator` 承担 Agent-C
- 推导产物 `plan/derivation_Q{n}.md` 是两轨契约
- 多子问题用 `pipeline_manager.py suggest-parallel` + `parallel-start`

## 参考实现

源仓库 `MathModeling-AI-Agent`：
- `agents/analysis_agent.py` — 推导 Agent（含 LaTeX 公式生成）
- `agents/code_agent.py` — 编码 Agent（含模型优选 + Python 代码生成）
- `agents/orchestrator.py` — 双 Agent 调度器
- `utils/knowledge_base.py` — 共享知识库