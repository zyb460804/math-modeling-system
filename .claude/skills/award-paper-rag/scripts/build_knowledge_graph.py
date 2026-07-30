#!/usr/bin/env python
"""
build_knowledge_graph.py — 知识图谱构建脚本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
从论文 .md 和算法资料中提取实体与关系，构建 LlamaIndex 兼容的
知识图谱，存入 storage/graph_store.json。

实体类型: Paper, Method, Competition, Problem, TaskType
关系类型: uses_method, belongs_to, solves, is_type

数据源:
  1. data/papers/*.md — 281 篇优秀论文（heading 分块后的 .md）
  2. resources/04_代码模板/ — 算法代码模板（方法名录）
  3. resources/03_方法算法/ — 算法教材/案例（方法定义）

用法:
  python build_knowledge_graph.py                # 全量构建
  python build_knowledge_graph.py --rebuild       # 删除旧图谱重建
  python build_knowledge_graph.py --limit 50      # 先索引 50 篇测试
  python build_knowledge_graph.py --no-papers     # 仅算法资料
  python build_knowledge_graph.py --no-methods    # 仅论文

依赖: llama-index (已在 requirements.txt)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── 路径 ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # award-paper-rag/
STORAGE_DIR = PROJECT_ROOT / "storage"
DATA_DIR = PROJECT_ROOT / "data" / "papers"
RESOURCES_DIR = Path(__file__).resolve().parents[4] / "resources"

# ── 实体常量 ──────────────────────────────────────────────────

# 已知数学建模方法关键词 → 规范名称
METHOD_PATTERNS: dict[str, str] = {
    # 评价类
    r"\b(?:AHP|层次分析)": "AHP_层次分析法",
    r"\b(?:TOPSIS|逼近理想解)": "TOPSIS_逼近理想解排序法",
    r"\b(?:熵权法?|熵值法|熵权)": "熵权法",
    r"\b(?:模糊综合评价|模糊评价|FCE)": "模糊综合评价",
    r"\b(?:灰色关联|灰色关联度|GRA)": "灰色关联分析",
    r"\b(?:DEA|数据包络)": "DEA_数据包络分析",
    r"\b(?:RSR|秩和比)": "RSR_秩和比法",
    r"\b(?:主成分分析|PCA)": "PCA_主成分分析",
    r"\b(?:因子分析)": "因子分析",
    r"\b(?:粗糙集)": "粗糙集",
    # 预测类
    r"\b(?:ARIMA|差分自回归)": "ARIMA",
    r"\b(?:LSTM|长短期记忆)": "LSTM",
    r"\b(?:GRU|门控循环)": "GRU",
    r"\b(?:灰色预测|GM\(1,1\)|GM\(1\s*,\s*1\)|GM模型)": "GM(1,1)_灰色预测",
    r"\b(?:Prophet)": "Prophet",
    r"\b(?:XGBoost|XGB)": "XGBoost",
    r"\b(?:LightGBM)": "LightGBM",
    r"\b(?:随机森林|Random\s*Forest)": "随机森林",
    r"\b(?:支持向量机|SVM|SVR)": "SVM_支持向量机",
    r"\b(?:BP神经网络|BP网络|反向传播)": "BP神经网络",
    r"\b(?:贝叶斯网络|贝叶斯)": "贝叶斯网络",
    r"\b(?:马尔可夫|Markov)": "马尔可夫链",
    r"\b(?:蒙特卡洛|Monte\s*Carlo)": "蒙特卡洛模拟",
    r"\b(?:时间序列)": "时间序列分析",
    r"\b(?:Elman)": "Elman神经网络",
    r"\b(?:NARX)": "NARX神经网络",
    r"\b(?:RBF)": "RBF神经网络",
    r"\b(?:小波分析)": "小波分析",
    r"\b(?:CNN|卷积神经)": "CNN",
    r"\b(?:GARCH)": "GARCH模型",
    r"\b(?:SARIMA)": "SARIMA",
    # 优化类
    r"\b(?:遗传算法|GA\b)": "GA_遗传算法",
    r"\b(?:粒子群|PSO)": "PSO_粒子群优化",
    r"\b(?:蚁群|ACO|蚁群算法)": "ACO_蚁群算法",
    r"\b(?:模拟退火|SA\b)": "SA_模拟退火",
    r"\b(?:禁忌搜索|TS\b)": "TS_禁忌搜索",
    r"\b(?:差分进化|DE\b)": "DE_差分进化",
    r"\b(?:NSGA[-\s]?II|非支配排序)": "NSGA-II",
    r"\b(?:MOPSO|多目标粒子群)": "MOPSO",
    r"\b(?:人工蜂群|ABC\b)": "ABC_人工蜂群算法",
    r"\b(?:线性规划|LP\b)": "LP_线性规划",
    r"\b(?:整数规划|0[\s-]*1规划)": "整数规划",
    r"\b(?:动态规划|DP\b)": "动态规划",
    r"\b(?:贪心|greedy)": "贪心算法",
    r"\b(?:贝叶斯优化)": "贝叶斯优化",
    r"\b(?:梯度下降)": "梯度下降",
    r"\b(?:约束规划|CP\b)": "约束规划",
    # 聚类/分类
    r"\b(?:K[\s-]?means|K均值)": "K-Means",
    r"\b(?:DBSCAN)": "DBSCAN",
    r"\b(?:层次聚类)": "层次聚类",
    r"\b(?:GMM|高斯混合)": "GMM_高斯混合模型",
    r"\b(?:SOM|自组织)": "SOM_自组织映射",
    r"\b(?:KNN|K近邻)": "KNN",
    r"\b(?:决策树)": "决策树",
    r"\b(?:AdaBoost)": "AdaBoost",
    r"\b(?:Stacking)": "Stacking集成",
    # 网络/图论
    r"\b(?:Dijkstra|迪杰斯特拉)": "Dijkstra算法",
    r"\b(?:Floyd)": "Floyd算法",
    r"\b(?:网络流)": "网络流",
    r"\b(?:图论)": "图论",
    # 微分方程/模拟
    r"\b(?:微分方程|ODE|常微分)": "微分方程",
    r"\b(?:偏微分|PDE)": "偏微分方程",
    r"\b(?:元胞自动机)": "元胞自动机",
    r"\b(?:系统动力学|SD模型)": "系统动力学",
    r"\b(?:排队论)": "排队论",
    r"\b(?:Agent[\s-]?Based|ABM)": "Agent-Based建模",
    # 检验/分析
    r"\b(?:灵敏度分析|sensitivity)": "灵敏度分析",
    r"\b(?:鲁棒性|robustness)": "鲁棒性检验",
    r"\b(?:假设检验)": "假设检验",
    r"\b(?:ANOVA|方差分析)": "方差分析",
    r"\b(?:回归分析)": "回归分析",
    r"\b(?:Spearman|斯皮尔曼)": "Spearman相关",
    r"\b(?:Pearson|皮尔逊)": "Pearson相关",
    r"\b(?:Kendall|肯德尔)": "Kendall相关",
}

# 题型关键词
TASK_PATTERNS: dict[str, str] = {
    r"\b(?:评价|评估|打分|评级|排名)": "evaluation_评价类",
    r"\b(?:预测|预报|预估)": "prediction_预测类",
    r"\b(?:优化|最优|最小化|最大化|调度|路径规划)": "optimization_优化类",
    r"\b(?:聚类|分类|识别|诊断)": "classification_分类聚类",
    r"\b(?:模拟|仿真)": "simulation_模拟仿真",
    r"\b(?:博弈|Game|均衡|策略)": "game_theory_博弈论",
    r"\b(?:网络|图|最短路径|流)": "network_网络图论",
}


def _read_paper_files(
    papers_dir: Path, limit: Optional[int] = None
) -> list[tuple[Path, str, dict]]:
    """读取论文 .md 文件，返回 (路径, 正文, 元数据) 列表。"""
    papers: list[tuple[Path, str, dict]] = []
    md_files = sorted(papers_dir.glob("*.md"))
    if limit:
        md_files = md_files[:limit]

    for fp in md_files:
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # 从文件名解析元数据
        meta = _parse_paper_filename(fp.stem)
        papers.append((fp, content, meta))
    return papers


def _parse_paper_filename(stem: str) -> dict:
    """从论文文件名解析 year/competition/problem。

    文件名格式: "2016_MCM_ICM__2016A--48649" 或 "2015_CUMCM_A_太阳影子定位"
    """
    meta: dict = {"year": 0, "competition": "unknown", "problem": "unknown"}
    # 提取年份
    m = re.search(r"^(\d{4})", stem)
    if m:
        meta["year"] = int(m.group(1))
    # 竞赛
    if "CUMCM" in stem or "国赛" in stem:
        meta["competition"] = "CUMCM"
    elif "MCM" in stem or "ICM" in stem or "美赛" in stem:
        meta["competition"] = "MCM-ICM"
    elif "MathorCup" in stem:
        meta["competition"] = "MathorCup"
    # 题号
    for p in ["A", "B", "C", "D", "E", "F"]:
        if re.search(rf"[_\-]{p}[_\-]", stem) or stem.endswith(p):
            meta["problem"] = p
            break
    return meta


def _extract_methods_from_text(text: str) -> set[str]:
    """从文本中提取方法名。"""
    found: set[str] = set()
    # 只在前 5000 字符搜索（摘要+引言+模型建立部分，方法密度最高）
    head = text[:5000]
    for pattern, method_name in METHOD_PATTERNS.items():
        if re.search(pattern, head, re.IGNORECASE):
            found.add(method_name)
    return found


def _extract_task_types(text: str) -> set[str]:
    """从文本推断题型。"""
    found: set[str] = set()
    head = text[:3000]
    for pattern, task_name in TASK_PATTERNS.items():
        if re.search(pattern, head, re.IGNORECASE):
            found.add(task_name)
    if not found:
        found.add("unknown")
    return found


def _get_known_methods_from_code_templates() -> set[str]:
    """从算法代码模板目录中提取方法名列表。"""
    methods: set[str] = set()
    code_dir = RESOURCES_DIR / "04_代码模板"
    if not code_dir.exists():
        return methods

    for root, dirs, files in code_dir.walk() if hasattr(code_dir, "walk") else []:
        for dname in dirs:
            methods.add(dname)
    # 通过遍历获取
    try:
        for p in sorted(code_dir.rglob("*")):
            if p.is_dir():
                name = p.name
                # 过滤掉太通用的目录名
                if len(name) > 3 and not name.startswith("."):
                    methods.add(name)
    except Exception:
        pass
    return methods


def _build_knowledge_graph(
    paper_dir: Path = DATA_DIR,
    persist_dir: Path = STORAGE_DIR,
    rebuild: bool = False,
    limit: Optional[int] = None,
    include_papers: bool = True,
    include_methods: bool = True,
) -> dict:
    """构建知识图谱并返回图结构。

    Returns:
        dict with keys: nodes, edges, triples, stats
    """
    if rebuild:
        graph_path = persist_dir / "graph_store.json"
        if graph_path.exists():
            graph_path.unlink()
            print("[kg] 已删除旧图谱", file=sys.stderr)

    t0 = time.perf_counter()

    # ── 节点存储 ────────────────────────────────────────────
    nodes: dict[str, dict] = {}   # node_id → {type, label, properties}
    triples: list[tuple[str, str, str]] = []  # (subject, predicate, object)

    def add_node(node_id: str, node_type: str, label: str, **props):
        if node_id not in nodes:
            nodes[node_id] = {"type": node_type, "label": label, "properties": props}

    def add_triple(subj: str, pred: str, obj: str):
        triples.append((subj, pred, obj))
        # 确保 subject 和 object 节点存在
        if subj not in nodes:
            add_node(subj, "Entity", subj)
        if obj not in nodes:
            add_node(obj, "Entity", obj)

    # ── 1. 论文实体提取 ──────────────────────────────────────
    if include_papers:
        papers = _read_paper_files(paper_dir, limit=limit)
        print(f"[kg] 读取 {len(papers)} 篇论文", file=sys.stderr)

        total_methods_found = 0
        for fp, content, meta in papers:
            doc_id = fp.stem
            # 添加论文节点
            add_node(
                doc_id,
                "Paper",
                doc_id[:80],
                year=meta.get("year", 0),
                competition=meta.get("competition", "unknown"),
                problem=meta.get("problem", "unknown"),
            )
            # 论文 → 竞赛
            comp = meta.get("competition", "unknown")
            if comp != "unknown":
                comp_id = f"competition__{comp}"
                add_node(comp_id, "Competition", comp)
                add_triple(doc_id, "belongs_to_competition", comp_id)

            # 论文 → 题号
            prob = meta.get("problem", "unknown")
            if prob != "unknown":
                prob_id = f"problem__{prob}"
                add_node(prob_id, "Problem", f"Problem {prob}")
                add_triple(doc_id, "solves_problem", prob_id)

            # 论文 → 方法
            methods = _extract_methods_from_text(content)
            for method in methods:
                method_id = f"method__{method}"
                add_node(method_id, "Method", method)
                add_triple(doc_id, "uses_method", method_id)
                total_methods_found += 1

            # 论文 → 题型
            tasks = _extract_task_types(content)
            for task in tasks:
                if task != "unknown":
                    task_id = f"task__{task}"
                    add_node(task_id, "TaskType", task)
                    add_triple(doc_id, "is_task_type", task_id)

        print(
            f"  [kg] 论文实体: {len(papers)}  方法提及: {total_methods_found}",
            file=sys.stderr,
        )

    # ── 2. 方法间关系（从代码模板目录结构推断）─────────────
    if include_methods:
        # 方法 ↔ 题型映射
        method_task_map = {
            "AHP_层次分析法": "evaluation_评价类",
            "TOPSIS_逼近理想解排序法": "evaluation_评价类",
            "熵权法": "evaluation_评价类",
            "模糊综合评价": "evaluation_评价类",
            "灰色关联分析": "evaluation_评价类",
            "DEA_数据包络分析": "evaluation_评价类",
            "RSR_秩和比法": "evaluation_评价类",
            "PCA_主成分分析": "evaluation_评价类",
            "因子分析": "evaluation_评价类",
            "粗糙集": "evaluation_评价类",
            "ARIMA": "prediction_预测类",
            "LSTM": "prediction_预测类",
            "GRU": "prediction_预测类",
            "GM(1,1)_灰色预测": "prediction_预测类",
            "Prophet": "prediction_预测类",
            "XGBoost": "prediction_预测类",
            "LightGBM": "prediction_预测类",
            "随机森林": "prediction_预测类",
            "SVM_支持向量机": "prediction_预测类",
            "BP神经网络": "prediction_预测类",
            "贝叶斯网络": "prediction_预测类",
            "马尔可夫链": "prediction_预测类",
            "时间序列分析": "prediction_预测类",
            "CNN": "prediction_预测类",
            "GA_遗传算法": "optimization_优化类",
            "PSO_粒子群优化": "optimization_优化类",
            "ACO_蚁群算法": "optimization_优化类",
            "SA_模拟退火": "optimization_优化类",
            "TS_禁忌搜索": "optimization_优化类",
            "DE_差分进化": "optimization_优化类",
            "NSGA-II": "optimization_优化类",
            "MOPSO": "optimization_优化类",
            "ABC_人工蜂群算法": "optimization_优化类",
            "LP_线性规划": "optimization_优化类",
            "整数规划": "optimization_优化类",
            "动态规划": "optimization_优化类",
            "贪心算法": "optimization_优化类",
            "贝叶斯优化": "optimization_优化类",
            "K-Means": "classification_分类聚类",
            "DBSCAN": "classification_分类聚类",
            "层次聚类": "classification_分类聚类",
            "KNN": "classification_分类聚类",
            "决策树": "classification_分类聚类",
            "AdaBoost": "classification_分类聚类",
            "SOM_自组织映射": "classification_分类聚类",
            "微分方程": "simulation_模拟仿真",
            "元胞自动机": "simulation_模拟仿真",
            "系统动力学": "simulation_模拟仿真",
            "排队论": "simulation_模拟仿真",
        }

        for method_name, task_name in method_task_map.items():
            method_id = f"method__{method_name}"
            task_id = f"task__{task_name}"
            if method_id in nodes or True:  # 即使方法未被论文引用也添加
                add_node(method_id, "Method", method_name)
                add_node(task_id, "TaskType", task_name)
                add_triple(method_id, "used_for_task", task_id)

        # 组合算法关系（从代码模板中识别）
        combos = [
            ("AHP_层次分析法", "熵权法", "often_combined_with"),
            ("GA_遗传算法", "BP神经网络", "often_combined_with"),
            ("PSO_粒子群优化", "SVM_支持向量机", "often_combined_with"),
            ("GA_遗传算法", "SA_模拟退火", "often_combined_with"),
            ("PSO_粒子群优化", "BP神经网络", "often_combined_with"),
            ("GA_遗传算法", "随机森林", "often_combined_with"),
            ("PCA_主成分分析", "SVM_支持向量机", "often_combined_with"),
            ("PCA_主成分分析", "随机森林", "often_combined_with"),
            ("灰色关联分析", "TOPSIS_逼近理想解排序法", "often_combined_with"),
            ("贝叶斯优化", "随机森林", "often_combined_with"),
            ("贝叶斯优化", "XGBoost", "often_combined_with"),
            ("ARIMA", "LSTM", "often_combined_with"),
            ("CNN", "LSTM", "often_combined_with"),
            ("小波分析", "LSTM", "often_combined_with"),
            ("GA_遗传算法", "模糊综合评价", "often_combined_with"),
        ]
        for m1, m2, rel in combos:
            id1, id2 = f"method__{m1}", f"method__{m2}"
            add_node(id1, "Method", m1)
            add_node(id2, "Method", m2)
            add_triple(id1, rel, id2)

    # ── 3. 竞赛层级 ──────────────────────────────────────────
    for comp_name in ["CUMCM", "MCM-ICM", "MathorCup", "电工杯", "五一赛"]:
        comp_id = f"competition__{comp_name}"
        add_node(comp_id, "Competition", comp_name)

    for prob_name in ["A", "B", "C", "D", "E", "F"]:
        prob_id = f"problem__{prob_name}"
        add_node(prob_id, "Problem", f"Problem {prob_name}")

    # ── 4. 构建图结构 ────────────────────────────────────────
    # 转换为 LlamaIndex KnowledgeGraphIndex 兼容格式
    # graph_dict: {node_id: [related_node_ids]}
    graph_dict: dict[str, list[str]] = defaultdict(list)
    for subj, _pred, obj in triples:
        graph_dict[subj].append(obj)
        graph_dict[obj].append(subj)
    # 去重
    graph_dict = {k: list(set(v)) for k, v in graph_dict.items()}

    graph_data = {
        "graph_dict": graph_dict,
        "_node_info": nodes,      # 扩展：节点类型和属性
        "_triples": [
            {"subject": s, "predicate": p, "object": o}
            for s, p, o in triples
        ],
    }

    # ── 持久化 ────────────────────────────────────────────────
    persist_dir.mkdir(parents=True, exist_ok=True)
    graph_path = persist_dir / "graph_store.json"
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)

    elapsed = time.perf_counter() - t0
    stats = {
        "nodes": len(nodes),
        "triples": len(triples),
        "node_types": {},
        "elapsed_seconds": round(elapsed, 1),
    }
    for node_data in nodes.values():
        t = node_data["type"]
        stats["node_types"][t] = stats["node_types"].get(t, 0) + 1

    print(f"\n[kg] ✓ 知识图谱构建完成！", file=sys.stderr)
    print(f"  节点: {stats['nodes']}  三元组: {stats['triples']}  耗时: {stats['elapsed_seconds']}s", file=sys.stderr)
    for nt, count in sorted(stats["node_types"].items()):
        print(f"    {nt}: {count}", file=sys.stderr)

    return graph_data


# ── CLI ────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build knowledge graph from math-model papers and algorithms."
    )
    p.add_argument(
        "--paper-dir",
        default=str(DATA_DIR),
        help=f"Papers directory (default: {DATA_DIR})",
    )
    p.add_argument(
        "--persist-dir",
        default=str(STORAGE_DIR),
        help=f"Persist directory (default: {STORAGE_DIR})",
    )
    p.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete old graph and rebuild.",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of papers to process (for testing).",
    )
    p.add_argument(
        "--no-papers",
        action="store_true",
        help="Skip paper processing (only method relations).",
    )
    p.add_argument(
        "--no-methods",
        action="store_true",
        help="Skip method-level relations (only paper entities).",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir)
    if args.no_papers is False and not paper_dir.exists():
        print(f"[kg] 论文目录不存在，仅构建方法图谱: {paper_dir}", file=sys.stderr)

    try:
        _build_knowledge_graph(
            paper_dir=paper_dir,
            persist_dir=Path(args.persist_dir),
            rebuild=args.rebuild,
            limit=args.limit,
            include_papers=not args.no_papers,
            include_methods=not args.no_methods,
        )
    except KeyboardInterrupt:
        print("\n[kg] 用户中断", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())