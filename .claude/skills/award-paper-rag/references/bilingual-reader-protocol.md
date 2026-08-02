# 中英对照论文精读协议

> **来源**：从 `nature-reader`（已归档）抽取核心方法论，适配 award-paper-rag 场景。
> **用途**：从 RAG 检索到优秀论文段落后，做**精读**（非摘要），保留原文锚点与图表位置。
> **配合**：`award-paper-rag` skill 的 `mmqa retrieve` 命令（检索）→ 本协议（精读）。

---

## 核心原则

> "精读不是摘要。摘要丢失原文的论证细节和图表上下文。"

当 RAG 返回相关段落后，默认产出**段落级中英对照精读文档**，不是总结。

---

## 精读产物结构

对每篇检索到的优秀论文，产出 4 个文件：

```
paper_output/research/<paper_id>/
├── paper.md              ← 中英对照精读主文档
├── source_map.json       ← 源锚点映射（每段→原 PDF 页码/位置）
├── translation_notes.md  ← 翻译难点与术语决策
└── assets/               ← 提取的图表（就地放置）
```

---

## paper.md 的写法

### 段落级对照（非全文翻译）

每个原文段落用以下格式：

```markdown
### 3.2 Model Formulation

> **原文**（Source: p.5, §3.2）
>
> We formulate the problem as a mixed-integer linear program (MILP) to minimize total transportation cost subject to capacity constraints...

**中文精读**：

作者将问题建模为混合整数线性规划（MILP），目标是最小化总运输成本，约束条件包括容量限制...

**方法论提取**：
- 建模选择：MILP（非 LP/非线性）
- 目标：总成本最小化
- 核心约束：容量

**可复用到我们的论文**：
- 如果我们的题目也是运输/分配类，这个 MILP 框架可以直接复用
- 注意：作者没有考虑时间窗约束，我们需要扩展
```

### 图表就地放置

图表**不能全堆到末尾**，必须放在第一次提到它的段落后面：

```markdown
> The results show a clear Pareto frontier (Figure 3).

**中文精读**：结果呈现了清晰的帕累托前沿（图 3）。

![Figure 3: Pareto frontier of the bi-objective optimization](assets/fig3_pareto.png)
*Figure 3: 双目标优化的帕累托前沿。X 轴为成本，Y 轴为时间。*

**分析**：这个前沿图说明...
```

---

## source_map.json 的写法

保留每个精读块到原文的精确映射，便于回溯：

```json
{
  "paper_id": "2023_D_O_001",
  "source_pdf": "resources/02_优秀论文/MCM_ICM_O奖/2023_D_001.pdf",
  "blocks": [
    {
      "block_id": "b_003_002",
      "page": 5,
      "section": "3.2 Model Formulation",
      "char_range": [1200, 1450],
      "original_text_hash": "sha256:abc123...",
      "translation_status": "complete",
      "method_extracted": "MILP formulation"
    }
  ]
}
```

**用途**：
- 写论文引用时，可以精确定位到原文页码
- 防止"AI 编造引用"（哈希校验）
- 可追溯"这个方法是从哪篇论文的哪一段学来的"

---

## translation_notes.md 的写法

记录翻译中的难点和术语决策：

```markdown
## 术语决策

| 英文 | 中文 | 决策理由 |
|------|------|---------|
| Pareto frontier | 帕累托前沿 | 国赛标准译法，不用"帕累托边界" |
| Heuristic | 启发式 | 不用"试探式"或"经验式" |
| Robustness | 稳健性 | 国赛评分量表用"稳健性"，不用"鲁棒性" |

## 翻译难点

### 难点 1：p.7 "the model scales favorably"
- 字面：模型扩展性良好
- 上下文：作者讨论数据量增大时的性能
- 决策译法："模型在大规模数据下仍保持良好性能"
```

---

## 与 award-paper-rag 的衔接

```
award-paper-rag mmqa retrieve "2023 D题 双目标优化"
        │
        ▼ （返回相关段落）
        
本协议：中英对照精读
  ├─ paper.md（精读主文档）
  ├─ source_map.json（锚点）
  ├─ translation_notes.md（术语）
  └─ assets/（图表）
        │
        ▼
        
写论文时引用：
  "参考 2023 D 题 O 奖论文的方法（paper.md §3.2），我们扩展了..."
```

---

## 什么时候用精读 vs 什么时候用摘要

| 场景 | 用什么 |
|------|--------|
| 学习优秀论文的建模方法 | **精读**（本协议） |
| 快速了解 100 篇论文的整体趋势 | 摘要（RAG 直接返回） |
| 写论文时引用具体方法 | **精读**（需要精确页码和术语） |
| 答辩准备"我们参考了哪些论文" | 摘要 + 精读混合 |

---

## 禁止行为

- ❌ 把精读降级为 3 句话摘要
- ❌ 图表全堆到文档末尾（失去上下文）
- ❌ 丢失原文页码/位置锚点
- ❌ 术语翻译前后不一致
- ❌ 编造原文中没有的方法或数据