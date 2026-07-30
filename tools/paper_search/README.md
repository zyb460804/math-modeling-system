# 论文检索工具（Paper Search）

> **版本**: v1.0 | **更新**: 2026-06-21
> **用途**: 搜索、下载、提取学术论文

---

## 工具清单

### 1. search_papers.py - 搜索学术论文

**功能**: 从多个学术搜索引擎搜索论文

**数据源**:
- Google Scholar
- Semantic Scholar
- arXiv
- PubMed
- CrossRef

**用法**:
```bash
python tools/paper_search/scripts/search_papers.py \
  --query "mathematical modeling optimization" \
  --source semantic_scholar \
  --limit 10 \
  --output paper_output/refs/search_results.json
```

**参数**:
- `--query`: 搜索关键词
- `--source`: 数据源（google_scholar, semantic_scholar, arxiv, pubmed, crossref）
- `--limit`: 返回结果数量
- `--output`: 输出文件路径

**输出格式**:
```json
{
  "query": "mathematical modeling optimization",
  "source": "semantic_scholar",
  "total_results": 150,
  "papers": [
    {
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "year": 2024,
      "abstract": "...",
      "url": "https://...",
      "doi": "10.xxx/xxx",
      "citation_count": 50
    }
  ]
}
```

### 2. download_paper.py - 下载论文PDF

**功能**: 下载论文PDF到本地

**用法**:
```bash
python tools/paper_search/scripts/download_paper.py \
  --url "https://arxiv.org/pdf/xxxx.xxxxx" \
  --output paper_output/refs/papers/
```

**参数**:
- `--url`: 论文URL
- `--output`: 输出目录

### 3. extract_references.py - 提取参考文献

**功能**: 从论文PDF中提取参考文献列表

**用法**:
```bash
python tools/paper_search/scripts/extract_references.py \
  --input paper_output/refs/papers/paper.pdf \
  --output paper_output/refs/references.json
```

**输出格式**:
```json
{
  "paper": "paper.pdf",
  "references": [
    {
      "id": 1,
      "authors": ["Author 1", "Author 2"],
      "title": "Reference Title",
      "year": 2023,
      "journal": "Journal Name",
      "doi": "10.xxx/xxx"
    }
  ]
}
```

---

## 集成到工作流

### 在选题阶段使用

```bash
# 搜索相关论文
python tools/paper_search/scripts/search_papers.py \
  --query "TOPSIS evaluation model" \
  --source semantic_scholar \
  --limit 5

# 下载关键论文
python tools/paper_search/scripts/download_paper.py \
  --url "..." \
  --output paper_output/refs/papers/
```

### 在写作阶段使用

```bash
# 提取参考文献
python tools/paper_search/scripts/extract_references.py \
  --input paper_output/refs/papers/key_paper.pdf \
  --output paper_output/refs/references.json
```

---

## 依赖

```bash
pip install requests beautifulsoup4 scholarly semanticscholar
```

---

## 版本历史

- v1.0.0 (2026-06-21): 初始版本
