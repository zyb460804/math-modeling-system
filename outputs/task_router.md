# outputs/task_router.md

> **v3.4 统一入口版 | 2026-06-21** | 统一索引见 `outputs/INDEX.md`

> 用于把”用户当前任务”快速路由到正确的 skill、prompts、outputs 和 deliverables，避免临时发挥和错调工具。

---

## 一、黄金路径速查（v3.4 更新）

| 常见任务 | 最短调用路径 | 必查质量门 | 结果去向 |
|---|---|---|---|
| 正式赛题全流程 | `paper-workflow-orchestrator` → 按阶段路由 | 证据门禁 + 三审计层 | `paper_output/` |
| 审题选模 | `/analyze` skill（统一入口） | 题型判断+模型路线 | `paper_output/step1/` |
| 审论文打分 | `/review` skill → `paper-reviewer` agent（统一入口） | 全量深度报告（9部分） | `paper_output/qa/` |
| 生成代码 | `/code` skill（从零生成）或 `/algorithm-runner`（执行模板） | 参数一致性门禁 | `paper_output/code/` |
| 生成图示 | `/figure` skill（统一入口） | render_check | `paper_output/figures/` |
| 准备答辩 | `/defense` skill（统一入口） | 问答+追问+模拟评分 | `deliverables/slides/` |
| 生成提交包 | `/submit` skill（统一入口） | 最终质量门 | `deliverables/` |
| 润色论文 | `paper-polisher` skill | 12点检查+质量评分 | 修改稿 |
| 降AI味 | `humanizer-zh-academic` skill（默认）或 `aigc-reduce` | 60分制 | 修改稿 |
| 一致性审计 | `consistency-auditor` skill | 三审计层第一层 | `qa/consistency_audit_report.json` |
| 完整性审计 | `completeness-auditor` skill | 三审计层第二层 | `qa/completeness_audit_report.json` |
| 记录决策 | `decision-logger` skill | 用户决策门禁 G2.5/G4.5 | `qa/decision_log.json` |

---

## 二、统一入口路由表（v3.4 新增）

> **核心原则：同一意图 → 默认最深输出。** 用户不需要知道"加什么词"才能拿到完整结果。

| 统一入口 | 覆盖的触发词 | 默认输出 | 对应 Skill |
|---------|-------------|---------|-----------|
| `review` / `paper-reviewer` agent | 打分、审稿、严格打分、深度评审、审论文 | 全量深度报告（9部分：总分+7模块+9信号+13要素四档+锚点对比+扣分细则+P0/P1/P2+门槛核验+三句话） | `review` |
| `defense` | 准备答辩、模拟答辩、答辩练习、评委提问 | 全量答辩包（10类问答+30条追问链+模拟评分+短答模板+分题型重点+风险预警） | `defense` |
| `analyze` | 审题、选模、推荐模型、建模路线 | 全量审题选模报告（题型判断+Top3路线+代码模板路径+风险预警+检验包+写作落点） | `analyze` |
| `figure` | 生成图示、画图、流程图、网络图、函数图、交互式图表、论文图、推荐图表 | 统一图表方案（自动判断需求→分派子skill→生成全部所需图→更新figure_index.json） | `figure` |
| `paper-polisher` | 润色、改写、polish、换个说法、更学术一点、更简洁一点 | 完整12点检查+段落改写+变更摘要+质量评分（60分制） | `paper-polisher` |
| `code` | 生成代码 | 从零生成代码框架（输出末节自动引 algorithm-runner） | `code` |
| `algorithm-runner` | 运行算法、执行代码 | 执行已有算法模板（输出末节自动引 code） | `algorithm-runner` |
| `submit` | 生成提交包 | 最终比赛提交包（自动判断阶段；输出末节说明与 solution-package-builder 的区别） | `submit` |
| AIGC降重 | 降AI味、降重、去AI检测 | 默认走 humanizer-zh-academic（14种AI模式+7项硬约束）；备选 aigc-reduce | `humanizer-zh-academic` |

---

## 三、先判断任务属于什么

任何任务先按下面四个问题判断：

1. 当前是在建系统，还是在做个案？
2. 当前是 `demo` 还是 `real_case`？
3. 当前最缺的是规则、路线、正文、代码、图示、审稿意见，还是提交包？
4. 当前输入最完整的是题面、数据、可提交稿、结果，还是只有一个模糊目标？

只要这四点清楚，后面的调用顺序就会稳定很多。

---

## 四、一级路由表（v3.4 更新）

### 轨道 A：Skill 自动化流水线（正式赛题推荐）

| 当前任务 | 典型输入 | 主入口 Skill | 必读 outputs | 默认产出 |
|---|---|---|---|---|
| 正式赛题全流程 | 赛题PDF+附件 | `paper-workflow-orchestrator` | 全部 | `paper_output/` 完整产物 |
| 题意解析 | 赛题PDF/截图 | `problem-doc-model-selector` | `outputs/problem_type_taxonomy.md` | `problem_analysis.json` |
| 模型路线 | `problem_analysis.json` | `modeling-paper-rubric-and-model-selector` | `outputs/method_matching.md` | `model_route.json`、`scoring_strategy.md` |
| 外部数据获取 | 需要补充文献/数据 | `authoritative-data-harvester` | - | `crawled_data/` |
| 数据处理与图表 | 附件数据 | `data-cleaning-and-visualization` | `outputs/data_cleaning_standards.md` | `paper_output/data_cleaned/`、`paper_output/figures/` |
| 特征工程 | 原始数据 | `feature-engineering` | - | 特征矩阵 |
| 建模代码与结果 | 数据+模型路线 | `model-code-and-result-generator` | `outputs/algorithm_templates.md` | `paper_output/results/` |
| 算法基准测试 | 多个算法 | `algorithm-benchmark` | - | 性能对比报告 |
| 证据门禁 | 所有产物 | `quality-assurance-auditor` | `outputs/final_quality_gate.md` | `qa/evidence_gate_report.json` |
| 正式写作 | 证据门禁通过 | `paper-formal-writer` | `outputs/writing_templates.md` | `final_paper_source.md`、`final_paper.docx` |
| 微单元生成 | 需要分块写作 | `paper-micro-unit-generator` | - | `paper_output/micro_units/` |
| 上下文记忆 | 各阶段完成后 | `context-memory-keeper` | - | 三层记忆更新 |

### 轨道 B：统一入口 Skill（手动/局部任务）

| 当前任务 | 典型输入 | 统一入口 | 默认产出 |
|---|---|---|---|
| 审题选模 | 赛题PDF | `/analyze` | 全量审题选模报告 |
| 审论文打分 | 论文稿 | `/review` → `paper-reviewer` agent | 全量深度报告（9部分） |
| 生成代码 | 模型路线 | `/code` | 代码框架（末节引 algorithm-runner） |
| 运行算法 | 已有代码 | `/algorithm-runner` | 执行结果（末节引 code） |
| 生成图示 | 需求描述 | `/figure` | 全部图表+索引 |
| 准备答辩 | 论文+结果 | `/defense` | 全量答辩包 |
| 生成提交包 | 全部产物 | `/submit` | 比赛提交包 |
| 润色论文 | 论文段落 | `paper-polisher` | 12点检查+改写+评分 |
| 降AI味 | 论文文本 | `humanizer-zh-academic` | 降重后文本 |
| 符号表构建 | 多个子问题 | `symbol-table-builder` | 统一符号表 |
| 鲁棒性检验 | 模型结果 | `robustness-checker` | 灵敏度/误差/基线对比 |
| 引用溯源 | 引用列表 | `citation-tracer` | 引用真实性验证 |
| 写作风格校准 | 用户过往作品 | `style-calibration` | 风格特征文件 |
| AI失败模式检查 | 论文/代码 | `ai-failure-checker` | 7-mode blocking checklist |
| 决策记录 | 选模/结果判断 | `decision-logger` | `qa/decision_log.json` |

### 三审计层（v3.6 新增）

| 审计层 | Skill | 检查内容 | 产出 |
|--------|-------|---------|------|
| 第一层 | `consistency-auditor` | 数字/文件名/符号一致性 | `qa/consistency_audit_report.json` |
| 第二层 | `completeness-auditor` | 审查文件/报告/产物齐全 | `qa/completeness_audit_report.json` |
| 第三层 | `quality-assurance-auditor` | 工作流完整性+反编造 | `qa/evidence_gate_report.json` |

### 传统 Prompt 路由（轨道 B 备选）

| 当前任务 | 典型输入 | 主入口 prompt | 必读 outputs | 默认产出 |
|---|---|---|---|---|
| 扫一遍资料 | 一批目录、资料包、历史文件 | `prompts/01_full_scan.md` | `outputs/file_map.md`、`outputs/asset_registry.md` | 更新文件地图与优先级 |
| 新增材料入库 | 新增 PDF/DOCX/代码/模板/案例资料 | `prompts/01_full_scan.md`、`prompts/02_extract_cards.md` | `outputs/material_inventory.md`、`outputs/extracted_document_text/`、`outputs/extracted_pdf_text/`、`outputs/_reports/award_pdf_extraction_report.md`、`outputs/_reports/award_pdf_ocr_report.md`、`outputs/extracted_material_synthesis.md`、`outputs/code_asset_index.md` | 形成可检索文本层、代码索引和回灌清单 |
| 抽卡建库 | 已扫描的资料 | `prompts/02_extract_cards.md` | `outputs/knowledge_base.md` | 更新知识卡片 |
| 知识点更新 | 新增规则、资料、提示词、算法、案例经验 | `prompts/29_update_knowledge_assets.md` | `outputs/knowledge_update_workflow.md`、`outputs/asset_registry.md`、`outputs/prompts_outputs_call_map.md` | 分类、回灌、同步、登记和待确认清单 |
| 建规则库 | 已有抽卡结果 | `prompts/03_build_rules.md` | `outputs/method_matching.md`、`outputs/writing_templates.md` 等 | 更新母库 |
| 调用提示词总母版 | 阶段目标、题面、数据字段、论文初稿或结果 | `prompts/25_prompt_master_pack.md` | `outputs/prompt_master_pack.md`、`outputs/prompts_outputs_call_map.md` | 抽取当前阶段可直接复制的提示词 |
| 新题开工 | 一道新题、附件说明、初始想法 | `prompts/23_start_new_case.md` | `outputs/task_router.md`、`outputs/production_specs.md`、`outputs/method_matching.md` | 单题开工包 |
| 审题 | 赛题、题面截图、任务说明 | `prompts/11_identify_problem_type.md` | `outputs/problem_type_taxonomy.md`、`outputs/model_selection_flow.md` | 题型判断与误判提醒 |
| 数据理解与预处理 | 题面附件、字段说明、原始数据 | `prompts/30_data_understanding.md` | `outputs/data_understanding_workflow.md`、`outputs/data_cleaning_standards.md` | 字段映射、数据质量诊断、建模输入输出表 |
| 选模 | 题型、约束、数据特征 | `prompts/12_select_model_route.md` | `outputs/method_matching.md`、`outputs/model_validation_by_type.md` | 主路线与备选路线 |
| 电工杯专题 | 电力/负荷/调度/机组/风光 | `prompts/12_select_model_route.md` | `outputs/competition_workflow.md` | 电工杯建模路线、代码模板、图表和答辩口径 |
| 写论文 | 题面、模型、结果、草稿 | `prompts/15_rewrite_abstract.md` 或 `prompts/05_generate_templates.md` | `outputs/writing_templates.md`、`outputs/result_analysis_templates.md` | 论文段落 |
| 生成代码 | 模型路线、参数、数据结构 | `prompts/19_generate_code.md` | `outputs/algorithm_templates.md`、`outputs/code_template_playbook.md` | 代码骨架或脚本 |
| 组合建模 | 评价后还要预测/优化、组合模型 | `prompts/12_select_model_route.md` | `outputs/model_chain_blueprints.md`、`outputs/method_matching.md` | 组合模型代码、阶段结果表、论文解释口径 |
| 生成图示 | 逻辑流程、变量关系、结果说明 | `prompts/20_generate_figures.md` | `outputs/figure_templates.md`、`outputs/visual_knowledge_base.md` | 图示方案与草图 |
| 生成表格与结果对表 | 参数、结果、代码输出、论文草稿 | `prompts/26_generate_tables.md` | `outputs/table_result_alignment_workflow.md`、`outputs/table_templates.md` | 表格方案与结果一致性核对表 |
| 生成 PPT 与讲述稿 | 论文、图表、核心结果、答辩目标 | `prompts/27_generate_slides.md` | `outputs/slide_defense_workflow.md`、`outputs/defense_qa_bank.md` | PPT 页面方案、讲述稿、备用问答 |
| 审稿改稿 | 可提交稿/修改稿/定稿 | `prompts/08_review_math_modeling_paper.md` | `outputs/scoring_rubric.md`、`outputs/review_priority_matrix.md`、`outputs/revision_checklist.md` | 按唯一评分量表输出 P0/P1/P2 问题单 |
| 准备答辩 | 论文、模型、结果、PPT 提纲 | `prompts/09_defense_math_modeling.md` | `outputs/defense_qa_bank.md`、`outputs/defense_followup_chains.md` | 问答与追问链 |
| 动态验收 | 代码、论文、结果文件、图表 | `prompts/24_dynamic_acceptance.md` | `outputs/reproducibility_checklist.md`、`outputs/revision_checklist.md` | 运行结果与真实性判定 |
| 最终质量门 | 论文、代码、图表、表格、PPT、AI说明 | `prompts/28_final_quality_gate.md` | `outputs/final_quality_gate_workflow.md`、`outputs/final_quality_gate.md` | 是否可提交/可答辩/可复现的放行判断 |
| 生成提交包 | 论文、代码、图示、表格、PPT | `prompts/21_generate_submission_pack.md` | `outputs/reproducibility_checklist.md` | 提交清单与缺口清单 |
| 个案回灌 | 已完成案例、审稿结果、答辩记录 | `prompts/22_case_feedback_loop.md` | `outputs/case_feedback_loop.md` | 母库更新任务清单 |

---

## 五、总路由规则

1. 如果用户只是问"怎么看、怎么优化、怎么升级"，优先归为系统建设或方案咨询。
2. 如果用户给出具体赛题，优先归为审题选模（`/analyze`）。
3. 如果用户给出论文稿，优先归为审稿改稿（`/review`）。
4. 如果用户给出数据或要求建模求解，优先归为代码生成（`/code`）或表格/图示生成（`/figure`）。
5. 如果用户接近交稿，优先归为提交冲刺（`/submit`）。
6. 如果用户给出做完后的经验、失误或评审反馈，优先归为个案回灌。
7. 如果任务要宣称可提交、可答辩或可复现，必须先走三审计层（consistency → completeness → quality-assurance）。
8. 如果涉及数据、字段、附件或参数，必须先统一数据口径。
9. **同一意图 → 默认最深输出**：用户不需要知道"加什么词"才能拿到完整结果。

---

## 六、GitHub 融合新增内容（v4.0）

### 合同体系

| 合同类型 | 模板位置 | 用途 |
|---------|---------|------|
| 模型合同 | `paper-workflow-orchestrator/references/model-contract-template.md` | 前置合同：核心结论+证据链+反冗余+交付规格 |
| 图表合同 | `paper-workflow-orchestrator/references/figure-contract-template.md` | 图表合同：结论+面板证据+灰度安全+色盲无障碍 |

### 门控架构（G1-G6）

| 门控 | 时机 | 要求 | 参考文档 |
|------|------|------|---------|
| G1 | 预检通过 | problem_files 非空 | `paper-workflow-orchestrator/references/gate-system.md` |
| G2 | PoC验证 | 每个候选方法有≤30行PoC | `paper-workflow-orchestrator/references/poc-validation-gate.md` |
| G2.5 | 方法选择后 | 用户填写选择理由（≥50字） | `decision-logger` skill |
| G3 | 证据门禁 | 所有产物通过QA | `quality-assurance-auditor` |
| G4 | 结果确认 | 用户确认结果合理性 | `decision-logger` skill |
| G4.5 | 结果确认后 | 用户填写确认理由（≥30字） | `decision-logger` skill |
| G5 | 格式门禁 | 论文格式检查通过 | `paper-formal-writer` |
| G6 | 最终门禁 | 三审计层全部PASS | `consistency-auditor` + `completeness-auditor` + `quality-assurance-auditor` |

### 数字冻结机制

参考：`paper-workflow-orchestrator/references/frozen-numbers-convention.md`

**3步解冻-修改-重冻**：
1. 解冻：从 `frozen_numbers.json` 读取当前冻结值
2. 修改：在代码/论文中修改数值
3. 重冻：更新 `frozen_numbers.json` 并重新校验一致性

### 选型资源

| 资源 | 路径 | 用途 |
|------|------|------|
| 95+场景选型矩阵 | `model-selector/references/model-selection-matrix.md` | 场景×问题决策矩阵 |
| 问题分解法 | `model-selector/references/problem-decomposition.md` | 12型问题分类+信号词+I/O规范 |
| 端到端Playbook | `model-selector/references/playbooks/` (12个) | 调度/物理/ML/评价/博弈/路径/数据/几何/网络/环境/政策 |

### 领域知识库（8大Cookbook）

| Cookbook | 路径 | 覆盖算法 |
|---------|------|---------|
| 优化 | `model-code-and-result-generator/references/cookbook-optimization.md` | GA/PSO/SA/LP/DP |
| 机器学习 | `model-code-and-result-generator/references/cookbook-ml.md` | XGBoost/RF/SVM/NN |
| 评价 | `model-code-and-result-generator/references/cookbook-evaluation.md` | TOPSIS/AHP/熵权/模糊 |
| 机理 | `model-code-and-result-generator/references/cookbook-mechanistic.md` | 传热/ODE/几何/光学 |
| 统计 | `model-code-and-result-generator/references/cookbook-statistical.md` | 假设检验/ANOVA/蒙特卡洛/贝叶斯 |
| 网络 | `model-code-and-result-generator/references/cookbook-network.md` | 图论/网络流/中心性 |
| 聚类 | `model-code-and-result-generator/references/cookbook-clustering.md` | 层次/K-Means/DBSCAN/GMM |
| 博弈 | `model-code-and-result-generator/references/cookbook-game-theory.md` | 纳什/演化/Stackelberg |

### 写作增强

| 资源 | 路径 | 用途 |
|------|------|------|
| Anti-AI检测指南 | `paper-formal-writer/references/anti-ai-detection-guide.md` | 8类AI痕迹+禁用词表+替换策略 |
| 4轮自审框架 | `paper-formal-writer/references/four-round-self-review.md` | Claim-Evidence→结构→表达→格式 |
| 章节架构 | `paper-formal-writer/references/section-architecture.md` | 摘要6要素/引言5要素/结果证据阶梯 |
| 证据金字塔 | `paper-formal-writer/references/evidence-pyramid.md` | 4层证据金字塔 |
| 常用短语库 | `paper-formal-writer/references/common-phrases.md` | 中英双语学术短语库（10章节） |
| 文献综述指南 | `paper-formal-writer/references/literature-review-guide.md` | T1/T2/T3信源路由+搜索4层法 |

---

## 七、先判断当前模式

### 1. demo 模式
适用场景：
- 还没有真实数据
- 先搭建链路
- 先验证目录、脚本和成品区是否能跑通

该模式下：
- 允许生成演示输出
- 允许保留占位字段
- 不允许宣称当前案例已可直接提交

### 2. real_case 模式
适用场景：
- 已拿到真实题面、真实数据或真实草稿
- 目标是做成该题最终交付物

该模式下：
- 必须补真实结果
- 必须补动态验收
- 必须补追溯链和最终口径一致性

---

## 八、二级路由：按当前缺口分流

### 1. 只有题面，没有路线
调用顺序：
1. `prompts/23_start_new_case.md`
2. `prompts/11_identify_problem_type.md`
3. `prompts/12_select_model_route.md`

### 2. 有路线，没有正文
调用顺序：
1. `prompts/05_generate_templates.md`
2. `prompts/15_rewrite_abstract.md`
3. `prompts/13_upgrade_result_analysis.md`

### 2.5 有题面或数据，但字段口径没理清
调用顺序：
1. `prompts/30_data_understanding.md`
2. `prompts/12_select_model_route.md`
3. `prompts/26_generate_tables.md`

### 3. 有正文，没有可信度
调用顺序：
1. `prompts/10_validation_output.md`
2. `prompts/14_strengthen_validation.md`
3. `prompts/16_low_score_risk_diagnosis.md`

### 4. 有模型，没有代码支撑
调用顺序：
1. `prompts/19_generate_code.md`
2. `prompts/21_generate_submission_pack.md` 中的代码清单部分

### 5. 有正文，没有图示
调用顺序：
1. `prompts/20_generate_figures.md`
2. 视情况同步更新 `deliverables/figures/`

### 5.5 有结果，但表格和数字口径没对齐
调用顺序：
1. `prompts/26_generate_tables.md`
2. `prompts/13_upgrade_result_analysis.md`
3. `prompts/28_final_quality_gate.md`

### 5.6 有论文和结果，要生成答辩 PPT
调用顺序：
1. `prompts/27_generate_slides.md`
2. `prompts/09_defense_math_modeling.md`
3. `prompts/18_defense_followup_drill.md`

### 6. 有完整可提交稿，要冲高分
调用顺序：
1. `prompts/08_review_math_modeling_paper.md`
2. `prompts/17_check_chain_closure.md`
3. `prompts/18_defense_followup_drill.md`

### 7. 一个案例做完了，要沉淀成系统资产
调用顺序：
1. `prompts/22_case_feedback_loop.md`
2. 视反馈结果更新相关 `outputs/`
3. 最后登记 `outputs/asset_registry.md`

### 8. 想验证当前案例到底是不是“真完成”
调用顺序：
1. `prompts/24_dynamic_acceptance.md`
2. `prompts/28_final_quality_gate.md`
3. `prompts/21_generate_submission_pack.md`
4. `prompts/22_case_feedback_loop.md`

### 9. 有大量新增资料，要先抽取再回灌
调用顺序：
1. 先用 `outputs/material_inventory.md` 判断新增资料类型、数量和优先级
2. DOCX/提示词/模板类先查 `outputs/extracted_document_text/`，确认是否已有可检索文本
3. 获奖/优秀论文 PDF 先查 `outputs/extracted_pdf_text/`、`outputs/_reports/award_pdf_extraction_report.md` 和 `outputs/_reports/award_pdf_ocr_report.md`，不要把未 OCR 或低文本量文件当作已读材料
4. 代码类资料先查 `outputs/code_asset_index.md`，不要直接从零生成代码
5. 用 `outputs/extracted_material_synthesis.md` 把新增资料转成回灌清单
6. 按主题分别更新 `outputs/knowledge_base.md`、`outputs/method_matching.md`、`outputs/scoring_rubric.md`、`outputs/code_template_playbook.md`
7. 最后补登记到 `outputs/asset_registry.md`

### 10. 用户新增了知识点，要全系统吸收
调用顺序：
1. `prompts/29_update_knowledge_assets.md`
2. `outputs/knowledge_update_workflow.md`
3. 先判断新增知识属于资料、规则、方法、写作、代码、提示词、答辩、案例经验还是系统流程
4. 按类型回灌到对应 `outputs/` 母库
5. 若影响调用方式，同步更新 `outputs/task_router.md` 和 `outputs/prompts_outputs_call_map.md`
6. 若形成核心资产，同步更新 `outputs/asset_registry.md`
7. 若能形成交付模板，同步更新 `deliverables/`
8. 若具有通用价值，同步检查根目录 `outputs/` 与 `prompts/` 体系
9. 最后输出已更新文件、仍需人工确认项和下一次调用建议

---

## 九、按题型反推主路径

| 题型判断 | 优先读取 | 主 prompt | 配套 outputs | 后续产出重点 |
|---|---|---|---|---|
| 评价类 | `outputs/problem_type_taxonomy.md` | `prompts/12_select_model_route.md` | `outputs/method_matching.md`、`outputs/method_misuse_alerts.md` | 指标体系、赋权、评价解释 |
| 预测类 | `outputs/model_selection_flow.md` | `prompts/12_select_model_route.md` | `outputs/model_validation_by_type.md` | 精度、误差、稳健性 |
| 优化类 | `outputs/model_selection_quick_table.md` | `prompts/12_select_model_route.md` | `outputs/algorithm_templates.md` | 目标函数、约束、求解与灵敏度 |
| 机理类 | `outputs/problem_type_taxonomy.md` | `prompts/12_select_model_route.md` | `outputs/model_chain_blueprints.md` | 假设、变量关系、动态机制 |
| 分类/识别类 | `outputs/method_matching.md` | `prompts/12_select_model_route.md` | `outputs/model_validation_by_type.md` | 特征、判别标准、误判分析 |
| 链式综合题 | `outputs/model_chain_blueprints.md` | `prompts/17_check_chain_closure.md` | `outputs/result_analysis_templates.md` | 中间层输出如何进入决策层 |

---

## 十、升级后建议的统一入口

以后只要任务还不明确，先走：

1. `prompts/00_route_task.md`
2. 看 `outputs/task_router.md`
3. 判断当前是 `demo` 还是 `real_case`
4. 再进入专项 prompt

这样可以减少四类常见错误：

1. 明明是审题任务，却直接开始写摘要
2. 明明要生成成品，却还停留在规则摘要
3. 明明案例已完成，却没有把经验回灌到母库
4. 明明还是 demo，却误判成 real_case 终稿

---

## 十一、统一主链路

本系统所有任务最终都归到同一条主链路中：

**任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌**

不同任务可以跳过不相关环节，但不得跳过两个控制点：

1. 涉及数据、字段、附件或参数时，必须先统一数据口径。
2. 宣称可提交、可答辩或可复现前，必须经过最终质量门。

---

## 十二、最短判断口令

如果你只想记一句：

> 先分清”我现在做系统还是做单题、是 demo 还是 real_case、最缺什么”，再按本路由表进入对应 prompt，而不是看到哪个文件顺眼就先调哪个。

---

## 十三、信息不足时的最小追问

| 缺口 | 只问这一句 |
|---|---|
| 不知道题型 | “最终要输出的是预测值、排序、最优方案、解释关系，还是分类/分群结果？” |
| 不知道数据 | “现在有数据文件吗？如果有，请给字段名或前几行样例。” |
| 不知道结果 | “已有模型结果或图表吗？如果没有，我先按待补结果写结构稿。” |
| 不知道交付 | “你要的是论文正文、代码、图表、表格、PPT，还是提交包清单？” |

---

## 十四、默认优先级

1. 比赛临场：先成品，后沉淀。
2. 系统建设：先索引，后模板，再工程化。
3. 论文改稿：先 P0，后 P1，再 P2。
4. 代码任务：先可运行，后好看，最后扩展。

---

## 十五、v4.2/v4.3 新增能力路由（工具型，非阶段型）

> 以下为新融合的工具型能力。它们**不改变主流程**，而是在对应阶段被按需调用。
> 触发词命中时，路由到对应 skill 的脚本；脚本未装依赖则提示安装。

### 读题 / 取数阶段

| 触发词 | 路由到 | 产出 |
|--------|--------|------|
| 提取表格 / PDF 表格 | `data-cleaning-and-visualization/scripts/extract_pdf_tables.py` | `paper_output/code/data/table_*.csv` + tables_index.json |
| 公式 OCR / 提取公式 | `problem-doc-model-selector/scripts/extract_formulas_ocr.py` | `paper_output/code/formulas_ocr.json` |
| 拉宏观数据 / 经济数据 | `authoritative-data-harvester/scripts/akshare_fetch.py` | `paper_output/code/data/<接口>.csv` + _meta.json |

### 建模 / 调参阶段

| 触发词 | 路由到 | 产出 |
|--------|--------|------|
| 超参调优 / 调参 | `model-code-and-result-generator/scripts/optuna_tune.py` | `paper_output/code/tune/best_params.json` + 优化历史图 |
| G4.6 自证门 | `model-code-and-result-generator/scripts/verification_template.py` + `qa-auditor/scripts/verify_gate.py` | `verifications/verify_*.py` 全 PASS |
| 模型可解释性 / SHAP | `feature-engineering/scripts/shap_explain.py` | `paper_output/figures/shap/*.png` + importance.json |
| **跑 MATLAB / ODE/曲线拟合/优化（MATLAB 强项）** | `matlab-model-code-generator/scripts/matlab_runner.py` + 3 模板 | `paper_output/code/matlab/run_report.json` + png/mat/json |

### 画图 / 写作阶段

| 触发词 | 路由到 | 产出 |
|--------|--------|------|
| 期刊风图表 / 图表美化 | `math-figure/scripts/journal_style.py` | 示例图 + 样式名清单 |
| 编译 LaTeX | `paper-formal-writer/scripts/compile_latex.py` | `paper_output/latex/build/*.pdf` |
| Typst 渲染 | `typst-renderer` skill（inject_typst.py） | `paper_output/typst/main.typ` → `final_paper.pdf` |
| 编辑 Word / Word 公式 | `docx-editor-cn` skill | 原生 OMML 公式 / XML 局部编辑 |
| 保留格式降重 | `aigc-reduce/scripts/replace_docx_preserve_format.py` | 格式不变的降重 .docx |

### 验收 / 交付阶段

| 触发词 | 路由到 | 产出 |
|--------|--------|------|
| 流水线状态 / 返工 | `qa-auditor/scripts/pipeline_manager.py` | `paper_output/state/pipeline.json` |
| 数值合理性 / inf nan | `qa-auditor/scripts/check_numeric_sanity.py` | `qa/numeric_sanity_report.json` |
| 报告新鲜度 | `context-memory-keeper/scripts/freshness_check.py` | STALE 报告清单 |
| 安全检查 / 密钥扫描 | `consistency-auditor/scripts/security_check.py` | 终端报告（git commit 前自动拦截） |
| 查优秀论文 / O 奖检索 | `award-paper-rag` skill（retrieve 离线 / chat 需 key） | 相关章节 top-k |

### 路由优先级

- 用户口令命中 → 走对应脚本（不进 orchestrator 主流水线）
- 主流水线运行中（如 code 阶段）→ orchestrator 可自动调 G4.6/numeric_sanity/security_check 做门禁
- 工具脚本依赖未装 → 打印安装提示，不阻断（降级到手动）
