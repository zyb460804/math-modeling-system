# CLAUDE.md — 数学建模竞赛生产系统

> **版本：v4.6 | 更新：2026-07-30**
> **v4.0→v4.6 全演进一览**：`paper_output/research/CHANGELOG.md`（一眼看全 7 轮演进的定位/来源/新增/报告）
> **v4.6 变更摘要：** 学术级方法论融合——`usail-hkust/LLM-MM-Agent`（NeurIPS 2025，MCM/ICM 2025 Finalist 前 2% 的建模副驾驶）。**HMML 分层建模方法库**（model-selector/references/hmml/）：5 domain / 18 subdomain / 97 method node 三层知识树（OR / Optimization / ML / Prediction / Evaluation），原样移植 180KB JSON + 162KB MD，选模从"场景→算法"升级为"问题→domain→subdomain→method"分层检索，与 model-selection-matrix（95+场景直查）互补。**actor-critic 选模算法指南**（hmml-retrieval-guide.md）：MethodScorer 自顶向下逐层打分（叶子 final_score = 父路径均分×0.5 + 自身分×0.5），LLM 批判 + embedding 相似双模式。**美赛题型分题策略**（problem-doc-model-selector/references/mcm-decompose-strategy.json+md）：A-F 六题型 × 3/4/5 子任务数的分题原则 + decompose→refine 两步流程，与 analyze skill 的 sub_problems 衔接。**scikit-opt 启发式算法桥接**（model-code-and-result-generator/references/heuristic-algo-scikit-opt.md）：7 种群体智能算法（DE/GA/PSO/SA/ACA/IA/AFSA）一行调用 + 与 cookbook-optimization 手写版的分工。共 8 新建 + 3 SKILL.md 修改，外科手术式增量不改骨架。详见 `paper_output/research/CHANGELOG.md`。
> **v4.5 变更摘要：** 全面体检 + 断链清零（8 维度多智能体审计 37 条发现 → 全部处置）。**P0 修复**：`render_check.py` 编译期 SyntaxError（global 先用后声明）→ 图表质量门禁（figure/s6/all 阶段）自 v3.6 以来首次真正可用，CLI 文档同步为子命令写法。**断链清零**：8 个社区 skill 的 11 个"文档引用但从未落地"脚本全部实现并冒烟通过（citation-tracer 2 / style-calibration 2 / academic-paper-composer 2 / academic-paper-strategist 2 / ai-failure-checker 1 / algorithm-benchmark 1 / feature-engineering preprocess 1），4 个错位 references/ 文件归位。**QA 去硬编码**：4 个门禁脚本（parameter/result/sensitivity/baseline）的旧赛题硬编码外置到 `paper_output/plan/qa_config.json`（schema 示例见 `quality-assurance-auditor/references/qa_config.example.json`），缺配置显式 SKIP 消灭假绿灯；另 3 个脚本补 argparse（--help 不再触发主逻辑写报告）。**RAG 修复**：papers.csv 2 行残留空格路径修正（`mmqa split` 再生成链路解阻）、nodes jsonl 重生成 6910→6863 与索引对齐、requirements.txt 对齐实际 5 依赖。**环境补齐**：docx-editor-cn npm install（docx/fast-xml-parser/temml）+ pandoc 3.10 → Word 原生公式链全线可用；MiKTeX/pix2text 未装（LaTeX 编译与公式 OCR 分支需先装）。**文档一致性**：CLAUDE.md 10 处失实修正（01_真题与附件、MASTER_PROMPT 位置、skill 计数 7→8/16→13、G4.6 路径、目录树补录等）。**清理**：16 个 .DS_Store/Thumbs.db、7 个空占位目录、tools/README 对齐实际；resources 约 32.8GB 完整重复（03 合集副本 + 嵌套拷贝）已全量校验实锤，删除命令备于 `resources/03_方法算法/README_国赛C题合集已去重.md` 待手动执行。统一验证：130 py 编译 0 失败 / 16 必需文件全在 / 13 关键脚本 --help 全过。
> **v4.4 变更摘要：** 系统整理 + 实测验证。架构：math-model-producer 归档至 `resources/_archive/`（单生产系统成型，双系统→单系统）。RAG：CSV 去重(254→251)、md 文件名尾随空格根因修复(`_safe_id` 截断后再 strip)、向量索引 rebuild(6863 节点，CSV=md=jsonl 三者一致)。文档：单系统路由全面更新(asset_registry/task_router/knowledge_update/deduplication/prompts-29/README/AGENTS 共 20+ 处)、3 个自动清单加迁移公告。实测验证：预检/状态门/门禁脚本全部跑通(`evidence_gate` 真实发现 Q3/Q5 缺评价指标、`check_paper_format` 发现 Word 缺图)、RAG 实测召回储能/微电网相关论文、11 个工具脚本全部 `--help` 通过。清理：39 个 `__pycache__` + 临时垃圾 + 重复 zip + `paper_output` 归档分层(`_archive_2026-06` / `_archive_2026-07_绿电直连型`)。
> **v4.3 变更摘要：** 工具链增强（Camelot/Pix2Text/SciencePlots/aigc-deslop + 数学 MCP 文档）。新增：PDF 表格提取（Camelot，赛题附表一键转 CSV/Excel）、公式/图表 OCR（Pix2Text，PDF 公式→LaTeX）、期刊风图表样式（SciencePlots，IEEE/Nature 一行出图）、Word 格式保留降重（aigc-deslop，9轮实测 55%→11%）、6 个数学/学术 MCP 配置文档（sympy/optimizer/arxiv/semantic-scholar/wolfram/math）。详见 `docs/math-mcp-servers.md`。
> **v4.2 变更摘要：** 同赛道生态大融合（5 仓库 / 26 新建）。新增：Typst 交付链路（17 Typst + 17 LaTeX = 34 套赛事模板 + typst-renderer skill）、GitOps 流水线状态机（pipeline_manager）、强制代码自证 G4.6 门（verify_gate + verification_template）、注入防护+密钥扫描+precommit hook（security_check）、通用 inf/nan/量级扫描（check_numeric_sanity）、Word 原生公式+XML 编辑（docx-editor-cn，temml→MathML→docx + office unpack/pack/validate）、SHA-256 报告新鲜度校验（freshness_check）、O 奖论文章节级 RAG（award-paper-rag，heading 分块+13 类分类器）、HIL 6 动作（confirm/edit/regenerate/ask/skip/abort）、4 层容错设计、双 Agent 推导↔编码解耦。详见 `paper_output/research/github_fusion_v4.2_report.md`。
> **v4.1 变更摘要：** 同级竞品外科手术式融合（handsomeZR/mathmodel-skill v6.1 + sweetcornna/mathodology）。新增：题型差异化加权（dim_weights.json）、empirical 分题型分位（by_topic A-F）、4 层反馈机制（L1 Critic/L2 回检/L3 Panel/L4 校准）、盲评 Panel（3 座 + 20 分冲突 + 真实稀缺性校准）、Per-Qi 加权聚合、figqa bbox 碰撞门、3 模式（fast/standard/championship）、Friendly Mode 问答式。13 新建 + 5 修改，详见 `paper_output/research/tier1_diff_and_port_report.md`。
> **变更摘要：** 大规模GitHub融合（15仓库→60+文件）：新增合同体系（Model/Figure Contract）、门控架构（G1-G6）、95+场景选型矩阵、8领域Cookbook、12端到端Playbook、22个新算法模板、Anti-AI-detection写作指南、4轮自审框架、证据金字塔、100+O奖论文库、90+经典题解、3版LaTeX模板。详见 §GitHub 15仓库融合。

---

## 开发命令（给改系统本身的人）

> 使用数学建模功能见下方「项目定位」起的内容；本节面向**修改本系统代码/文档**的开发场景。

### 安装依赖

```bash
./setup.ps1                # Windows：核心 + 交互式可选 + npm + 外部软件检查
./setup.sh --core          # macOS/Linux/Git Bash：只装核心
pip install -r docs/requirements-optional.txt   # v4.3 工具链（图表/PDF/SHAP/Optuna/akshare）
```

### 改完代码后的验证（每次修改 .py 后跑）

```bash
# 1. 编译扫描（应 0 失败；当前 130+ .py）
find .claude/skills tools outputs/scripts -name '*.py' -not -path '*/node_modules/*' -exec python -m py_compile {} +

# 2. --help 冒烟（关键门禁脚本，--help 不应触发主逻辑写报告）
python .claude/skills/math-figure/scripts/render_check.py --help
python .claude/skills/quality-assurance-auditor/scripts/evidence_gate.py --help
python .claude/skills/quality-assurance-auditor/scripts/pipeline.py --help

# 3. QA 门禁脚本换题注意：读 paper_output/plan/qa_config.json，缺配置显式 SKIP
#    schema 示例：.claude/skills/quality-assurance-auditor/references/qa_config.example.json
```

### RAG（award-paper-rag）语料链路

```bash
cd .claude/skills/award-paper-rag
python -m scripts.mmqa split --out-text-nodes-jsonl data/nodes/text_nodes.block.jsonl  # 再生成（改 papers.csv 后）
# 验证三者一致：papers.csv 行数 == md 语料数 == jsonl 节点数 == 6863
```

### Git 流程（仓库已发布到 GitHub）

```bash
git add -A && git commit -m "<type>: <描述>"   # type: feat/fix/docs/refactor
git push                                       # 远程已设 origin/main，无需加参数
```

### 测试现状

本系统**无 pytest 测试套件**——质量保障靠门禁脚本（evidence_gate / pipeline / render_check / consistency-auditor / completeness-auditor）在真实赛题流水线中验证。改门禁脚本后，用 `--help` + 临时合成数据冒烟即可。

---

## 项目定位

数学建模竞赛生产系统。Claude 在此项目中同时扮演：

- **总教练**（审题、选模、评分）
- **论文生产器**（写作、改稿、摘要）
- **代码生成器**（Python/Matlab 算法代码）
- **图示设计器**（流程图、结果图、答辩图）
- **答辩陪练**（问答、追问链、风险点）

---

## ⚡ MathModel Skill 工作流（Agent-Native 入口）

### Start Rule（CRITICAL）

任何数学建模论文任务都**必须先读取总控 skill**：

```
.claude/skills/paper-workflow-orchestrator/SKILL.md
```

触发词：`开始生成` `跑一下这个题` `生成数学建模论文` `分析赛题` `使用 MathModel Skill`

### 触发词统一入口（v3.4）

> **核心原则：同一意图 → 默认最深输出。** 用户不需要知道"加什么词"才能拿到完整结果。

| 统一入口 | 覆盖的触发词 | 默认输出 |
|---------|-------------|---------|
| `review` / `paper-reviewer` agent | 打分、审稿、严格打分、深度评审、审论文 | 全量深度报告（9部分：总分+7模块+9信号+13要素四档+锚点对比+扣分细则+P0/P1/P2+门槛核验+三句话） |
| `defense` | 准备答辩、模拟答辩、答辩练习、评委提问 | 全量答辩包（10类问答+30条追问链+模拟评分+短答模板+分题型重点+风险预警） |
| `analyze` | 审题、选模、推荐模型、建模路线 | 全量审题选模报告（题型判断+Top3路线+代码模板路径+风险预警+检验包+写作落点） |
| `figure` | 生成图示、画图、流程图、网络图、函数图、交互式图表、论文图、推荐图表 | 统一图表方案（自动判断需求→分派子skill→生成全部所需图→更新figure_index.json） |
| `paper-polisher` | 润色、改写、polish、换个说法、更学术一点、更简洁一点 | 完整12点检查+段落改写+变更摘要+质量评分（60分制） |
| `code` | 生成代码 | 从零生成代码框架（输出末节自动引 algorithm-runner） |
| `algorithm-runner` | 运行算法、执行代码 | 执行已有算法模板（输出末节自动引 code） |
| `submit` | 生成提交包 | 最终比赛提交包（自动判断阶段；输出末节说明与 solution-package-builder 的区别） |
| AIGC降重 | 降AI味、降重、去AI检测 | 默认走 humanizer-zh-academic（14种AI模式+7项硬约束）；备选 aigc-reduce |
| `blind-panel`（v4.1） | 盲评、盲审、模拟评委、校准打分、panel | 3 座独立盲评 + 20 分冲突仲裁 + 真实稀缺性校准（修正自评虚高） |
| 模式切换（v4.1） | 升级到 championship、切到 fast | orchestrator 模式切换（fast/standard/championship，按 deadline 自动推荐） |
| L2 回检（v4.1） | 做 L2 回检、跨阶段一致性检查 | qa-auditor 反馈层 L2：定向回滚不重做整阶段 |

> **唯一例外**：用户明确说"只要总分，不要分析"时，评审才输出精简版。

### 完整流水线

```
读题 → 拆题 → 模型路线 → 判断附件性质 → 生成/修改赛题专用代码 → 运行代码
→ 真实图表/表格/结果 → 证据门禁 → 正式 outline → Agent 全局写作
→ Word 排版 → 格式门禁 → 最终 QA →（championship）盲评 Panel + figqa 碰撞门
```

### 10 个 Native Skill 及路由（主轨道核心）

| Skill | 职责 | 触发时机 |
|-------|------|----------|
| `paper-workflow-orchestrator` | ★ 总入口，阶段判断与路由 | 任何数学建模任务的第一步 |
| `problem-doc-model-selector` | 题意解析、题型判断 | 刚开始/只有赛题 |
| `modeling-paper-rubric-and-model-selector` | 模型路线、评分闭环 | 有 `problem_analysis.json` 后 |
| `authoritative-data-harvester` | 外部权威数据获取 | 需要补充文献/数据 |
| `data-cleaning-and-visualization` | 数据处理、图表计划与生成 | 有模型路线后 |
| `model-code-and-result-generator` | 建模代码、结果证据契约 | 数据清洗后 |
| `quality-assurance-auditor` | 证据门禁、QA 任务清单 | 进入正文前/最终把关 |
| `paper-formal-writer` | 正式成稿、大纲契约、Word 排版、格式门禁 | 证据门禁通过后 |
| `paper-micro-unit-generator` | 微单元生成、局部扩写 | 需要分块写作/低能力兜底 |
| `context-memory-keeper` | 三层记忆架构（工作/短期/长期）+ 知识图谱集成 | 各阶段完成后 |

### 9 个 Legacy Skill（内部调度工具，原轨道 B，v3.4 统一入口已取代）

| Skill | 职责 | 口令 |
|-------|------|------|
| `scan` | 扫描目录、建文件地图、标优先级 | 先扫一遍资料 |
| `card` | 逐文件提炼知识卡片 | 抽卡 |
| `rules` | 更新评分表/方法匹配表/模板库 | 建规则库 |
| `analyze` | ★ 统一审题选模入口：题型判断+模型路线+代码模板+风险预警 | 审题/选模 |
| `review` | ★ 统一评审入口→委托 paper-reviewer agent，默认最深报告 | 审论文/打分 |
| `code` | 判断题型与算法，生成可运行代码（从零写代码） | 生成代码 |
| `defense` | ★ 统一答辩入口：问答库+追问链+模拟评分+短答模板 | 准备答辩/模拟答辩 |
| `submit` | 高分自检后输出论文+代码+图表+答辩清单（比赛提交包） | 生成提交包 |
| `figure` | ★ 统一图表入口：自动判断需求→分派子skill→生成全部图表 | 生成图示/画图 |

### 9 个 Nature 学术 Skill

| Skill | 职责 |
|-------|------|
| `nature-polishing` | Nature 风格英文润色、学术翻译 |
| `nature-writing` | Nature 风格论文写作、重建引言/讨论 |
| `nature-figure` | Nature/高影响力期刊多面板科学图表 |
| `nature-citation` | Nature/CNS 期刊文献检索与引用插入 |
| `nature-data` | 数据可用性声明、FAIR 检查 |
| `nature-reader` | 论文中英对照全文翻译、图表提取 |
| `nature-response` | Nature 风格逐条审稿回复信 |
| `nature-paper2ppt` | 论文转中文 PPT、组会汇报 |
| `nature-academic-search` | PubMed/CrossRef/arXiv 多源文献检索 |

### 2 个工具 Skill

| Skill | 职责 |
|-------|------|
| `git-snapshot` | 创建项目时间点快照，保留最近 10 个版本 |
| `algorithm-test` | 运行 Python 代码、语法检查、错误捕获 |

### 8 个新增 Skill（v3.6-v3.7 GitHub融合）

| Skill | 职责 | 来源 |
|-------|------|------|
| `consistency-auditor` | 一致性审计（三审计层第一层） | zhnnky329/MathModeling-skills |
| `completeness-auditor` | 完整性审计（三审计层第二层） | zhnnky329/MathModeling-skills |
| `decision-logger` | 决策日志记录 | zhnnky329/MathModeling-skills |
| `feature-engineering` | 特征工程标准化流程 | FinDii/FeatureEngineering |
| `algorithm-benchmark` | 算法基准测试 | szilard/benchm-ml |
| `style-calibration` | 写作风格校准 | Imbad0202/academic-research-skills |
| `citation-tracer` | 引用溯源工具 | Imbad0202/academic-research-skills |
| `ai-failure-checker` | AI失败模式检查（7-mode checklist） | Imbad0202/academic-research-skills |

### 10 个新增 Skill（v3.2）→ v3.4 降级为内部调度工具

| Skill | 职责 | 当前状态 |
|-------|------|---------|
| `model-selector` | 智能选模 | → 由 `/analyze` 内部调度 |
| `chart-recommender` | 图表推荐 | → 由 `/figure` 内部调度 |
| `defense-simulator` | 答辩模拟 | → 由 `/defense` 内部调度 |
| `algorithm-runner` | 算法执行 | 独立入口（与 code 互补，互引） |
| `result-validator` | 结果验证 | 自动触发 |
| `paper-rewriter` | 段落改写 | → 由 `paper-polisher` 内部调度 |
| `diagram-maker` | 流程图 | → 由 `/figure` 内部调度 |
| `interactive-chart` | 交互图表 | → 由 `/figure` 内部调度 |
| `math-figure` | 数学图表 | → 由 `/figure` 内部调度 |
| `network-graph` | 网络图 | → 由 `/figure` 内部调度 |

> **注意**：仅在 orchestrator 路由到对应阶段时读取对应 SKILL.md，不要预加载全部 skill 文件。

### 工具链增强（v4.3 新增）

> 融合来源：`atlanhq/camelot`（3716★）+ `breezedeus/Pix2Text`（3195★）+ `garrettj404/SciencePlots`（~5k★）+ `huanghfzhufeng/aigc-deslop`（18★）+ Optuna（14549★）+ SHAP/shapash（3247★）+ akshare（~10k★）。v4.3 聚焦**单点工具提效**（不改主流程，按需调用）。

#### 新增脚本（7 个，已登记进各 SKILL.md + 路由层 4/4）

| 能力 | 脚本 | 所属 skill | 价值 |
|------|------|-----------|------|
| **PDF 表格提取** | `extract_pdf_tables.py` | data-cleaning-and-visualization | 赛题附表一键转 CSV（Camelot，✓ 真实提取 A题.pdf） |
| **公式 OCR** | `extract_formulas_ocr.py` | problem-doc-model-selector | PDF 公式图→LaTeX（Pix2Text） |
| **期刊风图表** | `journal_style.py` | math-figure | IEEE/Nature 76 样式（SciencePlots，✓ 出图验证） |
| **Word 格式保留降重** | `replace_docx_preserve_format.py` | aigc-reduce | 降 AIGC 不破坏排版（aigc-deslop，9 轮实测 55%→11%） |
| **SHAP 可解释性** | `shap_explain.py` | feature-engineering | ML 题特征重要性（评委加分项） |
| **Optuna 超参调优** | `optuna_tune.py` | model-code-and-result-generator | TPE 贝叶斯优化（替代网格搜索） |
| **宏观数据获取** | `akshare_fetch.py` | authoritative-data-harvester | GDP/CPI/股价/行业产量（C 题刚需） |

#### 新增文档

- `docs/math-mcp-servers.md` — 6 个数学/学术 MCP 配置（sympy/optimizer/arxiv/semantic-scholar/wolfram/math，命令已从源仓库校准）

#### 已装 pip 包（全局可用）

SciencePlots 2.2.2 / camelot-py 2.0.0 / shap 0.51.0 / optuna 4.9.0 / akshare 1.18.75（Pix2Text 按需首装）

#### 依赖说明

- Pix2Text：`pip install pix2text`（首跑下模型，设 `HF_ENDPOINT=https://hf-mirror.com`）
- 数学 MCP：见 `docs/math-mcp-servers.md`，`claude mcp add` 按需装

### 同赛道生态融合（v4.2 新增）

> 融合来源：`jihe520/MathModelAgent`（2862★，行业最大）+ `RealSeaberry/AutoMCM-Pro`（144★，架构最佳）+ `Gostyan/docx-skill-4-cn-paper`（335★，Word 专家）+ `Kirito-Elucidator/MathModel-QA-Engine`（10★，F奖得主）+ `yushui2022/MathModel-Skill`（217★，同源 cherry-pick）。完整报告：`paper_output/research/github_fusion_v4.2_report.md`。

#### 新增能力

| 能力 | 关键文件 | 用途 |
|------|---------|------|
| **Typst 交付链路** | `resources/15_Typst模板/`（34 套）+ `typst-renderer` skill | 新增 Typst 排版分支（与 Word/LaTeX 三选一），17 Typst + 17 LaTeX，覆盖 14 中文赛事+3 英文 |
| **GitOps 流水线状态机** | `quality-assurance-auditor/scripts/pipeline_manager.py` | not_started→in_progress→pending_review→approved↔rework + 返工上限 + AP/Manual 双模式 + 并行阶段 |
| **强制代码自证 G4.6** | `quality-assurance-auditor/scripts/verify_gate.py` + `model-code-and-result-generator/scripts/verification_template.py` | 每模型必配 `verify_*.py`（约束/物理/数值），全 PASS 才进论文 |
| **通用数值合理性** | `check_numeric_sanity.py` | inf/nan/量级扫描（互补于硬编码 result_reasonableness） |
| **安全：注入+密钥+hook** | `security_check.py` + `precommit_scan.sh` | Markdown 注入防护 + 密钥扫描 + 提交前拦截 |
| **Word 原生公式+XML 编辑** | `docx-editor-cn` skill | temml→MathML→docx OMML 链 + office unpack/pack/validate 局部 XML 编辑 |
| **SHA-256 报告新鲜度** | `freshness_check.py` | 源变化后旧报告标记 STALE，强制重生 |
| **O 奖论文章节级 RAG** | `award-paper-rag` skill + mmqa/ 包 | heading 分块 + 13 类分类器 + 年份/题号/章节过滤，检索 190+ 篇优秀论文 |
| **HIL 6 动作** | `hil_6_actions.md` + `parse_hil_action.py` | confirm/edit/regenerate/ask/skip/abort（扩展 G2.5/G4.5 之外） |
| **4 层容错** | `four_layer_fault_tolerance.md` | L1 重试→L2 Fallback→L3 Shadow→L4 Feedback |
| **双 Agent 解耦** | `dual_agent_design.md` | 推导轨↔编码轨并行（多子问题赛题） |

#### 触发词新增

| 触发词 | 路由 |
|--------|------|
| Typst 渲染 / 编译 Typst / 用 Typst 排版 | `typst-renderer` skill |
| 编辑 Word / 改 Word 公式 / 局部修改 docx / LaTeX 公式转 Word 原生 | `docx-editor-cn` skill |
| 查优秀论文 / O 奖论文检索 / 章节检索 / 历年 C 题用了什么方法 | `award-paper-rag` skill |
| 流水线状态 / 推进阶段 / 返工 / 并行启动 | `pipeline_manager.py`（qa-auditor） |
| G4.6 自证门 / 验证所有模型 | `verify_gate.py` |
| 数值合理性 / inf nan 检查 | `check_numeric_sanity.py` |
| 报告新鲜度 / 校验报告是否过期 | `freshness_check.py` |
| 安全检查 / 密钥扫描 / 注入防护 | `security_check.py` |

#### 验证状态

- ✅ 9 个新脚本全部 `py_compile` / `bash -n` 通过
- ✅ pipeline_manager / verify_gate / check_numeric_sanity / freshness_check / parse_hil_action / build_typst_index 真实跑通
- ✅ 372 个 Typst/LaTeX 模板文件落地 + typst_index.json 生成（17 Typst + 17 LaTeX）
- ✅ docx-editor-cn 的 office/ 7 个 Python 工具 + mmqa/ 8 文件全部编译通过

#### 依赖说明（首次使用时安装）

- `docx-editor-cn`：`cd .claude/skills/docx-editor-cn && npm install`（docx / fast-xml-parser / temml）
- `award-paper-rag`：`pip install -r .claude/skills/award-paper-rag/scripts/requirements.txt`（llamaindex 0.14）+ 语料需先转 md 建 papers.csv
- `typst-renderer`：`winget install --id Typst.Typst`（Typst CLI）

### 同级竞品融合（v4.1 新增）

> 融合来源：`handsomeZR-netizen/mathmodel-skill` v6.1（153★）+ `sweetcornna/mathodology`（37★）。外科手术式增量，不替换骨架。完整报告：`paper_output/research/tier1_diff_and_port_report.md`。

#### 新增能力

| 能力 | 关键文件 | 用途 |
|------|---------|------|
| 题型差异化加权 | `outputs/dim_weights.json` | competition×task_type×stage×dim 加权 [0.7,1.5]，倒逼补 A 题 skipped 的 optimizer |
| empirical 分题型分位 | `outputs/empirical.json` v2.0 | by_topic A-F 图表/公式分位；A 题 figure p50=8（修正 v1.0 全局"10-15"误导）|
| 4 层反馈机制 | `.claude/skills/quality-assurance-auditor/references/feedback_layer{1-4}_*.md` | L1 阶段 Critic + diff 精修 / L2 跨阶段回检 / L3 Panel / L4 证据校准 |
| 盲评 Panel | `.claude/agents/blind-panel-judge.md` + `.claude/skills/blind-panel/` | 3 座独立盲评 + **20 分冲突仲裁** + 真实稀缺性校准（修正自评虚高）|
| Per-Qi 加权聚合 | `.claude/agents/paper-reviewer.md` §10 | 多子问题独立评分，只 refine 挂科 Qi |
| figqa 碰撞门 | `.claude/skills/math-figure/scripts/{figqa.py,pdf_qa.sh,make_contact_sheet.py}` | bbox 零碰撞 + 从编译 PDF 建 contact sheet（自测通过）|
| 3 模式 | `paper-workflow-orchestrator/SKILL.md` | fast/standard/championship，按 deadline 自动推荐 |
| Friendly Mode | 同上 | 问答式（AskUserQuestion），用户不敲 bash |

#### 触发词新增

| 触发词 | 路由 |
|--------|------|
| 盲评 / 盲审 / 模拟评委 / 校准打分 / panel | `blind-panel` skill（3 座并行）|
| 升级到 championship / 切到 fast | orchestrator 模式切换 |
| 做 L2 回检 / 跨阶段一致性检查 | qa-auditor L2 层 |

#### 验证状态

- ✅ empirical.json / dim_weights.json JSON 合法
- ✅ figqa.py `--self-test` PASS
- ✅ 5 个被修改文件全有备份（`port_backup_20260722/`）

### GitHub 15 仓库融合（v4.0 新增）

> 融合来源：XiaoMaColtAI(338⭐)、zhnnky329(191⭐)、Lupynow(99⭐)、ravenxrz(526⭐)、Lanrzip(495⭐)、RabbitWhite1(217⭐)、leost123456(177⭐)、Giyn(104⭐)、HeXavi8(87⭐)、qiziqiang(176⭐) 等 15 个仓库。

#### 新增参考文档（paper-workflow-orchestrator/references/）

| 文件 | 来源 | 用途 |
|------|------|------|
| `model-contract-template.md` | XiaoMaColtAI | 前置合同：核心结论+证据链+反冗余+交付规格 |
| `figure-contract-template.md` | XiaoMaColtAI | 图表合同：结论+面板证据+灰度安全+色盲无障碍 |
| `gate-system.md` | zhnnky329 | G1-G6 门控架构（含人工门 G2.5/G4.5） |
| `frozen-numbers-convention.md` | zhnnky329 | 数字冻结机制（3步解冻-修改-重冻） |
| `poc-validation-gate.md` | zhnnky329 | PoC验证门禁（≤30行+可行性数字） |

#### 新增选型资源（model-selector/references/）

| 文件 | 来源 | 用途 |
|------|------|------|
| `model-selection-matrix.md` | Lupynow | 95+场景×12类问题决策矩阵 |
| `problem-decomposition.md` | Lupynow | 12型问题分类法+信号词+I/O规范 |
| `playbooks/` (12个) | Lupynow | 端到端解题Playbook（调度/物理/ML/评价/博弈/路径/数据/几何/网络/环境/政策） |

#### 新增领域知识库（model-code-and-result-generator/references/）

| 文件 | 来源 | 覆盖领域 |
|------|------|---------|
| `cookbook-optimization.md` | Lupynow | GA/PSO/SA/LP/DP |
| `cookbook-ml.md` | Lupynow | XGBoost/RF/SVM/NN |
| `cookbook-evaluation.md` | Lupynow | TOPSIS/AHP/熵权/模糊 |
| `cookbook-mechanistic.md` | Lupynow | 传热/ODE/几何/光学 |
| `cookbook-statistical.md` | Lupynow | 假设检验/ANOVA/蒙特卡洛/贝叶斯 |
| `cookbook-network.md` | Lupynow | 图论/网络流/中心性 |
| `cookbook-clustering.md` | Lupynow | 层次/K-Means/DBSCAN/GMM |
| `cookbook-game-theory.md` | Lupynow | 南什/演化/Stackelberg |

#### 新增写作增强（paper-formal-writer/references/）

| 文件 | 来源 | 用途 |
|------|------|------|
| `anti-ai-detection-guide.md` | XiaoMaColtAI+Lupynow | 8类AI痕迹+禁用词表+替换策略 |
| `four-round-self-review.md` | XiaoMaColtAI+Lupynow | 4轮自审（Claim-Evidence→结构→表达→格式） |
| `section-architecture.md` | XiaoMaColtAI | 摘要6要素/引言5要素/结果证据阶梯 |
| `evidence-pyramid.md` | XiaoMaColtAI | 4层证据金字塔 |
| `common-phrases.md` | Lupynow | 中英双语学术短语库（10章节） |
| `literature-review-guide.md` | Lupynow | T1/T2/T3信源路由+搜索4层法+引用格式 |

#### 自动回环修正（v4.0 新增）

当检测脚本发现质量问题时，自动运行修正器并重检，最多循环 3 轮，仍失败才报告用户。

```bash
# 单个阶段自动检测+修复
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage code

# S5 阶段全部检测（数字/参数/结果/证据）
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s5

# S6 阶段全部检测（格式/图表/LaTeX/引用/AIGC）
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s6

# S7 阶段全部检测（一致性/完整性/符号表）
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage s7

# 全部 14 个阶段
python .claude/skills/quality-assurance-auditor/scripts/auto_detect_and_fix.py --stage all
```

| 阶段 | 检测 | 自动修复 | 源头 |
|------|------|---------|------|
| code | 代码运行验证 | 缺少导入/路径错误/编码错误/除零 | - |
| number | 数字一致性 | 论文数字 → 代码结果 | 代码为准 |
| parameter | 参数一致性 | 代码参数 → 题目要求 | 题目为准 |
| result | 结果合理性 | 缺失证据文件自动生成占位 | - |
| format | 格式门禁 | 空行/标点/公式格式/图表引用 | - |
| evidence | 证据门禁 | 缺失目录/文件自动创建 | - |
| consistency | 一致性审计 | 论文数字 → 代码结果 | 代码为准 |
| figure | 图表质量检查 | DPI/字体/重叠 → 自动调整参数重新渲染 | - |
| latex | LaTeX公式渲染 | 语法错误 → 自动修正 | - |
| completeness | 完整性审计 | 缺失文件/目录 → 自动创建占位 | - |
| citation | 引用一致性 | 断链引用/格式错误 → 自动修正 | - |
| aigc | AIGC检测 | AI痕迹过高 → 自动降重 | - |
| symbol | 符号表冲突 | 符号重复/不一致 → 自动解决 | - |
| code_style | 代码风格 | PEP8/格式 → 自动格式化 | - |

修正日志：`paper_output/qa/auto_correction_log.json`

#### 新增算法模板（resources/04_代码模板/Python/）

| 目录 | 新增模板 | 来源 |
|------|---------|------|
| `evaluation/` | DEA、FAHP、RSR、GRA热力图 | Giyn + RabbitWhite1 |
| `prediction/` | 灰色预测类、马尔可夫链、HMM、高斯过程 | Lanrzip + leost123456 + RabbitWhite1 |
| `optimization/` | NSGA-II、CVaR鲁棒、系统动力学、SA大地距离 | Lupynow + RabbitWhite1 |
| `statistical/` | MK突变检验、贝叶斯网络、LOF、GMM/EM、MCMC(Gibbs+M-H) | leost123456 + HeXavi8 + Lupynow |
| `simulation/` | 排队论、元胞自动机、食物链ODE | ravenxrz + Lupynow |
| `signal/` | 小波分析 | HeXavi8 |
| `ml/` | BP神经网络（从零） | HeXavi8 |

#### 新增参考资源（resources/）

| 目录 | 内容 | 来源 |
|------|------|------|
| `02_优秀论文/MCM_ICM_O奖/` | 100+篇O奖论文（2016-2020） | HeXavi8 + MathematicalModeling |
| `02_优秀论文/CUMCM_国赛/` | 国赛优秀论文（2015/2017） | MathematicalModeling |
| `08_参考资料/32种方法教材/` | 32种数学建模方法PDF教材 | MathematicalModeling |
| `08_参考资料/经典题解90/` | 90+经典题解.doc | MathematicalModeling |
| `08_参考资料/灵敏度分析论文/` | 60+篇灵敏度分析论文 | MathematicalModeling |
| `13_LaTeX模板/MCM_mcmthesis_v402/` | MCM LaTeX模板v4.02 | MathematicalModeling |
| `13_LaTeX模板/MCM_mcmthesis_cls/` | mcmthesis.cls模板 | HeXavi8 |
| `13_LaTeX模板/MCM_latex_template/` | MCM LaTeX模板 | Eurus-Holmes |

### 输入输出约定

- **赛题与附件** → `problem_files/`（必须非空）
- **补充数据** → `crawled_data/`（可选）
- **所有产物** → `paper_output/`（统一输出，不散落根目录）
- **赛题专用代码** → `paper_output/code/`（不写回 skill 目录）

### 正式交付门禁（七者缺一不可）

1. **证据门禁**：`quality-assurance-auditor/scripts/evidence_gate.py --mode official` 通过
2. **参数一致性门禁**：`quality-assurance-auditor/scripts/check_parameter_consistency.py` 通过
3. **结果合理性门禁**：`quality-assurance-auditor/scripts/check_result_reasonableness.py` 通过
4. **数字一致性门禁**：`quality-assurance-auditor/scripts/check_number_consistency.py` 通过
5. **格式门禁**：`paper-formal-writer/scripts/check_paper_format.py` 通过
6. **一致性审计**：`consistency-auditor/scripts/audit.py` 通过（三审计层第一层）
7. **完整性审计**：`completeness-auditor/scripts/audit.py` 通过（三审计层第二层）
8. 任一未通过 → **不得把 Word 称为最终稿**
9. **（championship 模式追加）盲评 Panel**：`blind-panel` skill 3 座盲评 PASS + `math-figure/scripts/figqa.py` 图表碰撞门 PASS；用于冲奖稿最终校准（standard 模式可选）

### 三审计层机制（v3.6 新增）

> **设计理念**：基于 zhnnky329/MathModeling-skills 的"每个审查者必须留下磁盘文件"原则。

```
论文完成后 → consistency-auditor → completeness-auditor → quality-assurance-auditor
三者全部PASS才能提交论文
```

| 审计层 | Skill | 检查内容 | 产出 |
|--------|-------|---------|------|
| 第一层 | `consistency-auditor` | 数字/文件名/符号与frozen_numbers.json交叉一致性 | `qa/consistency_audit_report.json` |
| 第二层 | `completeness-auditor` | 所有审查文件、审计报告、代码审查是否存在且质量达标 | `qa/completeness_audit_report.json` |
| 第三层 | `quality-assurance-auditor` | 工作流完整性、反编造、最终把关 | `qa/evidence_gate_report.json` |

### 用户决策门禁（v3.6 新增）

> **设计理念**：基于 zhnnky329/MathModeling-skills 的"AI owns mechanical correctness; the user owns modeling judgment"原则。

| 门禁 | 时机 | 要求 | 检查方式 |
|------|------|------|---------|
| **G2.5** | 方法选择后 | 用户填写选择理由（≥50字） | `decision-logger` 记录 |
| **G4.5** | 结果确认后 | 用户填写确认理由（≥30字） | `decision-logger` 记录 |
| **G4.6** | 代码运行后、结果引用进论文前 | 每个模型必配 `verifications/verify_*.py`，全 PASS 才能引用 | `verify_gate.py`（v4.2 新增，融合自 AutoMCM-Pro） |

**关键规则**：
- 决策理由必须由用户填写，AI不能代写
- 理由不能为空或过于简短
- 理由不能是AI模板文本
- 决策日志被 `consistency-auditor` 检查

### 原始数据只读保护（v3.6 新增）

`problem_files/` 目录已通过 `settings.json` 的 `deny` 规则保护：
- 禁止 Write/Edit 操作
- 禁止删除操作
- 原始数据只能读取，不能修改

### PoC验证门禁（v3.6 新增）

> **设计理念**：基于 zhnnky329/MathModeling-skills 的"每个候选方法必须有≤30行PoC在真实数据上运行"原则。

**Gate G2: PoC验证**

| 检查项 | 规则 | 严重度 |
|--------|------|--------|
| PoC文件存在 | 每个候选方法必须有PoC文件 | CRITICAL |
| PoC可运行 | PoC代码必须能成功运行 | CRITICAL |
| 有具体输出 | PoC必须产出具体数值结果 | CRITICAL |
| 使用真实数据 | PoC必须使用清洗后的真实数据 | HIGH |
| 代码行数≤30 | PoC代码不超过30行 | MEDIUM |

**PoC失败处理**:
- 标记为 `[REJECTED]`
- 记录失败原因
- 自动归档到 `paper_output/archived/{Q}/{method}_REJECTED/`

**相关Skill**: `model-selector`
**相关脚本**: `.claude/skills/model-selector/scripts/poc_validator.py`

### 图表render_check（v3.6 新增）

> **设计理念**：基于 zhnnky329/MathModeling-skills 的"each must pass render_check_and_log() before it can be designated a paper figure"原则。

**质量标准**:

| 检查项 | 标准 |
|--------|------|
| 最小字体 | ≥6.5pt |
| 最小分辨率 | ≥150 DPI |
| 最小尺寸 | ≥800×600 像素 |
| 文字重叠 | ≤5% 重叠比例 |
| 画布使用 | 白色区域≤80% |

**使用方式**:
```bash
# 检查单个图表
python .claude/skills/math-figure/scripts/render_check.py check --figure paper_output/figures/xxx.png

# 检查所有图表
python .claude/skills/math-figure/scripts/render_check.py check-all --dir paper_output/figures
```

**相关Skill**: `math-figure`
**相关脚本**: `.claude/skills/math-figure/scripts/render_check.py`

### 竞赛特化资源（v3.6 新增）

| 资源 | 路径 | 用途 |
|------|------|------|
| 竞赛特化句式库 | `outputs/phrase_bank.md` | 国赛获奖论文高频句式，按章节分类 |
| 实测分位数据 | `outputs/empirical.json` | v2.0：91 篇来源/59 可提取样本，**分题型 by_topic A-F** 图表/公式分位（A 题 figure p50=8）|
| 题型差异化加权（v4.1）| `outputs/dim_weights.json` | competition×task_type×stage×dim 加权 [0.7,1.5]，倒逼补 A 题 skipped 的 optimizer |

### 质量保障脚本

| 脚本 | 用途 | 何时使用 |
|------|------|---------|
| `check_parameter_consistency.py` | 检查代码参数是否与题目一致（配置驱动：读 paper_output/plan/qa_config.json，缺配置显式 SKIP） | 代码运行前 |
| `check_result_reasonableness.py` | 检查结果是否在合理范围（配置驱动：读 paper_output/plan/qa_config.json，缺配置显式 SKIP） | 代码运行后 |
| `check_number_consistency.py` | 检查论文数字是否与代码一致 | 论文写作后 |
| `inject_results_to_paper.py` | 自动将代码结果注入论文 | 论文写作时 |
| `run_sensitivity_analysis.py` | 自动生成灵敏度分析（配置驱动：读 paper_output/plan/qa_config.json，缺配置显式 SKIP） | 需要灵敏度分析时 |
| `run_baseline_comparison.py` | 自动运行基准对照（配置驱动：读 paper_output/plan/qa_config.json，缺配置显式 SKIP） | 需要展示优化价值时 |

---

## 目录结构（标准版 v3.0）

```
e:\数学建模\
├── CLAUDE.md              ← 本文件（快速入口，技能路由 + 10 条规则）
├── AGENTS.md              ← 完整系统规则（17 章，需深入了解时再读取）
├── README.md              ← 项目说明
│
├── .claude/agents/        ← ★ 9 个专业 Agent（v4.1 +blind-panel-judge）
│   ├── code-tester.md           Python 代码执行与验证
│   ├── paper-reviewer.md        论文评审（9 维度 100 分制 + §9 题型加权 + §10 Per-Qi）
│   ├── matlab-reviewer.md       Matlab 代码审查
│   ├── data-validator.md        数据质量验证
│   ├── data-explorer.md         快速 EDA 数据探索
│   ├── model-comparison.md      多模型并行对比
│   ├── citation-checker.md      引用一致性检查
│   ├── competition-prep.md      历史案例匹配备战
│   └── blind-panel-judge.md     ★ 盲评单座（v4.1，3 座并行之一）
│
├── .claude/skills/        ← ★ Claude Code Skill 包（67 个，v4.2 +3）
│   ├── [核心] 10 个流水线 skill（见上方 Native Skill 表，主轨道）
│   ├── [Legacy] 9 个手动 skill（scan/card/rules/analyze/review/code/defense/submit/figure，口令已统一入口取代）
│   ├── [新增] 10 个智能辅助 skill（model-selector/chart-recommender/defense-simulator/algorithm-runner/result-validator/paper-rewriter/diagram-maker/interactive-chart/math-figure/network-graph）
│   ├── [Nature] 9 个学术写作 skill（nature-polishing/writing/figure/citation/data/reader/response/paper2ppt/academic-search）
│   ├── [社区] 13 个社区 skill（zhnnky329 + Lupynow + academic-skills + Gabberflast + lishix520）
│   │   ├── symbol-table-builder        符号表自动构建
│   │   ├── robustness-checker          稳健性/灵敏度检查
│   │   ├── matlab-model-code-generator  MATLAB 代码生成
│   │   ├── python-code-reviewer        Python 代码审查
│   │   ├── matlab-code-reviewer        MATLAB 代码审查
│   │   ├── paper-polisher              论文润色
│   │   ├── solution-package-builder    提交包生成
│   │   ├── academic-defense-pptx       学术答辩PPT生成（Gabberflast）
│   │   ├── academic-paper-strategist   学术论文规划（lishix520）
│   │   ├── academic-paper-composer     学术论文写作（lishix520）
│   │   ├── aigc-reduce                AIGC降重/去AI味（xiaofenggan01）
│   │   ├── humanizer-zh-academic       中文学术写作降AIGC检测（redbaronyyyyy-eng）
│   │   └── csv-data-summarizer        CSV自动分析+可视化（coffeefuelbump）
│   ├── [GitHub融合] 8 个新增 skill（v3.6-v3.7）
│   │   ├── consistency-auditor         一致性审计（三审计层第一层）
│   │   ├── completeness-auditor        完整性审计（三审计层第二层）
│   │   ├── decision-logger             决策日志记录
│   │   ├── feature-engineering         特征工程标准化流程
│   │   ├── algorithm-benchmark         算法基准测试
│   │   ├── style-calibration           写作风格校准
│   │   ├── citation-tracer             引用溯源工具
│   │   └── ai-failure-checker          AI失败模式检查（7-mode checklist）
│   ├── [同级竞品融合 v4.1] 1 个新增 skill（handsomeZR + mathodology）
│   │   └── blind-panel                盲评 Panel（3 座 + 20 分冲突 + 真实稀缺性校准）
│   ├── [同赛道生态融合 v4.2] 3 个新增 skill（jihe520 + Gostyan + Kirito）
│   │   ├── typst-renderer             Typst 论文渲染（34 套赛事模板 + typst_index.json）
│   │   ├── docx-editor-cn             Word 原生公式（temml→docx）+ XML unpack/pack/validate
│   │   └── award-paper-rag            O 奖论文章节级 RAG（heading 分块 + 13 类分类器）
│   └── [工具] 4 个工具 skill（git-snapshot/algorithm-test/latex-renderer/word-counter）
│
├── prompts/               ← 31 个工作流提示词（00-30）
│   ├── MASTER_PROMPT_math_modeling.txt  总控提示词
│   ├── 00_route_task.md       任务路由
│   ├── 01-03                  扫描/抽卡/建规则
│   ├── 04-09                  审稿/模板/答辩/选题/审稿/答辩
│   ├── 10-18                  检验/题型/选模/结果/检验/摘要/低分/闭环/追问
│   ├── 19-21                  代码/图示/提交包
│   ├── 22-24                  回灌/开工/动态验收
│   ├── 25                     提示词总母版
│   ├── 26-28                  表格/PPT/终检
│   ├── 29                     知识更新
│   └── 30                     数据理解
│
├── outputs/               ← 规则/模板/知识库沉淀（74 文件 + 19 子目录）
│   ├── INDEX.md               ★ 统一索引（唯一入口 + 双向引用导航）
│   ├── knowledge_graph.md     ★ 知识图谱（实体-关系，Karpathy+GBrain 风格）
│   ├── scripts/
│   │   └── knowledge_graph_query.py  ★ 图谱查询脚本
│   ├── 系统调度层（11 文件）     task_router / asset_registry / file_map 等
│   ├── 建模选模层（13 文件）     method_matching / algorithm_templates 等
│   ├── 写作表达层（13 文件）     writing_templates / abstract_templates 等
│   ├── 审稿评分层（12 文件）     scoring_rubric / revision_checklist 等
│   ├── 答辩准备层（7 文件）      defense_qa_bank / defense_followup_chains 等
│   ├── 数据处理层（3 文件）      data_cleaning_standards 等
│   ├── 质量验收层（5 文件）      final_quality_gate 等
│   ├── 图表可视层（4 文件）      figure_templates 等
│   ├── 提示词调度（1 文件）      prompt_master_pack
│   ├── 提取文本/                 抽取文本存档
│   └── 案例子目录（19 个）       按算法分类的案例数据
│
├── paper_output/          ← ★ 当前赛题产物输出目录（v3.0 新增）
│   ├── OUTPUT_LAYOUT.md       输出位置说明
│   ├── final_paper.docx       正式 Word 论文（赛题产出时生成，历史稿在 _archive_*/）
│   ├── final_paper_source.md  Agent 写作源稿（赛题产出时生成，历史稿在 _archive_*/）
│   ├── step1/                 题意分析/大纲/评分对齐
│   ├── plan/                  模型路线/数据计划/图表计划/论文大纲
│   ├── code/                  赛题专用代码（data_processing/modeling/visualization/qa）
│   ├── data_cleaned/          清洗后数据
│   ├── results/               模型结果/指标/结论 JSON 契约
│   ├── tables/                论文表格 + table_index.json
│   ├── figures/               图表 + figure_index.json
│   ├── state/                 流水线状态机产物（pipeline_manager）
│   ├── research/              研究/融合报告（CHANGELOG 等）
│   └── qa/                    证据门禁/格式检查/工作流状态报告
│
├── problem_files/         ← ★ 赛题 PDF/Word 和附件（v3.0 新增，需手动放入赛题文件）
├── crawled_data/          ← 外部补充数据（可选）
│
├── resources/             ← 原始资料归档（按类别编号；真题入口是 problem_files/，补充竞赛资料在 09_竞赛资料/）
│   ├── 02_优秀论文/
│   ├── 03_方法算法/
│   ├── 04_代码模板/           14种必备算法 + 50种算法 + 创新型算法 + PMMAA算法与应用(79个notebook)
│   ├── 05_写作模板/           国赛论文模版 + AI使用详情模版
│   ├── 06_图表教程/           50+炫酷图表教程
│   ├── 07_提示词/             AI提示词汇总 + 五一赛提示词
│   ├── 08_参考资料/           速成讲义 + 速成资料汇总
│   ├── 09_竞赛资料/           C题资料 + 电工杯 + 五一赛 + MathorCup
│   ├── 10_算法cookbook/       ★ 8大类算法cookbook + 模型选型矩阵 + 问题分解（Lupynow）
│   ├── 11_题型playbook/       ★ 12个端到端题型playbook（Lupynow）
│   ├── 12_写作参考/           ★ 摘要/文献综述/模型验证/常用短语/国赛美赛指南（Lupynow）
│   ├── 13_LaTeX模板/          ★ CUMCM/MCM LaTeX模板（AutoMCM-Pro）
│   ├── 14_科学计算参考/       ★ scikit-learn/matplotlib/seaborn/statsmodels/sympy/networkx/统计分析
│   └── 15_Typst模板/          ★ 34 套赛事模板（17 Typst + 17 LaTeX，zh 14 赛事 + en 3，v4.2 jihe520）
│   └── _archive/              历史压缩包
│
├── deliverables/          ← 竞赛成品输出（手动/半自动产物）
│   ├── papers/               论文正文/摘要版
│   ├── code/                 Python/Matlab 代码
│   ├── figures/              图示（SVG/PNG）
│   ├── tables/               结果表格（CSV）
│   └── slides/               答辩材料/PPT
│
├── tools/                 ← 辅助工具（paper_search/visualization）
│
├── docs/                  ← MathModel-Skill 文档（v3.0 新增）
│   ├── SYSTEM_GUIDE.md        系统总指南
│   ├── agent-install-guide.md
│   ├── agent-native-workflow.md
│   ├── cumcm-paper-standard.md
│   ├── demo-walkthrough.md
│   ├── formal-paper-authoring.md
│   ├── generated-demo-workflow.md
│   ├── math-mcp-servers.md    数学/学术 MCP 配置（v4.3）
│   ├── output-layout.md
│   ├── prompt-assets.md
│   ├── starter-prompts.md
│   ├── workflow-contracts.md
│   └── （另有历史融合报告若干）
│
├── examples/              ← MathModel-Skill 示例（v3.0 新增）
│   ├── cumcm2024-b-demo/     2024国赛B题完整样例
│   └── quickstart/           最小安装验证示例
│
├── 05_我的作品/           ← 个人作品迭代区（含 五一赛/ 子目录）
└── nature-skills/         ← Nature 技能模块
```

---

## 核心工作流（单系统 · Skill 流水线）

> **v4.4 起：双系统已收敛为单生产系统**（math-model-producer 归档至 `resources/_archive/`）。
> **v3.4 起：触发词统一入口已取代旧"轨道 B"手动口令**——9 个 Legacy Skill 降级为内部调度工具，`prompts/` 降级为参考文档，不再是独立对等轨道。当前系统是**单轨道：Skill 流水线**。

### Skill 流水线（主轨道）

```
预检(problem_files非空) → 题意解析 → 模型路线 → 数据/图表计划
→ 生成赛题专用代码 → 运行真实结果 → 证据门禁 → 正式大纲
→ Agent全局写作 → Word排版 → 格式门禁 → 最终QA →（championship）盲评Panel + figqa碰撞门
```

### Prompt 工作流（Legacy 参考）

> `prompts/00-30` 的 31 个提示词文件仍保留为**参考文档**，用于灵活/局部任务和离线参考，但不再是与 Skill 并列的独立工作流。所有核心能力（审题/选模/代码/图表/评审/答辩/提交）均已由 Skill 统一入口覆盖（见下方口令映射）。

```
任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 →
代码/论文/图表生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌
```

---

## 必须遵守的 10 条规则

| # | 规则 | 入口文件 |
|---|------|----------|
| 1 | **Skill 优先路由** | `.claude/skills/paper-workflow-orchestrator/SKILL.md` |
| 2 | **Prompt 路由备选** | `prompts/00_route_task.md` 或 `outputs/task_router.md` |
| 3 | **评分唯一标准** | `outputs/scoring_rubric.md`（100 分制，7 维度，**不改分值**）；按 task_type 加权判等见 `outputs/dim_weights.json`（v4.1） |
| 4 | **优先复用沉淀** | `outputs/INDEX.md` 定位 → 调用对应模板 |
| 5 | **代码生成顺序** | 题型 → 模型 → 代码结构 → 主体代码 → 标注可运行/待补 |
| 6 | **论文写作顺序** | 结构 → 摘要 → 假设 → 模型 → 结果 → 检验 → 图示 |
| 7 | **证据门禁不通过不写稿** | `paper_output/qa/workflow_guard_report.md` 全绿才进入正式写作 |
| 8 | **格式门禁不通过不定稿** | 字数<18000/缺三级标题/图表未引用 → 不得称最终稿 |
| 9 | **最终质量门** | `outputs/final_quality_gate.md`（P0 未过不得提交） |
| 10 | **禁止编造** | 数据、文献、运行结果、p 值一律不得编造 |

---

## 口令映射

### Legacy 口令（v3.4 统一入口已取代原轨道 B）

| 口令 | 路由 | 默认输出 |
|------|------|---------|
| 先扫一遍资料 | `scan` skill | 文件地图+优先级 |
| 抽卡 | `card` skill | 知识卡片 |
| 建规则库 | `rules` skill | 评分表/方法匹配表更新 |
| 审题 / 选模 | `analyze` skill（统一入口） | 全量：题型+路线+代码模板+风险+检验包 |
| 审论文 / 打分 / 严格打分 | `review` skill → `paper-reviewer` agent（统一入口） | 全量深度报告（9部分） |
| 生成代码 | `code` skill | 从零生成代码（末节引 algorithm-runner） |
| 运行算法 / 执行代码 | `algorithm-runner` skill | 执行已有模板（末节引 code） |
| 生成图示 / 画图 / 流程图 / 网络图 | `figure` skill（统一入口） | 全量：自动判断→分派子skill→全部图表+索引 |
| 准备答辩 / 模拟答辩 | `defense` skill（统一入口） | 全量：问答+追问+模拟评分+短答+风险 |
| 生成提交包 | `submit` skill | 比赛提交包（自动判断阶段） |

### 工具口令

| 口令 | 对应操作 |
|------|----------|
| 渲染公式 / LaTeX转图片 | 扫描论文 LaTeX 公式 → 渲染为 PNG → 生成公式清单 |
| 字数统计 / 多少字了 | 分段统计中英文 → 图表公式计数 → 对标 18000 字 |
| 润色论文 / 改写 / polish | `paper-polisher` skill（统一入口）→ 完整12点检查+段落改写+变更摘要+质量评分 |
| 构建符号表 / build symbol table | 统一所有子问题符号定义，检查冲突 |
| 鲁棒性检验 / robustness check | 灵敏度/误差/基线对比检验 |
| 降AI味 / 降重 / 去AI检测 | 默认 `humanizer-zh-academic`（14种AI模式+7项硬约束+60分制）；备选 `aigc-reduce` |
| 准备解决方案包 / solution package | 整合建模解释+结果分析 → 论文写作材料包（写作中间产物，非最终提交包） |
| 特征工程 / feature engineering | `feature-engineering` skill → 数据预处理、转换、编码、缩放、特征选择 |
| 算法基准测试 / benchmark | `algorithm-benchmark` skill → 比较不同算法性能、精度、速度 |
| 论文检索 / search papers | `tools/paper_search/scripts/search_papers.py` → 从Semantic Scholar/arXiv搜索论文 |
| 写作风格校准 / style calibration | `style-calibration` skill → 从用户过往作品学习写作风格 |
| 引用溯源 / citation check | `citation-tracer` skill → 验证引用真实性、追踪引用来源 |
| AI失败模式检查 / AI failure check | `ai-failure-checker` skill → 7-mode blocking checklist（编造/幻觉/逻辑错误等） |
| 一致性审计 / consistency audit | `consistency-auditor` skill → 数字/文件/符号交叉一致性检查 |
| 完整性审计 / completeness audit | `completeness-auditor` skill → 审查文件/报告/产物齐全检查 |
| 记录决策 / log decision | `decision-logger` skill → 记录用户在选模/结果判断的决策理由 |
| 盲评 / 盲审 / 模拟评委 / 校准打分 / panel | `blind-panel` skill（v4.1）→ 3 座独立盲评 + 20 分冲突仲裁 + 真实稀缺性校准 |
| 升级到 championship / 切到 fast | orchestrator 模式切换（v4.1）→ 启用/关闭 L3+L4+盲评+figqa |
| 做 L2 回检 / 跨阶段一致性检查 | qa-auditor 反馈层 L2（v4.1）→ 定向回滚不重做整阶段 |
| 图表碰撞门 / figqa check | `math-figure/scripts/figqa.py`（v4.1）→ bbox 零碰撞 + 从编译 PDF 建 contact sheet |
| **Typst 渲染** / 编译 Typst / 用 Typst 排版 | `typst-renderer` skill（v4.2）→ 34 套赛事模板选型 + md→typst 注入 + 编译 PDF（3 次重试） |
| **编辑 Word** / 改 Word 公式 / 局部修改 docx | `docx-editor-cn` skill（v4.2）→ temml→MathML→docx 原生公式 + XML unpack/pack/validate |
| **查优秀论文** / O 奖论文检索 / 章节检索 | `award-paper-rag` skill（v4.2）→ heading 章节级 RAG（254 篇→6863 节点），`retrieve` 离线、`chat` 需 key |
| **流水线状态** / 推进阶段 / 返工 / 并行启动 | `qa-auditor/scripts/pipeline_manager.py`（v4.2）→ GitOps 状态机 + AP/Manual + 返工上限 |
| **G4.6 自证门** / 验证所有模型 | `qa-auditor/scripts/verify_gate.py`（v4.2）→ 每模型 verify_*.py 全 PASS 才引用 |
| **数值合理性** / inf nan 检查 | `qa-auditor/scripts/check_numeric_sanity.py`（v4.2）→ 通用 inf/nan/量级扫描 |
| **报告新鲜度** / 校验报告是否过期 | `context-memory-keeper/scripts/freshness_check.py`（v4.2）→ SHA-256 源哈希，旧报告标记 STALE |
| **安全检查** / 密钥扫描 / 注入防护 | `consistency-auditor/scripts/security_check.py`（v4.2）→ 密钥/路径/Markdown 注入（git commit 前自动拦截） |
| **编译 LaTeX** / latex 编译 | `paper-formal-writer/scripts/compile_latex.py`（v4.2）→ 2 pass + 失败重试 3 次（解析 .log 错误行） |
| **提取表格** / PDF 表格 / Camelot | `data-cleaning/scripts/extract_pdf_tables.py`（v4.3）→ 赛题附表一键转 CSV/Excel + 索引 |
| **公式 OCR** / 提取公式 / 图片转 LaTeX | `problem-doc-model-selector/scripts/extract_formulas_ocr.py`（v4.3）→ Pix2Text 公式识别 |
| **期刊风图表** / 图表美化 / SciencePlots | `math-figure/scripts/journal_style.py`（v4.3）→ IEEE/Nature/Science 76 样式 |
| **保留格式降重** / Word 格式保留 | `aigc-reduce/scripts/replace_docx_preserve_format.py`（v4.3）→ 改写降 AIGC 后原地放回 .docx 不破坏排版 |
| **模型可解释性** / 特征重要性 / SHAP | `feature-engineering/scripts/shap_explain.py`（v4.3）→ SHAP 条形/蜂群/依赖/waterfall 图 |
| **超参调优** / 调参 / Optuna | `model-code-and-result-generator/scripts/optuna_tune.py`（v4.3）→ TPE 贝叶斯优化（XGBoost/LightGBM/RF/SVR） |
| **拉宏观数据** / 经济数据 / akshare | `authoritative-data-harvester/scripts/akshare_fetch.py`（v4.3）→ GDP/CPI/股价/行业产量等 |
| **跑 MATLAB** / 执行 .m / matlab 运行 | `matlab-model-code-generator/scripts/matlab_runner.py`（v4.3）→ 无头 `matlab -batch` + 收 png/csv/mat + .mat→JSON + 3 能力模板（曲线拟合/优化/ODE） |

---

## 改稿优先级

- **P0**：不改会严重失分或无法自圆其说
- **P1**：影响质量和说服力
- **P2**：润色和冲高分增强

---

## 回复风格

- 准确、直接、克制、结构清晰
- 面向竞赛实战，避免空话套话
- 实战表达：「这里的主要问题是……」「更稳妥的写法是……」「这一步容易失分，因为……」
