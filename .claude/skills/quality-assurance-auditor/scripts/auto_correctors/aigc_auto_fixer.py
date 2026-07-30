#!/usr/bin/env python3
"""
AIGC 检测自动修复器
检测 AI 痕迹过高 → 自动应用降重策略

用法:
    python aigc_auto_fixer.py --errors path/to/errors.json
    python aigc_auto_fixer.py --paper paper_output/final_paper_source.md
    python aigc_auto_fixer.py --fix-all
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PAPER_SOURCE = ROOT / "paper_output" / "final_paper_source.md"

# 8 类 AI 痕迹模式（来自 anti-ai-detection-guide.md）
AI_PATTERNS = [
    {
        "name": "过度强调词",
        "pattern": r"(?:至关重要|不可或缺|举足轻重|尤为关键|极为重要|显著影响|深刻理解|全面分析)",
        "replacement": {
            "至关重要": "重要",
            "不可或缺": "需要",
            "举足轻重": "重要",
            "尤为关键": "较重要",
            "极为重要": "很重要",
            "显著影响": "影响",
            "深刻理解": "理解",
            "全面分析": "分析",
        },
    },
    {
        "name": "广告语言",
        "pattern": r"(?:突破性|革命性|令人震撼|划时代|里程碑|卓越|非凡|无与伦比)",
        "replacement": {
            "突破性": "新的",
            "革命性": "创新的",
            "令人震撼": "显著的",
            "划时代": "重要的",
            "里程碑": "关键",
            "卓越": "良好",
            "非凡": "较好",
            "无与伦比": "优异",
        },
    },
    {
        "name": "模糊归因",
        "pattern": r"(?:专家认为|研究表明|众所周知|不言而喻|毋庸置疑|事实上)",
        "replacement": {
            "专家认为": "文献[X]指出",
            "研究表明": "文献[X]结果显示",
            "众所周知": "",
            "不言而喻": "",
            "毋庸置疑": "",
            "事实上": "",
        },
    },
    {
        "name": "AI高频词",
        "pattern": r"(?:此外|另外|值得注意的是|需要指出的是|总而言之|综上所述|基于此|在此基础上)",
        "replacement": {
            "此外": "同时",
            "另外": "补充",
            "值得注意的是": "",
            "需要指出的是": "",
            "总而言之": "",
            "综上所述": "总结",
            "基于此": "据此",
            "在此基础上": "进一步",
        },
    },
    {
        "name": "套话开头",
        "pattern": r"(?:在当今|随着.*的快速发展|在.*领域|近年来|随着.*的不断深入)",
        "replacement": None,  # 需要上下文判断
    },
    {
        "name": "三段式强迫",
        "pattern": r"(?:首先.*其次.*最后|一方面.*另一方面.*此外|第一.*第二.*第三)",
        "replacement": None,  # 需要上下文判断
    },
    {
        "name": "同义词循环",
        "pattern": r"(?:模型|算法|方法|方案|策略|技术|手段|途径)(?:.*?(?:模型|算法|方法|方案|策略|技术|手段|途径)){2,}",
        "replacement": None,  # 需要上下文判断
    },
    {
        "name": "挑战与展望套话",
        "pattern": r"(?:尽管.*但是.*仍然|虽然.*不过.*依然|尽管取得了.*但仍面临|挑战与机遇并存)",
        "replacement": None,  # 需要上下文判断
    },
]


def scan_ai_patterns(paper_text: str) -> list:
    """扫描论文中的 AI 痕迹"""
    findings = []

    for pattern_info in AI_PATTERNS:
        matches = list(re.finditer(pattern_info["pattern"], paper_text))
        if matches:
            findings.append({
                "name": pattern_info["name"],
                "count": len(matches),
                "pattern": pattern_info["pattern"],
                "replacement": pattern_info.get("replacement"),
                "examples": [m.group(0) for m in matches[:3]],
            })

    return findings


def fix_ai_patterns(paper_text: str, findings: list) -> tuple:
    """修正 AI 痕迹"""
    fixed_count = 0

    for finding in findings:
        if finding["replacement"]:
            # 有明确替换规则
            for old, new in finding["replacement"].items():
                if old in paper_text:
                    paper_text = paper_text.replace(old, new)
                    fixed_count += 1
                    print(f"    [>] {finding['name']}: '{old}' -> '{new}'")
        else:
            # 需要上下文判断，只标记
            print(f"    [!] {finding['name']}: {finding['count']} 处，需人工判断")

    return paper_text, fixed_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AIGC 检测自动修复器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--paper", default=str(PAPER_SOURCE), help="论文文件路径")
    parser.add_argument("--fix-all", action="store_true", help="修复所有 AI 痕迹")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    if not paper_path.exists():
        print(f"[!] 论文文件不存在: {paper_path}")
        sys.exit(1)

    paper_text = paper_path.read_text(encoding="utf-8")

    print("[*] AIGC 检测扫描")

    # 统计字数
    cn_chars = len(re.findall(r"[一-鿿]", paper_text))
    print(f"    中文字数: {cn_chars}")

    # 扫描 AI 痕迹
    findings = scan_ai_patterns(paper_text)

    if not findings:
        print("[OK] 未发现明显 AI 痕迹")
        sys.exit(0)

    total_issues = sum(f["count"] for f in findings)
    print(f"\n[!] 发现 {len(findings)} 类 AI 痕迹，共 {total_issues} 处:")

    for f in findings:
        examples = ", ".join(f["examples"][:3])
        print(f"    - {f['name']}: {f['count']} 处 (例: {examples})")

    if args.fix_all or args.errors:
        print(f"\n[#] 自动修正...")
        fixed_text, fixed_count = fix_ai_patterns(paper_text, findings)

        if fixed_count > 0:
            paper_path.write_text(fixed_text, encoding="utf-8")
            print(f"\n[OK] 已修正 {fixed_count} 类 AI 痕迹")

            # 重新扫描
            new_findings = scan_ai_patterns(fixed_text)
            new_total = sum(f["count"] for f in new_findings)
            print(f"[>] 修正后剩余: {new_total} 处")
        else:
            print(f"\n[!] 无法自动修正，需人工处理")
            sys.exit(1)
    else:
        print("\n使用 --fix-all 自动修正")
        sys.exit(1)


if __name__ == "__main__":
    main()
