#!/usr/bin/env python3
"""
自动检测+修复包装器
在工作流的每个检测点自动调用，检测失败 → 自动修复 → 重检 → 仍失败才报告

用法:
    python auto_detect_and_fix.py --stage code          # S4: 代码运行后
    python auto_detect_and_fix.py --stage number        # S5: 数字一致性
    python auto_detect_and_fix.py --stage result        # S5: 结果合理性
    python auto_detect_and_fix.py --stage evidence      # S5: 证据门禁
    python auto_detect_and_fix.py --stage format        # S6: 格式门禁
    python auto_detect_and_fix.py --stage consistency   # S7: 一致性审计
    python auto_detect_and_fix.py --stage completeness  # S7: 完整性审计
    python auto_detect_and_fix.py --stage all           # 全部检测
    python auto_detect_and_fix.py --stage s5            # S5阶段全部
    python auto_detect_and_fix.py --stage s7            # S7阶段全部

返回码:
    0 = 检测通过（或自动修复后通过）
    1 = 检测失败（需人工介入）
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[4]
QA_DIR = ROOT / "paper_output" / "qa"
CORRECTORS_DIR = Path(__file__).parent / "auto_correctors"

# 阶段分组
STAGE_GROUPS = {
    "s4": ["code"],
    "s5": ["number", "result", "evidence", "parameter"],
    "s6": ["format", "figure", "latex", "citation", "aigc"],
    "s7": ["consistency", "completeness", "symbol"],
}

# 检测脚本配置
DETECTORS = {
    "code": {
        "script": ROOT / ".claude/skills/paper-workflow-orchestrator/scripts/run_and_verify.py",
        "fixer": CORRECTORS_DIR / "code_auto_fixer.py",
        "description": "代码运行验证",
        "max_rounds": 3,
    },
    "number": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_number_consistency.py",
        "fixer": CORRECTORS_DIR / "number_auto_fixer.py",
        "description": "数字一致性检查",
        "max_rounds": 2,
    },
    "result": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_result_reasonableness.py",
        "fixer": CORRECTORS_DIR / "evidence_auto_filler.py",
        "description": "结果合理性检查",
        "max_rounds": 2,
    },
    "evidence": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/evidence_gate.py",
        "fixer": CORRECTORS_DIR / "evidence_auto_filler.py",
        "description": "证据门禁检查",
        "max_rounds": 2,
    },
    "parameter": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_parameter_consistency.py",
        "fixer": CORRECTORS_DIR / "parameter_auto_fixer.py",
        "description": "参数一致性检查",
        "max_rounds": 2,
    },
    "format": {
        "script": ROOT / ".claude/skills/paper-formal-writer/scripts/check_paper_format.py",
        "fixer": CORRECTORS_DIR / "format_auto_fixer.py",
        "description": "格式门禁检查",
        "max_rounds": 2,
    },
    "consistency": {
        "script": ROOT / ".claude/skills/consistency-auditor/scripts/audit.py",
        "fixer": CORRECTORS_DIR / "number_auto_fixer.py",
        "description": "一致性审计",
        "max_rounds": 2,
    },
    "completeness": {
        "script": ROOT / ".claude/skills/completeness-auditor/scripts/audit.py",
        "fixer": CORRECTORS_DIR / "completeness_auto_filler.py",
        "description": "完整性审计",
        "max_rounds": 2,
    },
    "figure": {
        "script": ROOT / ".claude/skills/math-figure/scripts/render_check.py",
        "fixer": CORRECTORS_DIR / "figure_auto_fixer.py",
        "description": "图表质量检查",
        "max_rounds": 2,
    },
    "latex": {
        "script": CORRECTORS_DIR / "latex_auto_fixer.py",
        "fixer": CORRECTORS_DIR / "latex_auto_fixer.py",
        "description": "LaTeX公式检查",
        "max_rounds": 1,
        "combined": True,
    },
    "citation": {
        "script": CORRECTORS_DIR / "citation_auto_fixer.py",
        "fixer": CORRECTORS_DIR / "citation_auto_fixer.py",
        "description": "引用一致性检查",
        "max_rounds": 1,
        "combined": True,
    },
    "aigc": {
        "script": CORRECTORS_DIR / "aigc_auto_fixer.py",
        "fixer": CORRECTORS_DIR / "aigc_auto_fixer.py",
        "description": "AIGC检测扫描",
        "max_rounds": 2,
        "combined": True,
    },
    "symbol": {
        "script": CORRECTORS_DIR / "symbol_auto_fixer.py",
        "fixer": CORRECTORS_DIR / "symbol_auto_fixer.py",
        "description": "符号表一致性检查",
        "max_rounds": 1,
        "combined": True,
    },
    "code_style": {
        "script": CORRECTORS_DIR / "code_style_auto_fixer.py",
        "fixer": CORRECTORS_DIR / "code_style_auto_fixer.py",
        "description": "代码风格检查",
        "max_rounds": 1,
        "combined": True,
    },
}


def run_script(script_path: Path, extra_args: list = None) -> tuple:
    """运行脚本，返回 (passed, output)"""
    if not script_path.exists():
        return True, f"脚本不存在: {script_path}"

    cmd = ["python", str(script_path)]
    if extra_args:
        cmd.extend(extra_args)

    # 特殊参数
    if "evidence_gate" in str(script_path):
        cmd.extend(["--mode", "official"])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=180,
            cwd=str(ROOT),
            encoding="utf-8",
            errors="replace",
        )
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "脚本执行超时"
    except Exception as e:
        return False, f"脚本执行异常: {e}"


def detect_and_fix(stage: str, config: dict) -> bool:
    """检测+修复单个阶段"""
    max_rounds = config.get("max_rounds", 2)
    is_combined = config.get("combined", False)

    print(f"\n{'='*50}")
    print(f"[*] {config['description']}")
    print(f"{'='*50}")

    for round_num in range(1, max_rounds + 1):
        print(f"\n  --- 第 {round_num}/{max_rounds} 轮 ---")

        # 检测
        if is_combined:
            # combined 模式：检测时不加 --fix-all
            passed, output = run_script(config["script"])
        else:
            passed, output = run_script(config["script"])

        if passed:
            print(f"  [OK] 检测通过")
            return True

        # 检测失败，提取错误信息
        errors = []
        for line in output.split("\n"):
            line = line.strip()
            if any(kw in line.lower() for kw in ["error", "fail", "missing", "不一致", "缺失", "未通过", "偏差"]):
                errors.append(line)

        if not errors:
            errors = ["检测失败（无详细错误信息）"]

        print(f"  [!!] 检测失败 ({len(errors)} 个问题)")

        # 最后一轮不修复
        if round_num >= max_rounds:
            print(f"\n  [!!] 达到最大修正轮数 ({max_rounds})")
            print(f"  需人工介入的问题:")
            for err in errors[:5]:
                # 移除可能导致编码问题的字符
                safe_err = err.encode('ascii', 'replace').decode('ascii')
                print(f"    - {safe_err[:100]}")
            return False

        # 修复
        fixer = config.get("fixer")
        if not fixer or not fixer.exists():
            print(f"  [!] 无自动修复器")
            return False

        print(f"  [#] 自动修复...")

        # 写入错误文件
        error_file = QA_DIR / f"auto_fix_errors_{stage}.json"
        error_file.parent.mkdir(parents=True, exist_ok=True)
        error_file.write_text(
            json.dumps({"stage": stage, "errors": errors, "round": round_num}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 运行修复器
        if is_combined:
            fix_passed, fix_output = run_script(fixer, ["--fix-all"])
        else:
            fix_passed, fix_output = run_script(fixer, ["--errors", str(error_file)])

        if fix_passed:
            print(f"  [OK] 修复完成")
        else:
            print(f"  [!] 修复未完全成功，进入下一轮")

    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="自动检测+修复包装器")
    parser.add_argument("--stage", required=True, help="检测阶段（code/number/result/evidence/parameter/format/consistency/completeness/figure/latex/citation/aigc/symbol/code_style/s4/s5/s6/s7/all）")
    parser.add_argument("--max-rounds", type=int, help="最大修正轮数（覆盖默认值）")
    args = parser.parse_args()

    # 解析阶段
    stage = args.stage.lower()
    if stage == "all":
        stages = list(DETECTORS.keys())
    elif stage in STAGE_GROUPS:
        stages = STAGE_GROUPS[stage]
    elif stage in DETECTORS:
        stages = [stage]
    else:
        print(f"[!] 未知阶段: {stage}")
        print(f"    可用阶段: {', '.join(list(DETECTORS.keys()) + list(STAGE_GROUPS.keys()) + ['all'])}")
        sys.exit(1)

    print(f">>> 自动检测+修复")
    print(f"    阶段: {', '.join(stages)}")

    # 运行
    results = {}
    for s in stages:
        config = DETECTORS[s].copy()
        if args.max_rounds:
            config["max_rounds"] = args.max_rounds
        results[s] = detect_and_fix(s, config)

    # 汇总
    print(f"\n{'='*50}")
    print(f"[=] 汇总")
    print(f"{'='*50}")

    all_passed = True
    for s, passed in results.items():
        status = "[OK]" if passed else "[!!]"
        print(f"  {status} {DETECTORS[s]['description']}")
        if not passed:
            all_passed = False

    # 保存日志
    log_file = QA_DIR / "auto_detect_fix_log.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(
        json.dumps({
            "timestamp": datetime.now().isoformat(),
            "stages": stages,
            "results": results,
            "all_passed": all_passed,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if all_passed:
        print(f"\n[***] 全部通过！")
        sys.exit(0)
    else:
        print(f"\n[!] 部分阶段未通过，需人工介入")
        sys.exit(1)


if __name__ == "__main__":
    main()
