# scikit-opt 启发式算法桥接指南

> 本文档是 `cookbook-optimization.md`（手写实现）的姊妹篇：cookbook 讲原理与可定制模板，本文档讲如何用成熟库 scikit-opt 一行调用拿 baseline 结果。

## 0. 一句话定位

**scikit-opt（sko）封装 7 种群体智能算法，一行调用即可求解，适合竞赛中快速出 baseline。** 安装：`pip install scikit-opt`。官方文档：<https://scikit-opt.github.io/> 。中文文档：<https://www.guofei.site/os/sko_zh.html> 。源码：<https://github.com/guofei9987/scikit-opt> 。

> 当前稳定版本 0.6.6（2024+）。以下 API 基于官方文档与作者笔记交叉确认；个别参数版本间有微调，若运行报错请以本地 `pip show scikit-opt` 版本为准。

---

## 1. 七种算法对照表

| 算法（中文） | sko 类名 | 导入语句 | 典型适用问题 | 关键参数 | 与 cookbook-optimization.md 手写版的关系 |
|---|---|---|---|---|---|
| 差分进化 (DE) | `DE` | `from sko.DE import DE` | 连续变量、高维、非凸优化；对参数敏感但收敛快 | `size_pop`, `max_iter`, `F`(变异系数), `prob_mut`, `lb/ub`, `constraint_eq/ueq` | **互补**。cookbook 无 DE 模板，scikit-opt 是首选；比 GA 在函数优化上更强 |
| 遗传算法 (GA) | `GA` / `GA_TSP` | `from sko.GA import GA` / `GA_TSP` | 连续/离散/组合优化；TSP 路径；曲线拟合 | `size_pop`, `max_iter`, `prob_mut`, `lb/ub`, `precision`(整数规划), `constraint_eq/ueq` | **可替代 baseline**。cookbook §1 提供手写 SBX/PMX 算子（可定制、可写进论文创新点），scikit-opt 提供标准实数/整数编码 GA |
| 粒子群 (PSO) | `PSO` | `from sko.PSO import PSO` | 连续变量、多峰、不可微目标；收敛快 | `pop`(注意非 `size_pop`), `max_iter`, `w`(惯性), `c1/c2`(个体/社会), `lb/ub`, `constraint_ueq` | **可替代 baseline**。cookbook §2 提供手写 PSO（可监控每个粒子状态），scikit-opt 一行出结果 |
| 模拟退火 (SA) | `SA` / `SAFast` / `SABoltzmann` / `SACauchy` / `SA_TSP` | `from sko.SA import SA` | 组合优化、TSP、跳出局部最优；`SA` 默认等同 `SAFast` | `x0`(初始点), `T_max`, `T_min`, `L`(链长), `max_stay_counter`, `lb/ub` | **互补**。cookbook §3 讲 SA 原理与冷却调度；`resources/04_代码模板/Python/optimization/sa_geodesic.py` 是大地距离专用手写实现（scikit-opt 无此专用变体，需自定义邻域函数） |
| 蚁群 (ACA) | `ACA_TSP` | `from sko.ACA import ACA_TSP` | **仅 TSP / 路径优化**（scikit-opt 未提供通用连续 ACA） | `size_pop`(蚂蚁数), `max_iter`, `distance_matrix`, `alpha`(信息素), `beta`(能见度), `rho`(挥发) | **专用替代**。cookbook 无 ACA 模板，TSP 问题首选 scikit-opt |
| 免疫算法 (IA) | `IA_TSP` | `from sko.IA import IA_TSP` | **仅 TSP / 路径优化**（scikit-opt 未提供通用连续 IA） | `size_pop`, `max_iter`, `prob_mut`, `T`(亲和度阈值), `alpha`(多样性评价) | **专用替代**。cookbook 无 IA 模板，TSP 问题可用 |
| 人工鱼群 (AFSA) | `AFSA` | `from sko.AFSA import AFSA` | 连续变量、多目标、并行性好的问题 | `size_pop`, `max_iter`, `max_try_num`(捕食尝试), `step`, `visual`(感知范围), `q`, `delta`(拥挤度) | **互补**。cookbook 无 AFSA 模板；注：任务单中"AFO"即指此算法，scikit-opt 实际类名为 `AFSA`（Artificial Fish-Swarm Algorithm），无 `AFO`/`AF` 类名 |

### 重要 API 注意事项

1. **PSO 用 `pop` 不是 `size_pop`**：PSO 类的种群参数历史版本间不一致，作者笔记与多数教程代码示例用 `pop=40`，但官方文档表格写作 `size_pop=50`。实际运行以源码为准——若报参数错误，尝试切换 `pop` ↔ `size_pop`（需查本地版本确认）。
2. **ACA / IA 仅有 TSP 版本**：scikit-opt 的蚁群和免疫算法**只封装了 `ACA_TSP` 和 `IA_TSP`**，没有通用连续优化版本。连续优化请用 DE/GA/PSO/AFSA。
3. **SA 的三个变体**：`SA`（默认 Fast）、`SACauchy`（柯西分布，跳出局部最优更强）、`SABoltzmann`（玻尔兹曼分布，收敛更稳）。TSP 用 `SA_TSP`。
4. **GA 整数规划**：`precision` 参数设为整数（如 `precision=[1, 2, 1e-7]`）即可激活整数规划模式，对应维度变量取整数。
5. **约束写法**：`constraint_eq` 为等式约束列表（`lambda x: 1 - x[0] - x[1]`），`constraint_ueq` 为不等式约束列表（形式为 `<= 0`，如 `lambda x: x[0] + x[1] - 5` 表示 `x0+x1<=5`）。
6. **结果属性差异**：GA/DE 用 `best_x, best_y = algo.run()` + `generation_best_Y`；PSO 用 `algo.run()` 后取 `algo.gbest_x, algo.gbest_y, algo.gbest_y_hist`；SA 用 `best_x, best_y = algo.run()` + `algo.best_y_history`。

---

## 2. 最小可运行示例（7 种算法各一段）

> 以下示例使用 stdlib + numpy + scikit-opt，目标函数统一为 `f(x) = x1² + (x2-0.01)² + x3²`（三维，全局最优在原点附近）。`pip install scikit-opt numpy` 后即可运行。

### 2.1 差分进化 (DE)

```python
import numpy as np
from sko.DE import DE

def obj_func(x):
    x1, x2, x3 = x
    return x1 ** 2 + (x2 - 0.01) ** 2 + x3 ** 2

de = DE(func=obj_func, n_dim=3, size_pop=50, max_iter=200,
        F=0.5, prob_mut=0.001, lb=[-1, -1, -1], ub=[1, 1, 1])
best_x, best_y = de.run()
print('DE best_x:', best_x, 'best_y:', best_y)
# 每代最优: de.generation_best_X, de.generation_best_Y
```

### 2.2 遗传算法 (GA)

```python
import numpy as np
from sko.GA import GA

def schaffer(p):
    x1, x2 = p
    x = np.square(x1) + np.square(x2)
    return 0.5 + (np.square(np.sin(x)) - 0.5) / np.square(1 + 0.001 * x)

ga = GA(func=schaffer, n_dim=2, size_pop=30, max_iter=100,
        prob_mut=0.001, lb=[-1, -1], ub=[1, 1], precision=1e-7)
best_x, best_y = ga.run()
print('GA best_x:', best_x, 'best_y:', best_y)
# 每代最优: ga.generation_best_X, ga.generation_best_Y
```

### 2.3 粒子群 (PSO)

```python
from sko.PSO import PSO

def demo_func(x):
    x1, x2, x3 = x
    return x1 ** 2 + (x2 - 0.01) ** 2 + x3 ** 2

# 注意: PSO 用 pop（不是 size_pop）；若报错尝试切换参数名（需查文档确认）
pso = PSO(func=demo_func, n_dim=3, pop=40, max_iter=150,
          lb=[0, -1, 0.2], ub=[1, 1, 1], w=0.8, c1=0.5, c2=0.5)
pso.run()
print('PSO best_x:', pso.gbest_x, 'best_y:', pso.gbest_y)
# 收敛历史: pso.gbest_y_hist
```

### 2.4 模拟退火 (SA)

```python
from sko.SA import SA

demo_func = lambda x: x[0] ** 2 + (x[1] - 0.02) ** 2 + x[2] ** 2

sa = SA(func=demo_func, x0=[1, 1, 1], T_max=1, T_min=1e-9,
        L=300, max_stay_counter=10)
best_x, best_y = sa.run()
print('SA best_x:', best_x, 'best_y:', best_y)
# 退火历史: sa.best_y_history
# 变体: from sko.SA import SAFast, SACauchy, SABoltzmann
```

### 2.5 蚁群算法 (ACA_TSP，仅 TSP)

```python
import numpy as np
from scipy import spatial
from sko.ACA import ACA_TSP

num_points = 20
points = np.random.rand(num_points, 2)
dist_mat = spatial.distance.cdist(points, points, metric='euclidean')

def total_dist(routine):
    n, = routine.shape
    return sum(dist_mat[routine[i % n], routine[(i + 1) % n]] for i in range(n))

aca = ACA_TSP(func=total_dist, n_dim=num_points, size_pop=50,
              max_iter=200, distance_matrix=dist_mat,
              alpha=1, beta=2, rho=0.1)
best_x, best_y = aca.run()
print('ACA best route:', best_x, 'distance:', best_y)
```

### 2.6 免疫算法 (IA_TSP，仅 TSP)

```python
import numpy as np
from scipy import spatial
from sko.IA import IA_TSP

num_points = 12
points = np.random.rand(num_points, 2)
dist_mat = spatial.distance.cdist(points, points, metric='euclidean')

def total_dist(routine):
    n, = routine.shape
    return sum(dist_mat[routine[i % n], routine[(i + 1) % n]] for i in range(n))

ia = IA_TSP(func=total_dist, n_dim=num_points, size_pop=500, max_iter=800,
            prob_mut=0.2, T=0.7, alpha=0.95)
best_x, best_y = ia.run()
print('IA best route:', best_x, 'distance:', best_y)
```

### 2.7 人工鱼群 (AFSA)

```python
from sko.AFSA import AFSA

def func(x):
    x1, x2, x3 = x
    return (x1 - x2) ** 2 + (x2 - 0.01) ** 2 + x3 ** 2

afsa = AFSA(func, n_dim=3, size_pop=50, max_iter=100,
            max_try_num=100, step=0.5, visual=0.3, q=0.98, delta=0.5)
best_x, best_y = afsa.run()
print('AFSA best_x:', best_x, 'best_y:', best_y)
```

---

## 3. 选型建议：何时用 scikit-opt，何时手写

### 3.1 优先用 scikit-opt 的场景

| 场景 | 理由 |
|---|---|
| **竞赛时间紧，需要快速 baseline** | 一行调用拿到参考解，验证目标函数正确性、确定结果量级 |
| **该算法非论文核心创新点** | 例如论文主模型是机理建模，GA 只是参数标定的辅助手段，用 scikit-opt 即可 |
| **需要对比多种启发式算法选最优** | 7 种算法 API 统一，便于横向对比（DE vs GA vs PSO vs AFSA） |
| **TSP / 路径优化问题** | scikit-opt 的 `GA_TSP` / `ACA_TSP` / `IA_TSP` / `SA_TSP` 开箱即用 |
| **整数规划 / 约束优化** | GA 的 `precision` 参数支持整数规划；`constraint_eq/ueq` 支持非线性约束 |

### 3.2 优先手写的场景

| 场景 | 理由 |
|---|---|
| **算法本身是论文创新点** | 如"改进遗传算法（自适应交叉概率 + 模因局部搜索）"——评委要看算子设计，scikit-opt 的黑盒无法体现创新 |
| **需要自定义算子** | 如排列编码的 PMX/OX 交叉、多目标支配排序（NSGA-II 的非支配排序和拥挤度距离）、自适应变异 |
| **需要精确控制每一步** | 如记录每代种群多样性格式做收敛性分析、嵌入问题特定的修复策略、动态调整罚因子 |
| **多目标优化** | scikit-opt 不支持 Pareto 前沿；用 `resources/04_代码模板/Python/optimization/nsga2_multi_obj.py`（NSGA-II）手写 |
| **鲁棒优化** | scikit-opt 不支持 CVaR 约束；用 `resources/04_代码模板/Python/optimization/cvar_robust.py` 手写 |
| **非标准距离定义** | 如大地距离（椭球面）、路网距离；用 `resources/04_代码模板/Python/optimization/sa_geodesic.py` 手写 SA |

### 3.3 决策流程

```
该启发式算法是论文创新点吗？
├── 是 → 手写（cookbook-optimization.md + resources/04_代码模板/）
│        理由：需自定义算子、展示算法设计、评委要看实现细节
└── 否 → 该算法是通用 baseline 吗？
    ├── 是 → scikit-opt（本文档）
    │        理由：一行调用、社区维护、质量有保障
    └── 需要特殊变体（NSGA-II / CVaR / 大地距离 SA）
         → 手写（resources/04_代码模板/Python/optimization/）
```

---

## 4. 与 cookbook-optimization.md 的分工

| 维度 | cookbook-optimization.md | heuristic-algo-scikit-opt.md（本文档） |
|---|---|---|
| **定位** | 原理讲解 + 可定制手写模板 | 成熟库的快速调用指南 |
| **内容** | GA / PSO / SA / LP / IP / DP 的适用场景判断、核心公式、设计决策、收敛诊断、Python/MATLAB 模板路径 | 7 种算法的 sko API、最小示例、选型决策、与手写版的互补关系 |
| **代码风格** | 手写实现（可见每一步逻辑） | 库调用（一行出结果） |
| **适用阶段** | 模型设计阶段（理解原理、选择编码方式、设计算子） | 代码实现阶段（快速出 baseline、对比算法、验证目标函数） |
| **论文创新** | 可作为创新点写入论文（自定义算子、改进策略） | 仅作为 baseline，论文中写"使用 scikit-opt 库实现标准 GA" |
| **互补场景** | cookbook §1 GA 手写（SBX/PMX）↔ scikit-opt GA（标准实数编码）；cookbook §2 PSO 手写 ↔ scikit-opt PSO；cookbook §3 SA 原理 ↔ scikit-opt SA（3 种变体） | — |

### 与 resources/04_代码模板/Python/optimization/ 的关系

| 手写代码模板 | scikit-opt 对应 | 关系 |
|---|---|---|
| `nsga2_multi_obj.py`（NSGA-II 多目标） | scikit-opt 无多目标算法 | **手写专用**。Pareto 前沿必须手写 |
| `cvar_robust.py`（CVaR 鲁棒优化） | scikit-opt 无鲁棒优化 | **手写专用**。CVaR 约束必须手写 |
| `sa_geodesic.py`（SA 大地距离） | `sko.SA.SA`（通用 SA） | **互补**。通用 SA 用 scikit-opt；大地距离等非欧距离需自定义邻域函数，手写更灵活 |
| `system_dynamics.py`（系统动力学） | scikit-opt 无系统动力学 | **手写专用**。不属于群体智能范畴 |

---

## 5. 常见陷阱

1. **PSO 参数名**：`pop` vs `size_pop` 版本间不一致，报参数错误时优先尝试切换（需查本地版本确认）。
2. **ACA_TSP 的 numpy 兼容性**：旧版 scikit-opt 的 `ACA_TSP` 内部用了 `np.int`（NumPy≥1.24 已移除），运行报错时需将源码中 `np.int` 改为 `np.int32`（或升级 scikit-opt 到已修复版本）。
3. **约束格式**：`constraint_ueq` 必须是 `<= 0` 形式。例如 `x0 + x1 <= 5` 写作 `lambda x: x[0] + x[1] - 5`，符号写反会导致约束失效。
4. **目标函数最小化**：scikit-opt 所有算法默认最小化。最大化问题取负：`lambda x: -original_func(x)`。
5. **GA 整数规划**：`precision` 设为整数（如 `precision=[1, 2, 1e-7]`）激活整数模式；建议变量取值数为 $2^n$ 以保证收敛效果。
6. **SA 初始点 `x0`**：SA 需要提供初始点，与 GA/DE/PSO（只需边界）不同；初始点远离最优会显著影响收敛速度。

---

## 6. 参考来源

- scikit-opt 官方文档：<https://scikit-opt.github.io/>
- scikit-opt GitHub：<https://github.com/guofei9987/scikit-opt>
- 作者笔记（中文）：<https://www.guofei.site/os/sko_zh.html>
- scikit-opt 使用指北（中文详解）：<https://www.cnblogs.com/luohenyueji/p/18333387>
- PyPI：<https://pypi.org/project/scikit-opt/>
