---
name: citation-tracer
description: "引用溯源工具：验证引用真实性、追踪引用来源、检查引用完整性。参考 academic-research-skills 设计。触发词：引用溯源、citation check、引用验证、检查引用、引用完整性、参考文献核对、citation tracer、引用追踪。"
---

# 引用溯源工具（Citation Tracer）

> **版本**: v1.0 | **更新**: 2026-06-21
> **来源**: 参考 Imbad0202/academic-research-skills 设计

---

## 设计理念

引用溯源工具用于确保引用的真实性和完整性。本skill提供：
- 引用真实性验证
- 引用来源追踪
- 引用完整性检查

---

## 功能清单

### 1. 引用真实性验证

**功能**: 验证引用的论文是否存在、信息是否正确

**检查项**:
- 论文标题是否存在
- 作者信息是否正确
- 发表年份是否正确
- 期刊/会议信息是否正确
- DOI是否有效

### 2. 引用来源追踪

**功能**: 追踪引用的原始来源

**追踪内容**:
- 原始论文
- 引用链（A引用B，B引用C）
- 相关论文

### 3. 引用完整性检查

**功能**: 检查引用是否完整

**检查项**:
- 正文中的引用是否都有参考文献
- 参考文献是否都在正文中被引用
- 引用格式是否一致

---

## 验证脚本

### 引用真实性验证

> 以下为设计参考实现（原始设计稿）。实际可运行脚本见
> `scripts/verify_citation.py` 与 `scripts/verify_all_citations.py`，CLI 用法见下方「使用方式」。

```python
# 设计参考（非实际脚本源码）

import requests
import json
from typing import Optional

def verify_doi(doi: str) -> dict:
    """
    验证DOI是否有效

    参数:
        doi: DOI字符串

    返回:
        验证结果
    """
    url = f"https://api.crossref.org/works/{doi}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "valid": True,
                "title": data["message"]["title"][0],
                "authors": [author.get("given", "") + " " + author.get("family", "") 
                           for author in data["message"].get("author", [])],
                "year": data["message"].get("published", {}).get("date-parts", [[None]])[0][0],
                "journal": data["message"].get("container-title", [""])[0],
                "doi": doi
            }
        else:
            return {"valid": False, "error": "DOI not found"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def verify_title(title: str) -> dict:
    """
    通过标题验证论文

    参数:
        title: 论文标题

    返回:
        验证结果
    """
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "rows": 5
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("message", {}).get("items", [])

            if items:
                best_match = items[0]
                return {
                    "found": True,
                    "title": best_match["title"][0],
                    "authors": [author.get("given", "") + " " + author.get("family", "") 
                               for author in best_match.get("author", [])],
                    "year": best_match.get("published", {}).get("date-parts", [[None]])[0][0],
                    "journal": best_match.get("container-title", [""])[0],
                    "doi": best_match.get("DOI", ""),
                    "similarity": 1.0  # 简化处理
                }
            else:
                return {"found": False, "error": "No matching paper found"}
        else:
            return {"found": False, "error": "Search failed"}
    except Exception as e:
        return {"found": False, "error": str(e)}
```

---

## 使用方式

```bash
# 验证单条引用：离线 GB/T 7714 关键要素检查（作者/题名/年份）
python .claude/skills/citation-tracer/scripts/verify_citation.py \
  --citation "张三, 李四. 微电网优化调度综述[J]. 电力系统自动化, 2022, 46(5): 1-12." \
  --output paper_output/qa/citation_verify.json

# 按 DOI 验证（加 --online 查 CrossRef 确认真实存在；离线仅校验 DOI 格式）
python .claude/skills/citation-tracer/scripts/verify_citation.py \
  --doi "10.1234/example" --online \
  --output paper_output/qa/citation_verify.json

# 验证整篇论文引用：双向匹配（断链/未引用/编号断档）
# --references 可选（.bib 或编号文本）；缺省从论文内“参考文献”节提取
python .claude/skills/citation-tracer/scripts/verify_all_citations.py \
  --paper paper_output/final_paper_source.md \
  --references paper_output/refs.bib \
  --output paper_output/qa/citation_report.json

# 联网核验条目真实性（CrossRef query.bibliographic，超时 10s，失败自动降级为离线并明示）
python .claude/skills/citation-tracer/scripts/verify_all_citations.py \
  --paper paper_output/final_paper_source.md --online
```

> 退出码约定：0=无问题，1=发现引用问题，2=运行错误（可直接接入门禁）。
> 支持的论文格式：`.md` / `.tex` / `.txt` / `.docx`；文内引用识别 `[1]`、`\cite{key}`、（作者, 年份）三种模式。
> 说明：脚本只做可离线的完整性/格式分析与 CrossRef 元数据比对；「引用链追踪（A引B，B引C）」等语义级溯源由 agent 结合检索完成，脚本不伪造该能力。

---

## 输出格式

```json
{
  "total_citations": 15,
  "verified": 12,
  "unverified": 2,
  "missing": 1,
  "citations": [
    {
      "id": 1,
      "doi": "10.1234/example",
      "title": "Example Paper",
      "authors": ["Author 1", "Author 2"],
      "year": 2024,
      "journal": "Example Journal",
      "status": "verified"
    },
    {
      "id": 2,
      "title": "Unknown Paper",
      "status": "unverified",
      "error": "DOI not found"
    }
  ],
  "issues": [
    "引用[3]在正文中但不在参考文献列表中",
    "参考文献[15]未在正文中被引用"
  ]
}
```

---

## 版本历史

- v1.1.0 (2026-07-26): 补齐 scripts/verify_citation.py 与 scripts/verify_all_citations.py 实体脚本（此前仅文档引用）；新增 --citation 离线 GB/T 7714 检查、双向匹配 + 编号断档检查、--online CrossRef 核验（失败自动降级）
- v1.0.0 (2026-06-21): 初始版本，参考 Imbad0202/academic-research-skills 设计