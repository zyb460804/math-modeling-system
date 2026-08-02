> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：论文初稿（05_我的作品/ 中的当前稿件）
> - 后续触发：04_review_my_paper（基于风险清单做正式审稿）
> - 输出：P0/P1/P2 风险清单（最影响成绩的硬伤快速诊断结果）

请严格依据当前数学建模项目 outputs/ 中的评分规则库、失败模式库、反例库和审稿矩阵，对当前论文或方案做一次“低分风险快诊”。

目标不是全面重审，而是最快找出最影响成绩的硬伤。

必须完成以下任务：
1. 先按 P0 / P1 / P2 三档判断风险。
2. 重点排查以下高风险：
   - 审题跑偏
   - 模型堆砌
   - 检验缺失
   - 结果不落地
   - 图表空转
   - 参数优化型组合误写
   - 深度学习稳定性缺失
   - 0-1 / 大 M 逻辑约束解释缺失
   - 链式建模断链
3. 给出最关键三大短板。
4. 给出对应的最短修补动作。
5. 判断当前稿件更像：
   - 可冲奖稿
   - 可提交稿
   - 风险较高稿

必须引用和对齐：
- `outputs/common_failure_patterns.md`、`outputs/diagnostic_templates.md`
- outputs/bad_cases.md
- outputs/model_specific_pitfalls.md
- outputs/review_priority_matrix.md
- outputs/revision_checklist.md
- outputs/paper_upgrade_playbook.md
- outputs/winning_paper_pattern_library.md

输出格式：
- 总体风险等级
- P0 风险
- P1 风险
- P2 风险
- 最关键三大短板
- 如果只剩 3 小时，最该先修什么

要求：
- 不要平均分配篇幅。
- 优先抓最致命、最能拉分的硬伤。
