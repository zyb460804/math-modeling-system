---
name: award-paper-rag
description: O 奖/优秀论文章节级 RAG 问答引擎。按 Markdown heading 分块（非固定 token），正则状态机识别 13 类章节，支持 年份/题号/章节 多维过滤，跨年趋势对比。直接检索本项目 resources/02_优秀论文/ 的 190+ 篇优秀论文，取代 competition-prep 的模糊匹配。
tools: Read, Write, Edit, Bash, Glob
---

# O 奖论文 RAG 问答引擎

> 融合自 `Kirito-Elucidator/MathModel-QA-Engine`（10★，MCM/ICM F 奖得主作品）。
> 解决 competition-prep agent 关键词匹配历史案例"噪声大、不精准"的问题。

## 触发词

`查优秀论文` `O 奖论文检索` `历年 C 题用了什么方法` `参考往年写法` `RAG 问答` `章节检索`

## 为什么章节级 RAG 优于关键词匹配

数学建模论文结构高度统一（Summary → Introduction → Assumptions → Body → Sensitivity → Conclusion）。
普通 RAG 用固定 token 切分会把一段 Sensitivity Analysis 撕成两半，混入前后章节噪声。
本引擎**按 Markdown heading 分块**，每个节点 = 一个完整章节，自带 `year/problem/section/doc_id` 元数据。

## 核心能力

| 能力 | 描述 |
|------|------|
| **章节级分块** | markdown_blocks.py 按 heading 拆分，语义完整 |
| **13 类章节分类** | sections.py 正则状态机识别 Summary/Assumptions/Model/Sensitivity 等 13 类 |
| **多维过滤** | 年份 / 题号 / 章节 / 文档 ID 任意组合 |
| **跨年趋势** | 对同一题型（如历年 C 题）横向对比方法演变 |
| **低质节点过滤** | postprocessors.py 自动过滤纯标题/目录节点 |
| **多轮对话** | ChatMemoryBuffer 上下文记忆 |
| **API 兼容** | OpenAI / DeepSeek / 智谱 等任意 OpenAI 兼容接口 |

## 脚本（scripts/，融合自 mmqa/ 包）

```
scripts/
├── rag_cli.py              # 主入口（build 构建索引 / chat 交互问答）
├── corpus_converter.py     # 语料 → md 批量转换（pdfplumber + python-docx，断点续传）
├── requirements.txt        # llamaindex 0.14 + 依赖
└── mmqa/                   # 论文预处理工具包
    ├── markdown_blocks.py  # Markdown heading 解析器
    ├── sections.py         # 13 类章节分类器（正则 + 状态机）
    ├── node_export.py      # 分块 + JSONL 导出
    ├── postprocessors.py   # DropLowInfoNodes 低质节点过滤
    ├── papers_csv.py       # 论文元数据读取
    ├── titles_csv.py       # 标题归一化
    └── __main__.py         # python -m mmqa split
```

## 数据准备

语料已在 `resources/02_优秀论文/`（190+ 篇，CUMCM/MCM-ICM）。一键转 Markdown：

```bash
# 1. 批量转换 PDF/docx → md，并从目录结构自动解析 year/problem/competition/award
python scripts/corpus_converter.py            # 全量（断点续传）
python scripts/corpus_converter.py --limit 20 # 先转 20 篇测试
#   产出 data/papers/*.md + data/papers.csv

# 2. 构建 sections 索引（heading 分块 + 13 类分类）
python -m scripts.mmqa split
```

## 使用方式

```bash
# 首次：构建向量索引（约 5-10 分钟）
python scripts/rag_cli.py build

# 离线检索（不调 LLM，完全本地）：query + 元数据过滤 + top-k
python scripts/rag_cli.py retrieve --query "灵敏度分析" --top-k 5
python scripts/rag_cli.py retrieve --query "sensitivity" --year 2019 --problem C --section Body

# 问答（需 OPENAI_API_KEY 或任意 OpenAI 兼容端点）
python scripts/rag_cli.py chat
# > 历年 C 题 E 题的灵敏度分析一般怎么写？
# > 2023-2025 年 CUMCM A 题用了哪些优化方法？跨年趋势？
```

### 离线模式（无需 API key）

- `build` 和 `retrieve` **完全离线**：自动用 HuggingFace 本地 embedding（多语言 paraphrase-multilingual-MiniLM-L12-v2，384 维）
- 国内首跑设镜像：`HF_ENDPOINT=https://hf-mirror.com python scripts/rag_cli.py build`
- 已缓存后加速：`HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/rag_cli.py retrieve --query "..."`
- 仅 `chat`（生成式问答）需要 LLM API key

首次使用需：`pip install -r scripts/requirements.txt`（llamaindex 0.14 + HuggingFace embedding）

## 与其它 skill 的关系

- **competition-prep**：agent 仍负责"匹配当前题目特征推荐复用方案"，但底层检索改为调本 skill（精准章节级 vs 模糊关键词）
- **model-selector**：选模时可调本 skill 查"同类题型历年用什么模型"
- **paper-formal-writer**：写作时可调本 skill 查"某章节的优秀写法范式"

## 依赖

- Python 3.10+
- llamaindex 0.14、openai（或兼容接口）
- 向量索引存储于 `storage/`（自动生成）