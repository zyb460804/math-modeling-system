---
name: interactive-chart
description: 用 Plotly 生成交互式科学图表：3D曲面、平行坐标、动态时间线、等高线图。导出 HTML 可嵌入答辩。
---

# Interactive Chart — 交互式图表生成器

> **此 skill 是 `/figure` 统一入口的内部调度工具。** 用户说"交互式图表""3D图""动态图"等均由 `/figure` 统一接收后分派到本 skill。本 skill 保留独立触发词仅用于向后兼容。

用 Plotly 生成可交互的科学图表，支持缩放、悬停、筛选。

## 触发词

`交互式图表` `plotly` `3D图` `动态图` `可缩放图表` `HTML图表`

## 前置依赖

```bash
pip install plotly kaleido
```

## ★ 项目知识资产联动
本 skill 执行时，**必须**读取以下 `outputs/` 中已沉淀的规则：

| 资产 | 路径 | 用途 |
|------|------|------|
| 图表模板 | `outputs/figure_templates.md` | 图表类型选择标准 |
| 可视化策略 | `outputs/visualization_strategy_library.md` | 可视化方案库 |
| 科学图表参考 | `resources/14_科学计算参考/matplotlib/` | matplotlib 参考 |
| 图表教程 | `resources/06_图表教程/` | 炫酷图表教程 |

## 支持的图表类型

### 1. 3D 曲面图
适用：优化目标函数可视化、响应面分析

```python
import plotly.graph_objects as go
import numpy as np

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
fig.update_layout(title='目标函数响应面', scene=dict(
    xaxis_title='X₁', yaxis_title='X₂', zaxis_title='f(X₁, X₂)'))
fig.write_html('paper_output/figures/response_surface.html')
```

### 2. 平行坐标图
适用：多目标优化结果对比、多维度数据分析

```python
import plotly.express as px
import pandas as pd

df = pd.read_csv('paper_output/results/model_comparison.csv')
fig = px.parallel_coordinates(df, color='score',
    dimensions=['MAE', 'RMSE', 'R²', 'AIC'],
    color_continuous_scale=px.colors.diverging.Tealrose)
fig.write_html('paper_output/figures/parallel_coordinates.html')
```

### 3. 动态时间线
适用：时序预测对比、算法收敛过程

```python
import plotly.express as px
fig = px.line(df, x='time', y='value', color='model',
              animation_frame='iteration', title='预测对比')
fig.write_html('paper_output/figures/timeline_animation.html')
```

### 4. 等高线图
适用：约束优化可行域、损失函数地形

```python
import plotly.figure_factory as ff
fig = ff.create_annotated_heatmap(z=Z, x=list(x), y=list(y))
fig.write_html('paper_output/figures/contour.html')
```

### 5. 散点矩阵
适用：特征相关性探索、聚类结果可视化

```python
import plotly.express as px
fig = px.scatter_matrix(df, dimensions=['f1', 'f2', 'f3', 'f4'], color='cluster')
fig.write_html('paper_output/figures/scatter_matrix.html')
```

## 输出

- HTML 文件：`paper_output/figures/*.html`
- 静态 PNG（用于论文）：通过 `kaleido` 导出
- 嵌入答辩 PPT：使用 `<iframe>` 标签

## 约束

- 交互式图表仅用于探索和答辩，论文正文使用静态图
- 静态图导出使用 `fig.write_image('xxx.png', scale=3)`
- 配色与 matplotlib 图表保持一致