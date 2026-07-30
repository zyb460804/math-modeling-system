# Feedback Layer 2 — 跨阶段一致性回检

> 融合自 handsomeZR/mathmodel-skill@v6.1（2026-07-22）。适配本项目 S0-S8 流程。
> 在 S4/S5/S6 末尾自动触发。读状态文件，检测早期假设/选型/符号是否被后续阶段推翻。冲突时**定向回滚**，而非整段重来。

## 触发时机

```
after S4 (代码结果):  backtrack(targets=[S1 题意, S2 模型路线])
after S5 (证据门禁):  backtrack(targets=[S2 模型路线, S3 数据, S4 代码])
after S6 (正文写作):  backtrack(targets=[S3 数据, S4 代码, S5 证据, S6 稳健性])
```

也可由用户手动触发："做一次 L2 回检" / "做跨阶段一致性检查"。

## 回检矩阵（核心）

| 检查项 | 来源阶段 | 验证阶段 | 检测方法 |
|---|---|---|---|
| 题意前提 | S1 | S4-S7 | 选模 rationale 是否仍成立 |
| 子问题分解 | S1 | S4, S6 | 是否所有 Qi 都覆盖？Q3 复用 Q1/Q2？ |
| 模型路线 | S2 | S4, S5 | 代码实际求解是否仍可解？灵敏度下是否仍最优？ |
| 数据对齐 | S3 | S4, S6 | 代码用的参数/字段是否与题目要求一致（参数一致性门禁） |
| 符号一致 | S4 符号表 | S5, S6 | 全文符号唯一？单位一致？（符号表审计） |
| 数字冻结 | S5 frozen_numbers | S6 | 正文数字与 frozen_numbers.json 是否 100% 一致 |
| 时间预算 | S0 | S4, S6 | 是否超 30%？ |

## L2 Critic Prompt 模板

```
You are a meta-reviewer doing cross-stage consistency check.
Read the state files (problem_analysis.json / model_route.json / frozen_numbers.json / 符号表).
Check:
1. Are {early_stage}'s assumptions/decisions still valid given {late_stage}'s findings?
2. Any symbol/notation drift between stages?
3. Any assumption introduced late that should have been in S4 假设?
4. Any number in paper not matching frozen_numbers.json?
5. Any time budget overrun?

OUTPUT JSON:
{
  "trigger_stage": "S5",
  "checks": [
    {"id":"...", "from_stage":"S2","to_stage":"S4",
     "concern":"<具体描述>", "severity":"critical|warning|info",
     "evidence":"<指向具体文件字段>", "recommended_action":"no_revert|patch|full_revert"}
  ],
  "verdict": "all_consistent|patch_needed|revert_needed"
}
```

## Action 五档

| 动作 | 场景 | 处理 |
|---|---|---|
| `no_revert` | 小漂移，不影响主体 | 在后续 S7 评价/S6 写作显式记录（"本模型假设 X，S5 灵敏度发现 Y，但±10% 内主结论不变"）|
| `patch_local` | 局部修复 | 仅改 target_stage 一个字段 |
| `patch_with_review` | target 修 + 1-2 下游 | target_stage 修 + 下游 mark_for_review |
| `revert_partial` | 回滚 target 一个 sub-field | 如单条假设，触发链式 review |
| `revert_full` | 模型结构性错误（罕见）| 暂停，用户确认后才回滚整阶段 |

## 下游 mark_for_review 范围（不是无脑全重做）

| 下游 stage | review 范围 |
|---|---|
| S4 某 Qi | 仅该 Qi 的结果验证 + 子灵敏度；失败再升级到求解 |
| S5 证据 | 仅最受影响的 1 个参数扰动验证 |
| S6 写作 | 涉及该 concern 的章节，用 extract_diff.py section-level patch |
| S7 审计 | 重跑涉及的一致性/符号检查，不重跑全部 |

`depends_on(s, target, field)`：若下游 stage 的 inputs 含 target.field，则依赖。

## 常见检测案例

1. **符号漂移**：S4 定义 `α` 为折扣率，S5 Q2 中 `α` 被用作拉格朗日乘子 → patch：Q2 改用 `λ`，更新符号表
2. **假设隐式引入**：S5 Q3 引入"风险中性"假设但 S4 没列 → patch：S4 补假设+支撑
3. **模型族不一致**：S2 选优化族，S5 Q3 突然用蒙特卡罗 → (a) 显式说明触发条件；(b) revert_needed
4. **灵敏度推翻假设**：S6 在±5% 下假设 1 被显著推翻 → revert_needed(S4 假设) 或 patch(S7 评价节)
5. **数字不一致**：S6 正文出现 frozen_numbers.json 外的新数字 → patch：以 frozen_numbers 为准

## 与 L1 的区别

| | L1 | L2 |
|---|---|---|
| 触发 | 每阶段结尾 | S4/S5/S6 结尾 + 手动 |
| 范围 | 单阶段内部 | 跨多阶段 |
| 判据 | 5 维 rubric | 一致性 + 推翻关系 |
| 行动 | refine / block | no_revert / patch / revert |
| 频率 | 阶段 1-3 次 | 全程 3-5 次 |

## 输出与日志

每次 L2 触发写入 `paper_output/qa/L2_backtrack_log.json`：
```json
{"type":"L2_backtrack","ts":"...","trigger_stage":"S5",
 "checks_count":7,"actions_taken":{"no_revert":5,"patch":2,"revert":0},"details":[...]}
```

## 与本项目现有审计的关系

- `consistency-auditor`（一致性审计）≈ L2 的工程化子集（数字/文件/符号交叉一致）
- `completeness-auditor`（完整性审计）≈ L2 的产物齐全检查
- L2 = 在两者之上加"跨阶段语义一致性 + 定向回滚决策"
- 三审计层 + L2 回检全部通过才放行
