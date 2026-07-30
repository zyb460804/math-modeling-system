# Gate System（门禁系统）

> **用途**：定义从题目解析到最终提交的 6 道门禁（G1-G6），每道门禁有明确的进入条件、通过条件、失败回退。
> **来源**：MathModeling-skills/CLAUDE.md + design-principles.md
> **版本**：v1.0
> **核心原则**：门禁不是阶段（"我在哪里"），而是"我必须满足什么才能离开"。

---

## 门禁总览

```
G1 PROBLEM_PARSED
  ↓
G2 METHOD_VALIDATED [承重墙]
  ↓
G2.5 METHOD_CHOSEN_BY_HUMAN [人类决策门]
  ↓
G3 CODE_REVIEWED
  ↓
G4.5 RESULTS_JUDGED_BY_HUMAN [人类决策门]
  ↓
G4.6 RESULTS_SELF_VERIFIED [工程纪律门, v4.2]
  ↓
G4 RESULTS_FROZEN [承重墙]
  ↓
G5 PAPER_SECTION_READY
  ↓
G6 AUDIT_LAYER_PASSED
```

**关键规则**：
- 门禁失败后，所有下游产物标记为 DIRTY（不能自动信任）
- 承重墙门禁（[承重墙]）阻断下游所有操作
- 人类决策门禁（[人类决策门]）AI 只能建议，人类必须决策

---

## G1: PROBLEM_PARSED（题目已解析）

**门禁名称**：题目解析完成

**守卫目标**：确保题目被正确拆解为子问题，后续建模有据可依。

### 进入条件（Enter Conditions）

- `problem_files/` 目录非空（题目文件已放入）
- 用户已触发建模任务

### 通过条件（Pass Conditions）

以下文件全部存在且内容完整：

| 文件 | 内容要求 |
|------|---------|
| `planning/parse/problem_analysis.json` | 包含：目标、研究对象、约束条件、可用数据、期望输出、子问题列表 |
| `planning/classification/question_classification.json` | 每个子问题有：题型标签（评价/预测/优化/机理/...）、数据特征、候选方法方向 |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 题目文件缺失 | 提示用户放入 `problem_files/` |
| 子问题拆解不合理（粒度过粗/过细） | 提示 orchestrator 重新拆解 |
| 题型分类缺失 | 回退到 problem-classifier skill |

### 承重墙状态

**否** — G1 失败不阻断文件读取，但阻断方法选择。

---

## G2: METHOD_VALIDATED（方法已验证）

**门禁名称**：候选方法验证完成

**守卫目标**：确保每个候选方法都有真实数据上的 PoC 验证，杜绝"纸上谈兵"。

### 进入条件（Enter Conditions）

- G1 已通过
- 每个子问题的候选方法池已建立（`methods/Qx/qx_method_candidates.md`）

### 通过条件（Pass Conditions）

对每个子问题 Qx 的每个候选方法：

| 检查项 | 规则 | 严重度 |
|--------|------|--------|
| PoC 文件存在 | `methods/Qx/poc/<method>_poc.py` 存在 | CRITICAL |
| PoC 可运行 | PoC 代码必须能成功运行，无报错 | CRITICAL |
| 产出可行性数字 | PoC 必须输出一个具体数值结果（feasibility number） | CRITICAL |
| 使用真实数据 | PoC 必须使用 `workspace/data_clean/` 中的清洗后数据 | HIGH |
| 代码行数 <= 30 | PoC 代码不超过 30 行 | MEDIUM |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| PoC 不存在 | 回退到 method-selector skill，要求生成 PoC |
| PoC 运行失败 | 标记该候选为 `[REJECTED]`，归档到 `workspace/archived/` |
| PoC 无数值输出 | 要求补充输出，或标记为 `[REJECTED]` |
| 所有候选均 REJECTED | 触发备选方案评估，回退到 G1 重新审视子问题拆解 |

### 承重墙状态

**是** — G2 失败阻断代码生成。`code_generation_allowed_Qx = G2 PASS`。

---

## G2.5: METHOD_CHOSEN_BY_HUMAN（人类选模决策）

**门禁名称**：建模手方法选择（人类决策门）

**守卫目标**：AI 只建议不决策；方法选择必须由人类完成并留下理由。这是"AI 不能替人做会被评分的判断"原则的直接体现。

### 进入条件（Enter Conditions）

- G2 已通过（所有候选方法均有 PoC）
- `decision-prompt-builder` 已为该子问题生成 2-3 个 trade-off 问题

### 通过条件（Pass Conditions）

决策文件 `methods/Qx/decisions/method-selector_modeler_decision.md` 满足：

| 检查项 | 规则 |
|--------|------|
| `status` | 必须为 `DECIDED`（PENDING → 门禁 FAIL） |
| `decided_by` | 必须为 `human`（`ai` / `auto` → 门禁 FAIL） |
| `decided_at` | 非空时间戳 |
| `choice` | 指向一个具体的候选方法 ID |
| `rejected_alternatives` | 每个被拒绝的候选都有理由 |
| `confidence` | 非空（low / medium / high） |
| `evidence_refs` | 至少引用一个真实文件路径 |
| 建模手理由 | 非空、>= 50 字、引用具体证据（数字/候选 ID/符号）、不含哨兵标记 |
| 哨兵检测 | 不含 `<<<`、`TODO`、`TBD`、`待补充`、`...`、空字段 |
| 反抄袭 | 理由不得与 `ai_suggestion` 近逐字重复（normalized-whitespace 相等 / 极小编辑距离） |

### 哨兵标记（Sentinel Markers）

```markdown
---
schema_version: 1
skill: method-selector
scope: Q2
decision_id: q2_method_choice
status: DECIDED
decided_by: human
decided_at: 2026-06-06T14:20:00+08:00
ai_suggestion: "M2 entropy-TOPSIS — highest PoC feasibility"
choice: "M2"
rejected_alternatives:
  - { id: "M1", reason: "<<<HUMAN>>>" }   ← 必须由人类替换
  - { id: "M3", reason: "<<<HUMAN>>>" }   ← 必须由人类替换
confidence: medium
evidence_refs:
  - "methods/Q2/poc/m2_poc_result.txt"
---

## 建模手理由
<<<HUMAN: 用你自己的话，说明为什么选择这个方法，引用具体数字或标准。>>>
```

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 理由为空或含哨兵 | 提示用户填写理由 |
| 理由与 AI 建议近逐字重复 | WARN（不硬阻断，但记入 provenance ledger） |
| 理由未引用证据 | 提示用户引用具体 PoC 结果 |
| decided_by 非 human | 强制 FAIL，提示用户亲自填写 |

### 承重墙状态

**是** — G2.5 失败阻断代码生成。`code_generation_allowed_Qx = G2 ∧ G2.5`。

---

## G3: CODE_REVIEWED（代码已审查）

**门禁名称**：代码审查通过

**守卫目标**：确保生成的代码经过独立审查，质量达标。

### 进入条件（Enter Conditions）

- G2 + G2.5 均已通过
- 代码已生成至 `code/Qx/`（Python）或 `code/matlab/Qx/`（MATLAB）

### 通过条件（Pass Conditions）

| 检查项 | 规则 |
|--------|------|
| 审查文件存在 | `code/Qx/reviews/qx_<lang>_review.md` 存在 |
| 通过项数量 | >= 5 个显式 PASS 项（非口头"通过"） |
| 无 CRITICAL 问题 | 审查中无 CRITICAL 级别问题 |
| 代码可运行 | 代码能成功执行，输出到 `results/Qx/experiments/roundN/` |
| 输出完整性 | 生成 `run_summary.json` + 结果文件（CSV/JSON/PNG） |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 审查文件不存在 | 回退到对应 code-reviewer skill |
| PASS 项 < 5 | 要求补充审查内容 |
| 存在 CRITICAL 问题 | 修复代码后重新审查 |
| 代码运行失败 | 回退到代码生成阶段 |

### 承重墙状态

**否** — 但 G3 失败阻断结果冻结。

---

## G4.5: RESULTS_JUDGED_BY_HUMAN（人类结果判定）

**门禁名称**：结果判定（人类决策门）

**守卫目标**：在结果冻结前，人类必须对每个方法的实验结果做出判定（CHOSEN / BACKUP / REJECTED），并给出信心等级。

### 进入条件（Enter Conditions）

- G3 已通过（代码审查通过）
- `result-report-generator` 已生成实验报告
- `robustness-checker` 已生成稳健性报告

### 通过条件（Pass Conditions）

需要两份人类决策文件：

#### 4.5a 结果判定

文件：`methods/Qx/decisions/result-verdict_modeler_decision.md`

| 检查项 | 规则 |
|--------|------|
| 每个方法有判定标签 | `CHOSEN` / `BACKUP` / `REJECTED` 之一 |
| 判定理由引用具体数字 | 必须引用实验报告中的数值 |
| 整轮决策理由 | 说明本轮整体选择逻辑 |
| 信心等级 | low / medium / high |

#### 4.5b 稳定性判定

文件：`methods/Qx/decisions/stability-verdict_modeler_decision.md`

| 检查项 | 规则 |
|--------|------|
| 稳定性等级 | stable / borderline / unstable |
| 引用具体数字 | 必须引用稳健性报告中的数值 |
| 不确定性标记 | 标注哪些结论的稳健性存疑 |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 判定文件缺失 | 提示用户完成判定 |
| 判定理由未引用数字 | 提示用户补充具体数值 |
| REJECTED 标签 | 触发 `[REJECTED]` 归档流程（仅人类标签触发） |

### 承重墙状态

**是** — G4.5 失败阻断结果冻结。`freeze_allowed_Qx = G3 ∧ G4.5`。

---

## G4.6: RESULTS_SELF_VERIFIED（结果强制自证，v4.2 融合自 AutoMCM-Pro）

**门禁名称**：强制代码自证（工程纪律门，非人类决策）

**守卫目标**：每个模型 `paper_output/code/modeling/*.py` 必须配对 `verifications/verify_*.py`，覆盖约束满足 / 物理合理性 / 数值稳定性（inf/nan），全部 ✓ PASS 后结果才能被引用进论文。

### 进入条件（Enter Conditions）
- G4.5 已通过（人类已判定结果）

### 通过条件
- 每个 `modeling/*.py` 都有配对的 `verifications/verify_*.py`
- 所有 verify 脚本退出码 0（无 ✗ FAIL）

### 工具
- 骨架生成：`model-code-and-result-generator/scripts/verification_template.py --all`
- 门禁执行：`quality-assurance-auditor/scripts/verify_gate.py`（报告 `qa/verify_gate_report.json`）
- 数值补充：`check_numeric_sanity.py`（通用 inf/nan/量级扫描）

### 承重墙状态

**是** — G4.6 失败阻断结果冻结。`freeze_allowed_Qx = G3 ∧ G4.5 ∧ G4.6`。

---

## G4: RESULTS_FROZEN（结果已冻结）

**门禁名称**：结果冻结

**守卫目标**：数值从代码流向论文的唯一通道。冻结后，论文中的数字必须来自 `frozen_numbers.json`，而非原始代码输出。

### 进入条件（Enter Conditions）

- G4.5 已通过（人类完成结果判定）
- `solution-package-builder` 已生成论文材料包

### 通过条件（Pass Conditions）

| 检查项 | 规则 |
|--------|------|
| frozen_numbers.json 存在 | `results/Qx/reports/frozen_numbers.json` |
| 冻结时间有效性 | `frozen_at` 时间戳晚于所有源文件的 mtime |
| 每个数值有溯源 | 包含 `{value, source_file, source_line, frozen_at, frozen_by_skill}` |
| 决策溯源 | "为什么选 X" 类句子可追溯到 decision log 中的 `decision_id` |
| 论文材料包存在 | `results/Qx/reports/qx_solution_package_for_writer.md` 存在 |
| 包签完成 | `qx_package_signoff` 包含：keep / downgrade / drop 判定 |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| frozen_numbers.json 不存在 | 回退到 solution-package-builder |
| 源文件比冻结快照更新 | 标记 STALE，触发 解冻→修改→重冻结 三步协议 |
| 数值无法溯源到决策 | 回退到 G4.5 补充决策理由 |

### 承重墙状态

**是** — G4 失败阻断论文写作。论文手不得在 G4 之前写入数值断言。

---

## G5: PAPER_SECTION_READY（论文章节就绪）

**门禁名称**：论文章节完成

**守卫目标**：确保每个子问题的论文章节满足最低质量标准。

### 进入条件（Enter Conditions）

- G4 已通过（结果已冻结）
- 论文手收到 `qx_solution_package_for_writer.md` 材料包

### 通过条件（Pass Conditions）

| 检查项 | 规则 |
|--------|------|
| 字数下限 | 该章节满足最低字数要求（参见 scoring_rubric） |
| 数值讨论深度 | 每个数值结果有 >= 3 个讨论维度 |
| 图表 render_check | 所有论文图表通过 render_check（字号/DPI/尺寸/重叠） |
| 引用完整性 | 所有数值断言可追溯到 frozen_numbers.json |
| 三条规则满足 | Rule 1（有方法详解）、Rule 2（有结果分析）、Rule 3（看材料包） |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 字数不足 | 回退到 paper-section-writer 补充 |
| 讨论维度不足 | 回退到 paper-polisher 增强讨论 |
| 图表未通过 render_check | 回退到 math-figure-generator 修复 |
| 数值断言无法溯源 | 回退到 G4 检查 frozen_numbers |

### 承重墙状态

**否** — 但 G5 失败阻断最终审计。

---

## G6: AUDIT_LAYER_PASSED（审计层通过）

**门禁名称**：三重独立审计通过

**守卫目标**：三个正交审计器全部通过，确保论文可提交。

### 进入条件（Enter Conditions）

- G5 已通过（所有章节就绪）
- 所有子问题的论文章节已汇入主文件

### 通过条件（Pass Conditions）

三个审计器**全部** PASS（单一审计器的 "✅" 不充分）：

| 审计器 | 产出文件 | 检查内容 |
|--------|---------|---------|
| **consistency-auditor** | `paper/audits/cross_media_consistency_audit.md` | 跨媒介数字/文件名/符号/参数一致性（tex ↔ code ↔ frozen_numbers ↔ symbol_table） |
| **completeness-auditor** | `paper/audits/completeness_audit.md` | 所有声称"完成"的 skill 必须有实质性落盘产物（>= 5 PASS 项），口头完成不算 |
| **quality-assurance-auditor** | `paper/qa_report.md` | 工作流完整性、三条规则、反造假、论文质量 |

### 失败条件与回退（Fail & Fallback）

| 失败条件 | 回退操作 |
|---------|---------|
| 任一审计器 FAIL | 定位具体问题，回退到对应阶段修复 |
| 数字不一致 | 回退到 G4 重新冻结 |
| 产物缺失 | 回退到对应 skill 补充产物 |
| 反造假检测失败 | STOP，标记为 CRITICAL，不得提交 |

### 承重墙状态

**是** — G6 失败阻断最终提交。`submit_allowed = G6 PASS`。

---

## 人类决策门禁模式（Human Gate Pattern）

### 设计理念

> AI 拥有机械正确性；人类拥有建模判断。技能系统不能替人做出会被评分的判断。

### 适用门禁

| 门禁 | 决策内容 | 决策文件路径 |
|------|---------|-------------|
| G2.5 | 选择哪个方法、拒绝哪些方法、为什么 | `methods/Qx/decisions/method-selector_modeler_decision.md` |
| G4.5a | 每个方法的结果判定（CHOSEN/BACKUP/REJECTED） | `methods/Qx/decisions/result-verdict_modeler_decision.md` |
| G4.5b | 稳定性判定（stable/borderline/unstable） | `methods/Qx/decisions/stability-verdict_modeler_decision.md` |

### 哨兵标记（Sentinel Markers）

AI 在生成决策文件时，在人类必须填写的字段中放置哨兵：

```markdown
<<<HUMAN: 用你自己的话，说明为什么选择这个方法，引用具体数字或标准。>>>
```

**哨兵规则**：
- 哨兵必须由人类替换为真实内容
- 存活的哨兵（未被替换）阻断对应门禁
- 哨兵检测列表：`<<<`、`TODO`、`TBD`、`待补充`、`...`、空字段

### 恢复流程

1. 人类编辑决策文件，替换哨兵标记
2. `status` 翻转为 `DECIDED`，`decided_at` 刷新
3. 下次 orchestrator 运行时重新检查（无状态）
4. 门禁通过后，下游 DIRTY 产物**不会**自动信任
5. `consistency-auditor` 必须对受影响的 Qx 重新运行增量检查
6. 如果决策位于冻结数字之后，走 解冻→修改→重冻结 三步协议

### Learning 模式 vs Speed 模式

| 行为 | Learning 模式 | Speed 模式 |
|------|-------------|-----------|
| AI 建议时机 | 人类写完理由后才显示（防锚定） | 与问题并排显示 |
| 提问风格 | 2-3 个 trade-off 问题 | 1 个简洁问题 |
| 门禁严格度 | 相同（不削弱） | 相同（不削弱） |
| 字数下限 | 相同 | 相同 |
| 反抄袭检测 | 相同 | 相同 |

---

## 门禁与产物的对应关系

```
G1 → problem_analysis.json + question_classification.json
G2 → methods/Qx/poc/<method>_poc.py + feasibility numbers
G2.5 → methods/Qx/decisions/method-selector_modeler_decision.md [DECIDED by human]
G3 → code/Qx/reviews/qx_<lang>_review.md (>= 5 PASS)
G4.5 → methods/Qx/decisions/*_modeler_decision.md (result verdict + stability verdict)
G4 → results/Qx/reports/frozen_numbers.json + qx_solution_package_for_writer.md
G5 → paper/sections/qx.tex (word count + discussion depth + render_check)
G6 → paper/audits/ (consistency + completeness + QA 三份报告)
```