# HIL（Human-in-the-Loop）6 种决策动作

> 融合自 `jihe520/MathModelAgent`（2862★）的 HIL 机制。
> 本项目已有 G2.5/G4.5 两道用户决策门（确认型），本文档把决策词汇扩展为 6 种动作，
> 让 pipeline_manager.py 的 pending_review 状态支持更丰富的人机协作。

## 6 种动作

| 动作 | 标记 | 含义 | pipeline 行为 |
|------|------|------|--------------|
| **confirm** | `[APPROVED]` | 批准本阶段，推进到下一阶段 | `advance <stage>` |
| **edit** | `[EDIT] ...` | 用户直接修改产物（如改某段文字/参数），AI 继续推进 | 记录编辑 diff，然后 `advance` |
| **regenerate** | `[REGENERATE]` | 不满意，要求本阶段重做 | 等价 `rework <stage>`，review_round+1 |
| **ask** | `[ASK] 问题` | 用户向 AI 提问澄清，不推进也不返工 | AI 回答后仍停在 pending_review |
| **skip** | `[SKIP]` | 跳过本阶段（如某题不需要灵敏度分析） | 标记 skipped，推进到下一阶段 |
| **abort** | `[ABORT]` | 终止整条流水线 | current_stage=aborted，阻塞 |

## 动作解析规则

用户在 `paper_output/state/human_intervention.md` 写入标记，由
`scripts/parse_hil_action.py` 解析（也可被 `pipeline_manager.py check-approval` 调用）。

```markdown
## 审查结果区

[APPROVED]                      # → confirm

[EDIT] 把摘要第2段"显著提升"改为"提升 23.5%"   # → edit + 指令

[REGENERATE]                    # → regenerate

[ASK] 这个约束为什么要取 0.6？                  # → ask + 问题

[SKIP]                          # → skip（跳过灵敏度分析）

[ABORT]                         # → abort
```

## 与 G2.5/G4.5 的关系

- G2.5（方法选择后）、G4.5（结果确认后）仍由 `decision-logger` 记录用户理由（≥50/≥30 字）
- 本 6 动作是**阶段级**审查（每个 pending_review 都可用），G2.5/G4.5 是**特定节点**的强制理由
- 两者互补：6 动作控制"是否推进"，G2.5/G4.5 控制"决策质量是否记录"

## 注入防护

所有 6 种标记（`[APPROVED]/[EDIT]/[REGENERATE]/[ASK]/[SKIP]/[ABORT]`）均纳入
`security_check.py markdown` 的注入检测——防止用户/AI 伪造标记。
`pipeline_manager.py _sanitize` 在写入状态文件前把 `[X]` 转成 `⟦X⟧`。