---
name: style-calibration
description: "写作风格校准：从用户过往作品学习写作风格，使生成的论文更符合用户习惯。参考 academic-research-skills 设计。"
---

# 写作风格校准（Style Calibration）

> **版本**: v1.1 | **更新**: 2026-07-26
> **来源**: 参考 Imbad0202/academic-research-skills 设计

---

## 设计理念

写作风格校准用于学习用户的写作风格，使生成的论文更符合用户习惯。本skill提供：
- 风格分析（脚本，离线可计量指标）
- 风格画像构建（脚本，输出 style_profile.json）
- 风格偏差检测与修改建议（脚本）+ 按建议改写（agent 执行）

> **诚实说明**：脚本层只做可离线计量的统计（句长/段落/标点/开头词/连接词/中英混排/成语密度）与偏差检测；按建议实际改写文本属于语义级操作，由 agent 在会话中执行，脚本不自动改写。

---

## 流程图

```
用户过往作品
    ↓
风格分析（analyze_style.py）
    ↓
风格画像 style_profile.json
    ↓
草稿偏差检测（apply_style.py）→ 偏差报告 + 建议清单
    ↓
agent 按建议改写新论文
```

---

## 1. 风格分析

### 1.1 句式分析

```python
def analyze_sentence_patterns(text: str) -> dict:
    """
    分析句式模式

    参数:
        text: 输入文本

    返回:
        句式模式统计
    """
    import re

    # 统计句子长度
    sentences = re.split(r'[。！？]', text)
    sentence_lengths = [len(s) for s in sentences if s.strip()]

    # 统计句式类型
    patterns = {
        "简单句": 0,
        "复合句": 0,
        "并列句": 0
    }

    for sentence in sentences:
        if not sentence.strip():
            continue
        if "，" in sentence and "。" in sentence:
            patterns["复合句"] += 1
        elif "；" in sentence:
            patterns["并列句"] += 1
        else:
            patterns["简单句"] += 1

    return {
        "平均句长": sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
        "句式分布": patterns,
        "句子数量": len(sentence_lengths)
    }
```

### 1.2 词汇分析

```python
def analyze_vocabulary(text: str) -> dict:
    """
    分析词汇特征

    参数:
        text: 输入文本

    返回:
        词汇特征统计
    """
    import jieba
    import collections

    # 分词
    words = jieba.lcut(text)

    # 统计词频
    word_freq = collections.Counter(words)

    # 统计词汇多样性
    unique_words = len(word_freq)
    total_words = len(words)
    vocabulary_diversity = unique_words / total_words if total_words > 0 else 0

    # 统计高频词
    top_words = word_freq.most_common(20)

    return {
        "总词数": total_words,
        "独特词数": unique_words,
        "词汇多样性": vocabulary_diversity,
        "高频词": top_words
    }
```

---

## 2. 风格学习

### 2.1 风格特征提取

```python
def extract_style_features(text: str) -> dict:
    """
    提取风格特征

    参数:
        text: 输入文本

    返回:
        风格特征向量
    """
    # 句式分析
    sentence_patterns = analyze_sentence_patterns(text)

    # 词汇分析
    vocabulary = analyze_vocabulary(text)

    # 提取特征
    features = {
        "平均句长": sentence_patterns["平均句长"],
        "词汇多样性": vocabulary["词汇多样性"],
        "复合句比例": sentence_patterns["句式分布"]["复合句"] / sentence_patterns["句子数量"],
        "并列句比例": sentence_patterns["句式分布"]["并列句"] / sentence_patterns["句子数量"],
        "简单句比例": sentence_patterns["句式分布"]["简单句"] / sentence_patterns["句子数量"]
    }

    return features
```

### 2.2 风格模型构建

```python
def build_style_model(texts: list) -> dict:
    """
    构建风格模型

    参数:
        texts: 用户过往作品列表

    返回:
        风格模型
    """
    # 提取所有作品的风格特征
    all_features = []
    for text in texts:
        features = extract_style_features(text)
        all_features.append(features)

    # 计算平均风格
    avg_style = {}
    for key in all_features[0].keys():
        values = [f[key] for f in all_features]
        avg_style[key] = sum(values) / len(values)

    return {
        "平均风格": avg_style,
        "作品数量": len(texts),
        "风格特征": all_features
    }
```

---

## 3. 风格应用

### 3.1 风格偏差检测与调整建议

> 注意：本环节脚本产出的是"偏差检测 + 修改建议清单"，**不直接改写文本**；实际改写由 agent 按建议执行。

```python
def apply_style(text: str, style_model: dict) -> dict:
    """
    对比文本与风格模型，产出偏差与调整建议

    参数:
        text: 输入文本
        style_model: 风格模型

    返回:
        当前风格、目标风格与调整建议（不改写文本）
    """
    # 获取目标风格
    target_style = style_model["平均风格"]

    # 分析当前文本风格
    current_style = extract_style_features(text)

    # 调整建议
    suggestions = []

    if current_style["平均句长"] < target_style["平均句长"] * 0.8:
        suggestions.append("建议增加句子长度，使用更复杂的句式")
    elif current_style["平均句长"] > target_style["平均句长"] * 1.2:
        suggestions.append("建议缩短句子长度，使表达更简洁")

    if current_style["词汇多样性"] < target_style["词汇多样性"] * 0.8:
        suggestions.append("建议增加词汇多样性，避免重复用词")

    return {
        "当前风格": current_style,
        "目标风格": target_style,
        "调整建议": suggestions
    }
```

---

## 使用方式

```bash
# 1) 分析用户风格：--samples 支持多个文件或目录（目录递归收集 .txt/.md）
python .claude/skills/style-calibration/scripts/analyze_style.py \
  --samples user_papers/ \
  --output paper_output/qa/style_profile.json

# 2) 对照画像检查草稿：逐段输出偏差报告 + 修改建议清单（脚本不自动改写）
python .claude/skills/style-calibration/scripts/apply_style.py \
  --profile paper_output/qa/style_profile.json \
  --draft paper_output/final_paper_source.md \
  --output paper_output/qa/style_deviation_report.json
```

> 兼容别名：`--input` 等价于 `--samples`；`--style` 等价于 `--profile`；`--paper` 等价于 `--draft`。
> 两个脚本仅依赖 Python 标准库，可完全离线运行。拿到偏差报告后，由 agent 按 `paragraph_findings` 中的建议逐段改写。

---

## 输出格式

### style_profile.json（analyze_style.py 产出）

```json
{
  "tool": "analyze_style.py v1.1",
  "samples": [{"path": "user_papers/a.md", "chars": 1200, "sentences": 45}],
  "metrics": {
    "sentence_length": {"mean": 25.5, "median": 22.0, "p90": 48.0},
    "paragraph": {"mean_chars": 120.5, "median_chars": 98.0, "mean_sentences": 4.2},
    "punctuation_per_1000": {"逗号": 33.1, "顿号": 4.1, "分号": 5.5, "冒号": 2.8, "破折号": 1.4, "括号": 2.1, "问号": 0.7},
    "starters_top": [["因此", 6, 0.08], ["本文", 4, 0.05]],
    "connective_per_1000": 20.7,
    "connectives_top": [["因此", 6], ["然而", 4]],
    "english_ratio": 0.02,
    "digit_ratio": 0.01,
    "idiom_per_1000": 3.4,
    "idioms_found": [["相辅相成", 2]]
  },
  "note": "所有指标均为离线可计量统计；成语密度基于内置常用成语表，为近似值。"
}
```

### style_deviation_report.json（apply_style.py 产出）

```json
{
  "note": "本报告为偏差检测与修改建议清单；脚本不自动改写文本，实际改写由 agent 按建议执行。",
  "summary": {
    "consistency_score": 62,
    "paragraphs_total": 18,
    "paragraphs_checked": 15,
    "paragraphs_flagged": 5,
    "document_issue_count": 2
  },
  "document_issues": [
    {"metric": "英文占比", "draft": 0.21, "profile": 0.02,
     "suggestion": "全文英文字符占比 21.0%，高于画像 2.0%：核对术语中英文写法是否与既往作品一致"}
  ],
  "paragraph_findings": [
    {"paragraph_index": 3, "preview": "本节我们……",
     "issues": [
       {"metric": "平均句长", "draft": 78.0, "profile": 25.5,
        "suggestion": "本段平均句长 78.0 字，高于画像均值 25.5 字（P90=48.0）：建议把超过 48.0 字的长句拆成 2-3 句"},
       {"metric": "句首重复", "draft": "「模型」×4", "profile": "-",
        "suggestion": "本段有 4 个句子以「模型」开头：建议变换句首表达"}
     ]}
  ]
}
```

---

## 版本历史

- v1.1.0 (2026-07-26): 落地 `scripts/analyze_style.py` 与 `scripts/apply_style.py`（纯标准库、离线可跑，含冒烟验证）；明确脚本只做偏差检测+建议清单，实际改写由 agent 执行；CLI 统一为 `--samples` / `--profile` / `--draft`（保留 `--input` / `--style` / `--paper` 兼容别名）
- v1.0.0 (2026-06-21): 初始版本，参考 Imbad0202/academic-research-skills 设计