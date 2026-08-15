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
    python auto_detect_and_fix.py --stage all           # 全部检测（不含 code_style，见 DETECTORS 注）
    python auto_detect_and_fix.py --stage s5            # S5阶段全部
    python auto_detect_and_fix.py --stage s7            # S7阶段全部
    python auto_detect_and_fix.py --stage code_style    # 仅显式可用（不在 all 展开内）

四态（第三轮审查 MEDIUM-C + 第四轮 WARN 语义修复）：
    每项检测 = pass（真通过）/ skip（未实际检查：缺 qa_config、缺产物等，
    rc=0 但 stdout 行首 SKIP——绝不冒充"检测通过"）/ warn（advisory 告警：
    rc=2，如 render_check 的白区>80%/<1KB/边缘内容——"留白偏大"≠"不可交付"，
    不进修复轮、不计失败，但 stdout 明示 [!] WARN）/ fail（失败）。

返回码:
    0 = 无失败项（含 SKIP/WARN 项时 stdout 会明示 [--] SKIP / [!] WARN，未实际检查 ≠ 通过）
    1 = 检测失败（需人工介入）
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Windows GBK 控制台兼容：强制 stdout/stderr 走 utf-8（三态 [--] SKIP 的明示文案含中文，
# 乱码会让"未实际检查 ≠ 通过"的披露不可读——与 pipeline_manager.py 同款处理）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

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
        # HIGH-1 修复（二轮审查）：render_check.py 是子命令式 CLI，不带子命令只打印
        # help 且 rc=0——旧写法使该检测通道恒绿（help 的 rc=0 被当成"检测通过"）。
        # 必须显式传 check-all 并消费其 rc：check-all 有 failed 图时 rc=1。
        "args": ["check-all"],
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
        "description": "代码风格检查（仅显式 --stage code_style 可用，不在 all 展开内）",
        "max_rounds": 1,
        "combined": True,
        # D 修复（第三轮审查 MEDIUM，死通道）：code_style_auto_fixer.py 设计上必须
        # 显式传目标（--file/--errors/--fix-all），无参运行必 rc=1（"请指定 ..."），
        # 且其退出码语义与"检测"不兼容（rc=0 表示"改了 N 个文件"，0 处可改反而
        # rc=1）——旧版把它算进 --stage all 使 all 永败。现 --stage all 不再展开
        # code_style，仅显式指定时可用（见 main 的 all 分支）。
        "explicit_only": True,
    },
}


def run_script(script_path: Path, extra_args: list = None) -> tuple:
    """运行脚本，返回 (status, output)；status ∈ {"pass", "warn", "fail"}（第四轮四态化）。

    CR-4 修复：
    - 检测脚本不存在 = fail（原 return True 使任一检测器路径失效都显示"检测通过"）
    - 子进程解释器用 sys.executable（本机全局 python 是坏 venv，PATH 上的 "python" 不可用）

    rc 语义（第四轮修复 WARN 语义坍缩）：
    - rc=0 → "pass"（调用方再按 stdout SKIP 行降级为 skip 态）
    - rc=2 → "warn"（advisory 告警，不阻断：目前 render_check 用它表达白区>80%/
      <1KB/边缘内容等"建议改进"级问题——"留白偏大"≠"不可交付"，不进修复轮、
      不计失败；与 final_gate_runner 的 rc=2=advisory 约定一致）
    - 其它 rc（含超时/异常）→ "fail"
    """
    if not script_path.exists():
        return "fail", f"检测脚本不存在: {script_path}"

    cmd = [sys.executable, str(script_path)]
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
        if result.returncode == 0:
            return "pass", output
        if result.returncode == 2:
            return "warn", output
        return "fail", output
    except subprocess.TimeoutExpired:
        return "fail", "脚本执行超时"
    except Exception as e:
        return "fail", f"脚本执行异常: {e}"


def _skip_reason(output: str) -> str | None:
    """rc=0 的输出是否实为 SKIP（第三轮审查 MEDIUM-C 修复）。

    口径复制自 tools/quality_gate/pipeline_runner.py::classify_script_result
    （SKIP_STATUSES 含 PASS_WITH_SKIP；SKIP 识别 = stdout 任一行 strip 后以
    skip / [skip] 开头，大小写不敏感）。不跨目录 import：两处独立演化时以
    runner 为准同步。旧版只看 rc——number/result/parameter 缺 qa_config 时
    rc=0 却被打印成"[OK] 检测通过"，把"未实际检查"冒充成"通过"。
    覆盖：check_number/parameter/result 的行首 "SKIP（...）：..."、
    check_numeric_sanity 的行首 "[skip] ..."。
    """
    for ln in output.splitlines():
        low = ln.strip().lower()
        if low.startswith("skip") or low.startswith("[skip]"):
            return ln.strip()
    return None


def detect_and_fix(stage: str, config: dict) -> str:
    """检测+修复单个阶段。返回四态："pass" | "skip" | "warn" | "fail"。

    - "pass"：rc=0 且输出无 SKIP 行（真通过）
    - "skip"：rc=0 但输出行首 SKIP（未实际检查 ≠ 通过，不再冒充 [OK]）
    - "warn"：rc=2（advisory 告警，不阻断——如 render_check 的白区>80%/<1KB/
      边缘内容；不进修复轮、不计失败，但 [!] WARN 明示，绝不冒充"检测通过"）
    - "fail"：rc=1 等其它非零（含检测脚本不存在/超时/异常），走修复轮
    """
    max_rounds = config.get("max_rounds", 2)
    is_combined = config.get("combined", False)

    print(f"\n{'='*50}")
    print(f"[*] {config['description']}")
    print(f"{'='*50}")

    for round_num in range(1, max_rounds + 1):
        print(f"\n  --- 第 {round_num}/{max_rounds} 轮 ---")

        # 检测（combined 与普通模式在检测阶段行为一致，差异只在下方修复器参数——原 if/else 两分支相同，已合并）
        # 检测器自定义参数（如 figure 的 check-all 子命令）经 config["args"] 透传，缺省无参
        status, output = run_script(config["script"], config.get("args"))

        if status == "pass":
            skip_line = _skip_reason(output)
            if skip_line:
                print(f"  [--] SKIP（未实际检查 ≠ 通过）：{skip_line}")
                return "skip"
            print(f"  [OK] 检测通过")
            return "pass"

        if status == "warn":
            # rc=2 advisory：不进修复轮、不计失败——但绝不冒充"检测通过"，
            # 取输出末行（通常是子脚本的 rc 语义说明行）作 WARN 摘要
            warn_lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
            reason = warn_lines[-1] if warn_lines else "rc=2（advisory）"
            print(f"  [!] WARN（advisory，不阻断）：{reason[:200]}")
            return "warn"

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
            return "fail"

        # 修复
        fixer = config.get("fixer")
        if not fixer or not fixer.exists():
            print(f"  [!] 无自动修复器")
            return "fail"

        print(f"  [#] 自动修复...")

        # 写入错误文件
        error_file = QA_DIR / f"auto_fix_errors_{stage}.json"
        error_file.parent.mkdir(parents=True, exist_ok=True)
        error_file.write_text(
            json.dumps({"stage": stage, "errors": errors, "round": round_num}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 运行修复器（修复器 rc=2 不应出现；若出现按"未完全成功"处理，fail-closed）
        if is_combined:
            fix_status, fix_output = run_script(fixer, ["--fix-all"])
        else:
            fix_status, fix_output = run_script(fixer, ["--errors", str(error_file)])

        if fix_status == "pass":
            print(f"  [OK] 修复完成")
        else:
            print(f"  [!] 修复未完全成功，进入下一轮")

    return "fail"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="自动检测+修复包装器")
    parser.add_argument("--stage", required=True, help="检测阶段（code/number/result/evidence/parameter/format/consistency/completeness/figure/latex/citation/aigc/symbol/code_style/s4/s5/s6/s7/all——all 不含 code_style，后者仅显式可用）")
    parser.add_argument("--max-rounds", type=int, help="最大修正轮数（覆盖默认值）")
    args = parser.parse_args()

    # 解析阶段
    stage = args.stage.lower()
    if stage == "all":
        # D 修复（第三轮审查 MEDIUM）：code_style 是死通道（无参必 rc=1，
        # 且其退出码语义与检测不兼容，见 DETECTORS["code_style"] 注），
        # 移出 --stage all 的展开，仅显式 --stage code_style 可用。
        stages = [k for k in DETECTORS if not DETECTORS[k].get("explicit_only")]
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

    # 运行（results 值为四态 "pass" | "skip" | "warn" | "fail"）
    results = {}
    for s in stages:
        config = DETECTORS[s].copy()
        if args.max_rounds:
            config["max_rounds"] = args.max_rounds
        results[s] = detect_and_fix(s, config)

    # 汇总（四态：通过 / SKIP / WARN / 失败）
    print(f"\n{'='*50}")
    print(f"[=] 汇总")
    print(f"{'='*50}")

    status_marks = {"pass": "[OK]", "skip": "[--]", "warn": "[!]", "fail": "[!!]"}
    for s, r in results.items():
        if r == "skip":
            note = "（SKIP，未实际检查 ≠ 通过）"
        elif r == "warn":
            note = "（WARN，advisory 告警，不阻断）"
        else:
            note = ""
        print(f"  {status_marks[r]} {DETECTORS[s]['description']}{note}")

    failed_stages = [s for s, r in results.items() if r == "fail"]
    skipped_stages = [s for s, r in results.items() if r == "skip"]
    warn_stages = [s for s, r in results.items() if r == "warn"]
    # SKIP/WARN 不算失败，但也绝不冒充通过（上方 [--]/[!] 明示）
    all_passed = not failed_stages

    # 保存日志
    log_file = QA_DIR / "auto_detect_fix_log.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(
        json.dumps({
            "timestamp": datetime.now().isoformat(),
            "stages": stages,
            "results": results,
            "counts": {
                "pass": sum(1 for r in results.values() if r == "pass"),
                "skip": len(skipped_stages),
                "warn": len(warn_stages),
                "fail": len(failed_stages),
            },
            "all_passed": all_passed,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if all_passed:
        tail_notes = []
        if skipped_stages:
            # 含 SKIP 项时返回 0，但 stdout 必须明示：未实际检查 ≠ 通过
            tail_notes.append(
                f"[--] 无失败项，但 {len(skipped_stages)} 项检测为 SKIP"
                f"（未实际检查 ≠ 通过）：{', '.join(skipped_stages)}"
            )
        if warn_stages:
            # 含 WARN 项（advisory）时不影响 pass/fail 判定，但计数披露可见
            tail_notes.append(
                f"[!]  无失败项，{len(warn_stages)} 项检测为 WARN"
                f"（advisory 告警，不阻断）：{', '.join(warn_stages)}"
            )
        if tail_notes:
            print("\n" + "\n".join(tail_notes))
        else:
            print(f"\n[***] 全部通过！")
        sys.exit(0)
    else:
        print(f"\n[!] {len(failed_stages)} 项检测失败，需人工介入：{', '.join(failed_stages)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
