# Figure Contract Template（图表合同模板）

> **用途**：在编写任何绘图代码之前，必须先建立 Figure Contract，确保每张图都是一个视觉论证。
> **来源**：math-modeling-skill/references/roles/编程手/references/可视化规范.md
> **版本**：v1.0
> **标准**：SCI / Nature 级学术图表

---

## 1. 图表要证明的一句话结论（Core Claim）

用一句话写出这张图必须证明的核心主张。这张图的所有面板、标注、配色都服务于这句话。

**要求**：
- 必须是可被视觉证据支撑的命题（非抽象描述）
- 必须与 Model Contract 中对应子问题的证据角色一致
- 长度：一句话，不超过 30 字

**示例**：
> "本文模型在所有指标上均优于 3 个基线方法"
> "参数 alpha 在 0.3-0.5 区间内模型表现稳定"
> "2020-2025 年 PM2.5 浓度呈下降趋势且置信区间收窄"

---

## 2. 每个面板的独特证据（Panel Evidence）

将核心结论拆解为若干条证据，每个面板对应一条独特证据。

### 防冗余原则

**核心规则**：如果遮盖任意一个面板后，该图的核心结论仍能从其他面板完整读取，则该面板是冗余的。

**自检方法**：对每个面板，尝试遮盖后问自己："剩余面板能否完整支撑核心结论？" 如果能，该面板应被移除或合并。

### 面板规划表

| 面板 | 证据内容 | 面板类型 | 数据来源 |
|------|---------|---------|---------|
| a | [该面板唯一能证明的结论] | [柱状/折线/散点/热力图/箱线图] | [results/Qx/...] |
| b | [该面板唯一能证明的结论] | [柱状/折线/散点/热力图/箱线图] | [results/Qx/...] |

**数量约束**：
- 每个大图最多包含 **2 个子图**（面板 a + 面板 b）
- 禁止在一个大图中包含 3 个或更多子图
- 如需展示多张图表，分成多个独立图片文件

---

## 3. 反冗余检查（Anti-Redundancy Audit）

在完成面板规划后，执行以下检查：

### 检查清单

- [ ] 面板 a 和面板 b 是否各自承载独特证据？
- [ ] 遮盖面板 a 后，核心结论是否仍完整？（若是 → 面板 a 冗余）
- [ ] 遮盖面板 b 后，核心结论是否仍完整？（若是 → 面板 b 冗余）
- [ ] 两个面板是否使用了不同的视觉编码方式？（避免重复表达）
- [ ] 图表类型是否与数据类型匹配？（参见下方原型分类）

### 常见冗余模式

| 冗余类型 | 表现 | 修正 |
|---------|------|------|
| 数值重复 | 两个面板展示同一组数字的不同可视化 | 保留信息量更大的面板 |
| 结论重复 | 两个面板支撑同一论点 | 合并为一个面板或拆为两张独立图 |
| 视觉重复 | 柱状图和折线图展示同一趋势 | 保留折线图（趋势）或柱状图（对比） |

---

## 4. 图表原型分类（Figure Prototype）

根据数据特征和论证需求，选择合适的图表原型。

### 四种原型

| 原型 | 特征 | 适用场景 | 示例 |
|------|------|---------|------|
| **定量网格** | 多组数值对比，坐标轴明确 | 方法对比、参数扫描 | 分组柱状图、折线图 |
| **示意图主导** | 流程/结构/关系为主 | 模型框架、系统架构 | 流程图、网络图、示意图 |
| **混合** | 数值 + 结构并存 | 含数据标注的流程 | 带数据的桑基图、带数值的树状图 |
| **非对称** | 主图 + 辅图，强调层级 | 主结果 + 补充验证 | GridSpec 不对称布局 |

### 数据类型 → 图表推荐

| 数据类型 | 推荐图表 | 用途 |
|---------|---------|------|
| 分类对比 | 柱状图 / 分组柱状图 | 展示不同方法在同一指标上的差异 |
| 时间趋势 | 折线图 + 置信区间 | 展示随时间的变化趋势和不确定性 |
| 数据分布 | 箱线图 / 小提琴图 / 直方图 | 展示数据分布特征和异常值 |
| 相关性 | 散点图 + 拟合线 | 展示两个变量之间的关系 |
| 矩阵数据 | 热力图 | 展示相关性矩阵或混淆矩阵 |
| 组成结构 | 堆叠柱状图 | 展示各部分占比及变化 |
| 多维数据 | 3D 散点图 / 气泡图 | 展示三个及以上维度的关系 |
| 综合评价 | 雷达图 | 多指标综合对比 |

---

## 5. 灰度安全 + 色盲无障碍审计（Accessibility）

### 灰度安全

所有图表在打印为黑白时必须仍可辨识。要求：
- 不依赖纯色相区分不同数据系列
- 使用填充纹理（hatching）或标记形状（marker）作为冗余编码
- 关键对比必须在灰度下有足够明度差（>= 30%）

### 色盲无障碍

- 禁止仅依赖红-绿对比（最常见的色盲类型）
- 使用色盲安全调色板（如 PALETTE 中的蓝-橙-灰体系）
- 对关键数据系列添加文字标注或形状区分

### 检查方法

```python
def check_greyscale_safety(fig):
    """灰度安全快速检查"""
    # 1. 将 figure 保存为灰度 PNG
    fig.savefig('temp_grey.png', dpi=100)
    # 2. 用 PIL 转灰度
    from PIL import Image
    img = Image.open('temp_grey.png').convert('L')
    # 3. 检查不同系列的平均明度差
    # 如果任意两个系列的明度差 < 30，标记为不安全
```

---

## 6. matplotlib 发布级配置模板（Publication Config）

以下配置模板是所有绘图代码的基线。每个绘图脚本必须在开头包含此配置。

### 全局配置

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import numpy as np

warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# ===== SCI/Nature 级全局配置 =====

# 1. 中文字体优先 + 多字体备选
plt.rcParams['font.sans-serif'] = [
    'SimHei', 'Microsoft YaHei', 'Arial Unicode MS',
    'Arial', 'DejaVu Sans', 'Liberation Sans'
]
plt.rcParams['axes.unicode_minus'] = False

# 2. SVG 可编辑文本（强制）
plt.rcParams['svg.fonttype'] = 'none'

# 3. 无网格线 + 精简坐标轴（仅保留左+下 spines）
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.major.width'] = 0.8
plt.rcParams['ytick.major.width'] = 0.8

# 4. 图例无边框
plt.rcParams['legend.frameon'] = False

# 5. 字体大小层次
plt.rcParams['font.size'] = 7
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 6.5
plt.rcParams['ytick.labelsize'] = 6.5
plt.rcParams['legend.fontsize'] = 6.5
plt.rcParams['lines.linewidth'] = 1.5
```

### 标准调色板

```python
PALETTE = {
    # 主色 / 核心方法
    'blue_main':      '#0F4D92',
    'blue_secondary': '#3775BA',

    # 正向 / 改进色系
    'green_1': '#DDF3DE',
    'green_2': '#AADCA9',
    'green_3': '#8BCF8B',

    # 基线 / 对比色系
    'red_1':      '#F6CFCB',
    'red_2':      '#E9A6A1',
    'red_strong': '#B64342',

    # 中性辅助色
    'neutral_light': '#CFCECE',
    'neutral_mid':   '#767676',
    'neutral_dark':  '#4D4D4D',
    'neutral_black': '#272727',

    # 强调色（谨慎使用）
    'gold':    '#FFD700',
    'teal':    '#42949E',
    'violet':  '#9A4D8E',
    'magenta': '#EA84DD',
}
```

### 工具函数

```python
def luminance_text_color(hex_color):
    """根据背景色明度自动返回白色或深色文字"""
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2], 16) / 255, int(c[2:4], 16) / 255, int(c[4:6], 16) / 255
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return 'white' if luminance < 0.5 else '#333333'


def save_figure(fig, filename, output_dir='paper_output/figures'):
    """统一保存：SVG + PNG + 关闭图表"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(f'{output_dir}/{filename}.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)  # 强制关闭，防止内存泄漏
```

### 面板标签规范

```python
ax.text(-0.08, 1.08, 'a', transform=ax.transAxes,
        fontsize=22, fontweight='bold', va='top', ha='right')
```

- 小写粗体 `a, b, c, d, ...`
- 每个子图左上角（transAxes 坐标）
- 字号 22（绝对字号）

### 统计标注规范

```python
# p 值标注（右上角）
ax.text(0.95, 0.95, 'p = 0.003', transform=ax.transAxes,
        fontsize=7, color='#4D4D4D', va='top', ha='right', style='italic')

# 误差棒
ax.errorbar(x, y, yerr=std, fmt='o', capsize=3,
            color=PALETTE['blue_main'], markersize=5)

# n 数标注（右下角）
ax.text(0.95, 0.05, f'n = {n}', transform=ax.transAxes,
        fontsize=6.5, color='#767676', va='bottom', ha='right')
```

### 不对称布局模板

```python
fig = plt.figure(figsize=(10, 4))
gs = fig.add_gridspec(1, 3, width_ratios=[2, 1, 1], wspace=0.3)
ax0 = fig.add_subplot(gs[0])   # 主图
ax1 = fig.add_subplot(gs[1])   # 辅图 1
ax2 = fig.add_subplot(gs[2])   # 辅图 2
```

### 图幅尺寸建议

| 图表类型 | figsize |
|---------|---------|
| 单图（柱状/折线） | (8, 5) |
| 双子图并排 | (12, 5) |
| 双子图上下 | (7, 10) |
| GridSpec 不对称 | (10, 4) |
| 3D 图 | (8, 7) |
| 热力图 | (8, 6) |

---

## 7. 图表类型分类（Figure Type Classification）

所有图表必须归入以下四类之一：

| 类型 | 名称 | 用途 | 质量要求 |
|------|------|------|---------|
| Type 1 | 诊断图 | 建模手内部调试 | 不进入论文 |
| Type 2 | 对比图 | 方法对比 | 可进入论文，需 render_check |
| Type 3 | 论文图 | 最终结果展示 | 必须进入论文，出版级质量 |
| Type 4 | 附录图 | 补充材料 | 正文引用，附录展示 |

**render_check 标准**：
- 最小字体 >= 6.5pt
- 最小分辨率 >= 150 DPI
- 最小尺寸 >= 800x600 像素
- 文字重叠 <= 5% 重叠比例
- 画布使用：白色区域 <= 80%

---

## 8. 完整 Figure Contract 示例

```markdown
## Figure Contract — Figure 3: 本文模型 vs 基线方法对比

### 核心结论
本文提出的混合模型在 RMSE、MAE、R^2 三个指标上均优于 3 个基线方法。

### 面板规划

| 面板 | 证据内容 | 面板类型 |
|------|---------|---------|
| a | 4 种方法在 3 个指标上的分组柱状图，本文方法用蓝色高亮 | 分组柱状图 |
| b | 本文方法与最优基线的配对 t 检验结果（p 值标注） | 统计检验表 |

### 反冗余检查
- [x] 面板 a 展示绝对数值对比，面板 b 展示统计显著性 → 证据不重复
- [x] 遮盖面板 a 后无法知道具体数值差异 → 面板 a 不冗余
- [x] 遮盖面板 b 后无法确认差异是否显著 → 面板 b 不冗余

### 图表原型
定量网格（多组数值对比，坐标轴明确）

### 无障碍审计
- [x] 使用蓝-灰-橙体系，非红绿对比
- [x] 本文方法额外使用斜线填充纹理（灰度安全）
- [x] 基线方法使用不同 marker 形状

### 配置
- figsize: (12, 5)
- PALETTE: blue_main 本文方法, neutral_mid 基线方法
- 面板标签: a (左), b (右)
- 保存: SVG + PNG (300 DPI)
```

---

## 9. 常见问题排查

### 中文字体显示为方框

```python
# 快速诊断
import matplotlib.font_manager as fm
cn_fonts = [f.name for f in fm.fontManager.ttflist
            if any(k in f.name for k in ['Hei', 'YaHei', 'CJK'])]
print(cn_fonts)  # 期望: ['SimHei', 'Microsoft YaHei']
```

### SVG 文本在 Word 中不可编辑

确认配置中包含：
```python
plt.rcParams['svg.fonttype'] = 'none'
```

### Polyfit 病态条件警告

- 降低多项式阶数（<= 10）
- 使用 `numpy.polynomial.Polynomial.fit()` 替代
- 改用样条插值（`scipy.interpolate`）