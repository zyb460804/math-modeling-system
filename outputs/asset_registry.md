# outputs/asset_registry.md

> **v2.1 | 2026-08-15 v4.8/v4.9 口径同步**（v2.0 | 2026-05-31 标准化更新）
> 本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。
> **⚠️ 口径同步公告（2026-08-15）：** ① `prompts/` 32 个文件 v4.8 已全部归档至 `prompts/_archive/`——本文 prompt 资产行仅作历史参考，正常任务走 Skill 统一入口（`outputs/task_router.md` §二）；② `outputs/final_quality_gate_workflow.md` 已归档（v4.8，被 `final_quality_gate.md` 覆盖）；③ 根目录 `README_structure.md` 已移至 `resources/_archive/`；④ `outputs/extracted_document_text/`、`outputs/extracted_pdf_text/` 目录已不存在（提取报告在 `outputs/_reports/`）。
> **统一索引入口：`outputs/INDEX.md`** — 按功能域快速定位文件。
> 涉及数据时先对齐 `data_cleaning_standards.md`；涉及提交时先检查 `final_quality_gate.md`；缺真实数据时统一标【待补】，不得编造。

> 用于把当前系统中的核心资产统一登记成可检索、可路由、可复用的索引表。

---

## 一、登记原则

每个核心资产尽量登记以下字段：

- 资产路径
- 资产类型
- 服务对象
- 适用题型
- 输入要求
- 输出结果
- 优先调用阶段
- 上游依赖
- 下游去向
- 维护状态

---

## 二、字段说明

| 字段 | 含义 | 填写要求 |
|---|---|---|
| 资产路径 | 文件或目录位置 | 尽量写相对路径 |
| 资产类型 | prompt / output / deliverable / source | 统一四类 |
| 服务对象 | 审题 / 建模 / 写作 / 代码 / 图示 / 审稿 / 答辩 / 提交 | 可多选 |
| 适用题型 | 评价 / 预测 / 优化 / 机理 / 分类 / 图论 / 仿真 / 综合决策 | 至少写一类 |
| 输入要求 | 运行前需要什么 | 题面 / 数据 / 初稿 / 结果 / 图表 等 |
| 输出结果 | 会产出什么 | 规则 / 模板 / 审稿意见 / 代码 / 图示 / 成品 |
| 优先调用阶段 | 何时最该调用 | 开题 / 建模 / 写作 / 冲刺 等 |
| 上游依赖 | 先读什么 | 若无则写“无” |
| 下游去向 | 会继续支持什么 | 指向其他 prompt、output 或 deliverable |
| 维护状态 | 已稳定 / 用户补入项 / 需回灌 | 用于后续迭代 |

---

## 三、分层速查

| 层级 | 首选资产 | 作用 | 何时调用 |
|---|---|---|---|
| 总控层 | `AGENTS.md`、`README.md` | 统一系统定位、主链路、目录分工 | 启动、交接、系统升级时（`README_structure.md` 已移至 `resources/_archive/`） |
| 路由调度层 | `outputs/task_router.md`、`outputs/asset_registry.md`、`outputs/prompts_outputs_call_map.md` | 判断当前任务、定位 prompt 与 output | 任何新任务开始前 |
| 知识更新层 | `prompts/29_update_knowledge_assets.md`、`outputs/knowledge_update_workflow.md` | 新增知识、资料、提示词、算法和案例经验回灌 | 新增材料或经验后 |
| 数据口径层 | `outputs/data_cleaning_standards.md`、`outputs/data_understanding_workflow.md` | 统一字段、单位、缺失异常、参数来源和 P0 数据风险 | 有数据、附件、字段或参数时 |
| 模型算法层 | `outputs/method_matching.md`、`outputs/algorithm_templates.md` | 题型—模型—算法—风险匹配 | 审题选模和代码生成前 |
| 写作表达层 | `outputs/writing_templates.md`、`outputs/result_analysis_templates.md` | 论文结构、摘要、结果解释和结论表达 | 写作、改稿、摘要优化时 |
| 图表表格层 | `outputs/figure_templates.md`、`outputs/table_templates.md`、`outputs/table_result_alignment_workflow.md` | 图示结构、表格字段和结果一致性 | 论文成稿和答辩前 |
| 验收提交层 | `outputs/final_quality_gate.md`、`outputs/reproducibility_checklist.md`、`tools/quality_gate/final_gate_runner.py` | P0 阻断项、复现检查、一键终检、提交放行 | 提交、答辩或宣称完成前（`final_quality_gate_workflow.md` 已归档 v4.8） |

---

## 四、核心资产主表

| 资产路径 | 资产类型 | 服务对象 | 适用题型 | 输入要求 | 输出结果 | 优先调用阶段 | 上游依赖 | 下游去向 | 维护状态 |
|---|---|---|---|---|---|---|---|---|---|
| `AGENTS.md` | output | 全流程 | 全题型 | 用户任务 | 系统工作规则 | 全程 | 无 | 全部 prompt 与 outputs | 已稳定 |
| `README.md` | output | 入门/协同 | 全题型 | 当前仓库 | 系统说明 | 启动时 | 无 | `.claude/skills/paper-workflow-orchestrator/SKILL.md`（原 `prompts/00_route_task.md` 已归档） | 已稳定 |
| `outputs/production_specs.md` | output | 全流程 | 全题型 | 当前仓库 | 运行规范 | 启动时 | `AGENTS.md` | `outputs/task_router.md` | 已稳定 |
| `outputs/file_map.md` | output | 扫描/归档 | 全题型 | 目录与材料 | 文件地图 | 系统建设 | `prompts/01_full_scan.md` | `prompts/02_extract_cards.md` | 已稳定 |
| `outputs/asset_registry.md` | output | 调度/检索 | 全题型 | 核心资产清单 | 统一资产索引 | 启动时 | `README.md`、`outputs/production_specs.md` | `outputs/task_router.md` | 已稳定 |
| `outputs/task_router.md` | output | 调度/分流 | 全题型 | 任务目标、输入材料 | 路由建议与调用顺序 | 任何新任务 | `outputs/asset_registry.md` | 对应 prompt 与 outputs | 已稳定 |
| `outputs/knowledge_update_workflow.md` | output | 系统建设/回灌/调度 | 全题型 | 新增知识点、资料、提示词或案例经验 | 知识更新路径、母库落点、同步清单 | 新增知识后 | `prompts/29_update_knowledge_assets.md` | `outputs/task_router.md`、`outputs/asset_registry.md` | 已稳定 |
| `outputs/knowledge_base.md` | output | 系统建设/复盘 | 全题型 | 扫描与抽卡结果 | 通用知识卡母库 | 建库期 | `prompts/02_extract_cards.md` | `prompts/03_build_rules.md` | 已稳定 |
| `outputs/method_matching.md` | output | 审题/建模 | 评价/预测/优化/机理/分类/图论/仿真 | 题面与约束 | 方法匹配规则 | 选模前 | `outputs/problem_type_taxonomy.md` | `prompts/12_select_model_route.md` | 已稳定 |
| `outputs/algorithm_templates.md` | output | 建模/代码 | 评价/预测/优化/机理/分类/图论/仿真 | 模型路线 | 算法与代码模板 | 选模后 | `outputs/method_matching.md` | `prompts/19_generate_code.md` | 已稳定 |
| `outputs/writing_templates.md` | output | 写作 | 全题型 | 题面、模型、结果 | 论文段落模板 | 写作期 | `outputs/knowledge_base.md` | `prompts/15_rewrite_abstract.md` 等 | 已稳定 |
| `outputs/figure_templates.md` | output | 图示/答辩 | 全题型 | 模型流程、变量关系、结果 | 图示模板 | 写作后期 | `outputs/visual_knowledge_base.md` | `prompts/20_generate_figures.md` | 已稳定 |
| `outputs/scoring_rubric.md` | output | 审稿/评分/答辩 | 全题型 | 题面、论文、模型、答辩材料 | 唯一评分量表与统一打分口径 | 审稿/冲刺/答辩 | `prompts/03_build_rules.md` | `prompts/08_review_math_modeling_paper.md`、`outputs/review_priority_matrix.md` | 已稳定 |
| `outputs/review_priority_matrix.md` | output | 审稿 | 全题型 | 初稿/修改稿 | 问题优先级排序 | 冲刺期 | `outputs/scoring_rubric.md` | `prompts/08_review_math_modeling_paper.md` | 已稳定 |
| `outputs/defense_qa_bank.md` | output | 答辩 | 全题型 | 论文、模型、结果 | 高频问答 | 答辩期 | `outputs/scoring_rubric.md` | `prompts/09_defense_math_modeling.md` | 已稳定 |
| `outputs/reproducibility_checklist.md` | output | 复现/提交 | 全题型 | 代码、数据、结果文件 | 复现核对清单 | 提交前 | `deliverables/code/` | `prompts/21_generate_submission_pack.md` | 已稳定 |
| `outputs/case_feedback_loop.md` | output | 回灌/迭代 | 全题型 | 已完成案例 | 回灌协议 | 收尾阶段 | `deliverables/`、审稿结果 | `prompts/22_case_feedback_loop.md` | 已稳定 |
| `outputs/material_inventory.md` | output | 扫描/归档 | 全题型 | 当前资料目录 | 可回灌材料总清单 | 建库期/新增资料后 | 全量文件系统扫描 | `outputs/_reports/`（提取/OCR 报告）、`outputs/extracted_material_synthesis.md`（原 extracted_* 目录已不存在） | 已稳定 |
| ~~`outputs/extracted_document_text/`~~ | output | 系统建设/检索 | 全题型 | ~~DOCX/部分PDF原文~~ | ~~可全文检索的抽取文本~~ | **目录已不存在（勿再引用；提取报告在 `outputs/_reports/`）** | `outputs/material_inventory.md` | — | 已移除 |
| ~~`outputs/extracted_pdf_text/`~~ | output | 系统建设/检索/论文校准 | 全题型 | ~~获奖/优秀论文PDF~~ | ~~可检索论文文本~~ | **目录已不存在（勿再引用）** | `outputs/_reports/award_pdf_extraction_report.md`、`outputs/_reports/award_pdf_ocr_report.md` | — | 已移除 |
| `outputs/_reports/award_pdf_extraction_report.md` | output | 扫描/验收 | 全题型 | 获奖/优秀论文PDF | PDF文本提取报告 | 建库期/抽取后 | PDF批量提取 | `outputs/extracted_pdf_text/`、`outputs/award_pdf_ocr_needed.csv` | 已稳定 |
| `outputs/_reports/award_pdf_ocr_report.md` | output | 扫描/验收 | 全题型 | 扫描件PDF | OCR处理报告 | 建库期/OCR后 | `outputs/award_pdf_ocr_needed.csv` | `outputs/extracted_pdf_text/`、抽取质量复核 | 已稳定 |
| `outputs/code_asset_index.md` | output | 代码/建模 | 评价/预测/优化/机理/分类/图论/仿真 | Python/Matlab 文件 | 按题型归类的代码资产索引 | 生成代码前 | 代码模板目录 | `outputs/code_template_playbook.md`、`prompts/19_generate_code.md` | 已稳定 |
| `outputs/extracted_material_synthesis.md` | output | 系统建设/回灌 | 全题型 | 抽取文本与代码索引 | 新增材料归档与回灌规则 | 建库期/更新规则前 | `outputs/_reports/`（原 `extracted_document_text/`、`extracted_pdf_text/` 目录已不存在）、`outputs/code_asset_index.md` | `outputs/knowledge_base.md`、`outputs/method_matching.md`、`outputs/scoring_rubric.md` | 已稳定 |
| `outputs/prompt_master_pack.md` | output | 提示词调度/全流程 | 全题型 | 阶段目标、题面、数据、论文或结果 | 可复制的AI提示词总母版 | 赛中/训练/快速调用 | 提示词原始资料整合 | `prompts/25_prompt_master_pack.md` | 已稳定 |
| `outputs/data_understanding_workflow.md` | output | 数据/预处理/建模交接 | 全题型 | 题面附件、字段、原始数据 | 字段映射、质量诊断、输入输出表 | 数据理解期 | `outputs/data_cleaning_standards.md` | `prompts/30_data_understanding.md`、`prompts/26_generate_tables.md` | 已稳定 |
| `outputs/data_cleaning_standards.md` | output | 数据/预处理/复现 | 全题型 | 原始数据、字段说明、参数来源 | 清洗口径、异常缺失处理、P0数据风险 | 数据理解期 | `outputs/data_understanding_workflow.md` | `prompts/30_data_understanding.md`、代码与论文数据说明 | 已稳定 |
| `outputs/table_result_alignment_workflow.md` | output | 表格/结果对表/复现 | 全题型 | 参数、结果、代码输出、论文草稿 | 表格方案与关键数字一致性核对 | 写作/冲刺 | `outputs/table_templates.md`、`outputs/reproducibility_checklist.md` | `prompts/26_generate_tables.md`、`prompts/28_final_quality_gate.md` | 已稳定 |
| `outputs/slide_defense_workflow.md` | output | PPT/答辩 | 全题型 | 论文、图表、核心结果 | PPT页面结构、讲述稿、追问准备 | 答辩前 | `outputs/defense_qa_bank.md` | `prompts/27_generate_slides.md`、`prompts/18_defense_followup_drill.md` | 已稳定 |
| ~~`outputs/final_quality_gate_workflow.md`~~ | output | 终检/提交放行 | 全题型 | ~~论文、代码、图表、表格、PPT、AI说明~~ | ~~可提交/可答辩/可复现判定~~ | **v4.8 已归档（内容被 `final_quality_gate.md` 覆盖，勿再引用）** | — | — | 已归档 |
| `outputs/final_quality_gate.md` | output | 终检/提交放行 | 全题型 | 论文、代码、图表、表格、PPT、AI说明 | P0阻断项、终检清单、放行口径 | 最终提交前 | `outputs/scoring_rubric.md` | `prompts/_archive/28_final_quality_gate.md`、`deliverables/00_提交包总览与终检清单.md` | 已稳定 |
| `prompts/00_route_task.md` | prompt | 调度/分流 | 全题型 | 用户任务 | 调用路径 | 任何新任务 | `outputs/task_router.md` | 全部 prompt | 已稳定 |
| `prompts/01_full_scan.md` | prompt | 系统建设 | 全题型 | 一批资料 | 文件地图与优先级 | 建库期 | `README.md`、`outputs/file_map.md` | `prompts/02_extract_cards.md` | 已稳定 |
| `prompts/02_extract_cards.md` | prompt | 系统建设 | 全题型 | 已扫描资料 | 知识卡片 | 建库期 | `outputs/file_map.md` | `prompts/03_build_rules.md` | 已稳定 |
| `prompts/03_build_rules.md` | prompt | 系统建设 | 全题型 | 知识卡片与旧规则 | 统一规则库 | 建库期 | `outputs/knowledge_base.md` | 各专项 outputs | 已稳定 |
| `prompts/11_identify_problem_type.md` | prompt | 审题 | 全题型 | 题面 | 题型判断 | 开题 | `outputs/problem_type_taxonomy.md` | `prompts/12_select_model_route.md` | 已稳定 |
| `prompts/12_select_model_route.md` | prompt | 建模 | 全题型 | 题型、约束、数据 | 主路线与备选路线 | 开题/建模 | `outputs/method_matching.md` | 写作/代码/图示 | 已稳定 |
| `prompts/19_generate_code.md` | prompt | 代码 | 预测/优化/仿真/分类/评价 | 模型路线、数据结构 | 可运行代码或可替换骨架 | 写作后/生产验证期 | `outputs/algorithm_templates.md` | `deliverables/code/` | 已稳定 |
| `prompts/20_generate_figures.md` | prompt | 图示 | 全题型 | 逻辑结构或结果 | 图示方案与草图 | 写作后 | `outputs/figure_templates.md` | `deliverables/figures/` | 已稳定 |
| `prompts/21_generate_submission_pack.md` | prompt | 提交 | 全题型 | 论文、代码、图示、表格 | 提交包清单 | 冲刺期 | `outputs/reproducibility_checklist.md` | `deliverables/` | 已稳定 |
| `prompts/22_case_feedback_loop.md` | prompt | 回灌/复盘 | 全题型 | 已完成案例及问题 | 规则回灌清单 | 收尾阶段 | `outputs/case_feedback_loop.md` | 相关 outputs 更新 | 已稳定 |
| `prompts/23_start_new_case.md` | prompt | 单题开工/分流 | 全题型 | 新题题面、附件说明、模糊目标 | 单题最小工作包与执行顺序 | 开题 | `outputs/task_router.md`、`outputs/production_specs.md` | 审题/选模/写作/代码/图示 | 已稳定 |
| `prompts/24_dynamic_acceptance.md` | prompt | 动态验收 | 全题型 | deliverables、代码、结果文件 | 真实性判定与最小补齐项 | 冲刺/验收 | `outputs/reproducibility_checklist.md`、`outputs/revision_checklist.md` | 提交包/案例回灌 | 已稳定 |
| `prompts/25_prompt_master_pack.md` | prompt | 提示词调度 | 全题型 | 当前阶段、题面、数据、草稿或结果 | 当前阶段最该复制的AI提示词 | 任何阶段卡住时 | `outputs/prompt_master_pack.md` | 对应专项 prompt 或外部AI调用 | 已稳定 |
| `prompts/30_data_understanding.md` | prompt | 数据/预处理 | 全题型 | 题面附件、字段说明、原始数据 | 数据理解与预处理工作包 | 数据理解期 | `outputs/data_understanding_workflow.md` | 选模/表格/代码 | 已稳定 |
| `prompts/26_generate_tables.md` | prompt | 表格/结果对表 | 全题型 | 参数、结果、代码输出、论文草稿 | 表格方案和关键数字对表 | 写作/冲刺 | `outputs/table_result_alignment_workflow.md` | 论文/答辩/终检 | 已稳定 |
| `prompts/27_generate_slides.md` | prompt | PPT/答辩 | 全题型 | 论文、图表、结果、答辩目标 | PPT页面方案与讲述稿 | 答辩前 | `outputs/slide_defense_workflow.md` | `deliverables/slides/`、答辩追问 | 已稳定 |
| `prompts/28_final_quality_gate.md` | prompt | 终检/提交放行 | 全题型 | 论文、代码、图表、表格、PPT、AI说明 | 最终质量门判定 | 提交前 | `outputs/final_quality_gate_workflow.md` | 提交包/动态验收/回灌 | 已稳定 |
| `prompts/29_update_knowledge_assets.md` | prompt | 系统建设/回灌/同步 | 全题型 | 新增知识点、资料、提示词、算法或案例经验 | 分类、抽取、回灌、同步、登记和待确认清单 | 新增知识后 | `outputs/knowledge_update_workflow.md` | 各专项 outputs、deliverables | 已稳定 |
| `deliverables/papers/` | deliverable | 写作 | 全题型 | 论文骨架、结果、图表 | 正文与摘要成品 | 写作/冲刺 | `outputs/writing_templates.md` | 提交包 | 已稳定 |
| `deliverables/code/` | deliverable | 生产验证/提交 | 全题型 | 模型路线、参数、数据 | 求解代码、演示输出与说明 | 建模/提交 | `outputs/algorithm_templates.md` | 提交包 | 已稳定 |
| `deliverables/figures/` | deliverable | 写作/答辩 | 全题型 | 模型逻辑、关键结果 | 图示与草图 | 写作/答辩 | `outputs/figure_templates.md` | 论文/PPT | 已稳定 |
| `deliverables/tables/` | deliverable | 写作/提交 | 全题型 | 参数、结果、检验 | 关键表格 | 写作/提交 | `outputs/result_analysis_templates.md` | 论文/答辩 | 已稳定 |
| `deliverables/slides/` | deliverable | 答辩/提交 | 全题型 | 论文、图表、结论 | 答辩材料 | 答辩前 | `outputs/defense_qa_bank.md` | 提交包 | 已稳定 |

---

## 五、最小维护规则

1. 新增核心文件时，优先补登记到本表。
2. 若某文件已废弃或被替代，要在维护状态中标注，不要静默失效。
3. 若某个案例产出带来了可复用新套路，优先更新本表中的上游依赖和下游去向。
4. 若多个文件功能重叠，应在本表中明确“谁是主入口，谁是补充库”。

---

## 六、当前升级结论

当前项目已经不缺“资料”和“规则文件”，最需要的是：

1. 用本索引表把核心资产统一登记。
2. 用 `outputs/task_router.md` 把任务先分流再执行。
3. 用 `outputs/prompts_outputs_call_map.md` 把 prompt 与 output 固定配对。
4. 用 `outputs/knowledge_update_workflow.md` 保证新增知识不会停留在聊天记录或临时文件。
5. 用 `outputs/data_cleaning_standards.md` 和 `outputs/final_quality_gate.md` 控住真实数据、真实结果和提交放行。
6. 用 `outputs/case_feedback_loop.md` 把个案经验持续回灌。
