#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""G4.6 强制代码自证门：运行 paper_output/code/verifications/verify_*.py，
全部 ✓ PASS 才放行（结果才能被引用进论文）。

融合自 AutoMCM-Pro 的"Mandatory Self-Verification"机制（每个 models/*.py 必配
verifications/verify_*.py，验证约束满足/物理合理性/数值稳定性，全部 PASS 才引用）。

用法：
  python verify_gate.py                 # 运行所有 verify 脚本
  python verify_gate.py --fix-missing   # 缺失 verify 时自动生成骨架
退出码：0=全 PASS  1=有 FAIL  2=有 verify 缺失（含模型↔verify 对应缺失、模板生成失败）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

VERIFY_DIR = Path("paper_output/code/verifications")
REPORT_FILE = Path("paper_output/qa/verify_gate_report.json")


def find_models(modeling_dir: Path) -> list[Path]:
    """列出 modeling/ 下的模型脚本（跳过 _ 前缀；与 verification_template.py --all 同口径）。"""
    if not modeling_dir.exists():
        return []
    return sorted(m for m in modeling_dir.glob("*.py") if not m.name.startswith("_"))


def missing_verify_for_models(models: list[Path], verify_files: list[Path]) -> list[str]:
    """对应关系校验（CR-3）：每个 modeling/*.py 必须配 verify_{模型名}.py。

    命名约定见 model-code-and-result-generator/scripts/verification_template.py
    （gen_for_model 生成 VERIFY_DIR/verify_{module}.py）。
    返回缺 verify 的模型名清单；空列表 = 对应齐全。

    注意：tools/quality_gate/final_gate_runner.py 的 G4.6 inline 通过
    sys.path 插入后 `from verify_gate import missing_verify_for_models` 共用本函数。
    修改此处语义时两处同步，勿各写一份实现。
    """
    have = {v.name for v in verify_files}
    return [m.stem for m in models if f"verify_{m.stem}.py" not in have]


def generate_skeletons() -> bool:
    """调 verification_template.py 补齐缺失 verify 骨架。True=模板运行成功。

    CR-3：模板缺失或运行失败返回 False（调用方必须 return 2），
    禁止穿透到空 glob 后"验证 0 个=全过"。
    """
    tmpl = Path(".claude/skills/model-code-and-result-generator/scripts/verification_template.py")
    if not tmpl.exists():
        print(f"[gate] 模板脚本不存在，无法生成 verify 骨架: {tmpl}")
        return False
    proc = subprocess.run([sys.executable, str(tmpl), "--all", "--force"], check=False)
    if proc.returncode != 0:
        print(f"[gate] 模板运行失败 (rc={proc.returncode})，不得视为已补齐")
        return False
    return True


def run_one(script: Path) -> dict:
    """运行单个 verify 脚本，返回结构化结果。

    脚本以绝对路径执行（H-11 同源修复：防相对路径+子目录 cwd 组合下 ENOENT 假 FAIL）；
    cwd 保持本进程 cwd —— 本仓库 verify 脚本约定用 __file__ 定位自身数据，对 cwd 不敏感。
    """
    try:
        proc = subprocess.run(
            [sys.executable, str(script.resolve())],
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

    def collect_verifies() -> list[Path]:
        return sorted(VERIFY_DIR.glob("verify_*.py")) if VERIFY_DIR.exists() else []

    models = find_models(Path(args.modeling_dir))
    scripts = collect_verifies()
    missing = missing_verify_for_models(models, scripts)

    # --fix-missing：模板缺失/运行失败/生成后仍缺 → 一律 return 2（CR-3）
    if missing and args.fix_missing:
        print(f"[gate] 检测到 {len(missing)}/{len(models)} 个模型缺 verify，自动生成骨架…")
        if not generate_skeletons():
            return 2
        scripts = collect_verifies()
        missing = missing_verify_for_models(models, scripts)
        if missing:
            print(f"[gate] 骨架生成后仍缺 {len(missing)} 个: {', '.join(missing)}")
            return 2

    # 对应关系校验（CR-3）：模型数 ↔ verify 数不匹配 → FAIL 并列缺失清单
    if missing:
        print(f"[gate] ⚠ 模型↔verify 对应缺失（{len(missing)}/{len(models)} 个模型无配对 verify_*.py）:")
        print(f"      缺失清单: {', '.join(missing)}")
        print("      按 verify_{模型名}.py 约定补齐，或用 --fix-missing 生成骨架")
        return 2

    if not scripts:
        print("[gate] 无 verify 脚本，也无模型（跳过）")
        return 0

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
    REPORT_FILE.write_text(
        json.dumps(
            {
                "passed": n_fail == 0,
                "n_models": len(models),
                "n_pass": n_pass,
                "n_fail": n_fail,
                "missing_verify": missing,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[gate] 报告: {REPORT_FILE}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
