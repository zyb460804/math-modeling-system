---
name: figure
description: ★ 统一图表入口。自动判断论文需要什么图，调度所有子图表 skill 生成。说"画图""生成图示""流程图""网络图""交互图""论文图"均走此入口。
---

# /figure — 统一图表生成入口

> **核心原则**：同一意图 → 默认最深输出。所有图表相关的触发词均走此入口，内部自动路由到对应子 skill。

## 触发词（统一入口）

以下触发词**全部**路由到本 skill，内部根据上下文和需求自动调度：
`生成图示` `画图` `图表` `流程图` `架构图` `网络图` `函数图` `交互式图表` `论文图` `推荐图表` `可视化`

## 架构

```
用户说任何图表相关触发词
        │
        ▼
  ┌─────────────────────────┐
  │  /figure（本 skill）      │
  │  统一入口 + 需求判断     │
  └──────┬──────────────────┘
         │ 自动判断需要哪些图
         ├──► diagram-maker     → 流程图/架构图/算法步骤图
         ├──► chart-recommender → 数据结果图（柱状/折线/热力/雷达等）
         ├──► math-figure       → 函数图/几何图/概率分布/等高线
         ├──► network-graph     → 图论网络图/最短路径/社区检测
         ├──► interactive-chart → Plotly 交互图（答辩用）
         └──► nature-figure     → Nature 出版级多面板图（自动联动）
```

## 工作流

### Step 1: 判断论文需要什么图

读取以下信息自动判断：
- `paper_output/plan/` — 模型路线与数据计划
- `paper_output/results/` — 已有模型结果
- `paper_output/figures/figure_index.json` — 已有图表（避免重复）
- `outputs/figure_templates.md` — 图表模板库
- `outputs/visualization_strategy_library.md` — 可视化策略库

按论文阶段确定图表需求：

| 论文阶段 | 需要的图 | 分派子 skill |
|---------|---------|-------------|
| 模型建立 | 模型求解流程图/方法架构图 | `diagram-maker` |
| 模型建立 | 指标体系结构图 | `diagram-maker` |
| 求解过程 | 算法步骤图 | `diagram-maker` |
| 结果分析 | 结果对比柱状图/折线图/雷达图等 | `chart-recommender` → `nature-figure` |
| 结果分析 | 预测拟合曲线+置信区间 | `math-figure` → `nature-figure` |
| 结果分析 | 优化收敛曲线/3D响应面 | `interactive-chart` / `math-figure` |
| 结果分析 | 网络拓扑/最短路径图 | `network-graph` |
| 稳健性 | 灵敏度热力图/扰动对比图 | `chart-recommender` → `nature-figure` |
| 答辩 | 交互式图表（HTML） | `interactive-chart` |

### Step 2: 生成图示方案

输出统一的图示方案：

```markdown
## 图表生成方案

### 已有图表（跳过）
| 图名 | 文件 | 状态 |
|------|------|------|

### 待生成图表（按优先级排序）
| 优先级 | 图名 | 类型 | 用途 | 放置位置 | 分派子 skill | 数据来源 |
|--------|------|------|------|---------|-------------|---------|
| 1 | | | | | | |
| 2 | | | | | | |
```

### Step 3: 逐图生成

按优先级逐个调用子 skill 生成图表：
- 数据驱动的结果图 → `chart-recommender` 推荐类型 + `nature-figure` 出版级渲染
- 流程图/架构图 → `diagram-maker`（Mermaid 预览 + matplotlib 出版级）
- 数学图 → `math-figure`
- 网络图 → `network-graph`
- 交互图 → `interactive-chart`

### Step 4: 更新 figure_index.json

每张图生成后更新 `paper_output/figures/figure_index.json`：

```json
{
  "figures": [
    {
      "id": "fig_01",
      "name": "模型求解流程图",
      "file": "paper_output/figures/methodology_flowchart.png",
      "type": "流程图",
      "section": "模型建立",
      "claim": "展示从问题到结论的完整求解路径",
      "generated_by": "diagram-maker",
      "status": "done"
    }
  ],
  "generated_at": "2026-06-15T...",
  "total": 8,
  "done": 5,
  "pending": 3
}
```

## 子 skill 触发规则

| 子 skill | 何时调用 | 输入 | 输出 |
|----------|---------|------|------|
| `diagram-maker` | 需要流程图/架构图/算法步骤图/数据流向图 | 论文模型结构和算法流程 | Mermaid + matplotlib PNG/SVG |
| `chart-recommender` | 需要数据结果图（柱状/折线/雷达/热力等） | 题型+数据特征+展示目的 | 推荐图表类型+matplotlib 代码 |
| `math-figure` | 需要函数图像/几何示意/概率分布/等高线 | 数学公式或数据 | 300DPI PNG + SVG |
| `network-graph` | 需要图论网络可视化 | 节点/边/权重数据 | 静态 PNG + 交互式 HTML |
| `interactive-chart` | 需要答辩用交互式图表 | 数据 + 展示维度 | Plotly HTML |
| `nature-figure` | 需要出版级数据图表（论文终稿用） | 数据 + 图名/轴定义/配色 | PNG+SVG+PDF 300DPI |

### 自动联动规则

当图表属于以下类型时，**自动联动 `nature-figure`** 生成出版级版本：

| 图的类型 | 是否联动 nature-figure | 说明 |
|----------|----------------------|------|
| 结果展示图（柱状/条形/折线） | ✅ 必须联动 | 数据驱动，需要出版级质量 |
| 灵敏度/稳健性展示图 | ✅ 必须联动 | 数据驱动 |
| 变量关系图（散点/相关矩阵） | ✅ 必须联动 | 数据驱动 |
| 热力图 | ✅ 必须联动 | 数据驱动 |
| 技术路线图/流程图 | ❌ | 示意图，直接 SVG |
| 模型结构图 | ❌ | 示意图，直接 SVG |
| 算法流程图 | ❌ | 示意图，直接 SVG |
| 答辩交互图 | ❌ | HTML，不走出版级 |

## 输出位置

- 所有图表 → `paper_output/figures/`
- 图表索引 → `paper_output/figures/figure_index.json`
- 表格索引 → `paper_output/tables/table_index.json`

## 约束

- 每张关键图必须回答一个问题：题目结构 / 模型怎么走 / 变量如何关联 / 算法如何推进 / 结果说明什么
- 流程图不超过 10 个节点（保持清晰）
- 论文用图：PNG 300DPI + SVG（可编辑）
- 答辩用图：交互式 HTML 或 PNG 150DPI
- 中文标签，字号 ≥ 10pt
- 配色与论文整体一致
- 坐标轴、单位、图例、图表编号完整

## 系统同步说明

任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 最终质量门 → 提交/答辩 → 经验回灌。