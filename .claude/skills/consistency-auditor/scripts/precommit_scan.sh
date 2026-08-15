#!/usr/bin/env bash
# ⛔⛔⛔ 已弃用（DEPRECATED，2026-08-15 round3 LOW 处置）⛔⛔⛔
# 本脚本不再维护，勿用于拦截。它已由 .git/hooks/pre-commit +
# security_check.py staged（PreToolUse 侧为 .claude/hooks/precommit_secret_guard.py）
# 取代：现役拦截链扫 git 暂存区全部文件，模式与注入检查同源维护。
#
# 为什么不能再用它拦：
#   1. 模式严重过期——下方 PATTERNS 只有 4 组 grep 形态，而 security_check.py
#      现有 12 组（32-hex 键名上下文/密码字面量/大小写不敏感键名/sk-ant 优先序
#      等，含 round2 H-2/B8 修复），二者早已分岔，且 grep 缺二进制嗅探、
#      大文件截断扫描（round3 P0-2）、路径豁免等语义；
#   2. 形态顺序本身就是错的——sk- 通用模式排在 sk-ant 之前，正是 security_check.py
#      H-2 修复前的漏报顺序（sk-ant 会被 sk- 先吃掉部分前缀）；
#   3. 无任何调用方（主仓 hook 与 settings.json 均指向 security_check.py）。
# 依赖它拦截 = 虚假安全感（例如 "api_key": <32hex> 实弹实测它直接放行）。
#
# 保留本文件仅作历史参考（git 跟踪文件，是否删除属决策层）；如需拦截，请用：
#   python .claude/skills/consistency-auditor/scripts/security_check.py staged
# ============================================================================
# precommit_scan.sh — git 提交前密钥拦截（PreToolUse hook / git pre-commit 通用）
# 融合自 AutoMCM-Pro 的"密钥提交拦截"机制。
# 检测暂存区或指定文件中的硬编码密钥，发现则阻止提交（退出 1）。
#
# 作为 git hook：软链/复制到 .git/hooks/pre-commit
# 作为 Claude Code PreToolUse hook：在 settings.json 配置
#   { "matcher": "Bash", "command": "bash .claude/skills/consistency-auditor/scripts/precommit_scan.sh" }
set -euo pipefail

# ⚠ 弃用脚本运行时警告（消灭"它还能拦"的错觉；扫描行为保留仅作参考演示）
echo "[precommit_scan.sh] ⚠ 已弃用：模式过期，不构成有效拦截。" >&2
echo "[precommit_scan.sh] ⚠ 请改用 .git/hooks/pre-commit / security_check.py staged。" >&2

# 检测模式（⚠ 已过期，勿视作与 security_check.py 同步——见文件头弃用说明）
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