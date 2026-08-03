---
name: quality-assurance-auditor
description: "强制审计论文生成质量，防止模型偷换、逻辑断链、内容空洞。Invoke when 用户提出检查/审计/验收/确保/verify/QA，或合并前需要把关。触发词：质量审计、QA、evidence gate、证据门禁、工作流检查、质量验收、verify quality、门禁检查。"
---

# 质量审计员（Quality Assurance Auditor）

## 执行契约
- 上游输入：优先读取 `paper_output/plan/model_route.json`、`rubric_alignment.json`、`data_plan.json`、`visualization_plan.json`、`paper_output/figure_index.json`、`paper_output/results/` 与 `paper_output/tables/table_index.json`；缺失时回退到 `paper_output/step1/problem_analysis.json`。
- 必须输出：`paper_output/tasks.json`，并确保 `paper_output/micro_units/` 目录存在；正式成稿前必须输出 `paper_output/qa/evidence_gate_report.json` 与 `paper_output/qa/evidence_gate_report.md`。
- 下游交接：`paper-micro-unit-generator` 只应在 `tasks.json` 存在后生成正文；任务中必须保留模型路线、验证计划、图表建议、评分点、结果摘要、指标、表格和结论字段。
- 推荐下一步：正文生成前通过后进入 `paper-micro-unit-generator`；若已经生成 `final_paper.md` 或 `final_paper.docx`，则执行最终一致性检查并回到 `paper-workflow-orchestrator` 汇总。
- 失败回退：若 `problem_files/` 为空应阻塞；若模型路线缺失则用题意分析生成任务；若题意分析也缺失才使用通用任务模板。

## 目标
- 在论文生成的每一个关键节点插入“强制验收点”，只有审计通过才能进入下一步，防止“字数达标但逻辑错误”或“模型偷换”等隐性偷懒。
- 提供可量化的通过/失败判定，并给出具体修改清单，确保最终论文既“厚”又“对”。
- 明确区分“quickstart 验证草稿”和“正式比赛稿”：脚本跑通不等于论文合格；结果证据仍为骨架时，不得交付最终稿。
- 明确职责边界：`evidence_gate.py` 只判断真实结果、指标、图表、表格和结论证据是否足够；正式论文结构、字数、三级标题、图表引用和 Word 格式由 `paper-formal-writer/scripts/check_paper_format.py` 判断。两个门禁都通过后，才能称为正式稿。

## 适用时机
- 任何一步 skill（赛题解析、模型选型、结构设计、微单元生成）完成后，用户希望确认“这一步真的做对了吗？”
- 在合并全文之前，做最终一致性扫描，防止前后矛盾、遗漏约束、图表断链。
- 当用户怀疑“AI 偷偷简化了模型”或“生成的内容空洞”时，立即调用本 skill 进行强制审计。

## 输入
- 必填：待审计产物（如 `problem-doc-model-selector` 输出的模型路线、论文结构清单、或单个微单元文本）。
- 必填：原始赛题 PDF/Word 内容或关键约束摘录，用于对照。
- 可选：用户自定义的评分点清单（如 CUMCM 官方 rubric），可覆盖默认规则。

## 输出
- 审计报告（JSON + 人类可读）：
  - `checkpoint_id`：本次审计节点编号
  - `status`：PASS / FAIL
  - `score`：0–100 量化得分
  - `failures[]`：未通过项列表，含「问题描述」「位置」「建议修改」
  - `warnings[]`：可接受但建议优化的项
- 若状态为 FAIL，则**拒绝进入下一步**，并给出「必须修改清单」
- 若状态为 PASS，则给出「已验证通过」印章，可安全继续

## ★ 项目知识资产联动（必须执行）
本 skill 执行时，**必须**读取以下 `outputs/` 中已沉淀的规则，作为质量审计的权威依据：

| 资产 | 路径 | 用途 |
|------|------|------|
| 最终质量门 | `outputs/final_quality_gate.md` | P0/P1/P2 阻断项清单，提交前必检 |
| 评分量表 | `outputs/scoring_rubric.md` | 100分制7维度，审计打分的唯一标准 |
| 评审清单 | `outputs/revision_checklist.md` | 改稿检查清单 |
| 低分风险库 | `outputs/common_failure_patterns.md` | 常见低分原因与避坑指南 |
| 数据清洗标准 | `outputs/data_cleaning_standards.md` | 数据口径一致性检查 |
| 图表模板 | `outputs/figure_templates.md` | 图表质量检查标准 |

**执行规则**：
1. 审计打分必须以 `outputs/scoring_rubric.md` 的100分制为唯一标准
2. 最终一致性检查必须对照 `outputs/final_quality_gate.md` 的 P0 清单
3. 发现的问题必须按 P0/P1/P2 分级，P0 未过不得放行

## ★ 四层反馈机制（v4.1 融合自 handsomeZR/mathmodel-skill）

> 本项目原有"单遍审计 + auto-fix 回环"。融合 mathmodel-skill 的 4 层反馈后，形成**阶段级→跨阶段→独立 Panel→证据校准**的闭环。四层文档见 `references/feedback_layer{1,2,3,4}_*.md`。

| 层 | 触发 | 职责 | 文档 | 脚本 |
|---|---|---|---|---|
| **L1 阶段 Critic** | 每个 S 阶段产出后 | 5 维 rubric 评分 + diff-only 精修（最多 3 轮）+ verdict 状态机 | `feedback_layer1_critic.md` | `scripts/score_artifact.py` + `extract_diff.py` |
| **L2 跨阶段回检** | S4/S5/S6 末尾 + 手动 | 跨阶段一致性（符号/数字/假设/模型族）+ 定向回滚 | `feedback_layer2_backtrack.md` | — |
| **L3 独立 Panel** | S7 通过后、提交前 | 5 persona 隔离上下文并行 + 段落级缺陷定位（不预测奖项）| `feedback_layer3_panel.md` | `scripts/figqa.py`（在 math-figure）|
| **L4 证据校准** | championship 模式 | 证据账本/反例复核"分数升但证据没变强" | `feedback_layer4_calibration.md` | — |

### 启用规则
- **standard 模式**（默认）：L1 + L2
- **championship 模式**（冲奖）：L1 + L2 + L3 + L4
- **fast 模式**：仅 L1 单次（sanity check）
- 模式由 `paper-workflow-orchestrator` 按 deadline 距离自动推荐

### 与现有审计的关系
- `consistency-auditor` + `completeness-auditor`（三审计层）= L2 的工程化子集
- L2 在两者之上加"跨阶段语义一致性 + 定向回滚决策"
- `auto_detect_and_fix.py` 现有回环 = L1 的工程化兜底
- **L1/L2/L3/L4 + 三审计层 + 8 道门禁全部通过才可提交**

### Verdict 状态机（L1，三处一致：本文档 / feedback_layer1 / score_artifact.py）
`block`（≥1 high issue）> `pass_early`（min≥9 且 mean≥9）> `pass`（min≥7 且 mean≥8）> `refine`（section-patch，cap 3）> `carryover`（iter==3 交 L2）

权重来自 `outputs/dim_weights.json` stage_dim_weights[competition][task_type][stage]，clamp [0.7,1.5]。

## 审计维度（可逐层开关）
1. 赛题覆盖度
   - 是否 100% 识别所有子问题（Q1/Q2/Q3…）
   - 是否 100% 覆盖所有显式约束（不等式、边界、特殊条件）
2. 模型-任务匹配度
   - 模型类型（预测/优化/分类）与任务目标是否一致
   - 是否具备处理给定数据格式的能力（时序→时序模型、截面→回归等）
3. 逻辑一致性
   - 假设 ⇄ 模型推导 ⇄ 结果解释 是否闭环
   - 符号表是否出现冲突或双口径（同一符号两种含义）
4. 评分点对齐度
   - 每个高分点（敏感性分析、对照实验、误差量化）是否在结构或文本中被”可定位”地承诺
5. 机械重复检测（High Priority）
   - **允许凑字数**：允许使用”随着…的发展”、”综上所述”等学术连接词来增加篇幅，**不做**Fail判定。
   - **打击机械复制**：严查**连续段落完全重复**（如同一段话连续出现两次）、**占位符未替换**（如出现”补充说明”字样且内容重复）。若发现这种”乱七八糟”的重复，直接 FAIL。
   - **结构核查**：对比 `paper_prompt_default.md`，重点检查核心章节是否遗漏，对具体的段落格式可适当放宽。

## 附加产物
- **Word 导出 (docx)**: 审计通过后，若存在 `final_paper.md`，必须调用转换工具（如 pandoc 或 python-docx）将其转换为 `final_paper.docx`，作为最终交付物。不应只交付 Markdown。
6. 图表-正文链检测
   - 正文是否出现“见图 3”而图 3 真实存在且编号正确
   - 图表标题与正文描述是否语义一致

## 工作流程（可嵌套到任意阶段）
1. 接收待审计产物与原始赛题
2. 按用户指定的维度逐项扫描
3. 生成 PASS/FAIL 报告与修改清单
4. 若 FAIL，则**阻塞后续 skill 调用**，强制返回修改；若 PASS，则盖章放行
5. 可选：将审计结果写入 `.audit_log.jsonl`，供后续追溯

## 使用示例
- 输入：（1）problem-doc-model-selector 输出的「模型路线」、（2）赛题原文
- 行为：
  - 检查是否遗漏子问题 → 发现 Q3 未被提及 → FAIL
  - 报告：`failures: [{"issue": "子问题 Q3 未被识别", "suggestion": "在模型路线中补充 Q3 的任务拆解与指标定义"}]`
  - 用户必须先修正模型路线，重新审计通过后才能进入结构设计

## 防偷懒机制
- 本 skill **绝不生成任何新内容**，只做「Review & Reject」
- 所有判定规则公开透明，用户可自定义阈值或开关维度
- FAIL 时**强制阻塞**，无法通过 prompt 绕过，必须实质修改

## 备注
- 审计规则默认对齐 CUMCM 国赛评分标准，可通过 `rubric=` 参数覆盖
- 支持中英文赛题与输出，关键词库可扩展
- 审计本身不依赖外部大模型，全部基于规则与关键词库，确保速度与不偏性

---

## 附录 A：脚本入口（推荐）
本 skill 的可执行脚本都放在 `scripts/` 下。

当前 `scripts/pipeline.py` 是基础门禁脚本，负责初始化目录、检查 `problem_files/` 并生成 `paper_output/tasks.json`。

`scripts/evidence_gate.py` 是正式成稿前证据门禁脚本，负责检查每个 `question_id` 是否具备真实模型结果、评价指标、图表或表格证据、结论回扣和任务追踪。official 模式还会检查 `model_results.json` 中每个正式结果的 `execution_provenance`，确认 `source_code_path` 存在、`run_command` 非空、`run_exit_code=0` 且输出产物可追踪；没有真实代码运行来源的结果不得通过。它会输出 `paper_output/qa/evidence_gate_report.json` 与 `paper_output/qa/evidence_gate_report.md`。official 模式下未通过会返回非零退出码；quickstart 模式只给 warning。

`paper-formal-writer/scripts/check_paper_format.py` 是正式成稿后的格式门禁脚本，负责检查 `final_paper_source.md` 是否达到 `18000-25000` 目标、是否有 `1 / 1.1 / 1.1.1` 三级标题、每问是否有建模/算法/结果/检验、图表是否被正文引用、参考文献和附录是否完整。它不替代 `evidence_gate.py`，而是在证据门禁通过后继续阻止低字数、低格式质量的 Word 被称为最终稿。

- 若存在 `paper_output/plan/model_route.json`，脚本会优先按模型路线、评分点证据、主模型、验证计划和建议图表动态生成微单元清单。
- 若存在 `paper_output/plan/data_plan.json`、`visualization_plan.json` 与 `paper_output/figure_index.json`，脚本会做轻量证据链检查：确认图表 ID、输出路径和数据路径可追溯，但不会因为计划图尚未实际生成就阻塞全流程。
- 若存在 `paper_output/results/model_results.json`、`metrics.json`、`conclusions.json` 与 `paper_output/tables/table_index.json`，脚本会把 `result_summary`、`key_metrics`、`tables`、`conclusions`、`evidence_status` 写入每个子问题任务，供微单元生成器直接使用。
- 若不存在模型路线契约但存在 `paper_output/step1/problem_analysis.json`，脚本会按真实子问题、任务类型、推荐模型、验证计划和建议图表动态生成微单元清单。
- 若不存在结构化题意分析，脚本才回退到通用任务清单模板。
- 若 `paper_output/tasks.json` 已存在，默认不覆盖；需要按最新题意重新生成时，设置 `MATHMODEL_REGENERATE_TASKS=1` 后再运行。

更细的审计规则写在本 `SKILL.md` 中，Agent 在真正验收论文时必须结合正文、题面、任务清单和图表引用执行这些规则，而不能只把脚本跑通当作质量通过。

**在项目根目录运行**：
```bash
python .claude/skills/quality-assurance-auditor/scripts/pipeline.py
```

**正式成稿前运行证据门禁**：
```bash
python .claude/skills/quality-assurance-auditor/scripts/evidence_gate.py
```

**quickstart 验证时只看 warning**：
```bash
python .claude/skills/quality-assurance-auditor/scripts/evidence_gate.py --mode quickstart
```

**行为**：初始化目录 → 检查 `problem_files/` 是否为空（不通过则阻塞）→ 优先读取 `paper_output/plan/model_route.json` 与 `rubric_alignment.json` → 读取数据/图表/结果/表格契约做轻量证据链提示 → 回退读取 `paper_output/step1/problem_analysis.json` → 生成动态 `paper_output/tasks.json` → 汇报当前微单元完成进度并扫描占位痕迹。

## 目录约定（与项目全局对齐）
- 本技能会强制要求 `problem_files/` 非空。
- 本技能统一在 `paper_output/` 下产出任务清单与微单元目录。

## 前后衔接
- 常作为全局门禁：建议在“生成正文/合并全文”之前先跑一次。
- 后续通常接：`paper-micro-unit-generator`（生成微单元与合并）或回到 `paper-workflow-orchestrator` 继续完整 workflow。

## 约束（必须遵守）

- **Memory Interaction (必做)**:
  - **审计通过后**：必须调用 `context-memory-keeper`，将“审计通过状态”与“生成的任务清单概况”更新到 `Short-term Workbench`。
- 本技能是全局门禁：当用户要进入“生成正文/合并全文/交付论文”阶段，必须先通过本技能的目录检查与任务清单生成。
- 未生成 `paper_output/tasks.json` 时，禁止直接进入 `paper-micro-unit-generator`。
- 若 `evidence_gate.py` 未通过，禁止把 `final_paper.docx` 称为最终稿；必须回到 `model-code-and-result-generator` 或当前赛题专用代码，补齐真实结果、指标、图表、表格和结论。
- 若 `paper-formal-writer/scripts/check_paper_format.py` 未通过，禁止把 `final_paper.docx` 称为最终稿；必须回到 `final_paper_source.md` 补齐正文长度、标题结构、图表解释、参考文献或附录代码说明。
- 当用户已生成 `paper_output/final_paper.md` 时，建议再次调用本技能做最终一致性把关，确保“每问有结论、图表可定位、引用不断链”。

## 新增脚本（v4.2）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/pipeline_manager.py` | GitOps 流水线状态机（init/status/advance/rework + AP/Manual + 并行阶段 + 返工上限） | "流水线状态" / "推进阶段" / "返工" |
| `scripts/verify_gate.py` | G4.6 强制代码自证门——每模型 verify_*.py 全 PASS 才引用 | "G4.6" / "验证所有模型" |
| `scripts/check_numeric_sanity.py` | 通用 inf/nan/量级扫描（互补于硬编码 result_reasonableness） | "数值合理性" / "inf nan 检查" |
| `scripts/fallback_router.py` | L2 容错 7 类备用链（算法/编译/公式失败时切换备用方案） | "fallback" / "备用方案" / 容错自动触发 |

L1-L4 容错全落地：L1 auto_detect_and_fix → L2 fallback_router → L3 consistency LOW_CONFIDENCE → L4 pipeline rework + HIL。
