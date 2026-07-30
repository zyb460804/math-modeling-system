# Tier 1 同级竞品 Diff 与融合报告（v4.1）

- **执行日期**：2026-07-22
- **源仓库**：`handsomeZR-netizen/mathmodel-skill` @ v6.1（153★）· `sweetcornna/mathodology`（37★）
- **克隆位置**（项目外，不污染）：`C:\Users\27824\AppData\Local\Temp\mm_research\`
- **备份位置**（5 个被修改文件）：`C:\Users\27824\AppData\Local\Temp\mm_research\port_backup_20260722\`

## 一、关键发现（为什么移植）

本项目原有短板，对方有成熟方案：

| 本项目短板 | 源 | 价值 |
|---|---|---|
| empirical 无分题型、疑似手工编造 | mathmodel-skill | 59/91 可提取样本 + by_topic A-F 分位 + min/max/mean |
| 评分扁平、无题型差异 | mathmodel-skill | dim_weights：competition×task_type×stage×dim 加权 [0.7,1.5] |
| 单遍 QA、无阶段级 critic | mathmodel-skill | L1 阶段 Critic + diff-only 精修 + verdict 状态机 |
| 无跨阶段回检 | mathmodel-skill | L2 跨阶段一致性 + 定向回滚（不重做整阶段）|
| 单评审者、易虚高、无冲突检测 | mathodology | L3/盲评 3 座 + **20 分冲突规则** + 真实稀缺性校准 |
| 图表只查源图 | mathodology | figqa bbox 碰撞门 + **从编译后 PDF 建 contact sheet** |
| 无节奏控制 | mathmodel-skill | fast/standard/championship 3 模式 |
| 脚本密集、UX 差 | mathmodel-skill | Friendly Mode 问答式（AskUserQuestion）|

## 二、本次融合产物（13 新建 + 5 修改）

### 新建文件
| 文件 | 来源 | 作用 |
|---|---|---|
| `outputs/dim_weights.json` | mathmodel-skill | 题型差异化加权（7dim + stage_dim 两套）|
| `.claude/agents/blind-panel-judge.md` | mathodology | 盲评单座 agent（3 座之一）|
| `.claude/skills/blind-panel/SKILL.md` | mathodology | 盲评 Panel 协议 + 20 分冲突 + 档位阈值 |
| `.claude/skills/blind-panel/scripts/lint_run.py` | mathodology | scorecard 校验 + aggregate 聚合 |
| `.claude/skills/quality-assurance-auditor/references/feedback_layer1_critic.md` | mathmodel-skill | L1 阶段 Critic |
| `.claude/skills/quality-assurance-auditor/references/feedback_layer2_backtrack.md` | mathmodel-skill | L2 跨阶段回检 |
| `.claude/skills/quality-assurance-auditor/references/feedback_layer3_panel.md` | mathmodel-skill+mathodology | L3 独立 Panel |
| `.claude/skills/quality-assurance-auditor/references/feedback_layer4_calibration.md` | mathmodel-skill | L4 证据校准 |
| `.claude/skills/quality-assurance-auditor/scripts/score_artifact.py` | mathmodel-skill | verdict 计算 + aggregate_qi |
| `.claude/skills/quality-assurance-auditor/scripts/extract_diff.py` | mathmodel-skill | diff-only 精修 |
| `.claude/skills/math-figure/scripts/figqa.py` | mathodology | bbox 碰撞门（**自测通过**）|
| `.claude/skills/math-figure/scripts/pdf_qa.sh` | mathodology | 编译 PDF 页数/匿名/重复标注检查 |
| `.claude/skills/math-figure/scripts/make_contact_sheet.py` | mathodology | 从编译 PDF 建 contact sheet |

### 修改文件（已备份）
| 文件 | 变更 |
|---|---|
| `outputs/empirical.json` | v1.0 → v2.0-merged，加分题型 by_topic + 11 dims + 溯源，保留独有字段 |
| `.claude/agents/paper-reviewer.md` | 加 §9 题型加权 + §10 Per-Qi 加权聚合 |
| `.claude/skills/quality-assurance-auditor/SKILL.md` | 加 §四层反馈机制 + 各模式启用规则 |
| `.claude/skills/math-figure/SKILL.md` | 加 §figqa 图表碰撞门 + 与 render_check 分工 |
| `.claude/skills/paper-workflow-orchestrator/SKILL.md` | 加 §3 模式 + §Friendly Mode |

## 三、验证结果

- ✅ empirical.json 合法（version=2.0-merged，11 dims，6 topics A-F）
- ✅ dim_weights.json 合法（10 task_types，4 competitions）
- ✅ figqa.py `--self-test` PASS（正确检出 3 个碰撞）
- ✅ 5 个被修改文件全有备份
- ⚠️ pdf_qa.sh / make_contact_sheet.py 需 poppler-utils；lint_run.py 需 PyYAML（运行时按需安装）

## 四、对当前 A 题的直接影响

| 缺口 | 修复 |
|---|---|
| 图表仅 2 张被扣分 | empirical by_topic[A]：figure p25=5/p50=8 → 精准目标"补到≥5，目标 8"（v1.0 的全局"10-15"是误导）|
| optimizer 被 skipped | dim_weights[A_optimization] 加权 solver_feasibility×1.3 + robustness×1.3 → 评分倒逼补求解器 |
| 自评 96.3 虚高 | blind-panel 真实稀缺性校准（Outstanding≈top1-2%）→ 把分数校准回国二/国一档 |
| 5 子问题整篇评审 | paper-reviewer §10 Per-Qi → 只 refine 挂科的 Qi，不整篇返工 |

## 五、如何启用

```bash
# 1. 盲评（冲奖前）
# 用户说"盲评" / "校准打分" → blind-panel skill 派 3 座并行

# 2. figqa 图表碰撞门
python .claude/skills/math-figure/scripts/figqa.py --self-test
bash .claude/skills/math-figure/scripts/pdf_qa.sh paper_output/final_paper.pdf --max-pages 25 --anonymous

# 3. 模式切换
# 用户说"升级到 championship" → 启用 L3+L4+盲评+figqa
```

## 六、回滚

备份已持久化到项目内：`paper_output/research/port_backup_20260722/`（temp 另有一份副本）。

```bash
# 恢复 5 个被修改文件（从项目内备份）
BK="e:/数学建模/paper_output/research/port_backup_20260722"
cp "$BK/outputs/empirical.json" e:/数学建模/outputs/empirical.json
cp "$BK/outputs/scoring_rubric.md" e:/数学建模/outputs/scoring_rubric.md
cp "$BK/agents/paper-reviewer.md" e:/数学建模/.claude/agents/paper-reviewer.md
cp "$BK/skills/qa/SKILL.md" e:/数学建模/.claude/skills/quality-assurance-auditor/SKILL.md
cp "$BK/skills/math-figure/SKILL.md" e:/数学建模/.claude/skills/math-figure/SKILL.md
cp "$BK/skills/orchestrator/SKILL.md" e:/数学建模/.claude/skills/paper-workflow-orchestrator/SKILL.md
# 删除新建文件（13 个）即可完全回滚到 v4.0
```

## 七、未移植（后续可选）

- mathmodel-skill 的 `competitions/<comp>/` 完整竞赛包（winning_patterns/anti_patterns/distilled_phrases 等）——体量大，按需单独移植
- mathodology 的 8 skills + 9 agents 全量——本项目规模已更大，按需挑选
- `doctor.py`（preflight 体检）、`render_paper.py`（LaTeX 渲染）——本项目有等价物
- harness-agnostic（Codex 互通）——仅用 Codex 时有用

## 八、保留的本项目独有优势（未受影响）

63 skills + 8 agents、真实代码执行流水线、8 道交付门禁、三审计层、Model/Figure 合同、frozen_numbers、PoC 门、8 域 cookbook、100+ O 奖论文库、Nature skill 群——均未改动。本次是**外科手术式增量**，不替换骨架。
