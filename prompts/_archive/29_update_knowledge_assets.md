# 29_update_knowledge_assets.md

> 用于把用户新增的知识点、资料、提示词、案例经验、算法规则或高分表达，统一回灌到 `outputs/`、`prompts/`、`deliverables/`，避免知识只停留在聊天记录或零散文件里。

> **接口契约**
> - 前置依赖：新知识/经验（来自 22_case_feedback_loop 的回灌材料，或用户新增的知识点）
> - 后续触发：outputs/ 更新（知识图谱、规则库、模板库等文件的增量更新）
> - 输出：知识资产更新（更新后的 outputs/ 文件、新增规则条目、模板改进记录）

---

## 一、使用场景

当用户说：
- “我新增了知识点”
- “把这些资料吸收进去”
- “更新知识库”
- “全部榨干”
- “同步到 outputs 和 prompts”
- “这些规则以后也要用”
- “把这个经验沉淀下来”

优先调用本 prompt。

---

## 二、开始前必须读取

1. `outputs/task_router.md`
2. `outputs/asset_registry.md`
3. `outputs/prompts_outputs_call_map.md`
4. `outputs/knowledge_update_workflow.md`
5. `outputs/data_cleaning_standards.md`（若涉及数据、字段、附件或参数）
6. `outputs/final_quality_gate.md`（若涉及提交、答辩或可复现判断）
7. `outputs/material_inventory.md`（若新增的是资料）
8. `outputs/extracted_material_synthesis.md`（若已有抽取结果）
9. `outputs/knowledge_base.md`
10. `outputs/method_matching.md`
11. `outputs/scoring_rubric.md`
12. `outputs/writing_templates.md`
13. `outputs/case_feedback_loop.md`
14. `AGENTS.md`
15. `README.md`
16. `README_structure.md`

若新增内容涉及子系统同步（注：`math-model-producer/` 已于 2026-07-25 归档至 `resources/_archive/math-model-producer_old/`，其能力早已合并到根目录统一体系，无需再同步子系统）。

---

## 三、先判断新增知识类型

把新增内容至少归入下面一类，允许多选：

| 类型 | 判定信号 | 优先更新位置 |
|---|---|---|
| 原始资料 | PDF、DOCX、PPT、代码包、模板包、优秀论文 | `material_inventory`、`extracted_*`、`code_asset_index` |
| 通用规则 | 审题、建模、评分、避坑、流程经验 | `knowledge_base`、`scoring_rubric`、`bad_cases` |
| 方法模型 | 题型、算法、模型适用边界、误用提醒 | `method_matching`、`algorithm_templates`、`model_*` |
| 写作表达 | 摘要、结果分析、结论、过渡句、高分句式 | `writing_templates`、`result_analysis_templates`、`high_score_expression_library` |
| 检验稳健 | 误差、灵敏度、鲁棒性、复现、可信度 | `validation_checklist`、`model_validation_by_type`、`reproducibility_checklist` |
| 图示表格 | 技术路线图、流程图、结果图、参数表、对表 | `figure_templates`、`table_templates`、`visual_knowledge_base` |
| 代码模板 | Python/Matlab、预处理、求解、可视化、仿真 | `code_asset_index`、`code_template_playbook`、`algorithm_templates` |
| 提示词 | AI 提示词、比赛当天话术、阶段提示词 | `prompt_master_pack`、`prompts_outputs_call_map` |
| 答辩经验 | 高频问答、追问链、现场短答 | `defense_qa_bank`、`defense_followup_chains`、`defense_short_answers` |
| 案例回灌 | 某一题做完后的经验、失误、评审反馈 | `case_feedback_loop` 和相关母库 |
| 系统流程 | 路由、验收、提交、目录、子系统同步规则 | `task_router`、`asset_registry`、`README`、`AGENTS` |

---

## 四、固定更新顺序

### 1. 原始资料先入库

如果新增的是资料文件，不要直接写进规则库。先更新：
1. `outputs/material_inventory.md`
2. `outputs/extracted_document_text/` 或 `outputs/extracted_pdf_text/`
3. `outputs/_reports/award_pdf_extraction_report.md` 或 `outputs/_reports/award_pdf_ocr_report.md`（PDF 场景）
4. `outputs/code_asset_index.md`（代码场景）
5. `outputs/extracted_material_synthesis.md`

再从抽取结果回灌母库。

### 2. 规则进入母库

根据知识类型更新：
- `outputs/knowledge_base.md`
- `outputs/method_matching.md`
- `outputs/scoring_rubric.md`
- `outputs/writing_templates.md`
- `outputs/bad_cases.md`
- `outputs/common_failure_patterns.md`
- `outputs/algorithm_templates.md`
- `outputs/code_template_playbook.md`
- `outputs/figure_templates.md`
- `outputs/table_templates.md`
- `outputs/defense_qa_bank.md`

### 3. 调度入口同步

如果新增知识会影响“以后该怎么调用”，同步更新：
1. `outputs/task_router.md`
2. `outputs/prompts_outputs_call_map.md`
3. `outputs/asset_registry.md`
4. 对应 `prompts/*.md`

### 4. 成品区同步

如果新增知识能转成可交付模板或提交清单，同步更新：
- `deliverables/00_系统自测清单.md`
- `deliverables/00_提交包总览与终检清单.md`
- `deliverables/papers/`
- `deliverables/code/`
- `deliverables/figures/`
- `deliverables/tables/`
- `deliverables/slides/`
- `deliverables/math_modeling_knowledge_base_share/`

### 5. 子系统同步（已废弃）

> `math-model-producer/` 已于 2026-07-25 归档至 `resources/_archive/math-model-producer_old/`。根目录 `outputs/` 即唯一系统，新增通用知识直接回灌到上文 1-4 项对应的根目录文件即可，无需子系统同步。

---

## 五、输出格式

每次执行本 prompt，输出：

```markdown
## 1. 新增知识分类
- 类型：
- 来源：
- 是否需要 OCR / 抽取 / 代码索引：
- 是否需要同步子系统：

## 2. 已更新文件
| 文件 | 更新内容 | 原因 |
|---|---|---|

## 3. 母库回灌结果
- 审题/题型：
- 方法/算法：
- 写作/表达：
- 检验/稳健：
- 图示/表格：
- 代码/复现：
- 答辩/追问：
- 避坑/反例：

## 4. 仍需人工确认
- 真实数据：
- 真实结果：
- 代码运行：
- PDF/OCR质量：
- 是否适合泛化：

## 5. 下一次调用建议
- 最该继续更新：
- 最该优先使用的 prompt：
- 最该优先读取的 output：
```

---

## 六、硬性禁忌

1. 不要只把新增知识放进 README，却不回灌母库。
2. 不要只更新 prompts，不更新对应 outputs。
3. 不要把未读 PDF、未 OCR 扫描件、只看文件名的资料当作已吸收。
4. 不要把单个案例经验无条件泛化成全题型规则。
5. 不要把 demo 输出、占位结果、示例数据写成真实结论。
6. 不要新增核心资产后忘记登记 `outputs/asset_registry.md`。
7. `math-model-producer/` 已归档（2026-07-25），根目录 `outputs/` 即唯一系统，无需双系统同步。

---

## 七、一句话原则

新增知识点不是“多存一个文件”，而是要完成：

**分类 → 抽取 → 回灌母库 → 同步路由 → 登记资产 → 更新成品模板 → 子系统同步 → 留下待确认项**。

执行后必须能接回系统主链路：

**任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌**。
