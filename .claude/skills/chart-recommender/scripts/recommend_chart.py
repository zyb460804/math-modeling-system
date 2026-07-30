"""图表推荐脚本：根据题型和数据特征推荐最佳图表类型。

用法：python recommend_chart.py --type 优化 --data-type 时序
      python recommend-chart.py --list  # 列出所有图表类型

输出：推荐结果 JSON + matplotlib 代码模板
"""
import argparse
import json
import sys

# 图表类型索引
CHART_TYPES = {
    # 对比类
    "分组柱状图": {"purpose": "对比", "data": "分类+数值", "code": "bar_grouped"},
    "雷达图": {"purpose": "对比", "data": "多维度评分", "code": "radar"},
    "排名图": {"purpose": "对比", "data": "排序数据", "code": "ranking"},
    # 分布类
    "直方图": {"purpose": "分布", "data": "单变量", "code": "histogram"},
    "箱线图": {"purpose": "分布", "data": "分组数值", "code": "boxplot"},
    " violin图": {"purpose": "分布", "data": "分组数值", "code": "violin"},
    "KDE图": {"purpose": "分布", "data": "连续变量", "code": "kde"},
    # 趋势类
    "折线图": {"purpose": "趋势", "data": "时序", "code": "line"},
    "面积图": {"purpose": "趋势", "data": "时序+堆叠", "code": "area"},
    # 相关类
    "散点图": {"purpose": "相关", "data": "双变量", "code": "scatter"},
    "散点矩阵": {"purpose": "相关", "data": "多变量", "code": "scatter_matrix"},
    "热力图": {"purpose": "相关", "data": "矩阵", "code": "heatmap"},
    # 组成类
    "饼图": {"purpose": "组成", "data": "比例", "code": "pie"},
    "堆叠柱状图": {"purpose": "组成", "data": "分类+堆叠", "code": "bar_stacked"},
    # 优化类
    "收敛曲线": {"purpose": "优化", "data": "迭代过程", "code": "convergence"},
    "3D曲面图": {"purpose": "优化", "data": "二元函数", "code": "surface_3d"},
    "等高线图": {"purpose": "优化", "data": "二元函数", "code": "contour"},
    "平行坐标图": {"purpose": "优化", "data": "多维参数", "code": "parallel"},
    # 图论类
    "网络拓扑图": {"purpose": "图论", "data": "节点+边", "code": "network"},
    "最短路径图": {"purpose": "图论", "data": "路径", "code": "shortest_path"},
    # 其他
    "拟合曲线": {"purpose": "预测", "data": "拟合结果", "code": "fit_curve"},
    "残差图": {"purpose": "预测", "data": "残差", "code": "residual"},
    "ROC曲线": {"purpose": "分类", "data": "分类结果", "code": "roc"},
    "混淆矩阵": {"purpose": "分类", "data": "分类结果", "code": "confusion"},
}

# 题型→图表推荐
TYPE_CHART_MAP = {
    "评价": ["雷达图", "热力图", "分组柱状图", "排名图"],
    "预测": ["拟合曲线", "残差图", "折线图", "散点图"],
    "优化": ["收敛曲线", "3D曲面图", "等高线图", "平行坐标图"],
    "分类": ["混淆矩阵", "ROC曲线", "散点矩阵", "特征重要性图"],
    "聚类": ["散点图", "轮廓系数图", "热力图"],
    "图论": ["网络拓扑图", "最短路径图", "热力图"],
    "仿真": ["折线图", "面积图", "散点图", "敏感性分析图"],
}

# matplotlib 代码模板
CODE_TEMPLATES = {
    "bar_grouped": '''import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(categories))
width = 0.35
ax.bar(x - width/2, values1, width, label='Group 1')
ax.bar(x + width/2, values2, width, label='Group 2')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.tight_layout()
plt.savefig('paper_output/figures/chart.png', dpi=300)
''',
    "radar": '''import numpy as np
import matplotlib.pyplot as plt

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
values = values.tolist() + [values[0]]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.plot(angles, values, 'o-', linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
plt.savefig('paper_output/figures/radar.png', dpi=300)
''',
    "heatmap": '''import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(data, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax)
ax.set_title('Heatmap')
plt.tight_layout()
plt.savefig('paper_output/figures/heatmap.png', dpi=300)
''',
    "line": '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, 'b-', linewidth=2, marker='o', markersize=4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paper_output/figures/line.png', dpi=300)
''',
    "scatter": '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x, y, c=colors, s=sizes, alpha=0.6)
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.colorbar(ax.collections[0], label='Color')
plt.tight_layout()
plt.savefig('paper_output/figures/scatter.png', dpi=300)
''',
    "boxplot": '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(data, labels=labels)
ax.set_ylabel('Value')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paper_output/figures/boxplot.png', dpi=300)
''',
    "convergence": '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(len(history)), history, 'b-', linewidth=2)
ax.set_xlabel('Iteration')
ax.set_ylabel('Objective Value')
ax.set_title('Convergence Curve')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paper_output/figures/convergence.png', dpi=300)
''',
    "surface_3d": '''import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.savefig('paper_output/figures/surface.png', dpi=300)
''',
}


def recommend(problem_type: str, data_type: str = None) -> dict:
    """根据题型推荐图表。"""
    # 匹配题型
    matched_type = None
    for key in TYPE_CHART_MAP:
        if key in problem_type or problem_type in key:
            matched_type = key
            break

    if not matched_type:
        matched_type = "优化"

    recommended = TYPE_CHART_MAP.get(matched_type, [])

    result = {
        "problem_type": matched_type,
        "recommended_charts": [],
    }

    for chart_name in recommended:
        chart_info = CHART_TYPES.get(chart_name, {})
        code_key = chart_info.get("code", "")
        code_template = CODE_TEMPLATES.get(code_key, "# Template not available")

        result["recommended_charts"].append({
            "name": chart_name,
            "purpose": chart_info.get("purpose", ""),
            "data_type": chart_info.get("data", ""),
            "code_template": code_template,
        })

    return result


def list_charts() -> dict:
    """列出所有图表类型。"""
    by_purpose = {}
    for name, info in CHART_TYPES.items():
        p = info["purpose"]
        if p not in by_purpose:
            by_purpose[p] = []
        by_purpose[p].append(name)
    return {"total": len(CHART_TYPES), "by_purpose": by_purpose}


def main():
    parser = argparse.ArgumentParser(description="Chart recommender")
    parser.add_argument('--type', default=None, help='Problem type')
    parser.add_argument('--data-type', default=None, help='Data type')
    parser.add_argument('--list', action='store_true', help='List all charts')
    args = parser.parse_args()

    if args.list:
        result = list_charts()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not args.type:
        print("Error: --type is required", file=sys.stderr)
        sys.exit(1)

    result = recommend(args.type, args.data_type)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
