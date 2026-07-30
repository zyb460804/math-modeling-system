#Requires -Version 5.1
<#
.SYNOPSIS
    数学建模生产系统一键安装脚本（Windows PowerShell）
.DESCRIPTION
    安装 Python 核心依赖 + 可选依赖 + npm 依赖（docx-editor-cn）
    检查外部软件（Typst / pandoc）状态
.EXAMPLE
    .\setup.ps1              # 安装核心 + 提示可选
    .\setup.ps1 -Full        # 核心全部 + 可选全部
    .\setup.ps1 -CoreOnly    # 只装核心
#>
param(
    [switch]$Full,
    [switch]$CoreOnly
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Write-Step($msg) { Write-Host "`n>>> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    [!]  $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "    [X]  $msg" -ForegroundColor Red }

# ---------- 前置检查 ----------
Write-Step "环境检查"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Err "未找到 python，请先安装 Python 3.10+"
    exit 1
}
$pyVer = (python --version 2>&1)
Write-Ok "Python: $pyVer"

$hasNpm = $null -ne (Get-Command npm -ErrorAction SilentlyContinue)
if ($hasNpm) { Write-Ok "npm: $(npm --version)" } else { Write-Warn "npm 未安装（docx-editor-cn Word 公式链需要 Node.js 18+）" }

# ---------- 核心 Python 依赖 ----------
Write-Step "安装核心 Python 依赖"
pip install -r "$Root\docs\requirements_skill.txt" --quiet
if ($LASTEXITCODE -eq 0) { Write-Ok "核心依赖安装完成" } else { Write-Err "核心依赖安装失败"; exit 1 }

# ---------- 可选 Python 依赖 ----------
$installOptional = $Full -or (-not $CoreOnly)
if ($installOptional) {
    Write-Step "安装可选 Python 依赖（v4.3 工具链：图表/PDF表格/SHAP/Optuna/akshare）"
    $optionalChoice = if ($Full) { $true } else {
        $choice = Read-Host "    是否安装可选依赖？(Y/n)"
        $choice -ne 'n'
    }
    if ($optionalChoice) {
        pip install SciencePlots "camelot-py[cv]" shap optuna akshare --quiet
        if ($LASTEXITCODE -eq 0) { Write-Ok "可选依赖安装完成" } else { Write-Warn "部分可选依赖安装失败（不影响主流水线）" }
    } else {
        Write-Warn "跳过可选依赖。需要时可手动: pip install -r docs\requirements-optional.txt"
    }
}

# ---------- npm 依赖（docx-editor-cn）----------
if ($hasNpm) {
    Write-Step "安装 docx-editor-cn npm 依赖（Word 原生公式链）"
    Push-Location "$Root\.claude\skills\docx-editor-cn"
    npm install --silent 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Ok "docx-editor-cn 依赖安装完成" } else { Write-Warn "docx-editor-cn 安装失败（可选）" }
    Pop-Location
}

# ---------- RAG（可选）----------
if ($installOptional -and -not $CoreOnly) {
    $ragChoice = Read-Host "    是否安装 RAG 优秀论文检索依赖？(y/N)"
    if ($ragChoice -eq 'y') {
        Write-Step "安装 award-paper-rag 依赖"
        pip install -r "$Root\.claude\skills\award-paper-rag\scripts\requirements.txt" --quiet
        if ($LASTEXITCODE -eq 0) { Write-Ok "RAG 依赖安装完成" } else { Write-Warn "RAG 依赖安装失败（可选）" }
    }
}

# ---------- 外部软件检查 ----------
Write-Step "外部软件检查"

$typst = Get-Command typst -ErrorAction SilentlyContinue
if ($typst) { Write-Ok "Typst: $(typst --version)" }
else { Write-Warn "Typst 未安装（Typst 交付链需要）: winget install --id Typst.Typst" }

$pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if ($pandoc) { Write-Ok "pandoc: $(pandoc --version | Select-Object -First 1)" }
else { Write-Warn "pandoc 未安装（Word 原生公式链需要）: winget install --id JohnMacFarlane.Pandoc" }

# ---------- MCP 配置提示 ----------
Write-Step "MCP 配置提示"
Write-Host "    .mcp.json 中 6 个 MCP server 已配置:" -ForegroundColor White
Write-Host "    - 5 个 npx server（context7/filesystem/sequential-thinking/playwright/memory）" -ForegroundColor Gray
Write-Host "      → Claude Code 首次启动时自动下载，无需手动安装" -ForegroundColor Gray
Write-Host "    - 1 个 python server（nature-academic-search）" -ForegroundColor Gray
Write-Host "      → 如需启用: pip install -r nature-skills\skills\nature-academic-search\mcp-server\requirements.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "    记得把 .mcp.json 里 filesystem 的路径改成你的项目根目录" -ForegroundColor Yellow

# ---------- 完成 ----------
Write-Step "安装完成"
Write-Host "    下一步: 把赛题放入 problem_files\，对 Claude 说「开始生成数学建模论文」" -ForegroundColor Green
Write-Host ""
