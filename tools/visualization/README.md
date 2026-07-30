# 可视化工具（Visualization）

> **版本**: v1.0 | **更新**: 2026-06-21
> **用途**: 交互式图表、科学图表、仪表板

---

## 工具清单

### 1. interactive_chart.py - 交互式图表

**功能**: 使用Plotly创建交互式图表

**图表类型**:
- 散点图
- 折线图
- 柱状图
- 热力图
- 3D曲面图
- 平行坐标图

**用法**:
```bash
python tools/visualization/scripts/interactive_chart.py \
  --data paper_output/data_cleaned/data.csv \
  --type scatter \
  --x column1 \
  --y column2 \
  --output paper_output/figures/interactive_scatter.html
```

**参数**:
- `--data`: 数据文件路径
- `--type`: 图表类型
- `--x`: X轴列名
- `--y`: Y轴列名
- `--color`: 颜色列名
- `--output`: 输出文件路径

### 2. scientific_figure.py - 科学图表

**功能**: 创建出版级科学图表

**图表类型**:
- 多面板图
- 误差棒图
- 热力图
- 等高线图
- 向量场图

**用法**:
```bash
python tools/visualization/scripts/scientific_figure.py \
  --data paper_output/data_cleaned/data.csv \
  --type multi_panel \
  --panels 2x2 \
  --output paper_output/figures/scientific_figure.png
```

### 3. dashboard.py - 仪表板

**功能**: 创建交互式数据仪表板

**用法**:
```bash
python tools/visualization/scripts/dashboard.py \
  --data paper_output/data_cleaned/data.csv \
  --port 8050
```

---

## 依赖

```bash
pip install plotly dash matplotlib seaborn
```

---

## 示例

### 散点图

```python
import plotly.express as px
import pandas as pd

df = pd.read_csv("data.csv")
fig = px.scatter(df, x="column1", y="column2", color="category")
fig.show()
```

### 热力图

```python
import plotly.express as px
import pandas as pd

df = pd.read_csv("data.csv")
fig = px.imshow(df.corr())
fig.show()
```

### 3D曲面图

```python
import plotly.graph_objects as go
import numpy as np

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
fig.show()
```

---

## 版本历史

- v1.0.0 (2026-06-21): 初始版本
