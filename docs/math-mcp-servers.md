# 数学/学术 MCP 服务器配置指南（v4.3）

> Claude Code 通过 MCP（Model Context Protocol）接入外部工具服务器。本文档列出
> 经 v4.3 调研筛选、对数模竞赛有实际价值的 6 个数学/学术 MCP，附安装命令。
> 这些是**外部 MCP 服务器**，需你自行安装（我不能替你装），但装一次永久可用。

## 总览

| MCP | 能力 | 数模用途 | 推荐 |
|-----|------|---------|------|
| **sympy-mcp** | 符号计算（推导/化简/解方程） | 验算论文公式推导是否正确 | ⭐⭐⭐ |
| **mcp-optimizer** | 运筹优化（PuLP/OR-Tools） | 优化题（调度/路径/资源分配） | ⭐⭐⭐ |
| **arxiv-latex-mcp** | 拉 arXiv 论文 LaTeX 源码 | 深入理解某方法的数学细节 | ⭐⭐ |
| **semantic-scholar-mcp** | 2 亿论文图谱 + 引用网络 | 真实文献检索（补 nature-citation） | ⭐⭐ |
| **Wolfram-MCP** | Wolfram 高精度计算 | 复杂数值/符号（需 Wolfram ID） | ⭐ |
| **math-mcp** | 基础数学/统计 | 简单计算兜底 | ⭐ |

## 通用安装模式

Claude Code 添加 MCP 的标准方式：

```bash
# 方式一：claude mcp add（推荐，存用户配置）
claude mcp add <名称> -- <启动命令>

# 方式二：编辑项目 .mcp.json（团队共享）
```

大多数 Python MCP 用 `uvx`（uv 的临时运行器，免装）启动：
```bash
# 先装 uv（若未装）
pip install uv
# 或 winget install astral-sh.uv
```

## 1. sympy-mcp（符号计算）

源：`sdiehl/sympy-mcp`（77★）。提供符号化简、求导、积分、方程求解、矩阵运算。

```bash
# 需克隆后运行（未发 PyPI）
git clone https://github.com/sdiehl/sympy-mcp && cd sympy-mcp
claude mcp add sympy-mcp -- uv run mcp run server.py
```
装完即可对话："化简 sin(x)^2 + cos(x)^2"、"求 d/dx(x^3 e^x)"、"验证论文式(3)的推导"。

## 2. mcp-optimizer（运筹优化）

源：`dmitryanchikov/mcp-optimizer`（5★）。PuLP + OR-Tools，LP/MIP/约束规划。

```bash
# 已发 PyPI（uvx 版仅 PuLP，完整功能用 pip）
claude mcp add mcp-optimizer -- uvx mcp-optimizer
# 或完整：pip install "mcp-optimizer[stable]" 后 claude mcp add mcp-optimizer -- mcp-optimizer
```
用途：优化题直接让 Claude 建模求解（决策变量/目标/约束），不用手写 Python。

## 3. arxiv-latex-mcp（论文 LaTeX 源码）

源：`takashiishida/arxiv-latex-mcp`（141★）。拉 arXiv 论文 LaTeX，喂给模型理解方法细节。

```bash
# 已发 PyPI
claude mcp add arxiv-latex-mcp -- uvx arxiv-latex-mcp
```
用途：选模时"找 arXiv 上 XXX 方法的原始论文，看它的目标函数怎么构造"。

## 4. semantic-scholar-mcp（学术检索）

源：`smaniches/semantic-scholar-mcp`（12★，14 个工具）。Semantic Scholar 2 亿论文 + 引用图谱。

```bash
# 已发 PyPI（包名 s2-mcp-server）
claude mcp add semantic-scholar -- uvx s2-mcp-server
```
用途：真实文献检索（替代编造引用），"找 2020 年后关于 XXX 的被引 Top10 论文"。

## 5. Wolfram-MCP（高精度计算）

源：`paraporoco/Wolfram-MCP`（12★）。需 Wolfram ID + WolframScript。

```bash
# 前置：装 WolframScript（winget install Wolfram.WolframScript）+ 配 Wolfram ID
claude mcp add wolfram -- uvx git+https://github.com/paraporoco/Wolfram-MCP
```

## 6. math-mcp（基础数学兜底）

源：`EthanHenrickson/math-mcp`（165★）。基础数学/统计函数。

```bash
claude mcp add math-mcp -- npx -y @modelcontextprotocol/server-math
```

## 验证安装

```bash
claude mcp list              # 列出已装 MCP
claude mcp get sympy-mcp     # 查看某 MCP 详情
```
装后在 Claude Code 里说"用 sympy 验证这个公式"，会自动调用。

## 优先级建议

**优化/运筹题常考**：先装 `mcp-optimizer` + `sympy-mcp`（覆盖 80% 数模计算场景）。
**冲奖需文献支撑**：加 `semantic-scholar-mcp` + `arxiv-latex-mcp`（真实引用，防编造）。
**复杂符号推导**：最后加 `Wolfram-MCP`（需 Wolfram 账号）。

## 与项目内 skill 的关系

- MCP 是**运行时外部工具**（Claude 对话时实时调用）
- 项目 skill（如 `symbol-table-builder`、`robustness-checker`）是**流程编排**
- 两者互补：skill 编排流程时，底层计算可调 MCP（如 sympy-mcp 验算）
