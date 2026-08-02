---
name: paper-rewriter
description: 论文段落改写：输入原文+目标风格（学术/简洁/有力/中文/英文），输出改写版本。支持多风格切换。
---

# Paper Rewriter — 论文段落改写

> **此 skill 是 `paper-polisher` 统一入口的内部调度工具。** 用户说"改写""润色这段""换个说法"等均由 `paper-polisher` 统一接收后分派。本 skill 保留独立触发词仅用于向后兼容。

针对数学建模论文的段落级改写工具。

## 触发词

`改写` `润色这段` `换个说法` `更学术一点` `更简洁一点`

## 工作流

### Step 1: 分析原文

- 识别当前语言（中文/英文）
- 识别当前风格（口语/半学术/学术）
- 识别段落功能（引言/方法/结果/讨论/结论）

### Step 2: 确定目标

用户可选目标风格：
- **学术化**：增加专业术语、被动语态、引用格式
- **简洁化**：删除冗余、合并短句、减少修饰
- **有力化**：强化结论、增加数据支撑、使用主动语态
- **国赛风格**：对标 `outputs/high_score_expression_library.md` 和 `outputs/writing_templates.md`

### Step 3: 输出改写

```markdown
## 改写结果

### 原文
> [用户提供的原文]

### 改写版本
> [改写后的文本]

### 改写说明
- [具体修改了什么，为什么]
- [使用了哪些表达技巧]

### 可选：备选版本
> [另一个风格的改写版本]
```

## 改写规则

### 中文论文
- 使用 `outputs/high_score_expression_library.md` 中的高分表达
- 使用 `outputs/transition_sentence_bank.md` 中的过渡句
- 对标 `outputs/section_writing_templates.md` 的段落结构

### 英文论文
- 参考 `paper-formal-writer/references/english-academic-writing.md`（v4.8 从 nature-writing 抽取的美赛英文写作指南）
- 避免中式英语，使用地道学术表达
- 保持时态一致性（方法用过去时，结论用现在时）

## 约束

- 不改变原文的技术含义和数据
- 不添加原文中没有的信息
- 保留原文的引用标记 [X]
- 改写幅度由用户控制（微调/重写）