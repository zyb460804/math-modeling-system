---
name: blind-panel
description: "提交前盲评 Panel。3 座并行独立评审 + 20 分冲突仲裁 + 真实稀缺性校准。融合自 sweetcornna/mathodology award-gates。触发词：盲评、盲审、模拟评委、panel、冲奖评审、校准打分。"
---

# Blind Panel — 提交前盲评 Panel

> 融合自 sweetcornna/mathodology@award-gates（2026-07-22）。
> 解决本项目"单评审者易虚高、无冲突检测"的短板。与 paper-reviewer（详尽单评）正交：paper-reviewer 给修复清单，blind-panel 给校准后的获奖档位判定。

## 何时用

- paper-reviewer 评审通过、S7 三审计层全绿、准备提交前
- championship 模式（见 paper-workflow-orchestrator §3 模式）的最后冲刺
- 用户说"盲评""盲审""模拟评委""校准打分"

## 3 座盲评协议

Phase 7 在**一条消息内**并行派发 3 个 `blind-panel-judge` 座位，**无共享上下文**。每座只收到：自己的座位简报 + 渲染 PDF + 产物清单。**不收到**阶段日志、其它座记分卡、跨座联系——保证 3 份 scorecard 独立。

| 座 | 角色 | 评分焦点 |
|---|---|---|
| **Seat A** | 旗舰级通用评审 | 综合获奖价值（CUMCM 国一 / MCM Outstanding 视角）|
| **Seat B** | 创新 + 决策有用性 | 是否有真建模贡献；建议是否帮到 stakeholder |
| **Seat C** | 怀疑论应用数学裁判 | **只评正确性 + 可复现性** |

每座按竞赛特化维度打 0-100 分（权重和=1.0），产出加权总分，映射到校准档位，指出"若只改一处"的最限获奖短板。

## 聚合规则（lint_run.py aggregate）

Panel **PASS** 当且仅当**同时**满足：
- (a) 每座的 `implied_tier` ≥ 目标档位
- (b) 最小座 `weighted_total` 过目标总分阈值
- (c) 任一座的任一维度不低于目标档位的维度下限

### ⚠️ 20 分冲突规则（核心创新）

两座在某维度差 **> 20 分** → 判定为**证据冲突**，上交给 lead 仲裁，**绝不被平均掉**，未解决则阻断 clean pass。

### 档位阈值（按真实稀缺性校准，禁止通胀）

| 目标档位 | 总分 ≥ | 维度下限 ≥ |
|---|---|---|
| Outstanding / 国一 | 85 | 70 |
| Finalist / 国一边缘 | 80 | 65 |
| Meritorious / 国二 | 75 | 60 |

> Outstanding ≈ top 1-2%，国一 ≈ top 5-8%。**不得通胀打分强行 PASS。** 本项目历史自评偏高（A 题曾自评 96.3）；盲评负责把分数校准回真实档位。

## 输出块（每座一个 scorecard）

```yaml
scorecard:
  contest: CUMCM
  target_tier: 国一
  seat: A                       # A | B | C
  round: 1
  criteria:                     # 权重和=1.0，分数 0-100
    - {name: 建模, weight: 0.25, score: 82}
    - {name: 求解与算法, weight: 0.25, score: 80}
    - {name: 结果分析, weight: 0.20, score: 78}
    - {name: 论文写作, weight: 0.20, score: 85}
    - {name: 稳健性, weight: 0.10, score: 75}
  weighted_total: 81.0
  implied_tier: 国二
  fix_one_thing: "..."
  ranked_gaps: []
  do_not_regress: []
```

Lead 聚合 3 份 scorecard，写 `paper_output/qa/blind_panel_report.json`：
```json
{
  "target_tier": "国一",
  "seats": {"A": {...}, "B": {...}, "C": {...}},
  "aggregate": {"min_total": 79.5, "any_criterion_below_floor": false,
                "evidence_conflicts": [{"dim":"稳健性","seat_A":75,"seat_C":58,"delta":17}]},
  "verdict": "refine",      # pass | refine | block
  "bottleneck": "Seat C 正确性维度：Q3 结果无法复现"
}
```

## 迭代预算

- Panel 重打：最多 2 轮（round 1-2）
- 单轮无改进即提前停
- 预算耗尽 → 输出 decision_memo，停下等人工决策（**不静默继续**）

## 严重度阶梯（冲突仲裁用）

- `blocker`：违反规则/破坏题意覆盖/模型无效/无法复现/提交不安全
- `high`：不改会降档（含结果呈现稀疏或图表渲染缺陷）
- `medium`：应修或显式接受并说明
- `low`：抛光，不影响正确性/评分/复现/合规

未解决 `blocker`/`high` 不得推进。

## 与本项目其他评审的关系

| 组件 | 职责 | 与 blind-panel |
|---|---|---|
| `paper-reviewer` agent | 详尽单评 + 修复清单 | 互补：reviewer 给怎么改，panel 给校准档位 |
| `quality-assurance-auditor` | 证据/数字/格式门禁 | panel 前置：门禁绿才跑 panel |
| `consistency/completeness-auditor` | 一致性/完整性 | panel 前置 |
| L3 5-persona panel | 段落级缺陷定位 | panel 是奖级 3 座，L3 是段落级 5 人 |
| L4 校准 | 证据账本/反例 | panel 分歧可触发 L4 |

## 脚本

- `scripts/lint_run.py`（已复制自 mathodology）：scorecard 校验 + aggregate 聚合
  ```bash
  python .claude/skills/blind-panel/scripts/lint_run.py aggregate <scorecard_files...> --target 国一
  ```
  前置：PyYAML；脚本缺失依赖时打印可执行提示。

## 输入输出

- 输入：`paper_output/final_paper.docx`（或 PDF）+ 产物清单 + `outputs/scoring_rubric.md`
- 输出：`paper_output/qa/blind_panel_report.json` + 3 份 scorecard yaml
