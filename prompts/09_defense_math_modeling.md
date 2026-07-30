> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：论文终稿（final_paper.docx 或当前定稿）
> - 后续触发：18_defense_followup_drill（基于问答库做追问训练）
> - 输出：强化问答库（贴近国赛/校赛评委问法的高频问题 + 回答口径 + 风险点）

请基于当前数学建模项目 outputs/ 中已经沉淀的规则库，以及 05_我的作品/ 中的当前稿件，构建数学建模答辩强化版问答库。

注意：
- 这里只做数学建模比赛答辩，不要混入统计建模比赛专项要求。
- 问题要尽量贴近数学建模国赛/校赛常见评委问法。

至少覆盖以下类型：
1. 题目理解与问题抽象
2. 模型假设合理性
3. 为什么选这个模型而不是别的模型
4. 算法与变量类型是否匹配
5. 检验与稳健性分析是否充分
6. 结果如何转化为现实建议
7. 创新点是否真实有效
8. 模型边界与局限
9. 最容易被质疑的部分
10. 最容易被追问的 5 个问题

每题必须包含：
- 标准回答
- 风险提示
- 可能追问

结果写入 outputs/defense_qa_bank.md

必须引用和对齐：
- outputs/defense_qa_bank.md
- outputs/defense_model_specific_answers.md
- outputs/defense_followup_chains.md
- outputs/defense_short_answers.md
- outputs/defense_opening_and_closing.md
- outputs/high_score_expression_library.md
- outputs/model_chain_blueprints.md
