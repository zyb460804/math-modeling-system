# Context Memory (Active)

> **v2.0 — 三层记忆架构**
> Instructions for Agent:
> 1. Read this file before long MathModel workflows.
> 2. Keep long-term principles stable unless the user explicitly changes them.
> 3. Update the short-term workbench after major steps: problem parsing, data processing, QA, paper generation, and final delivery.
> 4. Update working memory after every sub-step (file paths, temp vars, current focus).
> 5. When this file exceeds 100 lines, compress: archive completed stages, keep conclusions only.
> 6. Cross-reference with `outputs/knowledge_graph.md` for model/algorithm navigation.

---

## 0. 工作记忆（Working Memory）

> 单次对话/子任务级别，30 分钟自动衰减，上限 20 行。

- 当前焦点：无活跃任务
- 正在处理的文件：无
- 临时变量：无
- 当前 agent 调用链：无

---

## 1. 长期准则（Long-Term Principles）

> 跨赛题、跨赛季，永久/半永久。仅在用户明确要求时修改。上限 40 行。

### 角色与语言
- Role: mathematical modeling workflow assistant.
- Output language: Chinese academic style unless the user asks otherwise.
- Delivery target: keep Markdown and Word outputs aligned when a full paper is requested.

### 工作流约束
- Workflow chain: problem parsing → model selection → data/code adaptation → QA → micro-unit generation → merge.
- Script rule: treat bundled `scripts/` as reusable code templates; adapt to current problem before trusting outputs.
- Evidence gate: `quality-assurance-auditor/scripts/evidence_gate.py --mode official` must pass before writing.
- Format gate: `paper-formal-writer/scripts/check_paper_format.py` must pass before finalizing.
- Word count threshold: ≥18000 characters for national competition papers.

### 评分标准锚点
- Scoring: → `outputs/scoring_rubric.md`（100分制7维度，不改分）
- P0 blocking: → `outputs/final_quality_gate.md`
- Red flags: → `outputs/algorithm_selection_red_flags.md`

### 禁止项
- 数据、文献、运行结果、p 值一律不得编造。
- 不得在未通过证据门禁时称论文为"最终稿"。
- 不得硬编码密钥或敏感信息。

---

## 2. 短期工作台（Short-Term Workbench）

> 单个赛题/竞赛周期，阶段性完成 → 归档到 memory_archive.md。上限 80 行。

### 当前赛题
- 题目：未设定
- 题型：未识别
- 附件状态：未检查
- 赛题文件路径：`problem_files/`（待放入）

### 模型路线
- 主模型：未选定
- 备选模型：未列出
- 模型链：未规划
- 知识图谱参考：→ `outputs/knowledge_graph.md`

### 数据状态
- 数据来源：未检查
- 清洗状态：未开始
- 清洗标准：→ `outputs/data_cleaning_standards.md`

### 代码状态
- 代码模板：→ `outputs/algorithm_templates.md`
- 生成代码路径：`paper_output/code/`
- 运行状态：未执行

### 图表状态
- 图表计划：未制定
- 已生成图表：无
- 图表模板：→ `outputs/figure_templates.md`

### QA 状态
- 证据门禁：未开始
- 格式门禁：未开始
- QA 报告路径：`paper_output/qa/workflow_guard_report.md`

### 论文状态
- 写作阶段：未开始
- 当前字数：0
- 摘要状态：未写
- 排版状态：未排

---

## 3. 外部资源 / 文献（External Resources）

> 记录本次赛题引用的外部数据源和文献。

- 无记录

---

## 4. 实体追踪快照（Entity Tracking Snapshot）

> 本次赛题使用的 MODEL/ALGORITHM/CODE 实体。详细索引见 `memory_entity_index.md`。

| 实体类型 | 名称 | 状态 | 知识图谱引用 |
|----------|------|------|-------------|
| （未使用） | | | |

---

## 5. 开放待办（Open Todos）

- [ ] Parse the problem statement.
- [ ] Select model route and scoring evidence.
- [ ] Inspect data files and adapt scripts.
- [ ] Run QA before paper generation.
- [ ] Generate and merge paper micro-units.
- [ ] Update entity tracking after model/algorithm selection.