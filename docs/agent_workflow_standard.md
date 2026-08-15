# Agent 工作规范（硬约束）

> **v1.1 | 2026-08-15**（v4.9 同步：终审阶段默认 championship）
> 背景：2026-08 实测 2023 国赛 B 题，Agent 凭任务熟悉度走"裸 Agent + 门禁"最小闭环，跳过 67 个 skill 与 89 个知识文件，论文自评仅 84 分（B+/A-），低于系统设计上限（90+）。本规范强制 Agent 必须走完整流程。

---

## 一、核心铁律

**门禁通过 ≠ 质量达标。** 门禁是"最低底线"，不是"交付标准"。交付标准是"调完全部相关 skill + 知识沉淀"。

**个人能力用在 skill 没覆盖的地方**（如本题的几何推导），**skill 覆盖的部分必须调用 skill**（选模/写作/降 AI 味/评审/答辩）。不得用"手工替换"代替 skill 调用，不得用"自评"代替"独立评审"。

---

## 二、必须执行的流程（不可跳过）

### 阶段 0：任务启动

```
读题 → 查 outputs/INDEX.md（定位知识资产）→ 查 outputs/method_matching.md（确认题型与方法映射）
```

**禁止**：跳过 INDEX.md 直接凭直觉选模。

### 阶段 1：选模

```
查 method_matching.md（11类任务×模型×算法×风险）
→ 查 model-selector/references/model-selection-matrix.md（95+场景直查）
→ 查 model-selector/references/hmml/（HMML分层方法库，v4.6）
→ 在论文里说明"为何选这个模型"对照系统标准
```

**禁止**：凭"我对这题熟悉"跳过选模查阅。

### 阶段 2：代码

```
查 resources/04_代码模板/（14种必备算法）
→ 查 resources/10_算法cookbook/（8大类算法手写实现）
→ 复用已有实现，不重复造轮子
```

**禁止**：明明有竞赛验证过的代码模板，却从零自己写。

### 阶段 3：写作

写作时必须对照以下文档（读它们不是"可选"）：

| 文档 | 用途 | 何时读 |
|------|------|--------|
| `outputs/phrase_bank.md` | 国赛获奖论文高频句式 | 写每段前 |
| `outputs/scoring_rubric.md` | 7维度100分制评分点 | 写大纲前 |
| `outputs/writing_templates.md` | 填空式高分模板 | 写每章前 |
| `paper-formal-writer/references/section-architecture.md` | 摘要6要素/引言5要素/结果证据阶梯 | 写摘要/引言/结果前 |
| `paper-formal-writer/references/evidence-pyramid.md` | 4层证据金字塔 | 组织论证时 |
| `paper-formal-writer/references/common-phrases.md` | 中英双语学术短语 | 润色时 |
| `outputs/empirical.json` + `dim_weights.json` | 实测分位+题型加权 | 验证图表数量时 |

### 阶段 4：降 AI 味（必须调 skill，不能手工替换）

```
调用 humanizer-zh-academic skill
  → 14 种 AI 模式扫描
  → 7 项硬约束检查
  → 60 分制评分
  → 段落级改写（不是词级替换）
```

**禁止**：用 sed/Python 脚本批量替换"充分→验证"这种词级操作代替 skill 调用。

### 阶段 5：评审（必须调独立 agent，不能自评）

```
调用 /review 或 paper-reviewer agent（9维度深度评审）
→ 对照 scoring_rubric.md 输出 P0/P1/P2 修改清单
```

**注意**：本阶段**不改论文**，只产出评审报告与问题清单。

**禁止**：用"我自评了 7 维度"代替独立 agent 评审。

### 阶段 5.5：按评审意见改稿（论文第三稿）

```
按 P0（必改）→ P1（建议改）→ P2（可选）顺序修改论文
→ 若 P0 改动较大，回到阶段 5 再评审一轮（最多 3 轮）
→ 产出三稿，送门禁
```

**禁止**：评审完直接跳答辩（不改稿）。

### 阶段 6：答辩材料（基于定稿）

```
调用 /defense skill
  → 10 类问答库
  → 30 条追问链
  → 模拟评分
  → 短答模板
```

**禁止**：论文写完不准备答辩材料。

### 阶段 7：盲评终审（v4.9 起 championship 为默认，盲评必做）

```
调用 blind-panel skill（3座独立盲评 + 20分冲突仲裁）
→ 调用 math-figure/scripts/figqa.py（图表碰撞门）
→ 调用 math-figure/scripts/render_check.py（图表质量门）
```

> v4.9 用户偏好固化：championship 为默认模式，本阶段为必做；仅当用户显式说"切 fast"/"这次用 standard"时降级（escape hatch）。

---

## 三、禁止行为清单

| # | 禁止 | 应做 |
|---|------|------|
| 1 | 跳过知识沉淀直接"凭能力做" | 先查 outputs/INDEX.md 定位 |
| 2 | 把"门禁通过"等同于"质量达标" | 门禁是底线，skill 调用才是交付标准 |
| 3 | 用"手工替换"代替 skill 调用 | 调 humanizer-zh-academic / paper-polisher |
| 4 | 用"自评"代替"独立评审" | 调 /review 或 paper-reviewer agent |
| 5 | 凭"对题目的熟悉度"跳过选模查阅 | 查 method_matching + model-selection-matrix |
| 6 | 明明有代码模板却从零自己写 | 查 resources/04_代码模板 + 10_算法cookbook |
| 7 | 论文写完不准备答辩材料 | 调 /defense skill |
| 8 | 凭模糊记忆写"与官方参考一致" | 用代码可复现的验证替代（退化/交叉/对称）|

---

## 四、执行顺序速查

```
读题
→ 查 outputs/INDEX.md
→ 查 method_matching + model-selection-matrix（选模）
→ 查 algorithm_templates + cookbook（复用代码）
→ 写代码 + 真实运行
→ 写论文初稿（对照 phrase_bank + scoring_rubric + section-architecture）【产出初稿】
→ 调 humanizer-zh-academic（降 AI 味，段落级）【产出二稿】
→ 调 /review（独立评审，P0/P1/P2 清单）【产出评审报告，不改论文】
→ 按 P0/P1/P2 修改论文【产出三稿】
→ （P0 改动大时回到评审，最多 3 轮）
→ 跑门禁（证据/格式/图表/G4.6/G4.10/三审计层/终检）【产出定稿】
→ 调 /defense（答辩材料，基于定稿）
→ 调 blind-panel 3 座盲评 + figqa 碰撞门（championship 默认，v4.9；escape hatch 才降级）
```

### 论文产出节点（多轮迭代）

| 节点 | 产出物 | 触发下一阶段 |
|------|--------|-------------|
| 阶段 3 完成 | **初稿**（source.md v1）| 送降 AI 味 |
| 阶段 4 完成 | **二稿**（去 AI 痕迹）| 送评审 |
| 阶段 5 完成 | **评审报告**（不改论文，只发现问题）| 送改稿 |
| 阶段 5.5 完成 | **三稿**（按 P0/P1/P2 改）| 送门禁 |
| 阶段 7 门禁全过 | **定稿**（final_paper.docx）| 送答辩 |

---

## 五、违反本规范的处理

- 若用户发现 Agent 跳过 skill 走捷径，有权要求 Agent 重做相应阶段
- 若 Agent 自行发现跳步，应主动补做并在交付时声明"已补做 X 阶段"
- 不得用"时间紧"作为跳步理由——时间紧应降级模式（fast），不能跳过核心 skill

---

## 六、代码级强制（v4.8 升级：从软约束到硬门禁）

> 原 v1.0 规范是文档级软约束（靠 Agent 自觉读、自觉遵守）。v4.8 新增 `tools/quality_gate/skill_invocation_gate.py`（G5 门禁），把"必调 skill"变成代码级强制——**不调 skill → final_gate_runner FAIL → 不得提交**。

### G5 必调 skill 门禁清单（FAIL 级，未调阻断提交）

> **设计原则**：每个阶段至少 1 道门禁，确保"每个环节都调用了 skill 或知识库"，无裸做环节。

| 门禁 | 阶段 | 必调 skill/知识库 | 期望产出文件 | 通过条件 |
|------|------|------------------|-------------|---------|
| G5.1 | 阶段0 任务启动 | 知识查阅（INDEX/matching/rubric/phrase_bank/section-arch）| `plan/knowledge_checkpoint.md` | 含 5 个关键词 |
| G5.2 | 阶段1 选模 | model-selector（method_matching + matrix + HMML）| `plan/model_selection_check.md` | ≥500 字节 |
| G5.3 | 阶段2 代码 | resources/04_代码模板 + 10_算法cookbook | `plan/code_reuse_check.md` | ≥300 字节 |
| G5.4 | 阶段3 写作 | section-architecture + evidence-pyramid + scoring_rubric | `plan/writing_alignment_check.md` | 含摘要六要素+引言五要素关键词 |
| G5.5 | 阶段4 降AI味 | humanizer-zh-academic | `qa/humanizer_report.json` | score ≥ 40/60 |
| G5.6 | 阶段5 评审 | paper-reviewer agent | `qa/paper_reviewer_report.md` | ≥3000 字节 |
| G5.7 | 阶段5.5 AI失败检查 | ai-failure-checker | `qa/ai_failure_check_report.json` | blocking = 0 |
| G5.8 | 阶段5.5 引用验证 | citation-tracer | `qa/citation_trace_report.md` | ≥200 字节 |
| G5.9 | 阶段6 答辩 | defense | `qa/defense_qa_bank.md` | ≥10 个问答标题 |

### G5 建议调 skill 清单（WARN 级，不阻断但提示覆盖率低）

| skill | 期望产出文件 |
|-------|-------------|
| paper-polisher | `qa/paper_polisher_report.md` |
| style-calibration | `qa/style_calibration_report.md` |
| robustness-checker | `qa/robustness_check_report.md` |
| symbol-table-builder | `plan/symbol_table_auto.md` |
| award-paper-rag mmqa retrieve | `qa/award_paper_rag_results.md` |
| blind-panel（冲奖模式）| `qa/blind_panel_report.md` |

### 执行方式

```bash
# 单独跑 G5 门禁
python tools/quality_gate/skill_invocation_gate.py

# 终检（含 G5，全过才可提交）
python tools/quality_gate/final_gate_runner.py
```

G5 门禁会输出覆盖率（当前 8%，目标 100%），并在 FAIL 时给出每个 skill 的"怎么调"修复指引。
