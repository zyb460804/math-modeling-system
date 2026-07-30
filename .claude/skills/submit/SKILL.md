---
name: submit
description: 高分自检后输出论文+代码+图表+答辩清单
---

# /submit — 生成提交包

按高分标准自检后，输出论文+代码+图表+答辩材料清单。

> **与 solution-package-builder 的区别**：
> - **本 skill（submit）**：产出**最终比赛提交包**（论文正文+摘要版+代码清单+图示清单+答辩提纲+PPT大纲+缺口项），用于正式比赛提交。
> - **solution-package-builder**：产出**写作中间材料包**（给写手用的 solution package + frozen_numbers.json），不直接用于比赛提交。
>
> 触发时自动按阶段判断：有 `final_paper_source.md` → 走 submit；只有中间结果 → 自动反问用户意图。

调用 `prompts/21_generate_submission_pack.md` 执行提交包生成。
必须先通过 `outputs/final_quality_gate.md` P0 阻断项检查。

输出：论文正文 → 摘要版 → 修改清单 → 代码清单 → 图示清单 → 答辩提纲 → 5 分钟答辩稿 → PPT 页面大纲 → 缺口与待补项。

系统同步说明：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。