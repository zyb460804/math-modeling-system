# 图论与网络算法手册

覆盖：网络流、最短路径、二分图匹配、中心性分析、K-Shell 分解、多层网络

---

## 1. 有向图网络流（水资源/基础设施类）

### 适用场景
- 水资源调度（流域、水库群）、电网潮流分配、供应链物流
- 节点间存在物理流（水/电/货）的单向传递系统

### 问题适配框架

| 图要素 | 问题映射 | 设计要点 |
|--------|---------|---------|
| 节点 V | 湖/水库/站点/仓库 | 每个节点需定义容量上限和初始状态 |
| 边 E | 连接水道/线路/运输路径 | 方向由高到低或由供到需 |
| 边权重 | 流量 Q / 运输量 | 受物理约束（管道容量、道路限行） |
| 源点 | 系统入口（上游水库/工厂） | 可多个源点 |
| 汇点 | 系统出口（下游/消费者） | 可多个汇点 |

### 质量守恒约束（核心公式）

对于任意非源非汇节点 v：
$$\sum_{(u,v)\in E} Q_{in}(u,v) = \sum_{(v,w)\in E} Q_{out}(v,w)$$

### 求解框架

**单目标**：最大流（Ford-Fulkerson / Edmonds-Karp）、最小费用流
**多目标**：NSGA-II，决策变量 = 各边流量 Q，目标 = 各利益方收益/成本函数

---

## 2. 最短路径与混合路径规划（交通网络类）

### A*-GA 混合路径规划

```
Algorithm: A*-GA Hybrid Path Planning
Input: 路网 G=(V,E), 边权重 w(u,v), 起点s, 终点t
Output: 最优路径 P*

1. 用改进 A* 生成 k 条初始路径（作为 GA 初始种群）
2. for generation = 1 to 100:
3.     select parents by tournament
4.     crossover(path1, path2) → 交换一段子路径
5.     if random < 0.05: mutation → 随机替换一个中间节点
6.     fitness = 1 / total_weight(path)
7. return best_path
```

### Dijkstra 多源多点

```python
import networkx as nx
G = nx.Graph()
G.add_weighted_edges_from([(u, v, w) for u, v, w in edges])
distances = nx.single_source_dijkstra_path_length(G, source)
all_pairs = dict(nx.all_pairs_dijkstra_path_length(G))
```

---

## 3. 中心性分析与关键节点识别

| 指标 | 公式 | 含义 | 适用场景 |
|------|------|------|---------|
| Degree Centrality | $C_D(v)=deg(v)/(N-1)$ | 节点直接连接的边数 | 局部重要性 |
| Closeness Centrality | $C_C(v)=(N-1)/\sum d(v,t)$ | 节点到所有其他节点的平均最短距离的倒数 | 传播效率 |
| Betweenness Centrality | $C_B(v)=\sum_{s\neq v\neq t}\frac{\sigma_{st}(v)}{\sigma_{st}}$ | 节点出现在最短路径中的频率 | 枢纽识别 |

---

## 4. 二分图匹配（匈牙利算法）

### 适用场景
- 任务分配（工人→任务、设备→工序）
- 资源配对问题

```python
from scipy.optimize import linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(cost_matrix)
```

---

## 5. 多层网络模型

### 适用场景
- 城市交通（公路+公交+轨道层次）
- 供应链多层网络（供应商→制造商→分销商→零售商）
- 基础设施耦合系统（电力+通信+交通）

### 关键分析维度
- **层内分析**：每层独立的最短路径、中心性、连通分量
- **层间耦合**：层间边的权重反映模式转换成本
- **级联失效**：删除一个节点，观察跨层传播的影响范围

---

## 6. 常见陷阱

| 陷阱 | 正确做法 |
|------|---------|
| 节点太多导致图密集不可读 | 先聚合（如区域级而非站点级），图节点<50 |
| 只跑最短路不给对比 | 报告至少2条备选路径及各自的 cost |
| 网络流无守恒检验 | 每个节点入流=出流，输出检验表 |
| K-Shell 层数随意定 | 用分数分布的自然断点确定层界 |
