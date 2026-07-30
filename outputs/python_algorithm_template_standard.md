# Python 算法模板工程化规范

> **v2.0 标准化 | 2026-05-31** | 统一索引见 `outputs/INDEX.md`

> 系统同步说明：本文件已纳入通用数学建模子生产系统。调用时默认遵循：任务路由 → 知识更新/资料入库 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 最终质量门 → 答辩/提交模板 → 经验回灌。涉及字段、参数或附件时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查 `outputs/final_quality_gate.md`；缺真实数据或运行结果时，统一标为【待补】，不得编造。

## 用途

用于把散装 Python 算法示例改造成比赛中可复制、可运行、可解释、可复现的模板。当前阶段不强行做完整 Python 包，优先建立统一代码结构和最小运行标准。

## 改造优先级

| 优先级 | 算法类型 | 代表方法 | 推荐原因 |
|---|---|---|---|
| P0 | 综合评价 | 熵权法、TOPSIS、AHP、灰色关联 | 国赛高频，容易形成表格和排序结果 |
| P0 | 数据预处理 | 缺失处理、异常检测、标准化、PCA | 所有题型都需要，能支撑后续模型 |
| P0 | 预测基线 | 移动平均、灰色预测、ARIMA、回归 | 能快速形成预测闭环和误差指标 |
| P1 | 机器学习预测 | 随机森林、XGBoost、LightGBM、SVR | 适合 C 题和大样本数据 |
| P1 | 优化规划 | 线性规划、整数规划、0-1 规划 | 方案输出清晰，论文表达稳定 |
| P1 | 智能优化 | GA、PSO、模拟退火、NSGA-II | 适合非凸、多目标和组合优化 |
| P2 | 仿真机理 | 蒙特卡洛、排队、微分方程、系统动力学 | 需要题目背景支撑，不能盲目套用 |
| P2 | 图论路径 | Dijkstra、Floyd、TSP、网络指标 | 适合路径、网络和调度类任务 |

## 标准文件结构

```text
code/
├── 01_prepare_inputs.py
├── 02_build_model.py
├── 03_solve_model.py
├── 04_analyze_results.py
├── 05_sensitivity_checks.py
├── utils.py
├── requirements.txt
└── README_reproduce.md
```

## 单文件模板结构

适合比赛临场快速提交时使用：

```text
main_model.py
├── 1. 参数区
├── 2. 数据读取与校验
├── 3. 数据预处理
├── 4. 模型函数
├── 5. 求解或训练
├── 6. 评价与检验
├── 7. 图表与结果导出
└── 8. 主函数入口
```

## 每个算法模板必须包含

| 模块 | 必须内容 | 检查标准 |
|---|---|---|
| 任务说明 | 适用题型、输入、输出、局限 | 读者能判断该不该用 |
| 参数区 | 文件路径、列名、模型参数、随机种子 | 不需要深入代码即可改参数 |
| 数据入口 | CSV/Excel 读取或样例数据生成 | 无真实数据时也能演示 |
| 输入校验 | 必要列、空值、维度、指标方向 | 错数据能尽早报清楚 |
| 核心函数 | 算法主体封装为函数 | 函数名表达用途 |
| 结果输出 | 表格、指标、排序、方案或预测值 | 能直接进入论文 |
| 可视化 | 至少一个服务结论的图或图表数据 | 不为装饰画图 |
| 复现说明 | 依赖、运行命令、输出文件 | 队友能独立运行 |
| 风险提示 | 适用边界、常见误用 | 避免论文中误写 |

## 推荐代码骨架

```python
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 42
INPUT_PATH = Path("data/input.csv")
OUTPUT_DIR = Path("outputs")

def load_data(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"找不到输入文件：{input_path}")
    data = pd.read_csv(input_path)
    if data.empty:
        raise ValueError("输入数据为空")
    return data

def validate_columns(data: pd.DataFrame, required_columns: list[str]) -> None:
    missing_columns = [column for column in required_columns if column not in data.columns]
    if missing_columns:
        raise ValueError(f"缺少必要字段：{missing_columns}")

def solve_model(data: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("在这里替换为具体算法")

def save_results(results: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "results.csv", index=False, encoding="utf-8-sig")

def main() -> None:
    data = load_data(INPUT_PATH)
    validate_columns(data, required_columns=[])
    results = solve_model(data)
    save_results(results, OUTPUT_DIR)

if __name__ == "__main__":
    np.random.seed(RANDOM_SEED)
    main()
```

## 题型专项输出标准

### 1. 综合评价类

必须输出：
- 指标方向表。
- 标准化后的指标矩阵。
- 权重表。
- 综合得分与排序表。
- 权重扰动或指标删减敏感性分析。

推荐文件：
- `indicator_weights.csv`
- `ranking_results.csv`
- `sensitivity_results.csv`

### 2. 预测类

必须输出：
- 训练集、验证集、测试集划分说明。
- 预测值与真实值对照表。
- MAE、RMSE、MAPE、R² 等误差指标。
- 预测曲线或残差图。

推荐文件：
- `prediction_results.csv`
- `metrics.csv`
- `residuals.csv`

### 3. 优化类

必须输出：
- 决策变量定义。
- 目标函数值。
- 约束满足检查表。
- 可执行方案表。
- 基准方案或参数扰动对比。

推荐文件：
- `decision_variables.csv`
- `objective_value.csv`
- `constraint_check.csv`
- `scenario_comparison.csv`

### 4. 聚类/分类类

必须输出：
- 特征列表和标准化说明。
- 类别标签或预测标签。
- 分类/聚类评估指标。
- 类群画像或重要特征解释。

推荐文件：
- `labels.csv`
- `cluster_profile.csv`
- `classification_metrics.csv`

### 5. 仿真与机理类

必须输出：
- 初始条件和参数表。
- 仿真轨迹或状态演化表。
- 多次重复结果或场景对比。
- 关键参数灵敏度结果。

推荐文件：
- `simulation_trace.csv`
- `scenario_results.csv`
- `parameter_sensitivity.csv`

## 依赖管理建议

| 场景 | 最小依赖 |
|---|---|
| 通用数据处理 | `numpy`, `pandas`, `matplotlib`, `openpyxl` |
| 机器学习 | `scikit-learn` |
| XGBoost/LightGBM | `xgboost`, `lightgbm` |
| 优化规划 | `scipy`, `pulp` 或 `ortools` |
| 时间序列 | `statsmodels` |
| 图论网络 | `networkx` |

## README_reproduce.md 最小内容

```markdown
# 复现说明

## 运行环境
- Python 版本：待补
- 依赖安装：`pip install -r requirements.txt`

## 输入文件
- `data/input.csv`：待补字段说明

## 运行命令
```bash
python main_model.py
```

## 输出文件
- `outputs/results.csv`：主结果表
- `outputs/metrics.csv`：评价指标表

## 待补说明
- 待补真实数据路径
- 待补字段映射
```

## 工程化检查清单

- [ ] 代码能在无真实数据时用样例数据演示，或明确说明缺少什么数据。
- [ ] 所有文件路径集中在参数区。
- [ ] 不硬编码用户本机绝对路径。
- [ ] 不把图表保存到混乱目录。
- [ ] 核心结果能直接对应论文中的表或图。
- [ ] 预测、分类、聚类任务有评价指标。
- [ ] 优化任务有约束检查。
- [ ] 随机算法设置随机种子。
- [ ] 输出 CSV 使用 `utf-8-sig`，方便 Excel 打开。
- [ ] README 写清运行方式和输出解释。

## 不建议做的事

- 不为每个小算法强行拆成复杂包结构。
- 不在比赛临场引入未经验证的大型框架。
- 不把多个无关算法塞进一个脚本。
- 不只输出图，不输出支撑图的数据表。
- 不用复杂模型替代必要的数据清洗和结果解释。
