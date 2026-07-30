# outputs/knowledge_graph.md — 数学建模知识图谱

> **最后更新：2026-06-01**
> **用途：** 实体-关系图谱，支撑题型匹配、历史经验复用、跨文件导航。
> **借鉴：** Karpathy LLM Wiki（双向引用） + Garry Tan GBrain（知识图谱 + 记忆分层）

---

## 一、实体类型

| 实体 | 说明 | 示例 |
|------|------|------|
| `PROBLEM` | 赛题/任务 | 2024国赛B题、2025美赛A题 |
| `MODEL` | 建模方法 | AHP、TOPSIS、BP神经网络、灰色预测 |
| `ALGORITHM` | 具体算法实现 | 熵权法、遗传算法、蒙特卡洛 |
| `CODE` | 代码资产 | `resources/04_代码模板/` 下的文件 |
| `RESULT` | 建模结果/指标 | RMSE=0.032、一致性比率CR=0.05 |
| `TEMPLATE` | 写作/图表模板 | `outputs/writing_templates.md` |
| `PROMPT` | 提示词 | `prompts/12_select_model_route.md` |
| `RULE` | 评分/约束规则 | `outputs/scoring_rubric.md` |
| `CASE` | 历史案例 | `outputs/evaluation/` 下的案例包 |
| `SKILL` | Claude Code Skill | `.claude/skills/` 下的 SKILL.md |

---

## 二、关系类型

| 关系 | 方向 | 说明 |
|------|------|------|
| `USES_MODEL` | PROBLEM → MODEL | 赛题使用了哪个模型 |
| `USES_ALGORITHM` | MODEL → ALGORITHM | 模型依赖哪个算法 |
| `HAS_CODE` | ALGORITHM → CODE | 算法对应哪个代码文件 |
| `PRODUCES` | CODE → RESULT | 代码运行产出结果 |
| `TEMPLATE_FOR` | TEMPLATE → MODEL | 模板服务于哪个写作阶段 |
| `PROMPT_FOR` | PROMPT → SKILL | 提示词对应哪个 Skill |
| `RULE_GOVERNS` | RULE → MODEL | 规则约束哪个环节 |
| `CASE_EXEMPLIFIES` | CASE → MODEL | 案例展示了哪个模型 |
| `DEPENDS_ON` | MODEL → MODEL | 模型链依赖（A→B 表示 B 依赖 A 的输出） |
| `VALIDATES` | RESULT → MODEL | 结果验证了模型有效性 |
| `AVOIDS` | RULE → ALGORITHM | 红旗规则：该算法在此场景不应使用 |

---

## 三、核心图谱（按题型组织）

### 3.1 评价类

```
PROBLEM("评价类赛题")
  ├── USES_MODEL → MODEL("层次分析法/AHP")
  │     ├── USES_ALGORITHM → ALGORITHM("特征值法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/01_层次分析法.py")
  │     ├── VALIDATES → RESULT("一致性比率CR<0.1")
  │     └── TEMPLATE_FOR → TEMPLATE("outputs/writing_templates.md#评价类")
  │
  ├── USES_MODEL → MODEL("TOPSIS")
  │     ├── USES_ALGORITHM → ALGORITHM("熵权法") ← DEPENDS_ON ← ALGORITHM("数据标准化")
  │     │     ├── HAS_CODE → CODE("resources/04_代码模板/03_熵权法TOPSIS.py")
  │     │     └── AVOIDS → RULE("outputs/algorithm_selection_red_flags.md#熵权法")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/entropy_topsis_kmeans/")
  │
  ├── USES_MODEL → MODEL("模糊综合评价")
  │     ├── USES_ALGORITHM → ALGORITHM("隶属度函数")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/evaluation/")
  │
  └── USES_MODEL → MODEL("灰色关联分析")
        ├── USES_ALGORITHM → ALGORITHM("灰色关联系数")
        └── AVOIDS → RULE("outputs/method_misuse_alerts.md#灰色关联")
```

### 3.2 预测类

```
PROBLEM("预测类赛题")
  ├── USES_MODEL → MODEL("灰色预测GM(1,1)")
  │     ├── USES_ALGORITHM → ALGORITHM("累加生成")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/05_灰色预测.py")
  │     ├── AVOIDS → RULE("outputs/algorithm_selection_red_flags.md#灰色预测")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/grey_forecast/")
  │
  ├── USES_MODEL → MODEL("ARIMA")
  │     ├── USES_ALGORITHM → ALGORITHM("差分平稳性检验")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/06_时间序列ARIMA.py")
  │     ├── DEPENDS_ON → MODEL("回归分析")  ← 残差修正
  │     └── CASE_EXEMPLIFIES → CASE("outputs/arima/")
  │
  ├── USES_MODEL → MODEL("BP神经网络")
  │     ├── USES_ALGORITHM → ALGORITHM("反向传播")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/08_BP神经网络.py")
  │     └── AVOIDS → RULE("outputs/method_misuse_alerts.md#BP神经网络")
  │
  ├── USES_MODEL → MODEL("回归分析")
  │     ├── USES_ALGORITHM → ALGORITHM("最小二乘法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/04_多元回归.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/regression/")
  │
  └── USES_MODEL → MODEL("组合预测")
        ├── DEPENDS_ON → MODEL("灰色预测GM(1,1)")
        ├── DEPENDS_ON → MODEL("ARIMA")
        ├── DEPENDS_ON → MODEL("BP神经网络")
        └── TEMPLATE_FOR → TEMPLATE("outputs/model_chain_blueprints.md#预测组合")
```

### 3.3 优化类

```
PROBLEM("优化类赛题")
  ├── USES_MODEL → MODEL("线性规划")
  │     ├── USES_ALGORITHM → ALGORITHM("单纯形法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/09_线性规划.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/linear_programming/")
  │
  ├── USES_MODEL → MODEL("整数规划/0-1规划")
  │     ├── USES_ALGORITHM → ALGORITHM("分支定界法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/10_整数规划.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/binary_programming/")
  │
  ├── USES_MODEL → MODEL("多目标优化")
  │     ├── USES_ALGORITHM → ALGORITHM("NSGA-II")
  │     ├── USES_ALGORITHM → ALGORITHM("遗传算法")
  │     └── AVOIDS → RULE("outputs/algorithm_selection_red_flags.md#多目标")
  │
  ├── USES_MODEL → MODEL("动态规划")
  │     └── USES_ALGORITHM → ALGORITHM("Bellman方程")
  │
  ├── USES_MODEL → MODEL("图论/最短路")
  │     ├── USES_ALGORITHM → ALGORITHM("Dijkstra")
  │     ├── USES_ALGORITHM → ALGORITHM("Floyd")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/11_图论最短路.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/graph_path/")
  │
  └── USES_MODEL → MODEL("排队论/仿真")
        ├── USES_ALGORITHM → ALGORITHM("蒙特卡洛模拟")
        │     ├── HAS_CODE → CODE("resources/04_代码模板/12_蒙特卡洛.py")
        │     └── CASE_EXEMPLIFIES → CASE("outputs/monte_carlo/")
        └── CASE_EXEMPLIFIES → CASE("outputs/queue_simulation/")
```

### 3.4 分类/聚类类

```
PROBLEM("分类/聚类类赛题")
  ├── USES_MODEL → MODEL("K-Means聚类")
  │     ├── USES_ALGORITHM → ALGORITHM("肘部法则选K")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/07_KMeans聚类.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/kmeans/")
  │
  ├── USES_MODEL → MODEL("PCA降维")
  │     ├── USES_ALGORITHM → ALGORITHM("特征分解")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/02_PCA主成分.py")
  │     └── CASE_EXEMPLIFIES → CASE("outputs/pca/")
  │
  └── USES_MODEL → MODEL("决策树/随机森林")
        ├── USES_ALGORITHM → ALGORITHM("信息增益")
        └── USES_ALGORITHM → ALGORITHM("Bagging")
```

### 3.5 统计分析类

```
PROBLEM("统计分析类赛题")
  ├── USES_MODEL → MODEL("Pearson相关")
  │     ├── USES_ALGORITHM → ALGORITHM("参数估计")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/连续变量相关性分析/")
  │     ├── VALIDATES → RESULT("相关系数表")
  │     └── TEMPLATE_FOR → TEMPLATE("outputs/result_analysis_templates.md#统计分析类模板")
  │
  ├── USES_MODEL → MODEL("Spearman相关")
  │     ├── USES_ALGORITHM → ALGORITHM("显著性检验")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/连续变量相关性分析/")
  │     └── VALIDATES → RESULT("显著性p值")
  │
  ├── USES_MODEL → MODEL("卡方检验")
  │     ├── USES_ALGORITHM → ALGORITHM("残差分析")
  │     └── CASE_EXEMPLIFIES → CASE("resources/11_题型playbook/playbook-ml-regression.md")
  │
  ├── USES_MODEL → MODEL("回归分析")
  │     ├── USES_ALGORITHM → ALGORITHM("共线性检验")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/回归分析/")
  │     ├── VALIDATES → RESULT("回归方程")
  │     └── VALIDATES → RESULT("残差图")
  │
  └── RULE_GOVERNS → RULE("outputs/scoring_rubric.md（求解与算法 20 分 + 稳健性 10 分）")
```

### 3.6 机理分析类

```
PROBLEM("机理分析类赛题")
  ├── USES_MODEL → MODEL("微分方程")
  │     ├── USES_ALGORITHM → ALGORITHM("数值积分")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/14种国赛必备算法源代码/机理分析-微分方程/")
  │     ├── VALIDATES → RESULT("演化轨迹")
  │     └── TEMPLATE_FOR → TEMPLATE("outputs/result_analysis_templates.md#机理类模板")
  │
  ├── USES_MODEL → MODEL("差分方程")
  │     ├── USES_ALGORITHM → ALGORITHM("参数拟合")
  │     └── VALIDATES → RESULT("参数估计")
  │
  ├── USES_MODEL → MODEL("系统动力学")
  │     ├── USES_ALGORITHM → ALGORITHM("欧拉法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/14种国赛必备算法源代码/系统动力学/")
  │     ├── VALIDATES → RESULT("稳态分析")
  │     └── CASE_EXEMPLIFIES → CASE("resources/11_题型playbook/playbook-physics-ode.md")
  │
  └── USES_MODEL → MODEL("Logistic增长")
        ├── USES_ALGORITHM → ALGORITHM("Runge-Kutta")
        └── VALIDATES → RESULT("情景对比")

  └── RULE_GOVERNS → RULE("outputs/scoring_rubric.md（建模 20 分 + 结果分析 15 分）")
```

### 3.7 图与网络类

```
PROBLEM("图与网络类赛题")
  ├── USES_MODEL → MODEL("Dijkstra")
  │     ├── USES_ALGORITHM → ALGORITHM("最短路搜索")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/Dijkstra/")
  │     ├── VALIDATES → RESULT("最短路径")
  │     └── TEMPLATE_FOR → TEMPLATE("outputs/figure_templates.md#网络图模板")
  │
  ├── USES_MODEL → MODEL("Floyd")
  │     ├── USES_ALGORITHM → ALGORITHM("启发式搜索")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/Floyd/")
  │     └── VALIDATES → RESULT("网络指标")
  │
  ├── USES_MODEL → MODEL("TSP")
  │     ├── USES_ALGORITHM → ALGORITHM("蚁群算法")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/蚁群算法/")
  │     └── VALIDATES → RESULT("社区划分")
  │
  ├── USES_MODEL → MODEL("复杂网络指标")
  │     ├── USES_ALGORITHM → ALGORITHM("社区检测")
  │     └── VALIDATES → RESULT("关键节点")
  │
  ├── USES_MODEL → MODEL("PageRank")
  │     └── CASE_EXEMPLIFIES → CASE("resources/11_题型playbook/playbook-path-planning.md")
  │
  └── RULE_GOVERNS → RULE("outputs/scoring_rubric.md（建模 20 分 + 结果分析 15 分）")
```

### 3.8 风险预警类

```
PROBLEM("风险预警类赛题")
  ├── USES_MODEL → MODEL("Logistic回归")
  │     ├── USES_ALGORITHM → ALGORITHM("分类训练")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/KNN分类/")
  │     ├── VALIDATES → RESULT("风险分数")
  │     └── TEMPLATE_FOR → TEMPLATE("outputs/result_analysis_templates.md#风险预警类模板")
  │
  ├── USES_MODEL → MODEL("随机森林")
  │     ├── USES_ALGORITHM → ALGORITHM("阈值设定")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/KNN分类/")
  │     └── VALIDATES → RESULT("预警等级")
  │
  ├── USES_MODEL → MODEL("XGBoost")
  │     ├── USES_ALGORITHM → ALGORITHM("风险排序")
  │     └── VALIDATES → RESULT("混淆矩阵")
  │
  ├── USES_MODEL → MODEL("贝叶斯网络")
  │     ├── USES_ALGORITHM → ALGORITHM("阈值扰动")
  │     │     └── HAS_CODE → CODE("resources/04_代码模板/50多种常用算法源代码/朴素贝叶斯/")
  │     └── VALIDATES → RESULT("召回率")
  │
  ├── USES_MODEL → MODEL("评分卡")
  │     ├── USES_ALGORITHM → ALGORITHM("混淆矩阵")
  │     └── VALIDATES → RESULT("AUC")
  │
  ├── CASE_EXEMPLIFIES → CASE("resources/10_算法cookbook/cookbook-ml.md")
  │
  └── RULE_GOVERNS → RULE("outputs/scoring_rubric.md（求解与算法 20 分 + 稳健性 10 分）")
```

---

## 四、文件双向引用图

> Karpathy 风格：每个文件标注「依赖谁」和「被谁依赖」，形成可导航的拓扑。

### 系统调度层

```
task_router.md ←── INDEX.md（入口定位）
       ↓ 分流到
       ├── method_matching.md（审题阶段）
       ├── writing_templates.md（写作阶段）
       ├── scoring_rubric.md（审稿阶段）
       ├── defense_qa_bank.md（答辩阶段）
       ├── final_quality_gate.md（验收阶段）
       └── prompt_master_pack.md（赛中调度）

asset_registry.md ←→ file_map.md（互为补充）
       ↑ 登记
       ├── algorithm_templates.md
       ├── code_asset_index.md
       └── knowledge_base.md

case_feedback_loop.md ←── 每个 CASE 完成后触发
       ↓ 回灌到
       ├── knowledge_base.md（知识卡片）
       ├── bad_cases.md（反例库）
       └── method_misuse_alerts.md（误用预警）
```

### 建模选模层

```
method_matching.md（主入口）
       ├── → model_selection_flow.md（详细流程）
       ├── → model_selection_quick_table.md（速查）
       ├── → problem_type_taxonomy.md（题型识别）
       ├── → algorithm_templates.md（代码模板）
       ├── → algorithm_selection_red_flags.md（避坑）
       └── → method_misuse_alerts.md（误用预警）

model_chain_blueprints.md ←── method_matching.md 选定组合模型后
       ↓ 指导
       ├── code_template_playbook.md（代码结构）
       └── python_algorithm_template_standard.md（代码规范）

case_to_method_route_library.md ←→ outputs/ 各案例子目录
       ↑ 回灌
       └── case_feedback_loop.md
```

### 写作表达层

```
writing_templates.md（主入口）
       ├── → abstract_templates.md（摘要专项）
       ├── → section_writing_templates.md（分节模板）
       ├── → result_analysis_templates.md（结果分析）
       └── → high_score_expression_library.md（表达升级）

transition_sentence_bank.md ←── 所有写作模板的润色补丁
paper_upgrade_playbook.md ←── scoring_rubric.md 的改稿行动版
       ↓ 对照
       └── revision_checklist.md（P0/P1/P2 清单）
```

### 审稿评分层

```
scoring_rubric.md（唯一评分标准）
       ├── → review_section_checklists.md（分节审稿）
       ├── → review_priority_matrix.md（问题排序）
       ├── → paper_score_calibration_library.md（校准）
       └── → diagnostic_templates.md（诊断）

revision_checklist.md ←── scoring_rubric.md 评分后
       ↓ 执行
       └── paper_upgrade_playbook.md（改稿行动）

bad_cases.md ←→ common_failure_patterns.md（互为补充）
       ↑ 回灌
       └── case_feedback_loop.md
```

---

## 五、跨层引用关系（全局视图）

```
┌─────────────────────────────────────────────────────────┐
│                    系统调度层                              │
│  task_router → asset_registry → file_map                 │
│       ↓              ↓              ↓                    │
├───────┼──────────────┼──────────────┼────────────────────┤
│       ↓              ↓              ↓                    │
│  ┌────▼────┐   ┌────▼────┐   ┌────▼────┐               │
│  │建模选模层│──→│写作表达层│──→│审稿评分层│               │
│  └────┬────┘   └────┬────┘   └────┬────┘               │
│       ↓              ↓              ↓                    │
│  ┌────▼────┐   ┌────▼────┐   ┌────▼────┐               │
│  │数据处理层│   │图表可视层│   │答辩准备层│               │
│  └────┬────┘   └────┬────┘   └────┬────┘               │
│       ↓              ↓              ↓                    │
│  ┌────▼──────────────▼──────────────▼────┐              │
│  │            质量验收层                    │              │
│  │  evidence_gate → final_quality_gate     │              │
│  └────────────────┬──────────────────────┘              │
│                   ↓                                      │
│  ┌────────────────▼──────────────────────┐              │
│  │          案例回灌 → 知识图谱更新         │              │
│  └───────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## 六、图谱查询接口

### 快速查询模式

| 查询意图 | 图谱遍历路径 |
|----------|-------------|
| "这个题型用什么模型？" | PROBLEM → USES_MODEL → MODEL |
| "这个模型的代码在哪？" | MODEL → USES_ALGORITHM → HAS_CODE → CODE |
| "这个算法有什么坑？" | ALGORITHM → AVOIDS → RULE |
| "历史上有类似案例吗？" | PROBLEM → USES_MODEL → CASE_EXEMPLIFIES → CASE |
| "组合模型怎么串？" | MODEL → DEPENDS_ON → MODEL → model_chain_blueprints.md |
| "结果能验证模型吗？" | RESULT → VALIDATES → MODEL |
| "这个模板服务哪个阶段？" | TEMPLATE → TEMPLATE_FOR → MODEL → PROBLEM |

### 脚本查询

```bash
# 查找某个模型的所有关联实体
python outputs/scripts/knowledge_graph_query.py --model "TOPSIS"

# 查找某个题型的完整建模路径
python outputs/scripts/knowledge_graph_query.py --problem-type "评价类"

# 查找某个算法的红旗规则
python outputs/scripts/knowledge_graph_query.py --algorithm "熵权法" --red-flags
```

---

## 七、维护规则

1. **新增实体**：在本文件对应章节添加，同时更新 `asset_registry.md`
2. **新增关系**：在第二节关系类型中定义，在第三节图谱中实例化
3. **双向一致性**：A→B 的关系，B 的条目中必须有 ←A 的反向引用
4. **定期审查**：每次竞赛结束后，用 `case_feedback_loop.md` 的回灌结果更新图谱
