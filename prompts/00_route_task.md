> 系统同步说明：本文件已纳入统一数学建模生产系统（v3.4 统一入口版）。调用时默认遵循：任务路由 → 知识更新/资料入库 → 单题开工 → 数据理解 → 审题选模 → 代码/论文/图表/表格生产 → 动态验收 → 三审计层 → 提交/答辩 → 经验回灌。涉及数据、字段、附件或参数时，先对齐 `outputs/data_cleaning_standards.md`；涉及提交、答辩或可复现判断时，先检查三审计层（consistency → completeness → quality-assurance）；缺真实数据或运行结果时，统一标为【待补】，不得编造。

> **接口契约**
> - 前置依赖：用户任务描述（文本）
> - 后续触发：根据路由结果调用对应 skill 或 prompt（见下方判断表）
> - 输出：任务分类 + 最短调用路径 + 推荐下一步 skill/prompt
> - **核心原则：同一意图 → 默认最深输出**（用户不需要知道"加什么词"才能拿到完整结果）

请先不要直接写答案，也不要直接进入某一个专项 prompt/skill。

你的第一步任务是：把”当前用户任务”路由到正确的系统路径。

开始前优先读取：
- `AGENTS.md`
- `README.md`
- `outputs/production_specs.md`
- `outputs/asset_registry.md`
- `outputs/task_router.md`

## ★ 统一入口速查（v3.4 新增）

> **核心原则：同一意图 → 默认最深输出。** 用户不需要知道”加什么词”才能拿到完整结果。

| 统一入口 | 覆盖的触发词 | 默认输出 |
|---------|-------------|---------|
| `review` / `paper-reviewer` agent | 打分、审稿、严格打分、深度评审、审论文 | 全量深度报告（9部分） |
| `defense` | 准备答辩、模拟答辩、答辩练习、评委提问 | 全量答辩包（10类问答+30条追问链） |
| `analyze` | 审题、选模、推荐模型、建模路线 | 全量审题选模报告（题型+路线+代码模板+风险） |
| `figure` | 生成图示、画图、流程图、网络图、函数图、交互式图表 | 统一图表方案（自动判断→分派→全部图表+索引） |
| `paper-polisher` | 润色、改写、polish、换个说法、更学术一点 | 完整12点检查+段落改写+质量评分（60分制） |
| `code` | 生成代码 | 从零生成代码框架（末节引 algorithm-runner） |
| `algorithm-runner` | 运行算法、执行代码 | 执行已有算法模板（末节引 code） |
| `submit` | 生成提交包 | 最终比赛提交包（自动判断阶段） |
| AIGC降重 | 降AI味、降重、去AI检测 | 默认走 humanizer-zh-academic（14种AI模式+7项硬约束） |

## 三审计层（v3.6 新增）

论文完成后必须通过三审计层才能提交：

```
论文完成后 → consistency-auditor → completeness-auditor → quality-assurance-auditor
三者全部PASS才能提交论文
```

| 审计层 | Skill | 检查内容 | 产出 |
|--------|-------|---------|------|
| 第一层 | `consistency-auditor` | 数字/文件名/符号一致性 | `qa/consistency_audit_report.json` |
| 第二层 | `completeness-auditor` | 审查文件/报告/产物齐全 | `qa/completeness_audit_report.json` |
| 第三层 | `quality-assurance-auditor` | 工作流完整性+反编造 | `qa/evidence_gate_report.json` |

---

然后按以下顺序判断：

1. 当前任务更属于哪一类：
- 系统建设
- 审题选模（用 `/analyze`）
- 论文写作
- 代码生成（用 `/code`）
- 图示生成（用 `/figure`）
- 审稿改稿（用 `/review`）
- 答辩准备（用 `/defense`）
- 提交冲刺（用 `/submit`）
- 个案回灌

2. 当前用户手里最完整的输入是什么：
- 只有目标
- 一道题
- 一批资料
- 一篇论文
- 一段代码
- 一组结果
- 一个接近完成的提交包

3. 当前最缺什么：
- 规则
- 路线
- 论文段落
- 代码
- 图示
- 审稿意见
- 答辩口径
- 提交清单

4. 给出最稳妥的调用顺序：
- 应先调用哪个 skill 或 prompt（优先使用统一入口）
- 应配套读取哪些 outputs
- 是否应直接生成 `deliverables/`
- 做完后是否应触发 `prompts/22_case_feedback_loop.md`

输出格式固定为：

## 1. 任务归类
- 当前任务类型
- 当前输入完整度
- 当前最关键缺口

## 2. 推荐调用路径
- 第一步（优先使用统一入口 skill）
- 第二步
- 第三步

## 3. 应优先读取的 outputs
- 文件 1
- 文件 2
- 文件 3

## 4. 建议产出
- 应更新的规则库
- 应生成的成品

要求：
- 路由要直接
- 不要空谈
- 不要一上来把全部 prompt/skill 都列出来
- 优先给最短、最稳妥、最能落地的路径
- **优先使用统一入口 skill**（/analyze、/review、/defense、/figure、/code、/submit 等）
- 正式赛题必须走三审计层（consistency → completeness → quality-assurance）

---

## ★ v4.2/v4.3 工具能力速查（按需调用，不进主流水线）

读题/取数：`extract_pdf_tables.py`（Camelot PDF 表格）/ `extract_formulas_ocr.py`（Pix2Text 公式）/ `akshare_fetch.py`（宏观金融数据）
建模/调参：`optuna_tune.py`（超参 TPE）/ `verification_template.py`+`verify_gate.py`（G4.6 自证）/ `shap_explain.py`（特征重要性）/ `matlab_runner.py` + 3 模板（MATLAB 强项：ODE/曲线拟合/优化）
画图/写作：`journal_style.py`（期刊风）/ `compile_latex.py`（LaTeX 编译重试）/ `typst-renderer`（Typst 交付）/ `docx-editor-cn`（Word 公式+XML）/ `replace_docx_preserve_format.py`（保留格式降重）
验收/检索：`pipeline_manager.py`（GitOps 状态）/ `check_numeric_sanity.py`（inf/nan）/ `freshness_check.py`（报告新鲜度）/ `security_check.py`（密钥/注入）/ `award-paper-rag`（优秀论文章节级 RAG）

**路由规则**：用户口令命中上表 → 直接调对应脚本（脚本未装依赖则提示安装，不阻断）；主流水线运行中 → orchestrator 自动调 G4.6/numeric_sanity/security_check 做门禁。详见 `outputs/task_router.md` §十五。
