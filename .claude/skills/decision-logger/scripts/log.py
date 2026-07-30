#!/usr/bin/env python3
"""
决策日志记录脚本

记录用户在选模、结果判断等关键节点的决策理由。

用法：
    python log.py --gate G2.5 --question Q1 --decision "熵权TOPSIS" --reason "..."
    python log.py --show
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 配置 UTF-8 输出
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 路径配置
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
DECISION_LOG = QA_DIR / "decision_log.json"

# 门禁定义
GATES = {
    "G2.5": {
        "name": "方法选择决策",
        "step": "method_selection",
        "min_reason_length": 50,
        "required_fields": ["decision", "reason", "question"]
    },
    "G4.5": {
        "name": "结果判断决策",
        "step": "result_verification",
        "min_reason_length": 30,
        "required_fields": ["decision", "reason", "question"]
    },
    "G1": {
        "name": "问题拆解确认",
        "step": "problem_confirmation",
        "min_reason_length": 20,
        "required_fields": ["decision", "reason"]
    },
    "G3": {
        "name": "代码审查确认",
        "step": "code_review_confirmation",
        "min_reason_length": 20,
        "required_fields": ["decision", "reason"]
    }
}

# AI生成的模板文本（禁止使用）
AI_TEMPLATE_PHRASES = [
    "基于以上分析",
    "综合考虑",
    "根据数据特征",
    "考虑到问题特点",
    "经过分析",
    "根据常见做法",
    "基于经验",
    "参考相关文献",
]


def load_decision_log() -> dict:
    """加载决策日志"""
    if not DECISION_LOG.exists():
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "decisions": [],
            "metadata": {
                "total_decisions": 0,
                "user_overrode_ai_count": 0,
                "last_updated": datetime.now().isoformat()
            }
        }

    try:
        return json.loads(DECISION_LOG.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠️ 加载决策日志失败: {exc}")
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "decisions": [],
            "metadata": {
                "total_decisions": 0,
                "user_overrode_ai_count": 0,
                "last_updated": datetime.now().isoformat()
            }
        }


def save_decision_log(log: dict):
    """保存决策日志"""
    QA_DIR.mkdir(parents=True, exist_ok=True)

    # 更新元数据
    log["metadata"]["total_decisions"] = len(log["decisions"])
    log["metadata"]["last_updated"] = datetime.now().isoformat()

    # 统计用户覆盖AI建议的次数
    override_count = sum(1 for d in log["decisions"] if d.get("user_overrode_ai", False))
    log["metadata"]["user_overrode_ai_count"] = override_count

    # 保存JSON
    DECISION_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 决策日志已保存: {DECISION_LOG}")


def validate_reason(reason: str, gate_config: dict) -> tuple[bool, str]:
    """验证决策理由"""
    min_length = gate_config.get("min_reason_length", 20)

    # 检查长度
    if len(reason.strip()) < min_length:
        return False, f"决策理由太短（至少{min_length}字）"

    # 检查是否是AI模板
    for phrase in AI_TEMPLATE_PHRASES:
        if reason.strip().startswith(phrase):
            return False, f"决策理由不能以AI模板开头：'{phrase}'"

    # 检查是否是简单的同意
    simple_responses = ["同意", "可以", "好的", "没问题", "accept", "ok", "yes"]
    if reason.strip().lower() in simple_responses:
        return False, "决策理由不能只是简单的同意"

    return True, ""


def add_decision(gate: str, question: str, decision: str, reason: str,
                 candidates: list = None, ai_suggestion: str = None,
                 key_results: dict = None, concerns: list = None):
    """添加决策记录"""
    # 验证门禁
    if gate not in GATES:
        print(f"❌ 未知门禁: {gate}")
        print(f"   可用门禁: {', '.join(GATES.keys())}")
        return False

    gate_config = GATES[gate]

    # 验证必填字段
    if not decision:
        print("❌ 决策不能为空")
        return False

    if not reason:
        print("❌ 决策理由不能为空")
        return False

    # 验证理由质量
    is_valid, error_msg = validate_reason(reason, gate_config)
    if not is_valid:
        print(f"❌ {error_msg}")
        return False

    # 加载日志
    log = load_decision_log()

    # 创建决策记录
    decision_record = {
        "id": f"decision_{len(log['decisions']) + 1:03d}",
        "gate": gate,
        "step": gate_config["step"],
        "question": question or "GLOBAL",
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "reason": reason,
        "source": "user"
    }

    # 添加可选字段
    if candidates:
        decision_record["candidates"] = candidates

    if ai_suggestion:
        decision_record["ai_suggestion"] = ai_suggestion
        decision_record["user_overrode_ai"] = (decision != ai_suggestion)

    if key_results:
        decision_record["key_results"] = key_results

    if concerns:
        decision_record["concerns"] = concerns

    # 添加到日志
    log["decisions"].append(decision_record)

    # 保存
    save_decision_log(log)

    print(f"✅ 决策已记录: {gate} - {gate_config['name']}")
    print(f"   子问题: {decision_record['question']}")
    print(f"   决策: {decision}")
    print(f"   理由: {reason[:50]}...")

    return True


def show_decision_log():
    """显示决策日志"""
    log = load_decision_log()

    if not log["decisions"]:
        print("📋 决策日志为空")
        return

    print("=" * 60)
    print("决策日志")
    print("=" * 60)
    print(f"创建时间: {log.get('created_at', 'N/A')}")
    print(f"总决策数: {log['metadata']['total_decisions']}")
    print(f"用户覆盖AI建议: {log['metadata']['user_overrode_ai_count']}次")
    print("")

    for i, decision in enumerate(log["decisions"], 1):
        gate = decision.get("gate", "N/A")
        step = decision.get("step", "N/A")
        question = decision.get("question", "N/A")
        timestamp = decision.get("timestamp", "N/A")
        dec = decision.get("decision", "N/A")
        reason = decision.get("reason", "N/A")
        source = decision.get("source", "N/A")
        override = decision.get("user_overrode_ai", False)

        print(f"### {i}. {gate} - {step} ({question})")
        print(f"时间: {timestamp}")
        print(f"决策: {dec}")
        print(f"理由: {reason}")
        print(f"来源: {source}")

        if override:
            print(f"✅ 用户覆盖AI建议")

        if "ai_suggestion" in decision:
            print(f"AI建议: {decision['ai_suggestion']}")

        if "candidates" in decision:
            print("候选方案:")
            for candidate in decision["candidates"]:
                status = "✅" if candidate.get("poc_status") == "PASS" else "❌"
                score = candidate.get("score", "N/A")
                print(f"  {status} {candidate.get('name', 'N/A')} (得分: {score})")

        if "key_results" in decision:
            print("关键结果:")
            for key, value in decision["key_results"].items():
                print(f"  - {key}: {value}")

        if "concerns" in decision and decision["concerns"]:
            print("用户关切:")
            for concern in decision["concerns"]:
                print(f"  - {concern}")

        print("")

    print("=" * 60)


def check_gate(gate: str, question: str = None) -> bool:
    """检查门禁是否满足"""
    log = load_decision_log()

    if gate not in GATES:
        print(f"❌ 未知门禁: {gate}")
        return False

    gate_config = GATES[gate]

    # 查找匹配的决策
    for decision in log["decisions"]:
        if decision.get("gate") != gate:
            continue

        if question and decision.get("question") != question:
            continue

        # 检查理由长度
        reason = decision.get("reason", "")
        min_length = gate_config.get("min_reason_length", 20)
        if len(reason.strip()) < min_length:
            print(f"❌ 决策理由太短（至少{min_length}字）")
            return False

        print(f"✅ 门禁 {gate} 已满足")
        print(f"   决策: {decision.get('decision')}")
        print(f"   时间: {decision.get('timestamp')}")
        return True

    print(f"❌ 门禁 {gate} 未满足：未找到决策记录")
    return False


def main():
    parser = argparse.ArgumentParser(description="决策日志记录脚本")

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 添加决策
    add_parser = subparsers.add_parser("add", help="添加决策")
    add_parser.add_argument("--gate", type=str, required=True,
                            help="门禁编号（如G2.5, G4.5）")
    add_parser.add_argument("--question", type=str, default=None,
                            help="子问题（如Q1）")
    add_parser.add_argument("--decision", type=str, required=True,
                            help="决策内容")
    add_parser.add_argument("--reason", type=str, required=True,
                            help="决策理由")
    add_parser.add_argument("--ai-suggestion", type=str, default=None,
                            help="AI建议")
    add_parser.add_argument("--candidates", type=str, default=None,
                            help="候选方案（JSON格式）")
    add_parser.add_argument("--key-results", type=str, default=None,
                            help="关键结果（JSON格式）")
    add_parser.add_argument("--concerns", type=str, default=None,
                            help="用户关切（JSON格式）")

    # 显示日志
    show_parser = subparsers.add_parser("show", help="显示决策日志")

    # 检查门禁
    check_parser = subparsers.add_parser("check", help="检查门禁")
    check_parser.add_argument("--gate", type=str, required=True,
                              help="门禁编号")
    check_parser.add_argument("--question", type=str, default=None,
                              help="子问题")

    args = parser.parse_args()

    if args.command == "add":
        # 解析JSON参数
        candidates = json.loads(args.candidates) if args.candidates else None
        key_results = json.loads(args.key_results) if args.key_results else None
        concerns = json.loads(args.concerns) if args.concerns else None

        success = add_decision(
            gate=args.gate,
            question=args.question,
            decision=args.decision,
            reason=args.reason,
            candidates=candidates,
            ai_suggestion=args.ai_suggestion,
            key_results=key_results,
            concerns=concerns
        )

        sys.exit(0 if success else 1)

    elif args.command == "show":
        show_decision_log()

    elif args.command == "check":
        success = check_gate(args.gate, args.question)
        sys.exit(0 if success else 1)

    else:
        # 默认显示日志
        show_decision_log()


if __name__ == "__main__":
    main()