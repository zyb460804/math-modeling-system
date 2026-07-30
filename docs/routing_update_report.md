# 路由更新完成报告

> **更新时间**: 2026-06-21
> **系统版本**: v3.7

---

## 一、已更新的路由

### 1. settings.json 注册 ✅

新skill已注册到 `.claude/settings.json`：

| Skill | 名称 | 描述 |
|-------|------|------|
| `feature-engineering` | 特征工程 | 数据预处理、转换、编码、缩放、特征选择 |
| `algorithm-benchmark` | 算法基准测试 | 比较不同算法性能、精度、速度 |
| `style-calibration` | 写作风格校准 | 从用户过往作品学习写作风格 |
| `citation-tracer` | 引用溯源 | 验证引用真实性、追踪引用来源 |
| `ai-failure-checker` | AI失败模式检查 | 7-mode blocking checklist |

### 2. CLAUDE.md 触发词映射 ✅

新增触发词：

| 触发词 | 路由Skill |
|--------|----------|
| 特征工程 / feature engineering | `feature-engineering` |
| 算法基准测试 / benchmark | `algorithm-benchmark` |
| 论文检索 / search papers | `tools/paper_search/scripts/search_papers.py` |
| 写作风格校准 / style calibration | `style-calibration` |
| 引用溯源 / citation check | `citation-tracer` |
| AI失败模式检查 / AI failure check | `ai-failure-checker` |
| 一致性审计 / consistency audit | `consistency-auditor` |
| 完整性审计 / completeness audit | `completeness-auditor` |
| 记录决策 / log decision | `decision-logger` |

### 3. 阶段路由表更新 ✅

`paper-workflow-orchestrator` 路由表已更新：

| 当前目标 | 优先调用 |
|---------|---------|
| 需要特征工程 | `feature-engineering` |
| 需要比较不同算法性能 | `algorithm-benchmark` |
| 需要检查AI生成内容的失败模式 | `ai-failure-checker` |
| 需要校准写作风格 | `style-calibration` |
| 需要验证引用真实性 | `citation-tracer` |
| 需要一致性审计 | `consistency-auditor` |
| 需要完整性审计 | `completeness-auditor` |
| 需要记录用户决策 | `decision-logger` |

---

## 二、可调用的命令

### 直接触发词

```bash
# 特征工程
特征工程
feature engineering

# 算法基准测试
算法基准测试
benchmark

# 论文检索
论文检索
search papers

# 写作风格校准
写作风格校准
style calibration

# 引用溯源
引用溯源
citation check

# AI失败模式检查
AI失败模式检查
AI failure check

# 一致性审计
一致性审计
consistency audit

# 完整性审计
完整性审计
completeness audit

# 记录决策
记录决策
log decision
```

### 脚本调用

```bash
# 特征工程
python .claude/skills/feature-engineering/scripts/preprocess.py --input data.csv --target y

# 算法基准测试
python .claude/skills/algorithm-benchmark/scripts/benchmark_evaluation.py --input data.csv

# 论文检索
python tools/paper_search/scripts/search_papers.py --query "TOPSIS" --source semantic_scholar

# AI失败模式检查
python .claude/skills/ai-failure-checker/scripts/check_failures.py --paper paper.md

# 一致性审计
python .claude/skills/consistency-auditor/scripts/audit.py

# 完整性审计
python .claude/skills/completeness-auditor/scripts/audit.py

# 记录决策
python .claude/skills/decision-logger/scripts/log.py add --gate G2.5 --question Q1 --decision "..." --reason "..."
```

---

## 三、完整工作流（v3.7）

```
S0. 预检
    ↓
S1. 题意解析
    ↓
S2. 模型路线 + PoC验证（Gate G2）
    ↓
    用户决策（Gate G2.5）← decision-logger
    ↓
S3. 数据处理 + 特征工程 ← feature-engineering
    ↓
S4. 代码运行 + 算法基准测试 ← algorithm-benchmark
    ↓
S5. 结果验证 + 数字冻结（Gate G4）
    ↓
    用户决策（Gate G4.5）← decision-logger
    ↓
S6. 图表生成 + render_check + 论文写作
    ↓
    写作风格校准 ← style-calibration
    ↓
    引用溯源 ← citation-tracer
    ↓
    AI失败模式检查 ← ai-failure-checker
    ↓
S7. 三审计层
    ├─ 一致性审计 ← consistency-auditor
    ├─ 完整性审计 ← completeness-auditor
    └─ 质量审计 ← quality-assurance-auditor
    ↓
S8. 最终提交
```

---

## 四、总结

所有新创建的skill已完成路由更新：

| 更新项 | 状态 |
|--------|------|
| settings.json 注册 | ✅ |
| CLAUDE.md 触发词映射 | ✅ |
| 阶段路由表更新 | ✅ |
| 工作流文档更新 | ✅ |

**现在所有新skill都可以被调用了** 🎉

---

**路由更新完成** ✅
