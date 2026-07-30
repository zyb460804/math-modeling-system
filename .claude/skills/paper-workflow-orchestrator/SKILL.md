---
name: paper-workflow-orchestrator
description: "MathModel Skill 总入口。触发词：数学建模、生成论文、分析赛题、CUMCM、MathorCup、华数杯、美赛、ICM、MathModel。任何数学建模任务先读本 skill 再路由子 skill。"
---

# 论文生成全流程编排器

## 启动门（必须第一步执行）

进入任何后续步骤之前，**必须**用 Bash 运行预检脚本：

```bash
python .claude/skills/paper-workflow-orchestrator/scripts/preflight_check.py
```

读取退出码和 `paper_output/preflight_report.json`：

- 退出码非 0 或 `status != "PASS"` → **立刻停止生成任何内容**。把报告中的 `errors` 原文反问用户，等用户修复 `problem_files/` 后重新运行预检；
- 不允许跳过预检；不允许"先凑合写一稿"；不允许凭印象判断附件状态；
- 预检通过后，按下方阶段路由表逐步推进。

## 状态门（每阶段开始前执行）

正式流程进入 S1-S8 任一阶段前，必须用 `workflow_guard.py` 检查截至当前阶段的产物状态。例如进入数据阶段前检查到 S2：

```bash
python .claude/skills/paper-workflow-orchestrator/scripts/workflow_guard.py --step S2
```

脚本会写入 `paper_output/qa/workflow_guard_report.json`。若退出码非 0 或 `status != "PASS"`，必须按报告失败项补齐上一阶段产物，不得跳步。

## Quickstart 用途说明

`scripts/quickstart_run.py` 仅用于安装验证。它产出的占位草稿写入 `paper_output/quickstart/`，并写入名为 `quickstart_draft.docx` 的草稿文件，**不会**通过证据门禁，不得对外宣称为最终稿。

正式赛题任务禁止调用 quickstart。若用户说"先快速看个样子"，先反问："你需要正式稿还是只验证安装？" 不要默认走 quickstart。

`scripts/run_all.py` 是已废弃命令的兼容提示，仅用于保护旧文档/旧脚本调用者，正式流程不再调用。

## 执行契约
- 上游输入：`problem_files/` 中的赛题与附件数据；可选读取 `crawled_data/` 中的补充权威数据。
- 必须输出：`paper_output/OUTPUT_LAYOUT.md`、`problem_analysis.json`、`model_route.json`、`rubric_alignment.json`、`scoring_strategy.md`、数据/图表计划、结果证据、证据门禁报告、`paper_outline.json`、`final_paper_source.md`、`final_paper.docx` 与格式检查报告。
- 下游交接：本技能是总入口，负责判断当前阶段并路由到其他 skill；用户不知道从哪个 skill 开始时优先调用它。
- 失败回退：`problem_files/` 为空时阻塞；模型路线、数据计划或图表生成失败时打印 warning 并继续，让 QA 按可用契约回退。

## 目标
- 本技能是正式入口，不是“一键脚本说明书”。正式赛题应由 Agent 先读题、拆题、判断附件性质，再生成或修改当前赛题专用代码，运行真实结果，最后基于完整证据链全局写作。
- 保持本项目的核心思路：以 skill 为主线，把“赛题解析 → 模型选择 → 数据处理 → 结果证据 → QA 门禁 → Agent 全局写作 → 最终 QA”串成一套可执行工作流。
- `scripts/quickstart_run.py` 只用于 quickstart、安装验证和 smoke test；它生成的是验证草稿，不代表正式比赛论文质量。
- `scripts/run_all.py` 已废弃，只保留迁移提示，不再作为正式论文或 quickstart 的执行入口。

## 运行模式（fast / standard / championship）（v4.1 融合自 handsomeZR/mathmodel-skill）

> 本项目原流程无节奏控制。融合 mathmodel-skill 的 3 模式后，按 deadline 距离自动推荐模式，控制反馈层深度与 token 预算。模式与竞赛正交。

| 模式 | 上下文策略 | 反馈层 | 用途 |
|---|---|---|---|
| **fast** | 只保留当前阻断项与最小证据 | L1 单次 | 选题试跑 / sanity check / 剩余时间紧 |
| **standard** | 按阶段加载并保留决策摘要 | L1 + L2 | 默认主流程 |
| **championship** | 终审阶段扩展证据与独立视角 | L1 + L2 + L3 + L4 + 盲评 Panel | 提交前最后冲刺、冲奖 |

### 自动推荐（按距 deadline 剩余）
- \> 60h：standard（最后 6h 升 championship）
- 24–60h：standard
- 6–24h：fast 关键阶段 + championship 终审
- < 6h：直接进最终 QA + championship 终审

### 启用方式
- 写入 `paper_output/plan/mode.json`：`{"mode":"standard","deadline":"<ISO>","reason":"..."}`
- 用户可手动覆盖："切到 fast" / "升级到 championship"
- 模式变化写入 `paper_output/qa/events.log`；**不静默切换**，不可观测 token 时消耗记为 null 不估算
- 上下文压力或时间不足时，向用户建议降级（championship → standard → fast），确认后才改

### 各模式触发的额外 skill
- fast：关闭微单元迭代、关闭 L2/L3/L4
- standard：启用 L1 精修 + L2 回检（默认）
- championship：额外启用 `blind-panel`（3 座盲评）+ L4 证据校准 + `math-figure/figqa` 碰撞门 + `math-figure/pdf_qa` 编译 PDF 检查

## Friendly Mode（问答式优先）（v4.1 融合自 handsomeZR/mathmodel-skill）

> 本项目原流程脚本密集（用户需手敲 `python .claude/skills/.../scripts/...py`）。融合 mathmodel-skill 的问答式 UX：**用户只回答编号问题，agent 自动读写状态**。

### 核心原则
- 离散选项（选竞赛 / 选题 / 选模型 / verdict 决策 / 选模式）→ **必须用问答式**，不让用户手敲 bash/python/json
- 自由文本（PDF 路径 / 截止时间）→ 单行回复
- 状态读写（`paper_output/plan/mode.json`、`tasks.json`）→ agent 自动完成
- 每个关键决策点都有"让我决定（推荐 X）"兜底选项

### 落地方式
- Claude Code：优先用 `AskUserQuestion` 工具呈现编号选项
- 无原生选择 UI 时：回退到 markdown 编号列表（语义等价）
- 示例：
  ```
  当前 A 题，题型=优化/规划。推荐模型路线：
  1. LP + 启发式（GA）—— 推荐，求解可行且利于多目标
  2. MILP 精确求解—— 精度高但 24 场景可能慢
  3. 让我决定（自定义）
  回复编号即可。
  ```

### 与现有口令的关系
- `审题/选模/review/defense/figure/code` 等口令**保留**（老用户兼容）
- 口令是无歧义明确指令时用；**多选题、风险决策、模式切换**用 Friendly Mode 问答
- 两者不矛盾：同一意图默认最深输出（见 CLAUDE.md 触发词统一入口）

## 入口路由规则
- 当用户说”开始生成数学建模论文””帮我做这个数学建模题””分析赛题””使用 MathModel Skill”或不知道该调用哪个 skill 时，先读取本技能。
- 先判断用户目标：正式论文走 Agent-native 全流程；只要题意、模型、数据、QA 或正文时，路由到对应子 skill。
- 不要让用户理解或选择多个 skill 的顺序；由本技能负责说明下一阶段，并在阶段完成后回到本技能判断下一步。
- 如用户只是验证安装或跑 quickstart，可调用：
  - `python .claude/skills/paper-workflow-orchestrator/scripts/quickstart_run.py`
- 正式赛题不要先跑 quickstart 脚本；应先读取题面和附件，再按当前赛题生成专用数据处理、建模和绘图代码。

## ★ 项目知识资产联动（必须执行）
本 skill 作为总控，**必须**在全流程中引导子 skill 读取 `outputs/` 中已沉淀的知识资产。各子 skill 的联动规则见各自 SKILL.md，以下为总控层面的桥接：

### 知识骨干（outputs/ 系统）
`outputs/` 包含 89 个规则/模板/知识库文件，按 8 大功能域组织，是本项目的**知识骨干**。所有 skill 执行时必须优先复用这些沉淀，而非临时发挥。

核心入口：
- `outputs/INDEX.md` — 统一索引，按功能域查到目标文件
- `outputs/scoring_rubric.md` — 评分唯一标准（100分制7维度）
- `outputs/method_matching.md` — 方法匹配表（题型×模型×算法×风险）
- `outputs/writing_templates.md` — 写作模板库（高分表达/结构模板）
- `outputs/final_quality_gate.md` — 最终质量门（P0/P1/P2 阻断项）

### 手动/局部任务桥接（prompts/ 系统）
`prompts/` 包含 31 个工作流提示词（00-30），是本项目的**手动工作流**系统。当用户需要局部任务（审题、审论文、答辩、代码生成等）而非完整流水线时，路由到对应 prompt：

| 口令 | 对应 prompt | 用途 |
|------|-------------|------|
| 审题 | `prompts/11_identify_problem_type.md` + `prompts/12_select_model_route.md` | 题型判断+选模 |
| 审论文 | `prompts/04_review_my_paper.md` + `prompts/08_review_math_modeling_paper.md` | 全文评分+改稿 |
| 生成代码 | `prompts/19_generate_code.md` | 代码生成 |
| 生成图示 | `prompts/20_generate_figures.md` | 图示方案 |
| 准备答辩 | `prompts/06_mock_defense.md` + `prompts/09_defense_math_modeling.md` | 答辩准备 |
| 生成提交包 | `prompts/21_generate_submission_pack.md` | 提交打包 |

**执行规则**：
1. 正式赛题走 Skill 自动化流水线（本 skill 路由）
2. 局部/灵活任务走 `prompts/` 手动工作流
3. 两套系统共享 `outputs/` 知识骨干，不矛盾

## 阶段路由表
| 当前目标 | 优先调用 |
|---|---|
| 刚开始、只给了赛题或不知道用哪个 skill | `problem-doc-model-selector` |
| 已有 `problem_analysis.json`，需要模型路线和评分闭环 | `modeling-paper-rubric-and-model-selector` |
| 需要外部权威数据 | `authoritative-data-harvester` |
| 需要处理附件数据、生成数据/图表计划或图表样板 | `data-cleaning-and-visualization` |
| 需要特征工程（数据预处理、转换、编码、缩放） | `feature-engineering` |
| 需要生成模型结果、评价指标、结论和表格证据 | `model-code-and-result-generator` |
| 需要比较不同算法性能 | `algorithm-benchmark` |
| 进入正文生成前，需要任务清单和门禁检查 | `quality-assurance-auditor` |
| 需要检查AI生成内容的失败模式 | `ai-failure-checker` |
| 证据门禁通过，需要正式成稿、规范格式、Word 排版 | `paper-formal-writer` |
| 需要校准写作风格 | `style-calibration` |
| 需要验证引用真实性 | `citation-tracer` |
| 需要微单元提示词资产、局部扩写或低能力模型兜底草稿 | `paper-micro-unit-generator` |
| 已有 `final_paper_source.md` 或 `final_paper.docx`，需要最终把关 | `quality-assurance-auditor` + `paper-formal-writer` |
| 需要一致性审计 | `consistency-auditor` |
| 需要完整性审计 | `completeness-auditor` |
| 需要记录用户决策 | `decision-logger` |
| **赛题 PDF 有附表**（成分/负荷/参数表） | `data-cleaning-and-visualization` 的 `extract_pdf_tables.py`（Camelot，v4.3） |
| **赛题 PDF 有公式图** | `problem-doc-model-selector` 的 `extract_formulas_ocr.py`（Pix2Text，v4.3） |
| **C 题需宏观/金融/行业数据** | `authoritative-data-harvester` 的 `akshare_fetch.py`（akshare，v4.3） |
| **ML 题需调参** | `model-code-and-result-generator` 的 `optuna_tune.py`（Optuna TPE，v4.3） |
| **ML 题需可解释性**（特征重要性） | `feature-engineering` 的 `shap_explain.py`（SHAP，v4.3） |
| **图表要期刊风**（IEEE/Nature） | `math-figure` 的 `journal_style.py`（SciencePlots，v4.3） |
| **降 AIGC 要保留 Word 排版** | `aigc-reduce` 的 `replace_docx_preserve_format.py`（v4.3） |
| **代码自证门 G4.6** | `model-code-and-result-generator` 的 `verification_template.py` + `qa-auditor` 的 `verify_gate.py`（v4.2） |
| **流水线状态/返工/并行** | `qa-auditor` 的 `pipeline_manager.py`（GitOps 状态机，v4.2） |
| **数值合理性（inf/nan/量级）** | `qa-auditor` 的 `check_numeric_sanity.py`（v4.2） |
| **报告新鲜度校验** | `context-memory-keeper` 的 `freshness_check.py`（SHA-256，v4.2） |
| **安全检查/密钥扫描** | `consistency-auditor` 的 `security_check.py`（v4.2，git commit 前自动拦截） |
| **Typst 交付**（替代 Word/LaTeX） | `typst-renderer` skill（v4.2，34 套赛事模板） |
| **Word 原生公式/局部 XML 编辑** | `docx-editor-cn` skill（v4.2，temml→docx + unpack/pack） |
| **LaTeX 编译**（带重试） | `paper-formal-writer` 的 `compile_latex.py`（v4.2） |
| **查历年优秀论文章节** | `award-paper-rag` skill（v4.2，章节级 RAG，retrieve 离线/chat 需 key） |
| **MATLAB 强项**（ODE/曲线拟合/优化/Simulink） | `matlab-model-code-generator` 的 `matlab_runner.py` + `matlab_templates/`（v4.3，无头 `matlab -batch`，本地 MATLAB 已接入） |
| 方法选择完成，需要签发建模合同 | 读取 `references/model-contract-template.md` → 调用 `model-code-and-result-generator` |
| 图表生成前，需要签发图表合同 | 读取 `references/figure-contract-template.md` → 调用 `data-cleaning-and-visualization` |
| 进入新阶段，需要执行门控检查 | 读取 `references/gate-system.md` → 执行对应 G1-G6 门控 |
| 结果冻结，需要锁定数字 | 读取 `references/frozen-numbers-convention.md` → 生成 `frozen_numbers.json` |
| 候选方法验证，需要 PoC 检查 | 读取 `references/poc-validation-gate.md` → 运行 PoC 验证 |
| 三审计层全过、championship 冲奖终审 | `.claude/agents/blind-panel-judge.md`（3 座并行）→ `blind-panel` skill 聚合 |
| 跨阶段一致性可疑（符号/数字/模型族漂移）| qa-auditor `references/feedback_layer2_backtrack.md` 定向回检 |
| 图表提交前碰撞门 | `math-figure/scripts/figqa.py` + `pdf_qa.sh`（从编译 PDF）|
| 评分需按题型差异化加权 | 加载 `outputs/dim_weights.json`（module_weights_7dim / stage_dim_weights）|
| 用户想切换节奏/UX | 见本文档"运行模式"（fast/standard/championship）+ "Friendly Mode" |

## 适用时机
- 用户已经在项目根目录下按约定放好了赛题 PDF/Word 和附件数据，需要“从零到万字论文”的一条龙自动流程时。
- 已经完成部分计算或占位符填充，但希望检查整体步骤是否完整、顺序是否合理，或想重跑核心流程时。

## 约束（必须遵守）

- **Memory Interaction (必做)**:
  - **全流程中**：作为总控，应当在每个关键步骤（清洗完、QA完、生成完）结束后，主动调用 `context-memory-keeper` 更新进度，确保如果流程中断，Memory 中留有断点记录。
- 本技能是全项目唯一“入口路由 skill”。用户只要提出“生成完整论文/跑完整流程”，优先读取本技能而不是让多个技能分散运行。
- 若 `problem_files/` 为空，必须先补齐赛题与附件数据，再运行流程。
- 当前赛题专用代码必须写入 `paper_output/code/`：数据处理放 `data_processing/`，绘图放 `visualization/`，建模放 `modeling/`，检查放 `qa/`。不要把 `q1_model.py`、绘图脚本或清洗脚本写回 `skills/*/scripts/`。
- 必须先判断附件性质：原始数据、结果模板、说明文档、参考材料要分开处理。像官方要求填写的 `result*.xlsx` 结果模板，不能被当作原始输入数据机械清洗，也不能据此伪造真实建模结果。
- 当任一子问题的 `evidence_status` 为 `missing`、`needs_real_modeling` 或 `scaffold_result_needs_review` 时，不得把 Word 称为最终稿；必须先补齐赛题专用代码、真实图表、表格、指标和结论。
- 若用户分开调用了其他技能，最终仍应回到本技能或按本技能的顺序完成：清洗与出图 → QA 任务清单 → 微单元生成 → 合并。

## 合同与门控体系（v4.0 新增）

以下 5 份参考文档定义了全流程的合同模板、门控架构和数字冻结规范。Orchestrator 负责在对应阶段按需加载，子 skill 通过读取这些文档获取约束和模板。

| 文档 | 路径 | 加载时机 | 用途 |
|------|------|----------|------|
| Model Contract 模板 | `references/model-contract-template.md` | 方法选择完成后、代码生成前 | 为每个子问题签发结构化的建模合同（输入/输出/指标/验证计划），锁定后续代码生成和结果验证的契约 |
| Figure Contract 模板 | `references/figure-contract-template.md` | 图表生成前 | 为每张论文图表签发合同（图题/数据源/渲染规格/引用位置），确保图表产出可追溯、可验证 |
| G1-G6 门控架构 | `references/gate-system.md` | Orchestrator 自身始终持有 | 定义全流程 6 道门控（G1 审题/G2 PoC/G3 数据/G4 结果/G5 正文/G6 终审）的检查逻辑、通过标准和阻断规则；Orchestrator 在每个阶段转换点调用对应门控 |
| 数字冻结机制 | `references/frozen-numbers-convention.md` | 结果冻结阶段（G4 门控通过后） | 定义 `frozen_numbers.json` 的写入/读取/校验规范，确保论文正文中的数字与冻结结果 100% 一致 |
| PoC 验证门禁 | `references/poc-validation-gate.md` | 方法验证阶段（G2 门控） | 定义每个候选方法的 PoC 验证标准（≤30行、真实数据、可运行、有具体输出），失败方法标记为 REJECTED 并归档 |

**执行规则**：
1. Orchestrator 进入对应阶段时**必须**先读取对应参考文档，再调度子 skill。
2. 子 skill 在生成合同或执行门控检查时，必须遵循参考文档中定义的模板和标准。
3. 门控未通过时，阻断后续阶段，不得跳步。
4. `frozen_numbers.json` 一旦写入，后续所有涉及数字的脚本和写作必须以它为准，不得覆盖。

## 正式交付门禁标准（以此判断是否”论文生产完整”）

- **必须通过：`quality-assurance-auditor/scripts/evidence_gate.py` 的 official 模式**
- **必须通过：`quality-assurance-auditor/scripts/check_number_consistency.py` 的数字一致性检查**
- **必须通过：`paper-formal-writer/scripts/check_paper_format.py` 的正式格式门禁**
- 必须存在：`paper_output/final_paper.docx`，但只有证据门禁、数字一致性检查和格式门禁都通过后才能称为正式稿。
- 必须存在：`paper_output/OUTPUT_LAYOUT.md`（当前项目输出位置说明）
- 必须存在：`paper_output/plan/paper_outline.json`（正式论文大纲契约）
- 必须存在：`paper_output/final_paper_source.md`（Agent 全局写作的正式 Markdown 源稿）
- 必须存在：`paper_output/step1/problem_analysis.json`（结构化题意分析）
- 必须存在：`paper_output/plan/model_route.json`（模型路线契约）
- 必须存在：`paper_output/plan/rubric_alignment.json`（评分点映射契约）
- 必须存在：`paper_output/plan/data_plan.json` 与 `visualization_plan.json`（数据与图表证据链契约）
- 必须存在：`paper_output/figure_index.json`（图表计划索引）
- 推荐存在：`paper_output/results/model_results.json`、`metrics.json`、`conclusions.json`（结果证据契约）
- 推荐存在：`paper_output/tables/table_index.json` 与 `paper_output/tables/`（论文表格证据）
- 推荐存在：`paper_output/code/README.md` 与 `paper_output/code/*/README.md`（当前赛题代码工作区说明）
- 推荐存在：`paper_output/tasks.json`
- 推荐存在：`paper_output/ref_check.md`
- 推荐存在：`paper_output/micro_units/`（作为提示词资产和验证草稿，不作为正式主流程）
- 建议存在：`paper_output/figures/` 与 `paper_output/data_cleaned/`（用于数据预处理与结果分析配图）
- **championship 模式追加（v4.1）**：`blind-panel` 3 座盲评 PASS + `math-figure/scripts/figqa.py` 图表碰撞门 PASS + qa-auditor `feedback_layer{1-4}` 四层反馈通过；冲奖稿最终校准用，standard 模式可选

## 脚本清单（本技能实际会用到的）
- `scripts/prepare_output_layout.py`：输出位置准备器。
  - 何时用：完整流程开始前、quickstart、安装验证或用户问“代码/图表/微单元放哪里”时。
  - 做什么：创建 `paper_output/OUTPUT_LAYOUT.md`、`paper_output/code/`、`data_cleaned/`、`figures/`、`tables/`、`results/`、`micro_units/` 等目录，并写入代码工作区 README。
- `scripts/quickstart_run.py`：quickstart / smoke test 执行器。
  - 何时用：quickstart、安装验证、调试，或用户明确要求只验证 workflow 链路。
  - 做什么：先准备输出目录规划 → 再跑 `problem-doc-model-selector/scripts/analyze_problem.py` 生成 `problem_analysis.json` → 再跑 `modeling-paper-rubric-and-model-selector/scripts/build_model_route.py` 生成模型路线与评分点契约 → 再生成数据/图表证据链契约并做清洗与可视化 → 再生成模型结果、指标、结论和表格证据契约 → 再跑 QA 生成动态 `paper_output/tasks.json` → 再离线生成微单元 → 再合并成 `paper_output/final_paper.md` 和 `paper_output/final_paper.docx`。
  - 注意：输出是验证草稿，不代表正式比赛论文。
- `scripts/run_all.py`：废弃迁移提示。
  - 何时用：旧命令误触时提示用户改用 `quickstart_run.py` 或正式 Agent-native workflow。
  - 做什么：只打印迁移提示，不执行生成流程。
- `scripts/workflow_guard.py`：S0-S8 状态门检查器。
  - 何时用：正式流程每个阶段开始前或用户要求检查当前进度时。
  - 做什么：检查预检、审题、模型路线、数据读取报告、建模代码、结果证据、证据门禁、正式稿和格式门禁是否按顺序具备；失败时写入 `paper_output/qa/workflow_guard_report.json` 并返回非 0。

## 自动回环修正（v4.0 新增）

当检测脚本发现质量问题时，自动运行修正器并重检，最多循环 3 轮。仍失败才报告用户。

```bash
# 运行全部检测+自动修正
python .claude/skills/quality-assurance-auditor/scripts/auto_correct_loop.py

# 只跑指定阶段
python .claude/skills/quality-assurance-auditor/scripts/auto_correct_loop.py --stage code number

# 只检测不修正
python .claude/skills/quality-assurance-auditor/scripts/auto_correct_loop.py --dry-run

# 最多5轮修正
python .claude/skills/quality-assurance-auditor/scripts/auto_correct_loop.py --max-rounds 5
```

| 阶段 | 检测脚本 | 自动修复器 | 修复能力 |
|------|---------|-----------|---------|
| `code` | run_and_verify.py | code_auto_fixer.py | 缺少导入、路径错误、编码错误、除零 |
| `number` | check_number_consistency.py | number_auto_fixer.py | 论文数字与frozen_numbers不一致 |
| `result` | check_result_reasonableness.py | evidence_auto_filler.py | 缺失证据文件自动生成占位 |
| `format` | check_paper_format.py | format_auto_fixer.py | 空行、标点、公式格式、图表引用 |
| `evidence` | evidence_gate.py | evidence_auto_filler.py | 缺失目录/文件自动创建 |
| `parameter` | check_parameter_consistency.py | （需人工确认） | 参数不一致 |
| `consistency` | consistency-auditor/audit.py | number_auto_fixer.py | 跨文件数字不一致 |
| `figure` | math-figure/render_check.py | figure_auto_fixer.py | DPI/字体/重叠 → 自动调整参数重新渲染 |
| `latex` | latex-renderer/render_formulas.py | latex_auto_fixer.py | LaTeX语法错误 → 自动修正 |
| `completeness` | completeness-auditor/audit.py | completeness_auto_filler.py | 缺失文件/目录 → 自动创建占位 |
| `citation` | citation_auto_fixer.py | citation_auto_fixer.py | 断链引用/格式错误 → 自动修正 |
| `aigc` | aigc_auto_fixer.py | aigc_auto_fixer.py | AI痕迹过高 → 自动降重 |
| `symbol` | symbol_auto_fixer.py | symbol_auto_fixer.py | 符号重复/不一致 → 自动解决 |
| `code_style` | code_style_auto_fixer.py | code_style_auto_fixer.py | PEP8/格式 → 自动格式化 |

**修正日志**：`paper_output/qa/auto_correction_log.json`

## 质量保障脚本（quality-assurance-auditor/scripts/）

以下脚本用于确保论文质量，防止编造数字和结果错误：

- `check_number_consistency.py`：数字一致性检查。
  - 何时用：论文写完后、提交前。
  - 做什么：比较论文中的关键数字与代码输出，确保一致。

- `check_parameter_consistency.py`：参数一致性检查。
  - 何时用：代码运行前、结果验证时。
  - 做什么：检查代码中的参数是否与题目要求一致（如36吨 vs 72吨）。

- `check_result_reasonableness.py`：结果合理性检查。
  - 何时用：代码运行后、论文写作前。
  - 做什么：检查代码输出的结果是否在合理范围内。

- `inject_results_to_paper.py`：结果自动注入论文。
  - 何时用：代码运行完成后、论文写作时。
  - 做什么：将代码运行结果自动注入到论文中，确保数字一致。

- `run_sensitivity_analysis.py`：灵敏度分析自动化。
  - 何时用：论文需要灵敏度分析时。
  - 做什么：自动运行不同参数下的模型，生成灵敏度分析结果。

- `run_baseline_comparison.py`：基准对照自动化。
  - 何时用：论文需要展示优化价值时。
  - 做什么：运行基准方案（不优化）并与优化方案对比。

## 前置约定
- 目录结构建议为：
  - 根目录：`<项目根目录>`
  - 赛题与附件：`problem_files/`（把赛题 PDF/Word 与附件数据直接放这里；QA 会检查该目录不为空）
  - 补充数据：`crawled_data/`（可选，爬虫或外部公开数据放这里）
  - 输出目录：`paper_output/`（脚本自动生成任务清单、微单元与合并稿）
  - 当前赛题专用代码：`paper_output/code/`（只放当前题目的数据处理、绘图、建模和检查代码）
  - 技能目录：`skills/...`
- Python 可用即可。

## 输入
- 必填：
  - 将赛题 PDF/Word 与附件数据放入 `problem_files/`。
- 可选：
  - 将补充数据放入 `crawled_data/`。

## 输出
- 中间文件：
  - `paper_output/OUTPUT_LAYOUT.md`：当前项目输出位置说明。
  - `paper_output/code/README.md`：当前赛题专用代码工作区说明。
  - `paper_output/code/data_processing/`：当前赛题数据处理代码。
  - `paper_output/code/visualization/`：当前赛题绘图和格式化图表代码。
  - `paper_output/code/modeling/`：当前赛题 q1/q2/q3 建模代码。
  - `paper_output/code/qa/`：可选的当前赛题检查代码。
  - `paper_output/step1/problem_analysis.json`：结构化赛题分析，连接后续 QA 与正文生成。
  - `paper_output/step1/A_题意对齐.md`、`B_论文大纲.md`、`C_评分点对齐表.md`、`D_模型路线.json`。
  - `paper_output/plan/model_route.json`：每一问的模型路线、验证计划和建议图表。
  - `paper_output/plan/rubric_alignment.json`：评分点与证据映射。
  - `paper_output/plan/scoring_strategy.md`：评分闭环说明。
  - `paper_output/plan/data_plan.json`：数据文件、字段画像、清洗任务与子问题链接。
  - `paper_output/plan/visualization_plan.json`：建议图表、图题、用途、候选字段与输出路径。
  - `paper_output/figure_index.json`：图表计划索引，供 QA 和正文引用核对。
  - `paper_output/results/model_results.json`：每问模型输出、参数、方案或预测结果的证据契约。
  - `paper_output/results/metrics.json`：每问评价指标、误差、得分或约束满足情况。
  - `paper_output/results/conclusions.json`：每问可回扣原题的结构化结论。
  - `paper_output/tables/table_index.json`：论文表格索引、表题、用途和路径。
  - `paper_output/tasks.json`：微单元任务清单。
  - `paper_output/micro_units/*.txt`：每个微单元一个文件。
  - `paper_output/generate_log.json`：生成日志。
- 最终交付：
  - `paper_output/final_paper.md`：合并后的 Markdown 论文草稿。
  - `paper_output/final_paper.docx`：Word 草稿，作为主要交付物。
  - `paper_output/ref_check.md`：交叉引用与编号断链报告。

## 工作流程（对应 workflow_full 分步）

### 自动检测+修复说明（v4.0 新增）

工作流中的每个检测点都会自动调用 `auto_detect_and_fix.py`，检测失败时自动修复并重检，最多循环 N 轮，仍失败才报告用户。

```bash
# 在每个检测点自动调用
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage <阶段>
```

| 检测点 | 阶段 | 自动修复能力 |
|--------|------|-------------|
| S4 代码运行后 | `code` | 缺少导入/路径错误/编码错误/除零 |
| S5 数字一致性 | `number` | 论文数字 → 代码结果（以代码为准） |
| S5 参数一致性 | `parameter` | 代码参数 → 题目要求（以题目为准） |
| S5 结果合理性 | `result` | 缺失证据文件自动生成占位 |
| S5 证据门禁 | `evidence` | 缺失目录/文件自动创建 |
| S6 格式门禁 | `format` | 空行/标点/公式格式/图表引用 |
| S6 图表质量 | `figure` | DPI/字体/重叠 → 自动调整参数重新渲染 |
| S6 LaTeX公式 | `latex` | 语法错误 → 自动修正 |
| S6 引用一致性 | `citation` | 断链引用/格式错误 → 自动修正 |
| S6 AIGC检测 | `aigc` | AI痕迹过高 → 自动降重 |
| S7 一致性审计 | `consistency` | 论文数字 → 代码结果（以代码为准） |
| S7 完整性审计 | `completeness` | 缺失文件/目录 → 自动创建占位 |
| S7 符号表冲突 | `symbol` | 符号重复/不一致 → 自动解决 |

**批量调用**：
```bash
# S5 阶段全部检测
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s5

# S6 阶段全部检测
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s6

# S7 阶段全部检测
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s7

# 全部检测
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage all
```

### 正式实现：Agent-native 工作流（推荐）
0. 读取赛题与附件，判断附件是原始数据、结果模板、说明文档还是参考材料。
1. 生成题意分析、模型路线、评分闭环、数据计划和图表计划。
2. **代码工厂**：运行代码工厂脚本，为每个子问题自动生成数据处理、建模和图表代码：
   ```bash
   python .claude/skills/paper-workflow-orchestrator/scripts/code_factory.py
   ```
   生成的代码写入 `paper_output/code/data_processing/`、`modeling/`、`visualization/`。
3. **自动运行+验证+修复**：运行所有生成的代码，自动验证结果，失败时自动修复：
   ```bash
   # 运行代码
   python .claude/skills/paper-workflow-orchestrator/scripts/run_and_verify.py
   # 自动检测+修复代码问题（最多3轮）
   python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage code
   ```
4. **Agent 二次修改**：对 `needs_review` 的子问题，Agent 根据具体题目修改 `paper_output/code/` 中的代码，替换占位逻辑为真实建模逻辑，然后重新运行 `run_and_verify.py`。
5. **S5 自动检测+修复**：运行证据门禁、数字一致性、参数一致性、结果合理性检查，失败时自动修复：
   ```bash
   python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s5
   ```
   未通过时继续补证据，不进入正式成稿。
6. 证据门禁通过后，运行 `paper-formal-writer/scripts/build_paper_outline.py` 生成 `paper_output/plan/paper_outline.json`。
7. Agent 读取 `paper_outline.json`、完整证据链和提示词资产，全局撰写 `paper_output/final_paper_source.md`。
8. **公式渲染+修复**：运行 LaTeX 公式渲染器，失败时自动修正语法：
   ```bash
   python .claude/skills/latex-renderer/scripts/render_formulas.py
   python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage latex
   ```
9. **S6 自动检测+修复**：运行格式门禁、图表质量、引用一致性、AIGC检测，失败时自动修复：
   ```bash
   python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s6
   ```
10. 运行 `paper-formal-writer/scripts/format_formal_docx.py` 生成正式 Word。
11. **S7 自动检测+修复**：运行三审计层（一致性、完整性、符号表），失败时自动修复：
    ```bash
    python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s7
    ```
12. 所有检测通过后，最终交付。

### Quickstart 验证流程（不是正式论文生产流程）
0. **输出目录规划**:
   - 调用 `paper-workflow-orchestrator/scripts/prepare_output_layout.py`，生成 `paper_output/OUTPUT_LAYOUT.md` 和 `paper_output/code/` 工作区说明。
   - 这一步只建立落点规范，不执行黑盒建模。
1. **赛题结构化分析**:
   - 调用 `problem-doc-model-selector/scripts/analyze_problem.py`，生成 `paper_output/step1/problem_analysis.json`。
   - 将每一问的任务类型、推荐模型、验证计划和建议图表固化为后续 skill 可读取的数据契约。
2. **模型路线与评分闭环**:
   - 调用 `modeling-paper-rubric-and-model-selector/scripts/build_model_route.py`，生成 `paper_output/plan/model_route.json`、`rubric_alignment.json` 和 `scoring_strategy.md`。
   - 若该步骤失败，流程继续，QA 回退到 `problem_analysis.json`。
3. **外部资源获取 (Optional)**:
   - 调用 `authoritative-data-harvester` 或 `g-sci` (若存在) 填充 `crawled_data/`。
   - **Memory Update**: 将获取的文献/数据源更新至 `memoryskill.md`。
4. 调用 `data-cleaning-and-visualization/scripts/run_pipeline.py`：先生成 `data_plan.json`、`visualization_plan.json` 与 `figure_index.json`，再扫描 `problem_files/` 与 `crawled_data/`，产出清洗数据与图表到 `paper_output/`。
5. 调用 `model-code-and-result-generator/scripts/build_result_contracts.py`：根据模型路线、清洗数据和图表计划生成 `model_results.json`、`metrics.json`、`conclusions.json` 与 `table_index.json`。真实赛题中应继续让 Agent 在 `paper_output/code/modeling/` 二次生成或修改专用建模代码，并补齐真实结果。
6. 调用 `quality-assurance-auditor/scripts/pipeline.py`：检查 `problem_files/`，优先根据模型路线、评分点、数据图表和结果证据生成动态 `paper_output/tasks.json`。
7. 调用 `paper-micro-unit-generator/scripts/generate_all_offline.py`：生成 `paper_output/micro_units/*.txt` 与 `paper_output/generate_log.json`。
8. 调用 `paper-micro-unit-generator/scripts/merge.py`：生成 `paper_output/final_paper.md` 与 `paper_output/ref_check.md`，**并直接生成 `paper_output/final_paper.docx`**。
9. **[Mandatory] Word 交付验证**:
   - 检查 `paper_output/final_paper.docx` 是否存在。
   - 优先使用 `scripts/merge.py` 直接生成的 Word 版本（原生 python-docx 生成，不依赖 Pandoc）。
   - 仅在直接生成失败时，才尝试调用 Pandoc 作为兜底方案。
   - 确保公式、图表、目录在 Word 中显示正常。

### 分步运行（需要时才用）

0. **外部资源获取**:
   - 若需要补充文献或数据，先运行 `authoritative-data-harvester` 或其他搜索技能。

0.5. 仅准备输出目录规划：
```bash
python .claude/skills/paper-workflow-orchestrator/scripts/prepare_output_layout.py
```

1. 仅做数据清洗与可视化：
```bash
python .claude/skills/data-cleaning-and-visualization/scripts/run_pipeline.py
```

1.5. 仅生成结果证据契约：
```bash
python .claude/skills/model-code-and-result-generator/scripts/build_result_contracts.py
```

2. 仅做赛题结构化分析：
```bash
python .claude/skills/problem-doc-model-selector/scripts/analyze_problem.py
```

3. 仅生成模型路线与评分闭环：
```bash
python .claude/skills/modeling-paper-rubric-and-model-selector/scripts/build_model_route.py
```

4. 仅生成任务清单（会检查 `problem_files/` 不为空，并优先读取 `model_route.json`）：
```bash
python .claude/skills/quality-assurance-auditor/scripts/pipeline.py
```

5. 仅生成微单元：
```bash
python .claude/skills/paper-micro-unit-generator/scripts/generate_all_offline.py
```

6. 仅合并生成论文：
```bash
python .claude/skills/paper-micro-unit-generator/scripts/merge.py
```

7. 仅生成正式论文大纲契约：
```bash
python .claude/skills/paper-formal-writer/scripts/build_paper_outline.py
```

8. 仅格式化正式 Word：
```bash
python .claude/skills/paper-formal-writer/scripts/format_formal_docx.py
```

9. 仅检查正式论文格式：
```bash
python .claude/skills/paper-formal-writer/scripts/check_paper_format.py
```

## 常见问题

- 报错“problem_files 为空”：把赛题 PDF/Word 与附件数据放进 `problem_files/` 后重跑。
- 想要看题意拆解：查看 `paper_output/step1/problem_analysis.json` 和 `paper_output/step1/A_题意对齐.md`。
- 想要看模型路线：查看 `paper_output/plan/model_route.json` 和 `paper_output/plan/scoring_strategy.md`。
- 想要看论文产出：最终文件是 `paper_output/final_paper.docx`，中间稿是 `paper_output/final_paper.md`。
- 想要看输出位置规划：查看 `paper_output/OUTPUT_LAYOUT.md`。
- 想要看赛题专用代码：查看 `paper_output/code/`，不要到 skill 包目录里找当前赛题代码。
- 想要看数据与图表：清洗数据在 `paper_output/data_cleaned/`，图表在 `paper_output/figures/`。
- 想要看结果证据：查看 `paper_output/results/` 与 `paper_output/tables/table_index.json`；其中草稿状态的结果需要结合真实建模代码补齐。
