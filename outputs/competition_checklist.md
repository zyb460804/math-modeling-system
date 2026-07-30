# outputs/competition_checklist.md — 赛中 72 小时流程检查清单

> **v2.0 | 2026-05-31**
> **用途：** 比赛当天按时间线推进的逐项检查清单。每一步标注入口→规则→产出→检验。
> **索引入口：** `outputs/INDEX.md`

> **定位**：本文件是赛中**72小时检查清单**。按时间线展开的勾选式清单。比赛当天逐项勾选使用。
> **相关文件**：`competition_workflow.md`（赛中工作流详细说明）、`competition_specific.md`（各赛事差异化指南）

---

## 总原则

1. 比赛当天不做「系统建设」，只做「成品生产」
2. 每一步都必须有可交付产出，不做空转
3. 遇到卡点先跳过，最后回来补
4. P0 优先于 P1，P1 优先于 P2

---

## 第一阶段：选题 + 审题（Day 1 上午，约 2-3h）

### ✅ 1.1 选题决策
- [ ] 三道题快速扫描，各写出「最终输出是什么」
- [ ] 对照 `outputs/topic_selection_guide.md` 判断 A/B/C 题稳妥度
- [ ] 按团队能力匹配题型（推导型 → A，比较型 → B，数据驱动型 → C）
- [ ] **产出**：选定题目 + 写出每问最终输出

**入口**：`prompts/07_select_topic.md` + `outputs/problem_type_taxonomy.md`

### ✅ 1.2 题型识别
- [ ] 判断题型（评价/预测/优化/机理/链式综合）
- [ ] 识别显式约束和隐含约束
- [ ] 标记子问题先后关系和服务关系
- [ ] **产出**：题型判断 + 建模主线 + 误判提醒

**入口**：`prompts/11_identify_problem_type.md` + `outputs/method_matching.md`

### ✅ 1.3 数据理解
- [ ] 读取附件，整理字段含义、单位、缺失率、异常值
- [ ] 按 `outputs/data_cleaning_standards.md` 统一口径
- [ ] 建立字段映射表（论文符号 ↔ 代码变量 ↔ 图表标签）
- [ ] **产出**：数据字典 + 预处理方案 + P0 数据风险

**入口**：`prompts/30_data_understanding.md` + `outputs/data_cleaning_standards.md`

---

## 第二阶段：建模 + 代码（Day 1 下午 ~ Day 2 上午，约 8-10h）

### ✅ 2.1 选模路线
- [ ] 按 `outputs/method_matching.md` 确定主模型 + 备选模型
- [ ] 写出每个模型的职责（解决什么问题、输出什么、进入哪一步）
- [ ] 确定最小检验包（查 `outputs/model_validation_by_type.md`）
- [ ] **产出**：建模路线图 + 模型职责分工表

**入口**：`prompts/12_select_model_route.md` + `outputs/method_matching.md`

### ✅ 2.2 代码生成
- [ ] 按题型选算法模板（查 `outputs/algorithm_templates.md`）
- [ ] 代码结构：预处理 → 主模型 → 结果输出 → 可视化
- [ ] 标注可直接运行部分和待替换参数
- [ ] **产出**：可运行代码骨架

**入口**：`prompts/19_generate_code.md` + `outputs/code_template_playbook.md`

### ✅ 2.3 运行 + 结果获取
- [ ] 替换真实数据和参数
- [ ] 运行主脚本，获取结果表格和图表
- [ ] 标记结果是否真实运行 vs 待补
- [ ] **产出**：结果表格（CSV）+ 可视化图表

**质量门**：代码能跑通 + 结果真实生成

---

## 第三阶段：论文写作（Day 2 下午 ~ Day 3 上午，约 8-10h）

### ✅ 3.1 论文结构搭建
- [ ] 按 `outputs/writing_templates.md` 选对应题型骨架
- [ ] 按「问题分析 → 假设 → 模型建立 → 求解 → 结果分析 → 检验 → 结论」顺序
- [ ] **产出**：论文骨架（每节有标题和待填内容指引）

**入口**：`prompts/05_generate_templates.md` + `outputs/writing_templates.md`

### ✅ 3.2 摘要写作（最后写！）
- [ ] 按「对象 → 任务 → 方法 → 关键结果 → 检验 → 价值」闭环
- [ ] 每问压缩为一句话，必须写具体结果数字
- [ ] 控制在 1 页内，关键词 3-5 个
- [ ] **产出**：完整摘要

**入口**：`prompts/15_rewrite_abstract.md` + `outputs/abstract_templates.md`

### ✅ 3.3 模型建立 + 求解过程写作
- [ ] 每个模型写清：变量、目标、约束或评价逻辑
- [ ] 组合模型写清模块职责分工
- [ ] 求解过程写清参数、流程、输入输出
- [ ] **产出**：模型建立 + 求解章节

**入口**：`outputs/section_writing_templates.md`

### ✅ 3.4 结果分析写作
- [ ] 每个关键结果按「现象 → 原因 → 启示」展开
- [ ] 图表后必须有解释句
- [ ] 组合模型必须与基础模型对照
- [ ] **产出**：结果分析章节

**入口**：`prompts/13_upgrade_result_analysis.md` + `outputs/result_analysis_templates.md`

### ✅ 3.5 检验分析写作
- [ ] 至少一种检验：误差/扰动/情景/对照
- [ ] 写清检验对象、方法、结果、结论
- [ ] **产出**：模型检验章节

**入口**：`prompts/14_strengthen_validation.md` + `outputs/sensitivity_and_robustness_templates.md`

---

## 第四阶段：图表 + 表格（Day 3 上午，约 2-3h）

### ✅ 4.1 图示生成
- [ ] 技术路线图（必备）
- [ ] 模型结构图/流程图（按需）
- [ ] 结果展示图（折线/柱状/热力图）
- [ ] 每张图标注图名、用途、放置位置
- [ ] **产出**：图示文件（SVG/PNG）

**入口**：`prompts/20_generate_figures.md` + `outputs/figure_templates.md`

### ✅ 4.2 表格生成
- [ ] 参数表：参数名、值、来源、含义
- [ ] 结果表：核心结果 + 对比
- [ ] 检验表：检验方法 + 结果 + 结论
- [ ] 每张表支撑一句核心结论
- [ ] **产出**：表格文件（CSV/Word）

**入口**：`prompts/26_generate_tables.md` + `outputs/table_templates.md`

---

## 第五阶段：终检 + 提交（Day 3 下午，约 3-4h）

### ✅ 5.1 论文自检
- [ ] 摘要是否完整闭环（有具体结果数字）
- [ ] 关键数字在摘要、正文、图表、结论中是否一致
- [ ] 代码输出 ↔ 论文数字 是否可追溯
- [ ] 图表是否都有图名、坐标轴、单位、图例
- [ ] **产出**：自检清单 + 修改项

**入口**：`outputs/final_quality_gate.md`

### ✅ 5.2 P0 阻断项检查
- [ ] 题型判断是否正确
- [ ] 每问是否有明确输出
- [ ] 是否有至少一项模型检验
- [ ] 摘要是否写了具体结果
- [ ] 关键数字是否可追溯
- [ ] 代码是否能跑通
- [ ] **产出**：P0 通过/不通过判定

**入口**：`prompts/28_final_quality_gate.md` + `outputs/final_quality_gate.md`

### ✅ 5.3 答辩准备
- [ ] 30-60 秒开场陈述
- [ ] 选模理由（为什么选这个模型而不是另一个）
- [ ] 检验结论（做了什么检验、结论是什么）
- [ ] 模型边界（什么情况下不适用）
- [ ] 创新点解释（补了什么短板）
- [ ] **产出**：答辩提纲 + 高频问答

**入口**：`prompts/09_defense_math_modeling.md` + `outputs/defense_qa_bank.md`

### ✅ 5.4 提交打包
- [ ] 论文正文 + 摘要版
- [ ] 代码清单（含 README）
- [ ] 图示清单
- [ ] 答辩材料
- [ ] AI 使用说明（如需要）
- [ ] **产出**：完整提交包

**入口**：`prompts/21_generate_submission_pack.md`

---

## 时间不够时的最短路径

如果只剩 6 小时，按这个顺序：

1. **审题选模**（30min）→ 题型 + 主模型 + 每问输出
2. **代码运行**（2h）→ 主脚本 + 结果表格 + 基本图表
3. **论文骨架**（1h）→ 问题分析 + 模型建立 + 结果 + 结论
4. **摘要**（30min）→ 完整闭环
5. **检验**（1h）→ 至少一种误差/扰动分析
6. **终检**（1h）→ 数字一致性 + P0 检查

---

## 赛后必做

- [ ] 走 `prompts/22_case_feedback_loop.md` 回灌可复用经验
- [ ] 更新 `outputs/knowledge_base.md`
- [ ] 登记新资产到 `outputs/asset_registry.md`
