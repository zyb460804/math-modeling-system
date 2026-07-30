#!/usr/bin/env python3
"""
论文检索脚本

从多个学术搜索引擎搜索论文。

用法：
    python search_papers.py --query "mathematical modeling" --source semantic_scholar --limit 10
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 配置 UTF-8 输出
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass


def search_semantic_scholar(query: str, limit: int = 10) -> list[dict]:
    """从Semantic Scholar搜索论文"""
    try:
        import requests

        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,url,externalIds,citationCount"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        papers = []
        for item in data.get("data", []):
            paper = {
                "title": item.get("title", ""),
                "authors": [a.get("name", "") for a in item.get("authors", [])],
                "year": item.get("year"),
                "abstract": item.get("abstract", ""),
                "url": item.get("url", ""),
                "doi": item.get("externalIds", {}).get("DOI", ""),
                "citation_count": item.get("citationCount", 0)
            }
            papers.append(paper)

        return papers

    except ImportError:
        print("❌ 需要安装requests: pip install requests")
        return []
    except Exception as e:
        print(f"❌ Semantic Scholar搜索失败: {e}")
        return []


def search_arxiv(query: str, limit: int = 10) -> list[dict]:
    """从arXiv搜索论文"""
    try:
        import requests
        import xml.etree.ElementTree as ET

        url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        # 解析XML
        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            abstract = entry.find("atom:summary", ns).text.strip()
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            year = entry.find("atom:published", ns).text[:4]
            url = entry.find("atom:id", ns).text

            paper = {
                "title": title,
                "authors": authors,
                "year": int(year),
                "abstract": abstract,
                "url": url,
                "doi": "",
                "citation_count": 0
            }
            papers.append(paper)

        return papers

    except ImportError:
        print("❌ 需要安装requests: pip install requests")
        return []
    except Exception as e:
        print(f"❌ arXiv搜索失败: {e}")
        return []


def search_papers(query: str, source: str = "semantic_scholar", limit: int = 10) -> list[dict]:
    """搜索论文"""
    if source == "semantic_scholar":
        return search_semantic_scholar(query, limit)
    elif source == "arxiv":
        return search_arxiv(query, limit)
    else:
        print(f"❌ 不支持的数据源: {source}")
        return []


def save_results(results: dict, output_path: Path):
    """保存搜索结果"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 结果已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="论文检索脚本")
    parser.add_argument("--query", type=str, required=True, help="搜索关键词")
    parser.add_argument("--source", type=str, default="semantic_scholar",
                        choices=["semantic_scholar", "arxiv"],
                        help="数据源")
    parser.add_argument("--limit", type=int, default=10, help="返回结果数量")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")

    args = parser.parse_args()

    print(f"搜索: {args.query}")
    print(f"数据源: {args.source}")
    print(f"限制: {args.limit}")

    # 搜索论文
    papers = search_papers(args.query, args.source, args.limit)

    if not papers:
        print("❌ 未找到论文")
        sys.exit(1)

    print(f"✅ 找到 {len(papers)} 篇论文")

    # 构建结果
    results = {
        "query": args.query,
        "source": args.source,
        "search_time": datetime.now().isoformat(),
        "total_results": len(papers),
        "papers": papers
    }

    # 保存结果
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(f"paper_output/refs/search_results.json")

    save_results(results, output_path)

    # 打印摘要
    print("\n搜索结果摘要:")
    for i, paper in enumerate(papers[:5], 1):
        print(f"{i}. {paper['title'][:60]}...")
        print(f"   作者: {', '.join(paper['authors'][:2])}")
        print(f"   年份: {paper['year']}")
        print(f"   引用: {paper['citation_count']}")
        print()


if __name__ == "__main__":
    main()
