# GitHub 15 仓库融合方案

> 生成日期：2026-06-21
> 融合来源：15 个 GitHub math-modeling 仓库（总 Stars 3,300+）

---

## 一、差距分析

### 当前系统已覆盖（63 skills）

| 能力 | 现有 Skill | 覆盖度 |
|------|-----------|--------|
| 工作流编排 | paper-workflow-orchestrator | ★★★★ |
| 题意解析 | problem-doc-model-selector | ★★★★ |
| 选模 | model-selector, modeling-paper-rubric-and-model-selector | ★★★★ |
| 代码生成 | model-code-and-result-generator, matlab-model-code-generator | ★★★★ |
| 论文写作 | paper-formal-writer, paper-micro-unit-generator | ★★★★ |
| 质量审计 | consistency-auditor, completeness-auditor, quality-assurance-auditor | ★★★★★ |
| 图表 | math-figure, figure, chart-recommender, diagram-maker | ★★★★ |
| 答辩 | defense, defense-simulator | ★★★★ |
| 符号表 | symbol-table-builder | ★★★★ |
| 稳健性 | robustness-checker | ★★★★ |
| 降AIGC | humanizer-zh-academic, aigc-reduce | ★★★★ |

### 当前系统缺失（需融合）

| 缺失能力 | 来源仓库 | 优先级 |
|----------|---------|--------|
| **Model Contract（前置合同）** | XiaoMaColtAI | P0 |
| **Figure Contract（图表合同）** | XiaoMaColtAI | P0 |
| **95+场景选型矩阵** | Lupynow | P0 |
| **8个领域Cookbook** | Lupynow | P0 |
| **12个端到端Playbook** | Lupynow | P1 |
| **门控架构 G1-G6** | zhnnky329 | P0 |
| **frozen_numbers.json 冻结机制** | zhnnky329 | P0 |
| **PoC验证门禁（≤30行）** | zhnnky329 | P0 |
| **Anti-AI-detection写作** | XiaoMaColtAI + Lupynow | P1 |
| **4轮自审框架** | XiaoMaColtAI + Lupynow | P1 |
| **双引擎文献搜索** | XiaoMaColtAI | P1 |
| **证据金字塔** | XiaoMaColtAI | P1 |
| **问题分解12型分类** | Lupynow | P1 |
| **Solver→Paper桥接** | Lupynow | P1 |
| **反同质化设计** | Lupynow | P2 |
| **MCM Memo/Letter模板** | Lupynow | P2 |
| **中英翻译工作流** | XiaoMaColtAI | P2 |
| **新算法模板（19个）** | 多仓库 | P1 |
| **O奖论文库（100+篇）** | HeXavi8 + MathematicalModeling | P1 |
| **90+经典题解** | MathematicalModeling | P1 |
| **32种方法教材** | MathematicalModeling | P2 |
| **10章PPT课件** | ShituoMa | P2 |

---

## 二、融合方案（5大模块）

### 模块 1：合同体系（from XiaoMaColtAI）

**新增文件：**
```
.claude/skills/paper-workflow-orchestrator/references/
├── model-contract-template.md      ← Model Contract 模板
└── figure-contract-template.md     ← Figure Contract 模板
```

**Model Contract 核心内容：**
- 一句话核心结论
- 证据链（每个模型证明什么，反冗余原则）
- 候选评估 + 备选方案
- 下游交付规格

**Figure Contract 核心内容：**
- 图表要证明的一句话结论
- 每个面板的独特证据
- 反冗余检查（去掉任何面板是否仍能得出结论）
- 灰度安全 + 色盲无障碍审计

### 模块 2：门控架构（from zhnnky329）

**新增文件：**
```
.claude/skills/paper-workflow-orchestrator/references/
├── gate-system.md                  ← G1-G6 门控定义
├── frozen-numbers-convention.md    ← 数字冻结机制
└── poc-validation-gate.md          ← PoC 验证门禁
```

**G1-G6 门控：**
| Gate | 名称 | 载重性 |
|------|------|--------|
| G1 | PROBLEM_PARSED | 否 |
| G2 | METHOD_VALIDATED（≤30行PoC） | 是 |
| G2.5 | METHOD_CHOSEN_BY_HUMAN | 是（人工门） |
| G3 | CODE_REVIEWED | 否 |
| G4.5 | RESULTS_JUDGED_BY_HUMAN | 是（人工门） |
| G4 | RESULTS_FROZEN | 是 |
| G5 | PAPER_SECTION_READY | 否 |
| G6 | AUDIT_LAYER_PASSED | 是 |

**Frozen Numbers 机制：**
- `frozen_numbers.json` 包含 `{value, source_file, source_line, frozen_at, frozen_by_skill}`
- 修改需 3 步：记录原因 → 更新源文件 → 重新冻结
- `consistency-auditor` 检查新鲜度

### 模块 3：选型矩阵 + Cookbook（from Lupynow）

**新增文件：**
```
.claude/skills/model-selector/references/
├── model-selection-matrix.md       ← 95+场景决策矩阵
├── problem-decomposition.md        ← 12型问题分类法
└── conflict-resolution-rules.md    ← 冲突解决规则

.claude/skills/model-code-and-result-generator/references/
├── cookbook-optimization.md         ← GA/PSO/SA/LP/DP
├── cookbook-ml.md                   ← XGBoost/RF/SVM/NN
├── cookbook-evaluation.md           ← TOPSIS/AHP/熵权/模糊
├── cookbook-mechanistic.md          ← 传热/ODE/几何/光学
├── cookbook-statistical.md          ← 假设检验/ANOVA/蒙特卡洛/贝叶斯
├── cookbook-network.md              ← 图论/网络流/中心性
├── cookbook-clustering.md           ← 层次/K-Means/DBSCAN/GMM
└── cookbook-game-theory.md          ← 南什/演化/Stackelberg
```

**95+场景矩阵格式：**
```
| 场景特征 | 主模型 | 备选模型 | 边界条件 | 风险 |
```

**12型问题分类：**
评价/预测/优化/机理/分类聚类/图路由/仿真/数据分析/混合/调度/策略/环境

### 模块 4：新算法模板库（from 6个算法仓库）

**新增目录：**
```
resources/04_代码模板/Python/
├── evaluation/
│   ├── dea_efficiency.py           ← DEA数据包络分析（Giyn + RabbitWhite1）
│   ├── fahp_fuzzy.py               ← 模糊AHP（Giyn）
│   ├── rsr_rank_sum.py             ← 秩和比（Giyn + HeXavi8）
│   ├── fuzzy_multi_level.py        ← 多级模糊综合评价（RabbitWhite1）
│   └── grey_relational_heatmap.py  ← 灰色关联+热力图（Giyn）
├── prediction/
│   ├── grey_prediction_class.py    ← 灰色预测类（Lanrzip，含GM(1,1)/新陈代谢/GM(2,1)）
│   ├── markov_chain.py             ← 马尔可夫链（RabbitWhite1 + HeXavi8）
│   ├── hmm_hidden_markov.py        ← HMM隐马尔可夫（leost123456）
│   └── gaussian_process.py         ← 高斯过程回归（RabbitWhite1）
├── optimization/
│   ├── nsga2_multi_obj.py          ← NSGA-II多目标优化（Lupynow）
│   ├── cvar_robust.py              ← CVaR鲁棒优化（Lupynow）
│   ├── system_dynamics.py          ← 系统动力学（Lupynow）
│   └── sa_geodesic.py              ← 模拟退火+大地距离（RabbitWhite1）
├── statistical/
│   ├── mk_mutation_test.py         ← MK突变检验（leost123456）
│   ├── bayesian_network.py         ← 贝叶斯网络（leost123456）
│   ├── lof_from_scratch.py         ← LOF异常检测（leost123456）
│   └── mcmc_sampling.py            ← MCMC采样（HeXavi8，Gibbs+M-H）
├── simulation/
│   ├── queuing_theory.py           ← 排队论M/M/1（ravenxrz + Lanrzip）
│   ├── cellular_automata.py        ← 元胞自动机交通流（ravenxrz）
│   └── monte_carlo_endogeneity.py  ← 蒙特卡洛内生性（Lanrzip）
└── signal/
    └── wavelet_analysis.py         ← 小波分析（HeXavi8）
```

**新增MATLAB模板：**
```
resources/04_代码模板/MATLAB/
├── cellular_automata_traffic.m     ← 多车道交通流（ravenxrz）
├── queuing_theory_mm1.m            ← 排队论（ravenxrz）
└── yalmip_optimization.m           ← YALMIP建模（ravenxrz）
```

### 模块 5：写作增强（from XiaoMaColtAI + Lupynow）

**新增文件：**
```
.claude/skills/paper-formal-writer/references/
├── anti-ai-detection-guide.md      ← 8类AI痕迹+禁用词表
├── four-round-self-review.md       ← 4轮自审框架
├── evidence-pyramid.md             ← 证据金字塔（4层）
├── section-architecture.md         ← 章节架构模式
├── abstract-6-element.md           ← 摘要6要素
└── cmcm-mcm-writing-diff.md        ← 国赛/美赛写作差异

.claude/skills/paper-formal-writer/references/phrases/
├── common-phrases-cn.md            ← 中文学术短语库
└── common-phrases-en.md            ← 英文学术短语库
```

**Anti-AI-detection 8类模式：**
1. 过度强调词（标志/关键/重要）
2. 广告语言（突破性/令人震撼）
3. 模糊归因（专家认为/研究表明）
4. 浅层分析（了/着结尾）
5. 套话"挑战与展望"
6. AI高频词（此外≤2次，深入探讨=0次）
7. 三段式强迫
8. 同义词循环

**4轮自审框架：**
1. 论点逻辑（Claim-Evidence映射）
2. 章节结构合规
3. 表达质量 + AI痕迹扫描
4. 格式标准

---

## 三、参考论文库整合

**新增O奖论文（100+篇）：**
```
resources/02_优秀论文/
├── MCM_ICM_O奖/
│   ├── 2016/   ← 来自 MathematicalModeling
│   ├── 2017/   ← 来自 MathematicalModeling
│   ├── 2018/   ← 来自 MathematicalModeling
│   ├── 2019/   ← 来自 HeXavi8（36篇）
│   └── 2020/   ← 来自 HeXavi8（37篇）
├── CUMCM_国赛/
│   ├── 2015/   ← 来自 MathematicalModeling
│   └── 2017/   ← 来自 MathematicalModeling
└── 经典题解/
    └── 90+经典题解.doc  ← 来自 MathematicalModeling
```

**LaTeX模板：**
```
resources/13_LaTeX模板/
├── MCM_mcmthesis_v402/    ← 来自 MathematicalModeling
├── MCM_mcmthesis_cls/     ← 来自 HeXavi8
└── MCM_latex_template/    ← 来自 Eurus-Holmes
```

---

## 四、Playbook 整合（from Lupynow）

**新增文件：**
```
.claude/skills/model-selector/references/playbooks/
├── playbook-scheduling-opt.md      ← 调度优化
├── playbook-physics-ode.md         ← 物理ODE
├── playbook-ml-classification.md   ← ML分类
├── playbook-ml-regression.md       ← ML回归
├── playbook-evaluation-decision.md ← 评价决策
├── playbook-strategy-game.md       ← 策略博弈
├── playbook-path-planning.md       ← 路径规划
├── playbook-data-insight.md        ← 数据洞察
├── playbook-geometric-kinematics.md← 几何运动学
├── playbook-mcm-network.md         ← MCM网络
├── playbook-mcm-environmental.md   ← MCM环境
└── playbook-mcm-policy.md          ← MCM政策
```

---

## 五、执行计划

| 阶段 | 任务 | 文件数 | 优先级 |
|------|------|--------|--------|
| Phase 1 | 合同体系（Model Contract + Figure Contract） | 2 | P0 |
| Phase 2 | 门控架构（G1-G6 + Frozen Numbers + PoC） | 3 | P0 |
| Phase 3 | 选型矩阵 + Cookbook（8个） | 11 | P0 |
| Phase 4 | 新算法模板（19个Python + 3个MATLAB） | 22 | P1 |
| Phase 5 | 写作增强（Anti-AI + 自审 + 短语库） | 8 | P1 |
| Phase 6 | 参考论文库整合 | 批量复制 | P1 |
| Phase 7 | Playbook（12个） | 12 | P1 |
| Phase 8 | 更新 CLAUDE.md 和系统文档 | 1 | P0 |

**总计新增：~60 个文件，增强 8 个现有 skill**
