#!/usr/bin/env python3
"""批量删除 outputs/ 文件中的"系统同步说明"模板头部冗余。

删除策略：按首尾标记匹配，不依赖固定字符串：
- 首标记：包含 "系统同步说明：本文件已纳入" 的行
- 尾标记：同一行或后续行中包含 "不得编造。" 的行
- 只删除首尾之间的行（含首尾），保留文件其余内容
- 清理删除后可能残留的多余空行

安全保证：
- 只处理包含首标记的文件
- 删除前后报告 diff 统计
- 不会触碰不含首标记的文件
"""
import re
import sys
from pathlib import Path

START_MARKER = "系统同步说明：本文件已纳入"
END_MARKER = "不得编造。"

def strip_boilerplate(filepath: Path) -> dict:
    """删除单个文件的模板头部，返回统计。"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    if START_MARKER not in content:
        return {"file": str(filepath), "action": "skip", "reason": "no marker"}

    # 找首标记行
    start_idx = None
    for i, line in enumerate(lines):
        if START_MARKER in line:
            start_idx = i
            break

    if start_idx is None:
        return {"file": str(filepath), "action": "skip", "reason": "marker not found in lines"}

    # 从首标记向后找尾标记
    end_idx = None
    for i in range(start_idx, len(lines)):
        if END_MARKER in lines[i]:
            end_idx = i
            break

    if end_idx is None:
        return {"file": str(filepath), "action": "skip", "reason": "end marker not found"}

    # 删除 start_idx 到 end_idx（含）
    removed_lines = lines[start_idx : end_idx + 1]
    removed_bytes = sum(len(l) + 1 for l in removed_lines)  # +1 for \n

    new_lines = lines[:start_idx] + lines[end_idx + 1 :]

    # 清理残留的多余空行（如果删除后留下 2+ 连续空行，压缩为 1 个）
    cleaned = []
    blank_streak = 0
    for line in new_lines:
        if line.strip() == "":
            blank_streak += 1
            if blank_streak <= 1:
                cleaned.append(line)
        else:
            blank_streak = 0
            cleaned.append(line)

    # 去除开头的空行（如果删除后文件以空行开头）
    while cleaned and cleaned[0].strip() == "":
        cleaned.pop(0)

    new_content = "\n".join(cleaned)

    # 写回
    filepath.write_text(new_content, encoding="utf-8")

    return {
        "file": str(filepath),
        "action": "stripped",
        "removed_lines": len(removed_lines),
        "removed_bytes": removed_bytes,
    }


def main():
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        print("[ERROR] outputs/ directory not found")
        sys.exit(1)

    # 只处理 .md 文件
    md_files = sorted(outputs_dir.glob("*.md"))
    print(f"扫描 {len(md_files)} 个 .md 文件\n")

    stats = {"stripped": 0, "skip": 0, "total_removed_bytes": 0}
    details = []

    for f in md_files:
        result = strip_boilerplate(f)
        details.append(result)
        if result["action"] == "stripped":
            stats["stripped"] += 1
            stats["total_removed_bytes"] += result["removed_bytes"]
            print(f"  [STRIPPED] {f.name} (-{result['removed_bytes']} bytes, -{result['removed_lines']} lines)")
        else:
            stats["skip"] += 1

    print(f"\n=== 汇总 ===")
    print(f"  处理文件: {len(md_files)}")
    print(f"  已删除模板: {stats['stripped']}")
    print(f"  跳过: {stats['skip']}")
    print(f"  总删除字节: {stats['total_removed_bytes']} (~{stats['total_removed_bytes'] // 1024} KB)")
    print(f"  总删除 token（估算）: ~{stats['total_removed_bytes'] * 2 // 5}")


if __name__ == "__main__":
    main()
