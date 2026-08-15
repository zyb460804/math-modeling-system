# MathModel Skill 数学建模竞赛生产系统 — 完整文档

> **版本：v3.4 | 2026-08-15**（对齐 v4.9 实况：54 skill / 9 agent / 7 hook / outputs 75 文件 / Nature 轨道 v4.8 已归档）
> 
> 本文档面向想学习和复用本系统的人。从零开始，包含系统架构、工作流程、核心组件详解、使用方法、扩展指南和踩坑记录。
> 
> **阅读建议**：
> - 想快速上手 → 直接看 [第 5 章：使用方法](#5-使用方法)
> - 想理解原理 → 从 [第 2 章：系统架构](#2-系统架构) 开始
> - 想自己搭建 → 看 [第 7 章：扩展指南](#7-扩展指南)
> - 想避坑 → 看 [第 8 章：踩坑记录](#8-踩坑记录)

---

## 目录

1. [系统定位](#1-系统定位)
2. [系统架构](#2-系统架构)
   - 2.1 整体架构图
   - 2.2 五层设计
   - 2.3 数据流
   - 2.4 组件关系
3. [核心组件](#3-核心组件)
   - 3.1 Skill 详解
   - 3.2 Agent 详解
   - 3.3 MCP Server 详解
   - 3.4 Hook 详解
   - 3.5 知识库详解
4. [工作流程](#4-工作流程)
   - 4.1 完整流水线
   - 4.2 每步详解
   - 4.3 关键代码文件
   - 4.4 结果文件说明
5. [使用方法](#5-使用方法)
   - 5.1 环境准备
   - 5.2 快速开始
   - 5.3 手动口令
   - 5.4 单脚本运行
   - 5.5 常见操作
6. [目录结构](#6-目录结构)
7. [扩展指南](#7-扩展指南)
   - 7.1 添加新 Skill
   - 7.2 添加新 Agent
   - 7.3 添加新 Hook
   - 7.4 添加新 MCP Server
   - 7.5 修改优化模型
8. [踩坑记录](#8-踩坑记录)
   - 8.1 Hook 相关
   - 8.2 优化器相关
   - 8.3 论文生成相关
   - 8.4 格式门禁相关
9. [附录](#9-附录)

---

## 1. 系统定位

### 1.1 一句话定义

**给一道数学建模竞赛题+附件数据，自动输出可上交的 Word 论文。**

### 1.2 Claude 的五个角色

| 角色 | 职责 | 对应组件 | 具体做什么 |
|------|------|----------|-----------|
| 总教练 | 审题、选模、评分 | `model-selector` skill | 读 PDF → 判断题型 → 推荐模型+算法 |
| 论文生产器 | 写作、改稿、摘要 | `paper-formal-writer` skill | 根据结果生成 18000+ 字论文 |
| 代码生成器 | Python/Matlab 代码 | `model-code-and-result-generator` skill | 生成优化模型代码并运行 |
| 图示设计器 | 流程图、结果图 | `diagram-maker` / `math-figure` skills | 生成论文所需的图表 |
| 答辩陪练 | 问答、追问链 | `defense` skill（统一入口，内部调度 defense-simulator） | 模拟评委提问并准备答案 |

### 1.3 适用竞赛

| 竞赛 | 适配度 | 说明 |
|------|--------|------|
| 国赛（CUMCM） | ★★★★★ | 完全适配，有专用评分量表和模板 |
| 美赛（MCM/ICM） | ★★★★☆ | 适配，需要英文写作支持 |
| 电工杯 | ★★★★☆ | 适配，有专用案例 |
| MathorCup | ★★★★☆ | 适配 |
| 五一赛 | ★★★☆☆ | 基本适配 |

### 1.4 系统能力边界

**能做的**：
- 读题+分析题型 ✅
- 匹配算法模板 ✅
- 求解优化问题（LP/MIP/非线性） ✅
- 生成 18000+ 字论文 ✅
- 自动排版 Word ✅
- 检查格式规范 ✅
- 生成流程图/数学图/网络图 ✅

**做不好的**：
- 需要深度数学推导的问题（需要人工介入）
- 参考文献可能编造（需要 `citation-tracer` 验证）
- 复杂多步问题需要手动拆解

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用户（参赛选手）                              │
│                    输入：赛题 PDF + 附件 Excel                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   paper-workflow-orchestrator                        │
│                   ★ 总控 Skill（阶段判断 + 路由）                     │
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│   │ 预检     │───→│ 题意解析 │───→│ 模型路线 │───→│ 数据处理 │      │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│        │                                               │             │
│        ▼                                               ▼             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│   │ 格式门禁 │←───│ Word排版 │←───│ 论文写作 │←───│ 建模代码 │      │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  轨道 A     │      │  轨道 B     │      │  Nature     │
   │  自动流水线  │      │  手动工作流  │      │（v4.8 归档） │
   │  10 Skills  │      │  9 Skills   │      │→references  │
   └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
          │                    │                     │
          ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        共享基础设施                                   │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐            │
│  │  6 MCP Server │  │  9 Agent      │  │  7 Hook       │            │
│  │  外部工具集成  │  │  并行子代理    │  │  生命周期钩子  │            │
│  └───────────────┘  └───────────────┘  └───────────────┘            │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐            │
│  │  知识库        │  │  算法模板库    │  │  图表教程库    │            │
│  │  75 文件       │  │  64+ 算法     │  │  50+ 图表     │            │
│  └───────────────┘  └───────────────┘  └───────────────┘            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        最终输出                                       │
│                    paper_output/final_paper.docx                     │
│                    含图表、公式、参考文献                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 五层设计

系统分为五层，从上到下分别是：

| 层 | 职责 | 组件 |
|----|------|------|
| **用户层** | 用户输入赛题和附件 | problem_files/ |
| **编排层** | 阶段判断、路由、全流程控制 | orchestrator skill |
| **执行层** | 具体任务执行（读题/建模/写作/排版） | 10 个核心 skill |
| **支撑层** | 并行执行、外部集成、生命周期管理 | 9 Agent + 6 MCP + 7 Hook |
| **知识层** | 评分标准、方法匹配、写作模板 | 75 个知识文件 |

**设计原则**：
- **编排层不做事**：orchestrator 只负责路由，不执行具体任务
- **执行层可替换**：每个 skill 独立，可以单独升级或替换
- **支撑层透明**：Agent/MCP/Hook 对用户不可见，自动工作
- **知识层共享**：所有 skill 共享同一套知识库

### 2.3 数据流

```
输入:
  problem_files/A题/A题.pdf          ──→ 题意解析
  problem_files/A题/附件*.xlsx       ──→ 数据处理

中间产物:
  paper_output/results/
    ├── clean_*.csv                  ← 数据处理输出
    ├── data_summary.json            ← 数据摘要
    ├── data_quality_report.md       ← 数据质量报告
    ├── q1_optimizer.json            ← Q1 结果
    ├── q2_results.json              ← Q2 结果
    ├── q3_results.json              ← Q3 结果
    ├── q4_results.json              ← Q4 结果
    └── validation_report.json       ← 验证报告

  paper_output/code/
    ├── data_processing/load_data.py ← 数据加载
    ├── modeling/optimizer_v2.py     ← 优化器
    ├── modeling/q*_model.py         ← 各问题模型
    └── visualization/
        ├── gen_figures.py           ← 图表生成
        └── gen_paper_v3.py          ← 论文生成

  paper_output/figures/
    ├── methodology.png              ← 方法论流程图
    ├── q1_analysis.png              ← Q1 分析图
    ├── q2q3_comparison.png          ← Q2/Q3 对比图
    ├── q3_heatmap.png               ← Q3 热力图
    └── q4_analysis.png              ← Q4 分析图

输出:
  paper_output/final_paper.docx      ← 最终论文（18000+ 字）
  paper_output/format_check_report.json ← 格式检查报告
```

### 2.4 组件关系

```
                    ┌─────────────────┐
                    │   用户输入       │
                    │   PDF + Excel   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   orchestrator  │ ← 编排层
                    │   路由到对应 skill │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ problem-doc   │   │ data-cleaning │   │ model-code    │
│ model-selector│   │ visualization │   │ result-gen    │
│               │   │               │   │               │
│ 调用知识库:    │   │ 调用脚本:      │   │ 调用脚本:      │
│ method_match  │   │ auto_pipeline │   │ optimizer_v2  │
│ problem_type  │   │ load_data     │   │ q1-q4_model   │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────────────────────────────────────────────┐
│                    paper_output/                       │
│   results/ + code/ + figures/ + final_paper.docx      │
└───────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────┐   ┌───────────────┐
│ quality-      │   │ paper-formal  │
│ assurance     │   │ writer        │
│ auditor       │   │               │
│               │   │ 调用脚本:      │
│ 调用脚本:      │   │ check_format  │
│ validate_     │   │ gen_paper_v3  │
│ results       │   │               │
└───────────────┘   └───────────────┘
```

**关键依赖关系**：
- `data-cleaning` 依赖 `problem_files/` 中的 Excel 文件
- `model-code` 依赖 `data-cleaning` 输出的 clean CSV
- `paper-formal-writer` 依赖 `model-code` 输出的 JSON 结果
- `quality-assurance` 依赖所有阶段的输出

---

## 3. 核心组件

### 3.1 Skill 详解

#### 3.1.1 什么是 Skill

Skill 是系统的核心执行单元。每个 Skill 是一个目录，包含：

```
.claude/skills/my-skill/
├── SKILL.md           ← 指令文件（必须有）
├── scripts/           ← 可执行脚本（可选）
│   ├── script1.py
│   └── script2.py
└── references/        ← 参考文档（可选）
    └── ref1.md
```

**SKILL.md 的结构**：
```markdown
---
name: my-skill
description: 这个 skill 做什么
disable-model-invocation: true  # 可选：禁止 Claude 自动调用
---

# My Skill

## 触发词
`口令1` `口令2`

## 工作流
1. 第一步
2. 第二步

## 输出
- 输出文件路径
- 输出格式说明
```

#### 3.1.2 Skill 分类详解

**轨道 A：核心流水线（10 个）**

这是系统的主干，按顺序执行：

| 顺序 | Skill | 输入 | 输出 | 有脚本 |
|------|-------|------|------|--------|
| 1 | `paper-workflow-orchestrator` | 用户指令 | 阶段判断 | ✅ preflight_check.py |
| 2 | `problem-doc-model-selector` | PDF 文本 | problem_analysis.json | ✅ analyze_problem.py |
| 3 | `modeling-paper-rubric-and-model-selector` | problem_analysis.json | model_route.json | ✅ build_model_route.py |
| 4 | `authoritative-data-harvester` | data_requirements.json | crawled_data/ | ✅ run.py |
| 5 | `data-cleaning-and-visualization` | problem_files/*.xlsx | clean CSV + 图表 | ✅ 7 个脚本 |
| 6 | `model-code-and-result-generator` | clean CSV + model_route | q*_results.json | ✅ build_result_contracts.py |
| 7 | `quality-assurance-auditor` | 所有结果 JSON | validation_report.json | ✅ evidence_gate.py |
| 8 | `paper-formal-writer` | 所有结果 + 图表 | final_paper.docx | ✅ 3 个脚本 |
| 9 | `paper-micro-unit-generator` | 大纲 | 分块内容 | ✅ generate_all_offline.py |
| 10 | `context-memory-keeper` | 各阶段输出 | 记忆文件 | ✅ |

**轨道 B：Legacy 手动（9 个）**

手动触发的工作流，适合局部任务：

| Skill | 口令 | 做什么 |
|-------|------|--------|
| `scan` | 先扫一遍资料 | 扫描目录 → 建文件地图 → 标优先级 |
| `card` | 抽卡 | 逐文件提炼知识卡片 |
| `rules` | 建规则库 | 更新评分表/方法匹配表/模板库 |
| `analyze` | 审题 | 判断题型 → 提炼目标 → 推荐建模路线 |
| `review` | 审论文 | 全文评分 → 问题拆解 → 修改优先级清单 |
| `code` | 生成代码 | 判断题型与算法 → 生成可运行代码框架 |
| `defense` | 准备答辩 | 答辩提纲 → 高频问答 → 追问链 → 风险点 |
| `submit` | 生成提交包 | 自检 → 论文+代码+图表+答辩清单 |
| `figure` | 生成图示 | 判断最需要的图 → 输出图示方案 |

**新增智能辅助（10 个）**

刚加入系统的 skill，补充核心流水线的不足：

| Skill | 口令 | 做什么 | 为什么需要 |
|-------|------|--------|-----------|
| `model-selector` | `/model-selector` | 题型→推荐模型+算法+风险+代码模板 | 每次比赛都要选模 |
| `chart-recommender` | `/chart-recommender` | 题型→最佳图表类型+matplotlib 代码 | 50+ 图表没有路由 |
| `defense-simulator` | `/defense-simulator` | 根据论文内容生成评委问题+追问链 | 答辩准备锦上添花 |
| `algorithm-runner` | `/algorithm-runner` | 匹配算法名→适配数据→执行→输出 JSON | 64 个模板没有一键执行 |
| ~~`result-validator`~~ | ~~自动触发~~ | ~~范围检查、统计检验~~ | **v4.8 归档** → `check_result_reasonableness.py` + `result-validation-rules.md` |
| `paper-rewriter` | `/paper-rewriter` | 输入原文+目标风格→改写版本 | 论文润色 |
| `diagram-maker` | `/diagram-maker` | 模型求解流程图、方法架构图 | 每篇论文都需要流程图 |
| `interactive-chart` | `/interactive-chart` | Plotly 3D 曲面、平行坐标 | 数据探索+答辩交互 |
| `math-figure` | `/math-figure` | 函数图像、几何示意、向量场 | 数学建模特色需求 |
| `network-graph` | `/network-graph` | 最短路径高亮、社区检测 | C 题图论问题高频 |

#### 3.1.3 Skill 执行机制

**有脚本的 Skill**：
```
用户触发 → Claude 读取 SKILL.md → Claude 执行 scripts/ 中的 Python 脚本 → 返回结果
```

**无脚本的 Skill**：
```
用户触发 → Claude 读取 SKILL.md → Claude 按照指令生成代码/文本 → 返回结果
```

**区别**：有脚本的 Skill 执行确定性更高，无脚本的 Skill 依赖 Claude 的理解能力。

### 3.2 Agent 详解

#### 3.2.1 什么是 Agent

Agent 是 Claude Code 的子代理，可以并行执行任务。每个 Agent 是一个 `.md` 文件：

```markdown
# Agent Name

## 职责
描述这个 Agent 做什么。

## 输入
- 输入格式说明

## 输出
- 输出格式说明

## 工具使用
- 使用哪些工具（Bash, Read, Glob, etc.）
```

#### 3.2.2 Agent 列表

| Agent | 职责 | 工具 | 使用场景 |
|-------|------|------|----------|
| `code-tester` | Python 代码执行与验证 | Bash, Read, Glob | 运行建模代码 |
| `paper-reviewer` | 论文评审（9 维度 100 分制） | All | 审论文 |
| `matlab-reviewer` | Matlab 代码审查 | All | Matlab 代码 |
| `data-validator` | 数据质量验证 | Bash, Read, Glob | 检查数据质量 |
| `data-explorer` | 快速 EDA 数据探索 | All | 数据探索 |
| `model-comparison` | 多模型并行对比 | All | 模型对比 |
| `citation-checker` | 引用一致性检查 | All | 检查引用 |
| `competition-prep` | 历史案例匹配备战 | All | 赛前准备 |
| `blind-panel-judge` | 盲评单座（3 座并行，v4.1） | All | championship 盲评终审 |

#### 3.2.3 Agent 使用方式

```bash
# 在 Claude Code 中直接调用
# 例如：让 code-tester 运行一个 Python 脚本
# Claude 会自动启动 code-tester agent 并行执行

# 也可以在代码中显式调用
# Agent 会并行执行，不阻塞主流程
```

### 3.3 MCP Server 详解

#### 3.3.1 什么是 MCP

MCP（Model Context Protocol）是 Anthropic 定义的协议，让 Claude 可以调用外部工具。MCP Server 是一个独立进程，通过 stdin/stdout 与 Claude 通信。

#### 3.3.2 MCP Server 列表

| Server | 用途 | 安装 | 提供的工具 |
|--------|------|------|-----------|
| `context7` | 库文档实时查询 | npm | 查询 npm/PyPI 文档 |
| `filesystem` | 文件系统访问 | npm | 读写文件、列目录 |
| `sequential-thinking` | 顺序推理 | npm | 多步推理链 |
| `playwright` | 浏览器自动化 | npm | 打开网页、截图、点击 |
| `memory` | 跨会话知识图谱 | npm | 创建/查询实体和关系 |
| `nature-academic-search` | 学术文献检索 | Python | PubMed/CrossRef/arXiv |

#### 3.3.3 MCP 配置

配置文件：`.mcp.json`

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "e:/数学建模"]
    }
  }
}
```

**注意**：`filesystem` 的第三个参数是允许访问的目录路径。

### 3.4 Hook 详解

#### 3.4.1 什么是 Hook

Hook 是 Claude Code 的生命周期钩子，在工具执行前后自动触发。

| Hook 类型 | 触发时机 | 用途 |
|-----------|----------|------|
| `PreToolUse` | 工具执行前 | 验证、阻止、参数修改 |
| `PostToolUse` | 工具执行后 | 格式化、检查、通知 |
| `Stop` | 会话结束时 | 最终验证、清理 |

#### 3.4.2 Hook 列表

| Hook | 类型 | 触发条件 | 做什么 |
|------|------|----------|--------|
| `protect_outputs.py` | PreToolUse | Write/Edit | 保护 outputs/ 和 .claude/ 不被覆盖 |
| `precommit_secret_guard.py` | PreToolUse | Bash | 提交前密钥/路径扫描拦截（v4.2） |
| `check_python.py` | PostToolUse | Edit/Write .py | Python 语法检查 |
| `format_python.py` | PostToolUse | Edit/Write .py | Black 自动格式化 |
| `auto_evidence_gate.py` | PostToolUse | Edit/Write | 关键文件变更时触发证据门禁 |
| `log_exit_code.py` | PostToolUse | Bash | 记录非零退出码 |
| `check_index_sync.py` | Stop | 会话结束 | 提醒更新 INDEX.md |

#### 3.4.3 Hook 实现示例

```python
#!/usr/bin/env python3
"""PreToolUse hook: block writes to protected directories."""
import sys, json

def main():
    # 从 stdin 读取 JSON（Claude Code 通过 stdin 传递数据）
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 解析失败则放行

    # 获取文件路径
    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # 检查是否是保护目录
    fp = file_path.replace("\\", "/")
    if fp.startswith("outputs/") or fp.startswith(".claude/"):
        sys.exit(2)  # 阻止写入

    sys.exit(0)  # 允许写入

if __name__ == "__main__":
    main()
```

**退出码**：`0`=允许，`2`=阻止

#### 3.4.4 Hook 配置

配置文件：`.claude/settings.json` 的 `hooks` 字段

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python e:/数学建模/.claude/hooks/protect_outputs.py"
          }
        ]
      }
    ]
  }
}
```

**注意**：必须使用绝对路径，否则在子目录编辑文件时会找不到 hook。

### 3.5 知识库详解

#### 3.5.1 知识库结构

位于 `outputs/` 目录，共 75 个文件（另有 `scripts/`、`_reports/` 两个子目录）：

```
outputs/
├── INDEX.md                    ← 统一索引（唯一入口）
├── knowledge_graph.md          ← 知识图谱（实体-关系）
│
├── 系统调度层（11 文件）
│   ├── task_router.md          ← 任务路由
│   ├── asset_registry.md       ← 资产注册
│   ├── file_map.md             ← 文件地图
│   └── ...
│
├── 建模选模层（13 文件）
│   ├── method_matching.md      ← 方法匹配表
│   ├── algorithm_templates.md  ← 算法模板库
│   ├── model_selection_flow.md ← 模型选型流程
│   └── ...
│
├── 写作表达层（14 文件）
│   ├── writing_templates.md    ← 写作模板
│   ├── abstract_templates.md   ← 摘要模板
│   ├── empirical.json          ← 实测分位（v2.0 by_topic）
│   └── ...
│
├── 审稿评分层（11 文件）
│   ├── scoring_rubric.md       ← 评分量表（100 分制）
│   ├── revision_checklist.md   ← 修订清单
│   └── ...
│
├── 答辩准备层（6 文件）
│   ├── defense_qa_bank.md      ← 答辩题库
│   ├── defense_followup_chains.md ← 追问链
│   └── ...
│
├── 数据处理层（3 文件）
├── 质量验收层（4 文件）
└── 图表可视层（4 文件）
```

#### 3.5.2 核心知识文件

| 文件 | 用途 | 被谁引用 |
|------|------|----------|
| `scoring_rubric.md` | 7 模块 100 分制评分标准（9 类质量信号只观察不改分值） | paper-reviewer, review |
| `method_matching.md` | 11 类任务×模型×算法×风险对照表 | model-selector, analyze |
| `writing_templates.md` | 摘要/问题分析/模型建立/求解模板 | paper-formal-writer |
| `high_score_expression_library.md` | 高分表达库 | paper-rewriter |
| `defense_qa_bank.md` | 十大高频答辩问题类型 | defense-simulator |
| `figure_templates.md` | 图表模板 | chart-recommender |
| `algorithm_templates.md` | 算法模板库 | algorithm-runner |

---

## 4. 工作流程

### 4.1 完整流水线

```
Step 1: 预检
  ├─ 检查 problem_files/ 是否有赛题文件
  └─ 输出: 预检通过/失败

Step 2: 题意解析
  ├─ 读取 PDF → 提取问题、附件、约束条件
  ├─ 调用: problem-doc-model-selector
  └─ 输出: paper_output/step1/problem_analysis.json

Step 3: 模型路线
  ├─ 根据题型匹配推荐模型+算法
  ├─ 查询: outputs/method_matching.md
  ├─ 调用: modeling-paper-rubric-and-model-selector
  └─ 输出: paper_output/plan/model_route.json

Step 4: 数据处理
  ├─ auto_pipeline.py: 清洗 Excel → 特征工程 → clean CSV
  ├─ 调用: data-cleaning-and-visualization
  └─ 输出: paper_output/results/clean_*.csv

Step 5: 建模代码
  ├─ 根据 model_route 生成 Python 代码
  ├─ 调用: model-code-and-result-generator
  └─ 输出: paper_output/code/modeling/q*_model.py

Step 6: 运行代码
  ├─ 执行优化模型，求解 Q1-Q5
  ├─ 调用: optimizer_v2.py (PuLP)
  └─ 输出: paper_output/results/q*_results.json

Step 7: 结果验证
  ├─ validate_results.py: 范围检查 + 交叉验证
  ├─ 调用: quality-assurance-auditor
  └─ 输出: paper_output/results/validation_report.json

Step 8: 图表生成
  ├─ gen_figures.py: matplotlib 生成论文图表
  ├─ 调用: data-cleaning-and-visualization
  └─ 输出: paper_output/figures/*.png

Step 9: 论文写作
  ├─ gen_paper_v3.py: 生成 Word 文档
  ├─ 调用: paper-formal-writer
  └─ 输出: paper_output/final_paper.docx

Step 10: 格式门禁
  ├─ check_paper_format.py: 检查字数、字体、章节、图表
  ├─ 调用: paper-formal-writer
  └─ 输出: paper_output/format_check_report.json
```

### 4.2 每步详解

#### Step 1: 预检

```python
# 检查 problem_files/ 是否有文件
import os
problem_dir = "problem_files"
files = os.listdir(problem_dir)
if not files:
    print("ERROR: problem_files/ is empty!")
    exit(1)
```

#### Step 2: 题意解析

**输入**：PDF 文件
**输出**：`problem_analysis.json`

```json
{
  "problem_type": "优化",
  "sub_type": "线性规划",
  "questions": [
    {
      "id": "Q1",
      "description": "典型风光场景下的运行指标分析",
      "data_needed": ["负荷曲线", "风光出力", "设备参数"],
      "model_hint": "功率平衡计算"
    }
  ],
  "attachments": [
    {"name": "附件1", "type": "时序数据", "rows": 24, "cols": 2}
  ]
}
```

#### Step 3: 模型路线

**输入**：`problem_analysis.json`
**输出**：`model_route.json`

```json
{
  "questions": [
    {
      "question_id": "Q1",
      "task_type": "综合建模/统计分析",
      "main_model": "功率平衡模型",
      "algorithm": "直接计算",
      "risk": "低"
    },
    {
      "question_id": "Q2",
      "task_type": "优化",
      "main_model": "0-1 整数规划",
      "algorithm": "PuLP CBC",
      "risk": "中"
    }
  ]
}
```

#### Step 4: 数据处理

**输入**：`problem_files/*.xlsx`
**输出**：`paper_output/results/clean_*.csv` + `data_summary.json`

```bash
python .claude/skills/data-cleaning-and-visualization/scripts/auto_pipeline.py
```

处理流程：
1. 扫描 problem_files/ 下所有 Excel/CSV
2. 加载为 DataFrame
3. 清洗：缺失值填充（中位数）、异常值标记（3*IQR）
4. 输出 clean CSV + 数据摘要

#### Step 5-6: 建模代码 + 运行

**输入**：clean CSV + model_route.json
**输出**：`q*_results.json`

核心代码：`optimizer_v2.py`

```python
import pulp

def solve_schedule(wind_pu, solar_pu, ammonia_daily, continuous=False):
    """求解最优调度方案。"""
    prob = pulp.LpProblem("AmmoniaPark", pulp.LpMinimize)

    # 决策变量
    p_buy = [pulp.LpVariable(f"buy_{t}", 0, None) for t in range(24)]
    p_sell = [pulp.LpVariable(f"sell_{t}", 0, None) for t in range(24)]

    if continuous:
        p_alkel = [pulp.LpVariable(f"alkel_{t}", 0, 10) for t in range(24)]
    else:
        z_alkel = [pulp.LpVariable(f"z_alkel_{t}", 0, 1, cat='Binary') for t in range(24)]
        p_alkel = [z_alkel[t] * 10 for t in range(24)]

    # 目标函数：最小化成本
    prob += pulp.lpSum([p_buy[t] * prices[t] * 1000 for t in range(24)])

    # 约束：功率平衡
    for t in range(24):
        prob += (p_buy[t] + renewable[t] == load[t] + p_alkel[t] + p_sell[t])

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return extract_results(prob)
```

#### Step 7: 结果验证

**输入**：`q*_results.json`
**输出**：`validation_report.json`

```bash
python .claude/skills/quality-assurance-auditor/scripts/validate_results.py
```

检查项：
- 范围检查：概率∈[0,1]、成本≥0
- 异常值：NaN/Inf
- 交叉验证：Q1 成本在 Q2 范围内、Q3<Q2

#### Step 8: 图表生成

**输入**：`q*_results.json`
**输出**：`paper_output/figures/*.png`

```bash
python paper_output/code/visualization/gen_figures.py
```

生成 5 张图：
1. `methodology.png` — 方法论流程图
2. `q1_analysis.png` — Q1 功率曲线 + 绿电指标
3. `q2q3_comparison.png` — Q2/Q3 成本对比
4. `q3_heatmap.png` — 24 场景热力图
5. `q4_analysis.png` — 离网运行分析

#### Step 9: 论文写作

**输入**：所有结果 + 图表
**输出**：`final_paper.docx`

```bash
python paper_output/code/visualization/gen_paper_v3.py
```

论文结构：
1. 摘要（500 字）
2. 一、问题重述
3. 二、问题分析
4. 三、模型假设
5. 四、符号说明
6. 五、模型建立与求解（Q1-Q5）
7. 六、灵敏度分析
8. 七、模型检验
9. 八、模型评价与推广
10. 九、结论
11. 参考文献

#### Step 10: 格式门禁

**输入**：`final_paper.docx`
**输出**：`format_check_report.json`

```bash
python .claude/skills/paper-formal-writer/scripts/check_paper_format.py
```

检查项：
- 字数 ≥ 18000
- 有三级标题结构
- 图表已引用
- 正文宋体小四（12pt）
- 标题黑体加粗（16pt/14pt/12pt）

### 4.3 关键代码文件

| 文件 | 职责 | 行数 | 依赖 |
|------|------|------|------|
| `paper_output/code/data_processing/load_data.py` | 数据加载（8 个 Excel） | ~130 | pandas, openpyxl |
| `paper_output/code/modeling/optimizer_v2.py` | PuLP 优化器（Q2-Q4） | ~180 | pulp, numpy |
| `paper_output/code/modeling/q1_model.py` | Q1 典型日分析 | ~80 | load_data |
| `paper_output/code/modeling/q2_model.py` | Q2 离散调度 | ~100 | optimizer_v2 |
| `paper_output/code/modeling/q3_model.py` | Q3 连续调度 | ~80 | optimizer_v2 |
| `paper_output/code/modeling/q4_model.py` | Q4 离网+储能 | ~100 | optimizer_v2 |
| `paper_output/code/visualization/gen_figures.py` | 图表生成 | ~150 | matplotlib |
| `paper_output/code/visualization/gen_paper_v3.py` | 论文生成 | ~400 | python-docx |
| `.claude/skills/paper-formal-writer/scripts/check_paper_format.py` | 格式门禁 | ~600 | python-docx |
| `.claude/skills/quality-assurance-auditor/scripts/validate_results.py` | 结果验证 | ~200 | numpy |
| `.claude/skills/data-cleaning-and-visualization/scripts/auto_pipeline.py` | 数据处理 | ~200 | pandas |

### 4.4 结果文件说明

| 文件 | 格式 | 内容 |
|------|------|------|
| `q1_optimizer.json` | JSON | Q1 典型日分析：功率曲线、绿电指标、成本 |
| `q2_results.json` | JSON | Q2 离散调度：典型场景 + 24 场景统计 |
| `q3_results.json` | JSON | Q3 连续调度：24 场景详细结果 |
| `q4_results.json` | JSON | Q4 离网分析：无储能 + 储能配置 |
| `validation_report.json` | JSON | 验证报告：范围检查、交叉验证 |
| `data_summary.json` | JSON | 数据摘要：列名、统计量、数据类型 |
| `format_check_report.json` | JSON | 格式检查：字数、字体、章节、图表 |

---

## 5. 使用方法

### 5.1 环境准备

```bash
# 1. 安装 Python 依赖
pip install pandas numpy matplotlib seaborn scipy pulp python-docx openpyxl pypdf

# 2. 安装 Node.js（用于 MCP Server）
# 下载：https://nodejs.org/

# 3. 安装 Claude Code
# 下载：https://claude.ai/code

# 4. 克隆本项目
git clone <repo-url>
cd 数学建模

# 5. 验证安装
python -c "import pandas, numpy, matplotlib, pulp, docx; print('OK')"
```

### 5.2 快速开始

```bash
# 1. 把赛题和附件放到 problem_files/ 目录
mkdir -p problem_files/A题
cp 赛题.pdf problem_files/A题/
cp 附件*.xlsx problem_files/A题/

# 2. 启动 Claude Code
claude

# 3. 输入触发词
# "开始生成"
# 或 "跑一下这个题"
# 或 "使用 MathModel Skill"

# 4. Claude 会自动执行 Step 1-10
# 中间可能需要你确认某些步骤

# 5. 最终输出在 paper_output/final_paper.docx
```

### 5.3 手动口令

| 口令 | 对应操作 | 何时用 |
|------|----------|--------|
| `/model-selector` | 智能选模 | 不确定用什么模型时 |
| `/chart-recommender` | 图表推荐 | 不确定画什么图时 |
| `/defense-simulator` | 答辩模拟 | 准备答辩时 |
| `/algorithm-runner` | 算法执行 | 想运行特定算法时 |
| `/paper-rewriter` | 段落改写 | 润色论文时 |
| `/diagram-maker` | 流程图生成 | 需要流程图时 |
| `/interactive-chart` | 交互式图表 | 数据探索时 |
| `/math-figure` | 数学图表 | 需要函数图/几何图时 |
| `/network-graph` | 网络图可视化 | 图论问题时 |

### 5.4 单脚本运行

```bash
# 数据处理
python .claude/skills/data-cleaning-and-visualization/scripts/auto_pipeline.py

# 结果验证
python .claude/skills/quality-assurance-auditor/scripts/validate_results.py

# 格式门禁
python .claude/skills/paper-formal-writer/scripts/check_paper_format.py

# 图表生成
python paper_output/code/visualization/gen_figures.py

# 论文生成
python paper_output/code/visualization/gen_paper_v3.py

# 运行所有模型
python paper_output/code/modeling/run_v2.py
```

### 5.5 常见操作

**想重新生成论文**：
```bash
python paper_output/code/visualization/gen_paper_v3.py
```

**想重新生成图表**：
```bash
python paper_output/code/visualization/gen_figures.py
```

**想验证结果**：
```bash
python .claude/skills/quality-assurance-auditor/scripts/validate_results.py
```

**想检查格式**：
```bash
python .claude/skills/paper-formal-writer/scripts/check_paper_format.py
```

---

## 6. 目录结构

```
数学建模/
├── CLAUDE.md                    ← 系统总控文档（必读）
├── AGENTS.md                    ← 完整系统规则（17 章）
├── .mcp.json                    ← MCP Server 配置
├── .gitignore                   ← Git 忽略规则
│
├── .claude/
│   ├── agents/                  ← 9 个专业 Agent
│   │   ├── code-tester.md
│   │   ├── paper-reviewer.md
│   │   ├── data-validator.md
│   │   ├── data-explorer.md
│   │   ├── model-comparison.md
│   │   ├── citation-checker.md
│   │   ├── competition-prep.md
│   │   ├── matlab-reviewer.md
│   │   └── blind-panel-judge.md ← 盲评单座（v4.1）
│
│   ├── skills/                  ← 54 个 Skill（v4.8 大扫除后；另有 _archive/ 14 个归档）
│   │   ├── paper-workflow-orchestrator/
│   │   ├── problem-doc-model-selector/
│   │   ├── modeling-paper-rubric-and-model-selector/
│   │   ├── data-cleaning-and-visualization/
│   │   ├── model-code-and-result-generator/
│   │   ├── quality-assurance-auditor/
│   │   ├── paper-formal-writer/
│   │   ├── model-selector/
│   │   ├── chart-recommender/
│   │   ├── diagram-maker/
│   │   └── ... (54 total)
│
│   ├── hooks/                   ← 7 个 Hook
│   │   ├── protect_outputs.py
│   │   ├── precommit_secret_guard.py
│   │   ├── check_python.py
│   │   ├── format_python.py
│   │   ├── auto_evidence_gate.py
│   │   ├── log_exit_code.py
│   │   └── check_index_sync.py
│   │
│   └── settings.json            ← Skill 注册 + Hook 配置
│
├── problem_files/               ← 赛题 PDF + 附件（手动放入）
│   └── A题/
│       ├── A题.pdf
│       └── 附件*.xlsx
│
├── paper_output/                ← ★ 统一输出目录
│   ├── final_paper.docx         ← 最终 Word 论文
│   ├── code/
│   │   ├── data_processing/
│   │   │   └── load_data.py     ← 数据加载
│   │   ├── modeling/
│   │   │   ├── optimizer_v2.py  ← PuLP 优化器
│   │   │   ├── q1_model.py      ← Q1 模型
│   │   │   ├── q2_model.py      ← Q2 模型
│   │   │   ├── q3_model.py      ← Q3 模型
│   │   │   ├── q4_model.py      ← Q4 模型
│   │   │   └── run_v2.py        ← 运行所有
│   │   └── visualization/
│   │       ├── gen_figures.py   ← 图表生成
│   │       └── gen_paper_v3.py  ← 论文生成
│   ├── results/
│   │   ├── clean_*.csv          ← 清洗后数据
│   │   ├── data_summary.json    ← 数据摘要
│   │   ├── q*_results.json      ← 各问题结果
│   │   ├── validation_report.json ← 验证报告
│   │   └── format_check_report.json ← 格式检查
│   ├── figures/
│   │   └── *.png                ← 论文图表
│   ├── tables/
│   │   └── *.csv                ← 论文表格
│   └── plan/
│       ├── model_route.json     ← 模型路线
│       └── paper_outline.json   ← 论文大纲
│
├── outputs/                     ← 知识库（75 文件 + scripts/、_reports/）
│   ├── INDEX.md                 ← 统一索引
│   ├── scoring_rubric.md        ← 评分量表
│   ├── method_matching.md       ← 方法匹配表
│   ├── writing_templates.md     ← 写作模板
│   └── ...
│
├── resources/                   ← 参考资料
│   ├── 04_代码模板/             ← 64+ 算法模板
│   ├── 06_图表教程/             ← 50+ 图表教程
│   └── ...
│
├── docs/                        ← 文档
│   └── SYSTEM_GUIDE.md          ← 本文档
│
└── deliverables/                ← 历史竞赛成品
    ├── papers/
    ├── code/
    └── figures/
```

---

## 7. 扩展指南

### 7.1 添加新 Skill

#### 步骤 1：创建目录和 SKILL.md

```bash
mkdir -p .claude/skills/my-skill
```

创建 `.claude/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: 做某件事的 skill
disable-model-invocation: true  # 可选：禁止 Claude 自动调用
---

# My Skill

## 触发词
`做某件事` `my-skill`

## 工作流
1. 第一步：做什么
2. 第二步：做什么
3. 第三步：做什么

## 输入
- 输入格式说明

## 输出
- 输出文件路径
- 输出格式说明

## 约束
- 约束条件 1
- 约束条件 2
```

#### 步骤 2：（可选）添加脚本

```bash
mkdir -p .claude/skills/my-skill/scripts
```

创建 `.claude/skills/my-skill/scripts/my_script.py`：

```python
#!/usr/bin/env python3
"""My skill script."""
import sys
import json

def main():
    # 读取输入
    data = json.load(sys.stdin)

    # 处理逻辑
    result = process(data)

    # 输出结果
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)

def process(data):
    # 你的逻辑
    return {"status": "ok"}

if __name__ == "__main__":
    main()
```

#### 步骤 3：注册到 settings.json

编辑 `.claude/settings.json`，在 `skills` 字段中添加：

```json
{
  "skills": {
    "my-skill": {
      "name": "我的 Skill",
      "description": "做某件事",
      "disable-model-invocation": true
    }
  }
}
```

#### 步骤 4：测试

```bash
# 在 Claude Code 中输入触发词
# "做某件事"
# 或 "/my-skill"
```

### 7.2 添加新 Agent

创建 `.claude/agents/my-agent.md`：

```markdown
# My Agent

## 职责
描述这个 Agent 做什么。

## 输入
- 输入格式说明

## 输出
- 输出格式说明

## 工具使用
- 使用哪些工具（Bash, Read, Glob, etc.）

## 工作流
1. 第一步
2. 第二步
3. 第三步

## 约束
- 约束条件
```

**使用方式**：在 Claude Code 中，Claude 会自动根据任务选择合适的 Agent。

### 7.3 添加新 Hook

#### 步骤 1：创建 Hook 脚本

创建 `.claude/hooks/my_hook.py`：

```python
#!/usr/bin/env python3
"""My hook description."""
import sys
import json

def main():
    # 从 stdin 读取 JSON
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 解析失败则放行

    # 获取文件路径
    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # 你的逻辑
    if should_block(file_path):
        print(f"Blocked: {file_path}", file=sys.stderr)
        sys.exit(2)  # 阻止

    sys.exit(0)  # 允许

def should_block(file_path):
    # 你的判断逻辑
    return False

if __name__ == "__main__":
    main()
```

#### 步骤 2：注册到 settings.json

编辑 `.claude/settings.json`，在 `hooks` 字段中添加：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python e:/数学建模/.claude/hooks/my_hook.py"
          }
        ]
      }
    ]
  }
}
```

**注意**：必须使用绝对路径！

### 7.4 添加新 MCP Server

编辑 `.mcp.json`，添加新的 server 配置：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server-package"]
    }
  }
}
```

或使用 Python：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/my_server.py"]
    }
  }
}
```

### 7.5 修改优化模型

如果要修改优化模型（例如添加新约束或新变量）：

1. 编辑 `paper_output/code/modeling/optimizer_v2.py`
2. 修改 `solve_schedule()` 函数
3. 运行 `python paper_output/code/modeling/run_v2.py` 测试
4. 运行 `python .claude/skills/quality-assurance-auditor/scripts/validate_results.py` 验证

---

## 8. 踩坑记录

### 8.1 Hook 相关

#### 问题 1：Hook 路径找不到

**现象**：编辑子目录文件时，Hook 报错 `can't open file '.claude/hooks/xxx.py'`

**原因**：Hook 配置了相对路径，Claude Code 在子目录执行时找不到

**解决**：使用绝对路径
```json
{
  "command": "python e:/数学建模/.claude/hooks/protect_outputs.py"
}
```

#### 问题 2：Hook 读不到文件路径

**现象**：Hook 中 `os.environ.get("CLAUDE_FILE_PATH")` 返回空

**原因**：Claude Code 通过 stdin JSON 传递数据，不是环境变量

**解决**：改为从 stdin 读取
```python
data = json.load(sys.stdin)
file_path = data.get("tool_input", {}).get("file_path", "")
```

### 8.2 优化器相关

#### 问题 3：LP 求解报 "unbounded"

**现象**：`linprog` 返回 `The problem is unbounded`

**原因**：P_buy 和 P_sell 可以同时为正，形成套利（低谷电价 0.3424 < 上网电价 0.3779）

**解决**：加购售电互斥约束
```python
# 方案 1：加 bounds
bounds[BUY + t] = (0, max_load_total)
bounds[SELL + t] = (0, float(renewable[t]))

# 方案 2：用 PuLP 的 0-1 变量
z_buy = [pulp.LpVariable(f"z_buy_{t}", 0, 1, cat='Binary') for t in range(24)]
prob += p_buy[t] <= M * z_buy[t]
prob += p_sell[t] <= M * (1 - z_buy[t])
```

#### 问题 4：Q2/Q3 结果相同

**现象**：离散和连续调度结果一样

**原因**：用连续 LP 做离散调度，没有 0-1 变量

**解决**：用 PuLP 的 `LpBinary` 变量
```python
z_alkel = [pulp.LpVariable(f"z_alkel_{t}", 0, 1, cat='Binary') for t in range(24)]
p_alkel = [z_alkel[t] * scale * ALKEL_POWER for t in range(24)]
```

### 8.3 论文生成相关

#### 问题 5：字体不对

**现象**：Word 打开后字体是 Calibri，不是宋体

**原因**：python-docx 默认字体是模板的默认字体（Calibri）

**解决**：显式设置字体
```python
run.font.name = 'Times New Roman'
run.font.size = Pt(12)
run.element.rPr.rFonts.set(
    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia',
    '宋体'
)
```

#### 问题 6：参考文献编造

**现象**：参考文献是 Claude 编造的，不存在

**原因**：Claude 会根据上下文生成看起来合理的文献

**解决**：使用 `citation-tracer` skill 验证引用真实性，或用 `authoritative-data-harvester`（含多源检索子能力）检索真实文献

### 8.4 格式门禁相关

#### 问题 7：格式门禁检查 markdown 不检查 docx

**现象**：门禁报 "字数不足"，但 docx 已经 18000+ 字

**原因**：门禁检查的是 `final_paper_source.md`（旧版），不是 `final_paper.docx`

**解决**：改为从 docx 提取文本
```python
def extract_docx_text(path):
    doc = Document(str(path))
    texts = []
    for para in doc.paragraphs:
        if para.text.strip():
            texts.append(para.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if para.text.strip():
                        texts.append(para.text)
    return "\n".join(texts)
```

#### 问题 8：章节标题匹配不到

**现象**：门禁报 "缺少 1 问题重述"，但 docx 中有 "一、问题重述"

**原因**：docx 用中文数字（一、二、三），门禁只匹配阿拉伯数字（1、2、3）

**解决**：添加中文数字映射
```python
CN_NUMBERS = {'一': '1', '二': '2', '三': '3', ...}

def has_required_section(text, label):
    number, title = label.split(" ", 1)
    # 匹配阿拉伯数字
    if re.search(rf"^{number}[.、\s]+.*{title}", text):
        return True
    # 匹配中文数字
    for cn, ar in CN_NUMBERS.items():
        if ar == number:
            if re.search(rf"^{cn}[、\s]+.*{title}", text):
                return True
    return False
```

---

## 9. 附录

### 9.1 完整 Skill 列表（54 个，v4.8）

> v4.8 归档 14 个（9 Nature + academic-paper-strategist/composer/defense-pptx + csv-data-summarizer + result-validator），新建 1 个（defense-ppt-builder-zh）。详见 `.claude/settings.json`。

```json
{
  "skills": {
    "scan": { "name": "扫描资料" },
    "card": { "name": "抽卡" },
    "rules": { "name": "建规则库" },
    "analyze": { "name": "审题" },
    "review": { "name": "审论文" },
    "code": { "name": "生成代码" },
    "figure": { "name": "生成图示" },
    "defense": { "name": "准备答辩" },
    "submit": { "name": "提交包" },
    "git-snapshot": { "name": "项目快照" },
    "algorithm-test": { "name": "代码测试" },
    "paper-workflow-orchestrator": { "name": "论文流水线总控" },
    "problem-doc-model-selector": { "name": "题意解析" },
    "modeling-paper-rubric-and-model-selector": { "name": "模型路线与评分" },
    "authoritative-data-harvester": { "name": "权威数据获取" },
    "data-cleaning-and-visualization": { "name": "数据清洗与可视化" },
    "model-code-and-result-generator": { "name": "建模代码与结果" },
    "quality-assurance-auditor": { "name": "质量门禁审计" },
    "paper-formal-writer": { "name": "正式论文成稿" },
    "paper-micro-unit-generator": { "name": "微单元生成" },
    "context-memory-keeper": { "name": "上下文记忆" },
    "latex-renderer": { "name": "LaTeX公式渲染" },
    "word-counter": { "name": "论文字数统计" },
    "matlab-code-reviewer": { "name": "Matlab代码审查" },
    "python-code-reviewer": { "name": "Python代码审查" },
    "matlab-model-code-generator": { "name": "Matlab代码生成" },
    "solution-package-builder": { "name": "解决方案包构建" },
    "paper-polisher": { "name": "论文润色" },
    "robustness-checker": { "name": "鲁棒性检验" },
    "symbol-table-builder": { "name": "符号表构建" },
    "model-selector": { "name": "智能选模" },
    "chart-recommender": { "name": "图表推荐" },
    "defense-simulator": { "name": "答辩模拟" },
    "algorithm-runner": { "name": "算法执行" },
    "paper-rewriter": { "name": "段落改写" },
    "diagram-maker": { "name": "流程图生成" },
    "interactive-chart": { "name": "交互式图表" },
    "math-figure": { "name": "数学图表" },
    "network-graph": { "name": "网络图可视化" },
    "defense-ppt-builder-zh": { "name": "国赛答辩PPT生成器" },
    "aigc-reduce": { "name": "AIGC降重" },
    "humanizer-zh-academic": { "name": "中文学术降AI" },
    "consistency-auditor": { "name": "一致性审计" },
    "completeness-auditor": { "name": "完整性审计" },
    "decision-logger": { "name": "决策日志" },
    "feature-engineering": { "name": "特征工程" },
    "algorithm-benchmark": { "name": "算法基准测试" },
    "style-calibration": { "name": "写作风格校准" },
    "citation-tracer": { "name": "引用溯源" },
    "ai-failure-checker": { "name": "AI失败模式检查" },
    "blind-panel": { "name": "盲评Panel" },
    "typst-renderer": { "name": "Typst论文渲染" },
    "docx-editor-cn": { "name": "Word原生公式与XML编辑" },
    "award-paper-rag": { "name": "O奖论文章节级RAG" }
  }
}
```

### 9.2 Python 依赖清单

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
pulp>=2.7.0
python-docx>=0.8.11
openpyxl>=3.0.10
pypdf>=3.0.0
pyyaml>=6.0
requests>=2.28.0
```

### 9.3 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [PuLP 文档](https://coin-or.github.io/pulp/)
- [python-docx 文档](https://python-docx.readthedocs.io/)
