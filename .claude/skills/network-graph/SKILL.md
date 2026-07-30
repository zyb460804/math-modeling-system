---
name: network-graph
description: 图论/网络可视化：最短路径高亮、社区检测着色、交互式网络图（PyVis）、出版级静态图（NetworkX）。
---

# Network Graph — 网络/图论可视化

> **此 skill 是 `/figure` 统一入口的内部调度工具。** 用户说"网络图""图论""最短路径"等均由 `/figure` 统一接收后分派到本 skill。本 skill 保留独立触发词仅用于向后兼容。

数学建模 C 题图论问题的专用可视化工具。

## 触发词

`网络图` `图论` `最短路径` `节点图` `拓扑图` `关系图`

## ★ 项目知识资产联动
本 skill 执行时，**必须**读取以下 `outputs/` 中已沉淀的规则：

| 资产 | 路径 | 用途 |
|------|------|------|
| 图表模板 | `outputs/figure_templates.md` | 网络图模板 |
| 科学图表参考 | `resources/14_科学计算参考/networkx/` | NetworkX 参考 |
| 算法 cookbook | `resources/10_算法cookbook/cookbook-network.md` | 图论算法参考 |
| 图表教程 | `resources/06_图表教程/` | 炫酷图表教程 |

## 前置依赖

```bash
pip install networkx pyvis matplotlib
```

## 图表类型

### 1. 出版级静态网络图（NetworkX + matplotlib）

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [(1,2,3), (1,3,5), (2,3,2), (2,4,4), (3,4,1)]
for u, v, w in edges:
    G.add_edge(u, v, weight=w)

pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(10, 8))

# 节点
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='#4ECDC4', ax=ax)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax)

# 边
nx.draw_networkx_edges(G, pos, width=2, edge_color='#666666', ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12, ax=ax)

# 高亮最短路径
shortest_path = nx.shortest_path(G, 1, 4, weight='weight')
path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='red', ax=ax)

ax.set_title('最短路径分析', fontsize=16)
plt.savefig('paper_output/figures/network_shortest_path.png', dpi=300, bbox_inches='tight')
```

### 2. 交互式网络图（PyVis）

```python
from pyvis.network import Network

net = Network(height='600px', width='100%', notebook=True)
net.add_node(1, label='节点1', color='#4ECDC4')
net.add_node(2, label='节点2', color='#FF6B6B')
net.add_edge(1, 2, value=3, title='权重=3')
net.show('paper_output/figures/interactive_network.html')
```

### 3. 社区检测可视化

```python
import community as community_louvain

partition = community_louvain.best_partition(G)
colors = [partition[node] for node in G.nodes()]
nx.draw_networkx(G, pos, node_color=colors, cmap=plt.cm.Set3, 
                 node_size=700, with_labels=True)
```

### 4. 有向图

```python
DG = nx.DiGraph()
DG.add_edges_from([(1,2), (2,3), (3,1), (2,4)])
nx.draw(DG, with_labels=True, node_color='lightblue',
        arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.1')
```

### 5. 加权网络热力图

```python
import numpy as np
adj_matrix = nx.to_numpy_array(G)
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(adj_matrix, cmap='YlOrRd')
ax.set_xticks(range(len(G.nodes())))
ax.set_yticks(range(len(G.nodes())))
ax.set_xticklabels(list(G.nodes()))
ax.set_yticklabels(list(G.nodes()))
plt.colorbar(im)
plt.savefig('paper_output/figures/network_heatmap.png', dpi=300)
```

## 输出

- 静态图：`paper_output/figures/network_*.png`（论文用）
- 交互式：`paper_output/figures/interactive_network.html`（答辩用）
- 邻接矩阵：`paper_output/tables/adjacency_matrix.csv`

## 约束

- 节点数 ≤ 50 时用全连接图，> 50 时用子图或聚合
- 中文标签需要设置字体
- 最短路径必须高亮显示