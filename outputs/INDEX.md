# outputs/INDEX.md — 数学建模生产系统统一索引

> **最后更新：2026-07-23（v4.3）**
> **系统全演进**：`paper_output/research/CHANGELOG.md`（v4.0→v4.3 四轮融合一览）
> **用途：** 本文件是整个 `outputs/` 的唯一入口索引。所有任务执行前，先在此表查到对应文件，再深入调用。
> **调用顺序：** `INDEX.md（定位文件）→ task_router.md（分流任务）→ 对应 prompt + output（执行）→ asset_registry.md（登记）`
> **v3.4 统一入口**：同一意图 → 默认最深输出。详见下方"统一入口 Skill → outputs 映射"。

---

## 一、目录总览

当前 `outputs/` 按 **8 大功能域** 组织，共 74 个文件 + 1 个子目录（`scripts/`）：

| 功能域 | 文件数 | 核心入口 | 服务阶段 |
|--------|--------|----------|----------|
| 🏗️ 系统调度 | 12 | `task_router.md` | 全流程 |
| 🧩 建模选模 | 13 | `method_matching.md` | 审题/建模 |
| ✍️ 写作表达 | 13 | `writing_templates.md` | 写作/改稿 |
| 🔍 审稿评分 | 12 | `scoring_rubric.md` | 审稿/冲刺 |
| 🎤 答辩准备 | 7 | `defense_qa_bank.md` | 答辩 |
| 📊 数据处理 | 3 | `data_cleaning_standards.md` | 数据理解 |
| ✅ 质量验收 | 5 | `final_quality_gate.md` | 提交前 |
| 🎨 图表可视 | 4 | `figure_templates.md` | 写作/答辩 |
| 📦 提示词调度 | 1 | `prompt_master_pack.md` | 赛中 |
| 🏆 赛中流程 | 1 | `competition_checklist.md` | 赛中72h |
| 📚 提取文本 | 6 文件 + 2 目录 | `extracted_material_synthesis.md` | 建库/检索 |
| 🏆 竞赛差异 | 1 | `competition_specific.md` | 各赛事格式/评分 |

---

## 一·bis、统一入口 Skill → outputs 映射（v3.4）

> **核心原则：同一意图 → 默认最深输出。** 用户说"审论文""打分""严格打分"均走同一入口，拿到相同全量报告。

| 统一入口 Skill | 默认输出 | 依赖的 outputs 文件 |
|---------------|---------|-------------------|
| `/review` → `paper-reviewer` agent | 9 部分全量深度报告（+§9 题型加权 +§10 Per-Qi）| `scoring_rubric.md` `method_matching.md` `validation_checklist.md` `reproducibility_checklist.md` **`dim_weights.json`**（v4.1）**`empirical.json`**（v2.0 by_topic）|
| `/defense` | 5 阶段全量答辩包 | `defense_qa_bank.md` `defense_followup_chains.md` `defense_short_answers.md` `defense_opening_and_closing.md` |
| `/analyze` | 5 阶段全量审题选模报告 | `method_matching.md` `algorithm_templates.md` `problem_type_taxonomy.md` `model_selection_flow.md` `model_selection_quick_table.md` |
| `/figure` | 自动判断→分派子skill→全部图表 | `figure_templates.md` `visualization_strategy_library.md` `chart_explanation_templates.md` |
| `paper-polisher` | 12 点检查+改写+评分 | `scoring_rubric.md` `bad_expression_blacklist.md` `high_score_expression_library.md` |
| `/code` | 从零生成代码 | `method_matching.md` `algorithm_templates.md` `code_template_playbook.md` |
| `/algorithm-runner` | 执行已有算法模板 | `code_asset_index.md` |
| `/submit` | 最终比赛提交包 | `final_quality_gate.md` `competition_checklist.md` |
| AIGC 降重 | 默认 `humanizer-zh-academic`；备选 `aigc-reduce` | — |
| `blind-panel`（v4.1） | 3 座独立盲评 + 20 分冲突 + 真实稀缺性校准 | `scoring_rubric.md` `empirical.json`（by_topic 锚点）|
| 模式切换（v4.1） | fast/standard/championship | — |

**内部调度工具**（由统一入口分派，不直接暴露）：
`diagram-maker` / `chart-recommender` / `math-figure` / `network-graph` / `interactive-chart` → `/figure`
`defense-simulator` → `/defense`
`model-selector` → `/analyze`
`paper-rewriter` → `paper-polisher`

---

## 一·septimo、工具链增强（v4.3 新增）

> 来源：camelot(3716★) + Pix2Text(3195★) + SciencePlots(~5k★) + aigc-deslop(18★) + Optuna(14549★) + SHAP/shapash(3247★) + akshare(~10k★)。完整报告：`paper_output/research/github_fusion_v4.3_report.md`。

### 新增脚本（7 个，单点工具，按需调用）

| 脚本 | 所属 skill | 用途（已验证） |
|------|-----------|------|
| `extract_pdf_tables.py` | data-cleaning-and-visualization | Camelot PDF 表格→CSV/Excel（✓ A题.pdf 真实提取） |
| `extract_formulas_ocr.py` | problem-doc-model-selector | Pix2Text 公式图→LaTeX |
| `journal_style.py` | math-figure | SciencePlots 期刊风（✓ 76 样式出图） |
| `replace_docx_preserve_format.py` | aigc-reduce | Word 格式保留降重（55%→11%） |
| `shap_explain.py` | feature-engineering | SHAP 特征重要性（ML 可解释性） |
| `optuna_tune.py` | model-code-and-result-generator | Optuna TPE 超参调优 |
| `akshare_fetch.py` | authoritative-data-harvester | 宏观/金融/行业数据 |

### 新增文档与已装包

- `docs/math-mcp-servers.md` — 6 个数学 MCP 配置（命令已校准）
- 已装：SciencePlots 2.2.2 / camelot 2.0.0 / shap 0.51 / optuna 4.9 / akshare 1.18.75

---

## 一·sexto、同赛道生态融合（v4.2 新增）

> 来源：`jihe520/MathModelAgent`(2862★) + `RealSeaberry/AutoMCM-Pro`(144★) + `Gostyan/docx-skill-4-cn-paper`(335★) + `Kirito-Elucidator/MathModel-QA-Engine`(10★) + `yushui2022/MathModel-Skill`(217★)。完整报告：`paper_output/research/github_fusion_v4.2_report.md`。

### 新增 Skill（3 个）

| Skill | 用途 | 关键产出 |
|-------|------|---------|
| `typst-renderer` | Typst 论文渲染（与 Word/LaTeX 三选一） | `resources/15_Typst模板/typst_index.json`（17 Typst + 17 LaTeX 集） |
| `docx-editor-cn` | Word 原生公式（temml→docx）+ XML unpack/pack/validate 局部编辑 | `scripts/office/{pack,unpack,validate,soffice}.py` + `convert_paper.js` |
| `award-paper-rag` | O 奖论文章节级 RAG（heading 分块 + 13 类分类器） | `scripts/mmqa/` + `rag_cli.py` |

### 新增脚本（9 个，全部已验证可运行）

| 脚本 | 所属 skill | 用途 |
|------|-----------|------|
| `pipeline_manager.py` | quality-assurance-auditor | GitOps 状态机（AP/Manual + 返工上限 + 并行阶段） |
| `verify_gate.py` | quality-assurance-auditor | G4.6 强制代码自证门 |
| `check_numeric_sanity.py` | quality-assurance-auditor | inf/nan/量级扫描（通用，互补 result_reasonableness） |
| `security_check.py` | consistency-auditor | 密钥/路径/Markdown 注入防护 |
| `precommit_scan.sh` | consistency-auditor | 提交前密钥拦截（git hook / PreToolUse） |
| `verification_template.py` | model-code-and-result-generator | 为每模型生成 verify_*.py 骨架 |
| `freshness_check.py` | context-memory-keeper | SHA-256 报告新鲜度（防旧报告） |
| `parse_hil_action.py` | decision-logger | HIL 6 动作解析 |
| `build_typst_index.py` | typst-renderer | Typst 模板索引构建 |

### 新增门控与机制

- **G4.6 强制代码自证门**：每个模型必配 `paper_output/code/verifications/verify_*.py`，全 PASS 才能引用进论文
- **HIL 6 动作**：confirm/edit/regenerate/ask/skip/abort（扩展 G2.5/G4.5）
- **4 层容错**：L1 重试（auto_detect_and_fix）→ L2 Fallback → L3 Shadow → L4 Feedback（pipeline rework）
- **双 Agent 解耦**：推导轨（plan/derivation_Qn.md）↔ 编码轨（code + verify）并行

---

## 一·ter、同级竞品融合（v4.1 新增）

> 来源：`handsomeZR/mathmodel-skill` v6.1 + `sweetcornna/mathodology`。完整报告：`paper_output/research/tier1_diff_and_port_report.md`。

### 评分与反馈层（审稿评分域 + 质量验收域）

| 文件/能力 | 位置 | 用途 |
|---|---|---|
| 题型差异化加权 | `outputs/dim_weights.json` | competition×task_type×stage×dim 加权 [0.7,1.5]（module_weights_7dim + stage_dim_weights）|
| empirical v2.0 分题型分位 | `outputs/empirical.json` | by_topic A-F 图表/公式分位（升级 v1.0）|
| 4 层反馈机制 | `.claude/skills/quality-assurance-auditor/references/feedback_layer{1-4}_*.md` | L1 Critic+diff精修 / L2 跨阶段回检 / L3 Panel / L4 证据校准 |
| 盲评 Panel | `.claude/agents/blind-panel-judge.md` + `.claude/skills/blind-panel/` | 3 座独立盲评 + 20 分冲突 + 真实稀缺性校准 |
| Per-Qi 加权聚合 | `.claude/agents/paper-reviewer.md` §10 | 多子问题独立评分，只 refine 挂科 Qi |
| figqa 碰撞门 | `.claude/skills/math-figure/scripts/{figqa.py,pdf_qa.sh,make_contact_sheet.py}` | bbox 零碰撞 + 从编译 PDF 建 contact sheet |
| 3 模式 + Friendly Mode | `.claude/skills/paper-workflow-orchestrator/SKILL.md` | fast/standard/championship；问答式 UX |

### 路由接入

| 触发词 | 路由 |
|---|---|
| 盲评/盲审/模拟评委/校准打分/panel | `blind-panel` skill |
| 升级到 championship/切到 fast | orchestrator 模式切换 |
| 做 L2 回检/跨阶段一致性检查 | qa-auditor L2 层 |
| 图表碰撞门/figqa check | `math-figure/scripts/figqa.py` |

## 一·quater、GitHub 融合新增内容（v4.0）

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

### 三审计层（v3.6 新增）

```
论文完成后 → consistency-auditor → completeness-auditor → quality-assurance-auditor
三者全部PASS才能提交论文
```

| 审计层 | Skill | 检查内容 | 产出 |
|--------|-------|---------|------|
| 第一层 | `consistency-auditor` | 数字/文件名/符号一致性 | `qa/consistency_audit_report.json` |
| 第二层 | `completeness-auditor` | 审查文件/报告/产物齐全 | `qa/completeness_audit_report.json` |
| 第三层 | `quality-assurance-auditor` | 工作流完整性+反编造 | `qa/evidence_gate_report.json` |

### 用户决策门禁（v3.6 新增）

| 门禁 | 时机 | 要求 | 检查方式 |
|------|------|------|---------|
| **G2.5** | 方法选择后 | 用户填写选择理由（≥50字） | `decision-logger` 记录 |
| **G4.5** | 结果确认后 | 用户填写确认理由（≥30字） | `decision-logger` 记录 |

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

### 新增 Skill（v3.6 GitHub融合）

| Skill | 职责 | 来源 |
|-------|------|------|
| `consistency-auditor` | 一致性审计（三审计层第一层） | zhnnky329/MathModeling-skills |
| `completeness-auditor` | 完整性审计（三审计层第二层） | zhnnky329/MathModeling-skills |
| `decision-logger` | 决策日志记录 | zhnnky329/MathModeling-skills |
| `feature-engineering` | 特征工程标准化流程 | FinDii/FeatureEngineering |
| `algorithm-benchmark` | 算法基准测试 | szilard/benchm-ml |
| `style-calibration` | 写作风格校准 | Imbad0202/academic-research-skills |
| `citation-tracer` | 引用溯源工具 | Imbad0202/academic-research-skills |
| `ai-failure-checker` | AI失败模式检查（7-mode checklist） | Imbad0202/academic-research-skills |

---

## 二、文件分类速查

### 🏗️ 系统调度层（11 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `task_router.md` | **主路由**：按任务类型分流到对应 prompt+output | 每次新任务开始 |
| `asset_registry.md` | **资产索引**：登记所有核心资产的上下游依赖 | 系统维护/新增资产 |
| `file_map.md` | **文件地图**：全项目文件分类、优先级、重复判断 | 扫描/建库 |
| `prompts_outputs_call_map.md` | **调用对照表**：prompt 与 output 固定配对 | 按阶段查找调用包 |
| `production_specs.md` | **生产规范**：分层、执行顺序、交付标准、禁止项 | 系统启动/交接 |
| `knowledge_update_workflow.md` | **知识更新流程**：新增知识的分类→抽取→回灌路径 | 新增资料/经验后 |
| `knowledge_base.md` | **知识卡片母库**：通用知识卡集中管理 | 建库/检索 |
| `case_feedback_loop.md` | **案例回灌协议**：个案经验如何回流母库 | 案例收尾时 |
| `competition_workflow.md` | **赛中总控流程**：比赛当天72h操作手册 | 赛中 |
| `material_inventory.md` | **材料清单**：所有可回灌材料的总清单 | 资料入库 |
| `deduplication_and_grading_guide.md` | **去重与评分指南** | 审稿/校准 |

### 🧩 建模选模层（13 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `method_matching.md` | **主入口**：题型×模型×算法×风险匹配 | 审题选模前 |
| `algorithm_templates.md` | **算法模板库**：按题型的算法代码模板 | 生成代码前 |
| `model_selection_flow.md` | **选模流程**：题型→主模型→备选→检验 | 审题/建模 |
| `model_selection_quick_table.md` | **选模速查表**：一页式压缩速查 | 快速决策 |
| `problem_type_taxonomy.md` | **题型分类**：7大题型识别与误判风险 | 审题 |
| `model_validation_by_type.md` | **分题型最小检验包**：每类模型最少检验项 | 补检验 |
| `model_chain_blueprints.md` | **模型链蓝图**：组合模型的标准架构 | 组合建模 |
| `case_to_method_route_library.md` | **题型→路线库**：历史案例的建模路线 | 选模参考 |
| `code_template_playbook.md` | **代码模板说明书**：代码结构、参数、复用说明 | 生成代码 |
| `code_asset_index.md` | **代码资产索引**：按题型归类的代码索引 | 查找代码 |
| `python_algorithm_template_standard.md` | **Python 算法模板标准** | 代码规范 |
| `algorithm_selection_red_flags.md` | **算法选型红旗**：什么时候不该用某个算法 | 选模时 |
| `method_misuse_alerts.md` | **方法误用预警**：常见误用场景 | 建模/复盘 |

### ✍️ 写作表达层（13 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `writing_templates.md` | **主入口**：论文各段落填空式模板 | 写论文 |
| `section_writing_templates.md` | **分节写作模板**：按章节快速套用 | 写论文 |
| `abstract_templates.md` | **摘要模板**：三段式高分摘要模板 | 写摘要 |
| `abstract_micro_templates.md` | **摘要微模板**：更短更快的摘要速写 | 快速摘要 |
| `result_analysis_templates.md` | **结果分析模板**：报数→解释→落地的升级模板 | 写结果分析 |
| `result_interpretation_templates.md` | **结果解释模板**：图表后解释的标准写法 | 写结果 |
| `chart_explanation_templates.md` | **图表解释模板**：折线图/柱状图/热力图后说明 | 图表后写作 |
| `transition_sentence_bank.md` | **过渡句库**：章节/模型/结果间过渡表达 | 润色 |
| `high_score_expression_library.md` | **高分表达库**：可直接套用的高分句式 | 写作/润色 |
| `winning_paper_pattern_library.md` | **获奖论文模式库**：优秀论文的可复用结构 | 学习/对照 |
| `paper_upgrade_playbook.md` | **论文升级手册**：从初稿到终稿的升级路径 | 改稿 |
| `topic_selection_guide.md` | **选题策略**：A/B/C 题选题判断 | 选题 |
| `phrase_bank.md` | **竞赛特化句式库**：国赛获奖论文高频句式，按章节分类 | 写作/润色 |
| `empirical.json` | **实测分位数据**：91篇国赛获奖论文的p25/p50/p75统计 | 评分锚定/质量评估 |

### 🔍 审稿评分层（12 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `scoring_rubric.md` | **主入口（唯一评分标准）**：100分制7维度 | 审稿/打分 |
| `revision_checklist.md` | **修改清单**：P0/P1/P2修改优先级 | 改稿 |
| `review_priority_matrix.md` | **审稿优先级矩阵**：问题排序 | 审稿 |
| `review_section_checklists.md` | **分节审稿清单**：逐段审稿 | 审稿 |
| `review_quick_comments.md` | **审稿短评模板**：快速审稿意见 | 审稿/复盘 |
| `paper_score_calibration_library.md` | **评分校准库** | 校准打分 |
| `bad_cases.md` | **反例库**：低分案例与教训 | 学习/避坑 |
| `bad_expression_blacklist.md` | **低分表达黑名单** | 写作/改稿 |
| `common_failure_patterns.md` | **常见失败模式** | 复盘/避坑 |
| `diagnostic_templates.md` | **诊断模板**：快速定位论文问题 | 审稿 |
| `model_specific_pitfalls.md` | **分题型避坑库** | 建模/复盘 |

### 🎤 答辩准备层（7 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `defense_qa_bank.md` | **主入口**：高频问答库 | 答辩准备 |
| `defense_followup_chains.md` | **追问链**：二追、三追问及应对 | 答辩演练 |
| `defense_short_answers.md` | **短答模板**：30秒快速回应 | 答辩 |
| `defense_model_specific_answers.md` | **分题型/分模型答辩口径** | 答辩 |
| `defense_opening_and_closing.md` | **开场收束模板** | 答辩 |
| `slide_defense_workflow.md` | **PPT答辩流程** | PPT制作 |

### 📊 数据处理层（3 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `data_cleaning_standards.md` | **主入口**：字段/单位/缺失/异常统一口径 | 数据理解 |
| `data_understanding_workflow.md` | **数据理解流程**：字段映射、质量诊断 | 数据理解 |
| `table_result_alignment_workflow.md` | **表格对表流程**：数字一致性核对 | 写作/终检 |

### ✅ 质量验收层（5 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `final_quality_gate.md` | **主入口**：P0阻断项终检清单 | 提交前 |
| ~~`final_quality_gate_workflow.md`~~ | ~~终检流程~~ | **v4.8 已归档**（内容被 `final_quality_gate.md` 完全覆盖）→ 用 `final_quality_gate.md` |
| `tools/quality_gate/final_gate_runner.py` | **一键终检总门（v4.5）**：G4.7 实物门+G4.6 自证门+G5 证据门+G4.8 数字一致性+G4.9 公式核验；`--paper-dir` 支持任意作品目录 | 提交前 |
| `tools/quality_gate/paper_artifact_check.py` | **G4.7 实物门（v4.5）**：docx 表格实体/图片/占位符、result*.xlsx 数据区非空、代码存在性 | 提交前 |
| `paper_output/plan/formula_verification.md` | **G4.9 公式核验记录（v4.5）**：真题核心公式与官方参考答案核对结果 | 建模时 |
| `validation_checklist.md` | **检验清单**：模型检验/误差/稳健性 | 补检验 |
| `reproducibility_checklist.md` | **复现清单**：代码复现核对 | 提交前 |
| `sensitivity_and_robustness_templates.md` | **灵敏度/稳健性模板** | 写检验 |

### 🎨 图表可视层（4 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `figure_templates.md` | **主入口**：图示结构模板 | 生成图示 |
| `table_templates.md` | **表格模板** | 生成表格 |
| `visual_knowledge_base.md` | **可视化知识库** | 图表选型 |
| `visualization_strategy_library.md` | **可视化策略库** | 图表策略 |

### 📦 提示词调度层（1 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `prompt_master_pack.md` | **提示词总母版**：国赛/美赛/五一赛全题型提示词 | 赛中/快速调用 |

### 🏆 赛中流程层（1 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `competition_checklist.md` | **赛中 72 小时检查清单**：按时间线的逐项检查 | 比赛当天 |

### 🔬 Nature Skills 桥接层（1 文件）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `nature_skills_bridge.md` | **Nature Skills 归档公告**（v3.0）：9 个 Nature skill 已归档，方法论精华去向说明 | 需要了解 Nature skill 归档后能力去向时 |

### 📚 提取文本层

| 路径 | 用途 |
|------|------|
| `extracted_document_text/` | DOCX/PDF 抽取的可检索文本 |
| `extracted_pdf_text/` | 获奖论文 PDF 抽取文本 |
| `extracted_material_synthesis.md` | 抽取材料综合归档 |
| `_reports/award_pdf_extraction_report.md` | PDF 提取报告（已归档） |
| `_reports/award_pdf_ocr_report.md` | OCR 处理报告（已归档） |
| `_reports/document_extraction_log.txt` | 提取日志（已归档） |
| `current_paper_extracted.txt` | 当前论文提取文本 |

### 🏆 竞赛差异指南（新增收录）

| 文件 | 用途 | 何时调用 |
|------|------|----------|
| `competition_specific.md` | **竞赛差异化指南**：CUMCM/MCM/ICM/MathorCup/五一赛/电工杯的格式和评分标准 | 选赛事后/提交前 |

---

## 三、双向引用导航（Karpathy 交叉引用）

> 每个文件标注「→ 被谁调用」和「← 依赖谁」，形成可跳转的知识网络。
> 完整图谱见 `knowledge_graph.md`，查询工具见 `scripts/knowledge_graph_query.py`。

### 引用格式说明

| 符号 | 含义 | 示例 |
|------|------|------|
| `→` | 本文件被以下文件/阶段调用 | `scoring_rubric.md → review_section_checklists.md` |
| `←` | 本文件依赖以下文件 | `paper_upgrade_playbook.md ← scoring_rubric.md` |
| `↔` | 双向依赖 | `file_map.md ↔ asset_registry.md` |

### 核心文件引用链

```
task_router.md
  → 被 INDEX.md 定位
  → 被 00_route_task.md 调用
  ← 分流到: method_matching | writing_templates | scoring_rubric | defense_qa_bank | final_quality_gate

method_matching.md
  ← 来自: task_router.md（审题阶段分流）
  → 流向: model_selection_flow.md（详细流程）
  → 流向: algorithm_templates.md（代码模板）
  → 流向: algorithm_selection_red_flags.md（避坑）
  ← 参考: problem_type_taxonomy.md（题型识别）
  ← 参考: case_to_method_route_library.md（历史路线）

scoring_rubric.md（唯一评分标准）
  ← 来自: task_router.md（审稿阶段分流）
  → 流向: review_section_checklists.md（分节审稿）
  → 流向: review_priority_matrix.md（问题排序）
  → 流向: paper_score_calibration_library.md（校准）
  → 流向: diagnostic_templates.md（诊断）
  → 流向: revision_checklist.md（改稿清单）
  → 流向: paper_upgrade_playbook.md（改稿行动）

writing_templates.md（写作主入口）
  ← 来自: task_router.md（写作阶段分流）
  → 流向: abstract_templates.md（摘要专项）
  → 流向: section_writing_templates.md（分节模板）
  → 流向: result_analysis_templates.md（结果分析）
  → 流向: high_score_expression_library.md（表达升级）
  ← 润色补丁: transition_sentence_bank.md
  ← 升级对照: paper_upgrade_playbook.md

final_quality_gate.md（终检）
  ← 来自: task_router.md（验收阶段分流）
  ← 依赖: scoring_rubric.md（评分标准）
  ← 依赖: validation_checklist.md（检验清单）
  ← 依赖: reproducibility_checklist.md（复现清单）
  → 流向: 21_generate_submission_pack.md（打包提交）

knowledge_graph.md（知识图谱）
  ← 被所有建模选模文件引用
  → 查询工具: scripts/knowledge_graph_query.py
  ↔ 同步: scripts/knowledge_graph_query.py（查询工具）
```

### 跨层引用热力图

| 文件 | 被引用次数 | 主要引用者 |
|------|-----------|-----------|
| `scoring_rubric.md` | 8 | review_*, revision_*, paper_upgrade_*, diagnostic_* |
| `method_matching.md` | 6 | model_selection_*, algorithm_*, case_to_method_* |
| `writing_templates.md` | 6 | abstract_*, section_*, result_*, high_score_* |
| `task_router.md` | 5 | INDEX.md, prompts_outputs_call_map, 所有阶段入口 |
| `final_quality_gate.md` | 4 | validation_*, reproducibility_*, 21_generate_* |
| `algorithm_templates.md` | 4 | code_template_playbook, code_asset_index, method_matching |
| `knowledge_graph.md` | 3 | method_matching, memoryskill, knowledge_graph_query.py |

---

## 五、功能域→Prompt 对应关系

| 功能域 | 对应 Prompts（按调用顺序） |
|--------|---------------------------|
| 系统调度 | `00_route_task` → `23_start_new_case` |
| 资料建库 | `01_full_scan` → `02_extract_cards` → `03_build_rules` |
| 审题选题 | `07_select_topic` → `11_identify_problem_type` → `12_select_model_route` |
| 写作改稿 | `05_generate_templates` → `08_review_math_modeling_paper` → `13_upgrade_result_analysis` → `15_rewrite_abstract` |
| 检验补强 | `10_validation_output` → `14_strengthen_validation` → `17_check_chain_closure` |
| 答辩准备 | `06_mock_defense` → `09_defense_math_modeling` → `18_defense_followup_drill` → `27_generate_slides` |
| 代码生成 | `19_generate_code` |
| 图示生成 | `20_generate_figures` → `26_generate_tables` |
| 数据理解 | `30_data_understanding` |
| 质量验收 | `24_dynamic_acceptance` → `28_final_quality_gate` → `21_generate_submission_pack` |
| 知识更新 | `29_update_knowledge_assets` |
| 提示词调度 | `25_prompt_master_pack` |
| 案例回灌 | `22_case_feedback_loop` |
| 低分快诊 | `16_low_score_risk_diagnosis` |
| 审稿改稿 | `04_review_my_paper` → `08_review_math_modeling_paper` |

---

## 六、命名规范

### outputs/ 文件命名规范

| 规则 | 说明 | 示例 |
|------|------|------|
| 全英文 snake_case | 文件名统一英文小写下划线 | `scoring_rubric.md` ✅ |
| 不含编号前缀 | 功能域分类靠本 INDEX，不靠文件名编号 | ~~`01_method_matching.md`~~ ❌ |
| 不含中文 | 文件名不含中文字符 | ~~`评价模板.md`~~ ❌ |
| 分类靠目录/索引 | 同一功能域的文件通过本 INDEX 聚合 | 见上方分类表 |

### prompts/ 文件命名规范

| 规则 | 说明 | 示例 |
|------|------|------|
| 两位数编号 + 英文描述 | 编号唯一，功能清晰 | `00_route_task.md` ✅ |
| 编号无跳跃 | 00-30 连续，无重复 | ~~两个 25 号~~ ❌（已修复） |

---

## 五、系统调用最小闭环

```
收到任务
  ↓
00_route_task.md → task_router.md（分流）
  ↓
按阶段选对应 prompt + output（查本 INDEX）
  ↓
执行：审题 → 选模 → 写作 → 代码 → 图示 → 检验
  ↓
28_final_quality_gate.md → final_quality_gate.md（终检）
  ↓
21_generate_submission_pack.md（打包提交）
  ↓
22_case_feedback_loop.md → case_feedback_loop.md（回灌经验）
```

---

## 六、自动回环修正（2026-06-21 新增）

当检测脚本发现质量问题时，自动运行修正器并重检，最多循环 3 轮，仍失败才报告用户。

```bash
python .claude/skills/quality-assurance-auditor/scripts/auto_correct_loop.py
```

| 阶段 | 检测脚本 | 自动修复器 | 修复能力 |
|------|---------|-----------|---------|
| code | run_and_verify.py | code_auto_fixer.py | 缺少导入/路径错误/编码错误/除零 |
| number | check_number_consistency.py | number_auto_fixer.py | 论文数字与frozen_numbers不一致 |
| result | check_result_reasonableness.py | evidence_auto_filler.py | 缺失证据文件自动生成占位 |
| format | check_paper_format.py | format_auto_fixer.py | 空行/标点/公式格式/图表引用 |
| evidence | evidence_gate.py | evidence_auto_filler.py | 缺失目录/文件自动创建 |
| parameter | check_parameter_consistency.py | （需人工确认） | 参数不一致 |
| consistency | consistency-auditor/audit.py | number_auto_fixer.py | 跨文件数字不一致 |
| figure | math-figure/render_check.py | figure_auto_fixer.py | DPI/字体/重叠 → 自动调整参数重新渲染 |
| latex | latex-renderer/render_formulas.py | latex_auto_fixer.py | LaTeX语法错误 → 自动修正 |
| completeness | completeness-auditor/audit.py | completeness_auto_filler.py | 缺失文件/目录 → 自动创建占位 |
| citation | citation_auto_fixer.py | citation_auto_fixer.py | 断链引用/格式错误 → 自动修正 |
| aigc | aigc_auto_fixer.py | aigc_auto_fixer.py | AI痕迹过高 → 自动降重 |
| symbol | symbol_auto_fixer.py | symbol_auto_fixer.py | 符号重复/不一致 → 自动解决 |
| code_style | code_style_auto_fixer.py | code_style_auto_fixer.py | PEP8/格式 → 自动格式化 |

修正日志：`paper_output/qa/auto_correction_log.json`

---

## 七、GitHub 集成资源（2026-06-21 新增）

> 以下资源通过 GitHub 集成自动同步至 `resources/` 目录，供全系统调用。

### 新增算法模板（22 个）

路径：`resources/04_代码模板/Python/`

| 子目录 | 算法文件 | 用途 |
|--------|----------|------|
| `evaluation/` | `dea_efficiency.py` | DEA 数据包络分析 |
| `evaluation/` | `fahp_fuzzy.py` | 模糊层次分析法（FAHP） |
| `evaluation/` | `rsr_rank_sum.py` | RSR 秩和比法 |
| `evaluation/` | `grey_relational_heatmap.py` | 灰色关联分析热力图 |
| `optimization/` | `nsga2_multi_obj.py` | NSGA-II 多目标优化 |
| `optimization/` | `cvar_robust.py` | CVaR 鲁棒优化 |
| `optimization/` | `system_dynamics.py` | 系统动力学仿真 |
| `optimization/` | `sa_geodesic.py` | 模拟退火（测地线版） |
| `prediction/` | `grey_prediction_gm11.py` | GM(1,1) 灰色预测 |
| `prediction/` | `markov_chain.py` | 马尔可夫链 |
| `prediction/` | `markov_chain_lupynow.py` | 马尔可夫链（Lupynow 增强版） |
| `prediction/` | `hmm_hidden_markov.py` | 隐马尔可夫模型（HMM） |
| `prediction/` | `gaussian_process.py` | 高斯过程回归 |
| `simulation/` | `food_web_ode.py` | 食物网 ODE 仿真 |
| `statistical/` | `mk_mutation_test.py` | Mann-Kendall 突变检验 |
| `statistical/` | `bayesian_network.py` | 贝叶斯网络 |
| `statistical/` | `gmm_em.py` | 高斯混合模型（EM 算法） |
| `statistical/` | `lof_from_scratch.py` | LOF 局部异常因子检测 |
| `statistical/` | `mcmc_gibbs.py` | MCMC Gibbs 采样 |
| `statistical/` | `mcmc_metropolis_hastings.py` | MCMC Metropolis-Hastings 采样 |
| `signal/` | `wavelet_analysis.py` | 小波分析 |
| `ml/` | `bpnn_from_scratch.py` | BP 神经网络（手写实现） |

**调用入口**：`/code` → `code_asset_index.md` → 按题型选取对应模板

### 新增 O 奖论文（187 篇）

路径：`resources/02_优秀论文/MCM_ICM_O奖/`

| 年份 | 题号 | 论文数 | 路径 |
|------|------|--------|------|
| 2016 | A-F | 21 篇 | `2016美赛O奖论文/` |
| 2019 | A-F | 39 篇 | `2019/A/` `2019/B/` ... `2019/F/` |
| 2020 | A-F | 41 篇 | `2020/A/` `2020/B/` ... `2020/F/` |
| 其他年份 | A-F | 86 篇 | 按年份/题号目录组织 |

**用途**：学习 O 奖论文结构、图表规范、摘要写法、模型选择策略
**调用入口**：`/review` 对照评分锚点 → `winning_paper_pattern_library.md`

### 新增 LaTeX 模板（3 版）

路径：`resources/13_LaTeX模板/`

| 模板 | 文件 | 适用场景 |
|------|------|----------|
| CUMCM 国赛模板 | `latex_template.tex` | 国赛论文排版 |
| MCM 美赛模板 | `mcm_template.tex` | 美赛论文排版 |
| MCM 备忘录模板 | `mcm_memo_template.tex` | 美赛 Memo 格式 |
| MCM 宏包（v4.02） | `MCM_mcmthesis_v402/` | mcmthesis.sty + 完整示例 |
| MCM cls 版 | `MCM_mcmthesis_cls/` | mcmthesis.cls 文档类版 |
| MCM 标准版 | `MCM_latex_template/` | 标准 MCM LaTeX 模板 |

**用途**：国赛/美赛论文排版，公式、图表、参考文献的 LaTeX 标准写法
**调用入口**：论文排版阶段 → `paper-formal-writer` → 选取对应模板

### 新增参考资料

路径：`resources/08_参考资料/`

#### 32 种方法教材（16 章 PDF）

路径：`resources/08_参考资料/32种方法教材/`

| 章节 | 内容 |
|------|------|
| 第1-4章 | 线性规划、整数规划、非线性规划、动态规划 |
| 第5-7章 | 图与网络、排队论、对策论 |
| 第8-9章 | 层次分析法、插值与拟合 |
| 第10-12章 | 数据统计描述、方差分析、回归分析 |
| 第13章 | 微分方程建模 |
| 第19章 | 神经网络模型 |
| 第22章 | 模糊数学模型 |
| 第28章 | 灰色系统理论及其应用 |

**用途**：建模选模时的理论依据和方法参考
**调用入口**：`/analyze` → `method_matching.md` → 理论支撑

#### 经典题解 90+ 篇

路径：`resources/08_参考资料/经典题解90/`

覆盖 90+ 道经典数学建模赛题的完整解答，包括：优化调度、选址分配、投资组合、排队系统、路径规划、评价决策等题型。

**用途**：学习建模思路、论文结构、求解方法
**调用入口**：`case_to_method_route_library.md` → 历史路线参考

#### 灵敏度分析论文

路径：`resources/08_参考资料/`（含于速成资料中）

**用途**：灵敏度分析方法论和写作参考
**调用入口**：`sensitivity_and_robustness_templates.md`

---

## 七、维护规则

1. **新增文件**：必须在本 INDEX 中登记所属功能域
2. **废弃文件**：在本 INDEX 标注"已废弃"，保留一周后删除
3. **功能重叠**：以本 INDEX 标注的"主入口"为准，其余为补充库
4. **版本更新**：每次重大变更后更新本文件顶部的"最后更新"日期
