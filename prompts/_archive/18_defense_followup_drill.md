> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：09_defense_math_modeling 输出的强化问答库
> - 后续触发：答辩准备（追问训练、模拟答辩）
> - 输出：追问清单（二追问、三追问链、关键应答策略、风险回避话术）

请围绕当前数学建模项目中的答辩库与追问链库，针对已有论文或方案生成一套更贴近真实答辩场景的“追问型答辩清单”。

目标不是只给首轮问答，而是把最可能出现的二追问、三追问也补出来。

至少覆盖以下类型：
1. 题目理解与问题抽象
2. 模型假设合理性
3. 为什么选这个模型而不是别的模型
4. 变量类型与算法是否匹配
5. 检验与稳健性是否充分
6. 结果如何落到现实建议
7. 创新点是否真实有效
8. 组合模型是否只是堆砌
9. 0-1 变量 / 大 M 约束到底表达了什么现实逻辑
10. 模型边界与局限

每题必须给出：
- 首问
- 标准回答
- 可能追问
- 追问下的更稳妥回应
- 风险提示

必须引用和对齐：
- outputs/defense_qa_bank.md
- outputs/defense_followup_chains.md
- outputs/defense_short_answers.md
- outputs/defense_model_specific_answers.md
- outputs/defense_opening_and_closing.md
- outputs/high_score_expression_library.md
- outputs/model_chain_blueprints.md

输出格式：
- 高频首问
- 二追问 / 三追问
- 更稳妥回应
- 风险提示
- 最危险的 5 条追问链

要求：
- 问题要像评委会真的问出来的话。
- 回答要短、稳、能自圆其说，避免过度展开把自己带进坑里。
