# outputs/case_feedback_loop.md

> **v2.0 标准化 | 2026-05-31** | 统一索引见 `outputs/INDEX.md`

> 用于把单个题目、单篇论文、单次审稿或单次答辩中得到的经验，稳定回灌到通用数学建模知识库中。

---

## 一、为什么必须做回灌

当前系统最容易停在这一步：

- 个案做出来了
- 论文也改了
- 代码也补了
- 但母库没有变强

如果不回灌，系统只是在“做项目”；  
做了回灌，系统才是在“变强”。

---

## 二、回灌触发条件

只要满足以下任一条件，就应该启动回灌：

1. 某个题目形成了稳定主路线
2. 某次审稿发现了新的高频硬伤
3. 某个图示结构特别好用
4. 某段代码骨架以后还能复用
5. 某次答辩暴露了高频追问
6. 某种方法在某类题上明确不适用

---

## 三、回灌固定流程

### 第一步：提炼案例标签
至少说明：

- 案例名称
- 题型
- 核心目标
- 主路线
- 备选路线
- 最终采用原因
- 主要风险点

### 第二步：提炼新增经验
至少说明：

- 新增了什么可复用规则
- 验证了什么旧规则是对的
- 推翻了什么原先想法
- 哪些表达、图示、代码值得长期保留

### 第三步：定位回写目标
按经验类型回写：

| 经验类型 | 优先回写文件 |
|---|---|
| 题型判断经验 | `outputs/problem_type_taxonomy.md` |
| 路线选择经验 | `outputs/method_matching.md`、`outputs/model_selection_flow.md` |
| 算法与代码经验 | `outputs/algorithm_templates.md`、`outputs/code_template_playbook.md` |
| 正文写作经验 | `outputs/writing_templates.md`、`outputs/result_analysis_templates.md` |
| 图示经验 | `outputs/figure_templates.md`、`outputs/visual_knowledge_base.md` |
| 审稿失分经验 | `outputs/common_failure_patterns.md`、`outputs/revision_checklist.md` |
| 答辩追问经验 | `outputs/defense_qa_bank.md`、`outputs/defense_followup_chains.md` |
| 复现经验 | `outputs/reproducibility_checklist.md` |

### 第四步：判断是否升级为母规则
满足以下任两条，可升级为母规则：

1. 在多个题型中都适用
2. 能明显减少失分风险
3. 能明显提高复现效率
4. 能直接复用到论文或答辩
5. 不是只依赖个案特殊数据

### 第五步：登记到资产索引
若新增了新文件、模板或清单，补登记到 `outputs/asset_registry.md`。

---

## 四、回灌输出模板

每次回灌尽量按以下结构：

### 1. 案例概览
- 案例名称
- 题型
- 主路线
- 结果状态

### 2. 本案例确认有效的规则
- 可复用规则
- 可复用表达
- 可复用图示
- 可复用代码骨架

### 3. 本案例暴露的新风险
- 审题风险
- 选模风险
- 推导风险
- 写作风险
- 复现风险
- 答辩风险

### 4. 母库更新建议
- 应更新哪些 outputs
- 每个 outputs 应补什么

### 5. 后续是否值得形成模板
- 值得 / 不值得
- 原因

---

## 五、回灌时最容易犯的错

1. 只记录“做了什么”，不抽象“以后怎么复用”
2. 只写成功经验，不记录失败路线
3. 只更新 deliverables，不更新 outputs
4. 只更新一个文件，忽略上下游联动文件
5. 把个案特例直接提升成通用规则

---

## 六、一句话标准

案例回灌完成的标准不是“写了复盘”，而是：

> 至少有一条可复用规则真正回写进母库，且下次能直接被调用。
