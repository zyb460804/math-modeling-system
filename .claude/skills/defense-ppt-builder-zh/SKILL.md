---
name: defense-ppt-builder-zh
description: "国赛/五一赛/MathorCup 中文答辩 PPT 生成器。从论文源稿+结果+图表直接生成 .pptx 文件（非大纲）。融合 nature-paper2ppt 的论证骨架+自审循环方法论与 academic-defense-pptx 的结构化论证模式，国赛中文适配（5-8 分钟、10-15 页、中文字体、评审口味）。触发词：生成答辩PPT / 答辩幻灯片 / defense ppt / 做答辩PPT。与 defense skill 衔接：defense 出 Markdown 问答库，本 skill 出 .pptx 文件。"
version: 1.0.0
source: "融合 nature-paper2ppt v5.0（论证骨架+自审循环）+ academic-defense-pptx（结构化论证），2026-08 国赛中文适配"
---

# 国赛中文答辩 PPT 生成器

## 定位

本 skill 是 `defense` 的下游产物生成器：

```
/defense（问答库+追问链+模拟评分，Markdown）
        │
        ▼
/defense-ppt-builder-zh（本 skill：答辩 PPT，.pptx 文件）
```

**与 defense skill 的分工**：
- `defense`：产出答辩**内容**（问答库、追问链、短答模板、风险点）
- 本 skill：产出答辩**演示文件**（.pptx，含图表、动画、排版）

## 触发词

`生成答辩PPT` `答辩幻灯片` `defense ppt` `做答辩PPT` `答辩PPT` `生成slides`

## 核心原则（融合 nature-paper2ppt + academic-defense-pptx）

### 1. 论证优先，不是论文缩印

PPT 的骨架是**论证链**，不是论文目录的复制粘贴。观众（评委）要在 5-8 分钟内回答：

1. 这道题的本质难点是什么？
2. 你们用了什么模型，为什么选它？
3. 关键结果是什么，可信吗？
4. 模型的创新点/亮点在哪？
5. 模型的边界和局限是什么？

**每页 PPT 必须能一句话说清"这页要回答上面哪个问题"**。

### 2. 图表驱动，不是文字驱动

- 国赛答辩 PPT 的核心资产是**关键图表**（模型框架图 + 主要结果图 + 灵敏度图）
- 每页文字 ≤ 80 字，图表占页面 ≥ 50%
- **禁止整页纯文字**（除非是关键公式推导页）

### 3. 反模板视觉（nature-paper2ppt 自审循环）

禁用以下模板化设计：
- ❌ WPS/Office 默认主题（蓝色渐变背景 + 白字）
- ❌ 每页都是"标题 + 项目符号列表"的千篇一律结构
- ❌ 整页截图论文内容（缩印式 PPT）
- ❌ 装饰性图标/动画/转场（分散评委注意力）

推荐设计：
- ✅ 简洁学术风（白底 + 深色字 + 1-2 个强调色）
- ✅ 图文混排（左侧图，右侧要点 / 上方图，下方结论）
- ✅ 关键数字用大字号突出（如准确率 95.3% 用 48pt 红色）
- ✅ 模型框架图作为"故事主线"贯穿多页

## 工作流（5 步 + 自审循环）

### Step 1: 加载论文与答辩材料

读取以下文件（缺则标记 `[待补]`，不阻塞）：

| 文件 | 用途 |
|------|------|
| `paper_output/final_paper_source.md` | 论文源稿（摘要/模型/结果/结论） |
| `paper_output/results/model_results.json` | 结果数据 |
| `paper_output/figures/` | 已生成的图表（直接复用到 PPT） |
| `paper_output/qa/defense_qa_bank.md` | defense skill 产出的问答库 |
| `paper_output/plan/model_route.json` | 模型路线（确认每问的核心模型） |

### Step 2: 确定题型与答辩节奏

| 题型 | 推荐页数 | 重点章节 | 时间分配 |
|------|---------|---------|---------|
| A 题（物理/几何/机理） | 12-15 页 | 机理推导 + 数值验证 + 灵敏度 | 推导 40% / 结果 40% / 总结 20% |
| B 题（优化/规划） | 10-13 页 | 模型构建 + 求解策略 + 方案对比 | 建模 30% / 求解 40% / 结果 30% |
| C 题（数据/评价） | 12-15 页 | 数据处理 + 评价指标 + 排名结果 | 数据 30% / 建模 40% / 结果 30% |
| D 题（统计/预测） | 12-15 页 | 数据特征 + 预测模型 + 精度验证 | 数据 25% / 建模 45% / 检验 30% |
| E/F 题（开放/App） | 10-12 页 | 问题定义 + 方案设计 + 可行性 | 定义 30% / 方案 50% / 验证 20% |

### Step 3: 构建论证骨架（核心）

按以下骨架组织页面（每页 = 一个论证单元）：

```
P1  封面（题号 + 题目 + 队号 + 成员）
P2  问题概述（1 句话讲清题目本质 + 难点图示）
P3  总体思路（模型框架图 ← 全场最重要的一页）
P4  问题一：模型建立（核心公式 + 假设）
P5  问题一：求解与结果（结果图 + 关键数字）
P6  问题一：检验（灵敏度/误差/对比 ← 评委加分项）
P7  问题二：模型建立
P8  问题二：求解与结果
P9  问题二：检验
P10 问题三：（如有，同上结构）
P11 创新点总结（3 条，每条 1 句话 + 1 个数字证据）
P12 模型评价（优点 + 局限 + 改进方向）
P13（备用）问答预备页（关键图表备份，答辩时快速跳转）
```

**规则**：
- 每问至少 3 页（建模/结果/检验）
- 检验页**不能省**（评委最关心"你们验证了吗"）
- 创新点页用数字说话（如"精度提升 12.3%"而非"精度大幅提升"）

### Step 4: 生成 .pptx 文件

使用 `python-pptx` 生成（脚本：`scripts/build_defense_pptx.py`）：

```bash
python .claude/skills/defense-ppt-builder-zh/scripts/build_defense_pptx.py \
  --source paper_output/final_paper_source.md \
  --figures paper_output/figures/ \
  --results paper_output/results/model_results.json \
  --qa-bank paper_output/qa/defense_qa_bank.md \
  --topic-type C \
  --output paper_output/defense.pptx
```

**设计参数**（国赛评审口味）：
- 尺寸：16:9（宽屏）
- 字体：标题 微软雅黑 Bold 32pt / 正文 微软雅黑 20pt / 数字 Times New Roman Bold
- 配色：白底（#FFFFFF）+ 深蓝标题（#1F4E79）+ 深灰正文（#333333）+ 红色强调（#C00000）
- 页码：右下角，格式"X / N"

### Step 5: 自审循环（nature-paper2ppt 核心方法论）

生成后**必须**跑自审循环，最多 3 轮修正：

| 自审项 | 检查标准 | 不通过则 |
|--------|---------|---------|
| **文字溢出** | 每页文字 ≤ 80 字，无文本框溢出 | 自动拆页或精简文字 |
| **图表质量** | 图片分辨率 ≥ 150 DPI，无模糊/拉伸 | 重新导出高清图 |
| **图表占比** | 结果页图表面积 ≥ 50% | 调整布局，放大图表 |
| **论证连贯** | 每页能回答 Step 1 的 5 个问题之一 | 重写页面标题 |
| **数字一致** | PPT 中的数字与论文/frozen_numbers.json 一致 | 用 frozen 数字覆盖 |
| **反模板** | 无 WPS 默认主题痕迹、无装饰性动画 | 清除模板样式 |
| **封面完整** | 题号/题目/队号/成员齐全 | 补全信息 |

自审日志写入 `paper_output/qa/defense_ppt_self_review.json`。

## 与 defense skill 的衔接

```
论文定稿（final_paper.docx 通过门禁）
        │
        ▼
/defense                              ← 生成答辩内容
  ├─ 10 类问答库（defense_qa_bank.md）
  ├─ 30 条追问链
  ├─ 模拟评分
  └─ 短答模板
        │
        ▼
/defense-ppt-builder-zh               ← 本 skill：生成答辩文件
  ├─ defense.pptx（主交付）
  ├─ 问答预备页（从 defense_qa_bank 提取关键问答作为备份页）
  └─ 自审报告（defense_ppt_self_review.json）
```

**问答预备页的设计逻辑**：
- PPT 主体讲论证链（12-13 页）
- 最后 2-3 页放"问答预备"（每问的关键数字 + 关键图表备份）
- 评委提问时快速跳转到对应页，**用图表回答，不用纯口述**

## 国赛 vs 美赛差异

| 维度 | 国赛/五一赛/MathorCup | 美赛 MCM/ICM |
|------|---------------------|-------------|
| 答辩 | 有（5-8 分钟 + 3-5 分钟提问） | 无（仅论文评审） |
| PPT 语言 | 中文 | 不需要 |
| PPT 页数 | 10-15 页 | — |
| 本 skill | ✅ 适用 | ❌ 不触发 |

美赛不需要本 skill，直接走 `/defense` 出问答库备自学即可。

## 输出

| 产物 | 路径 | 说明 |
|------|------|------|
| 答辩 PPT | `paper_output/defense.pptx` | 主交付物（.pptx 文件） |
| 论证骨架 | `paper_output/qa/defense_ppt_outline.md` | 页级大纲（每页标题+要点+图源） |
| 自审报告 | `paper_output/qa/defense_ppt_self_review.json` | 7 项自审结果 + 修正轮次 |

## 依赖

- `python-pptx`（pip install python-pptx）
- 已有图表（`paper_output/figures/`），若无则自动生成占位图并标记 `[待补真实图]`

## 与其他 skill 的关系

| skill | 关系 |
|-------|------|
| `defense` | 上游：defense 出内容，本 skill 出文件 |
| `paper-formal-writer` | 上游：论文源稿来源 |
| `model-code-and-result-generator` | 上游：结果与图表来源 |
| `figure` / `math-figure` | 图表来源（PPT 复用论文图表，不重画） |

## 禁止行为

- ❌ 整页截图论文（缩印式 PPT）
- ❌ 使用 WPS/Office 默认主题
- ❌ 答辩 PPT 超过 15 页（国赛 5-8 分钟讲不完）
- ❌ 省略检验页（评委最看重）
- ❌ 创新点用"大幅提升""显著改善"等模糊词（必须给数字）
- ❌ 装饰性动画/转场（分散评委注意力）