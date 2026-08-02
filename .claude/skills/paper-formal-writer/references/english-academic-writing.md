# 美赛英文学术写作指南

> **来源**：从 `nature-writing` v0.2.0（已归档）抽取核心方法论，美赛 MCM/ICM 适配。
> **用途**：美赛英文论文写作的论证骨架、章节模板、句式库。
> **适用场景**：**仅美赛**。国赛/五一赛/MathorCup 用中文，不需要本文档。
> **配合**：`section-architecture.md`（章节架构）+ `common-phrases.md`（双语短语）。

---

## 核心方法论：论证驱动写作

> "Write the argument before writing the sentences."

美赛论文的核心不是"英文好"，而是**论证链清晰**。AI 帮你润色英文，但不能帮你构造论证。

### 论证三件套（claim / evidence / boundary）

每段必须回答 3 个问题：

| 要素 | 含义 | 示例 |
|------|------|------|
| **claim** | 这段要声明什么 | "Our model achieves 95.3% accuracy on the test set." |
| **evidence** | 用什么证据支撑 | "As shown in Figure 4, the confusion matrix shows..." |
| **boundary** | 这个声明在什么条件下成立 | "This accuracy holds when the sample size exceeds 1000; below that, performance degrades." |

**缺一不可**：只有 claim 没有 evidence = 空话；有 evidence 没 claim = 数据堆砌；没 boundary = 过度声明。

---

## 一句话论证模板

在写每段前，先用一句话概括这段的论证：

```
In [system/problem], we show [advance] using [approach],
supported by [evidence], with [boundary].
```

**示例**：
> In the bike-sharing demand prediction problem, we show that a gradient boosting model with weather features outperforms baseline ARIMA by 12.3% in RMSE, supported by 5-fold cross-validation on the 2019-2021 dataset, with the boundary that this advantage diminishes for stations with fewer than 50 daily trips.

---

## 章节默认架构（美赛特化）

### Summary（Executive Summary）

美赛 Summary 是**独立成文**的，不是论文摘要的复制。结构：

```
1. Problem context (1-2 sentences)
2. Our approach (2-3 sentences, 含核心模型名)
3. Key results (2-3 sentences, 含具体数字)
4. Recommendations (1-2 sentences, 落地建议)
```

**字数**：1 页（约 500 词），不超过 2 页。

**句式**：
- 开头：`We model the [problem] as a [model type] to [objective].`
- 结果：`Our model achieves [metric] = [value], outperforming [baseline] by [improvement].`
- 建议：`We recommend [action], which would [expected benefit] under [condition].`

### Introduction

美赛 Introduction 比国赛更"叙事化"，结构：

```
1. Background (为什么这个问题重要)
2. Problem restatement (用自己的话重述题目)
3. Our approach (概述我们的思路)
4. Paper organization (可选：本文结构)
```

**句式**：
- 背景：`[Problem] has attracted increasing attention due to [reason].`
- 重述：`In this paper, we address the [Competition] Problem [X], which asks us to [task].`
- 思路：`Our approach combines [method A] with [method B] to [objective].`

### Results

美赛 Results 的时态规则：

| 内容 | 时态 | 示例 |
|------|------|------|
| 报告观察结果 | 过去时 | "The model achieved 95.3% accuracy." |
| 描述图表 | 现在时 | "Figure 3 shows the Pareto frontier." |
| 解释/讨论 | 现在时 | "This suggests that..." |

**禁止**：在 Results 段就开始解释"为什么"——那是 Discussion 的职责。

### Discussion / Sensitivity Analysis

美赛很看重 Sensitivity Analysis（灵敏度分析），结构：

```
1. What we tested (参数变化范围)
2. What happened (结果变化)
3. What it means (模型稳健性结论)
```

**句式**：
- 测试：`We varied [parameter] by ±20% to test model robustness.`
- 结果：`The optimal solution changed by only 3.2%, indicating low sensitivity.`
- 结论：`Our model is robust to [parameter] perturbations within [range].`

### Strengths and Weaknesses

美赛必有此节，结构：

```
Strengths:
1. [Strength 1] + [quantitative evidence]
2. [Strength 2] + [quantitative evidence]

Weaknesses:
1. [Weakness 1] + [why] + [mitigation]
2. [Weakness 2] + [why] + [mitigation]
```

**禁止**：只说优点不说缺点（美赛评审认为"承认局限=学术成熟"）。

---

## 动词校准（Calibrate verbs）

不同动词的"力度"不同，按证据强度选择：

| 力度 | 动词 | 用法 |
|------|------|------|
| 强 | `show`, `demonstrate`, `prove` | 有严格证明/大量数据 |
| 中 | `suggest`, `indicate`, `enable` | 有数据支撑但需谨慎 |
| 弱 | `may`, `could`, `might` | 推测/未来工作 |

**规则**：
- Results 用强动词（因为有数据）
- Discussion 用中/弱动词（因为是解释）
- **不要全篇用 `show`**（过度声明）

---

## 中式英语的 5 大失败模式

| 失败模式 | 中式英语 | 学术英语 |
|---------|---------|---------|
| 主语过长 | "It is obviously seen from Figure 3 that..." | "Figure 3 shows that..." |
| 无主语 | "By using this method, obtained the result..." | "Using this method, we obtained..." |
| 形容词堆砌 | "very very important" | "critical" / "essential" |
| 逻辑连接缺失 | 句子之间没有过渡词 | "However," / "Therefore," / "In contrast," |
| 时态混乱 | Results 段混用过去时和现在时 | Results 统一过去时 |

---

## 写作顺序（推荐）

美赛推荐写作顺序（非章节顺序）：

```
1. Results（先有数据）
2. Introduction + Conclusion（有了结果才能写引言和结论）
3. Title（最后定标题）
4. Discussion（有了结果才能讨论）
5. Methods（补方法细节）
6. Summary（最后写，浓缩全文）
```

**理由**：先写有数据支撑的部分（Results），再写需要全局视角的部分（Intro/Conclusion/Summary）。

---

## 与其他文档的关系

| 文档 | 分工 |
|------|------|
| 本文档 | 美赛英文写作的**方法论**（论证骨架、句式、时态） |
| `section-architecture.md` | 章节架构（中英文通用） |
| `common-phrases.md` | 中英双语学术短语库（10 章节） |
| `outputs/writing_templates.md` | 国赛中文模板（本文档是其英文版补充） |
| `outputs/phrase_bank.md` | 国赛高频句式（中文） |

---

## 禁止行为

- ❌ 用 Google Translate 逐句翻译中文草稿（逻辑会丢失）
- ❌ Summary 超过 2 页（美赛 Summary 1 页最佳）
- ❌ Results 段就开始解释"为什么"
- ❌ 全篇用 `show`（过度声明）
- ❌ 没有 Sensitivity Analysis（美赛必考）
- ❌ Strengths and Weaknesses 只写优点