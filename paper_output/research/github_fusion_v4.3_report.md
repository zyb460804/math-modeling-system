# GitHub 融合报告 v4.3（工具链增强 / 7 脚本 + 1 文档 / 7 源）

- **执行日期**：2026-07-23
- **定位**：v4.3 聚焦**单点工具提效**（不改主流程，按需调用），与 v4.2 的"交付链路+工程纪律"互补。
- **调研**：二轮 GitHub 搜索（科学绘图/PDF/OCR/MCP/AIGC/超参/可解释/数据等 12 组关键词），筛 7 个有增量价值的源。
- **完整路由**：CLAUDE.md 工具口令表 / task_router §十五 / orchestrator 阶段表 / 00_route_task 速查（4/4 覆盖）。

## 一、新增脚本（7 个）

| 脚本 | 所属 skill | 来源 | 解决的痛点 | 验证 |
|------|-----------|------|-----------|------|
| `extract_pdf_tables.py` | data-cleaning-and-visualization | camelot 3716★ | 赛题 PDF 附表人工抠 | ✓ A题.pdf 真实提取 10×2 表 → CSV+Excel+索引 |
| `extract_formulas_ocr.py` | problem-doc-model-selector | Pix2Text 3195★ | PDF 公式图手敲易错 | ✓ 语法通过（Pix2Text 按需装） |
| `journal_style.py` | math-figure | SciencePlots ~5k★ | 默认 matplotlib 样式显业余 | ✓ 76 样式 + demo 出图 |
| `replace_docx_preserve_format.py` | aigc-reduce | aigc-deslop 18★ | 降 AIGC 破坏 Word 排版 | ✓ 10.8KB 语法通过（9 轮实测 55%→11%） |
| `shap_explain.py` | feature-engineering | SHAP + shapash 3247★ | ML 题缺可解释性（评委扣分） | ✓ 包导入 + help 跑通 |
| `optuna_tune.py` | model-code-and-result-generator | Optuna 14549★ | 手动调参/网格搜索低效 | ✓ help 跑通（XGBoost/LightGBM/RF/SVR） |
| `akshare_fetch.py` | authoritative-data-harvester | akshare ~10k★ | C 题宏观数据难找 | ✓ 7 大类接口列出 |

## 二、新增文档

- `docs/math-mcp-servers.md` — 6 个数学/学术 MCP 配置（sympy-mcp / mcp-optimizer / arxiv-latex-mcp / semantic-scholar / Wolfram-MCP / math-mcp）。命令从源仓库 README 校准（3 个在 PyPI：`uvx 包名`）。

## 三、已装 pip 包（全局）

SciencePlots 2.2.2 · camelot-py 2.0.0 · shap 0.51.0 · optuna 4.9.0 · akshare 1.18.75（+ v4.2 已装的 llamaindex 0.14 / sentence-transformers 5.6 / torch 2.11）

## 四、未做的事项

| 事项 | 原因 |
|------|------|
| Pix2Text 实际下模型 | 数百 MB，首次使用时 `pip install pix2text` + `HF_ENDPOINT=hf-mirror.com` |
| 6 个数学 MCP 实际接入 | 需用户侧 `claude mcp add`（外部服务，我写了准确命令文档不能替装） |
| Tier 2（Mermaid/GraphRAG/Streamlit） | 用户说"可以"只确认 Tier 1，Tier 2 待决策 |

## 五、路由层同步（本次额外补）

发现新工具最初只在自己 SKILL.md（1/4），中央路由缺失。已补齐 4/4：
- CLAUDE.md 工具口令表 +16 条
- task_router.md +§十五
- orchestrator 阶段路由表 +16 行
- 00_route_task.md +v4.2/v4.3 速查

## 六、与 v4.2 的关系

| 维度 | v4.2 | v4.3 |
|------|------|------|
| 定位 | 交付链路 + 工程纪律 | 单点工具提效 |
| 典型 | Typst/GitOps/自证/RAG/新鲜度 | Camelot/SHAP/Optuna/akshare |
| 改主流程 | 是（新 skill + 新门控 G4.6） | 否（脚本挂在现有 skill，按需调） |

两者完全互补，无冲突。
