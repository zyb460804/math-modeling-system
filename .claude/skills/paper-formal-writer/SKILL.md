---
name: paper-formal-writer
description: "国赛数学建模正式论文范式、outline、Word 排版和格式门禁 skill。Invoke when 证据门禁通过后需要生成 CUMCM 风格正式论文、规范标题编号、扩写正文、插入图表表格、导出 Word 或检查论文格式。触发词：正式成稿、Word排版、格式门禁、outline、论文写作、CUMCM格式、check_paper_format、导出Word。"
---

# 正式论文范式写作器

## 执行契约
- 上游输入：必须优先读取 `paper_output/plan/model_route.json`、`paper_output/results/`、`paper_output/tables/table_index.json`、`paper_output/figure_index.json` 和证据门禁报告。
- 核心输出：`paper_output/plan/paper_outline.json`、`paper_output/final_paper_source.md`、`paper_output/final_paper.docx`、`paper_output/format_check_report.md`。
- 下游交接：格式检查通过后，回到 `quality-assurance-auditor` 做最终一致性检查；未通过时继续补正文、图表解释或证据引用。
- 失败回退：证据门禁未通过时，不得把 Word 称为最终稿；可以只生成 outline 和待写作清单。

## 目标
- 本技能负责正式论文范式、章节编号、写作约束、Word 排版和格式检查。
- 正式论文必须由 Agent 基于完整证据链全局写作，不得机械拼接 quickstart 草稿或微单元草稿。
- 标题编号固定采用 `1 / 1.1 / 1.1.1`。
- 正式稿默认目标为 `18000-25000` 中文字；低于 `18000` 在正式格式检查中失败。

## 何时使用
- `quality-assurance-auditor/scripts/evidence_gate.py` official 模式已经通过，需要进入正式成稿。
- 用户要求“按国赛论文格式”“正式 Word”“扩写到比赛论文工作量”“图表插入并解释”“检查论文格式”。
- 已有 `final_paper_source.md` 或 `final_paper.md`，需要统一 Word 样式、图题表题和标题层级。

## References
- 正式格式总规范：`references/cumcm-paper-standard.md`
- 可直接交给 Agent 的全文模板：`references/formal-paper-template.md`
- 各章节扩写规则：`references/section-expansion-rules.md`
- 图表、公式、算法和结果解释规则：`references/figure-table-writing-rules.md`

## 写作增强工具（v4.0 新增）

以下参考资料在工作流特定阶段按需加载，无需一次性全部读取。

| 参考资料 | 路径 | 加载时机 | 用途 |
|----------|------|----------|------|
| 章节架构模式 | `references/section-architecture.md` | **规划论文结构时**加载 | 标准章节组织模式、段落递进逻辑、结构模板 |
| 证据金字塔 | `references/evidence-pyramid.md` | **组织论证时**加载 | 证据层级、论证强度、数据→结论的推理链 |
| 中英双语学术短语库 | `references/common-phrases.md` | **写作时按章节**加载 | 各章节高频学术表达、中英对照、避免口语化 |
| 文献检索指南 | `references/literature-review-guide.md` | **写文献综述时**加载 | 文献检索策略、综述结构、引用规范 |
| 4轮自审框架 | `references/four-round-self-review.md` | **论文完成后**加载 | 4轮系统化自审清单：结构→论证→表达→格式 |
| Anti-AI-detection写作指南 | `references/anti-ai-detection-guide.md` | **自审Round 3时**加载 | 降低AI生成痕迹、增强人写感、规避AIGC检测 |
| AI 写作红绿灯 | `references/ai-traffic-light.md` | **写作前/降AI味时**加载 | 绿/黄/红灯行为边界 + paper-type 诊断（v4.8 整合自 nature-polishing） |
| 美赛英文写作指南 | `references/english-academic-writing.md` | **写 MCM/ICM 英文稿时**加载 | 论证驱动写作 + 章节默认架构 + 中式英语失败模式（v4.8 整合自 nature-writing） |

### 路由规则

在正式工作流中，按以下节点加载对应文档：

1. **Step 2-3（outline + 全局写作前）**：加载 `section-architecture.md`，规划章节骨架
2. **Step 3（撰写第5章模型建立与求解）**：加载 `evidence-pyramid.md`，组织论证链
3. **Step 3（撰写各章节时）**：按当前章节加载 `common-phrases.md` 中对应片段
4. **Step 3（撰写第8章参考文献/文献综述部分）**：加载 `literature-review-guide.md`
5. **Step 4（格式检查后）**：加载 `four-round-self-review.md`，执行4轮自审
6. **Step 4（自审Round 3 表达层审查）**：加载 `anti-ai-detection-guide.md`，降低AIGC痕迹
7. **写 MCM/ICM 英文稿时**：加载 `english-academic-writing.md`，按论证驱动结构组织英文表达
8. **写作前/降AI味阶段**：加载 `ai-traffic-light.md`，先做 paper-type 诊断再决定改写强度

## ★ 项目知识资产联动（必须执行）
本 skill 执行时，**必须**读取以下 `outputs/` 中已沉淀的规则，作为正式写作的权威依据：

| 资产 | 路径 | 用途 |
|------|------|------|
| 写作模板库 | `outputs/writing_templates.md` | 高分表达、结构模板、失分表达黑名单 |
| 摘要模板 | `outputs/abstract_templates.md` | 六段式摘要填空模板 |
| 结果分析模板 | `outputs/result_analysis_templates.md` | 结果分析写作模板 |
| 灵敏度分析模板 | `outputs/sensitivity_and_robustness_templates.md` | 灵敏度/鲁棒性写作模板 |
| 结果解读模板 | `outputs/result_interpretation_templates.md` | 结果解读与讨论写作模板 |
| 评审清单 | `outputs/revision_checklist.md` | 改稿检查清单 |
| 评分量表 | `outputs/scoring_rubric.md` | 100分制7维度，写作时对齐评分点 |

**执行规则**：
1. Agent 全局写作 `final_paper_source.md` 时，必须先读 `outputs/writing_templates.md` 获取高分表达模板
2. 摘要写作必须参考 `outputs/abstract_templates.md` 的六段式结构
3. 结果分析写作必须参考 `outputs/result_analysis_templates.md`，避免"只报数不解释"
4. 不得使用 `outputs/revision_checklist.md` 中标记的失分表达

## 脚本清单
- `scripts/build_paper_outline.py`
  - 读取题意、模型路线、结果、指标、结论、图表和表格索引。
  - 输出 `paper_output/plan/paper_outline.json`。
- `scripts/format_formal_docx.py`
  - 输入 `paper_output/final_paper_source.md`。
  - 输出 `paper_output/final_paper.docx` 和 `paper_output/format_check_report.md`。
  - 使用 `python-docx`，不依赖 LibreOffice。
- `scripts/check_paper_format.py`
  - 检查字数、章节、三级标题、图表引用、参考文献、附录、占位符、证据覆盖和 Word 视觉结构。
  - Word 视觉 QA 至少检查 docx 能否打开、段落数、标题样式数量、图片数量和表格数量是否与索引大体匹配。
  - 输出 `paper_output/format_check_report.md` 与 `paper_output/format_check_report.json`。

## 正式工作流
1. 确认证据门禁已通过；若未通过，先补齐 `paper_output/code/`、`results/`、`tables/` 和 `figures/`。
2. 运行：
   ```bash
   python .claude/skills/paper-formal-writer/scripts/build_paper_outline.py
   ```
3. Agent 读取 `paper_outline.json` 和 references，基于完整证据链全局撰写：
   ```text
   paper_output/final_paper_source.md
   ```
4. 运行：
   ```bash
   python .claude/skills/paper-formal-writer/scripts/format_formal_docx.py
   python .claude/skills/paper-formal-writer/scripts/check_paper_format.py
   ```
5. 若格式检查失败，按报告补正文、图表解释、参考文献、附录或缺失章节。

## 正式论文必须满足
- 摘要按子问题展开，包含方法、模型、算法和关键结果。
- `1 问题重述`、`2 问题分析`、`3 模型假设`、`4 符号说明`、`5 模型的建立与求解`、`6 模型检验与灵敏度分析`、`7 模型评价与推广`、`8 参考文献`、`附录` 结构完整。
- 每问在第 5 章中至少包含 `5.x.1 建模思路`、`5.x.2 变量定义与公式推导`、`5.x.3 求解算法`、`5.x.4 结果分析`、`5.x.5 模型检验或灵敏度分析`。
- 每张图表必须在正文中引用并解释；图表不能只插入不分析。
- 每个公式必须先定义变量、再给公式、再解释公式含义和用途。
- 算法必须用 `Step 1`、`Step 2` 等形式说明。

## 与其他 skill 的关系
- `paper-workflow-orchestrator`：总入口，证据门禁通过后路由到本技能。
- `paper-micro-unit-generator`：提示词资产库和兜底草稿工具，不再作为正式论文主笔。
- `quality-assurance-auditor`：负责证据门禁；本技能负责格式门禁，两者都通过后才可称为正式稿。

## 新增脚本（v4.2/v4.3）

| 脚本 | 用途 | 触发 |
|------|------|------|
| `scripts/compile_latex.py` | LaTeX 论文编译（2 pass + 失败重试 3 次，解析 .log 错误行） | "编译 LaTeX" / "latex 编译" |
| `scripts/office/` | docx XML 级局部编辑工具（pack/unpack/validate/soffice + helpers） | "局部改 Word" / "docx 解包" |

compile_latex 融合自 AutoMCM-Pro；office/ 融合自 Gostyan/docx-skill-4-cn-paper。两条 LaTeX/Word 交付链路的工程保障。
