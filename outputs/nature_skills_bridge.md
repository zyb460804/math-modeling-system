# outputs/nature_skills_bridge.md — Nature Skills 与数学建模系统桥接

> **v2.0 | 2026-05-31**
> **用途：** 将 `nature-skills/` 中的 3 个高价值 skill 接入数学建模生产系统，提供跨系统调用指引。

---

## 一、接入策略

Nature Skills 是面向学术论文投稿的技能模块，其中 3 个与数学建模竞赛直接重叠：

| Skill | 竞赛场景 | 对应 outputs/ 文件 |
|-------|----------|-------------------|
| `nature-figure` | 论文配图、答辩图表、多面板结果图 | `figure_templates.md`、`visualization_strategy_library.md` |
| `nature-paper2ppt` | 答辩 PPT 制作 | `slide_defense_workflow.md` |
| `nature-writing` | 美赛英文写作、摘要润色 | `writing_templates.md`、`high_score_expression_library.md` |

---

## 二、nature-figure 调用指引

**何时调用**：需要生成论文配图或答辩图表时，先按 `outputs/figure_templates.md` 确定图种和结构，再按 nature-figure 的标准提升到投稿级质量。

**调用路径**：
1. 判断图种（流程图/结果图/对比图/检验图）→ `outputs/figure_templates.md`
2. 确定图表结论和证据逻辑 → nature-figure "figure contract" 方法
3. 选择 Python (matplotlib/seaborn) 或 R (ggplot2)
4. 按 nature-figure 标准生成 → SVG/PDF/TIFF 输出

**竞赛适配规则**：
- 国赛/五一赛优先用 Python (matplotlib)，不需要 R
- 美赛可用 Python 或 R，但团队只能选一个
- 图表风格：简洁学术，避免过度花哨，一图一结论
- 导出格式：国赛 Word 嵌入优先 PNG/SVG；美赛优先 PDF/SVG
- 颜色策略：统一色系，不用彩虹色；红绿仅用于涨跌/好坏方向

**Nature-figure 核心原则（竞赛精简版）**：
1. 先定结论（这张图要证明什么）
2. 再选图种（折线/柱状/热力图/散点/箱线图）
3. 再定布局（单图 vs 多面板）
4. 最后写代码生成

**调用入口**：`nature-skills/skills/nature-figure/skill.md`

---

## 三、nature-paper2ppt 调用指引

**何时调用**：需要生成答辩 PPT 时，替代 `outputs/slide_defense_workflow.md` 的手动流程，直接用论文内容生成 .pptx。

**调用路径**：
1. 准备论文内容（摘要 + 关键图表 + 结论）
2. 调用 nature-paper2ppt → 自动识别论文类型和论点
3. 输出中文答辩 PPT（.pptx）
4. 按 `outputs/defense_qa_bank.md` 补充答辩问答准备

**竞赛适配规则**：
- 国赛/五一赛答辩通常 5-8 分钟，PPT 页数控制在 10-15 页
- 美赛无答辩，不需要此 skill
- PPT 内容来源：摘要 + 模型建立 + 关键结果 + 检验结论 + 优缺点
- 每页不超过 1 个核心信息点

**调用入口**：`nature-skills/skills/nature-paper2ppt/skill.md`

---

## 四、nature-writing 调用指引

**何时调用**：美赛英文论文写作、英文摘要润色、Discussion 结构设计时。

**调用路径**：
1. 先按 `outputs/writing_templates.md` 确定论文骨架
2. 英文表达润色时调用 nature-writing
3. 对照 `outputs/high_score_expression_library.md` 确保竞赛风格

**竞赛适配规则**：
- 仅用于美赛英文写作，国赛/五一赛用中文
- nature-writing 的 "Nature 风格" 需要降级到 "竞赛论文风格"：
  - 不要写 Nature 级别的 Introduction 叙事
  - 保持 Executive Summary 独立成文
  - 图表说明要简洁，不需要 Nature 级详细
  - 假设和局限说明保留，但不需要 Nature 级证据层级

**调用入口**：`nature-skills/skills/nature-writing/skill.md`

---

## 五、跨系统调用速查

| 赛事 | 需要图示 | 需要PPT | 需要英文 |
|------|----------|---------|----------|
| 国赛 | nature-figure (Python) | nature-paper2ppt | — |
| 美赛 | nature-figure (Python/R) | — | nature-writing |
| 五一赛 | nature-figure (Python) | nature-paper2ppt | — |
| 电工杯 | nature-figure (Python) | nature-paper2ppt | — |
| MathorCup | nature-figure (Python) | nature-paper2ppt | — |

---

## 六、不纳入的 Nature Skills 及原因

| Skill | 原因 |
|-------|------|
| `nature-academic-search` | 竞赛期间无文献检索需求，且需要 MCP 工具 |
| `nature-citation` | 竞赛论文引用不要求 Nature 级规范 |
| `nature-data` | 竞赛不需要 Data Availability Statement |
| `nature-reader` | 论文阅读用中文对照更高效，可按需单独调用 |
| `nature-polishing` | 被 nature-writing 覆盖，且竞赛不追求 Nature 级润色 |
| `nature-response` | 竞赛无审稿回复环节 |
