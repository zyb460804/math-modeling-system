# 数学建模竞赛生产系统 v3.6 — 完整工作流程

> **更新时间**: 2026-06-21
> **系统版本**: v3.6

---

## 一、总览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         数学建模竞赛生产系统 v3.6                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  轨道A: Skill自动化流水线（正式赛题推荐）                                       │
│  轨道B: Prompt手动工作流（灵活/局部任务）                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 二、轨道A：完整流水线

### 阶段总览

```
S0. 预检 → S1. 题意解析 → S2. 模型路线 → S3. 数据处理 → S4. 代码运行
    → S5. 结果验证 → S6. 论文写作 → S7. 三审计 → S8. 最终提交
```

### 详细流程图

```
                              ┌──────────────────┐
                              │   开始新赛题      │
                              └────────┬─────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S0: 预检门禁                                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  脚本: paper-workflow-orchestrator/scripts/preflight_check.py               │
│  检查: problem_files/ 是否非空                                               │
│  产出: paper_output/preflight_report.json                                   │
│  规则: 预检不通过 → 立即停止，不允许"先凑合写一稿"                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │ PASS
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S1: 题意解析                                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: problem-doc-model-selector                                          │
│  产出: paper_output/step1/problem_analysis.json                             │
│  内容: 子问题划分、任务类型、数据特征、约束条件                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S2: 模型路线 + PoC验证（Gate G2 ★）                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: modeling-paper-rubric-and-model-selector                            │
│        ↓                                                                    │
│  Skill: model-selector（含PoC验证）                                          │
│  脚本: model-selector/scripts/poc_validator.py                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/plan/model_route.json                                     │
│    - paper_output/plan/rubric_alignment.json                                │
│    - paper_output/methods/{Q}/poc/{method}_poc.py                           │
│    - paper_output/methods/{Q}/poc/{method}_poc_result.json                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Gate G2 检查项:                                                             │
│    ✓ 每个候选方法有PoC文件（≤30行）                                            │
│    ✓ PoC在真实数据上运行成功                                                  │
│    ✓ PoC产出具体数值结果                                                     │
│    ✗ PoC失败 → 标记[REJECTED] → 归档到 archived/                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Gate G2.5 用户决策（decision-logger）:                                       │
│    ✓ 用户选择最终方法                                                        │
│    ✓ 用户填写选择理由（≥50字）                                                │
│    ✓ 记录到 paper_output/qa/decision_log.json                               │
│    ✗ AI不能代写理由                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S3: 数据处理 + 符号表                                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: data-cleaning-and-visualization                                     │
│  Skill: symbol-table-builder                                                │
│  Skill: authoritative-data-harvester（如需外部数据）                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/data_cleaned/cleaned_data.csv                             │
│    - paper_output/plan/data_plan.json                                       │
│    - paper_output/plan/visualization_plan.json                              │
│    - paper_output/plan/symbol_table.md                                      │
│    - paper_output/figure_index.json                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S4: 代码运行 + 结果生成                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: model-code-and-result-generator                                     │
│  Skill: python-code-reviewer / matlab-code-reviewer                         │
│  Skill: robustness-checker                                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/code/{Q}/q_main.py                                        │
│    - paper_output/code/{Q}/reviews/q_python_review.md                       │
│    - paper_output/results/{Q}/experiments/roundN/                            │
│    - paper_output/results/{Q}/reports/q_final_result_analysis.md            │
│    - paper_output/robustness/{Q}/q_robustness_report.md                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S5: 结果验证 + 数字冻结（Gate G4 ★）                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: solution-package-builder                                            │
│  Skill: decision-logger（Gate G4.5 用户确认）                                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/results/{Q}/reports/q_solution_package_for_writer.md       │
│    - paper_output/results/{Q}/reports/frozen_numbers.json ★                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Gate G4 检查项:                                                             │
│    ✓ frozen_numbers.json 存在且有 frozen_at 时间戳                            │
│    ✓ frozen_at 晚于所有 code_source_files 的 mtime                           │
│    ✓ 每个数字有 source_file 和 source_locator                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Gate G4.5 用户决策（decision-logger）:                                       │
│    ✓ 用户确认结果和稳定性                                                     │
│    ✓ 用户填写确认理由（≥30字）                                                │
│    ✓ 记录到 paper_output/qa/decision_log.json                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S6: 图表生成 + 论文写作                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: math-figure / figure                                                │
│  脚本: math-figure/scripts/render_check.py                                  │
│  Skill: paper-formal-writer                                                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/figures/*.png                                             │
│    - paper_output/tables/*.csv                                              │
│    - paper_output/tables/table_index.json                                   │
│    - paper_output/final_paper_source.md                                     │
│    - paper_output/final_paper.docx                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  图表 render_check 检查项:                                                    │
│    ✓ 最小字体 ≥ 6.5pt                                                       │
│    ✓ 最小分辨率 ≥ 150 DPI                                                    │
│    ✓ 最小尺寸 ≥ 800×600 像素                                                 │
│    ✓ 文字重叠 ≤ 5%                                                          │
│    ✓ 画布使用 ≤ 80% 白色区域                                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  论文数字规则:                                                                │
│    ✓ 论文中的数字必须来自 frozen_numbers.json                                  │
│    ✓ 不能编造数字                                                            │
│    ✓ 修改数字必须走 "解冻→修改→重冻结" 三步                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S7: 三审计层（Gate G6）                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  审计层1: consistency-auditor                                                │
│    脚本: consistency-auditor/scripts/audit.py                                │
│    检查: 数字/文件名/符号与frozen_numbers.json交叉一致性                          │
│    产出: paper_output/qa/consistency_audit_report.json                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  审计层2: completeness-auditor                                               │
│    脚本: completeness-auditor/scripts/audit.py                               │
│    检查: 所有审查文件、审计报告、代码审查是否存在且质量达标                           │
│    产出: paper_output/qa/completeness_audit_report.json                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  审计层3: quality-assurance-auditor                                          │
│    脚本: quality-assurance-auditor/scripts/evidence_gate.py                  │
│    检查: 工作流完整性、反编造、最终把关                                          │
│    产出: paper_output/qa/evidence_gate_report.json                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  规则: 三者全部PASS才能提交论文                                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │ ALL PASS
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  S8: 最终提交                                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Skill: submit                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  正式交付门禁（七者缺一不可）:                                                  │
│    [ ] 证据门禁: evidence_gate.py --mode official                           │
│    [ ] 参数一致性: check_parameter_consistency.py                           │
│    [ ] 结果合理性: check_result_reasonableness.py                           │
│    [ ] 数字一致性: check_number_consistency.py                              │
│    [ ] 格式门禁: check_paper_format.py                                      │
│    [ ] 一致性审计: consistency-auditor                                       │
│    [ ] 完整性审计: completeness-auditor                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  产出:                                                                       │
│    - paper_output/final_paper.docx                                          │
│    - paper_output/final_paper_source.md                                     │
│    - paper_output/qa/（所有审计报告）                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、门禁总览

| 门禁 | 时机 | 检查内容 | 脚本 |
|------|------|---------|------|
| **S0 预检** | 开始前 | problem_files/ 非空 | preflight_check.py |
| **G2 PoC验证** | 选模后 | 每个候选方法≤30行PoC在真实数据上运行成功 | poc_validator.py |
| **G2.5 用户决策** | 选模后 | 用户填写选择理由（≥50字） | decision-logger |
| **G4 数字冻结** | 结果后 | frozen_numbers.json 存在且时效 | solution-package-builder |
| **G4.5 用户决策** | 结果后 | 用户填写确认理由（≥30字） | decision-logger |
| **render_check** | 图表后 | 字体/分辨率/重叠/画布检查 | render_check.py |
| **一致性审计** | 论文后 | 数字/文件/符号交叉一致性 | consistency-auditor |
| **完整性审计** | 论文后 | 审查文件/报告/产物齐全 | completeness-auditor |
| **证据门禁** | 提交前 | 真实结果/指标/图表/表格/结论 | evidence_gate.py |
| **格式门禁** | 提交前 | 字数/标题/图表引用/参考文献 | check_paper_format.py |

---

## 四、关键文件清单

### 输入文件

```
problem_files/              ← 赛题PDF/Word和附件（必须非空，只读保护）
├── A题/
│   ├── problem.pdf
│   └──附件1.xlsx
└── README.md
```

### 输出文件

```
paper_output/
├── step1/
│   └── problem_analysis.json           # 题意分析
├── plan/
│   ├── model_route.json                # 模型路线
│   ├── rubric_alignment.json           # 评分对齐
│   ├── data_plan.json                  # 数据计划
│   ├── visualization_plan.json         # 图表计划
│   ├── symbol_table.md                 # 符号表
│   └── paper_outline.json              # 论文大纲
├── methods/
│   └── {Q}/
│       ├── {Q}_method_candidates.md    # 候选方法
│       └── poc/
│           ├── method_a_poc.py         # PoC代码
│           └── method_a_poc_result.json # PoC结果
├── archived/
│   └── {Q}/
│       └── method_c_REJECTED/          # 淘汰方法归档
├── code/
│   └── {Q}/
│       ├── q_main.py                   # 建模代码
│       └── reviews/
│           └── q_python_review.md      # 代码审查
├── data_cleaned/
│   └── cleaned_data.csv                # 清洗后数据
├── results/
│   └── {Q}/
│       ├── experiments/
│       │   └── roundN/                 # 实验结果
│       └── reports/
│           ├── q_final_result_analysis.md
│           ├── q_solution_package_for_writer.md
│           └── frozen_numbers.json ★   # 冻结数字
├── robustness/
│   └── {Q}/
│       └── q_robustness_report.md      # 鲁棒性报告
├── figures/
│   └── *.png                           # 图表
├── tables/
│   └── *.csv                           # 表格
├── qa/
│   ├── decision_log.json               # 决策日志
│   ├── consistency_audit_report.json   # 一致性审计
│   ├── completeness_audit_report.json  # 完整性审计
│   ├── evidence_gate_report.json       # 证据门禁
│   └── format_check_report.json        # 格式检查
├── final_paper_source.md               # 论文源稿
├── final_paper.docx                    # Word文档
├── figure_index.json                   # 图表索引
└── table_index.json                    # 表格索引
```

---

## 五、Skill路由表

| 用户意图 | 触发词 | 路由Skill |
|---------|--------|----------|
| 开始新赛题 | 开始生成、跑一下这个题 | paper-workflow-orchestrator |
| 审题选模 | 审题、选模、推荐模型 | analyze → model-selector |
| 生成代码 | 生成代码、写代码 | code |
| 运行代码 | 运行算法、执行代码 | algorithm-runner |
| 生成图示 | 画图、流程图、函数图 | figure → math-figure |
| 审论文 | 打分、审稿、严格打分 | review → paper-reviewer |
| 准备答辩 | 准备答辩、模拟答辩 | defense |
| 生成提交包 | 生成提交包 | submit |
| 润色论文 | 润色、改写、polish | paper-polisher |
| 降AI味 | 降AI味、降重 | humanizer-zh-academic |

---

## 六、Quick Start

### 安装验证

```bash
python .claude/skills/paper-workflow-orchestrator/scripts/quickstart_run.py
```

### 正式赛题

1. 将赛题放入 `problem_files/`
2. 说"开始生成数学建模论文"
3. 按照提示逐步完成

### 口令速查

```bash
# 审题选模
审题 / 选模 / 推荐模型

# 生成代码
生成代码 / 写代码

# 运行代码
运行算法 / 执行代码

# 生成图示
画图 / 流程图 / 函数图 / 网络图

# 审论文
打分 / 审稿 / 严格打分 / 审论文

# 准备答辩
准备答辩 / 模拟答辩 / 答辩练习

# 生成提交包
生成提交包

# 润色论文
润色 / 改写 / polish / 换个说法

# 降AI味
降AI味 / 降重 / 去AI检测
```

---

## 七、设计理念

> **"AI owns mechanical correctness; the user owns modeling judgment."**

- **门禁驱动**：每个阶段有明确的通过条件
- **数字冻结**：论文数字追溯到冻结快照
- **审计独立**：三个审计者互相制衡
- **用户决策**：关键判断必须用户填写理由
- **PoC验证**：每个方法必须在真实数据上运行
- **自动归档**：淘汰方法自动归档不干扰
- **质量检查**：图表自动render_check

---

**系统版本**: v3.6
**更新时间**: 2026-06-21
