# 四层容错机制

> 融合自 `jihe520/MathModelAgent`（2862★）的四层容错设计。
> 本项目已有 `auto_detect_and_fix.py` 的 3 轮重试循环（第一层），本文档补全 4 层。
> 当检测脚本发现质量问题时，按层级递进处理，最多 3 轮回退，仍失败才报告用户。

## 四层架构

```
质量问题
   │
   ▼
┌──────────────────────────────────────────────────────┐
│ L1 有限重试（auto_detect_and_fix.py 已实现）          │
│   同一修正器最多重试 3 轮，每轮检测→修复→重检          │
│   适用于：偶发失败、格式小错、导入缺失                 │
└──────────────────────────────────────────────────────┘
   │ L1 失败（3 轮未通过）
   ▼
┌──────────────────────────────────────────────────────┐
│ L2 Fallback Hand Off（回退到更强/更稳方案）            │
│   - 算法失败 → 切换备用算法（如 NSGA-II 失败 → GA）    │
│   - 模型不收敛 → 降低复杂度（非线性 → 线性）           │
│   - LaTeX 编译失败 → 切 Typst（typst-renderer）        │
│   - Word 公式失败 → 切 docx-editor-cn temml 链         │
│   记录 fallback 事件到 qa/fallback_log.json            │
└──────────────────────────────────────────────────────┘
   │ L2 也失败
   ▼
┌──────────────────────────────────────────────────────┐
│ L3 Evaluator Shadow Mode（评估器影子模式）             │
│   不重做，改为"降级交付 + 显式标注不确定"：            │
│   - 原方案保留，但在论文中标注"本结果需进一步验证"     │
│   - consistency-auditor 标记该结论为 LOW_CONFIDENCE    │
│   - paper-reviewer 对该部分加权降分                    │
└──────────────────────────────────────────────────────┘
   │ 仍无法通过门禁
   ▼
┌──────────────────────────────────────────────────────┐
│ L4 Feedback Rerun（反馈注入重跑）                      │
│   - 暂停流水线（pipeline_manager rework），等人介入    │
│   - 把 L1-L3 的失败原因、尝试过的方案写入              │
│     review_request.md，请用户决策                      │
│   - 用户在 human_intervention.md 用 HIL 6 动作响应     │
│   - 默认 max-reworks=5，超出后强制暂停                 │
└──────────────────────────────────────────────────────┘
```

## 与现有机制的关系

| 层 | 本项目已有能力 | 增量 |
|----|--------------|------|
| L1 | `auto_detect_and_fix.py` 3 轮循环（14 阶段修正器） | 已实现，保持 |
| L2 | 部分 cookbook 有备用算法；latex/word 无 fallback | 显式化：fallback_log + 切换规则表 |
| L3 | `consistency-auditor` 可标记不确定 | Shadow 标注协议 + reviewer 降权 |
| L4 | `pipeline_manager.py rework` + max-reworks | 已通过 pipeline_manager 实现 |

## 落地脚本

- L1：`.claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py`（已存在，14 阶段修正器，3 轮重试）
- L2：`fallback_router.py` + `fallback_routes.json`（**已实现**，7 类备用链：optimization/clustering/evaluation/prediction/ml/latex_compile/word_formula）
- L3：`consistency-auditor/scripts/` 增加 LOW_CONFIDENCE 标记
- L4：`pipeline_manager.py rework` + `parse_hil_action.py`（已实现）

## 触发顺序（伪代码）

```python
for layer in [L1_RETRY, L2_FALLBACK, L3_SHADOW]:
    if run_layer(layer) == PASS:
        return PASS
# L1-L3 全失败 → L4 暂停等人
pipeline.rework(stage, feedback="L1-L3 全失败，详见 fallback_log.json")
```