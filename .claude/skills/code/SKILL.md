---
name: code
description: "判断题型与算法，生成可运行代码框架。触发词：生成代码、写代码、代码框架、code、从零写代码、题型判断代码、算法代码生成。"
---

# /code — 生成代码

判断题型与算法 → 生成可运行或可补全的代码框架。

> **与 algorithm-runner 的区别**：本 skill 从零生成新代码；`algorithm-runner` 执行已有算法模板。如需执行已有模板而非从零写代码，走 `/algorithm-runner`。

调用 `prompts/19_generate_code.md` 执行代码生成。
对齐 `outputs/method_matching.md`、`outputs/algorithm_templates.md`、`outputs/code_template_playbook.md`。

输出：题型判断 → 算法推荐 → 代码结构 → 主体代码 → 直接运行/待补标注 → 论文对接说明。

输出最后一节自动补：**如需执行已有算法模板（而非从零写代码），见 algorithm-runner skill。**

系统同步说明：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。