"""智能选模脚本：根据题型推荐模型+算法+风险。

用法：python select_model.py --type 优化 --subtype 线性规划
      python select_model.py --problem problem_analysis.json

输出：推荐结果 JSON
"""
import argparse
import json
import os
import sys
from pathlib import Path

# 方法匹配数据（从 outputs/method_matching.md 提取）
METHOD_matching = {
    "评价": {
        "models": [
            {"name": "熵权TOPSIS", "algorithm": "熵权法+TOPSIS", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/熵权TOPSIS/"},
            {"name": "AHP层次分析", "algorithm": "AHP", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/AHP/"},
            {"name": "模糊综合评价", "algorithm": "模糊数学", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/模糊综合评价/"},
            {"name": "DEA数据包络", "algorithm": "DEA", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/DEA/"},
            {"name": "灰色关联分析", "algorithm": "灰色理论", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/灰色关联分析/"},
        ],
        "charts": ["雷达图", "热力图", "柱状图", "排名图"],
    },
    "预测": {
        "models": [
            {"name": "ARIMA", "algorithm": "时间序列", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/ARIMA/"},
            {"name": "灰色预测GM(1,1)", "algorithm": "灰色理论", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/灰色预测/"},
            {"name": "LSTM", "algorithm": "深度学习", "risk": "高", "code": "resources/04_代码模板/50多种常用算法源代码/LSTM/"},
            {"name": "Prophet", "algorithm": "时间序列", "risk": "低", "code": "resources/04_代码模板/14种国赛必备算法源代码/Prophet.py"},
            {"name": "XGBoost", "algorithm": "集成学习", "risk": "中", "code": "resources/04_代码模板/14种国赛必备算法源代码/XGBoost.py"},
        ],
        "charts": ["拟合曲线+置信区间", "残差图", "误差分布图", "预测对比图"],
    },
    "优化": {
        "models": [
            {"name": "线性规划", "algorithm": "单纯形法/内点法", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/线性规划/"},
            {"name": "整数规划", "algorithm": "分支定界", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/整数规划/"},
            {"name": "遗传算法", "algorithm": "进化算法", "risk": "中", "code": "resources/04_代码模板/14种国赛必备算法源代码/遗传算法.py"},
            {"name": "粒子群算法", "algorithm": "群智能", "risk": "中", "code": "resources/04_代码模板/14种国赛必备算法源代码/粒子群算法.py"},
            {"name": "模拟退火", "algorithm": "随机搜索", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/模拟退火/"},
        ],
        "charts": ["收敛曲线", "3D曲面图", "等高线图", "平行坐标图"],
    },
    "分类": {
        "models": [
            {"name": "随机森林", "algorithm": "集成学习", "risk": "低", "code": "resources/04_代码模板/14种国赛必备算法源代码/随机森林.py"},
            {"name": "SVM", "algorithm": "核方法", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/SVM/"},
            {"name": "KNN", "algorithm": "距离度量", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/KNN/"},
            {"name": "逻辑回归", "algorithm": "广义线性", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/逻辑回归/"},
            {"name": "BP神经网络", "algorithm": "深度学习", "risk": "高", "code": "resources/04_代码模板/50多种常用算法源代码/BP神经网络/"},
        ],
        "charts": ["混淆矩阵热力图", "ROC曲线", "散点矩阵", "特征重要性图"],
    },
    "聚类": {
        "models": [
            {"name": "K-means", "algorithm": "划分聚类", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/K-means/"},
            {"name": "DBSCAN", "algorithm": "密度聚类", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/DBSCAN/"},
            {"name": "层次聚类", "algorithm": "层次聚类", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/层次聚类/"},
        ],
        "charts": ["聚类散点图(PCA降维)", "轮廓系数图", "树状图"],
    },
    "图论": {
        "models": [
            {"name": "Dijkstra", "algorithm": "最短路径", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/Dijkstra/"},
            {"name": "Floyd", "algorithm": "全源最短路径", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/Floyd/"},
            {"name": "最小生成树", "algorithm": "Prim/Kruskal", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/最小生成树/"},
            {"name": "网络流", "algorithm": "最大流/最小割", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/网络流/"},
        ],
        "charts": ["网络拓扑图", "最短路径高亮图", "社区检测图"],
    },
    "仿真": {
        "models": [
            {"name": "蒙特卡洛", "algorithm": "随机模拟", "risk": "低", "code": "resources/04_代码模板/50多种常用算法源代码/蒙特卡洛/"},
            {"name": "排队论", "algorithm": "随机过程", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/排队论/"},
            {"name": "系统动力学", "algorithm": "微分方程", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/系统动力学/"},
            {"name": "元胞自动机", "algorithm": "离散模拟", "risk": "中", "code": "resources/04_代码模板/50多种常用算法源代码/元胞自动机/"},
        ],
        "charts": ["时间序列图", "状态转移图", "敏感性分析图"],
    },
}


def select_model(problem_type: str, sub_type: str = None, data_type: str = None) -> dict:
    """根据题型推荐模型。"""
    # 匹配题型
    matched_type = None
    for key in METHOD_matching:
        if key in problem_type or problem_type in key:
            matched_type = key
            break

    if not matched_type:
        # 默认返回优化
        matched_type = "优化"

    info = METHOD_matching[matched_type]

    # 构建推荐
    recommendations = []
    for i, model in enumerate(info["models"][:3]):
        recommendations.append({
            "rank": i + 1,
            "name": model["name"],
            "algorithm": model["algorithm"],
            "risk": model["risk"],
            "code_path": model["code"],
        })

    return {
        "problem_type": matched_type,
        "sub_type": sub_type,
        "recommendations": recommendations,
        "recommended_charts": info["charts"],
        "total_options": len(info["models"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Smart model selector")
    parser.add_argument('--type', required=True, help='Problem type (评价/预测/优化/分类/聚类/图论/仿真)')
    parser.add_argument('--subtype', default=None, help='Sub-type')
    parser.add_argument('--problem', default=None, help='Problem analysis JSON file')
    args = parser.parse_args()

    result = select_model(args.type, args.subtype)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
