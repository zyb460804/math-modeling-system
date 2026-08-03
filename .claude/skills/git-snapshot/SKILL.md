---
name: git-snapshot
description: "创建项目时间点快照，保留最近10个版本。触发词：git快照、项目快照、snapshot、版本快照、时间点快照、打快照。"
---

# /git-snapshot — 项目快照与版本保护

## 触发条件
用户说"存档"、"快照"、"备份"、"snapshot"、"checkpoint"、"save"时调用。

## 工作流

### 1. 扫描当前状态
列出项目下所有非 `.git` 目录的顶层文件和目录，记录：
- 文件数量（按扩展名统计：.py / .m / .md / .docx / .pdf / .csv / .txt / .svg / .png / .yaml / .json）
- 最近修改的 5 个文件

### 2. 创建快照
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$snapshotDir = "e:\数学建模\snapshots\$timestamp"
New-Item -ItemType Directory -Path $snapshotDir -Force

# 只快照关键文件夹（排除 snapshots/、nature-skills/、__pycache__/）
$folders = @("prompts", "outputs", "deliverables", ".claude")
foreach ($f in $folders) {
    if (Test-Path "e:\数学建模\$f") {
        Copy-Item "e:\数学建模\$f" "$snapshotDir\$f" -Recurse -Force
    }
}
# 快照根目录关键文件
$files = @("CLAUDE.md", "AGENTS.md", "README.md")
# MASTER_PROMPT_math_modeling.txt 已移入 prompts/，随 $folders 中的 prompts 整体备份
foreach ($f in $files) {
    if (Test-Path "e:\数学建模\$f") {
        Copy-Item "e:\数学建模\$f" "$snapshotDir\$f" -Force
    }
}
```

### 3. 生成快照报告
输出快照目录路径、文件统计、与上次快照的差异（如果有上次快照）。

### 4. 清理旧快照
保留最近 10 个快照，删除更早的。