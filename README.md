# 数学建模竞赛生产系统

> **面向 CUMCM（国赛）/ MCM-ICM（美赛）/ 华为杯 / 电工杯 / 五一赛等数学建模竞赛的 Claude Code 工作区。**
> 把 Claude 变成你的建模总教练 + 论文生产器 + 代码生成器 + 图示设计器 + 答辩陪练。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-67-blue)](.claude/skills/)
[![Version](https://img.shields.io/badge/version-4.6-green)](CLAUDE.md)

---

## 这是什么

这不是一个资料仓库，而是一套**能持续把赛题转化成可提交论文**的生产系统。它通过 **67 个 Claude Code Skill + 9 个专业 Agent + 8 道门禁 + 3 轮审计**，覆盖从审题到答辩的全流程：

```
读题 → 拆题 → 模型路线 → 数据清洗 → 生成/运行代码
→ 真实图表/结果 → 证据门禁 → Agent 全局写作
→ Word/LaTeX/Typst 排版 → 格式门禁 → 最终 QA → （冲奖）盲评 Panel
```

**设计原则**：AI 负责机械正确性（编译/一致性/格式），人类负责建模判断（选模/结果确认）——每处关键决策都有人工门禁。

---

## 快速开始

### 1. 环境要求

- **Claude Code**（CLI 或 IDE 扩展）
- **Python 3.10+**
- **Node.js 18+**（docx-editor-cn 和部分 MCP server 需要）
- **Typst CLI**（可选，Typst 交付链路）：`winget install --id Typst.Typst`
- **pandoc**（可选，Word 原生公式链）：`winget install --id JohnMacFarlane.Pandoc`

### 2. 安装

```bash
git clone <你的仓库地址>
cd 数学建模

# Python 依赖
pip install -r docs/requirements_skill.txt

# Word 原生公式链（可选）
cd .claude/skills/docx-editor-cn && npm install && cd ../../..

# RAG 优秀论文检索（可选）
pip install -r .claude/skills/award-paper-rag/scripts/requirements.txt
```

### 3. 配置

```bash
# MCP 配置：.mcp.json 已就绪，只需把 filesystem 的 "." 改成你的项目根目录绝对路径
# 例: "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/数学建模"]

# 权限模板：复制并按需修改
cp .claude/settings.local.example.json .claude/settings.local.json
```

### 4. 使用

把赛题 PDF/Word 和附件放入 `problem_files/`，然后对 Claude 说：

> **开始生成数学建模论文**

或用具体口令触发局部能力：

| 口令 | 作用 |
|------|------|
| `审题` / `选模` | 审题选模（题型判断 + Top3 模型路线 + 风险预警） |
| `生成代码` | 从零生成可运行代码框架 |
| `生成图示` / `画图` | 统一图表入口（自动判断需求→分派子 skill） |
| `审论文` / `打分` | 9 维度 100 分制深度评审 |
| `准备答辩` / `模拟答辩` | 问答库 + 追问链 + 模拟评分 |
| `降AI味` / `降重` | 中文学术写作降 AIGC 检测 |
| `润色` / `polish` | 12 点检查 + 段落改写 + 质量评分 |

---

## 系统能力

| 能力 | 工具 | 说明 |
|------|------|------|
| **分层建模选模** | HMML 方法库（[NeurIPS 2025](https://github.com/usail-hkust/LLM-MM-Agent)） | 5 domain / 18 subdomain / 97 method 三层检索 + actor-critic 打分 |
| **RAG 优秀论文检索** | `award-paper-rag` skill | 章节级 heading 分块 + 13 类分类器（语料需自备） |
| **PDF 表格提取** | Camelot | 赛题附表一键转 CSV |
| **期刊风图表** | SciencePlots | IEEE/Nature/Science 76 样式 |
| **Word 原生公式** | `docx-editor-cn` skill | temml → MathML → docx OMML |
| **Typst 交付** | `typst-renderer` skill | 34 套赛事模板（17 Typst + 17 LaTeX） |
| **GitOps 流水线** | `pipeline_manager.py` | 状态机 + 并行阶段 + 返工上限 |
| **强制代码自证** | G4.6 门 `verify_gate.py` | 每模型配 verify_*.py，全 PASS 才引用 |
| **盲评 Panel** | `blind-panel` skill | 3 座独立盲评 + 20 分冲突仲裁（冲奖模式） |
| **超参调优 / 可解释性** | Optuna / SHAP | ML 题加分项 |

---

## 目录结构

```
├── .claude/
│   ├── skills/          ★ 67 个 Skill（流水线/评审/图表/学术/社区）
│   ├── agents/            9 个专业 Agent
│   └── settings.json      权限配置（allow/deny 规则）
├── prompts/               31 个工作流提示词（00-30）
├── outputs/               规则/模板/知识库（评分表/方法匹配/写作模板）
├── docs/                  系统文档 + requirements_skill.txt
├── examples/              CUMCM 2024 B 题完整样例
├── nature-skills/         9 个 Nature 学术写作 Skill
├── tools/                 辅助工具（paper_search / visualization）
│
├── CLAUDE.md              ★ 系统入口指令（Claude 读取的第一个文件）
├── AGENTS.md              完整系统规则（17 章）
├── ATTRIBUTION.md         致谢与来源
├── LICENSE                MIT
│
├── problem_files/         放赛题（gitignore，不入仓）
└── paper_output/          产物输出（gitignore 个人产物，保留文档骨架）
```

> **`resources/` 资料库不入仓**（含第三方版权的论文 PDF / 视频 / 安装包，261GB）。
> 如需竞赛资料，参见 [ATTRIBUTION.md](ATTRIBUTION.md) 列出的来源仓库自行获取。

---

## 门禁体系（过不了不进下一阶段）

| 门 | 时机 | 作用 |
|----|------|------|
| G1 证据门禁 | 代码→写作前 | 每问 metrics 齐、无编造 |
| G2 方法门禁 | 选模后 | 用户填选择理由 ≥50 字 |
| G2.5 PoC 门 | 候选方法 | ≤30 行 PoC 在真实数据跑通 |
| G4.6 自证门 | 引用结果前 | 每模型 verify_*.py 全 PASS |
| G5 格式门禁 | 定稿前 | 字数 / 三级标题 / 图表引用 / 公式 |
| G6 数字门禁 | 写作后 | 论文数字 = 代码结果 |
| 三审计层 | 最终 | 一致性 + 完整性 + 工作流 |

---

## 演进历史

7 轮迭代，详见 [CHANGELOG](paper_output/research/CHANGELOG.md)：

| 版本 | 定位 |
|------|------|
| v4.0 | 地基（15 仓库融合：合同/门控/Cookbook/Playbook） |
| v4.1 | 评分质量（盲评 Panel / figqa / 题型加权） |
| v4.2 | 交付纪律（Typst / GitOps / G4.6 自证 / docx 公式 / RAG） |
| v4.3 | 单点提效（Camelot / Pix2Text / SciencePlots / SHAP / Optuna） |
| v4.4 | 系统整理（单系统成型 / RAG 去重 / 路由更新） |
| v4.5 | 全面体检（8 维度审计 / P0 门禁修复 / 断链清零） |
| v4.6 | 学术方法论（[MM-Agent NeurIPS 2025](https://github.com/usail-hkust/LLM-MM-Agent)：HMML / actor-critic / 美赛分题策略） |

---

## 致谢

本系统融合了 30+ 开源项目的设计与代码，详见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## License

[MIT](LICENSE) — 本仓库的集成代码以 MIT 开源。第三方代码保留其原始 license。
