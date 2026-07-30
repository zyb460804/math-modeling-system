# GitHub 数学建模 Skill 与项目调研报告

> **调研时间**: 2026-06-20
> **调研目标**: 寻找可优化当前系统的 GitHub 项目和 Skill

---

## 一、核心发现：高价值数学建模 Skill

### 1. zhnnky329/MathModeling-skills ⭐191

**URL**: https://github.com/zhnnky329/MathModeling-skills

**核心理念**: "AI owns mechanical correctness; the user owns modeling judgment"

**28个Skill结构**:

| 阶段 | Skill | 功能 |
|------|-------|------|
| 基础 | workflow-orchestrator | 会话状态跟踪、门禁检查 |
| 基础 | problem-parser | 题意解析→目标/对象/约束/数据/输出 |
| 基础 | problem-classifier | 子问题任务类型标注 |
| 基础 | symbol-table-builder | 统一符号表维护 |
| 基础 | model-assumptions-builder | 必要假设 vs 简化假设分离 |
| 基础 | data-auditor-cleaner | 数据审计+清洗+原始数据只读保护 |
| 选模 | method-selector | 2-4候选方法+≤30行PoC+真实数据验证 |
| 选模 | decision-prompt-builder | 决策点2-3个权衡问题（用户决定） |
| 选模 | modeler-decision-logger | 用户决策追加日志 |
| 代码 | model-code-analyzer | 实验布局规划 |
| 代码 | python-model-code-generator | Python代码生成（固定SEED=2026） |
| 代码 | matlab-model-code-generator | MATLAB代码生成 |
| 代码 | code-reviewer | 代码审查路由 |
| 代码 | python-code-reviewer | ≥5项具体检查+file:line引用 |
| 结果 | result-report-generator | 多方法对比报告 |
| 结果 | robustness-checker | 灵敏度/误差/基线对比（≥5项检查） |
| 结果 | final-method-explainer | 方法完整解释 |
| 结果 | figure-table-planner | 图表4类规划（诊断/对比/论文/附录） |
| 结果 | math-figure-generator | matplotlib图表+render_check验证 |
| 结果 | solution-package-builder | frozen_numbers.json冻结数字 |
| 论文 | paper-section-writer | 分段写作+字数下限+≥3讨论维度 |
| 论文 | paper-polisher | 时态/措辞/公式一致性检查 |
| 论文 | reference-manager | BibTeX生成+引用真实性验证 |
| 审计 | consistency-auditor | 数字/文件名/符号交叉一致性 |
| 审计 | completeness-auditor | 审查文件存在性+质量检查 |
| 审计 | quality-assurance-auditor | 工作流完整性+反编造检查 |

**6道门禁（Gate）设计**:

```
G1: PROBLEM_PARSED      → 题意解析完成
G2: METHOD_VALIDATED ★  → PoC在真实数据上运行成功
G2.5: CHOSEN_BY_HUMAN 👤 → 用户选择方法+写理由（非AI代写）
G3: CODE_REVIEWED       → 代码审查文件落盘
G4: RESULTS_FROZEN ★    → frozen_numbers.json冻结
G4.5: JUDGED_BY_HUMAN 👤 → 用户判断结果+稳定性
G5: PAPER_SECTION_READY → 论文分段完成
G6: AUDIT_LAYER_PASSED  → 三审计层全部通过
```

**可借鉴的关键设计**:
1. **frozen_numbers.json** - 数字冻结机制，防止代码修复后论文数字过时
2. **PoC验证** - 每个候选方法必须有≤30行PoC在真实数据上运行
3. **三审计层** - consistency + completeness + quality 三个独立审计
4. **用户决策门禁** - G2.5和G4.5必须用户填写理由，不能AI代写
5. **REJECTED自动归档** - 淘汰方法自动移入workspace/archived/
6. **原始数据只读** - data_raw/ 通过settings.json deny保护

---

### 2. handsomeZR-netizen/mathmodel-skill ⭐111

**URL**: https://github.com/handsomeZR-netizen/mathmodel-skill

**核心特色**:
- **10阶段工程化流程** - 从选题到提交的完整管道
- **全程问答式（Friendly Mode）** - 用户输入1-4编号即可推进
- **harness-agnostic** - 同时支持Claude Code和Codex，状态文件互通
- **4层反馈机制** - 跨阶段一致性回检
- **竞赛特化层** - CUMCM/MCM/电工杯分别有：

| 竞赛 | 蒸馏内容 |
|------|---------|
| CUMCM | 91篇真国赛2023-2025获奖论文自动烘焙 |
| MCM/ICM | COMAP公开scoring rubric + Outstanding Winner模式 |
| 电工杯 | 历年题量 + 公开评审标准估算 |

**竞赛特化文件**:
- `winning_patterns.md` - 获奖模式
- `phrase_bank.md` - 高频句式库
- `anti_patterns.md` - 32条反模式
- `distilled_*.md` - 段落/命名/结构/格式蒸馏
- `empirical.json` - p25/p50/p75实测分位
- `abstract_template.md` - 5段式+完整示例
- `paper_skeleton.md` - 22-25页骨架

**可借鉴的关键设计**:
1. **实测分位锚定打分** - 基于91篇真论文的p25/p50/p75数据
2. **竞赛特化句式库** - phrase_bank.md高频句式供模仿
3. **反模式库** - anti_patterns.md 32条常见错误
4. **跨harness状态互通** - decision_log.json跨工具共享
5. **问答式交互** - 降低使用门槛

---

### 3. Imbad0202/academic-research-skills ⭐33215

**URL**: https://github.com/Imbad0202/academic-research-skills

**核心价值**: 学术研究全流程skill套件，v3.13.0

**关键模块**:
- `academic-paper` - 论文写作
- `academic-paper-reviewer` - 论文评审
- `academic-pipeline` - 研究管道
- `deep-research` - 深度研究

**可借鉴的设计**:
1. **7-mode blocking checklist** - AI研究失败模式检查清单
2. **Style Calibration** - 从用户过往作品学习写作风格
3. **Writing Quality Check** - 检测机器生成痕迹
4. **trust-chain frontmatter** - 引用来源溯源
5. **locator infrastructure** - 三层引用锚点

---

## 二、Claude Code Skill 生态系统

### 4. ComposioHQ/awesome-claude-skills ⭐65390

**URL**: https://github.com/ComposioHQ/awesome-claude-skills

Claude Skills精选列表，包含大量可参考的skill设计模式。

### 5. sickn33/antigravity-awesome-skills ⭐41273

**URL**: https://github.com/sickn33/antigravity-awesome-skills

1600+可安装agentic skills，涵盖Claude Code、Cursor、Codex CLI等。

### 6. affaan-m/ECC ⭐219035

**URL**: https://github.com/affaan-m/ECC

Claude Code性能优化系统，包含skills、instincts、memory、security等模块。

---

## 三、数学建模资源库

### 7. personqianduixue/Math_Model ⭐4575

**URL**: https://github.com/personqianduixue/Math_Model

数学建模全资源库，包含：
- LaTeX模板（国赛/美赛）
- mathorcup、电工杯等竞赛资料
- MATLAB代码

### 8. hacheyz/PMMAA ⭐407

**URL**: https://github.com/hacheyz/PMMAA

Python数学建模算法应用，持续更新的算法库。

### 9. Lanrzip/Mathematical-Modeling ⭐495

**URL**: https://github.com/Lanrzip/Mathematical-Modeling

数学建模模型集+Python实现。

---

## 四、优化建议：可引入的关键机制

### 优先级 P0（必须引入）

#### 1. frozen_numbers.json 数字冻结机制

**来源**: zhnnky329/MathModeling-skills

**当前问题**: 代码修复后，论文中的数字可能过时

**解决方案**:
```json
// paper_output/results/frozen_numbers.json
{
  "Q1": {
    "main_result": 0.847,
    "source_script": "code/Q1/modeling.py",
    "source_run": "results/Q1/experiments/round2/run_summary.json",
    "frozen_at": "2026-06-20T14:30:00Z",
    "change_log": []
  }
}
```

**实现要点**:
- 代码运行后自动提取关键数字
- 论文写作时只能引用frozen_numbers.json中的数字
- 修改数字必须记录变更日志并重新冻结

#### 2. PoC验证门禁（Gate G2）

**来源**: zhnnky329/MathModeling-skills

**当前问题**: 选模阶段可能选择理论上可行但实际跑不通的方法

**解决方案**:
- 每个候选方法必须有≤30行PoC代码
- PoC必须在真实清洗数据上运行并产出具体结果
- PoC失败的方法标记[REJECTED]并归档

#### 3. 三审计层（Gate G6）

**来源**: zhnnky329/MathModeling-skills

**当前问题**: 单一QA可能遗漏问题

**解决方案**:
```
审计层1: consistency-auditor - 数字/文件名/符号交叉一致性
审计层2: completeness-auditor - 审查文件存在性+质量
审计层3: quality-assurance-auditor - 工作流完整性+反编造
三者全部PASS才能提交
```

---

### 优先级 P1（强烈建议引入）

#### 4. 竞赛特化句式库

**来源**: handsomeZR-netizen/mathmodel-skill

**实现**:
```
outputs/
├── phrase_bank.md          # 高频句式库
├── winning_patterns.md     # 获奖模式
├── anti_patterns.md        # 反模式库
└── empirical.json          # 实测分位数据
```

#### 5. 用户决策门禁（Gate G2.5 / G4.5）

**来源**: zhnnky329/MathModeling-skills

**设计理念**: "AI owns mechanical correctness; the user owns modeling judgment"

**实现**:
- 选模决策必须用户填写理由
- 结果判断必须用户确认
- 空白或AI代写的理由会导致门禁失败

#### 6. 原始数据只读保护

**来源**: zhnnky329/MathModeling-skills

**实现**:
```json
// .claude/settings.json
{
  "permissions": {
    "deny": ["Write:data_raw/*", "Edit:data_raw/*"]
  }
}
```

---

### 优先级 P2（建议引入）

#### 7. 图表render_check验证

**来源**: zhnnky329/MathModeling-skills

**检查项**:
- 文字重叠检测
- 超出画布检测
- 字体小于6.5pt检测

#### 8. 决策追加日志

**来源**: zhnnky329/MathModeling-skills

**实现**: modeler-decision-logger记录所有用户决策，论文中的"为什么选这个方法"必须追溯到此日志

#### 9. 跨阶段一致性回检

**来源**: handsomeZR-netizen/mathmodel-skill

**实现**: 4层反馈机制，每个阶段完成后自动检查与前序阶段的一致性

---

## 五、可直接复用的Skill

### 从 zhnnky329/MathModeling-skills 引入

| Skill | 用途 | 引入方式 |
|-------|------|---------|
| robustness-checker | 灵敏度/误差/基线对比 | 直接复用 |
| symbol-table-builder | 统一符号表 | 直接复用 |
| consistency-auditor | 数字一致性审计 | 直接复用 |
| completeness-auditor | 文件完整性审计 | 直接复用 |

### 从 handsomeZR-netizen/mathmodel-skill 引入

| 资源 | 用途 | 引入方式 |
|------|------|---------|
| empirical.json | 实测分位数据 | 直接复用 |
| phrase_bank.md | 高频句式库 | 直接复用 |
| anti_patterns.md | 反模式库 | 直接复用 |
| abstract_template.md | 摘要模板 | 直接复用 |

### 从 Imbad0202/academic-research-skills 引入

| 模块 | 用途 | 引入方式 |
|------|------|---------|
| academic-paper-reviewer | 论文评审 | 参考设计 |
| deep-research | 深度研究 | 参考设计 |

---

## 六、实施路线图

### Phase 1: 核心机制引入（1-2天）

1. 引入 frozen_numbers.json 机制
2. 引入 PoC 验证门禁
3. 引入三审计层设计
4. 引入原始数据只读保护

### Phase 2: 竞赛特化（2-3天）

1. 构建国赛句式库
2. 构建反模式库
3. 构建实测分位数据
4. 优化摘要模板

### Phase 3: Skill增强（3-5天）

1. 引入 robustness-checker
2. 引入 consistency-auditor
3. 引入 completeness-auditor
4. 优化图表render_check

### Phase 4: 持续优化

1. 收集真论文数据构建empirical.json
2. 持续更新句式库和反模式库
3. 优化用户决策交互体验

---

## 七、总结

**最有价值的3个项目**:

1. **zhnnky329/MathModeling-skills** - 28个skill + 6道门禁 + 三审计层，设计最完整
2. **handsomeZR-netizen/mathmodel-skill** - 竞赛特化 + 实测分位 + 问答式交互
3. **Imbad0202/academic-research-skills** - 学术写作全流程 + 引用真实性验证

**核心借鉴理念**:

> "AI owns mechanical correctness; the user owns modeling judgment."
> "每个数字必须追溯到一个冻结快照，每个审查者必须留下磁盘文件，没有skill能自己标记为'完成'。"

这些项目的核心设计思想是：**门禁驱动、数字冻结、审计独立、用户决策**。引入这些机制可以显著提升当前系统的可靠性和竞赛实战价值。
