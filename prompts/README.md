# prompts/ 目录说明

> **状态：已归档（v4.8，2026-08-02）**
> **当前状态：32 个文件全部移到 `_archive/`，主路径不再使用。**

## 为什么要归档

这 32 个 prompt 文件是项目早期（v1.0~v3.3）的"手动工作流"系统，每个文件是一个独立的提示词模板（审题/选模/代码/图表/答辩/提交等）。

从 **v3.4** 起，"触发词统一入口"取代了旧"轨道 B"手动口令——所有核心能力（审题/选模/代码/图表/评审/答辩/提交）均由 **Skill 统一入口**覆盖。`prompts/` 降级为"参考文档"。

到 **v4.8**（本次实测 2023 国赛 B 题），确认：
- 32 个 prompt 文件 **100% 有对应 skill 替代**
- 本次做题走 Skill 流水线，**0 个 prompt 被调用**
- skill 系统已成熟，prompt 作为"双保险"的价值消失

因此归档到 `_archive/`，主路径不再保留。

## 替代关系速查

| prompts/ 文件 | 替代的 skill / outputs |
|---|---|
| 00_route_task / MASTER_PROMPT | paper-workflow-orchestrator/SKILL.md |
| 01-03 scan/card/rules | scan / card / rules skill（Legacy 内部调度）|
| 04/08 review | review → paper-reviewer agent |
| 05_generate_templates | outputs/writing_templates.md |
| 06/09/18 defense | defense skill + defense_followup_chains.md |
| 10/14 validation | quality-assurance-auditor（evidence_gate / verify_gate）|
| 11/12 审题选模 | analyze / model-selector skill |
| 13 result_analysis | outputs/result_analysis_templates.md |
| 15 abstract | paper-polisher skill |
| 16 low_score_diagnosis | outputs/diagnostic_templates.md |
| 17 chain_closure | consistency-auditor skill |
| 19 code | code skill |
| 20 figures | figure skill |
| 21 submission_pack | submit / solution-package-builder skill |
| 22/29 case_feedback / knowledge_update | 赛后回灌流程（outputs/case_feedback_loop.md）|
| 23/24 start/acceptance | paper-workflow-orchestrator + qa-auditor |
| 25 master_pack | outputs/prompt_master_pack.md |
| 26 tables | outputs/table_templates.md |
| 27 slides | defense-ppt-builder-zh skill（v4.8 新建）|
| 28 final_gate | tools/quality_gate/final_gate_runner.py |
| 30 data_understanding | data-cleaning-and-visualization skill |

## 如果需要回退

万一 skill 系统出问题，可以从 `_archive/` 恢复对应 prompt 手动执行。但正常工作流应走 skill。

## 相关文档

- CLAUDE.md「口令映射」段——Legacy 口令的 skill 路由
- paper-workflow-orchestrator/SKILL.md——当前主入口
- docs/agent_workflow_standard.md——Agent 工作规范（v4.8）
