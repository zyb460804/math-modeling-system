> 系统同步说明：本文件已纳入统一数学建模生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：08_review_math_modeling_paper 输出的审稿报告
> - 后续触发：论文修改（将升级版结果分析回写论文）
> - 输出：升级版结果分析（现象—原因—比较—启示四段式，替代原始报数）

请严格围绕当前数学建模项目中的 outputs 规则库，把已有结果、表格和图形改写成高分感更强的“结果分析 / 结果解释 / 结果落地”文本。

目标不是重复报数，而是把结果写成“现象—原因—比较—启示”。

必须完成以下任务：
1. 识别当前结果属于哪一类：
   - 排名 / 评价结果
   - 预测结果
   - 回归 / 统计结果
   - 优化方案结果
   - 聚类 / 分类结果
   - 机理仿真结果
   - 链式建模结果
2. 对每个关键结果补成完整解释：
   - 现象是什么
   - 为什么会这样
   - 与谁相比优在哪里 / 代价是什么
   - 对现实决策意味着什么
3. 若有图表，必须给每张关键图补一句“这个图到底说明了什么”。
4. 若是组合模型，必须补：
   - 与基础模型的对照
   - 提升来自哪里
5. 若是链式建模，必须写清：
   - 中间层输出了什么
   - 如何进入决策层
   - 最终动作是什么
6. 若存在边界或局限，必须补一句边界说明，避免写得过满。

必须引用和对齐：
- `outputs/result_analysis_templates.md`、`outputs/result_interpretation_templates.md`
- outputs/chart_explanation_templates.md
- outputs/transition_sentence_bank.md
- outputs/section_writing_templates.md
- outputs/bad_expression_blacklist.md
- outputs/visualization_strategy_library.md
- outputs/model_chain_blueprints.md
- outputs/high_score_expression_library.md

输出格式：
- 关键结果 1：原始结果 → 改写后分析
- 关键结果 2：原始结果 → 改写后分析
- 图表配套解释
- 可直接放入正文的收束段
- 当前结果分析最容易掉分的点

要求：
- 不要只写“结果如图所示”“模型效果较好”这类空话。
- 每段尽量落到现实建议、执行动作或管理启示。
