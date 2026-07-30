---
name: docx-editor-cn
description: 中文学术 Word 编辑器。两条能力：(1) LaTeX 公式 → Word 原生 OMML 公式（temml→MathML→docx 链）；(2) 已有 .docx 的 XML 级局部编辑（unpack/pack/validate）。补 paper-formal-writer 不具备的"局部改 Word"和"原生公式注入"能力。
tools: Read, Write, Edit, Bash, Glob
---

# 中文学术 Word 编辑器

> 融合自 `Gostyan/docx-skill-4-cn-paper`（335★）。本 skill 与 `paper-formal-writer` 互补：
> `paper-formal-writer` 负责**整篇生成** Word；本 skill 负责**局部 XML 编辑**和**原生公式注入**。

## 触发词

`编辑 Word` `改 Word 公式` `局部修改 docx` `LaTeX 公式转 Word 原生` `三线表` `docx 解包`

## 两条核心能力

### 能力 1：LaTeX → Word 原生公式（Node.js 链）

```
LaTeX 字符串 → temml → MathML → mathml-to-docx.js → Word 原生 OMML
```

- `scripts/convert_paper.js`：Markdown → 完整 .docx（含公式/三线表/自动编号/上标引用）
- `scripts/mathml-to-docx.js`：MathML → docx OMML 转换器
- `scripts/new_doc.js`：docx 构建辅助函数
- `scripts/formula.py` / `scripts/table.py`：公式/表格预处理

**首次使用需安装依赖**（Node.js ≥ 18）：
```bash
cd .claude/skills/docx-editor-cn && npm install   # docx, fast-xml-parser, temml
```

### 能力 2：已有 .docx 的 XML 级局部编辑（纯 Python，无依赖）

```
现有 .docx → unpack.py（解包 XML）→ 编辑 document.xml/styles.xml → pack.py（重打包）→ validate.py（校验）
```

- `scripts/office/unpack.py`：解压 .docx 为可读 XML
- `scripts/office/pack.py`：XML → .docx（159 行）
- `scripts/office/validate.py`：文档完整性校验（111 行）
- `scripts/office/soffice.py`：LibreOffice 调用（格式转换/PDF 导出，183 行）
- `scripts/office/helpers/merge_runs.py`：合并相邻 run
- `scripts/office/helpers/simplify_redlines.py`：简化修订标记

这套工具同时复制到 `paper-formal-writer/scripts/office/`，供 paper-formal-writer 直接调用。

## 使用方式

```
/docx-editor-cn convert --md paper_output/final_paper_source.md --out paper_output/final_paper.docx
/docx-editor-cn formula --latex "E=mc^2"           # 单条公式 → OMML 片段
/docx-editor-cn unpack --docx paper_output/final_paper.docx
/docx-editor-cn pack --xmldir paper_output/docx_xml --out paper_output/final_paper_edited.docx
/docx-editor-cn validate --docx paper_output/final_paper.docx
```

## 默认格式（中国大陆学术规范）

| 项目 | 规格 |
|------|------|
| 纸张 | A4（210mm × 297mm） |
| 页边距 | 上下左右各 2.5cm |
| 正文中文 | 宋体（SimSun） |
| 正文英文/数字 | Cambria Math / Times New Roman |
| 三线表 | 标准三线表样式 |
| 引用 | 上标 [1][2] |
| 编号 | 标题/图/表自动编号 |

## 与其它 skill 的关系

- **paper-formal-writer**：主 Word 交付。本 skill 补其短板（原生公式 + 局部 XML 编辑）
- **typst-renderer / latex-renderer**：Typst/LaTeX 链路。本 skill 是 Word 链路的公式增强
- **quality-assurance-auditor**：`scripts/office/validate.py` 可作 G7 格式门禁的 docx 完整性检查

## 依赖

- **能力 1**：Node.js ≥ 18 + npm install（docx / fast-xml-parser / temml）
- **能力 2**：Python 3.8+，**无第三方依赖**（zipfile + xml.etree）
- **soffice.py**（可选）：LibreOffice（用于 docx→PDF / 格式转换）