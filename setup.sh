#!/usr/bin/env bash
# 数学建模生产系统一键安装脚本（macOS / Linux / Git Bash）
# 用法:
#   ./setup.sh           # 交互式（核心 + 询问可选）
#   ./setup.sh --full    # 全装
#   ./setup.sh --core    # 只装核心
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

mode="${1:---interactive}"

echo ""
echo ">>> 环境检查"
python --version || { echo "未找到 python，请先安装 Python 3.10+"; exit 1; }
command -v npm >/dev/null && echo "    [OK] npm $(npm --version)" || echo "    [!]  npm 未安装（docx-editor-cn 需要 Node.js 18+）"

echo ""
echo ">>> 安装核心 Python 依赖"
pip install -r "$ROOT/docs/requirements_skill.txt" --quiet
echo "    [OK] 核心依赖完成"

if [ "$mode" != "--core" ]; then
    echo ""
    if [ "$mode" = "--full" ]; then
        choice="y"
    else
        read -p "    是否安装可选依赖（图表/PDF表格/SHAP/Optuna/akshare）？(y/n) " choice
    fi
    if [ "$choice" = "y" ]; then
        echo ">>> 安装可选 Python 依赖"
        pip install SciencePlots "camelot-py[cv]" shap optuna akshare --quiet && echo "    [OK] 可选依赖完成" || echo "    [!]  部分可选依赖失败（不影响主流程）"
    fi
fi

if command -v npm >/dev/null; then
    echo ""
    echo ">>> 安装 docx-editor-cn npm 依赖"
    cd "$ROOT/.claude/skills/docx-editor-cn" && npm install --silent && echo "    [OK] docx-editor-cn 完成" || echo "    [!]  安装失败（可选）"
    cd "$ROOT"
fi

echo ""
echo ">>> 外部软件检查"
command -v typst >/dev/null && echo "    [OK] Typst $(typst --version)" || echo "    [!]  Typst 未装（Typst 交付链需要）"
command -v pandoc >/dev/null && echo "    [OK] pandoc $(pandoc --version | head -1)" || echo "    [!]  pandoc 未装（Word 公式链需要）"

echo ""
echo ">>> MCP 配置提示"
echo "    .mcp.json 里 5 个 npx server 首次启动 Claude Code 时自动下载"
echo "    nature-academic-search (python MCP) 按需: pip install -r nature-skills/skills/nature-academic-search/mcp-server/requirements.txt"
echo "    记得把 .mcp.json 里 filesystem 的路径改成你的项目根目录"

echo ""
echo ">>> 完成。把赛题放入 problem_files/，对 Claude 说「开始生成数学建模论文」"
