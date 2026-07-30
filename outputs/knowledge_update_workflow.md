# outputs/knowledge_update_workflow.md

> **v2.0 标准化 | 2026-05-31** | 统一索引见 `outputs/INDEX.md`

> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> 用于规定“新增知识点”进入本数学建模生产系统后的固定更新路径，保证知识不会散落在聊天记录、临时文件或单个案例目录里。

---

## 一、目标

新增知识点必须被转化为以下至少一种系统资产：

1. 可检索资料
2. 可复用知识卡片
3. 可调用建模规则
4. 可复制提示词
5. 可运行代码模板
6. 可套用写作表达
7. 可用于答辩的问答口径
8. 可交付的成品模板
9. 可回灌的案例经验
10. 可路由的系统入口

如果一个新增知识点没有进入任何资产，它就不算真正被系统吸收。

---

## 二、知识更新总链路

固定链路：

```text
新增知识
→ 类型判断
→ 原始资料入库 / 直接规则归类
→ 抽取文本或代码索引
→ 形成回灌清单
→ 更新专项母库
→ 更新路由与调用关系
→ 更新资产登记
→ 更新 deliverables 模板或清单
→ 同步 math-model-producer
→ 留下待确认项
```

---

## 三、按知识类型更新到哪里

| 新增知识类型 | 第一落点 | 母库落点 | 调度落点 | 成品落点 |
|---|---|---|---|---|
| PDF/DOCX/讲义/论文 | `material_inventory`、`extracted_*` | `extracted_material_synthesis` | `asset_registry` | 分享包或参考清单 |
| 代码资料 | `code_asset_index` | `code_template_playbook`、`algorithm_templates` | `prompts/19_generate_code.md` | `deliverables/code/` |
| 审题规则 | `knowledge_base` | `problem_type_taxonomy`、`method_matching` | `task_router` | 新题开工包 |
| 方法模型 | `method_matching` | `algorithm_templates`、`model_validation_by_type` | `prompts/12_select_model_route.md` | 代码/图示/论文模板 |
| 写作表达 | `writing_templates` | `result_analysis_templates`、`high_score_expression_library` | `prompts/15_rewrite_abstract.md` | 论文模板 |
| 检验规则 | `validation_checklist` | `sensitivity_and_robustness_templates`、`reproducibility_checklist` | `prompts/14_strengthen_validation.md` | 终检清单 |
| 图表结构 | `visual_knowledge_base` | `figure_templates`、`table_templates` | `prompts/20_generate_figures.md`、`prompts/26_generate_tables.md` | figures/tables |
| 答辩口径 | `defense_qa_bank` | `defense_short_answers`、`defense_followup_chains` | `prompts/09_defense_math_modeling.md` | slides/答辩材料 |
| 提示词 | `prompt_master_pack` | `prompts_outputs_call_map` | `prompts/25_prompt_master_pack.md` | 分享包 |
| 案例经验 | `case_feedback_loop` | 与案例相关母库 | `prompts/22_case_feedback_loop.md` | 提交包/复盘清单 |
| 系统规则 | `AGENTS.md` | `production_specs`、`task_router` | `00_route_task` | 系统自测清单 |

---

## 四、必须同步的核心文件

### 1. 根系统控制层

- `AGENTS.md`
- `README.md`
- `README_structure.md`

适用情况：新增知识改变了系统默认行为、目录职责、工作流、质量门或子系统同步规则。

### 2. prompts 调用层

- `prompts/00_route_task.md`
- `prompts/01_full_scan.md`
- `prompts/02_extract_cards.md`
- `prompts/03_build_rules.md`
- `prompts/22_case_feedback_loop.md`
- `prompts/25_prompt_master_pack.md`
- `prompts/29_update_knowledge_assets.md`

适用情况：新增知识改变了“该怎么发起任务、抽卡、建库、回灌、调提示词”。

### 3. outputs 规则层

- `outputs/knowledge_update_workflow.md`
- `outputs/task_router.md`
- `outputs/asset_registry.md`
- `outputs/prompts_outputs_call_map.md`
- `outputs/material_inventory.md`
- `outputs/extracted_material_synthesis.md`
- `outputs/knowledge_base.md`
- `outputs/method_matching.md`
- `outputs/scoring_rubric.md`
- `outputs/writing_templates.md`
- `outputs/algorithm_templates.md`
- `outputs/code_template_playbook.md`
- `outputs/figure_templates.md`
- `outputs/table_templates.md`
- `outputs/defense_qa_bank.md`
- `outputs/case_feedback_loop.md`

适用情况：新增知识需要沉淀为可复用规则、模板或调用索引。

### 4. deliverables 成品层

- `deliverables/00_系统自测清单.md`
- `deliverables/00_提交包总览与终检清单.md`
- `deliverables/math_modeling_knowledge_base_share/`
- `deliverables/papers/`
- `deliverables/code/`
- `deliverables/figures/`
- `deliverables/tables/`
- `deliverables/slides/`

适用情况：新增知识能直接变成论文、代码、图表、表格、PPT、分享包或提交包模板。

### 5. 子系统层（已归档）

> `math-model-producer/` 已于 2026-07-25 整体归档至 `resources/_archive/math-model-producer_old/`。其 prompts/ 和 outputs/ 早已合并到根目录统一体系，不再作为独立回灌目标。新增通用知识直接写入根目录 `outputs/` 与 `prompts/`。

---

## 五、更新后的验收标准

一次知识更新完成，至少要满足：

1. 已判断新增知识类型。
2. 若是资料，已进入可检索文本层或代码索引。
3. 已更新至少一个专项母库。
4. 若影响调用方式，已更新 `task_router` 或 `prompts_outputs_call_map`。
5. 若形成核心资产，已更新 `asset_registry`。
6. 若可形成成品模板，已更新 `deliverables`。
7. 若具备通用价值，已同步 `math-model-producer`。
8. 已标注不能确认的真实数据、真实结果、OCR 质量或代码运行状态。

---

## 六、最小更新包

如果时间很紧，只做最小包：

1. `outputs/knowledge_base.md`
2. `outputs/method_matching.md` 或 `outputs/writing_templates.md` 或 `outputs/scoring_rubric.md`
3. `outputs/task_router.md`
4. `outputs/asset_registry.md`
5. `outputs/knowledge_update_workflow.md`

如果新增的是提示词，再加：

1. `outputs/prompt_master_pack.md`
2. `prompts/25_prompt_master_pack.md`
3. `outputs/prompts_outputs_call_map.md`

如果新增的是通用资料，再加：

1. `outputs/material_inventory.md`
2. `outputs/extracted_document_text/` 或 `outputs/extracted_pdf_text/`
3. `outputs/extracted_material_synthesis.md`

---

## 七、禁止事项

1. 禁止把“知识更新”只写进 README。
2. 禁止只更新 prompt，不更新 output 支撑库。
3. 禁止新增核心文件后不登记资产。
4. 禁止把未验证的案例经验泛化成全局规则。
5. 禁止把未运行代码、占位数据或 demo 结果写成真实结论。
6. `math-model-producer/` 已归档（2026-07-25），根目录 `outputs/` 即唯一系统，无需双系统同步。

---

## 八、一句话口径

新增知识点的最终目标是让系统下次能自动调用它，而不是让它只存在于某个聊天回合里。
