# HMML 选模算法指南 — MethodScorer 自顶向下打分检索

> 来源：`MMAgent/agent/retrieve_method.py`（usail-hkust/LLM-MM-Agent, NeurIPS 2025）
> 落地版本：v4.6 融合 · 仅文档，不改流水线代码

---

## 1. HMML 三层结构总览

HMML.json 是一棵不规则多叉树。顶层 5 个 Domain，每个 Domain 下挂 Level-2 节点（Subdomain 或 Category），Level-2 节点的 Children 即为 Method 叶子（或再嵌套一层 Category 后挂 Method 叶子）。

| Domain | Level-2 节点（Subdomain / Category） | Method 叶子数 |
|--------|--------------------------------------|---------------|
| **Operations Research**（运筹学） | Programming Theory · Graph Theory · Stochastic Programming Theory | 25 |
| **Optimization Methods**（优化方法） | Deterministic Algorithms · Heuristic Algorithm · Iterative Algorithm · Constrained Optimization · Solving Techniques | 23 |
| **Machine Learning**（机器学习） | Classification · Clustering · Regression · Dimensionality Reduction · Ensemble Learning Algorithms | 22 |
| **Prediction**（预测） | Discrete Prediction · Continuous Prediction | 12 |
| **Evaluation Methods**（评价方法） | Scoring Evaluation · Statistical Evaluation · Goodness of Fit Test | 15 |
| **合计** | **18** | **97** |

> 关键区分：Level-2 节点中，Children 的第一个元素含 `method_class` 字段的为 **Subdomain**（需继续下钻），否则为 **Category**（其 Children 即 Method 叶子）。部分 Subdomain（如 Dimensionality Reduction、Continuous Prediction、Statistical Evaluation）会再嵌套一层 Category。

---

## 2. MethodScorer 自顶向下打分算法

### 2.1 核心思想

对树的每一层，用 `score_func` 给当前层的所有候选 Children 打分；到达 Method 叶子层时，叶子的 `final_score` 由两部分加权合成：

```
final_score = parent_path_average × parent_weight + self_score × child_weight
            = parent_path_average × 0.5   + self_score × 0.5     （默认权重）
```

- `parent_path_average`：从根到当前叶子父节点的路径上所有祖先分数的算术平均
- `self_score`：叶子自身由 score_func 给出的分数
- `parent_weight = 0.5`、`child_weight = 0.5`（源码默认值，可调）

### 2.2 伪代码

```
function MethodScorer(score_func, parent_weight=0.5, child_weight=0.5):

  function process(tree):
      leaves = []
      for root in tree:
          process_node(root, parent_scores=[])
      for root in tree:
          collect_leaves(root)        # 收集所有带 final_score 的叶子
      return leaves

  function process_node(node, parent_scores):
      if node has no children:
          return                       # 叶子（在父节点的处理中已打分）

      children = node.children
      first_child = children[0]

      if first_child has 'method_class':      # ── 中间层（Domain / Subdomain）
          # 给当前层 children 打分
          scores = score_func([
              {method: c.method_class, description: c.description} for c in children
          ])
          for i, child in enumerate(children):
              child.score = scores[i]

          # 更新祖先路径：追加当前 node 自身分数（若有）
          new_parent = copy(parent_scores)
          if node has 'score':
              new_parent.append(node.score)

          # 递归处理每个 child
          for child in children:
              process_node(child, new_parent)

      else:                                    # ── 叶子层（Children 为 Method）
          # 给 Method 叶子打分
          scores = score_func([
              {method: c.method, description: c.description} for c in children
          ])
          for i, child in enumerate(children):
              child_score = scores[i]
              parent_avg = mean(parent_scores) if parent_scores else 0
              child.final_score = parent_avg × parent_weight + child_score × child_weight

  function collect_leaves(node):
      if node has children:
          for child in node.children:
              collect_leaves(child)
      else:
          if node has 'final_score':
              leaves.append({method, description, score: final_score})
```

### 2.3 retrieve_methods 主流程

```
function retrieve_methods(problem_description, top_k=6, method='embedding'):
    if RAG enabled:
        if method == 'embedding':
            score_func = EmbeddingScorer.score_method(problem_description)
        else:
            score_func = llm_score_method(problem_description)

        scored_leaves = MethodScorer(score_func).process(hmml_tree)
        scored_leaves.sort(by score, descending)
        return scored_leaves[:top_k]          # 返回 top_k 个方法
    else:
        return full HMML markdown             # RAG 关闭时直接返回全文
```

---

## 3. 两种打分模式

| 模式 | 参数 | 实现 | 适用场景 |
|------|------|------|----------|
| **Embedding 相似** | `method='embedding'` | `EmbeddingScorer.score_method(problem_desc, methods)` → 向量余弦相似 | 快速初筛、大批量方法、无需 LLM 调用（省 token/省时间）；适合第一轮粗筛 |
| **LLM 批判** | `method='llm'`（或除 embedding 外任意值） | `llm_score_method(problem_desc, methods)` → 用 `METHOD_CRITIQUE_PROMPT` 让 LLM 对每个方法多维度打分后取均分 | 精细评估、需要语义推理判断适用性；适合 top-k 精排或 embedding 无法区分的相近方法 |

### LLM 批判的评分细节

```
function llm_score_method(problem_description, methods):
    # 1. 格式化方法列表
    methods_str = "1. {method} {description}\n2. ..."

    # 2. 构造 prompt（METHOD_CRITIQUE_PROMPT 模板）
    prompt = METHOD_CRITIQUE_PROMPT.format(problem_description, methods_str)

    # 3. LLM 生成 → 解析 JSON
    answer = llm.generate(prompt)
    method_scores = parse_json(answer)['methods']    # 每个方法多维度评分

    # 4. 每个方法的最终分 = 各维度均分
    for m in method_scores:
        m.score = mean(m.scores.values())

    return method_scores
```

LLM 批判模式对每个方法从多个维度打分（如适用性、复杂度、数据需求等），最终取维度均值作为该方法的 self_score。

---

## 4. top_k=6 取出后如何结合 problem_analysis 给出推荐

MethodScorer 输出的是按 `final_score` 降序排列的方法列表，默认取前 6 个。推荐流程：

1. **获取 top_k 方法**：`scored_leaves[:6]` → 6 个候选方法（含 method 名 + description + final_score）
2. **结合 problem_analysis 过滤**：
   - 根据 `problem_analysis.json` 中的题型、数据特征、约束条件，排除明显不适用的高分方法（如数据量太小不适合深度学习）
   - 补充 matrix 查询结果中 HMML 未覆盖的方法
3. **分组推荐**：按 Domain 分组（如"优化类候选 3 个 + 评价类候选 2 个"），给出主模型 + 辅助模型建议
4. **进入 PoC 验证**：每个候选方法生成 ≤30 行 PoC 代码（Gate G2），在真实数据上运行

---

## 5. 与本系统 analyze skill 的衔接

```
/analyze（统一审题选模入口）
  │
  ├─ Step 1: 解析输入（题型 / 数据特征 / 约束）
  │     └─ 产出 problem_analysis
  │
  ├─ Step 2: 匹配方法 ← HMML 在此介入
  │     ├─ 2a. 查 model-selection-matrix.md（场景 → 算法直查）
  │     ├─ 2b. 查 HMML（问题 → 领域 → 方法分层检索）
  │     │      ├─ 确定 Domain（运筹/优化/ML/预测/评价）
  │     │      ├─ 逐层下钻 Subdomain → Category
  │     │      ├─ （可选）用 MethodScorer 算法打分排序
  │     │      └─ 取 top_k 候选方法 + <core_idea>/<application> 描述
  │     └─ 2c. 合并去重 → 候选方法清单
  │
  ├─ Step 3: 生成候选方法（2-4 个，每个含 PoC 代码）
  ├─ Step 4: PoC 验证（Gate G2）
  └─ Step 5: 输出推荐 → Gate G2.5（用户决策）
```

**分工边界**：
- `analyze` 负责：题型判断、模型路线规划、PoC 验证、用户决策门禁
- HMML 负责：方法节点级知识提供（建模思路、核心思想、应用场景）+ 可选的分层打分检索
- `model-selection-matrix.md` 负责：场景特征 → 具体算法的精确映射 + 冲突裁决规则

三者互补：analyze 是流程编排者，matrix 是场景直查表，HMML 是方法知识树。
