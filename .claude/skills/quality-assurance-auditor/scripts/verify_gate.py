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
三态（报告 JSON status 字段 + SKIP 行）：PASS / FAIL / SKIP——无模型也无 verify 的空项目
写显式 SKIP（未验证≠通过，不再伪装 PASS），rc 仍为 0，供 pipeline_runner 三态消费。
空壳暴露：每脚本 assert 语句计数写入报告与 stdout——n_assertions 为 AST 真实可执行断言数
（ast.walk 统计 ast.Assert 节点，注释/字符串里的 assert 不算）；n_assert_text 保留字面计数作对照，
两者并列暴露"字面多、AST 少=注释刷数可疑"。0 条（AST 口径）的 rc=0 verify 一眼可见。
注意：计数是暴露指标非门禁——不据此放行也不据此阻断，评审/审计据此定位空壳自证。
freshness 接线（P1-11）：报告写盘后自动调 freshness_check.py record --sources <本门禁依赖的
verifications/ + modeling/ 目录>，为报告绑定源哈希；record 失败只降级为报告内 warning，不影响门禁判定。
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

VERIFY_DIR = Path("paper_output/code/verifications")
REPORT_FILE = Path("paper_output/qa/verify_gate_report.json")

# assert 字面计数（仅对照用）：识别"rc=0 但一条断言都没有"的橡皮图章 verify。
# 负向后顾排除属性/标识符内的 assert（如 self_assert、x.assert）；注释/字符串里按字面计。
# 真实计数以 AST 为准（count_assertion_stats），字面值只用来暴露"注释刷数"差异。
ASSERT_RE = re.compile(r"(?<![\w.])assert\s")

# freshness_check.py 位置（同仓 .claude/skills/ 下，按 __file__ 定位，不依赖 cwd）
FRESHNESS_SCRIPT = (
    Path(__file__).resolve().parents[2] / "context-memory-keeper" / "scripts" / "freshness_check.py"
)


def find_models(modeling_dir: Path) -> list[Path]:
    """列出 modeling/ 下的模型脚本（跳过 _ 前缀；与 verification_template.py --all 同口径）。"""
    if not modeling_dir.exists():
        return []
    return sorted(m for m in modeling_dir.glob("*.py") if not m.name.startswith("_"))


def missing_verify_for_models(models: list[Path], verify_files: list[Path]) -> list[str]:
    """对应关系校验（CR-3）：每个 modeling/*.py 必须配 verify_{模型名}.py。

    命名约定见 model-code-and-result-generator/scripts/verification_template.py
    （gen_for_model 生成 VERIFY_DIR/verify_{module}.py）。
    兼容词序变体：verify_q1_model.py 也算 q1_model.py 的自证
    （历史作品存在 q1_model ↔ verify_q1_model 词序颠倒，实质对应不因词序而失效）。
    返回缺 verify 的模型名清单；空列表 = 对应齐全。

    注意：tools/quality_gate/final_gate_runner.py 的 G4.6 inline 通过
    sys.path 插入后 `from verify_gate import missing_verify_for_models` 共用本函数。
    修改此处语义时两处同步，勿各写一份实现。
    """
    def _tokens(name: str) -> frozenset[str]:
        # 去掉 verify 前缀后按下划线分词；q1 保持原样不拆数字
        return frozenset(t for t in name.split("_") if t and t != "verify")
    have = {_tokens(v.stem) for v in verify_files}
    verify_names = {v.name for v in verify_files}
    missing = []
    for m in models:
        mt = _tokens(m.stem)
        # 精确命名 verify_{stem} 直接命中；否则允许 token 集相等的词序变体
        if f"verify_{m.stem}.py" not in verify_names and mt not in have:
            missing.append(m.stem)
    return missing


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


def count_assertion_stats(script: Path) -> tuple[int, int]:
    """统计单个 verify 脚本的断言数，返回 (AST 真实数, 字面对照数)。

    - AST 口径（n_assertions）：ast.walk 统计 ast.Assert 节点 = 真实可执行断言；
      注释/字符串里的 assert 不算（P1-6：旧字面正则可被注释刷高）。
    - 字面口径（n_assert_text）：旧正则计数保留作对照——字面多而 AST 少 = 注释刷数可疑。
    读不到源码两个都返回 -1；AST 解析失败（语法错误）真实数返回 -1、字面数照常给出。
    只计数不阻断：计数是暴露指标非门禁，评审据此定位空壳 verify。
    """
    try:
        src = script.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return -1, -1
    n_text = len(ASSERT_RE.findall(src))
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return -1, n_text
    n_ast = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Assert))
    return n_ast, n_text


def record_freshness(report: Path, sources: list[Path]) -> None:
    """
报告写盘后为它记录源哈希（P1-11 真接线，消灭 record 空转）。

    - 只绑定本门禁的核心依赖（verifications/ + modeling/），不绑定全量源；
    - 失败不 FAIL：freshness 记录是附加元数据，其失败降级为报告内一行 warning
      + stdout 提示，绝不让"哈希记录失败"变成门禁本身的 FAIL（如实分级）。
    """
    existing = [s for s in sources if Path(s).exists()]
    if not existing or not FRESHNESS_SCRIPT.exists():
        print(f"[gate] 跳过 freshness record（无已存在的依赖源或 freshness_check.py 不存在: {FRESHNESS_SCRIPT}）")
        return
    try:
        proc = subprocess.run(
            [sys.executable, str(FRESHNESS_SCRIPT), "record", str(report),
             "--sources", *[str(s) for s in existing]],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
        )
        if proc.returncode == 0:
            tail = (proc.stdout or "").strip().splitlines()
            msg = tail[-1].removeprefix("[fresh] ") if tail else "freshness source_hash 已记录"
            print(f"[gate] {msg}")
            return
        reason = (proc.stderr or proc.stdout or "").strip().splitlines()
        reason_text = reason[-1] if reason else f"rc={proc.returncode}"
    except Exception as exc:  # noqa: BLE001 —— 记录失败必须降级，不得击穿门禁
        reason_text = str(exc)
    print(f"[gate] ⚠ 记录哈希失败（不阻断门禁）：{reason_text}")
    try:  # 降级为报告内 warning：重新读盘追加（record 可能已改写文件）
        data = json.loads(report.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data.setdefault("warnings", []).append(
                f"freshness record 失败，本报告未绑定 source_hash：{reason_text}"
            )
            report.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass  # 连追加都失败时只剩 stdout 痕迹，不再向上抛


def write_report(payload: dict, sources: list[Path] | None = None) -> None:
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    # P1-11：报告落地后立即绑定源哈希（失败降级为 warning，不影响已写盘的报告语义）
    record_freshness(REPORT_FILE, sources or [VERIFY_DIR])


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
    except OSError as exc:
        # fail-closed：脚本在 glob 与执行之间被并发删除/权限不可读等 OS 层错误，
        # 按该 verify FAIL 处理（不是跳过）——崩整门会让后续 verify 全部漏跑
        return {
            "script": str(script).replace("\\", "/"),
            "passed": False,
            "returncode": -1,
            "stdout_tail": "",
            "stderr_tail": f"OSERROR: {exc}",
        }


def main() -> int:
    p = argparse.ArgumentParser(description="G4.6 强制代码自证门")
    p.add_argument("--fix-missing", action="store_true", help="缺失 verify 时自动生成骨架")
    p.add_argument("--modeling-dir", default="paper_output/code/modeling")
    args = p.parse_args()

    # freshness 绑定源：本门禁的结论只依赖这两个目录（存在才绑定，见 record_freshness）
    freshness_sources = [VERIFY_DIR, Path(args.modeling_dir)]

    def collect_verifies() -> list[Path]:
        return sorted(VERIFY_DIR.glob("verify_*.py")) if VERIFY_DIR.exists() else []

    models = find_models(Path(args.modeling_dir))
    scripts = collect_verifies()
    missing = missing_verify_for_models(models, scripts)

    # --fix-missing：模板缺失/运行失败/生成后仍缺 → 一律 return 2（CR-3）
    if missing and args.fix_missing:
        print(f"[gate] 检测到 {len(missing)}/{len(models)} 个模型缺 verify，自动生成骨架…")
        if not generate_skeletons():
            write_report({"status": "FAIL", "n_models": len(models), "missing_verify": missing,
                          "results": [], "note": "verification_template.py 缺失或运行失败，无法生成骨架"},
                         freshness_sources)
            return 2
        scripts = collect_verifies()
        missing = missing_verify_for_models(models, scripts)
        if missing:
            print(f"[gate] 骨架生成后仍缺 {len(missing)} 个: {', '.join(missing)}")
            write_report({"status": "FAIL", "n_models": len(models), "missing_verify": missing,
                          "results": [], "note": "骨架生成后仍缺配对 verify"}, freshness_sources)
            return 2

    # 对应关系校验（CR-3）：模型数 ↔ verify 数不匹配 → FAIL 并列缺失清单
    if missing:
        print(f"[gate] ⚠ 模型↔verify 对应缺失（{len(missing)}/{len(models)} 个模型无配对 verify_*.py）:")
        print(f"      缺失清单: {', '.join(missing)}")
        print("      按 verify_{模型名}.py 约定补齐，或用 --fix-missing 生成骨架")
        write_report({"status": "FAIL", "n_models": len(models), "missing_verify": missing,
                      "results": [], "note": "模型↔verify 对应缺失，未运行任何自证"}, freshness_sources)
        return 2

    if not scripts:
        # 显式 SKIP（G-01 残留）：无模型也无 verify ≠ 验证通过。rc 保持 0（不阻断空项目），
        # 但报告写 status=SKIP、stdout 打印以 SKIP 开头的行——pipeline_runner
        # classify_script_result 对 rc=0 + "SKIP…" 行判为 SKIP（三态），不再伪装 PASS。
        print("[gate] 无 verify 脚本，也无模型")
        print("SKIP：无模型（未验证≠通过）——G4.6 本次未执行任何自证，不得据此宣称结果可信")
        write_report({
            "status": "SKIP",
            "n_models": 0,
            "n_pass": 0,
            "n_fail": 0,
            "n_assertions_total": 0,
            "missing_verify": [],
            "results": [],
            "note": "无模型无 verify：显式 SKIP（未验证≠通过），非 PASS",
        }, freshness_sources)
        print(f"[gate] 报告: {REPORT_FILE}")
        return 0

    print(f"[gate] 运行 {len(scripts)} 个 verify 脚本…\n")
    results = []
    for s in scripts:
        r = run_one(s)
        n_ast, n_text = count_assertion_stats(s)
        r["n_assertions"] = n_ast
        r["n_assert_text"] = n_text
        if n_text > 0 and n_ast == 0:
            r["assert_count_suspect"] = True  # 字面有 assert 但 AST 无：注释/字符串刷数
        results.append(r)
        mark = "✓" if r["passed"] else "✗"
        flag = "  ⚠ 字面≠AST（注释刷数可疑）" if r.get("assert_count_suspect") else ""
        print(f"  {mark} {s.name}  (rc={r['returncode']}, asserts={n_ast}, assert_text={n_text}){flag}")

    n_pass = sum(1 for r in results if r["passed"])
    n_fail = len(results) - n_pass
    n_assertions_total = sum(r["n_assertions"] for r in results if r["n_assertions"] > 0)
    n_assert_text_total = sum(r["n_assert_text"] for r in results if r["n_assert_text"] > 0)
    print(f"\n{'═' * 48}")
    print(f"  G4.6 VERIFY GATE: {n_pass} PASS / {n_fail} FAIL")
    print(f"  assert 真实（AST）共 {n_assertions_total} 条 / 字面（含注释）共 {n_assert_text_total} 条")
    if n_assertions_total == 0:
        if n_assert_text_total > 0:
            print(f"  ⚠ AST 真实 0 条 vs 字面 {n_assert_text_total} 条——注释/字符串刷数痕迹，空壳自证（不阻断，评审必查）")
        else:
            print("  ⚠ 全部 verify 合计 0 条 assert——空壳自证（不阻断，但评审必查）")
    print("  （计数是暴露指标非门禁：不据此放行也不据此阻断）")
    print(f"{'═' * 48}")

    write_report({
        "status": "PASS" if n_fail == 0 else "FAIL",
        "passed": n_fail == 0,
        "n_models": len(models),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_assertions_total": n_assertions_total,
        "n_assert_text_total": n_assert_text_total,
        "assert_count_note": "n_assertions=AST 真实断言数（ast.Assert），n_assert_text=字面计数（含注释/字符串）；计数是暴露指标非门禁",
        "missing_verify": missing,
        "results": results,
    }, freshness_sources)
    print(f"[gate] 报告: {REPORT_FILE}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
