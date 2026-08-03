---
name: typst-renderer
description: Typst 论文渲染器。从 17 套赛事模板选型，将 final_paper_source.md 注入 Typst 模板并编译为 PDF，或直接渲染 Typst 公式。与 latex-renderer 并列，为偏好 Typst 排版的赛题提供更快的编译链路。触发词：Typst渲染、编译Typst、用Typst排版、typst renderer、Typst PDF、Typst模板。
tools: Read, Write, Edit, Bash, Glob
---

# Typst 论文渲染

> 融合自 `jihe520/MathModelAgent`（2862★）。Typst 相对 LaTeX 的优势：编译快（毫秒级）、语法简洁、原生中文/公式/图表支持好、单文件依赖少。本项目默认 Word 主交付，本 skill 提供 Typst 可选交付链路。

## 触发词

`Typst 渲染` `编译 Typst` `生成 Typst 论文` `Typst 转 PDF` `用 Typst 排版`

## 模板库（17 套，位于 `resources/15_Typst模板/`）

| 赛事 | 中文 (zh) | 英文 (en) |
|------|-----------|-----------|
| 默认通用 | zh/default | en/default |
| 国赛 CUMCM | zh/cumcm | — |
| 美赛 MCM/ICM | zh/mcm | en/mcm |
| 亚太 APMCM | zh/apmcm | en/apmcm |
| 华数杯 | zh/huashubei | — |
| 华为杯 | zh/huaweibei | — |
| 长三角 | zh/changsanjiao | — |

每套含 `main.typ`（入口）+ `references.typ`（引用）+ `sections/*.typ`（按章节分文件）。同结构 LaTeX 版本在 `*-latex/` 目录（供 latex-renderer 复用）。

## 功能

1. **模板选型**：根据 `paper_output/step1/problem_analysis.json` 的 `competition` 字段自动匹配赛事模板；未识别时用 `default`
2. **内容注入**：从 `paper_output/final_paper_source.md` 解析章节，按章节写入对应 `sections/*.typ`
3. **编译 PDF**：调用 `typst compile main.typ` 生成 `paper_output/final_paper.pdf`
4. **公式直渲**：单条 Typst/LaTeX 公式 → PNG（回退到 latex-renderer 的 matplotlib 链路）
5. **编译自检**：编译失败时解析错误行号，最多重试 3 次（对齐 AutoMCM-Pro 的 LaTeX 重试机制）

## 使用方式

```
/typst-renderer                         # 自动选型 + 注入 + 编译
/typst-renderer --template mcm --lang en # 指定模板
/typst-renderer --compile-only           # 仅编译已有 main.typ
/typst-renderer --formula "E=mc^2"       # 渲染单条公式为 PNG
```

## 输出结构

```
paper_output/
├── typst/                     # 当前赛题 Typst 工作区
│   ├── main.typ
│   ├── references.typ
│   └── sections/*.typ
└── final_paper.pdf            # 编译产物
```

## 依赖

- **Typst CLI**（必须）：`winget install --id Typst.Typst` 或 `cargo install --locked typst-cli`
- Python 3.8+（模板注入脚本）

若 Typst 未安装，skill 引导安装后再编译；公式直渲回退到 latex-renderer。

## 实现脚本

- **内容注入+编译**：`scripts/inject_typst.py`（md→typst 语法转换 + 模板自动选型 + 复制到 paper_output/typst/ + `typst compile` 带 3 次重试）
- **模板索引**：`scripts/build_typst_index.py`（扫描 `resources/15_Typst模板/` 生成 typst_index.json）

## 与其它 skill 的关系

- **latex-renderer**：并列。Typst 用本 skill，LaTeX 用 latex-renderer，两条交付链路二选一
- **paper-formal-writer**：Word 主交付不变；Typst 是 `final_paper_source.md` 之后的**可选**导出分支
- **quality-assurance-auditor**：Typst 编译产物进 G6 格式门禁（PDF 编译必须成功）
