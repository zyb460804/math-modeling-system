# 多源文献检索协议

> **来源**：从 `nature-academic-search`（已归档）抽取核心方法论，整合进 authoritative-data-harvester。
> **用途**：竞赛期间需要补充文献/数据来源时的多源检索指南。
> **配合**：`authoritative-data-harvester` skill + `tools/paper_search/scripts/search_papers.py`。

---

## 何时用多源检索

| 场景 | 是否需要 |
|------|---------|
| 国赛/五一赛（中文，72h） | 通常不需要（题目给的数据够用） |
| 美赛 MCM/ICM（英文，96h） | **需要**（补充背景文献 + 方法支撑） |
| MathorCup（中文，72h） | 按需（C 题大数据类可能需要） |
| 赛前备战（学习优秀论文） | **需要**（大规模文献调研） |

---

## 多源检索优先级

按**可信度**和**相关性**排序：

| 优先级 | 源 | 工具/MCP | 最适合 |
|--------|---|---------|-------|
| 1 | **Semantic Scholar** | `search_semantic_scholar` | 引用图谱、领域过滤、竞赛论文最常用 |
| 2 | **CrossRef** | `search_crossref` | 跨学科、引用计数验证 |
| 3 | **arXiv** | `search_arxiv` | 预印本（数学/CS/物理/统计方法最新进展） |
| 4 | **Google Scholar** | `search_google_scholar` | 广泛搜索（爬取，质量参差） |
| 5 | **知网/CNKI** | 手动/第三方 | **中文文献必须**（国赛/五一赛） |

### 按题型的源选择

| 题型 | 优先源 | 理由 |
|------|--------|------|
| A 题（物理/几何） | arXiv（数学/物理）+ 知网 | 机理推导需要最新方法 |
| B 题（优化） | Semantic Scholar + arXiv（CS/Optimization） | 启发式算法/元启发式最新进展 |
| C 题（数据/评价） | 知网 + Semantic Scholar | 中文评价方法（TOPSIS/熵权）文献在知网 |
| D 题（统计/预测） | arXiv（stat.ML）+ Semantic Scholar | 时序预测/ML 最新方法 |

---

## 检索工作流（4 步）

### Step 1: 关键词构建

从题目提取**核心概念词**，扩展为搜索查询：

```
题目：基于多源数据的电力系统负荷预测
        │
        ▼
核心概念：负荷预测 / 多源数据 / 电力系统
        │
        ▼
英文查询（用于 Semantic Scholar/arXiv）：
  - "load forecasting" + "multi-source data"
  - "power system" + "short-term load forecasting"
  - "electricity demand prediction" + "machine learning"

中文查询（用于知网）：
  - "电力负荷预测" + "多源数据"
  - "短期负荷预测" + "深度学习"
```

**技巧**：
- 同义词扩展（load forecasting = demand prediction = consumption forecasting）
- 限定时间范围（近 5 年优先）
- 先广泛搜索再缩小

### Step 2: 多源并行检索

```bash
# 使用项目已有的搜索脚本
python tools/paper_search/scripts/search_papers.py \
  --query "load forecasting multi-source" \
  --source semantic_scholar \
  --limit 10

python tools/paper_search/scripts/search_papers.py \
  --query "load forecasting multi-source" \
  --source arxiv \
  --limit 10
```

### Step 3: 相关性筛选

对每条结果，按以下标准筛选：

| 标准 | 权重 |
|------|------|
| 标题相关性 | 高 |
| 摘要相关性 | 高 |
| 引用数 | 中（高引用=经典，但可能旧） |
| 发表时间 | 中（近 3 年优先） |
| 期刊/会议级别 | 中（顶会/顶刊优先） |

**保留规则**：筛选后保留 **5-10 篇核心文献**，不要贪多。

### Step 4: 引用格式转换

将筛选后的文献转换为统一格式：

```bash
# 导出为 BibTeX（LaTeX 用）
python tools/paper_search/scripts/search_papers.py \
  --query "..." \
  --export-format bibtex \
  --output paper_output/references.bib

# 导出为 .ris（EndNote/Zotero 用）
python tools/paper_search/scripts/search_papers.py \
  --query "..." \
  --export-format ris \
  --output paper_output/references.ris
```

---

## 引用真实性核验（关键！）

> **铁律**：不得编造引用。每条引用必须能在数据库中查到真实文献。

### 核验清单

对每条准备引用的文献：

| 检查项 | 方法 |
|--------|------|
| DOI 有效 | 在 doi.org 检查 |
| 标题匹配 | 搜索标题，确认论文存在 |
| 作者匹配 | 确认作者是论文真实作者 |
| 年份匹配 | 确认发表年份 |
| 内容支撑 | **读了摘要**确认论文确实支撑你的声明 |

### 引用分级（来自 nature-citation 方法论）

| 级别 | 含义 | 能否引用 |
|------|------|---------|
| **强支撑** | 论文直接证明你的声明 | ✅ 直接引用 |
| **部分支撑** | 论文证明部分声明，需补充其他引用 | ✅ 组合引用 |
| **背景支撑** | 论文提供背景，不直接证明声明 | ⚠️ 只能用于引言背景 |
| **不建议引用** | 标题相关但内容不支撑 | ❌ 不引用 |

---

## 与其他 skill 的关系

| skill | 关系 |
|-------|------|
| `authoritative-data-harvester` | 本文档是其子能力（文献检索） |
| `citation-tracer` | 引用真实性核验（本文档的 Step 4 对接它） |
| `award-paper-rag` | 优秀论文检索（竞赛论文，非学术文献） |
| `bilingual-reader-protocol`（award-paper-rag/references/） | 检索到文献后的精读协议 |

---

## 禁止行为

- ❌ 编造引用（"Smith et al., 2023" 但这篇论文不存在）
- ❌ 不读摘要就引用（标题相关≠内容支撑）
- ❌ 引用二次来源（应引原始论文 A，而非引述 A 的综述 B）
- ❌ 把背景支撑的文献当成强支撑引用
- ❌ 搜索后不导出到 `paper_output/references.bib`（写论文时找不到）