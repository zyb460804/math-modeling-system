# 去AI味写作指南

> 基于 Wikipedia "Signs of AI writing" 研究整理，针对数学建模竞赛论文的 AI 痕迹识别与去除方法论。

---

## 使用时机

论文初稿完成后、最终交付前，必须通读本文并逐条自查。本文与 `four-round-self-review.md` 第三轮「表述质量审查」配合使用。

---

## 一、八类 AI 写作痕迹（中英文）

### 1. 过度强调重要性（Overemphasis on Importance）

AI 模型倾向于用大词强调每件事的重要性，这在学术写作中显得空洞。

**中文禁用词/短语**：

| 禁用词/短语 | 替换方式 |
|------------|---------|
| 标志着 | 删除或改为具体事实 |
| 重要的 | 删除或用数据说明为什么重要 |
| 关键作用 | 具体描述起到了什么作用 |
| 奠定了坚实基础 | 删除或用具体贡献替代 |
| 发挥了重要作用 | 用数据替代：「使 F1 提升了 3.2%」 |
| 具有重要意义 | 直接说有什么意义 |
| 突显了其重要性 | 删除 |

**英文禁用词/短语**：

| 禁用词/短语 | 替换方式 |
|------------|---------|
| plays a crucial role | is essential for / contributes to（且要具体说什么贡献） |
| marks a significant milestone | 删除或用具体事实替代 |
| has been demonstrated to | has been shown to（更简洁） |
| It is worth noting that | 全文 0-1 次，直接说那件事 |

```
❌ 该模型在食品安全风险预警中发挥了重要作用，标志着智能化监管的新阶段。
✅ 该模型将食品安全风险预警的召回率从 78.3% 提升至 92.1%，误报率降低 4.2 个百分点。

❌ The model plays a crucial role in advancing the field of predictive analytics.
✅ The model improves F1 from 0.82 to 0.91 on the test set, reducing false positives by 38%.
```

---

### 2. 宣传性和广告式语言（Promotional / Ad-style Language）

学术论文不是产品发布会，禁用广告式修辞。

**中文禁用词/短语**：

| 禁用词/短语 | 替换方式 |
|------------|---------|
| 拥有（复杂结构） | 用简单系动词「是/存在/具有」 |
| 突破性的 | 删除，让读者自行判断 |
| 著名的 | 删除 |
| 令人震撼的 | 删除 |
| 惊艳的 | 删除 |
| 完美的 / 极致的 | 用具体指标描述 |
| 充分展示了…的魅力 | 删除 |
| 深入探讨了…的潜力 | 删除 |
| 结果令人振奋 | 直接写结果数据 |

**英文禁用词/短语**：

| 禁用词/短语 | 替换方式 |
|------------|---------|
| groundbreaking | 删除 |
| revolutionary | 删除 |
| remarkable | 全文 0 次 |
| impressive | 删除 |
| state-of-the-art | 只有在确实是 SOTA 且有 benchmark 对比时才用 |
| shed light on | 用具体动词：reveal the mechanism of |
| pave the way for | enable / allow |
| a wide range of | various, diverse（全文 ≤ 1 次） |

```
❌ 本文提出的突破性算法拥有令人震撼的预测精度。
✅ 本文提出的算法在 3 个测试集上的预测精度分别为 95.6%、93.1% 和 91.4%，平均比基线方法高 8.2%。

❌ Our groundbreaking algorithm achieves remarkable performance across diverse benchmarks.
✅ Our algorithm achieves 95.6% accuracy on Dataset A, 93.1% on Dataset B, and 91.4% on Dataset C, outperforming the strongest baseline by 8.2% on average.
```

---

### 3. 模糊归因（Vague Attribution）

不给出处的引用等于没说。

**中文禁用表达**：

| 禁用表达 | 替换方式 |
|---------|---------|
| 专家认为… | 给出具体引用 [Author, Year] 或删除 |
| 行业报告显示… | 给出具体报告名称和发布机构 |
| 研究表明… | 给出具体文献引用 |
| 据报道… | 谁报道的？给出来源 |
| 众所周知… | 要么给引用，要么删除此句 |

**英文禁用表达**：

| 禁用表达 | 替换方式 |
|---------|---------|
| It is well known that | 给引用或删除 |
| Experts suggest that | 给具体引用 |
| Studies have shown that | 给具体文献 |
| It has been reported that | 给来源 |

```
❌ 研究表明，深度学习在图像识别领域取得了显著进展。
✅ 在 ImageNet 分类任务上，ResNet[1] 的 Top-5 错误率已降至 3.57%，ViT[2] 进一步降至 2.1%。

❌ It is well known that machine learning models require large datasets.
✅ Brown et al. (2020) demonstrated that GPT-3's performance scales logarithmically with dataset size up to 300B tokens.
```

---

### 4. 带有「了/着」结尾的肤浅分析（Shallow Analysis with -ing / 了/着 Patterns）

这类表达后面往往跟着空洞的内容。

**中文禁用表达**：

| 禁用表达 | 问题 | 替换方式 |
|---------|------|---------|
| 突显了… | 后面通常没有具体内容 | 直接说结论 |
| 反映了… | 同上 | 直接说结论 |
| 展示了… | 同上 | 后面必须跟具体数据 |
| 说明了… | 同上 | 后面必须跟具体数据 |
| 体现了… | 同上 | 直接说明特征 |

**英文禁用表达**：

| 禁用表达 | 替换方式 |
|---------|---------|
| highlighting the importance of | 直接说结论 |
| reflecting the complexity of | 直接说结论 |
| demonstrating the effectiveness of | 后面必须跟具体数据 |
| showcasing the potential of | 删除或用数据替代 |

规则：如果用了这些词，后面必须紧跟具体数据或删掉整句。

```
❌ 图 3 展示了不同参数下模型性能的变化情况。
✅ 图 3 显示，当 λ 从 0.01 增至 0.1 时，F1 分数从 0.87 升至 0.92；继续增大至 1.0 时 F1 降至 0.85，表明过强的正则化损害了模型拟合能力。

❌ Figure 3 demonstrates the effectiveness of our approach across different parameter settings.
✅ Figure 3 shows that F1 increases from 0.87 to 0.92 as λ grows from 0.01 to 0.1, then drops to 0.85 at λ=1.0, indicating that excessive regularization impairs model fitting.
```

---

### 5. 公式化的「挑战与展望」（Formulaic "Challenges and Outlook"）

AI 生成的文章结尾千篇一律。

**中文禁用套路**：

| 禁用套路 | 替换方式 |
|---------|---------|
| 尽管取得了一定的成果，但仍存在一些不足，未来将进一步研究… | 指出具体的局限性（附边界条件）和具体的扩展方向 |
| 本文的研究还存在诸多不足，期待未来能够进一步完善 | 列 1-2 个具体可操作的改进方向 |
| 相信随着技术的不断发展，… | 删除 |
| 前景广阔 | 删除 |

**英文禁用套路**：

| 禁用套路 | 替换方式 |
|---------|---------|
| Despite promising results, further research is needed... | 指出具体局限和可操作的改进方向 |
| Future work will explore... | 给出具体扩展方向 |
| We believe this field will continue to grow... | 删除 |
| valuable insights / promising direction / fruitful area | 删除，用具体贡献替代 |

```
❌ 尽管本文取得了一定成果，但仍存在一些不足。未来将进一步研究更复杂的场景，相信随着技术的发展，该领域将取得更大突破。

✅ 本文模型的局限在于假设作物价格固定（实际价格波动 ±15%）。后续可将价格设为随机变量，在鲁棒优化框架下求解。此外，当前只考虑了单一作物轮作，多作物协同优化值得进一步探索。

❌ In conclusion, our model demonstrates superior performance and provides valuable insights for future research in this field.

✅ Our model improves F1 by 8.2% over the strongest baseline, primarily because Focal Loss prevents easy negatives from dominating the gradient. The main limitation is that this gain shrinks to 2.1% when training data falls below 1,000 samples (see Section 5.2).
```

规则：最后一段必须包含至少一个具体数字 + 一个具体局限。禁止以「valuable insights」「promising direction」「fruitful area for future work」结尾。

---

### 6. 过度使用的 AI 词汇（Overused AI Vocabulary）

以下词汇在 AI 生成文本中出现频率远高于人类写作。

**中文过度使用词**：

| 过度使用词 | 建议频率 | 替代词 |
|-----------|---------|--------|
| 此外 | 全文 ≤2 次 | 同时、另外、另一方面 |
| 深入探讨 | 全文 0 次 | 分析、讨论 |
| 增强 | 尽量不用 | 提高、提升（跟具体数字） |
| 显著地 | 只有 p<0.05 时才用 | 删除或用数字 |
| 关键的 | 全文 ≤1 次 | 删除或具体描述 |
| 重要的是 | 全文 0 次 | 值得注意的是（也只偶尔用） |
| 不可忽视的 | 全文 0 次 | 直接用数据说明其影响 |
| 高度复杂的 | 全文 0 次 | 描述具体复杂在哪里 |
| 核心的 | 全文 ≤1 次 | 删除或具体描述 |
| 与…保持一致 | 全文 ≤1 次 | 直接说一致或不一致 |

**英文过度使用词**：

| 过度使用词 | 建议频率 | 替代词 |
|-----------|---------|--------|
| moreover | 全文 0-1 次 | also, in addition（或直接不加连接词） |
| furthermore | 全文 0-1 次 | also, additionally |
| notably | 全文 0 次 | 删除或用数据说明 |
| crucially | 全文 0 次 | 同上 |
| intriguingly | 全文 0 次 | 如果真有趣，用数据让读者自己觉得有趣 |
| undoubtedly | 全文 0 次 | 删除 |
| significantly | 只有统计显著时才用 | with a statistically significant difference (p<0.05) |

---

### 7. 「三法则」的过度使用（Overuse of the "Rule of Three"）

AI 喜欢强行把一切分成三组。

**中文禁用模式**：

| 禁用模式 | 替换方式 |
|---------|---------|
| 原因有三：… | 有几个原因就写几个 |
| 从三个方面来看：… | 除非真的是恰好三个方面 |
| 主要分为三类/三种/三大… | 用编号列表而非「三」 |
| 不仅…而且… | 极少使用，这是 AI 的标志性句式 |

**英文禁用模式**：

| 禁用模式 | 替换方式 |
|---------|---------|
| Not only... but also... | 拆成两句，或用 In addition to X, Y also... |
| Three factors contribute to... | 有几个因素就写几个 |
| On the one hand... On the other hand... | 只在真正有对立时用 |
| First and foremost | 直接用 First |

```
❌ 选择 XGBoost 的原因有三：首先，它具有较高的预测精度；其次，它对缺失值不敏感；第三，它能够处理非线性关系。

✅ 选择 XGBoost 的理由：(1) 在 12 个对比算法中预测精度最高（RMSE=0.23），(2) 无需缺失值填充即可直接处理本数据集中 8% 的缺失字段，(3) 树模型对特征量纲不敏感，省去了标准化步骤。
```

---

### 8. 优雅变体 / 同义词循环（Elegant Variation / Synonym Cycling）

AI 为避免用词重复会不断替换同义词，但这在学术写作中反而造成混淆。

**中文问题模式**：

| 问题模式 | 正确做法 |
|---------|---------|
| 在「模型」「算法」「方法」「方案」「框架」之间不停切换 | 一个概念用一个词到底 |
| 前文说「XGBoost 模型」，后文变成「XGBoost 算法」再变成「XGBoost 方法」 | 固定为「XGBoost 模型」 |
| 「预测精度」「预测准确率」「预测正确率」混用 | 从符号说明表中选一个并坚持用 |

**英文问题模式**：

| 问题模式 | 正确做法 |
|---------|---------|
| switching between "model", "approach", "framework", "method", "technique" | stick to one term |
| "prediction accuracy" / "predictive accuracy" / "forecasting precision" | choose one and use consistently |

原则：同一个概念用同一个词。准确比优雅重要。

---

## 二、英文特有的 AI 味问题

> 以下针对美赛英文论文。英文 AI 生成文本有不同于中文的痕迹特征。

### 英文 AI 句式特征

| AI 特征 | 问题 | 修复 |
|---------|------|------|
| It is... that... 强调句过度 | "It is important to note that..." "It is clear that..." | 删除强调结构，直接说 |
| In conclusion, it can be seen that... | 公式化结尾 | 直接总结贡献，不要「可以看见」 |
| It should be emphasized that | 空洞前缀 | 直接说 |

### 英文标点 AI 痕迹

| 问题 | 表现 | 修复 |
|------|------|------|
| 过度使用 em dash（—） | 英文 AI 特别爱用 em dash 做插入语——每段 2-3 个 | 全文 em dash ≤ 2 个。用逗号、括号或拆句替代 |
| 分号连锁 | "the model is robust; moreover, it is efficient; furthermore, it is scalable" | 拆成三句，或改成并列结构 |
| 冒号列表泛滥 | "Three factors were identified: A, B, and C." 然后后面又跟一个冒号列表 | 列表用一次即可，不要嵌套 |

---

## 三、注入真实感（Injecting Authenticity）

除了去除 AI 味，还需要主动注入「人味」。

### 对结果做出反应

```
❌ 当 λ=0.1 时模型性能下降。
✅ 意外的是，当 λ=0.1 时模型性能反而下降——我们原本预期更强的正则化会在小样本设定下提升泛化能力，但实验结果表明它导致了欠拟合。
```

### 承认局限性的正确姿势

不要说放之四海皆准的万能局限，要说**本次建模具体选择**带来的局限：

```
❌ 数据量有限，可能影响模型性能。
✅ 本文的训练数据仅覆盖 2018-2023 年，未包含 2024 年极端气候事件。在气候异常年份，模型的预测精度可能下降——这一点在灵敏度分析的 ±30% 扰动测试中已有体现（RMSE 从 0.23 升至 0.41）。
```

### 解释「为什么」而不仅是「是什么」

```
❌ 从图 4 可以看出，GA 在迭代 50 次后收敛。
✅ 图 4 显示 GA 在迭代 50 次后收敛。快速收敛的原因在于初始化阶段用了贪心算法生成了较高质量的初始种群，使搜索从接近最优解的区域开始。
```

---

## 四、数学建模论文特有注意事项

### 模型描述类禁用词

| 禁用 | 替换 |
|------|------|
| 深入探讨了… | 分析了… |
| 充分展示了… | 结果显示… |
| 具有重要意义 | （用具体数字替代） |
| 结果令人振奋 | （直接写结果数据） |
| 取得了良好的效果 | 在测试集 A/B/C 上准确率分别为… |
| 该模型表现出色 | 该模型在 XX 指标上达到 0.XX |
| 达到了较高水平 | 达到 95.6%，比基线高 8.2% |
| 性能优越 | 在 6 项指标中的 5 项上优于对比方法 |

### 结果描述铁律

每句话至少包含以下三者之一：
1. 一个具体数字
2. 一个具体对比
3. 一个因果解释

```
❌ 模型在测试集上表现良好。                    （三者全无）
❌ 模型的准确率较高。                          （有比较词但无数字）
✅ 模型的准确率达到 95.6%，比逻辑回归高 8.2%。 （有数字 + 有对比）
✅ 模型在长尾类别上的提升尤为明显（+12.3%），因为 Focal Loss 降低了易分样本的权重。
                                              （有数字 + 有因果解释）
```

### 人称约束

| 禁止使用 | 应使用 |
|---------|--------|
| 本研究 | 本文、该研究 |
| 本论文 | 本文 |
| 我们 | （省略主语） |
| 笔者 | 本文 |
| 我们的 | 该、本文提出的 |

### 叙述方式规范

避免过度分点，多使用整段叙述。分点仅用于：模型假设（5-8条）、符号说明（表格）、算法步骤（3-5步）、模型优缺点。

---

## 五、快速自检清单

论文写完后，逐条检查：

### 中文自检

- [ ] 是否出现了「标志着」「重要的」「关键作用」等过度强调词？
- [ ] 是否有「不仅…而且…」的平行结构？
- [ ] 是否有「专家认为」「研究表明」（且没给引用）？
- [ ] 是否强行将内容分成三组（「原因有三」「三个方面」）？
- [ ] 是否出现了「突破性的」「令人震撼的」等广告词？
- [ ] 是否过度使用破折号（——）？
- [ ] 是否在「模型/算法/方法/方案」之间来回切换？
- [ ] 是否有公式化的「挑战与展望」段落？
- [ ] 每个「展示了/反映了/突显了」后面是否跟了具体数据？
- [ ] 每句话是否至少有数字、对比或因果解释之一？
- [ ] 「此外」是否出现了超过 2 次？
- [ ] 结论是否用万能句子？是否有本文具体建模选择带来的局限？

### 英文自检（美赛专用）

- [ ] `moreover` 和 `furthermore` 加起来 ≤ 2 次？
- [ ] 没有 `notably` / `crucially` / `intriguingly` / `remarkably`？
- [ ] 全文 em dash（—）≤ 2 个？
- [ ] 有没有 `Not only... but also...`？
- [ ] 有没有 `shed light on` / `pave the way for` / `plays a crucial role`？
- [ ] 结尾段是否有具体数字 + 具体局限？（而非 generic future work）
- [ ] 动词强度与证据强度匹配（show/demonstrate vs suggest/may）？
- [ ] Related Work 按主题综合法而非逐篇罗列？