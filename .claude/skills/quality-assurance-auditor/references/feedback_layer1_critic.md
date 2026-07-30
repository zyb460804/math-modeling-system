# Feedback Layer 1 — 阶段级 Critic + diff-only 精修

> 融合自 handsomeZR/mathmodel-skill@v6.1（2026-07-22）。适配本项目 S0-S8 流程。
> 每阶段产出后立即触发；强制结构化 JSON；最多迭代 3 次；diff-only 精修（不重生整稿）。

## 触发时机

每个 S 阶段（S1 题意/S3 数据/S4 代码结果/S5 证据/S6 正文/S7 审计）产出后进入 L1：

```
artifact_v0 = current_stage_output
critique_v0 = layer1_critic(artifact_v0, rubric=outputs/scoring_rubric.md 对应段)

if critique_v0.verdict == "pass":       save & next stage
elif critique_v0.verdict == "refine":
    for i in 1..3:
        artifact_vi = refine_with_diff_only(artifact_v(i-1), critique_v(i-1))  # extract_diff.py
        critique_vi = layer1_critic(artifact_vi, rubric)
        if critique_vi.verdict == "pass": break
        if iter == 3: mark_as_carryover & next stage   # 留给 L2
elif critique_v0.verdict == "block":    halt & report to user
```

## Critic Prompt 模板

```
You are a strict {competition} grader for {stage_id} ({stage_name}).
Score the artifact below against the rubric.

Competition: {cumcm | mcm | diangong | mathorcup | wuyi}
Task type: {task_type}   # 来自 problem_analysis.json，e.g. A_optimization
{task_type_weighting_hint}   # 来自 outputs/dim_weights.json module_weights_7dim

Rubric (outputs/scoring_rubric.md + outputs/dim_weights.json):
{rubric_dims}

Empirical hint (outputs/empirical.json by_topic[topic]，仅作异常提示):
{empirical_hint}

Artifact:
{artifact_content_or_path}

OUTPUT EXACTLY THIS JSON, NO OTHER TEXT:
{
  "stage_id": "<S1|S3|S4|S5|S6|S7>",
  "iteration": <int>,
  "variant": "stage_level" | "per_qi",    # 多子问题论文用 per_qi
  "qi_id": "Q1" | ... | null,
  "scores": {
    "1_<dim_name>": {"score": <int 1-10>, "evidence": "<≤30字>"},
    "2_<dim_name>": {...}, "3_<dim_name>": {...}, "4_<dim_name>": {...}, "5_<dim_name>": {...}
  },
  "min_score": <int>, "mean_score": <float>,
  "issues": [
    {"severity": "high|medium|low", "where": "<§5.1.2 公式(5.3)>",
     "anti_pattern_id": "<A1|B5|...>|null", "fix": "<≤50字>"}
  ],
  "evidence_metrics": {"abstract_chars": <int>, "formula_count": <int>, "figure_count": <int>, "reference_count": <int>},
  "verdict": "pass_early|pass|pass_with_review|refine|refine_partial|block"
}
```

## Verdict 规则（优先级从高到低，顺序不可变）

```python
def verdict(scores, issues, weights=None):
    """
    weights: outputs/dim_weights.json stage_dim_weights[competition][task_type][stage]
    未列出 dim 默认 1.0；clamp [0.7, 1.5]。
    """
    raw_min = min(scores.values())
    weighted_mean = (sum(s * weights.get(d,1.0) for d,s in scores.items())
                     / sum(weights.get(d,1.0) for d,s in scores.items())) if weights else mean(scores.values())
    high_issues = [i for i in issues if i["severity"] == "high"]
    if len(high_issues) >= 1:          return "block"
    if raw_min >= 9 and weighted_mean >= 9: return "pass_early"   # iter-1 早退
    if raw_min >= 7 and weighted_mean >= 8: return "pass"
    return "refine"
```

| verdict | 触发 | 行为 |
|---|---|---|
| `block` | issues 含 ≥1 high | 暂停，用户介入 |
| `pass_early` | raw_min≥9 且 weighted_mean≥9 | iter-1 早退 |
| `pass` | raw_min≥7 且 weighted_mean≥8 | 进下一阶段 |
| `refine` | 其他 | section-patch 精修，iter+=1（cap 3）|
| `refine_partial`（per_qi）| 任 Qi.min<7，其他已 pass | 仅 refine 该 Qi |
| `carryover`（调度器）| iter==3 仍 refine | 进下一阶段，标记由 L2 处理 |

## Per-Qi 场景（多子问题，见 paper-reviewer §10）

Stage S5/S6 对每个 Qi 各跑一次 critic（variant=per_qi, qi_id），全部跑完后调 `scripts/score_artifact.py --mode aggregate_qi` 聚合。**fail-closed**：任 Qi 缺 issues 字段时聚合器失败，不得用均分掩盖 high 严重问题。

## Diff-only 精修协议（关键）

**不要重生整稿。** 用 `scripts/extract_diff.py` 只精修 issues 指出部分：

```
The previous artifact had these issues: {issues_json}
Generate a UNIFIED DIFF (git-style) that fixes them.
Do not rewrite anything not directly mentioned in issues.
```

定向 diff 限制改动范围、便于审查与回滚。

## 各阶段 dim 参考

| Stage | dims |
|---|---|
| S1 题意 | 1_role_clarity / 2_tools_ready / 3_time_planning / 4_problem_scan / 5_collab_protocol |
| S3 数据/选模 | 1_subproblem_decomposition / 2_key_variables / 3_math_skeleton / 4_data_alignment / 5_dependency |
| S4 代码结果（per_qi）| 1_problem_fit / 2_math_rigor / 3_solve_correctness / 4_visualization / 5_physical_meaning |
| S5 证据（stage_level）| 1_subproblem_completeness / 2_cross_reference_chain / 3_symbol_consistency / 4_visual_density / 5_time_budget |
| S6 稳健性 | 1_multivariate_perturbation / 2_perturbation_realism / 3_output_completeness / 4_robust_interval / 5_failure_warning |
| S7 写作 | 1_abstract / 2_section_completeness / 3_formulas_figures_citations / 4_language / 5_visual_consistency |

## 实现要点

- **JSON 必须可解析**：用 `json.loads` 验证
- **issues 长度 ≤ 5**：太多说明需回阶段重做，不是精修
- **iteration cap = 3**：第 4 次直接 carryover
- **block 必须人工介入**：Skill 暂停，输出 issues 等用户确认

## 与其他层接口

- L1 通过 → 写 decision_log + 进下一阶段
- L1 carryover → 标记 issue，在 S5/S6/S8 末尾由 L2 优先回检
- L1 block → 暂停，用户决定 revise 还是放弃

## 实现脚本

- `scripts/score_artifact.py`（已复制）：verdict 计算 + aggregate_qi 模式
- `scripts/extract_diff.py`（已复制）：diff-only 精修
- `scripts/auto_detect_and_fix.py`：现有自动修复回环（L1 的工程化兜底）
