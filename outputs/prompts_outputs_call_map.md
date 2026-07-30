# outputs/prompts_outputs_call_map.md

> **v2.0 | 2026-05-31 标准化更新**
> **统一索引入口：`outputs/INDEX.md`** — 按 8 大功能域快速定位文件。
> Prompt 编号 25_data_understanding 已重编号为 **30_data_understanding**，原 25 号仅保留 prompt_master_pack。

> 用于把 `prompts/` 与 `outputs/` 之间的调用关系一次性对齐，方便按任务阶段快速找到”该用哪个 prompt，配哪几个输出库”。

---

## 一、总原则

1. `prompts/` 负责**发起任务、组织动作、驱动输出**。
2. `outputs/` 负责**沉淀规则、提供模板、给出检查口径**。
3. `outputs/task_router.md` 负责**先分流，再调用**。
4. `outputs/asset_registry.md` 负责**把核心资产登记成统一索引**。
5. `outputs/case_feedback_loop.md` 负责**把个案经验重新回灌到母库**。
6. 最稳妥的使用方式不是单独调用某一个文件，而是：
   - 先用 prompt 定义当前任务；
   - 再用对应 outputs 作为规则支撑；
   - 最后把结果继续沉淀回 outputs。
7. 涉及数据、字段、附件或参数时，必须先配套 `outputs/data_cleaning_standards.md`。
8. 涉及提交、答辩或“能不能交”判断时，必须先配套 `outputs/final_quality_gate.md`。
9. 新增知识点、资料、提示词、算法或案例经验时，必须先配套 `outputs/knowledge_update_workflow.md`。
10. 若时间紧，优先保证：
   - 审题识别正确；
   - 选模路线清楚；
   - 检验最小可信度包补齐；
   - 结果分析能落地；
   - 答辩能回答“为什么这样做”。

---

## 二、常用任务调用包

| 任务包 | 推荐调用顺序 | 配套 outputs | 产出 |
|---|---|---|---|
| 新增知识包 | `prompts/29_update_knowledge_assets.md` → 必要时 `prompts/02_extract_cards.md` / `prompts/03_build_rules.md` | `outputs/knowledge_update_workflow.md`、`outputs/asset_registry.md`、专项母库 | 分类、回灌、同步、登记和待确认项 |
| 单题建模包 | `prompts/00_route_task.md` → `prompts/23_start_new_case.md` → 数据理解 → 审题选模 → 成品生产 | `outputs/task_router.md`、`outputs/data_cleaning_standards.md`、`outputs/method_matching.md` | 单题工作包、模型路线、交付物 |
| 论文改稿包 | `prompts/08_review_math_modeling_paper.md` → `prompts/17_check_chain_closure.md` → 必要时专项重写 | `outputs/scoring_rubric.md`、`outputs/revision_checklist.md`、`outputs/review_priority_matrix.md` | P0/P1/P2 修改清单 |
| 提交终检包 | `prompts/24_dynamic_acceptance.md` → `prompts/28_final_quality_gate.md` → `prompts/21_generate_submission_pack.md` | `outputs/final_quality_gate.md`、`outputs/reproducibility_checklist.md`、`outputs/table_result_alignment_workflow.md` | 可提交/可答辩/可复现判断 |

---

## 三、按阶段的最稳妥调用顺序

### 0. 任务路由阶段
推荐顺序：
1. `prompts/00_route_task.md`

优先配套输出库：
- `outputs/production_specs.md`
- `outputs/asset_registry.md`
- `outputs/task_router.md`

### 0.5 提示词总母版调用阶段
推荐顺序：
1. `prompts/25_prompt_master_pack.md`

优先配套输出库：
- `outputs/prompt_master_pack.md`
- `outputs/prompts_outputs_call_map.md`
- `outputs/task_router.md`
- `outputs/asset_registry.md`

适用场景：
- 比赛当天要直接复制高质量AI提示词
- 不确定当前阶段该用哪一段提示词
- 需要把国赛、五一赛、美赛A-F题型提示词统一调度

### 1. 审题 / 选题阶段
推荐顺序：
1. `prompts/07_select_topic.md`
2. `prompts/11_identify_problem_type.md`
3. `prompts/12_select_model_route.md`

优先配套输出库：
- `outputs/topic_selection_guide.md`
- `outputs/problem_type_taxonomy.md`
- `outputs/method_matching.md`
- `outputs/model_selection_flow.md`
- `outputs/model_selection_quick_table.md`
- `outputs/method_misuse_alerts.md`

### 2. 资料扫描 / 建库阶段
推荐顺序：
1. `prompts/01_full_scan.md`
2. `prompts/02_extract_cards.md`
3. `prompts/03_build_rules.md`

优先配套输出库：
- `outputs/file_map.md`
- `outputs/material_inventory.md`
- `outputs/extracted_document_text/`
- `outputs/extracted_pdf_text/`
- `outputs/_reports/award_pdf_extraction_report.md`
- `outputs/_reports/award_pdf_ocr_report.md`
- `outputs/code_asset_index.md`
- `outputs/extracted_material_synthesis.md`
- `outputs/knowledge_base.md`
- `outputs/scoring_rubric.md`
- `outputs/method_matching.md`
- `outputs/writing_templates.md`
- `outputs/bad_cases.md`

### 2.5 知识点更新 / 全系统回灌阶段
推荐顺序：
1. `prompts/29_update_knowledge_assets.md`
2. `prompts/02_extract_cards.md`（需要抽卡时）
3. `prompts/03_build_rules.md`（需要并入规则库时）
4. `prompts/22_case_feedback_loop.md`（来自完整案例时）

优先配套输出库：
- `outputs/knowledge_update_workflow.md`
- `outputs/material_inventory.md`
- `outputs/extracted_document_text/`
- `outputs/extracted_pdf_text/`
- `outputs/extracted_material_synthesis.md`
- `outputs/knowledge_base.md`
- `outputs/method_matching.md`
- `outputs/scoring_rubric.md`
- `outputs/writing_templates.md`
- `outputs/algorithm_templates.md`
- `outputs/code_template_playbook.md`
- `outputs/prompt_master_pack.md`
- `outputs/case_feedback_loop.md`
- `outputs/asset_registry.md`

### 3. 正式建模阶段
推荐顺序：
1. `prompts/11_identify_problem_type.md`
2. `prompts/12_select_model_route.md`
3. `prompts/17_check_chain_closure.md`（若是链式建模）

优先配套输出库：
- `outputs/problem_type_taxonomy.md`
- `outputs/method_matching.md`
- `outputs/model_selection_flow.md`
- `outputs/model_selection_quick_table.md`
- `outputs/model_specific_pitfalls.md`
- `outputs/method_misuse_alerts.md`

### 3.5 数据理解 / 预处理阶段
推荐顺序：
1. `prompts/30_data_understanding.md`
2. `prompts/26_generate_tables.md`（需要字段表、参数表、结果对表时）

优先配套输出库：
- `outputs/data_understanding_workflow.md`
- `outputs/data_cleaning_standards.md`
- `outputs/table_result_alignment_workflow.md`
- `outputs/table_templates.md`
- `outputs/reproducibility_checklist.md`
- `outputs/model_validation_by_type.md`

### 4. 写作 / 补正文阶段
推荐顺序：
1. `prompts/05_generate_templates.md`
2. `prompts/15_rewrite_abstract.md`
3. `prompts/13_upgrade_result_analysis.md`

优先配套输出库：
- `outputs/writing_templates.md`
- `outputs/abstract_templates.md`
- `outputs/abstract_micro_templates.md`
- `outputs/result_analysis_templates.md`
- `outputs/section_writing_templates.md`
- `outputs/chart_explanation_templates.md`
- `outputs/transition_sentence_bank.md`
- `outputs/bad_expression_blacklist.md`

### 5. 检验 / 稳健性补强阶段
推荐顺序：
1. `prompts/10_validation_output.md`
2. `prompts/14_strengthen_validation.md`

优先配套输出库：
- `outputs/validation_checklist.md`
- `outputs/model_validation_by_type.md`
- `outputs/sensitivity_and_robustness_templates.md`
- `outputs/review_priority_matrix.md`
- `outputs/result_analysis_templates.md`

### 6. 审稿 / 改稿阶段
推荐顺序：
1. `prompts/16_low_score_risk_diagnosis.md`
2. `prompts/04_review_my_paper.md`
3. `prompts/08_review_math_modeling_paper.md`

优先配套输出库：
- `outputs/common_failure_patterns.md`
- `outputs/model_specific_pitfalls.md`
- `outputs/revision_checklist.md`
- `outputs/review_priority_matrix.md`
- `outputs/review_section_checklists.md`
- `outputs/review_quick_comments.md`
- `outputs/scoring_rubric.md`

### 7. 答辩阶段
推荐顺序：
1. `prompts/27_generate_slides.md`
2. `prompts/06_mock_defense.md`
3. `prompts/09_defense_math_modeling.md`
4. `prompts/18_defense_followup_drill.md`

优先配套输出库：
- `outputs/slide_defense_workflow.md`
- `outputs/defense_qa_bank.md`
- `outputs/defense_short_answers.md`
- `outputs/defense_followup_chains.md`
- `outputs/defense_model_specific_answers.md`
- `outputs/defense_opening_and_closing.md`
- `outputs/scoring_rubric.md`

### 7.5 终检 / 提交放行阶段
推荐顺序：
1. `prompts/24_dynamic_acceptance.md`
2. `prompts/28_final_quality_gate.md`
3. `prompts/21_generate_submission_pack.md`

优先配套输出库：
- `outputs/final_quality_gate_workflow.md`
- `outputs/final_quality_gate.md`
- `outputs/reproducibility_checklist.md`
- `outputs/scoring_rubric.md`
- `outputs/review_priority_matrix.md`
- `outputs/table_result_alignment_workflow.md`

### 8. 个案回灌阶段
推荐顺序：
1. `prompts/22_case_feedback_loop.md`

优先配套输出库：
- `outputs/case_feedback_loop.md`
- `outputs/asset_registry.md`
- 与当前案例最相关的母库文件

---

## 三、逐 prompt 对照表

| Prompt | 主要作用 | 最该配套的 outputs | 最适合什么时候用 |
|---|---|---|---|
| `prompts/00_route_task.md` | 先把任务分流到正确工作流 | `production_specs.md`、`asset_registry.md`、`task_router.md` | 任何任务刚开始时 |
| `prompts/25_prompt_master_pack.md` | 调用AI提示词总母版，按阶段抽取可直接复制的提示词 | `prompt_master_pack.md`、`prompts_outputs_call_map.md`、`task_router.md` | 赛中需要快速拿到对应阶段提示词时 |
| `prompts/01_full_scan.md` | 扫描资料、建地图 | `file_map.md` | 刚接手资料时 |
| `prompts/02_extract_cards.md` | 抽卡沉淀可复用规则 | `knowledge_base.md` | 已扫完资料，准备沉淀时 |
| `prompts/03_build_rules.md` | 把碎规则收成母库 | `scoring_rubric.md`、`method_matching.md`、`writing_templates.md`、`bad_cases.md` | 规则开始成体系时 |
| `prompts/04_review_my_paper.md` | 通用总审稿 | `revision_checklist.md`、`review_quick_comments.md`、`scoring_rubric.md` | 论文已有完整草稿时 |
| `prompts/05_generate_templates.md` | 批量出模板 | `writing_templates.md`、`abstract_templates.md` | 需要快速搭论文骨架时 |
| `prompts/06_mock_defense.md` | 基础答辩演练 | `defense_qa_bank.md`、`defense_short_answers.md` | 首轮答辩准备 |
| `prompts/07_select_topic.md` | 选题判断 | `topic_selection_guide.md` | 比赛开题前 |
| `prompts/08_review_math_modeling_paper.md` | 数模专项终审 | `revision_checklist.md`、`review_priority_matrix.md`、`paper_score_calibration_library.md`、`deduplication_and_grading_guide.md` | 交稿前最后总审 |
| `prompts/09_defense_math_modeling.md` | 强化版答辩库 | `defense_qa_bank.md`、`defense_model_specific_answers.md` | 正式答辩准备 |
| `prompts/10_validation_output.md` | 系统化检验清单 | `validation_checklist.md` | 写检验小节时 |
| `prompts/11_identify_problem_type.md` | 先识别题型本质 | `problem_type_taxonomy.md`、`model_selection_flow.md` | 审题后、选模前 |
| `prompts/12_select_model_route.md` | 产出主路线与备选路线 | `method_matching.md`、`model_selection_quick_table.md`、`model_validation_by_type.md`、`competition_workflow.md`（电工杯专题） | 题型已判定后 |
| `prompts/13_upgrade_result_analysis.md` | 把报数结果升级成高分分析 | `result_analysis_templates.md`、`result_interpretation_templates.md`、`chart_explanation_templates.md`、`transition_sentence_bank.md` | 写结果分析时 |
| `prompts/14_strengthen_validation.md` | 快速补最小可信度包 | `validation_checklist.md`、`model_validation_by_type.md`、`sensitivity_and_robustness_templates.md` | 检验不足、时间紧时 |
| `prompts/15_rewrite_abstract.md` | 重写摘要 | `abstract_templates.md`、`abstract_micro_templates.md`、`bad_expression_blacklist.md` | 论文接近成稿时 |
| `prompts/16_low_score_risk_diagnosis.md` | 快速抓致命硬伤 | `common_failure_patterns.md`、`diagnostic_templates.md`、`review_priority_matrix.md` | 只想先抓最危险问题时 |
| `prompts/17_check_chain_closure.md` | 检查链式闭环是否成立 | `result_analysis_templates.md`、`review_section_checklists.md`、`common_failure_patterns.md` | 使用链式建模时 |
| `prompts/18_defense_followup_drill.md` | 练二追问、三追问 | `defense_followup_chains.md`、`defense_short_answers.md`、`defense_opening_and_closing.md` | 答辩前强化冲刺 |
| `prompts/19_generate_code.md` | 生成可运行或可替换的建模代码框架 | `algorithm_templates.md`、`code_template_playbook.md`、`python_algorithm_template_standard.md`、`model_validation_by_type.md` | 有模型路线但缺代码时 |
| `prompts/20_generate_figures.md` | 生成论文配图与答辩图示方案 | `figure_templates.md`、`visual_knowledge_base.md`、`visualization_strategy_library.md`、`chart_explanation_templates.md` | 有模型/结果但缺图示时 |
| `prompts/21_generate_submission_pack.md` | 生成可提交、可答辩、可复现的提交包方案 | `reproducibility_checklist.md`、`paper_upgrade_playbook.md`、`final_quality_gate_workflow.md` | 交稿前整理全套材料时 |
| `prompts/22_case_feedback_loop.md` | 把个案经验回灌为母库规则 | `case_feedback_loop.md`、`asset_registry.md` | 案例基本完成后 |
| `prompts/23_start_new_case.md` | 新题快速拉起单题工作包 | `task_router.md`、`production_specs.md`、`method_matching.md` | 刚拿到新题时 |
| `prompts/24_dynamic_acceptance.md` | 动态验收 demo/real_case 与复现真实性 | `reproducibility_checklist.md`、`revision_checklist.md` | 判断当前案例是否真完成时 |
| `prompts/30_data_understanding.md` | 生成数据理解、字段映射与预处理工作包 | `data_understanding_workflow.md`、`data_cleaning_standards.md` | 有附件/字段但口径没理清时 |
| `prompts/26_generate_tables.md` | 生成表格方案和结果对表 | `table_result_alignment_workflow.md`、`table_templates.md` | 有结果但表格/数字没对齐时 |
| `prompts/27_generate_slides.md` | 生成PPT页面方案和讲述稿 | `slide_defense_workflow.md`、`defense_qa_bank.md` | 论文结果已有、准备答辩时 |
| `prompts/28_final_quality_gate.md` | 做最终质量门和提交放行判断 | `final_quality_gate_workflow.md`、`final_quality_gate.md`、`scoring_rubric.md` | 提交前最后一轮检查时 |
| `prompts/29_update_knowledge_assets.md` | 新增知识点全系统吸收，完成分类、抽取、回灌、同步、登记 | `outputs/knowledge_update_workflow.md`、`outputs/asset_registry.md`、`outputs/prompts_outputs_call_map.md`、各专项母库 | 用户新增知识点、资料、提示词、案例经验后 |

---

## 四、按常见任务反推该调用什么

### 1. 我刚拿到题，不知道它本质是什么
直接调用：
- `prompts/11_identify_problem_type.md`
- `prompts/12_select_model_route.md`

配套：
- `outputs/problem_type_taxonomy.md`
- `outputs/model_selection_flow.md`
- `outputs/model_selection_quick_table.md`

### 2. 我已经知道是预测题，但不知道该上什么模型
直接调用：
- `prompts/12_select_model_route.md`

配套：
- `outputs/method_matching.md`
- `outputs/model_validation_by_type.md`
- `outputs/method_misuse_alerts.md`

### 3. 我论文结果分析很空，只会报数
直接调用：
- `prompts/13_upgrade_result_analysis.md`

配套：
- `outputs/result_analysis_templates.md`
- `outputs/chart_explanation_templates.md`
- `outputs/bad_expression_blacklist.md`

### 4. 我担心检验太弱，会被说“不可信”
直接调用：
- `prompts/10_validation_output.md`
- `prompts/14_strengthen_validation.md`

配套：
- `outputs/validation_checklist.md`
- `outputs/model_validation_by_type.md`
- `outputs/sensitivity_and_robustness_templates.md`

### 5. 我觉得摘要像流水账
直接调用：
- `prompts/15_rewrite_abstract.md`

配套：
- `outputs/abstract_templates.md`
- `outputs/abstract_micro_templates.md`
- `outputs/bad_expression_blacklist.md`

### 6. 我只剩几个小时，想先抓最致命问题
直接调用：
- `prompts/16_low_score_risk_diagnosis.md`
- `prompts/08_review_math_modeling_paper.md`

配套：
- `outputs/common_failure_patterns.md`
- `outputs/review_priority_matrix.md`
- `outputs/revision_checklist.md`

### 7. 我是链式建模，但总感觉两段是断的
直接调用：
- `prompts/17_check_chain_closure.md`
- `prompts/13_upgrade_result_analysis.md`

配套：
- `outputs/result_analysis_templates.md`
- `outputs/review_section_checklists.md`
- `outputs/common_failure_patterns.md`

### 8. 我要准备答辩，但怕被连续追问
直接调用：
- `prompts/09_defense_math_modeling.md`
- `prompts/18_defense_followup_drill.md`

配套：
- `outputs/defense_qa_bank.md`
- `outputs/defense_followup_chains.md`
- `outputs/defense_short_answers.md`

### 9. 我一个案例已经做完了，想让系统本身也变强
直接调用：
- `prompts/22_case_feedback_loop.md`

配套：
- `outputs/case_feedback_loop.md`
- `outputs/asset_registry.md`
- 与当前案例最相关的 `outputs/`

### 10. 我有数据和附件，但不知道字段怎么接模型
直接调用：
- `prompts/30_data_understanding.md`

配套：
- `outputs/data_understanding_workflow.md`
- `outputs/data_cleaning_standards.md`
- `outputs/table_templates.md`

### 11. 我有结果，但论文、表格、PPT数字怕不一致
直接调用：
- `prompts/26_generate_tables.md`
- `prompts/28_final_quality_gate.md`

配套：
- `outputs/table_result_alignment_workflow.md`
- `outputs/reproducibility_checklist.md`
- `outputs/final_quality_gate_workflow.md`

### 12. 我要把论文结果做成答辩PPT
直接调用：
- `prompts/27_generate_slides.md`
- `prompts/18_defense_followup_drill.md`

配套：
- `outputs/slide_defense_workflow.md`
- `outputs/defense_qa_bank.md`
- `outputs/defense_followup_chains.md`

### 13. 我要最终判断能不能提交
直接调用：
- `prompts/24_dynamic_acceptance.md`
- `prompts/28_final_quality_gate.md`
- `prompts/21_generate_submission_pack.md`

配套：
- `outputs/final_quality_gate_workflow.md`
- `outputs/final_quality_gate.md`
- `outputs/reproducibility_checklist.md`
- `outputs/scoring_rubric.md`

---

## 五、最稳妥的全流程组合包

### 1. 开题稳妥包
- `prompts/07_select_topic.md`
- `prompts/11_identify_problem_type.md`
- `prompts/12_select_model_route.md`

对应 outputs：
- `topic_selection_guide.md`
- `problem_type_taxonomy.md`
- `method_matching.md`
- `model_selection_flow.md`

### 2. 写作成稿包
- `prompts/05_generate_templates.md`
- `prompts/15_rewrite_abstract.md`
- `prompts/13_upgrade_result_analysis.md`
- `prompts/10_validation_output.md`

对应 outputs：
- `writing_templates.md`
- `abstract_templates.md`
- `result_analysis_templates.md`
- `validation_checklist.md`
- `section_writing_templates.md`

### 3. 冲刺改稿包
- `prompts/16_low_score_risk_diagnosis.md`
- `prompts/08_review_math_modeling_paper.md`
- `prompts/14_strengthen_validation.md`
- `prompts/17_check_chain_closure.md`

对应 outputs：
- `common_failure_patterns.md`
- `review_priority_matrix.md`
- `revision_checklist.md`
- `review_section_checklists.md`
- `model_validation_by_type.md`

### 4. 答辩强化包
- `prompts/06_mock_defense.md`
- `prompts/09_defense_math_modeling.md`
- `prompts/18_defense_followup_drill.md`

对应 outputs：
- `defense_qa_bank.md`
- `defense_short_answers.md`
- `defense_followup_chains.md`
- `defense_model_specific_answers.md`
- `defense_opening_and_closing.md`

### 5. 最强版冲刺包
- `prompts/07_select_topic.md`
- `prompts/11_identify_problem_type.md`
- `prompts/12_select_model_route.md`
- `prompts/13_upgrade_result_analysis.md`
- `prompts/14_strengthen_validation.md`
- `prompts/16_low_score_risk_diagnosis.md`
- `prompts/18_defense_followup_drill.md`

对应 outputs：
- `winning_paper_pattern_library.md`
- `case_to_method_route_library.md`
- `code_template_playbook.md`
- `paper_upgrade_playbook.md`
- `model_chain_blueprints.md`
- `visualization_strategy_library.md`

### 6. 最后24小时救稿包
- `prompts/15_rewrite_abstract.md`
- `prompts/13_upgrade_result_analysis.md`
- `prompts/14_strengthen_validation.md`
- `prompts/16_low_score_risk_diagnosis.md`
- `prompts/17_check_chain_closure.md`

对应 outputs：
- `paper_upgrade_playbook.md`
- `review_priority_matrix.md`
- `revision_checklist.md`
- `model_validation_by_type.md`
- `high_score_expression_library.md`
- `model_chain_blueprints.md`

### 7. C题链式冲刺包
- `prompts/11_identify_problem_type.md`
- `prompts/12_select_model_route.md`
- `prompts/17_check_chain_closure.md`
- `prompts/13_upgrade_result_analysis.md`
- `prompts/14_strengthen_validation.md`

对应 outputs：
- `case_to_method_route_library.md`
- `model_chain_blueprints.md`
- `result_analysis_templates.md`
- `model_validation_by_type.md`
- `visualization_strategy_library.md`

### 8. 高压答辩追问包
- `prompts/09_defense_math_modeling.md`
- `prompts/18_defense_followup_drill.md`
- `prompts/16_low_score_risk_diagnosis.md`

对应 outputs：
- `defense_qa_bank.md`
- `defense_followup_chains.md`
- `defense_short_answers.md`
- `defense_opening_and_closing.md`
- `high_score_expression_library.md`
- `winning_paper_pattern_library.md`

### 9. 系统升级包
- `prompts/00_route_task.md`
- `prompts/01_full_scan.md`
- `prompts/02_extract_cards.md`
- `prompts/03_build_rules.md`
- `prompts/22_case_feedback_loop.md`

对应 outputs：
- `production_specs.md`
- `asset_registry.md`
- `task_router.md`
- `knowledge_base.md`
- `case_feedback_loop.md`

---

## 六、最短调用建议

如果你不想记很多文件，只记下面这 10 个 prompt 就够了：

1. `00_route_task.md`
2. `07_select_topic.md`
3. `11_identify_problem_type.md`
4. `12_select_model_route.md`
5. `15_rewrite_abstract.md`
6. `13_upgrade_result_analysis.md`
7. `14_strengthen_validation.md`
8. `16_low_score_risk_diagnosis.md`
9. `18_defense_followup_drill.md`
10. `22_case_feedback_loop.md`

对应最常用 outputs：
- `production_specs.md`
- `task_router.md`
- `topic_selection_guide.md`
- `problem_type_taxonomy.md`
- `method_matching.md`
- `result_analysis_templates.md`
- `validation_checklist.md`
- `abstract_templates.md`
- `review_priority_matrix.md`
- `defense_qa_bank.md`
- `case_feedback_loop.md`

如果时间允许，最推荐再补这 6 个增强库：
- `case_to_method_route_library.md`：直接按典型题反推主路线。
- `high_score_expression_library.md`：把摘要、结果、检验、答辩压成更像高分稿的句式。
- `paper_upgrade_playbook.md`：最后 24 小时快速补闭环。
- `model_chain_blueprints.md`：链式题优先补“中间层输出 → 决策层输入”。
- `defense_short_answers.md`：把高频追问压成 15 秒—40 秒现场短答。
- `defense_followup_chains.md`：高压答辩时按主问题—二追问—三追问连续展开。

这套已经足够覆盖：**路由、审题、选模、写摘要、写结果、补检验、抓硬伤、练答辩、做完回灌**。

---

## 七、最终结论

现在这套系统的关系已经明确：

- `prompts/` = **动作层 / 调用层 / 工作流入口**
- `outputs/` = **规则层 / 模板层 / 审稿口径层**
- `task_router + asset_registry + case_feedback_loop` = **系统调度层 / 回灌层**

最稳妥的用法不是“只看 outputs”或“只跑 prompts”，而是：

> 先用路由入口分清任务，再调用对应 prompt 与 outputs 完成任务，最后把结果继续沉淀回 outputs。

这就是当前项目最完整、最顺手的调用方式。
