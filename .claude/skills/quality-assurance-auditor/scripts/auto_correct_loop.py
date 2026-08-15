#!/usr/bin/env python3
"""
自动回环修正器 v4.0
检测失败 → 定位问题 → 自动修正 → 重检 → 仍失败 → 再修正（最多3轮）→ 仍失败才报告用户

用法:
    python auto_correct_loop.py                    # 运行全部检测+自动修正
    python auto_correct_loop.py --stage code       # 只跑代码阶段
    python auto_correct_loop.py --stage number     # 只跑数字一致性
    python auto_correct_loop.py --stage evidence   # 只跑证据完整性
    python auto_correct_loop.py --stage format     # 只跑格式检查
    python auto_correct_loop.py --max-rounds 5     # 最多5轮
    python auto_correct_loop.py --dry-run          # 只检测不修正
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# 项目根目录
ROOT = Path(__file__).resolve().parents[4]
QA_DIR = ROOT / "paper_output" / "qa"
CORRECTORS_DIR = Path(__file__).parent / "auto_correctors"

# 检测脚本映射
DETECTORS = {
    "code": {
        "script": ROOT / ".claude/skills/paper-workflow-orchestrator/scripts/run_and_verify.py",
        "description": "代码运行验证",
        "fixer": CORRECTORS_DIR / "code_auto_fixer.py",
        "fix_description": "自动修复代码错误",
    },
    "number": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_number_consistency.py",
        "description": "数字一致性检查",
        "fixer": CORRECTORS_DIR / "number_auto_fixer.py",
        "fix_description": "自动修正论文数字",
    },
    "result": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_result_reasonableness.py",
        "description": "结果合理性检查",
        "fixer": CORRECTORS_DIR / "evidence_auto_filler.py",
        "fix_description": "自动补齐缺失证据",
    },
    "format": {
        "script": ROOT / ".claude/skills/paper-formal-writer/scripts/check_paper_format.py",
        "description": "格式门禁检查",
        "fixer": CORRECTORS_DIR / "format_auto_fixer.py",
        "fix_description": "自动修正格式问题",
    },
    "evidence": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/evidence_gate.py",
        "description": "证据门禁检查",
        "fixer": CORRECTORS_DIR / "evidence_auto_filler.py",
        "fix_description": "自动补齐缺失证据",
    },
    "parameter": {
        "script": ROOT / ".claude/skills/quality-assurance-auditor/scripts/check_parameter_consistency.py",
        "description": "参数一致性检查",
        "fixer": CORRECTORS_DIR / "parameter_auto_fixer.py",
        "fix_description": "自动修正代码参数（以题目为准）",
    },
    "consistency": {
        "script": ROOT / ".claude/skills/consistency-auditor/scripts/audit.py",
        "description": "一致性审计",
        "fixer": CORRECTORS_DIR / "number_auto_fixer.py",
        "fix_description": "自动修正不一致项",
    },
    "figure": {
        "script": ROOT / ".claude/skills/math-figure/scripts/render_check.py",
        "description": "图表质量检查",
        "fixer": CORRECTORS_DIR / "figure_auto_fixer.py",
        "fix_description": "自动修正图表参数并重新渲染",
        # render_check.py 是子命令式 CLI，不带子命令只打印 help 且 rc=0——
        # 必须显式传 check-all 并消费其 rc（与 auto_detect_and_fix.py 同源修复）
        "args": ["check-all"],
    },
    "latex": {
        "script": ROOT / ".claude/skills/latex-renderer/scripts/render_formulas.py",
        "description": "LaTeX公式渲染",
        "fixer": CORRECTORS_DIR / "latex_auto_fixer.py",
        "fix_description": "自动修正LaTeX语法错误",
    },
    "completeness": {
        "script": ROOT / ".claude/skills/completeness-auditor/scripts/audit.py",
        "description": "完整性审计",
        "fixer": CORRECTORS_DIR / "completeness_auto_filler.py",
        "fix_description": "自动补齐缺失文件和目录",
    },
    "citation": {
        "script": CORRECTORS_DIR / "citation_auto_fixer.py",
        "description": "引用一致性检查",
        "fixer": CORRECTORS_DIR / "citation_auto_fixer.py",
        "fix_description": "自动修正引用格式和断链",
        "combined": True,
    },
    "aigc": {
        "script": CORRECTORS_DIR / "aigc_auto_fixer.py",
        "description": "AIGC检测扫描",
        "fixer": CORRECTORS_DIR / "aigc_auto_fixer.py",
        "fix_description": "自动降低AI痕迹",
        "combined": True,
    },
    "symbol": {
        "script": CORRECTORS_DIR / "symbol_auto_fixer.py",
        "description": "符号表一致性检查",
        "fixer": CORRECTORS_DIR / "symbol_auto_fixer.py",
        "fix_description": "自动解决符号冲突",
        "combined": True,
    },
    "code_style": {
        "script": CORRECTORS_DIR / "code_style_auto_fixer.py",
        "description": "代码风格检查",
        "fixer": CORRECTORS_DIR / "code_style_auto_fixer.py",
        "fix_description": "自动格式化代码",
        "combined": True,
    },
}

# 修正报告
CORRECTION_LOG = []


def _skip_reason(output: str) -> str | None:
    """rc=0 的输出是否实为 SKIP（口径复制自 auto_detect_and_fix.py）。

    number/result/parameter 缺 qa_config 时 rc=0 且行首打印 "SKIP（...）：..."——
    "未实际检查"不能冒充"检测通过"，调用方据此以 [--] SKIP 明示。
    """
    for ln in output.splitlines():
        low = ln.strip().lower()
        if low.startswith("skip") or low.startswith("[skip]"):
            return ln.strip()
    return None


def run_detector(name: str, config: dict) -> dict:
    """运行检测脚本，返回 {passed, errors, output, skip_reason}

    fail-closed 对齐（auto_detect_and_fix.py 同源修复，旧版三处假绿）：
    - 检测脚本不存在 = FAIL（旧版 return passed=True 使任一检测器路径失效都显示"通过"）；
    - 子进程解释器用 sys.executable（本机全局 python 指向坏 venv，PATH 上的 "python" 不可用）；
    - 检测器自定义参数经 config["args"] 透传（figure 的 render_check.py 不带子命令
      只打印 help 且 rc=0，旧写法使图表检测通道恒绿）；
    - rc=0 但输出行首 SKIP = 未实际检查，返回 skip_reason 供调用方明示（不冒充通过）。
    """
    script = config["script"]
    if not script.exists():
        msg = f"检测脚本不存在: {script}"
        return {"passed": False, "errors": [msg], "output": msg, "skip_reason": None}

    print(f"  [?] 检测: {config['description']}...")

    # 构建命令
    cmd = [sys.executable, str(script)]
    cmd.extend(config.get("args") or [])
    # 证据门禁需要 --mode official 参数
    if "evidence_gate" in str(script):
        cmd.extend(["--mode", "official"])
    # combined 模式：检测时不加 --fix-all
    if config.get("combined"):
        pass  # 不加 --fix-all，只做检测

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
            cwd=str(ROOT),
            encoding="utf-8",
            errors="replace",
        )
        output = (result.stdout or "") + (result.stderr or "")
        passed = result.returncode == 0
        skip_reason = _skip_reason(output) if passed else None

        # 解析错误信息
        errors = []
        if not passed:
            # 尝试解析 JSON 报告
            for report_name in [
                "workflow_guard_report.json",
                "evidence_gate_report.json",
                "consistency_audit_report.json",
            ]:
                report_path = QA_DIR / report_name
                if report_path.exists():
                    try:
                        report = json.loads(report_path.read_text(encoding="utf-8"))
                        if "errors" in report:
                            errors.extend(report["errors"])
                        elif "failures" in report:
                            errors.extend(report["failures"])
                        elif "issues" in report:
                            errors.extend(report["issues"])
                    except Exception:
                        pass

            # 从输出中提取错误
            if not errors:
                for line in output.split("\n"):
                    line = line.strip()
                    if any(
                        kw in line.lower()
                        for kw in ["error", "fail", "missing", "不一致", "缺失", "不合格", "未通过"]
                    ):
                        errors.append(line)

        status = "[OK] PASS" if passed else "[!!] FAIL"
        print(f"    {status} ({len(errors)} 个问题)")
        return {"passed": passed, "errors": errors, "output": output, "skip_reason": skip_reason}

    except subprocess.TimeoutExpired:
        print("    [~] 超时")
        return {"passed": False, "errors": ["检测超时"], "output": ""}
    except Exception as e:
        print(f"    [X] 异常: {e}")
        return {"passed": False, "errors": [str(e)], "output": ""}


def run_fixer(name: str, config: dict, errors: list) -> bool:
    """运行修复脚本，返回是否成功修复"""
    fixer = config.get("fixer")
    if not fixer or not fixer.exists():
        print(f"    [!] 无自动修复器: {config['fix_description']}")
        return False

    print(f"  [#] 修复: {config['fix_description']}...")

    # 将错误信息写入临时文件供修复器读取
    error_file = QA_DIR / f"auto_correct_errors_{name}.json"
    error_file.parent.mkdir(parents=True, exist_ok=True)
    error_file.write_text(
        json.dumps({"stage": name, "errors": errors, "timestamp": datetime.now().isoformat()}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 构建修复命令（解释器用 sys.executable：本机 PATH 上的 "python" 是坏 venv）
    fix_cmd = [sys.executable, str(fixer), "--errors", str(error_file)]
    # combined 模式：修复时加 --fix-all
    if config.get("combined"):
        fix_cmd = [sys.executable, str(fixer), "--fix-all"]

    try:
        result = subprocess.run(
            fix_cmd,
            capture_output=True,
            timeout=180,
            cwd=str(ROOT),
            encoding="utf-8",
            errors="replace",
        )
        output = (result.stdout or "") + (result.stderr or "")
        success = result.returncode == 0

        if success:
            print(f"    [OK] 修复完成")
        else:
            print(f"    [!!] 修复失败")
            # 提取失败原因
            for line in output.split("\n"):
                if "error" in line.lower() or "fail" in line.lower():
                    print(f"      → {line.strip()}")

        CORRECTION_LOG.append({
            "stage": name,
            "round": len(CORRECTION_LOG) + 1,
            "errors_count": len(errors),
            "fix_success": success,
            "output": output[:500],
        })

        return success

    except subprocess.TimeoutExpired:
        print(f"    [~] 修复超时")
        return False
    except Exception as e:
        print(f"    [X] 修复异常: {e}")
        return False


def run_stage(name: str, max_rounds: int = 3, dry_run: bool = False) -> bool:
    """运行单个阶段的检测-修复循环"""
    config = DETECTORS.get(name)
    if not config:
        print(f"[!!] 未知阶段: {name}")
        return False

    print(f"\n{'='*60}")
    print(f"[*] 阶段: {config['description']}")
    print(f"{'='*60}")

    for round_num in range(1, max_rounds + 1):
        print(f"\n  --- 第 {round_num}/{max_rounds} 轮 ---")

        # 检测
        result = run_detector(name, config)

        if result.get("skip_reason"):
            # rc=0 但行首 SKIP（如缺 qa_config）：未实际检查 ≠ 通过，明示后不阻断
            print(f"\n  [--] SKIP（未实际检查 ≠ 通过）：{result['skip_reason']}")
            return True

        if result["passed"]:
            print(f"\n  [OK] {config['description']} 通过")
            return True

        # 已通过，不需要修复
        if dry_run:
            print(f"\n  [*] dry-run 模式，跳过修复")
            print(f"  发现 {len(result['errors'])} 个问题:")
            for err in result["errors"][:5]:
                print(f"    - {err[:100]}")
            return False

        # 修复
        if round_num < max_rounds:
            fixed = run_fixer(name, config, result["errors"])
            if not fixed:
                print(f"\n  [!] 自动修复失败，进入下一轮检测")
        else:
            print(f"\n  [!!] 达到最大修正轮数 ({max_rounds})")
            print(f"  未修复的问题:")
            for err in result["errors"][:10]:
                print(f"    - {err[:150]}")
            return False

    return False


def run_all(stages: list = None, max_rounds: int = 3, dry_run: bool = False) -> dict:
    """运行全部或指定阶段"""
    if stages is None:
        stages = list(DETECTORS.keys())

    print(">>> 自动回环修正器 v4.0")
    print(f"   最大修正轮数: {max_rounds}")
    print(f"   模式: {'dry-run' if dry_run else '自动修正'}")
    print(f"   阶段: {', '.join(stages)}")

    results = {}
    for name in stages:
        results[name] = run_stage(name, max_rounds, dry_run)

    # 输出汇总
    print(f"\n{'='*60}")
    print("[=] 汇总报告")
    print(f"{'='*60}")

    all_passed = True
    for name, passed in results.items():
        status = "[OK] PASS" if passed else "[!!] FAIL"
        desc = DETECTORS[name]["description"]
        print(f"  {status} {desc}")
        if not passed:
            all_passed = False

    # 保存修正日志
    log_file = QA_DIR / "auto_correction_log.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "max_rounds": max_rounds,
                "dry_run": dry_run,
                "results": {k: v for k, v in results.items()},
                "corrections": CORRECTION_LOG,
                "all_passed": all_passed,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n  [-] 修正日志: {log_file.relative_to(ROOT)}")

    if all_passed:
        print("\n*** 全部通过！")
    else:
        print("\n[!] 部分阶段未通过，需要人工介入")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="自动回环修正器")
    parser.add_argument("--stage", nargs="+", choices=list(DETECTORS.keys()), help="指定运行的阶段")
    parser.add_argument("--max-rounds", type=int, default=3, help="最大修正轮数（默认3）")
    parser.add_argument("--dry-run", action="store_true", help="只检测不修正")
    args = parser.parse_args()

    results = run_all(args.stage, args.max_rounds, args.dry_run)
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()