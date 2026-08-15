#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL GATE RUNNER — 一键终检总门（v4.5）

把系统里分散的客观门禁串成一条命令，任何最终稿提交前必须运行且全部 PASS：

  1. G4.7 实物门      paper_artifact_check.py    论文表格实体/图片/占位符、result*.xlsx 非空、代码存在
  2. G4.6 代码自证门  verify_gate.py             模型必须配 verify_*.py 且全部 PASS（缺失即 FAIL）
  3. G5  证据门        evidence_gate.py          结果/指标/结论/图表证据齐备（official 模式）
  4. G4.8 数字一致性  generic_number_check       论文数字在结果文件中有来源（只取 w:t 可见文本；
                                   无来源去重比例>30% 升级 FAIL，清单保留供人工复核）
  5. G4.9 公式核验门  formula_verification.md    真题必须做官方参考答案公式核验并落盘
  6. G4.10 图片嵌入门  image_embed_check.py      Markdown ![](path) 语法数 vs Word 实际内嵌图数（防"见图N"纯文字漏检）
  7. G5 skill 调用门  skill_invocation_gate.py   必调 skill 产物核验（rc=2 WARN 不阻断）
  8. G5 盲评证据门    blind_panel_report.json    championship（v4.9 默认）盲评证据（与 pipeline_runner
                                   S8 同口径：缺文件/占位/座数不足/无 verdict → FAIL）

背景：2026-08 实测 B 题作品出现"空 result xlsx / 0 表格 docx / 编造公式 / 摘要正文数字矛盾"，
根因是作品放桌面导致硬编码 paper_output/ 的门禁全部落空。本 runner 支持 --paper-dir 指向任意目录。

用法：
    python final_gate_runner.py                          # 作品目录默认 paper_output/
    python final_gate_runner.py --paper-dir C:/Users/xxx/Desktop/测试
    python final_gate_runner.py --workdir E:/数学建模    # 系统门禁脚本的运行目录

退出码：0 = 全部通过；1 = 有 failures（不得宣称可提交/可答辩/可复现）。

fail-closed 原则（CR-2）：任何被依赖的检查器脚本缺失 → 对应门记 pass=False 并使整体 FAIL，
不做"未找到，跳过"的无痕放行；显式 --skip-* 旗标是唯一合法跳过途径。

v4.10.2（第四轮对抗性审查修复，2026-08-15）：
  - G4.8 扫描范围排除 _archive* 目录段（docx 与 results 同口径，对齐 G4.7）——
    归档数字不再稀释无来源比例、归档旧 results 不再给正文数字"假来源"
  - G4.8 docx 在案但无可提取文本 → FAIL_P0（检查未实际执行 ≠ 通过，旧版静默 PASS）
  - G5 证据门闭环接线（R1 消缺）：evidence_gate.py 已支持 --paper-dir 后，调用方
    把已 resolve 的 paper_dir 传入——证据门检查对象与 --paper-dir 一致，
    重定向时报告内留"已重定向"信息行（旧版为"无法重定向"警示，根因已修）

v4.10.1（第三轮审查修复，2026-08-15）：
  - P0-1 盲评门真消费 verdict：与 pipeline_runner 共用 blind_panel_schema 校验
    （verdict 枚举且仅 pass 放行 / 每座 weighted_total 有限数值 ≥0 / conflicts 非空拒）
  - P0-4 --skip-blind-panel 留痕：跳过时仍追加 step（pass=False + skipped_by_flag=True），
    报告 status 记 PASS_WITH_SKIP（SKIP≠PASS），stdout 显示 ⏭️——跳过不再无痕
  - P0-5 G4.8 双口径 + 可配阈值：无来源数字 uniq 比例与 raw 计数双报
    （同值重复 1000 次 raw 如实记 1000）；阈值提为 --missing-ratio-threshold（默认 0.30）
  - LOW docx_visible_text 补页眉/页脚（header*/footer*.xml）与脚注（footnotes.xml）
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

# ── 共用校验模块（第三轮审查 P0-1）──
# blind_panel_schema.py 与本文件同目录；final_gate_runner（本函数）与
# pipeline_runner.championship_missing_evidence 消费同一实现，两链口径永不分裂。
# 互指：tools/quality_gate/pipeline_runner.py（同 verify_gate.missing_verify_for_models
# 被 final_gate_runner 复用的共用模式）。脚本方式运行时 sys.path[0] 即本目录；
# 被当作模块 import 时补目录重试。
try:
    from blind_panel_schema import blind_panel_report_problems
except ImportError:  # pragma: no cover - 仅在被作为模块导入且 sys.path 无本目录时触发
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from blind_panel_schema import blind_panel_report_problems

NUM_RE = re.compile(r"\d+(?:\.\d+)?")
# G4.8 无来源数字比例阈值（去重口径，FAIL 判定口径）：超过即从"人工复核 warning"升级为 FAIL。
# 可经 --missing-ratio-threshold 覆盖（P0-5），默认不变。
MISSING_RATIO_FAIL = 0.30
# docx 可见文本节点：<w:t>…</w:t>（含带属性形式如 <w:t xml:space="preserve">）
WT_TEXT_RE = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.DOTALL)
# docx 参与可见文本提取的 XML 部件：正文/页眉/页脚/脚注（第三轮审查 LOW：
# 页眉页码、脚注里的数字此前漏检，读者在 Word 里看得到、门禁却看不见）
DOCX_TEXT_PARTS_RE = re.compile(r"^word/(?:document\d*|header\d*|footer\d*|footnotes)\.xml$")


def run(cmd: list[str], cwd: Path, timeout: int = 300) -> dict:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(cwd), timeout=timeout)
        return {"cmd": " ".join(str(c) for c in cmd), "rc": proc.returncode,
                "out": (proc.stdout or "")[-1200:], "err": (proc.stderr or "")[-500:]}
    except Exception as exc:
        return {"cmd": " ".join(str(c) for c in cmd), "rc": -1, "out": "", "err": str(exc)}


def docx_visible_text(docx_path: Path) -> str:
    """提取 docx 可见文本：word/document.xml + 页眉/页脚(header*/footer*.xml) + 脚注(footnotes.xml)
    的 <w:t> 文本节点内容。

    二轮审查（2026-08-15）：直接对 document.xml 原文跑数字正则会把 w:sz="24"、
    w:rsidR="00AB12CD" 等 XML 属性值当成论文数字——真实树 49 个"无来源"大半是
    这类属性噪音。只取 w:t 后，数字集合 = 读者在 Word 里真正看到的数字。
    三轮审查（LOW）：页眉页码/页脚年份/脚注数字同样是读者可见文本，此前漏检——
    现按 DOCX_TEXT_PARTS_RE 一并提取（部件缺失即跳过，兼容极简 docx）。
    """
    import zipfile
    from xml.sax.saxutils import unescape
    parts: list[str] = []
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if not DOCX_TEXT_PARTS_RE.match(name):
                continue
            xml = z.read(name).decode("utf-8", errors="replace")
            parts.append("\n".join(unescape(m.group(1)) for m in WT_TEXT_RE.finditer(xml)))
    return "\n".join(parts)


def generic_number_check(paper_dir: Path, missing_ratio_fail: float = MISSING_RATIO_FAIL) -> tuple[list[str], list[str]]:
    """论文正文数字 vs 结果文件数字集合：论文出现但结果文件里找不到的数字列为 warning。

    容差：结果集合含数值时，论文数字需在 [v*(1-tol), v*(1+tol)] 内命中。
    结果文件：<paper-dir>/results/*.json/*.csv（或 --results 指定）。
    升级口径（二轮审查 G4.8 双修②）：无来源数字的去重比例超过 missing_ratio_fail
    （默认 30%，可 --missing-ratio-threshold 配置）时记 FAIL_P0——超阈值正文数字
    无法溯源，疑似成段编造/占位，不得放行；阈值内仍为 warning，清单保留供人工复核。
    双口径展示（三轮审查 P0-5）：uniq 比例为 FAIL 判定口径，raw 计数如实并列展示——
    同值重复 1000 次的攻击稿在 raw 口径如实记 1000，不再被去重口径稀释成 1。
    """
    warnings: list[str] = []
    info: list[str] = []

    def _is_active(f: Path) -> bool:
        # 第四轮审查：归档目录段（_archive* 前缀）不参与数字核对——与
        # paper_artifact_check.check_artifacts 同一口径。旧版把归档 docx/results
        # 一并扫入有两重污染：归档数字匹配 results 会稀释无来源比例（去重分母
        # 变大，真 FAIL 被冲淡成 PASS）；归档 results 的旧数字会给正文"假来源"
        return not any(p.startswith("_archive") for p in f.relative_to(paper_dir).parts[:-1])

    docx_files = [f for f in paper_dir.rglob("*.docx") if _is_active(f)]
    if not docx_files:
        return info, ["未找到 docx，跳过数字一致性"]
    # 提取论文数字（只取≥2位整数或小数，降低噪音；仅 w:t 可见文本，见 docx_visible_text）
    text = ""
    for d in docx_files:
        if "backup" in d.name.lower() or "~$" in d.name:
            continue
        try:
            text += "\n" + docx_visible_text(d)
        except Exception:
            continue
    if not text.strip():
        # 第四轮审查：docx 在案但一个可见文本都提取不到（zip 损坏/全解析失败）——
        # 检查未实际执行却 rc=0 属假绿，按 FAIL_P0 升级（G4.7 也会对解析失败报 FAIL）
        return info, ["FAIL_P0: docx 存在但无可提取文本（解析全部失败？），数字一致性本次未实际核对，不得据此宣称通过"]
    paper_nums = [float(x) for x in NUM_RE.findall(text) if len(x) >= 2]
    # 结果文件数字（同样排除归档目录里的旧 results）
    result_files = ([f for f in paper_dir.rglob("results/*.json") if _is_active(f)]
                    + [f for f in paper_dir.rglob("results/*.csv") if _is_active(f)])
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

    def has_source(v: float) -> bool:
        return any(abs(v - r) <= max(tol * abs(r), 0.5) for r in result_nums)

    missing = [v for v in paper_nums if not has_source(v)]
    uniq_missing = sorted(set(missing))
    uniq_total = len(set(paper_nums))
    ratio = (len(uniq_missing) / uniq_total) if uniq_total else 0.0
    # P0-5 双口径：uniq 比例是 FAIL 判定口径，raw 计数如实展示（防同值重复刷低去重比例）
    info.append(
        f"论文数字 raw {len(paper_nums)} 个（去重 {uniq_total}，仅 w:t 可见文本），"
        f"结果文件数字 {len(result_nums)} 个，无来源 raw {len(missing)} 个"
        f"（去重 {len(uniq_missing)}；FAIL 判定用去重比例 {ratio:.1%} vs 阈值 {missing_ratio_fail:.0%}；"
        f"raw 如实计数——同值重复 1000 次则 raw 记 1000，去重口径只记 1）"
    )
    if uniq_missing:
        top = ", ".join(f"{x:g}" for x in uniq_missing[:20])
        warnings.append(f"论文中以下数字在结果文件中无来源（需人工复核是否编造/占位）: {top}")
    if uniq_total and ratio > missing_ratio_fail:
        warnings.append(
            f"FAIL_P0: 无来源数字去重比例 {ratio:.1%} 超过阈值 {missing_ratio_fail:.0%}"
            f"（raw 口径 {len(missing)}/{len(paper_nums)} 个无来源；阈值可 --missing-ratio-threshold 配置）——"
            "正文数字无法溯源到 results/，疑似成段编造/占位，不得放行（清单见上一条 warning）"
        )
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


def check_blind_panel_championship(paper_dir: Path) -> tuple[list[str], list[str]]:
    """championship 盲评证据门：与 pipeline_runner S8 championship_missing_evidence
    共用 blind_panel_schema.blind_panel_report_problems（同一校验函数，两链口径一致）。

    三轮审查 P0-1（HIGH）：旧版只查 seats≥3 + verdict 键存在——三座数值分 +
    verdict="block" 的报告照样 PASS（pipeline_runner S8 却会拒），两链结论相反。
    现共用校验口径：缺文件/疑似占位/JSON 不合规 → FAIL；verdict 必须命中枚举
    pass|refine|block 且仅 pass 放行；每座 weighted_total 必须是有限数值且 ≥0
    （NaN/-50/空座对象/非数值一律拒）；aggregate.evidence_conflicts 非空 → FAIL。
    合法跳过途径：显式 --skip-blind-panel（对应 orchestrator escape hatch 降级
    standard/fast；P0-4 置位时仍追加 skipped_by_flag step 留痕，不再无痕）。
    schema 依据 .claude/skills/blind-panel/SKILL.md：seats {"A":..,"B":..,"C":..} + verdict。
    """
    failures: list[str] = []
    info: list[str] = []
    report = paper_dir / "qa" / "blind_panel_report.json"
    how = ("调 blind-panel skill：3 座并行盲评 → Lead 聚合写 paper_output/qa/blind_panel_report.json"
           "（schema: seats A/B/C 各含数值 weighted_total + verdict ∈ pass|refine|block，"
           "见 .claude/skills/blind-panel/SKILL.md）")
    problems, data = blind_panel_report_problems(report)
    if problems:
        failures.extend(f"championship（v4.9 默认模式）盲评证据不达标：{p} —— {how}" for p in problems)
        return failures, info
    seats = data.get("seats", {}) if isinstance(data, dict) else {}
    info.append(f"盲评聚合报告在案且通过共用校验: seats={sorted(seats)}, verdict={data.get('verdict')}")
    return failures, info


def main() -> int:
    ap = argparse.ArgumentParser(description="一键终检总门（实物+自证+证据+数字+公式）")
    ap.add_argument("--paper-dir", default="paper_output", help="作品目录（任意位置）")
    ap.add_argument("--workdir", default=".", help="系统门禁脚本运行目录（含 .claude/skills 与 paper_output）")
    ap.add_argument("--skip-evidence", action="store_true", help="跳过证据门（无 model_route.json 时可加）")
    ap.add_argument("--skip-blind-panel", action="store_true",
                    help="跳过 championship 盲评证据门（仅对应 orchestrator escape hatch 显式降级 standard/fast 时合法；"
                         "跳过会在报告追加 skipped_by_flag step 留痕，status=PASS_WITH_SKIP，SKIP≠PASS）")
    ap.add_argument("--missing-ratio-threshold", type=float, default=MISSING_RATIO_FAIL,
                    help="G4.8 无来源数字去重比例 FAIL 阈值（默认 0.30；须在 (0,1] 区间）")
    args = ap.parse_args()
    if not (0 < args.missing_ratio_threshold <= 1):
        ap.error(f"--missing-ratio-threshold 须在 (0,1] 区间，收到 {args.missing_ratio_threshold}")

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
    # 与 code_files 同一排除规则：qa/quality_gate/__pycache__ 下的 verify_*.py 是工具或
    # 测试残留（如对抗性测试临时目录），不得被当作作品自证脚本执行或参与对应关系校验
    verify_files = [
        f for f in paper_dir.rglob("verify_*.py")
        if f.is_file() and not ({"qa", "quality_gate", "__pycache__"} & set(f.relative_to(paper_dir).parts))
    ]
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
            # 第四轮闭环接线（R1 消缺）：evidence_gate.py 已支持 --paper-dir（reconfigure_paths
            # 统一重绑路径常量），调用方把已 resolve 的 paper_dir 传入——证据门从此检查的
            # 就是本 runner 的被检对象，"作品放桌面导致门禁查错 paper_output"的假绿/误伤双隐患消除
            r_ev = run([py, str(scripts / "evidence_gate.py"), "--mode", "official",
                        "--paper-dir", str(paper_dir)], workdir)
            ev_note = ""
            try:
                if paper_dir != (workdir / "paper_output").resolve():
                    ev_note = (f"ℹ 证据门已重定向：--paper-dir={paper_dir}（≠ workdir 的 paper_output，"
                               f"报告落在该作品目录的 qa/ 下）")
            except Exception:
                pass
            steps.append({"gate": "G5_EVIDENCE_GATE", "cmd": r_ev["cmd"], "rc": r_ev["rc"],
                          "pass": r_ev["rc"] == 0,
                          "out_tail": ((ev_note + "\n") if ev_note else "") + r_ev["out"],
                          "err_tail": r_ev["err"]})
        else:
            steps.append({"gate": "G5_EVIDENCE_GATE", "cmd": "N/A", "rc": 1, "pass": False,
                          "out_tail": "evidence_gate.py 未找到（fail-closed）——检查器缺失=FAIL，唯一合法跳过途径是显式 --skip-evidence", "err_tail": ""})
    # 4) 数字一致性（通用提取；P0-5：双口径展示 + 阈值可 CLI 配置）
    info, warns = generic_number_check(paper_dir, args.missing_ratio_threshold)
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
    # 8) championship 盲评证据门（v4.10）：与 pipeline_runner S8 共用同一校验函数
    if not args.skip_blind_panel:
        bp_fail, bp_info = check_blind_panel_championship(paper_dir)
        steps.append({"gate": "G5_BLIND_PANEL_CHAMPIONSHIP", "cmd": "file-check", "rc": 1 if bp_fail else 0,
                      "pass": not bp_fail, "out_tail": "\n".join(bp_info + bp_fail), "err_tail": ""})
    else:
        # P0-4 留痕（三轮审查 MEDIUM）：旧版置位时该 step 完全不进报告，读者无从得知
        # 盲评门被跳过。现仍追加 step（pass=False + skipped_by_flag=True），报告与
        # stdout 双可审计；不计入 failed（显式旗标是文件头声明的唯一合法跳过），
        # 但 status 记 PASS_WITH_SKIP —— SKIP≠PASS，pipeline_runner 侧按 SKIP 侧归类。
        steps.append({"gate": "G5_BLIND_PANEL_CHAMPIONSHIP", "cmd": "N/A", "rc": 3, "pass": False,
                      "skipped_by_flag": True,
                      "out_tail": "被 --skip-blind-panel 显式跳过（对应 orchestrator escape hatch 降级 "
                                  "standard/fast；SKIP≠PASS，本结论不含盲评证据，不得按 championship 全绿口径宣称）",
                      "err_tail": ""})

    # 汇总（P0-4：skipped_by_flag 的 step 不算 failed，但单独成清单供审计）
    failed = [s for s in steps if not s["pass"] and not s.get("skipped_by_flag")]
    skipped_gates = [s["gate"] for s in steps if s.get("skipped_by_flag")]
    report = {
        "gate": "FINAL_GATE_RUNNER",
        "status": "FAIL" if failed else ("PASS_WITH_SKIP" if skipped_gates else "PASS"),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper_dir": str(paper_dir.resolve()),
        "skipped_gates": skipped_gates,
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
        if s.get("skipped_by_flag"):
            mark = "⏭️"
        elif s["pass"]:
            mark = "✅"
        else:
            mark = "❌"
        print(f"  {mark} {s['gate']}  (rc={s['rc']})")
        tail = (s["out_tail"] or "").strip().splitlines()
        for line in tail[-4:]:
            print(f"       {line.strip()}")
        if s["err_tail"]:
            print(f"       [stderr] {s['err_tail'][-200:]}")
    print("─" * 60)
    if failed:
        print(f"  ❌ 终检未通过（{len(failed)} 道门 FAIL）——不得宣称可提交/可答辩/可复现")
        if skipped_gates:
            print(f"  ⏭️ 另有 {len(skipped_gates)} 道门被显式跳过（SKIP≠PASS）: {', '.join(skipped_gates)}")
        return 1
    if skipped_gates:
        print(f"  ⏭️ 终检通过（status=PASS_WITH_SKIP），但 {len(skipped_gates)} 道门被显式跳过"
              f"（SKIP≠PASS）: {', '.join(skipped_gates)} —— 结论不含盲评证据")
        return 0
    print("  ✅ 终检全部通过，可进入提交包生成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

