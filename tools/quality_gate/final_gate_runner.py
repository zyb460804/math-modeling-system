#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL GATE RUNNER — 一键终检总门（v4.5）

把系统里分散的客观门禁串成一条命令，任何最终稿提交前必须运行且全部 PASS：

  1. G4.7 实物门      paper_artifact_check.py    论文表格实体/图片/占位符、result*.xlsx 非空、代码存在
  2. G4.6 代码自证门  verify_gate.py             模型必须配 verify_*.py 且全部 PASS（缺失即 FAIL）
  3. G5  证据门        evidence_gate.py          结果/指标/结论/图表证据齐备（official 模式）
  4. G4.8 数字一致性  generic_number_check       论文数字在结果文件中有来源（warning 级，人工复核）
  5. G4.9 公式核验门  formula_verification.md    真题必须做官方参考答案公式核验并落盘
  6. G4.10 图片嵌入门  image_embed_check.py      Markdown ![](path) 语法数 vs Word 实际内嵌图数（防"见图N"纯文字漏检）

背景：2026-08 实测 B 题作品出现"空 result xlsx / 0 表格 docx / 编造公式 / 摘要正文数字矛盾"，
根因是作品放桌面导致硬编码 paper_output/ 的门禁全部落空。本 runner 支持 --paper-dir 指向任意目录。

用法：
    python final_gate_runner.py                          # 作品目录默认 paper_output/
    python final_gate_runner.py --paper-dir C:/Users/xxx/Desktop/测试
    python final_gate_runner.py --workdir E:/数学建模    # 系统门禁脚本的运行目录

退出码：0 = 全部通过；1 = 有 failures（不得宣称可提交/可答辩/可复现）。

fail-closed 原则（CR-2）：任何被依赖的检查器脚本缺失 → 对应门记 pass=False 并使整体 FAIL，
不做"未找到，跳过"的无痕放行；显式 --skip-* 旗标是唯一合法跳过途径。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def run(cmd: list[str], cwd: Path, timeout: int = 300) -> dict:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(cwd), timeout=timeout)
        return {"cmd": " ".join(str(c) for c in cmd), "rc": proc.returncode,
                "out": (proc.stdout or "")[-1200:], "err": (proc.stderr or "")[-500:]}
    except Exception as exc:
        return {"cmd": " ".join(str(c) for c in cmd), "rc": -1, "out": "", "err": str(exc)}


def generic_number_check(paper_dir: Path) -> tuple[list[str], list[str]]:
    """论文正文数字 vs 结果文件数字集合：论文出现但结果文件里找不到的数字列为 warning。

    容差：结果集合含数值时，论文数字需在 [v*(1-tol), v*(1+tol)] 内命中。
    结果文件：<paper-dir>/results/*.json/*.csv（或 --results 指定）。
    """
    warnings: list[str] = []
    info: list[str] = []
    docx_files = list(paper_dir.rglob("*.docx"))
    if not docx_files:
        return info, ["未找到 docx，跳过数字一致性"]
    # 提取论文数字（只取≥2位整数或小数，降低噪音）
    text = ""
    for d in docx_files:
        if "backup" in d.name.lower() or "~$" in d.name:
            continue
        try:
            import zipfile
            with zipfile.ZipFile(d) as z:
                text += z.read("word/document.xml").decode("utf-8", errors="replace")
        except Exception:
            continue
    paper_nums = [float(x) for x in NUM_RE.findall(text) if len(x) >= 2]
    # 结果文件数字
    result_files = list(paper_dir.rglob("results/*.json")) + list(paper_dir.rglob("results/*.csv"))
    result_nums: set[float] = set()
    for rf in result_files:
        try:
            raw = rf.read_text(encoding="utf-8", errors="replace")
            result_nums.update(float(x) for x in NUM_RE.findall(raw) if len(x) >= 2)
        except Exception:
            continue
    if not result_nums:
        return info, ["FAIL_P0: 未找到结果数字文件（results/*.json|*.csv），论文数字无法客观核对来源"]
    tol = 0.05
    missing: list[float] = []
    for v in paper_nums:
        if not any(abs(v - r) <= max(tol * abs(r), 0.5) for r in result_nums):
            missing.append(v)
    info.append(f"论文数字 {len(paper_nums)} 个，结果文件数字 {len(result_nums)} 个，无来源候选 {len(missing)} 个")
    if missing:
        top = ", ".join(f"{x:g}" for x in sorted(set(missing))[:20])
        warnings.append(f"论文中以下数字在结果文件中无来源（需人工复核是否编造/占位）: {top}")
    return info, warnings


def check_formula_verification(workdir: Path, paper_dir: Path) -> tuple[list[str], list[str]]:
    """G4.9 公式核验门：真题任务必须存在公式核验记录，且无【待核验】残留。"""
    failures: list[str] = []
    info: list[str] = []
    candidates = [
        workdir / "paper_output" / "plan" / "formula_verification.md",
        paper_dir / "formula_verification.md",
        paper_dir / "qa" / "formula_verification.md",
    ]
    found = next((p for p in candidates if p.exists()), None)
    if found is None:
        failures.append(
            "缺少公式核验记录 paper_output/plan/formula_verification.md —— 真题必须先用官方参考答案/权威论文核对核心公式，"
            "未核验的公式不得写入正文（防止编造修正系数/经验公式）"
        )
        return failures, info
    text = found.read_text(encoding="utf-8", errors="replace")
    for marker in ["【待核验", "待核验", "TODO", "TBD", "<<<"]:
        if marker in text:
            failures.append(f"公式核验记录 {found.name} 仍有残留标记「{marker}」")
    info.append(f"公式核验记录存在: {found.name}")
    return failures, info


def main() -> int:
    ap = argparse.ArgumentParser(description="一键终检总门（实物+自证+证据+数字+公式）")
    ap.add_argument("--paper-dir", default="paper_output", help="作品目录（任意位置）")
    ap.add_argument("--workdir", default=".", help="系统门禁脚本运行目录（含 .claude/skills 与 paper_output）")
    ap.add_argument("--skip-evidence", action="store_true", help="跳过证据门（无 model_route.json 时可加）")
    args = ap.parse_args()

    paper_dir = Path(args.paper_dir).resolve()  # H-11：先 resolve，rglob/子进程全部走绝对路径
    workdir = Path(args.workdir).resolve()
    here = Path(__file__).resolve().parent
    scripts = workdir / ".claude" / "skills" / "quality-assurance-auditor" / "scripts"
    py = sys.executable

    steps: list[dict] = []
    def add(name: str, cmd: list[str], cwd: Path):
        r = run(cmd, cwd)
        steps.append({"gate": name, "cmd": r["cmd"], "rc": r["rc"], "pass": r["rc"] == 0,
                      "out_tail": r["out"], "err_tail": r["err"]})

    # 1) 实物门
    add("G4.7_ARTIFACT_GATE", [py, str(here / "paper_artifact_check.py"), "--paper-dir", str(paper_dir)], workdir)
    # 2) 代码自证门：作品目录内有代码必须配 verify_*.py 并全部 PASS（防空转绕过）
    #    模型↔verify 对应关系校验与 verify_gate.py 共用同一实现：
    #    sys.path 插入 quality-assurance-auditor/scripts 后 import missing_verify_for_models，
    #    勿在两处各写一份 —— 互指：.claude/skills/quality-assurance-auditor/scripts/verify_gate.py
    #    （排除规则按相对 paper_dir 的路径段判断，只跳过作品自带的 qa/quality_gate 工具代码，
    #     不受作品目录恰好放在某个名为 qa 的祖先目录下影响）
    code_files = []
    for f in paper_dir.rglob("*.py"):
        if not f.is_file():
            continue
        rel_parts = f.relative_to(paper_dir).parts
        if "qa" in rel_parts or "quality_gate" in rel_parts or "__pycache__" in rel_parts:
            continue
        code_files.append(f)
    verify_files = [f for f in paper_dir.rglob("verify_*.py") if f.is_file()]
    modeling_dir = paper_dir / "code" / "modeling"
    models = (sorted(m for m in modeling_dir.glob("*.py") if not m.name.startswith("_"))
              if modeling_dir.exists() else [])
    try:
        sys.path.insert(0, str(scripts))
        from verify_gate import missing_verify_for_models
    except Exception as exc:
        missing_verify_for_models = None
        vg_import_err = str(exc)
    if not code_files:
        steps.append({"gate": "G4.6_VERIFY_GATE", "cmd": "N/A", "rc": 0, "pass": True,
                      "out_tail": "作品目录无代码（由 G4.7 实物门判 FAIL）", "err_tail": ""})
    elif missing_verify_for_models is None:
        # 检查器（共享校验函数）不可用 = FAIL（fail-closed，同 CR-2 原则）
        steps.append({"gate": "G4.6_VERIFY_GATE", "cmd": "N/A", "rc": 1, "pass": False,
                      "out_tail": f"verify_gate.py 不可导入，无法执行模型↔verify 对应关系校验（fail-closed）: {vg_import_err}", "err_tail": ""})
    elif not verify_files:
        steps.append({"gate": "G4.6_VERIFY_GATE", "cmd": "N/A", "rc": 2, "pass": False,
                      "out_tail": f"发现 {len(code_files)} 个代码文件但无 verify_*.py 自证脚本——模型结果未经自证不得写入论文", "err_tail": ""})
    else:
        vouts = []
        all_pass = True
        # 对应关系校验（CR-3）：每个 code/modeling/*.py 必须配 verify_{模型名}.py
        missing = missing_verify_for_models(models, verify_files)
        if missing:
            all_pass = False
            vouts.append(f"模型↔verify 对应缺失（{len(missing)}/{len(models)}）: {', '.join(missing)} —— 每个模型必须配 verify_{{模型名}}.py")
        for vf in verify_files:
            # vf 已是绝对路径（paper_dir 先 resolve），cwd=脚本所在目录 —— H-11：消除"相对路径+子目录 cwd"的 ENOENT 假 FAIL
            r = run([py, str(vf)], vf.parent)
            all_pass = all_pass and r["rc"] == 0
            vouts.append(f"{vf.name}: {'PASS' if r['rc']==0 else 'FAIL'} (rc={r['rc']})")
        steps.append({"gate": "G4.6_VERIFY_GATE", "cmd": "run verify_*.py", "rc": 0 if all_pass else 1,
                      "pass": all_pass, "out_tail": "\n".join(vouts), "err_tail": ""})
    # 3) 证据门（official）—— 检查器缺失 = FAIL（fail-closed），显式 --skip-evidence 是唯一合法跳过
    if not args.skip_evidence:
        if (scripts / "evidence_gate.py").exists():
            add("G5_EVIDENCE_GATE", [py, str(scripts / "evidence_gate.py"), "--mode", "official"], workdir)
        else:
            steps.append({"gate": "G5_EVIDENCE_GATE", "cmd": "N/A", "rc": 1, "pass": False,
                          "out_tail": "evidence_gate.py 未找到（fail-closed）——检查器缺失=FAIL，唯一合法跳过途径是显式 --skip-evidence", "err_tail": ""})
    # 4) 数字一致性（通用提取）
    info, warns = generic_number_check(paper_dir)
    num_fail = any(w.startswith("FAIL_P0") for w in warns)
    steps.append({"gate": "G4.8_NUMBER_CONSISTENCY", "cmd": "generic", "rc": 1 if num_fail else 0,
                  "pass": not num_fail, "out_tail": "\n".join(info + [w for w in warns if not w.startswith("FAIL_P0")]),
                  "err_tail": "\n".join(w for w in warns if w.startswith("FAIL_P0"))})
    # 5) 公式核验门
    f_fail, f_info = check_formula_verification(workdir, paper_dir)
    steps.append({"gate": "G4.9_FORMULA_VERIFICATION", "cmd": "file-check", "rc": 1 if f_fail else 0,
                  "pass": not f_fail, "out_tail": "\n".join(f_info + f_fail), "err_tail": ""})
    # 6) 图片嵌入门（v4.7 新增）：Markdown ![](path) 语法数 vs Word 实际内嵌图数
    #    背景：2023 B 题踩坑——md 写"见图N"纯文字，pandoc 转 Word 后 0 图，原格式门禁未发现
    #    WARN（rc=2）不阻断提交；FAIL（rc=1）阻断
    img_script = here / "image_embed_check.py"
    if img_script.exists():
        r_img = run([py, str(img_script), "--paper-dir", str(paper_dir)], workdir)
        img_pass = r_img["rc"] in (0, 2)  # WARN 不阻断
        steps.append({"gate": "G4.10_IMAGE_EMBED_GATE", "cmd": r_img["cmd"], "rc": r_img["rc"],
                      "pass": img_pass, "out_tail": r_img["out"], "err_tail": r_img["err"]})
    else:
        # CR-2：检查器缺失 = FAIL（原为 pass=True"未找到，跳过"的无痕放行）
        steps.append({"gate": "G4.10_IMAGE_EMBED_GATE", "cmd": "N/A", "rc": 1, "pass": False,
                      "out_tail": "image_embed_check.py 未找到（fail-closed）——检查器缺失=FAIL", "err_tail": ""})
    # 7) Skill 调用强制门（v4.8 新增）：检查必调 skill 是否真调过
    #    背景：规范要求 Agent 必须调 humanizer/review/defense 等 skill，但原门禁不查
    #    FAIL（rc=1）阻断提交；WARN（rc=2）不阻断但提示覆盖率低
    skill_script = here / "skill_invocation_gate.py"
    if skill_script.exists():
        r_skill = run([py, str(skill_script), "--paper-dir", str(paper_dir)], workdir)
        skill_pass = r_skill["rc"] in (0, 2)  # WARN 不阻断，FAIL 阻断
        steps.append({"gate": "G5_SKILL_INVOCATION_GATE", "cmd": r_skill["cmd"], "rc": r_skill["rc"],
                      "pass": skill_pass, "out_tail": r_skill["out"][-1500:], "err_tail": r_skill["err"]})
    else:
        # CR-2：检查器缺失 = FAIL（原为 pass=True"未找到，跳过"的无痕放行）
        steps.append({"gate": "G5_SKILL_INVOCATION_GATE", "cmd": "N/A", "rc": 1, "pass": False,
                      "out_tail": "skill_invocation_gate.py 未找到（fail-closed）——检查器缺失=FAIL", "err_tail": ""})

    # 汇总
    failed = [s for s in steps if not s["pass"]]
    report = {
        "gate": "FINAL_GATE_RUNNER",
        "status": "FAIL" if failed else "PASS",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper_dir": str(paper_dir.resolve()),
        "steps": steps,
    }
    report_path = paper_dir / "qa" / "final_gate_report.json"
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        print(f"[runner] 报告写入失败: {exc}")

    print("═" * 60)
    print("  FINAL GATE RUNNER（v4.5 一键终检总门）")
    print("═" * 60)
    for s in steps:
        mark = "✅" if s["pass"] else "❌"
        print(f"  {mark} {s['gate']}  (rc={s['rc']})")
        tail = (s["out_tail"] or "").strip().splitlines()
        for line in tail[-4:]:
            print(f"       {line.strip()}")
        if s["err_tail"]:
            print(f"       [stderr] {s['err_tail'][-200:]}")
    print("─" * 60)
    if failed:
        print(f"  ❌ 终检未通过（{len(failed)} 道门 FAIL）——不得宣称可提交/可答辩/可复现")
        return 1
    print("  ✅ 终检全部通过，可进入提交包生成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

