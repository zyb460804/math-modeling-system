#!/usr/bin/env bash
# precommit_scan.sh — git 提交前密钥拦截（PreToolUse hook / git pre-commit 通用）
# 融合自 AutoMCM-Pro 的"密钥提交拦截"机制。
# 检测暂存区或指定文件中的硬编码密钥，发现则阻止提交（退出 1）。
#
# 作为 git hook：软链/复制到 .git/hooks/pre-commit
# 作为 Claude Code PreToolUse hook：在 settings.json 配置
#   { "matcher": "Bash", "command": "bash .claude/skills/consistency-auditor/scripts/precommit_scan.sh" }
set -euo pipefail

# 检测模式（与 security_check.py 同步）
PATTERNS='(sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9\-]{20,}|ghp_[A-Za-z0-9]{36}|AKIA[A-Z0-9]{16})'

# 待扫描文件：优先 git 暂存区；无 git 时扫传入参数；都没有则跳过
FILES=()
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    while IFS= read -r f; do
        [ -f "$f" ] && FILES+=("$f")
    done < <(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
fi
# 追加命令行参数（用于 PreToolUse 传 $FILE_PATH）
for a in "$@"; do [ -f "$a" ] && FILES+=("$a"); done

if [ ${#FILES[@]} -eq 0 ]; then
    exit 0
fi

HITS=0
for f in "${FILES[@]}"; do
    # 只扫文本文件
    case "$f" in
        *.py|*.md|*.tex|*.typ|*.json|*.js|*.ts|*.sh|*.yml|*.yaml|*.toml|*.env|*.ini) ;;
        *) continue ;;
    esac
    if grep -nE "$PATTERNS" "$f" >/dev/null 2>&1; then
        echo "[precommit] ✗ 检测到疑似密钥，阻止提交：" >&2
        grep -nE "$PATTERNS" "$f" | head -5 | sed 's/^/    /' >&2
        echo "    文件: $f" >&2
        echo "    请改用环境变量，或从文件中移除密钥后再提交。" >&2
        HITS=$((HITS + 1))
    fi
done

if [ "$HITS" -gt 0 ]; then
    exit 1
fi
exit 0