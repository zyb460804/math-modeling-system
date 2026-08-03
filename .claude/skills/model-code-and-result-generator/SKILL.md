---
name: model-code-and-result-generator
description: "根据 model_route.json、数据计划和清洗数据，为数学建模论文生成结果证据契约和 q1/q2/q3 建模代码脚手架。Invoke when 需要把模型输出、评价指标、结构化结论、论文表格和当前赛题专用建模代码沉淀到 paper_output/results/、paper_output/tables/ 和 paper_output/code/modeling/，供 QA 与正文生成读取。触发词：建模代码、模型代码、生成代码、结果契约、model_results、评价指标生成、conclusions、建模脚本。"
---

# 建模代码与结果证据生成器

## 目标

本 skill 不是万能自动建模系统。它的作用是给 Agent 一个稳定的“结果证据层”和可运行的赛题专用建模代码起点，避免正文只根据模型路线空写，也避免 Agent 面对数据时无头乱转。

真实赛题中，Agent 必须根据 `model_route.json`、数据字段、题目约束和评分要求二次修改生成的 `q*_model.py`。生成代码固定放在 `paper_output/code/modeling/`，不要写回 skill 包的 `scripts/`。

## 执行契约

- 上游输入：优先读取 `paper_output/plan/model_route.json`、`data_plan.json`、`visualization_plan.json`，并扫描 `paper_output/data_cleaned/`。
- 必须输出：`paper_output/results/model_results.json`、`metrics.json`、`conclusions.json`、`paper_output/tables/table_index.json`、`paper_output/tables/*.csv`。
- 建模代码输出：`paper_output/code/modeling/result_contract_io.py`、`run_modeling.py`、`q1_model.py`、`q2_model.py`、`q3_model.py` 或与 `question_id` 对应的 `q*_model.py`。
- 下游交接：`quality-assurance-auditor` 读取结果与表格证据后写入 `tasks.json`；`paper-micro-unit-generator` 通过任务清单引用结果、指标、表格和结论。
- 失败回退：如果没有清洗数据或真实建模代码，仍生成契约骨架，并用 `needs_real_modeling` 标记，不伪装成最终比赛结果。

## 脚本

- `scripts/build_result_contracts.py`
  - 何时用：已有模型路线，需要生成结果契约、表格索引和当前赛题的 q1/q2/q3 建模代码。
  - 做什么：
    1. **★ 智能算法选择器**：读取 `references/algorithm_registry.json`，根据 `model_route.json` 中每问的 `main_model` 关键词匹配真实算法代码文件（49 种算法）。
    2. 匹配成功 → 生成 wrapper 脚本调用真实算法代码，status = `"computed"`。
    3. 匹配失败 → 回退到 7 种脚手架（预测/优化/评价/分类/聚类/仿真/通用），status = `"scaffold_result_needs_review"`。
    4. 生成结果契约、表格索引、`paper_output/code/modeling/README.md`。
  - 覆盖规则：生成文件带有 managed marker；如果 Agent 已经手工改写并去掉 marker，本脚本会保留用户文件，不覆盖。
- `scripts/result_contract_templates.py`
  - 何时用：需要了解不同任务类型应沉淀哪些指标、表格和结论字段。
  - 做什么：提供预测、优化、评价、分类、聚类、仿真、通用建模的契约模板。
- `references/algorithm_registry.json`
  - 何时用：`build_result_contracts.py` 自动读取，无需手动调用。
  - 做什么：定义 49 种算法的 id、display_name、task_type、keywords、file_path、function_name、imports、pip_packages。算法选择器通过 keywords 匹配 `main_model` 字段，找到对应的代码文件路径。

## ★ 项目知识资产联动（必须执行）
本 skill 执行时，**必须**读取以下 `outputs/` 和 `resources/` 中已沉淀的规则，作为代码生成和结果契约的权威依据：

| 资产 | 路径 | 用途 |
|------|------|------|
| 算法模板库 | `outputs/algorithm_templates.md` | 按题型的算法代码模板 |
| 代码模板说明书 | `outputs/code_template_playbook.md` | 代码结构、参数、复用说明 |
| 14种必备算法 | `resources/04_代码模板/14种必备算法/` | Python/Matlab 源代码 |
| 50种扩展算法 | `resources/04_代码模板/50种算法/` | 按题型分类的算法代码 |
| 创新型算法 | `resources/04_代码模板/创新型算法/` | 组合/创新算法代码 |

**执行规则**：
1. 生成 `q*_model.py` 前，必须先查 `outputs/algorithm_templates.md` 确认该题型的标准算法代码结构
2. 优先复用 `resources/04_代码模板/` 中已有的算法代码，而非从零编写
3. 生成的代码必须标注"可运行"与"待补"部分，不得伪装成完整可运行代码

## 领域知识库（v4.0 新增）

本 skill 通过 `references/` 下的 8 本领域 cookbook 为代码生成提供领域专用的算法模板、参数调优经验和常见陷阱说明。`build_result_contracts.py` 在生成 `q*_model.py` 时，根据 `model_route.json` 中每问的 `main_model` 或 `task_type` 字段自动路由到对应的 cookbook，作为代码生成的领域上下文注入。

### Cookbook 路由规则

| 问题类型 | 路由关键词（`main_model` / `task_type`） | Cookbook 文件 | 覆盖算法 |
|---------|----------------------------------------|-------------|---------|
| 优化问题 | 优化、规划、调度、选址、路径、GA、PSO、SA、LP、DP、遗传、粒子群、退火 | `references/cookbook-optimization.md` | GA / PSO / SA / LP / DP |
| 预测/ML | 预测、回归、机器学习、XGBoost、随机森林、SVM、神经网络、分类预测 | `references/cookbook-ml.md` | XGBoost / RF / SVM / NN |
| 评价/决策 | 评价、排序、权重、TOPSIS、AHP、熵权、模糊、多准则 | `references/cookbook-evaluation.md` | TOPSIS / AHP / 熵权法 / 模糊综合评价 |
| 机理/物理 | 机理、传热、ODE、微分方程、物理、光学、几何、动力学 | `references/cookbook-mechanistic.md` | 传热模型 / ODE / 几何光学 |
| 统计分析 | 统计、假设检验、ANOVA、蒙特卡洛、贝叶斯、方差分析、显著性 | `references/cookbook-statistical.md` | 假设检验 / ANOVA / 蒙特卡洛 / 贝叶斯 |
| 图/网络 | 图论、网络流、最短路、中心性、Dijkstra、Floyd、网络优化 | `references/cookbook-network.md` | 图论 / 网络流 / 中心性分析 |
| 聚类/分类 | 聚类、分类、K-Means、层次聚类、DBSCAN、GMM、分群 | `references/cookbook-clustering.md` | 层次聚类 / K-Means / DBSCAN / GMM |
| 博弈/策略 | 博弈、纳什、演化、Stackelberg、策略、竞争、均衡 | `references/cookbook-game-theory.md` | 纳什均衡 / 演化博弈 / Stackelberg |

### 执行规则

1. **路由优先级**：先匹配 `task_type`，再匹配 `main_model` 关键词；命中多个 cookbook 时全部加载，由 Agent 合并上下文。
2. **与 algorithm_registry.json 的关系**：`algorithm_registry.json` 负责算法代码文件的精确匹配（49 种）；cookbook 负责提供该算法的领域背景、参数调优经验和常见陷阱。两者互补，不冲突。
3. **加载时机**：在 `build_result_contracts.py` 匹配到算法后、生成 `q*_model.py` 代码之前，读取对应 cookbook 作为领域上下文。
4. **兜底逻辑**：如果 `main_model` 关键词未命中任何 cookbook，回退到脚手架回退逻辑（见下方），不强制加载。

### 参考文档（references/）

| 文件 | 用途 |
|------|------|
| `references/heuristic-algo-scikit-opt.md` | scikit-opt（sko）7 种启发式算法（DE/GA/PSO/SA/ACA/IA/AFSA）桥接指南：`pip install scikit-opt` 一行调用拿 baseline，含选型建议（scikit-opt 做 baseline+快速出结果 vs cookbook-optimization.md 做创新+可定制）、7 个最小示例、与手写 NSGA-II/CVaR/SA 大地距离模板的分工 |

## 任务类型分发

### ★ 智能算法选择（优先）

`build_result_contracts.py` 会先查 `references/algorithm_registry.json`，根据 `main_model` 关键词匹配真实算法。覆盖 49 种算法，按 task_type 分组：

| task_type | 可匹配算法 |
|-----------|-----------|
| evaluation | TOPSIS、熵权法、AHP、DEA、灰色关联、模糊综合评价、神经网络评价、秩和比 |
| forecasting | ARIMA、灰色预测、Logistic、BP神经网络、回归分析、指数平滑、高斯回归、马尔可夫、随机森林、XGBoost、Prophet、移动平均、季节指数 |
| classification | 随机森林、LightGBM、KNN、决策树、朴素贝叶斯 |
| clustering | K-Means、层次聚类、GMM、SOM |
| optimization | 线性规划、整数规划、0-1规划、非线性规划、多目标规划、遗传算法、PSO、蚁群、模拟退火、NSGA-II、动态规划、最速下降法 |
| simulation | 微分方程、SIR模型、人口模型、战争模型 |
| preprocessing | PCA、IQR异常检测 |
| graph | Dijkstra、Floyd |

### 脚手架回退（智能选择失败时）

- 预测/回归/时间序列 -> forecasting scaffold：生成目标列、特征列、预测值、残差、RMSE、MAE、MAPE。
- 优化/规划/调度/选址/路径 -> optimization scaffold：生成代理目标函数、方案排序、约束满足率待补项。
- 评价/排序/权重/TOPSIS/AHP/熵权 -> evaluation scaffold：生成指标归一化、综合得分、排序和权重敏感性待补项。
- 分类/识别/判别 -> classification scaffold：生成代理分类标签、准确率/F1 待补项。
- 聚类/分群 -> clustering scaffold：生成代理聚类标签、聚类数、簇内紧凑度。
- 仿真/机理/动力学/微分 -> simulation scaffold：生成趋势代理、情景结果、拟合误差和敏感性参数。
- 其他 -> general scaffold：生成数值字段统计摘要和通用结果表。

## 输出位置

```text
paper_output/
|-- code/
|   `-- modeling/
|       |-- run_modeling.py
|       |-- result_contract_io.py
|       |-- q1_model.py
|       |-- q2_model.py
|       |-- q3_model.py
|       `-- README.md
|-- results/
|   |-- model_results.json
|   |-- metrics.json
|   `-- conclusions.json
`-- tables/
    |-- table_index.json
    |-- table_q1_result_skeleton.csv
    |-- table_q1_forecasting_scaffold.csv
    `-- ...
```

统一规则：

- 所有路径使用相对路径。
- 所有 JSON 包含 `schema_version`、`generated_by`、`generated_at`。
- 每条结果、指标、结论和表格都应带 `question_id`。
- 草稿或脚手架结果必须使用 `status` 或 `evidence_status` 标记。
- 正式结果必须带 `execution_provenance`，包含 `source_code_path`、`run_command`、`run_exit_code` 和 `output_artifacts`；official evidence gate 会拒绝没有真实代码运行来源的结果。
- 正文中引用的表格必须能在 `paper_output/tables/table_index.json` 找到。

## 使用方式

推荐由 `paper-workflow-orchestrator` 在数据清洗与可视化之后调用。也可以手动运行：

```bash
python .claude/skills/model-code-and-result-generator/scripts/build_result_contracts.py
```

生成脚手架后，Agent 应按真实赛题执行：

```bash
python paper_output/code/modeling/run_modeling.py
```

然后重新运行 QA，让 `paper_output/tasks.json` 读取刷新后的 `model_results.json`、`metrics.json`、`conclusions.json` 和 `table_index.json`。

## 真实赛题使用原则

- 不要把占位式指标或代理结果直接当成最终比赛结果。
- 优先修改 `paper_output/code/modeling/q*_model.py`，不要修改 skill 包内的 `scripts/`。
- 正式建模完成后，必须由建模代码实际运行并把真实输出写回 `paper_output/results/` 与 `paper_output/tables/`；不要手写 `model_results.json` 冒充运行结果。
- 如果某一问没有真实结果，QA 应保留 warning，正文不得把该问写成已经完成精确计算。

## 新增脚本（v4.2/v4.3）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/verification_template.py` | G4.6 强制自证：为每个 `modeling/*.py` 生成配对的 `verifications/verify_*.py` 骨架 | "生成自证脚本" / "G4.6" |
| `scripts/optuna_tune.py` | Optuna 超参自动调优（TPE 贝叶斯优化，XGBoost/LightGBM/RF/SVR）+ 可视化 | "超参调优" / "调参" / "Optuna" |

ML/优化题用 Optuna 替代网格搜索，论文写"贝叶斯优化（TPE）"更专业。`pip install optuna`。
