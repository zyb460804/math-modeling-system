---
name: latex-renderer
description: LaTeX 公式渲染器。将 LaTeX 公式转为 PNG 图片嵌入 Word，或生成公式编号清单。触发词：渲染公式、LaTeX转图片、latex render、公式渲染、公式PNG、LaTeX公式编译。
tools: Read, Write, Edit, Bash, Glob
---

# LaTeX 公式渲染

## 触发词

`渲染公式` `LaTeX转图片` `公式嵌入Word` `生成公式图片`

## 功能

1. **扫描论文**：从 `paper_output/` 中的 .md 文件提取所有 LaTeX 公式（`$...$` 和 `$$...$$`）
2. **渲染为 PNG**：使用 matplotlib 将公式渲染为高分辨率 PNG 图片
3. **生成清单**：输出 `paper_output/tables/formula_index.json`，记录公式编号、LaTeX 源码、图片路径
4. **嵌入提示**：生成 python-docx 代码片段，将公式图片插入 Word 文档

## 使用方式

```
/latex-renderer                    # 扫描并渲染所有公式
/latex-renderer --formula "E=mc^2" # 渲染单个公式
/latex-renderer --dpi 300          # 指定分辨率
```

## 输出结构

```
paper_output/
├── figures/
│   ├── formula_001.png
│   ├── formula_002.png
│   └── ...
└── tables/
    └── formula_index.json
```

## 依赖

- matplotlib（已安装）
- Python 3.8+

## 实现脚本

调用时执行：`paper_output/code/visualization/render_latex.py`

如脚本不存在，由 skill 引导 Claude 生成该脚本后执行。

## LaTeX 论文编译（整篇 .tex → PDF）

整篇论文编译（非单公式渲染）用专用脚本：

```
.claude/skills/paper-formal-writer/scripts/compile_latex.py
  --tex paper_output/latex/main.tex --engine xelatex --passes 2
```

融合自 AutoMCM-Pro：默认 2 pass（处理 TOC/交叉引用），失败解析 `.log` 错误行，最多重试 3 轮。退出码 0=成功 / 1=失败 / 2=引擎未安装。