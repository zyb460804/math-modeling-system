---
name: math-figure
description: "数学建模专用数学图表：函数图像、几何示意图、向量场、概率分布、等高线+3D曲面对照。含render_check质量检查。触发词：数学图表、函数图、几何示意图、向量场、等高线、3D曲面、math figure、render_check、概率分布。"
---

# Math Figure — 数学图表生成器（含render_check）

> **此 skill 是 `/figure` 统一入口的内部调度工具。** 用户说"函数图""数学图像""等高线"等均由 `/figure` 统一接收后分派到本 skill。本 skill 保留独立触发词仅用于向后兼容。

> **v3.6 更新**：新增render_check质量检查机制，每个图表必须通过质量检查才能用于论文。

## 设计理念

> "Each must pass render_check_and_log() before it can be designated a paper figure."

本skill的核心改进：
- 每个图表生成后必须运行**render_check**
- 检查**文字重叠**、**超出画布**、**字体过小**等问题
- 质量检查报告落盘到 `paper_output/qa/`
- 不合格图表必须修复后重新检查

## ★ figqa 图表碰撞门（v4.1 融合自 sweetcornna/mathodology）

> render_check 查源图质量；figqa 进一步做 **bbox 碰撞门**——任何文字/标注/图例与数据元素重叠、或元素被裁剪，**直接失败中断 run**。这是 mathodology 的独门武器：源图"看着没问题"，排版阶段一个数字/字体改动就会让手放标注撞上数据。

### 三件套脚本（已复制到 `scripts/`）
| 脚本 | 来源 | 作用 | 依赖 |
|---|---|---|---|
| `scripts/figqa.py` | mathodology | matplotlib bbox 碰撞门；可 import (`from figqa import assert_no_overlap`) 也可 CLI；`--self-test` 自测 | matplotlib |
| `scripts/pdf_qa.sh` | mathodology | **编译后 PDF** 的页数/匿名/重复 `Figure N:` 标注/空白页检查 | poppler-utils |
| `scripts/make_contact_sheet.py` | mathodology | **从编译 PDF（非源图）** 建 contact sheet 用于图表 QA | poppler-utils + matplotlib |

### 关键纪律
- **contact sheet 必须从编译后 PDF 构建**，不从源图——只有编译后的 contact sheet 能抓到排版阶段的裁剪/缩放缺陷
- 图表工厂里接 `assert_no_overlap(fig)`，让任何重叠**失败 run** 而非"看着没问题"
- 视觉"looks fine" 通过源图 contact sheet 不算数；必须零碰撞退出 + 编译 PDF 的干净 pdf_qa 报告
- 提交前把 `figqa.py` 复制进赛题代码目录，让提交包脱离 skill 也能重跑碰撞门

### 使用
```bash
# 自测
python .claude/skills/math-figure/scripts/figqa.py --self-test
# 检查编译后 PDF（提交前必跑）
bash .claude/skills/math-figure/scripts/pdf_qa.sh paper_output/final_paper.pdf --max-pages 25 --anonymous
# 从编译 PDF 建 contact sheet
python .claude/skills/math-figure/scripts/make_contact_sheet.py paper_output/final_paper.pdf -o paper_output/qa/contact_sheet.png
```

### 与 render_check 的分工
| 检查 | render_check | figqa/pdf_qa |
|---|---|---|
| DPI/字体/尺寸 | ✅ 源图 | — |
| 文字重叠比例 | ✅ ≤5% | ✅ bbox 零碰撞（更严）|
| 编译后排版缺陷 | ❌ | ✅ 从 PDF 建 contact sheet |
| 匿名/页数/重复标注 | ❌ | ✅ pdf_qa |

**两者都过才算图表门禁绿。**

生成数学建模论文中需要的数学类图表。

## 触发词

`函数图` `数学图像` `几何图` `概率分布` `向量场` `等高线`

## ★ 项目知识资产联动
本 skill 执行时，**必须**读取以下 `outputs/` 中已沉淀的规则：

| 资产 | 路径 | 用途 |
|------|------|------|
| 图表模板 | `outputs/figure_templates.md` | 数学图表模板 |
| 科学图表参考 | `resources/14_科学计算参考/matplotlib/` | matplotlib 参考 |
| 图表教程 | `resources/06_图表教程/` | 炫酷图表教程 |

## 图表类型

### 1. 函数图像
适用：展示目标函数、损失函数、激活函数

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 1000)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Sigmoid
axes[0].plot(x, 1/(1+np.exp(-x)), 'b-', lw=2)
axes[0].set_title('Sigmoid', fontsize=14)
axes[0].grid(True, alpha=0.3)

# ReLU
axes[1].plot(x, np.maximum(0, x), 'r-', lw=2)
axes[1].set_title('ReLU', fontsize=14)
axes[1].grid(True, alpha=0.3)

# Tanh
axes[2].plot(x, np.tanh(x), 'g-', lw=2)
axes[2].set_title('Tanh', fontsize=14)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('paper_output/figures/activation_functions.png', dpi=300)
```

### 2. 概率分布图
适用：展示数据分布、贝叶斯先验/后验

```python
from scipy import stats
x = np.linspace(-4, 4, 1000)
fig, ax = plt.subplots(figsize=(8, 5))
for mu, sigma, color in [(0,1,'blue'), (0,0.5,'red'), (1,1,'green')]:
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color=color, lw=2,
            label=f'μ={mu}, σ={sigma}')
ax.fill_between(x, stats.norm.pdf(x, 0, 1), alpha=0.1)
ax.legend(fontsize=12)
ax.set_title('正态分布', fontsize=14)
plt.savefig('paper_output/figures/normal_distributions.png', dpi=300)
```

### 3. 等高线 + 3D 曲面对照
适用：优化问题的目标函数可视化

```python
from mpl_toolkits.mplot3d import Axes3D
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2  # 目标函数

fig = plt.figure(figsize=(14, 5))
# 左：等高线
ax1 = fig.add_subplot(121)
cs = ax1.contourf(X, Y, Z, levels=20, cmap='viridis')
ax1.set_title('等高线图')
plt.colorbar(cs)
# 右：3D曲面
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax2.set_title('3D曲面图')
plt.savefig('paper_output/figures/contour_3d.png', dpi=300)
```

### 4. 几何示意图
适用：可行域、约束区域、凸包

```python
import matplotlib.patches as patches
fig, ax = plt.subplots(figsize=(8, 8))
# 可行域
feasible = plt.Polygon([[0,0], [4,0], [3,3], [0,4]], alpha=0.3, color='green', label='可行域')
ax.add_patch(feasible)
# 等高线
ax.contour(X, Y, Z, levels=10, cmap='coolwarm')
# 最优解
ax.plot(1, 2, 'r*', markersize=20, label='最优解')
ax.legend()
ax.set_title('约束优化可行域')
plt.savefig('paper_output/figures/feasible_region.png', dpi=300)
```

### 5. 向量场/梯度场
适用：梯度下降可视化、微分方程方向场

```python
x, y = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
u = -x  # 梯度x分量
v = -y  # 梯度y分量
fig, ax = plt.subplots(figsize=(8, 8))
ax.quiver(x, y, u, v, alpha=0.7)
ax.streamplot(x, y, u, v, color='blue', linewidth=1, density=1.5)
ax.set_title('梯度场')
plt.savefig('paper_output/figures/gradient_field.png', dpi=300)
```

## 输出规范

- 分辨率：300 DPI
- 格式：PNG（论文） + SVG（可编辑）
- 中文标签：使用 `SimHei` 或 `Microsoft YaHei`
- 数学公式：使用 LaTeX 格式（`$...$`）

## 新增脚本（v4.3）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/journal_style.py` | SciencePlots 期刊风样式——一行让 matplotlib 出 IEEE/Nature/Science 风（76 样式） | "期刊风图表" / "SciencePlots" / "图表美化" |

`pip install SciencePlots`。`journal_style.py list` 看样式，`journal_style.py demo --style IEEE风` 出示例图。绘图脚本里 `plt.style.use(["science","ieee","no-latex"])`。