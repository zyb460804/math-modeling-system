"""
knowledge_graph_query.py — 数学建模知识图谱查询工具

用法：
    python knowledge_graph_query.py --model "TOPSIS"
    python knowledge_graph_query.py --problem-type "评价类"
    python knowledge_graph_query.py --algorithm "熵权法" --red-flags
    python knowledge_graph_query.py --file "writing_templates.md"
    python knowledge_graph_query.py --path "评价类" "TOPSIS"
    python knowledge_graph_query.py --stats

借鉴：GBrain 知识图谱查询 + Karpathy 交叉引用导航
"""

import argparse
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 图谱数据结构
# ============================================================

@dataclass
class Entity:
    name: str
    type: str  # PROBLEM, MODEL, ALGORITHM, CODE, RESULT, TEMPLATE, PROMPT, RULE, CASE, SKILL
    description: str = ""
    file_path: str = ""
    tags: list = field(default_factory=list)


@dataclass
class Relation:
    source: str
    target: str
    type: str  # USES_MODEL, USES_ALGORITHM, HAS_CODE, PRODUCES, etc.
    description: str = ""


class KnowledgeGraph:
    """数学建模知识图谱"""

    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.relations: list[Relation] = []
        self._build_graph()

    def _add_entity(self, name: str, etype: str, desc: str = "", path: str = "", tags: list = None):
        self.entities[name] = Entity(name, etype, desc, path, tags or [])

    def _add_relation(self, source: str, target: str, rtype: str, desc: str = ""):
        self.relations.append(Relation(source, target, rtype, desc))

    def _build_graph(self):
        """构建知识图谱"""

        # ---- 评价类 ----
        self._add_entity("评价类赛题", "PROBLEM", "涉及多指标综合评价的竞赛题目", tags=["评价"])
        self._add_entity("层次分析法/AHP", "MODEL", "主观赋权的多准则决策方法", "resources/04_代码模板/01_层次分析法.py", ["评价", "赋权"])
        self._add_entity("TOPSIS", "MODEL", "逼近理想解排序法", "resources/04_代码模板/03_熵权法TOPSIS.py", ["评价", "排序"])
        self._add_entity("模糊综合评价", "MODEL", "基于模糊数学的综合评价", tags=["评价", "模糊"])
        self._add_entity("灰色关联分析", "MODEL", "基于灰色理论的关联度分析", tags=["评价", "灰色"])
        self._add_entity("特征值法", "ALGORITHM", "AHP 中的权重计算方法", tags=["AHP"])
        self._add_entity("熵权法", "ALGORITHM", "客观赋权方法", tags=["TOPSIS", "赋权"])
        self._add_entity("隶属度函数", "ALGORITHM", "模糊评价中的隶属度计算", tags=["模糊"])
        self._add_entity("灰色关联系数", "ALGORITHM", "灰色关联分析的核心计算", tags=["灰色"])

        self._add_relation("评价类赛题", "层次分析法/AHP", "USES_MODEL")
        self._add_relation("评价类赛题", "TOPSIS", "USES_MODEL")
        self._add_relation("评价类赛题", "模糊综合评价", "USES_MODEL")
        self._add_relation("评价类赛题", "灰色关联分析", "USES_MODEL")
        self._add_relation("层次分析法/AHP", "特征值法", "USES_ALGORITHM")
        self._add_relation("TOPSIS", "熵权法", "USES_ALGORITHM")
        self._add_relation("模糊综合评价", "隶属度函数", "USES_ALGORITHM")
        self._add_relation("灰色关联分析", "灰色关联系数", "USES_ALGORITHM")

        # 评价类案例
        self._add_entity("entropy_topsis_kmeans案例", "CASE", "熵权-TOPSIS-聚类组合案例", "resources/11_题型playbook/playbook-evaluation-decision.md")
        self._add_entity("evaluation案例", "CASE", "评价类通用案例", "resources/10_算法cookbook/cookbook-evaluation.md")
        self._add_relation("TOPSIS", "entropy_topsis_kmeans案例", "CASE_EXEMPLIFIES")
        self._add_relation("模糊综合评价", "evaluation案例", "CASE_EXEMPLIFIES")

        # 评价类红旗
        self._add_rule("熵权法", "数据量过少时熵权法失效", "outputs/algorithm_selection_red_flags.md")
        self._add_rule("灰色关联分析", "数据波动大时灰色关联不适用", "outputs/method_misuse_alerts.md")

        # ---- 预测类 ----
        self._add_entity("预测类赛题", "PROBLEM", "涉及时间序列或因果预测的竞赛题目", tags=["预测"])
        self._add_entity("灰色预测GM(1,1)", "MODEL", "小样本灰色预测模型", "resources/04_代码模板/05_灰色预测.py", ["预测", "灰色"])
        self._add_entity("ARIMA", "MODEL", "自回归积分滑动平均模型", "resources/04_代码模板/06_时间序列ARIMA.py", ["预测", "时间序列"])
        self._add_entity("BP神经网络", "MODEL", "反向传播神经网络", "resources/04_代码模板/08_BP神经网络.py", ["预测", "神经网络"])
        self._add_entity("回归分析", "MODEL", "多元线性/非线性回归", "resources/04_代码模板/04_多元回归.py", ["预测", "回归"])
        self._add_entity("组合预测", "MODEL", "多模型加权组合预测", tags=["预测", "组合"])
        self._add_entity("累加生成", "ALGORITHM", "灰色预测的数据预处理", tags=["灰色预测"])
        self._add_entity("差分平稳性检验", "ALGORITHM", "ARIMA 的平稳性检验", tags=["ARIMA"])
        self._add_entity("反向传播", "ALGORITHM", "BP 神经网络的训练算法", tags=["BP"])
        self._add_entity("最小二乘法", "ALGORITHM", "回归分析的参数估计", tags=["回归"])

        self._add_relation("预测类赛题", "灰色预测GM(1,1)", "USES_MODEL")
        self._add_relation("预测类赛题", "ARIMA", "USES_MODEL")
        self._add_relation("预测类赛题", "BP神经网络", "USES_MODEL")
        self._add_relation("预测类赛题", "回归分析", "USES_MODEL")
        self._add_relation("预测类赛题", "组合预测", "USES_MODEL")
        self._add_relation("灰色预测GM(1,1)", "累加生成", "USES_ALGORITHM")
        self._add_relation("ARIMA", "差分平稳性检验", "USES_ALGORITHM")
        self._add_relation("BP神经网络", "反向传播", "USES_ALGORITHM")
        self._add_relation("回归分析", "最小二乘法", "USES_ALGORITHM")
        self._add_relation("组合预测", "灰色预测GM(1,1)", "DEPENDS_ON")
        self._add_relation("组合预测", "ARIMA", "DEPENDS_ON")
        self._add_relation("组合预测", "BP神经网络", "DEPENDS_ON")

        # 预测类案例
        self._add_entity("grey_forecast案例", "CASE", "灰色预测案例", "resources/11_题型playbook/playbook-ml-regression.md")
        self._add_entity("arima案例", "CASE", "ARIMA时间序列案例", "resources/10_算法cookbook/cookbook-ml.md")
        self._add_entity("regression案例", "CASE", "回归分析案例", "resources/11_题型playbook/playbook-ml-regression.md")
        self._add_entity("forecast_residual_correction案例", "CASE", "预测残差修正案例", "resources/10_算法cookbook/cookbook-statistical.md")
        self._add_relation("灰色预测GM(1,1)", "grey_forecast案例", "CASE_EXEMPLIFIES")
        self._add_relation("ARIMA", "arima案例", "CASE_EXEMPLIFIES")
        self._add_relation("回归分析", "regression案例", "CASE_EXEMPLIFIES")

        # 预测类红旗
        self._add_rule("灰色预测GM(1,1)", "数据增长过快时不适用", "outputs/algorithm_selection_red_flags.md")
        self._add_rule("BP神经网络", "样本量<50时过拟合风险高", "outputs/method_misuse_alerts.md")

        # ---- 优化类 ----
        self._add_entity("优化类赛题", "PROBLEM", "涉及规划、调度、选址的竞赛题目", tags=["优化"])
        self._add_entity("线性规划", "MODEL", "目标函数和约束均为线性", "resources/04_代码模板/09_线性规划.py", ["优化", "规划"])
        self._add_entity("整数规划/0-1规划", "MODEL", "决策变量为整数的规划", "resources/04_代码模板/10_整数规划.py", ["优化", "整数"])
        self._add_entity("多目标优化", "MODEL", "同时优化多个目标", tags=["优化", "多目标"])
        self._add_entity("动态规划", "MODEL", "多阶段决策优化", tags=["优化", "动态"])
        self._add_entity("图论/最短路", "MODEL", "网络流与路径优化", "resources/04_代码模板/11_图论最短路.py", ["优化", "图论"])
        self._add_entity("排队论/仿真", "MODEL", "排队系统建模与仿真", tags=["优化", "仿真"])
        self._add_entity("单纯形法", "ALGORITHM", "线性规划求解算法", tags=["线性规划"])
        self._add_entity("分支定界法", "ALGORITHM", "整数规划求解算法", tags=["整数规划"])
        self._add_entity("NSGA-II", "ALGORITHM", "多目标进化算法", tags=["多目标"])
        self._add_entity("遗传算法", "ALGORITHM", "进化优化算法", tags=["优化"])
        self._add_entity("Bellman方程", "ALGORITHM", "动态规划核心方程", tags=["动态规划"])
        self._add_entity("Dijkstra", "ALGORITHM", "单源最短路径算法", tags=["图论"])
        self._add_entity("Floyd", "ALGORITHM", "全源最短路径算法", tags=["图论"])
        self._add_entity("蒙特卡洛模拟", "ALGORITHM", "随机模拟方法", tags=["仿真"])

        self._add_relation("优化类赛题", "线性规划", "USES_MODEL")
        self._add_relation("优化类赛题", "整数规划/0-1规划", "USES_MODEL")
        self._add_relation("优化类赛题", "多目标优化", "USES_MODEL")
        self._add_relation("优化类赛题", "动态规划", "USES_MODEL")
        self._add_relation("优化类赛题", "图论/最短路", "USES_MODEL")
        self._add_relation("优化类赛题", "排队论/仿真", "USES_MODEL")
        self._add_relation("线性规划", "单纯形法", "USES_ALGORITHM")
        self._add_relation("整数规划/0-1规划", "分支定界法", "USES_ALGORITHM")
        self._add_relation("多目标优化", "NSGA-II", "USES_ALGORITHM")
        self._add_relation("多目标优化", "遗传算法", "USES_ALGORITHM")
        self._add_relation("动态规划", "Bellman方程", "USES_ALGORITHM")
        self._add_relation("图论/最短路", "Dijkstra", "USES_ALGORITHM")
        self._add_relation("图论/最短路", "Floyd", "USES_ALGORITHM")
        self._add_relation("排队论/仿真", "蒙特卡洛模拟", "USES_ALGORITHM")

        # 优化类案例
        self._add_entity("linear_programming案例", "CASE", "线性规划案例", "resources/11_题型playbook/playbook-scheduling-opt.md")
        self._add_entity("binary_programming案例", "CASE", "0-1整数规划案例", "resources/11_题型playbook/playbook-scheduling-opt.md")
        self._add_entity("graph_path案例", "CASE", "图论最短路案例", "resources/11_题型playbook/playbook-path-planning.md")
        self._add_entity("monte_carlo案例", "CASE", "蒙特卡洛模拟案例", "resources/10_算法cookbook/cookbook-optimization.md")
        self._add_entity("queue_simulation案例", "CASE", "排队仿真案例", "resources/11_题型playbook/playbook-scheduling-opt.md")
        self._add_relation("线性规划", "linear_programming案例", "CASE_EXEMPLIFIES")
        self._add_relation("整数规划/0-1规划", "binary_programming案例", "CASE_EXEMPLIFIES")
        self._add_relation("图论/最短路", "graph_path案例", "CASE_EXEMPLIFIES")
        self._add_relation("排队论/仿真", "monte_carlo案例", "CASE_EXEMPLIFIES")
        self._add_relation("排队论/仿真", "queue_simulation案例", "CASE_EXEMPLIFIES")

        # 优化类红旗
        self._add_rule("多目标优化", "目标冲突未明确定义时不应使用", "outputs/algorithm_selection_red_flags.md")

        # ---- 分类/聚类类 ----
        self._add_entity("分类/聚类类赛题", "PROBLEM", "涉及聚类、降维、分类的竞赛题目", tags=["分类"])
        self._add_entity("K-Means聚类", "MODEL", "基于距离的划分聚类", "resources/04_代码模板/07_KMeans聚类.py", ["聚类"])
        self._add_entity("PCA降维", "MODEL", "主成分分析降维", "resources/04_代码模板/02_PCA主成分.py", ["降维"])
        self._add_entity("决策树/随机森林", "MODEL", "基于树结构的分类/回归", tags=["分类", "集成"])
        self._add_entity("肘部法则选K", "ALGORITHM", "K-Means 最佳K值选择", tags=["K-Means"])
        self._add_entity("特征分解", "ALGORITHM", "PCA 的核心计算", tags=["PCA"])
        self._add_entity("信息增益", "ALGORITHM", "决策树分裂准则", tags=["决策树"])
        self._add_entity("Bagging", "ALGORITHM", "随机森林的集成策略", tags=["随机森林"])

        self._add_relation("分类/聚类类赛题", "K-Means聚类", "USES_MODEL")
        self._add_relation("分类/聚类类赛题", "PCA降维", "USES_MODEL")
        self._add_relation("分类/聚类类赛题", "决策树/随机森林", "USES_MODEL")
        self._add_relation("K-Means聚类", "肘部法则选K", "USES_ALGORITHM")
        self._add_relation("PCA降维", "特征分解", "USES_ALGORITHM")
        self._add_relation("决策树/随机森林", "信息增益", "USES_ALGORITHM")
        self._add_relation("决策树/随机森林", "Bagging", "USES_ALGORITHM")

        # 分类类案例
        self._add_entity("kmeans案例", "CASE", "K-Means聚类案例", "resources/11_题型playbook/playbook-ml-classification.md")
        self._add_entity("pca案例", "CASE", "PCA降维案例", "resources/10_算法cookbook/cookbook-ml.md")
        self._add_relation("K-Means聚类", "kmeans案例", "CASE_EXEMPLIFIES")
        self._add_relation("PCA降维", "pca案例", "CASE_EXEMPLIFIES")

        # ---- 统计分析类 ----
        self._add_entity("统计分析类赛题", "PROBLEM", "涉及影响因素、相关性、显著性的竞赛题目", tags=["统计"])
        self._add_entity("Pearson相关分析", "MODEL", "连续变量线性相关分析", tags=["统计", "相关"])
        self._add_entity("Spearman秩相关", "MODEL", "非参数秩次相关分析", tags=["统计", "秩次"])
        self._add_entity("卡方检验", "MODEL", "离散变量独立性检验", tags=["统计", "离散"])
        self._add_entity("多元回归分析", "MODEL", "多变量因果关系建模", "resources/04_代码模板/50多种常用算法源代码/回归分析预测模型Matlab+Python代码/regression_analysis.py", ["统计", "回归"])
        self._add_entity("共线性检验", "ALGORITHM", "VIF方差膨胀因子检验", tags=["回归"])
        self._add_entity("残差分析", "ALGORITHM", "回归残差正态性和异方差检验", tags=["回归"])
        self._add_entity("显著性检验", "ALGORITHM", "p值和置信区间计算", tags=["统计"])

        self._add_relation("统计分析类赛题", "Pearson相关分析", "USES_MODEL")
        self._add_relation("统计分析类赛题", "Spearman秩相关", "USES_MODEL")
        self._add_relation("统计分析类赛题", "卡方检验", "USES_MODEL")
        self._add_relation("统计分析类赛题", "多元回归分析", "USES_MODEL")
        self._add_relation("多元回归分析", "共线性检验", "USES_ALGORITHM")
        self._add_relation("多元回归分析", "残差分析", "USES_ALGORITHM")
        self._add_relation("多元回归分析", "显著性检验", "USES_ALGORITHM")

        # ---- 机理分析类 ----
        self._add_entity("机理分析类赛题", "PROBLEM", "涉及传播、增长、系统演化的竞赛题目", tags=["机理"])
        self._add_entity("微分方程模型", "MODEL", "基于连续变化率的机理建模", "resources/04_代码模板/14种国赛必备算法源代码/机理分析 - 微分方程（种群增长）.py", ["机理", "微分方程"])
        self._add_entity("Logistic增长模型", "MODEL", "饱和增长的S曲线模型", tags=["机理", "增长"])
        self._add_entity("SIR传染病模型", "MODEL", "易感-感染-恢复传播模型", "resources/04_代码模板/50多种常用算法源代码/传染病模型Matlab+Python代码/epidemic_model.py", ["机理", "传播"])
        self._add_entity("系统动力学", "MODEL", "多变量反馈演化模型", "resources/04_代码模板/14种国赛必备算法源代码/系统动力学（SD）简化版（基于微分方程）.py", ["机理", "反馈"])
        self._add_entity("数值积分", "ALGORITHM", "微分方程数值求解方法", tags=["微分方程"])
        self._add_entity("参数拟合", "ALGORITHM", "机理模型参数估计", tags=["机理"])
        self._add_entity("Runge-Kutta法", "ALGORITHM", "高精度数值积分方法", tags=["微分方程"])

        self._add_relation("机理分析类赛题", "微分方程模型", "USES_MODEL")
        self._add_relation("机理分析类赛题", "Logistic增长模型", "USES_MODEL")
        self._add_relation("机理分析类赛题", "SIR传染病模型", "USES_MODEL")
        self._add_relation("机理分析类赛题", "系统动力学", "USES_MODEL")
        self._add_relation("微分方程模型", "数值积分", "USES_ALGORITHM")
        self._add_relation("微分方程模型", "参数拟合", "USES_ALGORITHM")
        self._add_relation("微分方程模型", "Runge-Kutta法", "USES_ALGORITHM")
        self._add_relation("SIR传染病模型", "数值积分", "USES_ALGORITHM")
        self._add_relation("系统动力学", "数值积分", "USES_ALGORITHM")

        # ---- 图与网络类 ----
        self._add_entity("图与网络类赛题", "PROBLEM", "涉及最短路、网络结构、选址的竞赛题目", tags=["图论"])
        self._add_entity("Dijkstra最短路", "MODEL", "单源最短路径算法", "resources/04_代码模板/50多种常用算法源代码/Dijkstra 算法（最短路径算法）Matlab+Python代码/dijkstra_algorithm.py", ["图论", "最短路"])
        self._add_entity("Floyd全源最短路", "MODEL", "全源最短路径算法", "resources/04_代码模板/50多种常用算法源代码/Floyd 算法（全源最短路径算法）Matlab+Python代码/floyd_algorithm.py", ["图论", "最短路"])
        self._add_entity("TSP旅行商", "MODEL", "旅行商路径优化问题", tags=["图论", "组合"])
        self._add_entity("复杂网络分析", "MODEL", "网络拓扑结构与中心性分析", tags=["图论", "网络"])
        self._add_entity("蚁群算法", "ALGORITHM", "基于信息素的路径优化算法", "resources/04_代码模板/14种国赛必备算法源代码/优化类 - 蚁群算法（TSP）.py", ["图论", "启发式"])
        self._add_entity("PageRank", "ALGORITHM", "网页重要性排序算法", tags=["网络"])
        self._add_entity("社区检测", "ALGORITHM", "网络社区发现算法", tags=["网络"])

        self._add_relation("图与网络类赛题", "Dijkstra最短路", "USES_MODEL")
        self._add_relation("图与网络类赛题", "Floyd全源最短路", "USES_MODEL")
        self._add_relation("图与网络类赛题", "TSP旅行商", "USES_MODEL")
        self._add_relation("图与网络类赛题", "复杂网络分析", "USES_MODEL")
        self._add_relation("TSP旅行商", "蚁群算法", "USES_ALGORITHM")
        self._add_relation("复杂网络分析", "PageRank", "USES_ALGORITHM")
        self._add_relation("复杂网络分析", "社区检测", "USES_ALGORITHM")

        # ---- 风险预警类 ----
        self._add_entity("风险预警类赛题", "PROBLEM", "涉及风险评分、预警阈值、违约预测的竞赛题目", tags=["风险"])
        self._add_entity("Logistic回归分类", "MODEL", "二分类风险预测模型", tags=["风险", "分类"])
        self._add_entity("随机森林分类", "MODEL", "集成树分类风险模型", tags=["风险", "集成"])
        self._add_entity("XGBoost分类", "MODEL", "梯度提升树分类模型", tags=["风险", "提升"])
        self._add_entity("贝叶斯网络", "MODEL", "概率图模型风险推理", tags=["风险", "概率"])
        self._add_entity("评分卡模型", "MODEL", "基于WOE/IV的信用评分", tags=["风险", "评分"])
        self._add_entity("阈值优化", "ALGORITHM", "ROC曲线最佳阈值选择", tags=["风险"])
        self._add_entity("混淆矩阵分析", "ALGORITHM", "分类模型性能评估", tags=["风险"])
        self._add_entity("风险分级", "ALGORITHM", "基于分数的等级划分", tags=["风险"])

        self._add_relation("风险预警类赛题", "Logistic回归分类", "USES_MODEL")
        self._add_relation("风险预警类赛题", "随机森林分类", "USES_MODEL")
        self._add_relation("风险预警类赛题", "XGBoost分类", "USES_MODEL")
        self._add_relation("风险预警类赛题", "贝叶斯网络", "USES_MODEL")
        self._add_relation("风险预警类赛题", "评分卡模型", "USES_MODEL")
        self._add_relation("Logistic回归分类", "阈值优化", "USES_ALGORITHM")
        self._add_relation("Logistic回归分类", "混淆矩阵分析", "USES_ALGORITHM")
        self._add_relation("随机森林分类", "混淆矩阵分析", "USES_ALGORITHM")
        self._add_relation("XGBoost分类", "混淆矩阵分析", "USES_ALGORITHM")
        self._add_relation("评分卡模型", "风险分级", "USES_ALGORITHM")

        # ---- 写作/审稿模板（跨题型通用） ----
        self._add_entity("writing_templates", "TEMPLATE", "论文各段落填空式模板", "outputs/writing_templates.md")
        self._add_entity("abstract_templates", "TEMPLATE", "三段式高分摘要模板", "outputs/abstract_templates.md")
        self._add_entity("scoring_rubric", "RULE", "100分制7维度评分标准", "outputs/scoring_rubric.md")
        self._add_entity("algorithm_templates", "TEMPLATE", "按题型的算法代码模板", "outputs/algorithm_templates.md")
        self._add_entity("method_matching", "TEMPLATE", "题型×模型×算法×风险匹配", "outputs/method_matching.md")
        self._add_entity("figure_templates", "TEMPLATE", "图示结构模板", "outputs/figure_templates.md")
        self._add_entity("defense_qa_bank", "TEMPLATE", "高频问答库", "outputs/defense_qa_bank.md")
        self._add_entity("final_quality_gate", "RULE", "P0阻断项终检清单", "outputs/final_quality_gate.md")
        self._add_entity("model_chain_blueprints", "TEMPLATE", "组合模型的标准架构", "outputs/model_chain_blueprints.md")
        self._add_entity("algorithm_selection_red_flags", "RULE", "算法选型红旗", "outputs/algorithm_selection_red_flags.md")
        self._add_entity("method_misuse_alerts", "RULE", "方法误用预警", "outputs/method_misuse_alerts.md")

    def _add_rule(self, target: str, desc: str, file_path: str):
        rule_name = f"红旗:{target}"
        self._add_entity(rule_name, "RULE", desc, file_path)
        self._add_relation(target, rule_name, "AVOIDS")

    # ---- 查询接口 ----

    def find_model(self, name: str) -> dict:
        """查找模型及其所有关联实体"""
        name = self._resolve_name(name, "MODEL")
        if not name:
            return {"error": f"未找到模型: {name}"}

        result = {
            "model": self.entities[name].__dict__,
            "algorithms": [],
            "code": [],
            "cases": [],
            "red_flags": [],
            "dependencies": [],
            "dependents": [],
        }

        for rel in self.relations:
            if rel.source == name:
                target = self.entities.get(rel.target)
                if not target:
                    continue
                if rel.type == "USES_ALGORITHM":
                    algo_info = target.__dict__.copy()
                    # 找算法的代码和红旗
                    algo_info["code"] = []
                    algo_info["red_flags"] = []
                    for r2 in self.relations:
                        if r2.source == rel.target:
                            t2 = self.entities.get(r2.target)
                            if t2:
                                if r2.type == "HAS_CODE":
                                    algo_info["code"].append(t2.__dict__)
                                elif r2.type == "AVOIDS":
                                    algo_info["red_flags"].append(t2.__dict__)
                    result["algorithms"].append(algo_info)
                elif rel.type == "CASE_EXEMPLIFIES":
                    result["cases"].append(target.__dict__)
                elif rel.type == "AVOIDS":
                    result["red_flags"].append(target.__dict__)
                elif rel.type == "DEPENDS_ON":
                    result["dependencies"].append(target.__dict__)

            elif rel.target == name and rel.type == "DEPENDS_ON":
                result["dependents"].append(self.entities[rel.source].__dict__)

        return result

    def find_problem_type(self, name: str) -> dict:
        """查找题型的完整建模路径"""
        name = self._resolve_name(name, "PROBLEM")
        if not name:
            return {"error": f"未找到题型: {name}"}

        result = {
            "problem": self.entities[name].__dict__,
            "models": [],
        }

        for rel in self.relations:
            if rel.source == name and rel.type == "USES_MODEL":
                model_info = self.find_model(rel.target)
                result["models"].append(model_info)

        return result

    def find_algorithm(self, name: str, red_flags_only: bool = False) -> dict:
        """查找算法及其红旗规则"""
        name = self._resolve_name(name, "ALGORITHM")
        if not name:
            return {"error": f"未找到算法: {name}"}

        result = {
            "algorithm": self.entities[name].__dict__,
            "code": [],
            "red_flags": [],
            "used_by_models": [],
        }

        for rel in self.relations:
            if rel.source == name:
                target = self.entities.get(rel.target)
                if not target:
                    continue
                if rel.type == "HAS_CODE":
                    result["code"].append(target.__dict__)
                elif rel.type == "AVOIDS":
                    result["red_flags"].append(target.__dict__)
            elif rel.target == name and rel.type == "USES_ALGORITHM":
                result["used_by_models"].append(self.entities[rel.source].__dict__)

        if red_flags_only:
            return {"algorithm": name, "red_flags": result["red_flags"]}

        return result

    def find_file_references(self, filename: str) -> dict:
        """查找文件的所有引用关系"""
        result = {"file": filename, "referenced_by": [], "references": []}

        for name, entity in self.entities.items():
            if filename in entity.file_path:
                result["referenced_by"].append({
                    "name": name,
                    "type": entity.type,
                    "description": entity.description,
                })

        return result

    def find_path(self, source_type: str, target_name: str) -> list:
        """查找从某题型到某实体的完整路径"""
        paths = []
        target = self._resolve_name(target_name)
        if not target:
            return [f"未找到实体: {target_name}"]

        # BFS 查找路径
        visited = set()
        queue = [(source_type, [source_type])]

        while queue:
            current, path = queue.pop(0)
            if current == target:
                paths.append(path)
                continue
            if current in visited:
                continue
            visited.add(current)

            for rel in self.relations:
                if rel.source == current and rel.target not in visited:
                    queue.append((rel.target, path + [f"--{rel.type}-->", rel.target]))
                elif rel.target == current and rel.source not in visited:
                    queue.append((rel.source, path + [f"<--{rel.type}--", rel.source]))

        return paths if paths else [f"未找到从 {source_type} 到 {target_name} 的路径"]

    def get_stats(self) -> dict:
        """获取图谱统计信息"""
        type_counts = {}
        for entity in self.entities.values():
            type_counts[entity.type] = type_counts.get(entity.type, 0) + 1

        rel_counts = {}
        for rel in self.relations:
            rel_counts[rel.type] = rel_counts.get(rel.type, 0) + 1

        return {
            "total_entities": len(self.entities),
            "total_relations": len(self.relations),
            "entity_types": type_counts,
            "relation_types": rel_counts,
        }

    def _resolve_name(self, name: str, expected_type: str = None) -> Optional[str]:
        """模糊匹配实体名称"""
        # 精确匹配
        if name in self.entities:
            if expected_type is None or self.entities[name].type == expected_type:
                return name

        # 模糊匹配
        candidates = []
        for ename, entity in self.entities.items():
            if name.lower() in ename.lower():
                if expected_type is None or entity.type == expected_type:
                    candidates.append(ename)

        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            # 优先选择精确前缀匹配
            for c in candidates:
                if c.lower().startswith(name.lower()):
                    return c
            return candidates[0]

        return None


# ============================================================
# CLI
# ============================================================

def main():
    # Windows GBK 兼容：强制 UTF-8 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="数学建模知识图谱查询工具")
    parser.add_argument("--model", type=str, help="查找模型及其关联实体")
    parser.add_argument("--problem-type", type=str, help="查找题型的完整建模路径")
    parser.add_argument("--algorithm", type=str, help="查找算法及其红旗规则")
    parser.add_argument("--red-flags", action="store_true", help="仅显示红旗规则（配合 --algorithm）")
    parser.add_argument("--file", type=str, help="查找文件的所有引用关系")
    parser.add_argument("--path", nargs=2, metavar=("FROM", "TO"), help="查找从某实体到某实体的路径")
    parser.add_argument("--stats", action="store_true", help="显示图谱统计信息")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    graph = KnowledgeGraph()

    if args.stats:
        result = graph.get_stats()
    elif args.model:
        result = graph.find_model(args.model)
    elif args.problem_type:
        result = graph.find_problem_type(args.problem_type)
    elif args.algorithm:
        result = graph.find_algorithm(args.algorithm, args.red_flags)
    elif args.file:
        result = graph.find_file_references(args.file)
    elif args.path:
        result = graph.find_path(args.path[0], args.path[1])
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_result(result)


def _print_result(result):
    """格式化输出"""
    if isinstance(result, dict):
        if "error" in result:
            print(f"❌ {result['error']}")
            return

        if "total_entities" in result:
            # 统计信息
            print("📊 知识图谱统计")
            print(f"  实体总数: {result['total_entities']}")
            print(f"  关系总数: {result['total_relations']}")
            print("\n  实体类型分布:")
            for t, c in sorted(result['entity_types'].items()):
                print(f"    {t}: {c}")
            print("\n  关系类型分布:")
            for t, c in sorted(result['relation_types'].items()):
                print(f"    {t}: {c}")
            return

        if "model" in result and "algorithms" in result:
            # 模型查询结果
            m = result['model']
            print(f"🔍 模型: {m['name']}")
            print(f"   描述: {m['description']}")
            if m.get('file_path'):
                print(f"   代码: {m['file_path']}")

            if result['algorithms']:
                print(f"\n   📐 关联算法 ({len(result['algorithms'])}):")
                for algo in result['algorithms']:
                    print(f"      • {algo['name']} — {algo['description']}")
                    for code in algo.get('code', []):
                        print(f"        → 代码: {code['file_path']}")
                    for flag in algo.get('red_flags', []):
                        print(f"        ⚠️ 红旗: {flag['description']}")

            if result['cases']:
                print(f"\n   📁 历史案例 ({len(result['cases'])}):")
                for case in result['cases']:
                    print(f"      • {case['name']} → {case['file_path']}")

            if result['red_flags']:
                print(f"\n   ⚠️ 红旗规则 ({len(result['red_flags'])}):")
                for flag in result['red_flags']:
                    print(f"      • {flag['description']}")

            if result['dependencies']:
                print(f"\n   ⬅️ 依赖的模型:")
                for dep in result['dependencies']:
                    print(f"      • {dep['name']}")

            if result['dependents']:
                print(f"\n   ➡️ 被依赖（下游模型）:")
                for dep in result['dependents']:
                    print(f"      • {dep['name']}")

        elif "problem" in result and "models" in result:
            # 题型查询结果
            p = result['problem']
            print(f"🔍 题型: {p['name']}")
            print(f"   描述: {p['description']}")
            print(f"\n   📐 可用模型 ({len(result['models'])}):")
            for model in result['models']:
                if isinstance(model, dict) and 'model' in model:
                    m = model['model']
                    print(f"      • {m['name']} — {m['description']}")
                    for algo in model.get('algorithms', []):
                        print(f"        └─ {algo['name']}")

        elif "algorithm" in result and "used_by_models" in result:
            # 算法查询结果
            a = result['algorithm']
            print(f"🔍 算法: {a['name']}")
            print(f"   描述: {a['description']}")

            if result['code']:
                print(f"\n   💻 代码:")
                for code in result['code']:
                    print(f"      • {code['file_path']}")

            if result['red_flags']:
                print(f"\n   ⚠️ 红旗规则:")
                for flag in result['red_flags']:
                    print(f"      • {flag['description']}")

            if result['used_by_models']:
                print(f"\n   📐 被以下模型使用:")
                for m in result['used_by_models']:
                    print(f"      • {m['name']}")

        elif "file" in result:
            # 文件引用查询
            print(f"🔍 文件: {result['file']}")
            if result['referenced_by']:
                print(f"   被以下实体引用:")
                for ref in result['referenced_by']:
                    print(f"      • [{ref['type']}] {ref['name']} — {ref['description']}")
            else:
                print("   未找到引用")

    elif isinstance(result, list):
        # 路径查询结果
        print("🔍 路径查询结果:")
        for i, path in enumerate(result, 1):
            if isinstance(path, str):
                print(f"   {path}")
            else:
                print(f"   路径 {i}: {' '.join(str(p) for p in path)}")


if __name__ == "__main__":
    main()
