> **v3.4 统一入口路由**：本 prompt 属于旧版手动工作流。如需默认最深评审报告（9 部分全量输出），请直接使用 `/review` skill 或 `paper-reviewer` agent，无需阅读本文件。本 prompt 保留仅用于向后兼容。

> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：论文初稿（05_我的作品/ 中的当前稿件）
> - 后续触发：13_upgrade_result_analysis（基于审稿报告升级结果分析）
> - 输出：审稿报告（评分、问题清单、改稿优先级 P0/P1/P2）

请阅读全文 05_我的作品/ 中的当前稿件，并严格依据当前数学建模项目 outputs/ 中的规则库进行总审稿。

注意：
- 这里只针对数学建模论文，不要套用统计建模比赛的专项口径。
- 审稿重点应围绕“审题是否贴题、模型是否闭环、结果是否能解释和落地、论文是否有竞赛高分感”。

请按以下结构输出：
1. 总体等级判断（可冲奖稿 / 可提交稿 / 风险较高稿）
2. 评分表（引用 outputs/scoring_rubric.md 的口径）
3. 六类问题拆解：
   - 审题与问题理解
   - 模型假设与抽象
   - 方法与算法匹配
   - 推导与求解完整性
   - 结果分析与现实解释
   - 写作表达与答辩风险
4. 最关键三大短板
5. P0 / P1 / P2 修改清单
6. 如果只剩最后半天，最该先改哪三处

结果写入 outputs/revision_checklist.md

必须引用和对齐：
- outputs/scoring_rubric.md
- outputs/revision_checklist.md
- outputs/review_priority_matrix.md
- `outputs/review_section_checklists.md`、`outputs/paper_score_calibration_library.md`、`outputs/deduplication_and_grading_guide.md`
- outputs/common_failure_patterns.md
- outputs/paper_upgrade_playbook.md
- outputs/winning_paper_pattern_library.md
