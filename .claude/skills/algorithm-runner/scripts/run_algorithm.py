"""算法执行脚本：匹配算法模板，适配数据，执行，输出结果。

用法：python run_algorithm.py --algorithm 熵权TOPSIS --data data.csv
      python run_algorithm.py --list  # 列出所有可用算法

输出：执行结果 JSON
"""
import argparse
import json
import os
import sys
import subprocess
from pathlib import Path

# 算法模板索引
ALGORITHM_INDEX = {
    # 评价类
    "熵权TOPSIS": {"path": "resources/04_代码模板/50多种常用算法源代码/熵权TOPSIS/", "type": "评价", "lang": "python"},
    "AHP": {"path": "resources/04_代码模板/50多种常用算法源代码/AHP/", "type": "评价", "lang": "python"},
    "模糊综合评价": {"path": "resources/04_代码模板/50多种常用算法源代码/模糊综合评价/", "type": "评价", "lang": "python"},
    "DEA": {"path": "resources/04_代码模板/50多种常用算法源代码/DEA/", "type": "评价", "lang": "python"},
    "灰色关联分析": {"path": "resources/04_代码模板/50多种常用算法源代码/灰色关联分析/", "type": "评价", "lang": "python"},
    # 预测类
    "ARIMA": {"path": "resources/04_代码模板/50多种常用算法源代码/ARIMA/", "type": "预测", "lang": "python"},
    "灰色预测": {"path": "resources/04_代码模板/50多种常用算法源代码/灰色预测/", "type": "预测", "lang": "python"},
    "LSTM": {"path": "resources/04_代码模板/50多种常用算法源代码/LSTM/", "type": "预测", "lang": "python"},
    "Prophet": {"path": "resources/04_代码模板/14种国赛必备算法源代码/Prophet.py", "type": "预测", "lang": "python"},
    "XGBoost": {"path": "resources/04_代码模板/14种国赛必备算法源代码/XGBoost.py", "type": "预测", "lang": "python"},
    "LightGBM": {"path": "resources/04_代码模板/14种国赛必备算法源代码/LightGBM.py", "type": "预测", "lang": "python"},
    # 优化类
    "线性规划": {"path": "resources/04_代码模板/50多种常用算法源代码/线性规划/", "type": "优化", "lang": "python"},
    "整数规划": {"path": "resources/04_代码模板/50多种常用算法源代码/整数规划/", "type": "优化", "lang": "python"},
    "遗传算法": {"path": "resources/04_代码模板/14种国赛必备算法源代码/遗传算法.py", "type": "优化", "lang": "python"},
    "粒子群算法": {"path": "resources/04_代码模板/14种国赛必备算法源代码/粒子群算法.py", "type": "优化", "lang": "python"},
    "模拟退火": {"path": "resources/04_代码模板/50多种常用算法源代码/模拟退火/", "type": "优化", "lang": "python"},
    "NSGA-II": {"path": "resources/04_代码模板/14种国赛必备算法源代码/NSGA-II.py", "type": "优化", "lang": "python"},
    # 分类/聚类
    "随机森林": {"path": "resources/04_代码模板/14种国赛必备算法源代码/随机森林.py", "type": "分类", "lang": "python"},
    "K-means": {"path": "resources/04_代码模板/50多种常用算法源代码/K-means/", "type": "聚类", "lang": "python"},
    "DBSCAN": {"path": "resources/04_代码模板/50多种常用算法源代码/DBSCAN/", "type": "聚类", "lang": "python"},
    # 图论
    "Dijkstra": {"path": "resources/04_代码模板/50多种常用算法源代码/Dijkstra/", "type": "图论", "lang": "python"},
    "Floyd": {"path": "resources/04_代码模板/50多种常用算法源代码/Floyd/", "type": "图论", "lang": "python"},
    # 仿真
    "蒙特卡洛": {"path": "resources/04_代码模板/50多种常用算法源代码/蒙特卡洛/", "type": "仿真", "lang": "python"},
    "排队论": {"path": "resources/04_代码模板/50多种常用算法源代码/排队论/", "type": "仿真", "lang": "python"},
    "PCA": {"path": "resources/04_代码模板/14种国赛必备算法源代码/PCA.py", "type": "降维", "lang": "python"},
    "TOPSIS": {"path": "resources/04_代码模板/50多种常用算法源代码/TOPSIS/", "type": "评价", "lang": "python"},
    "熵权法": {"path": "resources/04_代码模板/50多种常用算法源代码/熵权法/", "type": "评价", "lang": "python"},
}


def list_algorithms() -> dict:
    """列出所有可用算法。"""
    by_type = {}
    for name, info in ALGORITHM_INDEX.items():
        t = info["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(name)
    return {"total": len(ALGORITHM_INDEX), "by_type": by_type}


def find_algorithm(name: str) -> dict:
    """查找算法模板。"""
    # 精确匹配
    if name in ALGORITHM_INDEX:
        return {"name": name, **ALGORITHM_INDEX[name]}

    # 模糊匹配
    for key in ALGORITHM_INDEX:
        if name in key or key in name:
            return {"name": key, **ALGORITHM_INDEX[key]}

    return None


def run_algorithm(algo_info: dict, data_path: str = None) -> dict:
    """执行算法。"""
    base_dir = "e:/数学建模"
    algo_path = os.path.join(base_dir, algo_info["path"])

    if not os.path.exists(algo_path):
        return {"status": "error", "message": f"Algorithm path not found: {algo_path}"}

    # 查找 Python 脚本
    if algo_path.endswith(".py"):
        script_path = algo_path
    else:
        # 在目录中找 .py 文件
        py_files = [f for f in os.listdir(algo_path) if f.endswith(".py")]
        if not py_files:
            return {"status": "error", "message": f"No Python files found in {algo_path}"}
        script_path = os.path.join(algo_path, py_files[0])

    # 执行
    try:
        cmd = [sys.executable, script_path]
        if data_path:
            cmd.extend(["--data", data_path])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=base_dir,
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "algorithm": algo_info.get("name", "unknown"),
            "script": script_path,
            "returncode": result.returncode,
            "stdout": result.stdout[:2000],
            "stderr": result.stderr[:1000],
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Algorithm execution timed out (120s)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Algorithm runner")
    parser.add_argument('--algorithm', default=None, help='Algorithm name')
    parser.add_argument('--data', default=None, help='Data file path')
    parser.add_argument('--list', action='store_true', help='List all algorithms')
    args = parser.parse_args()

    if args.list:
        result = list_algorithms()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not args.algorithm:
        print("Error: --algorithm is required", file=sys.stderr)
        sys.exit(1)

    algo = find_algorithm(args.algorithm)
    if not algo:
        print(f"Error: Algorithm '{args.algorithm}' not found", file=sys.stderr)
        sys.exit(1)

    result = run_algorithm(algo, args.data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
