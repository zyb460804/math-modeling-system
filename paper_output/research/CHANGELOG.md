# 数学建模生产系统 CHANGELOG（v4.0 → v4.9）

> 一处看全系统的演进。每轮的定位、来源、新增、修改、报告链接。
> 最新在前。完整系统规则见 [CLAUDE.md](../../CLAUDE.md)，统一索引见 [outputs/INDEX.md](../../outputs/INDEX.md)。

---

## 演进总览

```
v4.0 (2026-07)  大规模融合（15 仓库）——打地基：合同体系/门控 G1-G6/Cookbook/Playbook/算法模板
   ↓
v4.1 (2026-07-22) 同级竞品（2 仓库）——评分质量：盲评 Panel/figqa/dim_weights/4 层反馈/3 模式
   ↓
v4.2 (2026-07-23) 同赛道生态（5 仓库）——交付链路+工程纪律：Typst/GitOps/G4.6 自证/docx 公式/RAG/新鲜度
   ↓
v4.3 (2026-07-23) 工具链增强（7 源）——单点提效：Camelot/Pix2Text/SciencePlots/SHAP/Optuna/akshare/aigc-deslop
   ↓
v4.4 (2026-07-25) 系统整理+实测验证——单系统成型：双系统归档/RAG 去重重建/路由全面更新/门禁实测跑通
   ↓
v4.5 (2026-07-26) 全面体检+断链清零——8 维度审计 37 发现全处置：P0 门禁修复/11 缺失脚本落地/QA 去硬编码/环境补齐
   ↓
v4.6 (2026-07-30) 学术方法论融合——usail-hkust/LLM-MM-Agent (NeurIPS 2025)：HMML 分层方法库+actor-critic 选模+美赛分题策略+scikit-opt 桥接
   ↓
v4.7 (2026-08) 图片嵌入链路加固——G4.10 图片嵌入门（image_embed_check.py）+ pandoc/md 纯文字"见图N"不嵌图坑修复
   ↓
v4.8 (2026-08-02) 第四档 skill 大扫除——归档 14 个 skill、消化方法论、新建 defense-ppt-builder-zh、prompts/ 全量归档，67→54
   ↓
v4.9 (2026-08-03) championship 默认 + 交付链 P0（OMML 公式渲染/resolve_path/figure_index）+ pipeline_runner 一键调度 + 门禁三轮加固（2026-08-15 波次）
```

| 版本 | 定位 | 新 Skill | 新脚本 | 关键能力 |
|------|------|---------|--------|---------|
| **v4.9** | 用户偏好固化 + 交付链 P0 + 一键调度 | 0 | +1（pipeline_runner） | championship 默认（escape hatch 才降级）/ format_formal_docx 跨 skill 复用 latex_to_omml / resolve_path 多候选 / pipeline_runner 9 阶段接力 / 门禁三轮加固（fail-closed + verdict 真消费 + blind_panel_schema 两链同口径） |
| **v4.8** | 第四档 skill 大扫除 | +1（defense-ppt-builder-zh）−14（归档） | +0（+7 references） | 归档 14 skill（9 Nature + 5 低频）/ 67→54 / prompts 32 文件全量归档 / G5 门禁矩阵 v1.1 / settings 精简 |
| **v4.7** | 图片嵌入链路加固 | 0 | +1（image_embed_check） | G4.10 图片嵌入门：Markdown `![](path)` 计数 vs Word `word/media/*` 实际内嵌数，防"见图N"纯文字漏检 |
| **v4.6** | 学术方法论融合 | 0 | 0（+8 参考文档） | HMML 97 方法分层库 / actor-critic 选模 / 美赛 A-F 分题策略 / scikit-opt 7 启发式桥接 |
| **v4.5** | 全面体检 + 断链清零 | 0 | +11（补落地） | P0 图表门禁修复 / 11 断链脚本实现 / QA 配置驱动化 / RAG 链路解阻 / docx 公式链环境补齐 / 文档失实 10 处修正 |
| **v4.4** | 系统整理 + 实测验证 | 0 | 0 | 双系统→单系统归档 / RAG CSV 去重 254→251 + 索引 rebuild 6863 节点 / 路由 20+ 处更新 / 门禁实测跑通 |
| **v4.3** | 单点工具提效 | 0（挂现有 skill） | +7 | PDF 表格 / 公式 OCR / 期刊风图表 / SHAP / Optuna / akshare / Word 保留降重 |
| **v4.2** | 交付链路 + 工程纪律 | +3 | +13 | Typst 34 模板 / GitOps 状态机 / G4.6 自证 / docx 公式 / 章节级 RAG / SHA-256 新鲜度 / 4 层容错 / 双 Agent |
| **v4.1** | 评分与图表质量 | +1（blind-panel） | +5（修正器/反馈层） | 盲评 3 座 + 20 分冲突 / figqa 碰撞门 / dim_weights 题型加权 / L1-L4 反馈 / fast-standard-championship 3 模式 |
| **v4.0** | 地基（合同 + 门控 + 知识库） | +8（社区） | 22 算法模板 | Model/Figure Contract / G1-G6 门控 / 95+ 选型矩阵 / 8 Cookbook / 12 Playbook / Anti-AI 写作 / 100+ O 奖库 |

累计（截至 v4.9）：**54 个 active skill（v4.8 大扫除后；另有 14 个归档于 `.claude/skills/_archive/`）/ 30+ 新脚本 / 34 套 Typst 赛事模板（372 模板文件）/ 81MB RAG 索引 / 6 数学 MCP 文档 / HMML 97 方法分层库**。

---

## v4.9 — championship 默认 + 交付链 P0 + pipeline_runner（2026-08-03，加固波次至 2026-08-15）

**定位**：用户偏好固化为默认模式；修复交付链三处 P0；把 orchestrator 路由逻辑代码化为一键调度器。

**championship 默认（用户偏好固化）**：
- 每次解题默认走 3 座盲评 Panel + figqa 碰撞门 + 4 层反馈 L1-L4，不再按 deadline 自动降级（v4.1 原为自动推荐）
- escape hatch 保留：用户说"切 fast"/"这次用 standard"才偏离；deadline <6h 只"建议"降级、确认才改
- 落点：`paper-workflow-orchestrator/SKILL.md` 运行模式段重写 + CLAUDE.md 7 处同步（头部摘要/触发词表/完整流水线/交付门禁/主轨道流水线/口令映射/v4.1 触发词表）

**交付链 P0 修复（三件）**：
- `paper-formal-writer/scripts/format_formal_docx.py` 公式渲染链重写：**真 import 跨 skill 复用** `docx-editor-cn/scripts/formula.py::latex_to_omml`（`_locate_docx_editor_scripts()` 从脚本文件位置逐级上溯定位，不依赖 cwd）；480 个 `$...$`/`$$...$$` 全转 Word 原生 OMML，覆盖 body/center/heading/list/表格 cell 5 路径；失败退化 Cambria Math 纯文本并计 `_OMML_STATS`（DEGRADED 可见）
- `resolve_path` 多候选路径查找：相对路径依次尝试 `paper_output/` → 项目根（修复图片路径解析，6 张图全嵌入）；含绝对路径/`..`/越界/扩展名白名单四重安全门
- `paper_output/figure_index.json` / `tasks.json` 补齐（证据门禁 PASS）

**pipeline_runner 一键调度（`tools/quality_gate/pipeline_runner.py`）**：
- 9 阶段状态机（S1 审题 / S2 选模+G2.5 / S3 代码 / S3b 自证 G4.6 / S4 结果+G4.5 / S5 证据门 / S6 写作 / S7 格式门 / S8 终检），对齐 pipeline_manager 的 STAGE_ORDER
- 脚本型阶段（S3b/S5/S7/S8）自动 subprocess，PASS 才推进；认知型阶段输出 AGENT_HANDOFF（退出码 2 等 Agent 接力）；produces 文件齐备的 agent 阶段自动推进
- championship 接线：check_numeric_sanity → S5、freshness_check → S8 前、blind_panel_report.json 存在性 → S8 产物门；figqa 为 live 检测不硬接脚本（S4/S6 handoff 提示）

**门禁三轮加固（2026-08 波次，commits 4de1292 / 615d99f / 2b938af）**：
- 第一轮（4de1292）：门禁 fail-closed（checker 缺失即 FAIL，显式 skip 旗标留痕）、审批门强制、密钥 redact
- 第二轮（615d99f）：B7 审批消费错位修复 + verdict 真消费（枚举 pass|refine|block 且仅 pass 放行）+ 旧门禁误报雷区清零
- 第三轮（2b938af）：终检 verdict 真消费 + 幽灵条目 CRITICAL + freshness 真接线 + 锚定统一（`_project_root.py::find_project_root` 替代 Path.cwd，format_formal_docx 等受益）
- 脚本侧自我标注版本：pipeline_runner v4.9.1-v4.9.3、final_gate_runner v4.10.1（`blind_panel_schema.py` 两链共用盲评校验；G4.8 双口径+阈值可配；SKIP≠PASS 三态展示）

**报告**：本轮无独立融合报告；来源为本 CHANGELOG 回填 + CLAUDE.md v4.9 摘要 + 脚本 docstring 溯源（2026-08-15 审计补录）。

---

## v4.8 — 第四档 skill 大扫除（2026-08-02）

**定位**："能转化的转化，不能的删除"。skill 总数 67→54，第四档"几乎不触发"从 16 个→2 个（typst-renderer + docx-editor-cn 保留为可选交付链路）。

**归档 14 个 skill** → `.claude/skills/_archive/`（git mv 可恢复）：
- 9 个 Nature：nature-polishing / nature-writing / nature-figure / nature-paper2ppt / nature-reader / nature-academic-search / nature-citation / nature-data / nature-response
- 5 个低频：academic-paper-strategist、academic-paper-composer（哲学论文，与竞赛无关）、academic-defense-pptx（并入新 skill）、csv-data-summarizer、result-validator

**方法论精华 100% 消化**：6 份新 references（ai-traffic-light / english-academic-writing / figure-evidence-layering / bilingual-reader-protocol / multi-source-search / result-validation-rules）+ quick-eda-protocol + 1 个新 references 整合 csv 能力。

**新建 1 个 skill**：`defense-ppt-builder-zh`（国赛中文答辩 PPT 生成器，融合 nature-paper2ppt + academic-defense-pptx）。

**配套**：G5 门禁矩阵 v1.1（`tools/quality_gate/skill_applicability_matrix.json` 含 archived_skills 清单）；settings.json 删 14 个注册 + 添 defense-ppt-builder-zh + blind-panel；`prompts/` 32 个文件全量归档至 `prompts/_archive/`（实测 0 调用，100% 有 skill 替代）。

**报告**：`outputs/nature_skills_bridge.md` v3.0 + `prompts/README.md` 归档公告。

---

## v4.7 — 图片嵌入链路加固（2026-08）

**定位**：堵住"md 写'见图N'纯文字、Word 实际无图"的交付漏洞。

**新增 G4.10 图片嵌入门**：`tools/quality_gate/image_embed_check.py`——比对 Markdown `![](path)` 语法引用数与 Word 解包后 `word/media/*` 实际内嵌图数；pandoc 链路下 md 里写"见图N"纯文字不会嵌图（必须 `![](path)` 相对路径 + 正确工作目录），旧格式门禁不查此项。

> 溯源说明：本节依据 `paper-workflow-orchestrator/SKILL.md` 阶段路由表（G4.10 标注 v4.7）与 `final_gate_runner.py` 八门清单回填（2026-08-15 审计补录），无独立融合报告。

---

## v4.6 — 学术方法论融合（2026-07-30）

**定位**：引入学术界数学建模智能体的方法论资产。来源 `usail-hkust/LLM-MM-Agent`（NeurIPS 2025 录用 + ICML 2025 AI4MATH Workshop，辅助两支本科生队获 MCM/ICM 2025 Finalist 前 2%）。纯加法（落地参考文档+知识库），不改骨架与流水线代码。

**核心移植**：

| 移植资产 | 落地位置 | 增量价值 |
|---------|---------|---------|
| **HMML 分层建模方法库** | `model-selector/references/hmml/`（HMML.json 180KB + HMML.md 162KB + README.md） | 5 domain（OR/Optimization/ML/Prediction/Evaluation）/ 18 subdomain / 97 method node 三层知识树；选模从"场景→算法"升级为"问题→domain→subdomain→method"分层检索，与 model-selection-matrix（95+场景直查）互补 |
| **actor-critic 选模算法指南** | `model-selector/references/hmml-retrieval-guide.md` | MethodScorer 自顶向下逐层打分（叶子 final_score = 父路径均分×0.5 + 自身分×0.5）、LLM 批判 + embedding 相似双模式、top_k=6 推荐+PoC 验证流程 |
| **美赛题型分题策略** | `problem-doc-model-selector/references/mcm-decompose-strategy.json+md` | A-F 六题型 × 3/4/5 子任务数分题原则 + decompose→refine 两步流程；与 analyze skill 的 problem_analysis.json/sub_problems 衔接 |
| **scikit-opt 启发式算法桥接** | `model-code-and-result-generator/references/heuristic-algo-scikit-opt.md` | 7 种群体智能算法（DE/GA/PSO/SA/ACA/IA/AFSA）一行调用示例 + 与 cookbook-optimization 手写版的分工（库做 baseline/快速出结果，手写做创新/可定制） |

**修改**：3 个 SKILL.md 各追加参考资源引用（model-selector +2 行 / problem-doc-model-selector 新增参考资源段 / model-code-and-result-generator +1 段）。

**跳过**（非方法论/强 LLM 依赖）：`llm/`（运行时 API）、`utils/embedding.py`、`demo/`（Next.js 前端）、`code_template/main1-10.py`（具体题目代码）。

**验证**：HMML.json MD5 与源一致（原样复制）、json.load 解析 97 method node、8 新文件 + 3 SKILL.md 引用全部到位。

---

## v4.5 — 全面体检 + 断链清零（2026-07-26）

**定位**：系统健康度。不引入外部融合，用 8 维度多智能体审计（门禁脚本/skill 完整性/JSON 配置/RAG 索引/文档一致性/垃圾扫描/代码编译/依赖环境）产出 37 条发现（P0×1 / P1×14 / P2×22），全部处置。

**P0 修复**：
- `math-figure/scripts/render_check.py` 编译期 SyntaxError（`global FIGURES_DIR` 先用后声明）→ 该脚本被 orchestrator / gate-system / auto_detect_and_fix 等 5 处引用，意味着图表质量门禁（figure/s6/all 阶段）自 v3.6 上线以来从未真正执行过。已改为参数传递去除 global 副作用，CLI 文档同步为子命令写法（`check --figure` / `check-all --dir`）。

**断链清零（11 个"文档引用但从未落地"的脚本全部实现 + 冒烟通过）**：
- citation-tracer：`verify_citation.py` + `verify_all_citations.py`（GB/T 7714 要素检查 + 双向匹配 + 可选 CrossRef 在线核验，网络失败自动降级）
- style-calibration：`analyze_style.py`（风格画像 JSON）+ `apply_style.py`（偏差检测报告，改写由 agent 执行）
- academic-paper-composer：`chapter_quality_check.py` + `final_evaluation.py`；另将 2 个错位 md 归位 `references/`
- academic-paper-strategist：`evaluate_samples.py` + `gap_analysis.py`；另将 2 个错位 md 归位 `references/`
- ai-failure-checker：`check_failures.py`（7-mode 离线扫描，冒烟 7/7 抓出 + 干净样本 0 误报）
- algorithm-benchmark：`benchmark_evaluation.py`（6 模型 5 折 CV 排名）
- feature-engineering：`preprocess.py`（缺失/编码/缩放/IQR 异常值 CLI）

**QA 门禁配置驱动化（消灭假绿灯）**：
- `check_parameter_consistency` / `check_result_reasonableness` / `run_sensitivity_analysis` / `run_baseline_comparison` 四脚本的旧赛题（绿电直连型合成氨）硬编码全部外置到 `paper_output/plan/qa_config.json`；schema 示例（原硬编码值搬入存档）：`quality-assurance-auditor/references/qa_config.example.json`；**缺配置显式 SKIP（exit 0），绝不 PASS**
- `pipeline.py` / `check_numeric_sanity.py`（+`--results-dir`）/ `check_paper_format.py`（+`--source`）补 argparse，`--help` 不再触发主逻辑写报告

**RAG 链路解阻（award-paper-rag）**：
- papers.csv 2 行残留 `' .md'` 空格路径修正 → `python -m scripts.mmqa split` 语料再生成命令解阻
- nodes jsonl 重生成 6910→6863，与向量索引节点数完全对齐（消除 3 篇论文 47 个重复节点，兜底重建不再产出污染索引）
- requirements.txt 从脱节的 meta 包改为实际 5 依赖（llama-index-core / embeddings-openai / llms-openai / embeddings-huggingface / sentence-transformers）

**环境补齐**：
- docx-editor-cn `npm install` 完成（docx / fast-xml-parser / temml）+ pandoc 3.10 安装 → **Word 原生公式链（temml→MathML→OMML）全线可用**
- 未装（分支标注）：MiKTeX（LaTeX 编译分支需先装，Typst 分支可替代）、pix2text（公式 OCR，赛前按需装）

**文档一致性（CLAUDE.md 10 处失实修正）**：
- 删除不存在的 `01_真题与附件/`（真题入口 = `problem_files/`）、MASTER_PROMPT 移至 prompts/ 节点、skill 计数 7→8 / 16→13、G4.6 双脚本补全路径、paper_output 树注归档、docs/ 补录、tools/ 入树、render_check 用法改子命令、质量保障脚本表注配置驱动
- completeness-auditor SKILL.md 死命令改指 `symbol_auto_fixer.py`

**清理**：
- 16 个 `.DS_Store`/`Thumbs.db`、7 个空占位目录（13_LaTeX模板 3 个 + tools 4 个）、tools/README v1.1 对齐实际
- resources 约 32.8GB 完整重复实锤（03 合集 2137 文件与 09 逐一相同 + 嵌套拷贝 409 文件零独有）；删除命令因会话权限拦截备于 `resources/03_方法算法/README_国赛C题合集已去重.md` 待手动执行

**统一验证**：130 个 .py 编译 0 失败 / 16 必需文件全在 / 13 关键脚本 `--help` 全过 / papers.csv 残留 0 → ALL PASS。

---

## v4.4 — 系统整理 + 实测验证（2026-07-25）

**定位**：单生产系统成型。无外部融合，聚焦架构收敛与实测。

- **架构**：math-model-producer 归档至 `resources/_archive/`（双系统→单系统）
- **RAG**：papers.csv 去重 254→251、md 文件名尾随空格根因修复（`_safe_id` 截断后再 strip）、向量索引 rebuild（6863 节点）
- **文档**：单系统路由全面更新（asset_registry / task_router / knowledge_update / deduplication / prompts-29 / README / AGENTS 共 20+ 处）、3 个自动清单加迁移公告
- **实测**：预检/状态门/门禁脚本跑通（`evidence_gate` 真实发现 Q3/Q5 缺评价指标、`check_paper_format` 发现 Word 缺图）、RAG 实测召回储能/微电网论文、11 个工具脚本 `--help` 通过
- **清理**：39 个 `__pycache__` + 临时垃圾 + 重复 zip、`paper_output` 归档分层（`_archive_2026-06` / `_archive_2026-07_绿电直连型`）
- **遗留（v4.5 已处置）**：papers.csv path 列 2 行空格漏改、nodes jsonl 未随索引重建同步去重

---

## v4.3 — 工具链增强（2026-07-23）

**定位**：单点工具提效。不改主流程，脚本挂现有 skill 按需调用。

**来源（7 个）**：atlanhq/camelot(3716★) · breezedeus/Pix2Text(3195★) · garrettj404/SciencePlots(~5k★) · huanghfzhufeng/aigc-deslop(18★) · Optuna(14549★) · SHAP/shapash(3247★) · akshare(~10k★)

**新增脚本（7）**：
- `extract_pdf_tables.py`（Camelot，PDF 表格→CSV，✓ 真实提取 A题.pdf）
- `extract_formulas_ocr.py`（Pix2Text，公式图→LaTeX）
- `journal_style.py`（SciencePlots，76 期刊样式，✓ 出图）
- `replace_docx_preserve_format.py`（aigc-deslop，Word 格式保留降重，55%→11%）
- `shap_explain.py`（SHAP 特征重要性，ML 可解释性）
- `optuna_tune.py`（Optuna TPE 超参调优）
- `akshare_fetch.py`（宏观/金融/行业数据，C 题刚需）

**新增文档**：`docs/math-mcp-servers.md`（6 个数学 MCP 配置，命令已校准）

**已装包**：SciencePlots 2.2.2 / camelot 2.0.0 / shap 0.51 / optuna 4.9 / akshare 1.18.75

**路由同步**：CLAUDE.md 工具口令 +7 · task_router §十五 · orchestrator 阶段表 +7 · 00_route_task 速查

**报告**：[github_fusion_v4.3_report.md](github_fusion_v4.3_report.md)

---

## v4.2 — 同赛道生态融合（2026-07-23）

**定位**：交付链路 + 工程纪律。新 skill + 新门控 G4.6。

**来源（5 个）**：jihe520/MathModelAgent(2862★) · RealSeaberry/AutoMCM-Pro(144★) · Gostyan/docx-skill-4-cn-paper(335★) · Kirito-Elucidator/MathModel-QA-Engine(10★,F奖) · yushui2022/MathModel-Skill(217★,同源)

**新增 Skill（3）**：
- `typst-renderer` — Typst 交付链路（34 套赛事模板：17 Typst + 17 LaTeX，zh 14 赛事 + en 3）
- `docx-editor-cn` — Word 原生公式（temml→MathML→docx OMML）+ XML unpack/pack/validate 局部编辑
- `award-paper-rag` — O 奖论文章节级 RAG（heading 分块 + 13 类分类器，254 篇→6863 节点→81MB 索引，离线 retrieve）

**新增脚本（13）**：
- GitOps 状态机：`pipeline_manager.py`（AP/Manual + 返工上限 + 并行阶段）
- 强制代码自证：`verify_gate.py` + `verification_template.py`（**G4.6 门**）
- 数值合理性：`check_numeric_sanity.py`（通用 inf/nan/量级）
- 安全：`security_check.py` + `precommit_secret_guard.py` hook（密钥/路径/注入防护，已接入 settings.json）
- 容错：`fallback_router.py` + `fallback_routes.json`（L2，7 类备用链）
- 新鲜度：`freshness_check.py`（SHA-256）
- HIL：`parse_hil_action.py`（6 动作 confirm/edit/regenerate/ask/skip/abort）
- Typst：`build_typst_index.py` + `inject_typst.py`
- 语料：`corpus_converter.py`（多根目录吞本地文章）
- LaTeX：`compile_latex.py`（2 pass + 重试 3 次）

**新增门控**：**G4.6 RESULTS_SELF_VERIFIED**（每模型 verify_*.py 全 PASS 才冻结）

**新增参考文档**：`hil_6_actions.md` · `four_layer_fault_tolerance.md`（L1-L4 容错）· `dual_agent_design.md`（推导↔编码解耦）

**报告**：[github_fusion_v4.2_report.md](github_fusion_v4.2_report.md)

---

## v4.1 — 同级竞品融合（2026-07-22）

**定位**：评分与图表质量。

**来源（2 个）**：handsomeZR-netizen/mathmodel-skill v6.1(153★) · sweetcornna/mathodology(37★)

**新增 Skill（1）**：`blind-panel`（盲评 Panel，3 座独立盲评 + 20 分冲突仲裁 + 真实稀缺性校准）

**新增能力**：
- 题型差异化加权：`outputs/dim_weights.json`（competition×task_type×stage×dim，[0.7,1.5]）
- empirical 分题型分位：`outputs/empirical.json` v2.0（by_topic A-F，A 题 figure p50=8）
- 4 层反馈机制：L1 阶段 Critic / L2 跨阶段回检 / L3 独立 Panel / L4 证据校准
- figqa 图表碰撞门：bbox 零碰撞 + 从编译 PDF 建 contact sheet
- 3 模式：fast / standard / championship（按 deadline 自动推荐）
- Friendly Mode：问答式（AskUserQuestion）
- Per-Qi 加权聚合：多子问题独立评分，只 refine 挂科 Qi

**报告**：[tier1_diff_and_port_report.md](tier1_diff_and_port_report.md)

---

## v4.0 — 大规模 GitHub 融合（2026-07）

**定位**：打地基。合同体系 + 门控架构 + 知识库 + 算法模板。

**来源（15 个）**：XiaoMaColtAI(338★) · zhnnky329(191★) · Lupynow(99★) · ravenxrz(526★) · Lanrzip(495★) · RabbitWhite1(217★) · leost123456(177★) · Giyn(104★) · HeXavi8(87★) · qiziqiang(176★) · FinDii · szilard · Imbad0202 等

**新增参考文档（合同 + 门控）**：
- `model-contract-template.md` / `figure-contract-template.md`（前置合同）
- `gate-system.md`（G1-G6 门控，含人工门 G2.5/G4.5）
- `frozen-numbers-convention.md`（数字冻结机制）
- `poc-validation-gate.md`（PoC 验证门禁 ≤30 行）

**新增选型资源**：`model-selection-matrix.md`（95+ 场景决策矩阵）· `problem-decomposition.md`（12 型问题分类）· 12 个 `playbooks/`

**新增领域 Cookbook（8）**：optimization / ml / evaluation / mechanistic / statistical / network / clustering / game-theory

**新增写作增强**：`anti-ai-detection-guide.md` · `four-round-self-review.md` · `section-architecture.md` · `evidence-pyramid.md` · `common-phrases.md` · `literature-review-guide.md`

**新增算法模板（22）**：DEA / FAHP / RSR / GRA / NSGA-II / 灰色预测 / 马尔可夫 / HMM / 高斯过程 / MK 突变检验 / 贝叶斯网络 / MCMC / 排队论 / 元胞自动机 / 小波分析 / BP 神经网络 等

**新增资源库**：100+ O 奖论文（MCM/ICM 2016-2020）· 90+ 经典题解 · 32 种方法教材 · 60+ 灵敏度论文 · 3 版 LaTeX 模板

**新增 Skill（8，社区融合 v3.6）**：consistency-auditor / completeness-auditor / decision-logger / feature-engineering / algorithm-benchmark / style-calibration / citation-tracer / ai-failure-checker

---

## 版本间关系（互补，无冲突）

```
v4.0 地基      ─┐
v4.1 评分质量  ─┤→  共同构成完整生产系统
v4.2 交付纪律 ─┤   每轮只加，不替换骨架
v4.3 单点提效 ─┘
v4.4-v4.5 系统整理与体检（收敛为单系统 + 断链清零）
v4.6-v4.7 方法论与交付链增补（HMML / G4.10）
v4.8 收缩（归档 14 + prompts 下线，67→54）
v4.9 默认冲奖模式 + 一键调度 + 门禁加固
```

- **v4.0/v4.1** → 评分与图表质量（合同/门控/盲评/选型）
- **v4.2** → 交付链路与工程纪律（Typst/GitOps/自证/RAG）
- **v4.3** → 单点工具提效（PDF/OCR/SHAP/Optuna/数据）
- **v4.8/v4.9** → 默认行为固化（championship）与调度/门禁收敛

## 待决策 / 未完成项

| 事项 | 版本 | 状态 |
|------|------|------|
| docx-editor-cn npm install（Node.js ≥18） | v4.2 | ✅ v4.5 已完成（含 pandoc 3.10） |
| 6 个数学 MCP 实际接入 | v4.3 | 用户侧 `claude mcp add`（文档已备） |
| Pix2Text 模型下载 | v4.3 | 按需首装（设 HF 镜像，赛前建议预装） |
| MiKTeX/TeX Live（LaTeX 编译分支） | v4.5 | 未装（用户选择暂不装；Typst 分支可替代） |
| resources 32.8GB 重复删除 | v4.5 | 已校验实锤，命令备于 `resources/03_方法算法/README_国赛C题合集已去重.md` 待手动执行 |
| Tier 2（Mermaid/GraphRAG/Streamlit） | v4.3+ | 待用户决策 |
| G5.5 humanizer 阈值口径统一（skill_invocation_gate 生效值 40 vs pipeline_runner S6 handoff 文案 58） | v4.9 | 待统一（skill_invocation_gate.py 内 TODO H-12 已标注） |
| 门禁编号"G5"一词三义（阶段门 G5 / 终检链 G5 ××门 / G5.1-G5.9）统一或别名化 | v4.9 | 待决策（2026-08-15 审计已在各路由文档加消歧注） |
