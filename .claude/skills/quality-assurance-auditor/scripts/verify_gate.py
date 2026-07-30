#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""G4.6 强制代码自证门：运行 paper_output/code/verifications/verify_*.py，
全部 ✓ PASS 才放行（结果才能被引用进论文）。

融合自 AutoMCM-Pro 的"Mandatory Self-Verification"机制（每个 models/*.py 必配
verifications/verify_*.py，验证约束满足/物理合理性/数值稳定性，全部 PASS 才引用）。

用法：
  python verify_gate.py                 # 运行所有 verify 脚本
  python verify_gate.py --fix-missing   # 缺失 verify 时自动生成骨架
退出码：0=全 PASS  1=有 FAIL  2=有 verify 缺失
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

VERIFY_DIR = Path("paper_output/code/verifications")
REPORT_FILE = Path("paper_output/qa/verify_gate_report.json")


def run_one(script: Path) -> dict:
    """运行单个 verify 脚本，返回结构化结果。"""
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        passed = proc.returncode == 0
        return {
            "script": str(script).replace("\\", "/"),
            "passed": passed,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-800:],
            "stderr_tail": proc.stderr[-400:] if proc.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "script": str(script).replace("\\", "/"),
            "passed": False,
            "returncode": -1,
            "stdout_tail": "",
            "stderr_tail": "TIMEOUT (>300s)",
        }


def main() -> int:
    p = argparse.ArgumentParser(description="G4.6 强制代码自证门")
    p.add_argument("--fix-missing", action="store_true", help="缺失 verify 时自动生成骨架")
    p.add_argument("--modeling-dir", default="paper_output/code/modeling")
    args = p.parse_args()

    if not VERIFY_DIR.exists() or not any(VERIFY_DIR.glob("verify_*.py")):
        # 检查是否有模型但缺 verify
        modeling = Path(args.modeling_dir)
        models = sorted(modeling.glob("*.py")) if modeling.exists() else []
        models = [m for m in models if not m.name.startswith("_")]
        if models and args.fix_missing:
            print(f"[gate] 检测到 {len(models)} 个模型缺 verify，自动生成骨架…")
            tmpl = Path(".claude/skills/model-code-and-result-generator/scripts/verification_template.py")
            if tmpl.exists():
                subprocess.run(
                    [sys.executable, str(tmpl), "--all", "--force"],
                    check=False,
                )
            else:
                print(f"[gate] 模板脚本不存在: {tmpl}")
        elif models:
            print(f"[gate] ⚠ 有 {len(models)} 个模型但无 verify 脚本（用 --fix-missing 生成）")
            return 2
        else:
            print("[gate] 无 verify 脚本，也无模型（跳过）")
            return 0

    scripts = sorted(VERIFY_DIR.glob("verify_*.py"))
    print(f"[gate] 运行 {len(scripts)} 个 verify 脚本…\n")
    results = []
    for s in scripts:
        r = run_one(s)
        results.append(r)
        mark = "✓" if r["passed"] else "✗"
        print(f"  {mark} {s.name}  (rc={r['returncode']})")

    n_pass = sum(1 for r in results if r["passed"])
    n_fail = len(results) - n_pass
    print(f"\n{'═' * 48}")
    print(f"  G4.6 VERIFY GATE: {n_pass} PASS / {n_fail} FAIL")
    print(f"{'═' * 48}")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    import json
    REPORT_FILE.write_text(
        json.dumps(
            {"passed": n_fail == 0, "n_pass": n_pass, "n_fail": n_fail, "results": results},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[gate] 报告: {REPORT_FILE}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())