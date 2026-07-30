# 工具集（Tools）

> **版本**: v1.1 | **更新**: 2026-07-26
> **设计理念**: 参考 XiaoMaColtAI/math-modeling-skill 的工具集分离设计
> **v1.1 说明**: v1.0 规划的 docx/pdf/xlsx/feature_engineering 4 个子目录从未落地（空目录已于 v4.5 体检时清理）。等价能力已由 `.claude/skills/` 内的脚本承担，见下方「能力路由」。

---

## 目录结构（实际）

```
tools/
├── paper_search/            # 论文检索工具
│   ├── README.md
│   └── scripts/search_papers.py
└── visualization/           # 可视化工具（仅 README，脚本见 figure 系 skill）
    └── README.md
```

---

## 工具清单

### 论文检索（paper_search）

| 工具 | 用途 |
|------|------|
| `search_papers.py` | 从 Semantic Scholar / arXiv 搜索学术论文 |

```bash
python tools/paper_search/scripts/search_papers.py --query "mathematical modeling"
```

---

## 能力路由（v1.0 规划目录 → 实际承担者）

| 原规划 | 实际入口 |
|--------|---------|
| docx/（Word 处理） | `.claude/skills/docx-editor-cn/`（原生公式 + XML 编辑）、`paper-formal-writer`（Word 排版） |
| pdf/（PDF 处理） | `.claude/skills/data-cleaning-and-visualization/scripts/extract_pdf_tables.py`（表格）、`problem-doc-model-selector/scripts/extract_formulas_ocr.py`（公式 OCR） |
| xlsx/（Excel 处理） | pandas 直读直写（各代码模板内置） |
| feature_engineering/ | `.claude/skills/feature-engineering/scripts/`（preprocess.py / shap_explain.py） |
| visualization/ 脚本 | `.claude/skills/math-figure/`、`interactive-chart`、`network-graph`、`diagram-maker` |

---

## 设计原则

1. **工具独立**: 每个工具可以独立运行
2. **接口统一**: 所有工具使用统一的命令行接口
3. **不重复建设**: skill 内已有的能力不在 tools/ 下复制第二份
4. **可扩展**: 确有跨 skill 复用需求时再新建子目录，落地脚本与 README 同步创建

---

## 版本历史

- v1.1 (2026-07-26): 对齐实际——清理 4 个空目录，补能力路由表（v4.5 体检）
- v1.0 (2026-06-21): 初始版本，创建工具集分离结构
