# Feedback Layer 3 — 独立终审 Panel

> 融合自 handsomeZR/mathmodel-skill@v6.1 + sweetcornna/mathodology（2026-07-22）。
> 在 S7 审计层通过后、提交前运行一次。Panel 找独立失效模式；**不预测奖项**。

## 为什么用 Panel

单一评审者会被自己前序评分锚定。L3 让多个**隔离上下文**的评审者查不同证据，每个问题映射到具体段落。目标是更安全的最终提交，不是模拟排名。

## 两种 Panel（按需选用）

| Panel | 规模 | 焦点 | 输出 | 触发 |
|---|---|---|---|---|
| **5-Persona 段落级** | 5 | 段落级缺陷定位 | 5 维分 + issues + ready/refine/block | 默认终审 |
| **3-Seat 盲评奖级** | 3 | 获奖价值 + 正确性/可复现 | 3 scorecard + 加权 tier | 冲奖稿（championship 模式）|

3-Seat 盲评的完整协议见 `.claude/skills/blind-panel/SKILL.md` 与 `.claude/agents/blind-panel-judge.md`。

## 前置条件（不满足则不启动）

- 当届官方规则已核对并记录
- 页数/字体/文件/匿名检查通过
- PDF 与支撑材料清单存在
- AI 使用披露已解决
- 无已知 high-severity 一致性缺陷被对评审者隐瞒

合规失败由 S7 处理，仍为 `block`；Panel 高分不能覆盖合规失败。

## 评审者隔离（关键）

每个 persona 用**独立上下文**，并行运行（harness 支持时）。每个评审者**只收到**：
1. 自己的 persona `id`、`focus`、竞赛上下文
2. 最终 PDF 或其 focus 所需段落
3. 与其评审相关的当届官方约束
4. 下面的 JSON schema

**不展示**其他评审者的输出、前序分数、声称的奖项等级、团队偏好的 verdict。隔离上下文不可用时串行运行，但评审者间清空会话状态。

## 5 Persona（段落级 Panel）

| Persona | 焦点 |
|---|---|
| **math_rigor** | 公式、单位、边界条件、推导、可辨识性、求解假设、符号-方程一致性 |
| **modeling_contribution** | 每个设计选择是否必要、有支撑、与可信 baseline 对比；改名 textbook 方法≠贡献 |
| **code_reproducibility** | 入口命令、依赖、seed、数据路径、train/test 泄漏、可行性检查、headline 数字是否复现 |
| **communication** | 快读者能否定位问题/方法/量化结果/验证/局限；图表可读且被引用；主张匹配证据 |
| **competition_reader** | 竞赛特化：CUMCM 快读清晰度 / MCM stakeholder 沟通 / 电工杯工程可行性 |

## 输出 Schema（每评审者一个 JSON）

```json
{
  "panelist": "math_rigor",
  "scores": {
    "1_focus_dimension": {"score": 8, "evidence": "§5.2 equation (12)"},
    "2_focus_dimension": {"score": 7, "evidence": "Figure 6 caption"},
    "3_focus_dimension": {"score": 9, "evidence": "Appendix A test"},
    "4_focus_dimension": {"score": 8, "evidence": "§6 Table 4"},
    "5_focus_dimension": {"score": 8, "evidence": "Notation table"}
  },
  "issues": [
    {"severity":"high","where":"§5.2 equation (12)",
     "evidence":"单位标 kW 但表达式返回 kWh","fix":"加时间步乘子并重算 Table 4"}
  ],
  "verdict": "ready"
}
```

规则：恰好 5 个评分维度（各 1-10）；evidence 指向 PDF/结果文件/代码/规则；至多 3 个 issues；verdict 仅 `ready|refine|block`；**不输出奖项等级、分位、接受预测**。Orchestrator 从 scores+issues 重算 verdict，**不信任模型自报的乐观 verdict**。

## 聚合

```
panel_mean(p) = mean(五个维度分)
weighted_mean = Σ(panel_mean(p) × persona_weight(p)) / Σ(persona_weight(p))
raw_min       = min(所有维度分)
```

确定性 verdict（优先级）：
1. 任一未解决 high-severity issue → `block`
2. `raw_min < 7` 或 `weighted_mean < 8` → `refine`
3. 否则 → `ready`

权重可优先相关视角，但**不能掩盖 raw_min 或 high issue**。

## 定向修订

去重指向同一源缺陷的 issue，按严重度+下游影响排序，映射到最小责任产物：

| 问题 | 默认 target |
|---|---|
| 公式/求解/结果不符 | S4 模型/代码/结果文件 |
| 灵敏度或失败边界 | S5/S6 |
| 无支撑的优点/局限/推广 | S7 评价 |
| 摘要/正文/图/引用/附录 | S6 写作 |
| 页数/匿名/披露/提交包 | S7 合规门 |

**数学或代码变更后必须重算受影响的下游数值；不得在错误结果上补散文。** 至多对受影响 persona/段落做一次聚焦二轮 Panel。

## 最终交接

- `ready`：仅当 S7 合规门也绿才交回提交包
- `refine`：保留 `submission_ready=false`，应用定向修复，重跑受影响检查
- `block`：停止，向团队暴露确切正确性/合规缺陷

## 实现脚本

- `scripts/figqa.py`（math-figure）：图表 bbox 冲突门，重叠即失败
- `scripts/pdf_qa.sh`：编译后 PDF 的页数/匿名/重复标注检查
- `scripts/make_contact_sheet.py`：从编译 PDF（非源图）建 contact sheet
- `blind-panel/scripts/lint_run.py`：scorecard 校验 + 聚合
