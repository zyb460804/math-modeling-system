# GitHub 融合报告 v4.2（9 批次 / 5 仓库 / 26 新建文件）

- **执行日期**：2026-07-23
- **调研范围**：8 组关键词 × GitHub Search API，抓取 10 候选仓库 README + 文件树
- **源仓库（本次融合）**：
  - `jihe520/MathModelAgent`（2862★）— Typst 模板 + HIL 6 动作 + 4 层容错
  - `RealSeaberry/AutoMCM-Pro`（144★）— GitOps 状态机 + 强制自证 + 注入防护 + 数值检查
  - `Gostyan/docx-skill-4-cn-paper`（335★）— temml→docx 公式链 + XML unpack/pack
  - `Kirito-Elucidator/MathModel-QA-Engine`（10★，F 奖得主）— 章节级 RAG
  - `yushui2022/MathModel-Skill`（217★，同源分支）— SHA-256 新鲜度
- **克隆位置**：`paper_output/research/sources/`（6 仓库）+ raw 下载（MathModelAgent 372 模板文件）
- **排除（已融合）**：handsomeZR/mathmodel-skill、sweetcornna/mathodology、XiaoMaColtAI、zhnnky329、Lupynow、ravenxrz、Lanrzip、HeXavi8、qiziqiang 等 15 仓库（见 CLAUDE.md v4.0-v4.1）

## 一、关键发现（本次填补的空白）

| 本项目空白 | 源 | 融合价值 |
|---|---|---|
| 完全没有 Typst | jihe520 | 17 Typst + 17 LaTeX = 34 套赛事模板，覆盖 14 中文赛事 + 3 英文 |
| 无流水线状态机（只有布尔门禁） | AutoMCM-Pro | not_started→in_progress→pending_review→approved↔rework + 返工上限 |
| 无强制代码自证 | AutoMCM-Pro | G4.6 门：每模型配 verify_*.py，全 PASS 才进论文 |
| 无注入防护 | AutoMCM-Pro | _sanitize + security_check markdown 注入检测 |
| 无密钥提交拦截 | AutoMCM-Pro | precommit_scan.sh（git/PreToolUse 通用） |
| 无通用 inf/nan/量级扫描 | AutoMCM-Pro | check_numeric_sanity.py（互补于硬编码 result_reasonableness） |
| Word 无原生公式注入 + 无局部 XML 编辑 | Gostyan | docx-editor-cn skill（temml 链 + office unpack/pack/validate） |
| 无报告新鲜度校验 | yushui2022 | SHA-256 freshness_check（防旧报告） |
| 历史案例检索靠关键词模糊匹配 | Kirito | award-paper-rag 章节级 RAG（heading 分块 + 13 类分类器） |
| 决策动作只有 APPROVED/REWORK | jihe520 | HIL 6 动作（confirm/edit/regenerate/ask/skip/abort） |
| 单 orchestrator 串行，推导阻塞编码 | Hyde-yd | 双 Agent 解耦设计（推导轨 ↔ 编码轨并行） |

## 二、新建文件清单（26 新建）

### 新建 Skill（3 个）

| Skill | 来源 | 核心文件 |
|---|---|---|
| `typst-renderer` | jihe520 | `SKILL.md` + `scripts/build_typst_index.py`（已生成 typst_index.json：17 Typst + 17 LaTeX 集） |
| `docx-editor-cn` | Gostyan | `SKILL.md` + `scripts/`（convert_paper.js, mathml-to-docx.js, formula.py, office/{pack,unpack,validate,soffice}.py + helpers/） |
| `award-paper-rag` | Kirito | `SKILL.md` + `scripts/`（rag_cli.py + mmqa/ 8 文件：markdown_blocks/sections/node_export/postprocessors…） |

### 新建脚本（9 个）

| 脚本 | 所属 skill | 来源 | 作用（已验证可运行） |
|---|---|---|---|
| `pipeline_manager.py` | quality-assurance-auditor | AutoMCM-Pro | GitOps 状态机（init/status/advance/rework/parallel，✓ 真实跑通） |
| `verify_gate.py` | quality-assurance-auditor | AutoMCM-Pro | G4.6 强制代码自证门（✓ 检出 11 模型无 verify） |
| `check_numeric_sanity.py` | quality-assurance-auditor | AutoMCM-Pro | inf/nan/量级扫描（✓ 扫 21 结果文件全干净） |
| `security_check.py` | consistency-auditor | AutoMCM-Pro | 密钥/路径/注入防护（path/env/scan/markdown/all） |
| `precommit_scan.sh` | consistency-auditor | AutoMCM-Pro | 提交前密钥拦截（git hook / PreToolUse 通用） |
| `verification_template.py` | model-code-and-result-generator | AutoMCM-Pro | 为每模型生成 verify_*.py 骨架（G4.6 配套） |
| `freshness_check.py` | context-memory-keeper | yushui2022 | SHA-256 新鲜度（record/check，✓ 真实跑通） |
| `parse_hil_action.py` | decision-logger | jihe520 | HIL 6 动作解析（✓ 真实跑通） |
| `build_typst_index.py` | typst-renderer | jihe520 | 模板索引构建（✓ 生成 typst_index.json） |

### 新建参考文档（3 个）

| 文档 | 所属 skill | 来源 | 内容 |
|---|---|---|---|
| `hil_6_actions.md` | decision-logger/references | jihe520 | HIL 6 动作协议 + 与 G2.5/G4.5 关系 |
| `four_layer_fault_tolerance.md` | quality-assurance-auditor/references | jihe520 | L1 重试→L2 Fallback→L3 Shadow→L4 Feedback |
| `dual_agent_design.md` | model-code-and-result-generator/references | Hyde-yd | 推导轨↔编码轨解耦 + 并行调度 + 交付契约 |

### 新建资源（1 个目录，372 文件）

| 资源 | 来源 | 内容 |
|---|---|---|
| `resources/15_Typst模板/` | jihe520 | 187 .typ + 185 .tex，34 套（zh 14 赛事 + en 3 赛事），含 typst_index.json |

## 三、未新建、仅补充的能力（对齐现有 skill）

| 现有 skill | 补充 |
|---|---|
| `paper-formal-writer/scripts/office/` | 复制 Gostyan 的 pack/unpack/validate/soffice + helpers（Python 侧复用 XML 编辑） |
| `decision-logger` | HIL 6 动作扩展（不替换 G2.5/G4.5，互补） |
| `quality-assurance-auditor` | pipeline_manager（状态机）+ verify_gate（G4.6）+ numeric_sanity 互补于 pipeline.py（路径工具） |
| `competition-prep` | 底层检索可改调 award-paper-rag（章节级 RAG 取代关键词匹配） |

## 四、验证结果

- ✅ 9 个新脚本全部 `py_compile` / `bash -n` 通过
- ✅ pipeline_manager.py：init/status 真实跑通（AP/CUMCM/2 问题）
- ✅ verify_gate.py：检出"11 模型无 verify 脚本"（正确识别 G4.6 缺口）
- ✅ check_numeric_sanity.py：扫描 21 个真实结果文件全干净
- ✅ freshness_check.py：识别 6+ 个 NO_HASH 报告（待 record）
- ✅ parse_hil_action.py：解析真实 human_intervention.md
- ✅ build_typst_index.py：生成 typst_index.json（17 Typst + 17 LaTeX）
- ✅ 372 个 Typst/LaTeX 模板文件下载（1 个网络中断：shuweibei-latex/2_analysis.tex，可重跑恢复）
- ✅ office/ 7 个 Python 工具全部编译通过
- ✅ mmqa/ 8 个 Python 文件全部编译通过

## 五、未做的事项（需用户决策或后续）

| 事项 | 原因 |
|---|---|
| docx-editor-cn 的 npm install | 需 Node.js ≥ 18，按需在首次使用时 `cd .claude/skills/docx-editor-cn && npm install` |
| award-paper-rag 的向量索引构建 | 语料 md 化已由 `corpus_converter.py` 完成（191 篇 PDF/docx → md + papers.csv），向量索引需先 `pip install -r requirements.txt`（llamaindex 0.14）再 `python rag_cli.py build` |
| LaTeX 编译重试机制 | AutoMCM-Pro 的 compile_pdf.py 重试逻辑，typst-renderer SKILL.md 已声明"编译失败重试 3 次"，脚本待按需生成 |

## 五·补、收尾增量（L2 容错 + 语料转换 + 提交拦截）

| 文件 | 来源 | 作用（已验证） |
|---|---|---|
| `quality-assurance-auditor/scripts/fallback_router.py` + `fallback_routes.json` | jihe520 L2 | 7 类备用链（optimization/clustering/evaluation/prediction/ml/latex_compile/word_formula），`next` 消费式推进，链耗尽自动建议 L3/L4，记录到 fallback_log.json（✓ 端到端跑通） |
| `award-paper-rag/scripts/corpus_converter.py` | Kirito 配套 | 191 篇 PDF/docx → md（pdfplumber + python-docx，断点续传），从目录结构解析 year/problem/competition/award 生成 papers.csv（✓ 跑通） |
| `.claude/hooks/precommit_secret_guard.py` + settings.json 接入 | AutoMCM-Pro | PreToolUse Bash hook，仅 git commit 时触发密钥扫描，零开销门控（✓ 干净提交放行/含密钥阻断） |

至此 4 层容错 L1-L4 全部落地：
- L1 `auto_detect_and_fix.py`（14 阶段修正器，3 轮重试）
- **L2 `fallback_router.py`（7 类备用链）✅ 本次实现**
- L3 consistency-auditor LOW_CONFIDENCE 标记
- L4 `pipeline_manager.py rework` + `parse_hil_action.py`

## 六、与 v4.1 的关系

v4.1 融合同级竞品（handsomeZR + mathodology），本次 v4.2 融合的是**更广泛的同赛道生态**（jihe520 行业最大 + AutoMCM-Pro 架构最佳 + Gostyan Word 专家 + Kirito RAG 创新 + yushui2022 同源 cherry-pick）。两者互补，无冲突：
- v4.1 的盲评 Panel / figqa / dim_weights / 4 层反馈 → 评分与图表质量
- v4.2 的 Typst / GitOps / 自证 / docx / RAG / 新鲜度 → 交付链路与工程纪律
