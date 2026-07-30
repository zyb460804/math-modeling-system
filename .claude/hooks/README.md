# Hooks — 数学建模生产系统

## 目录

| 脚本 | 触发器 | 功能 | 退出码 |
|------|--------|------|--------|
| `protect_outputs.py` | PreToolUse (Write/Edit) | 阻止写入 outputs/、.claude/、resources/ | 2=阻止, 0=放行 |
| `check_python.py` | PostToolUse (Edit/Write) | .py 文件语法检查 (py_compile) | 1=语法错误, 0=通过 |
| `format_python.py` | PostToolUse (Edit/Write) | .py 文件自动格式化 (black) | 0=成功/跳过 |
| `auto_evidence_gate.py` | PostToolUse (Edit/Write) | 关键 JSON 变更时自动触发证据门禁 | 0=始终放行 |
| `log_exit_code.py` | PostToolUse (Bash) | 记录非零退出码（信息性） | 0=始终放行 |
| `check_index_sync.py` | Stop (会话结束) | 提醒更新 INDEX.md | 0=始终放行 |

## 保护范围

```
outputs/     → 只允许写入 INDEX.md
.claude/     → 完全禁止写入（保护 skills/agents/settings）
resources/   → 完全禁止写入（保护原始资料）
```

## 调试

```bash
# 测试单个 hook
echo '{"tool_input":{"file_path":"outputs/test.md"}}' | python .claude/hooks/protect_outputs.py
echo $?  # 应输出 2

echo '{"tool_input":{"file_path":"outputs/INDEX.md"}}' | python .claude/hooks/protect_outputs.py
echo $?  # 应输出 0
```

## 添加新 Hook

1. 在此目录创建 `.py` 脚本
2. 在 `.claude/settings.json` 的 `hooks` 节添加对应 matcher
3. 更新本 README