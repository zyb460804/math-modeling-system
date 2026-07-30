> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：`11_identify_problem_type.md` 的题型判断输出
> - 后续触发：`19_generate_code.md`（代码）或 `05_generate_templates.md`（写作）
> - 输出：主模型 + 备选模型 + 最小检验包 + 写作落点

请基于当前数学建模项目中的规则库，为当前题目输出一份“主模型 + 备选模型 + 检验方案 + 写作落点”的选模建议。

注意：
- 这里只做数学建模选模，不混入统计建模比赛专项口径。
- 目标不是把会的模型全列出来，而是选出最稳妥、最匹配、最容易写出高分感的路线。

必须完成以下任务：
1. 根据题型与数据特征，给出：
   - 主模型
   - 备选模型
   - 不建议优先使用的模型
2. 对每个候选方案说明：
   - 为什么适合
   - 解决什么核心任务
   - 前提条件是什么
   - 最容易踩什么坑
3. 若适合组合模型，必须说明：
   - 谁是主模型
   - 谁是补充模块 / 超参数优化器
   - 为什么组合后确实有增益
4. 若涉及离散决策、互斥、启停、固定费用、指派等逻辑，必须判断是否需要 0-1 变量 / 整数规划 / 大 M 约束。
5. 给出最小检验包：
   - 至少要做哪些误差 / 稳健性 / 对照检验
6. 给出写作落点：
   - 模型建立怎么写
   - 求解怎么写
   - 结果分析怎么写

必须引用和对齐：
- outputs/method_matching.md
- outputs/model_selection_flow.md
- outputs/model_selection_quick_table.md
- outputs/model_validation_by_type.md
- outputs/method_misuse_alerts.md
- outputs/case_to_method_route_library.md
- outputs/code_template_playbook.md
- outputs/algorithm_selection_red_flags.md
- `outputs/model_chain_blueprints.md`、`outputs/competition_workflow.md`
- outputs/writing_templates.md
- outputs/section_writing_templates.md

输出格式：
- 推荐主路线
- 备选路线
- 不建议路线
- 最小检验包
- 写作落点
- 选模风险提醒

要求：
- 明确“为什么是这个模型，而不是别的模型”。
- 不允许只给模型名，不解释变量类型、任务目标和约束结构。
- 参数优化型组合必须写成“主模型 + 超参数优化器”，不能误写成双主模型。
