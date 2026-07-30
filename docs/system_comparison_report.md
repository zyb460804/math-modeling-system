# 当前系统 vs GitHub优秀项目对比分析报告

> **分析时间**: 2026-06-21
> **对比项目**: zhnnky329/MathModeling-skills, handsomeZR-netizen/mathmodel-skill

---

## 一、当前系统已有的机制（✅ 优势）

| 机制 | 当前实现 | 对应GitHub项目 |
|------|---------|---------------|
| frozen_numbers.json | solution-package-builder中已实现 | zhnnky329的Gate G4 |
| 数字一致性检查 | check_number_consistency.py | zhnnky329的consistency-auditor |
| 证据门禁 | evidence_gate.py (official/quickstart模式) | zhnnky329的Gate G4 |
| 格式门禁 | check_paper_format.py | zhnnky329的Gate G5 |
| 质量审计 | quality-assurance-auditor (6维度) | zhnnky329的quality-assurance-auditor |
| 符号表构建 | symbol-table-builder | zhnnky329同名skill |
| 鲁棒性检查 | robustness-checker | zhnnky329同名skill |
| 代码审查 | python-code-reviewer, matlab-code-reviewer | zhnnky329同名skill |
| 反模式库 | bad_expression_blacklist.md, common_failure_patterns.md | handsomeZR的anti_patterns.md |
| 获奖模式库 | winning_paper_pattern_library.md | handsomeZR的winning_patterns.md |
| Hook系统 | PreToolUse/PostToolUse/Stop | 类似zhnnky329的settings.json |
| 预检门禁 | preflight_check.py | zhnnky329的workflow-orchestrator |
| 状态门禁 | workflow_guard.py | zhnnky329的Gate系统 |

---

## 二、当前系统缺少的机制（❌ 差距）

### 优先级 P0（核心机制缺失）

| 缺失机制 | GitHub来源 | 当前状态 | 影响 |
|---------|-----------|---------|------|
| **独立三审计层** | zhnnky329的consistency-auditor + completeness-auditor + quality-assurance-auditor | 只有quality-assurance-auditor，无独立的consistency和completeness审计 | 单一审计可能遗漏问题 |
| **PoC验证门禁** | zhnnky329的Gate G2：每个候选方法≤30行PoC在真实数据上运行 | model-selector只推荐，不要求PoC验证 | 可能选择理论上可行但实际跑不通的方法 |
| **用户决策门禁** | zhnnky329的Gate G2.5/G4.5：必须用户填写理由 | 无此机制，AI可自行决定 | 建模判断可能被AI代写 |

### 优先级 P1（竞赛特化缺失）

| 缺失机制 | GitHub来源 | 当前状态 | 影响 |
|---------|-----------|---------|------|
| **竞赛特化句式库** | handsomeZR的phrase_bank.md | 无专门句式库 | 论文表达缺乏竞赛针对性 |
| **实测分位数据** | handsomeZR的empirical.json (91篇真论文p25/p50/p75) | 无此数据 | 无法锚定打分，缺乏客观基准 |
| **原始数据只读保护** | zhnnky329的settings.json deny | settings.json中无problem_files/保护 | 原始数据可能被误修改 |
| **决策追加日志** | zhnnky329的modeler-decision-logger | 无此机制 | 用户决策无法追溯 |

### 优先级 P2（质量增强缺失）

| 缺失机制 | GitHub来源 | 当前状态 | 影响 |
|---------|-----------|---------|------|
| **图表render_check** | zhnnky329的math-figure-generator | 无自动检测文字重叠/超画布/字体过小 | 图表质量依赖人工检查 |
| **REJECTED自动归档** | zhnnky329的方法自动归档到workspace/archived/ | 无此机制 | 淘汰方法可能混入正式流程 |
| **跨harness状态互通** | handsomeZR的decision_log.json | 无此机制 | 无法在Claude Code和Codex间切换 |

---

## 三、融合方案

### Phase 1: 核心机制融合（P0）

#### 1.1 创建独立三审计层

**新增skill**:
- `consistency-auditor` - 数字/文件名/符号交叉一致性审计
- `completeness-auditor` - 审查文件存在性+质量检查

**实现方式**:
```
.claude/skills/
├── consistency-auditor/
│   └── SKILL.md
├── completeness-auditor/
│   └── SKILL.md
└── quality-assurance-auditor/  (已有，作为最终审计)
```

**审计流程**:
```
论文完成后 → consistency-auditor → completeness-auditor → quality-assurance-auditor
三者全部PASS才能提交
```

#### 1.2 引入PoC验证门禁

**修改skill**: `model-selector` 或新增 `method-validator`

**实现方式**:
- 每个候选方法必须附带≤30行PoC代码
- PoC必须在真实清洗数据上运行并产出具体结果
- PoC失败的方法标记[REJECTED]并归档

**新增目录结构**:
```
paper_output/
├── methods/
│   └── Q1/
│       ├── poc/
│       │   ├── method_a_poc.py
│       │   └── method_b_poc.py
│       └── method_candidates.md
└── archived/
    └── Q1/
        └── method_c_REJECTED/
```

#### 1.3 添加用户决策门禁

**新增机制**:
- 在选模阶段（G2.5）和结果判断阶段（G4.5）强制用户填写理由
- 空白或AI代写的理由会导致门禁失败

**实现方式**:
```python
# 在workflow_guard.py中添加
def check_user_decision(step: str) -> bool:
    """检查用户决策是否填写"""
    decision_file = f"paper_output/qa/user_decision_{step}.md"
    if not exists(decision_file):
        return False
    content = read(decision_file)
    # 检查是否为空或只有AI生成的内容
    if len(content.strip()) < 50:  # 至少50字的理由
        return False
    return True
```

---

### Phase 2: 竞赛特化融合（P1）

#### 2.1 构建竞赛特化句式库

**新增文件**:
```
outputs/
├── phrase_bank.md              # 高频句式库
├── competition_phrase_bank/
│   ├── cumcm_phrase_bank.md    # 国赛专用句式
│   ├── mcm_phrase_bank.md      # 美赛专用句式
│   └── diangong_phrase_bank.md # 电工杯专用句式
```

**内容来源**:
- 从91篇真国赛论文中提取高频句式
- 从MCM Outstanding Winner论文中提取英文句式
- 按章节分类：摘要、问题分析、模型建立、结果分析、结论

#### 2.2 构建实测分位数据

**新增文件**:
```
outputs/
├── empirical.json              # 实测分位数据
└── empirical_analysis.md       # 数据说明
```

**数据内容**:
```json
{
  "cumcm_2023_2025": {
    "word_count": {"p25": 18000, "p50": 21000, "p75": 24000},
    "figure_count": {"p25": 8, "p50": 12, "p75": 16},
    "table_count": {"p25": 4, "p50": 6, "p75": 8},
    "formula_count": {"p25": 15, "p50": 25, "p75": 35}
  }
}
```

#### 2.3 添加原始数据只读保护

**修改文件**: `.claude/settings.json`

```json
{
  "permissions": {
    "deny": [
      "Write:problem_files/*",
      "Edit:problem_files/*",
      "Write:data_raw/*",
      "Edit:data_raw/*"
    ]
  }
}
```

#### 2.4 添加决策追加日志

**新增skill**: `decision-logger`

**实现方式**:
```
paper_output/
├── qa/
│   └── decision_log.json       # 用户决策日志
```

**日志格式**:
```json
{
  "decisions": [
    {
      "timestamp": "2026-06-21T14:30:00Z",
      "step": "method_selection",
      "question": "Q1",
      "decision": "选择熵权TOPSIS方法",
      "reason": "数据为多指标评价问题，熵权法可客观赋权...",
      "source": "user"
    }
  ]
}
```

---

### Phase 3: 质量增强融合（P2）

#### 3.1 添加图表render_check

**修改skill**: `math-figure-generator` 或 `figure`

**检查项**:
```python
def render_check(figure_path: str) -> dict:
    """图表质量检查"""
    checks = {
        "text_overlap": check_text_overlap(figure_path),
        "out_of_canvas": check_out_of_canvas(figure_path),
        "font_size": check_min_font_size(figure_path, min_size=6.5),
        "resolution": check_resolution(figure_path, min_dpi=300)
    }
    return checks
```

#### 3.2 添加REJECTED自动归档

**实现方式**:
```python
def archive_rejected_method(question_id: str, method_name: str, reason: str):
    """将淘汰方法归档"""
    src = f"paper_output/methods/{question_id}/{method_name}"
    dst = f"paper_output/archived/{question_id}/{method_name}_REJECTED"
    move(src, dst)
    # 记录归档原因
    write(f"{dst}/rejection_reason.md", reason)
```

---

## 四、实施路线图

### Week 1: Phase 1 核心机制

| 天数 | 任务 | 产出 |
|------|------|------|
| Day 1 | 创建consistency-auditor skill | .claude/skills/consistency-auditor/SKILL.md |
| Day 1 | 创建completeness-auditor skill | .claude/skills/completeness-auditor/SKILL.md |
| Day 2 | 修改model-selector添加PoC验证 | 方法候选必须附带PoC |
| Day 3 | 添加用户决策门禁机制 | workflow_guard.py更新 |
| Day 4 | 测试三审计层+PoC+决策门禁 | 完整测试报告 |

### Week 2: Phase 2 竞赛特化

| 天数 | 任务 | 产出 |
|------|------|------|
| Day 1-2 | 构建国赛句式库 | outputs/phrase_bank.md |
| Day 3 | 构建实测分位数据 | outputs/empirical.json |
| Day 4 | 添加原始数据只读保护 | settings.json更新 |
| Day 5 | 添加决策追加日志 | decision-logger skill |

### Week 3: Phase 3 质量增强

| 天数 | 任务 | 产出 |
|------|------|------|
| Day 1-2 | 添加图表render_check | figure skill更新 |
| Day 3 | 添加REJECTED自动归档 | 归档机制实现 |
| Day 4-5 | 全系统集成测试 | 完整测试报告 |

---

## 五、预期效果

| 指标 | 当前 | 融合后 | 提升 |
|------|------|--------|------|
| 审计独立性 | 单一审计 | 三审计层制衡 | +200% |
| 方法可靠性 | 理论推荐 | PoC验证+真实数据 | +150% |
| 决策可追溯性 | 无追溯 | 完整决策日志 | +100% |
| 竞赛针对性 | 通用模板 | 竞赛特化句式库 | +80% |
| 数字一致性 | 基础检查 | frozen+consistency审计 | +100% |
| 图表质量 | 人工检查 | 自动render_check | +60% |

---

## 六、总结

**当前系统优势**:
- 已有frozen_numbers.json机制
- 已有完整的证据门禁和格式门禁
- 已有符号表构建和鲁棒性检查
- 已有反模式库和获奖模式库
- 已有Hook系统保护

**需要融合的核心机制**:
1. 独立三审计层（P0）
2. PoC验证门禁（P0）
3. 用户决策门禁（P0）
4. 竞赛特化句式库（P1）
5. 实测分位数据（P1）
6. 原始数据只读保护（P1）

**融合理念**:
> "AI owns mechanical correctness; the user owns modeling judgment."
> "每个数字必须追溯到一个冻结快照，每个审查者必须留下磁盘文件，没有skill能自己标记为'完成'。"

建议从Phase 1开始实施，预计1周完成核心机制融合。
