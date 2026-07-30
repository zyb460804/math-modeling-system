#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为每个模型生成配对的 verify_*.py 自证脚本骨架（G4.6 强制代码自证）。

融合自 AutoMCM-Pro/demo/CUMCM_Workspace/src/verifications/verify_problem1.py 的验证范式。
设计：每个 paper_output/code/modeling/*.py 必须有配对的
      paper_output/code/verifications/verify_*.py，覆盖：
        1. 参数核验（手工推导 vs 代码）
        2. 结果合理性（区间/量级/符号）
        3. 边界条件
        4. 物理约束（决策变量范围/目标值/约束满足）
      所有验证项必须 ✓ PASS，结果才能被引用进论文。

用法：
  python verification_template.py --model paper_output/code/modeling/problem1.py
  python verification_template.py --all          # 为所有模型生成
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

CODE_DIR = Path("paper_output/code")
MODELING_DIR = CODE_DIR / "modeling"
VERIFY_DIR = CODE_DIR / "verifications"

TEMPLATE = '''"""
{docstring}
强制代码自证（G4.6 门）— 所有验证项必须 ✓ PASS 才能进论文。
融合自 AutoMCM-Pro 验证范式。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../modeling"))
# from {module} import (...)   # ← 导入被验证模型的函数/常量

PASS, FAIL = "✓ PASS", "✗ FAIL"
results: list[tuple[str, str, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    status = PASS if condition else FAIL
    results.append((name, status, detail))
    print(f"  {{status}}  {{name}}" + (f": {{detail}}" if detail else ""))


def main() -> int:
    # ── 1. 参数核验（手工推导 vs 代码）────────────────────
    print("\\n=== 验证1：参数核验 ===")
    # check("参数A精确", abs(val_a - expected_a) < tol, f"val={{val_a}}")

    # ── 2. 结果合理性（区间/量级/符号）──────────────────
    print("\\n=== 验证2：结果合理性 ===")
    # check("目标值>0", obj > 0, f"obj={{obj}}")

    # ── 3. 数值稳定性（inf/nan 检查）─────────────────────
    print("\\n=== 验证3：数值稳定性 ===")
    # 对每个关键结果检查非 inf / 非 nan
    # check("结果非nan", not math.isnan(x), f"x={{x}}")
    # check("结果非inf", not math.isinf(x), f"x={{x}}")

    # ── 4. 边界条件 / 物理约束 ──────────────────────────
    print("\\n=== 验证4：物理约束 ===")
    # check("决策变量在范围内", lo <= var <= hi, f"var={{var}}")

    # ── 汇总 ────────────────────────────────────────────
    n_pass = sum(1 for _, s, _ in results if s == PASS)
    n_fail = sum(1 for _, s, _ in results if s == FAIL)
    print(f"\\n{'═' * 48}")
    print(f"  TOTAL: {{n_pass}} PASS / {{n_fail}} FAIL")
    print(f"{'═' * 48}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
'''


def gen_for_model(model_path: Path, force: bool = False) -> Path | None:
    if not model_path.exists():
        print(f"[skip] 模型不存在: {model_path}")
        return None
    module = model_path.stem
    out = VERIFY_DIR / f"verify_{module}.py"
    if out.exists() and not force:
        print(f"[skip] 已存在（用 --force 覆盖）: {out}")
        return out
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    docstring = f"验证 {module} 结果 — 对应模型 {model_path.name}"
    out.write_text(
        TEMPLATE.format(docstring=docstring, module=module), encoding="utf-8"
    )
    print(f"[ok] 生成自证脚本: {out}")
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="生成 G4.6 自证脚本骨架")
    p.add_argument("--model", help="指定模型文件路径")
    p.add_argument("--all", action="store_true", help="为 modeling/ 下所有 .py 生成")
    p.add_argument("--force", action="store_true", help="覆盖已有 verify 脚本")
    args = p.parse_args()

    if args.all:
        models = sorted(MODELING_DIR.glob("*.py")) if MODELING_DIR.exists() else []
        models = [m for m in models if not m.name.startswith("_")]
        if not models:
            print(f"[warn] 无模型: {MODELING_DIR}")
        for m in models:
            gen_for_model(m, args.force)
    elif args.model:
        gen_for_model(Path(args.model), args.force)
    else:
        p.print_help()


if __name__ == "__main__":
    main()