#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PIPELINE RUNNER — 一键流水线调度器（v4.9 + CR-5/G-05 修复）

把 paper-workflow-orchestrator 的路由逻辑代码化：
  - 脚本型环节（门禁/审计/格式）：自动 subprocess 跑，PASS 才推进
  - 认知型环节（审题/写作/盲评）：输出 AGENT_HANDOFF 指令，交 Agent 接力
  - 状态推进：复用 pipeline_manager.py 的 pipeline.json（GitOps 状态机）

v4.9.2（第二轮审查修复，B7/C/D/E/F 对应 runner 侧）：
  - championship verdict 真消费：verdict 必须命中 blind-panel SKILL.md 枚举
    pass|refine|block 且 = pass 才放行；每座 weighted_total 必须为数值；
    aggregate.evidence_conflicts 非空 → 拒绝（12 字节矛盾 JSON 不再放行）
  - classify 兜底：rc=0 但报告 status=FAIL/FAILED/ERROR → FAIL（以磁盘报告为准）；
    未知 status 词 → 至少 WARN，绝不当 PASS；PASS_WITH_SKIP 归 SKIP 侧
  - S3b verify_gate 接 report 键（qa/verify_gate_report.json）：空项目
    status=SKIP 时 runner 正确显示 ⏭️ 而非 PASS
  - 数字门禁 0 匹配（check_number_consistency 改 SKIP 后）本侧无需改动即可显示 ⏭️

v4.9.1（CR-5 / G-05 / G-07 修复）：
  - check_produces 强化：目录型 produce 必须非空；JSON 型 produce 必须 ≥10 字节且
    json.loads 可解析（坏 JSON = 未完成）
  - 脚本阶段三态展示：PASS / SKIP / WARN / FAIL。SKIP 由子脚本 stdout 的
    "SKIP：" / "[skip]" 行或其报告 JSON 的 status 字段识别（SKIP≠PASS，绝不混显）
  - 含 SKIP 的阶段：状态记 "skipped"（pipeline_manager 已知状态），推进不阻断，
    但汇总行注明"含 N 项 SKIP"；全流水线完成时若有 SKIP 阶段，不再打 "🎉 全流水线 approved"
  - --stage 传未知 ID：argparse 直接报错退出码 2，不再落到 "🎉 全流水线 approved"
  - championship 接线（v4.9 文档承诺兑现）：
      * 【脚本强制】check_numeric_sanity.py → S5 子步骤
      * 【脚本强制】freshness_check.py check → S8 终检前
      * 【证据文件存在性检查】blind-panel 聚合报告 qa/blind_panel_report.json →
        S8 产物缺失则该阶段不得 approved（rc=2 转 Agent 接力）
      * 【仅 handoff 提示，未脚本接线】figqa 碰撞门为 live matplotlib 检测，
        无离线批量模式，不硬接脚本，在 S4/S6 handoff 与 S8 输出中显式列出
  - 状态文件向后兼容：stage id 只增不改；新增字段（skip_count/skipped_steps）只增

用法：
  python tools/quality_gate/pipeline_runner.py init              # 初始化流水线
  python tools/quality_gate/pipeline_runner.py                   # 自动推进到下一个接力点
  python tools/quality_gate/pipeline_runner.py status            # 只看当前状态
  python tools/quality_gate/pipeline_runner.py --stage S5_evidence_gate  # 只跑指定阶段

退出码：
  0 = 当前批次推进完成（全 approved，或脚本阶段 PASS）
  1 = 有门禁 FAIL（需 Agent 修复后重跑）
  2 = 到 Agent 接力点（等 Agent 完成 + 用户决策后重跑）；也用于 --stage 非法参数
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── 路径 ──
WORK_DIR = Path.cwd()
OUTPUT_DIR = WORK_DIR / "paper_output"
STATE_DIR = OUTPUT_DIR / "state"
PIPELINE_FILE = STATE_DIR / "pipeline.json"
SKILLS_DIR = WORK_DIR / ".claude" / "skills"
TOOLS_QG = WORK_DIR / "tools" / "quality_gate"
QA_SCRIPTS = SKILLS_DIR / "quality-assurance-auditor" / "scripts"
PY = sys.executable

# ── 三态分类词汇（CR-5 + 第二轮审查 D/MEDIUM 兜底）──
# 子脚本 rc=0 时：stdout 出现以 skip/[skip] 开头的行，或报告 JSON status 命中 SKIP 词表 → SKIP
# PASS_WITH_SKIP（如 render_check 部分检查项跳过）归入 SKIP 侧一致处理：含跳过 ≠ 纯通过
SKIP_STATUSES = {"SKIP", "SKIPPED", "PASS_WITH_SKIP"}
# 报告 JSON status 命中 WARN 词表（rc=0）→ WARN（可见但不阻断）
WARN_STATUSES = {"WARN", "WARNING", "DEGRADED", "STALE"}
# 报告 JSON status 明示失败而子脚本 rc 却=0 → 以磁盘报告为准 FAIL（fail-closed）
FAIL_STATUSES = {"FAIL", "FAILED", "ERROR"}
# 报告 JSON status 显式通过词表；不在任何已知名单的未知词一律 WARN 兜底，绝不当 PASS
PASS_STATUSES = {"PASS", "PASSED", "OK", "SUCCESS"}
# 状态机里"已越过"的状态：approved=真通过；skipped=带 SKIP 推进（≠通过）
ADVANCED_STATUSES = {"approved", "skipped"}

# blind-panel 聚合报告 verdict 枚举（第二轮审查 HIGH-2）
# 来源：.claude/skills/blind-panel/SKILL.md 聚合 schema——
#   "verdict": "refine",      # pass | refine | block
# 只有 pass 是放行枚举；refine/block 须先按 bottleneck/fix_one_thing 修改后重评
BLIND_PANEL_VERDICTS = {"pass", "refine", "block"}
BLIND_PANEL_PASS_VERDICTS = {"pass"}


# ── 阶段定义（对齐 pipeline_manager.py STAGE_ORDER）──
# type=script  → runner 自动 subprocess 跑，PASS 才推进
# type=agent   → runner 输出 AGENT_HANDOFF，交 Agent 接力（产出齐备后下次自动推进）
# produces     → 目录型要求非空；文件型要求 ≥10 字节，.json 还要求可解析
# scripts[].report → 相对 paper_output/ 的报告 JSON 路径（读 status 字段做三态分类）
STAGES: list[dict] = [
    {
        "id": "S1_problem_analysis",
        "name": "审题选模",
        "type": "agent",
        "skills": ["problem-doc-model-selector", "award-paper-rag", "authoritative-data-harvester"],
        "produces": ["step1/problem_analysis.json"],
        "handoff": (
            "【审题选模】\n"
            "1. 读 outputs/INDEX.md + method_matching.md + scoring_rubric.md + phrase_bank.md + section-architecture.md，"
            "写 plan/knowledge_checkpoint.md（G5.1 知识查阅门必调）\n"
            "2. 读 problem_files/ 赛题 → 调 problem-doc-model-selector → 生成 paper_output/step1/problem_analysis.json\n"
            "3. 调 award-paper-rag 查 O 奖同类题用了什么方法\n"
            "4. 调 authoritative-data-harvester 拉外部数据（如需）"
        ),
    },
    {
        "id": "S2_modeling_route",
        "name": "模型路线 + G2.5 决策",
        "type": "agent",
        "skills": ["modeling-paper-rubric-and-model-selector", "model-selector", "decision-logger"],
        "produces": ["plan/model_route.json", "plan/model_selection_check.md"],
        "decision_gate": "G2.5（选模理由 ≥50 字，用户填，AI 不得代写）",
        "handoff": (
            "【模型路线】\n"
            "1. 调 modeling-paper-rubric-and-model-selector 生成 plan/model_route.json\n"
            "2. 对照 outputs/method_matching.md + model-selection-matrix.md，写 plan/model_selection_check.md（G5.2 选模对照门）\n"
            "3. 🚪 G2.5：用户填选模理由（≥50字）→ 调 decision-logger 记录"
        ),
    },
    {
        "id": "S3_code_generation",
        "name": "代码生成",
        "type": "agent",
        "skills": ["data-cleaning-and-visualization", "model-code-and-result-generator", "feature-engineering"],
        "produces": ["code/modeling"],  # 目录型 produce：必须存在且非空（空目录≠完成）
        "handoff": (
            "【代码生成】\n"
            "1. 查 resources/04_代码模板/ + resources/10_算法cookbook/，写 plan/code_reuse_check.md（G5.3 代码复用门）\n"
            "2. 调 data-cleaning-and-visualization 清洗数据 → paper_output/data_cleaned/\n"
            "3. 调 model-code-and-result-generator 生成 paper_output/code/modeling/ 建模代码\n"
            "4. 每个候选方法 ≤30 行 PoC 在真实数据上验证（G2 PoC 门）"
        ),
    },
    {
        "id": "S3b_code_verify",
        "name": "代码自证门（G4.6）",
        "type": "script",
        "scripts": [
            # report 接线（第二轮审查 F）：verify_gate 空项目写 status=SKIP 的报告
            # （qa/verify_gate_report.json），runner 侧 SKIP_STATUSES 直接接住显示 ⏭️，
            # 不再"跳过显示成 PASS"
            {"cmd": [PY, str(QA_SCRIPTS / "verify_gate.py")], "label": "G4.6 verify_gate（每模型 verify_*.py 全 PASS）",
             "report": "qa/verify_gate_report.json"},
        ],
    },
    {
        "id": "S4_run_results",
        "name": "运行结果 + G4.5 决策",
        "type": "agent",
        "skills": ["algorithm-runner", "math-figure", "chart-recommender", "decision-logger"],
        "produces": ["results/model_results.json", "results/metrics.json", "results/conclusions.json"],
        "decision_gate": "G4.5（结果确认 ≥30 字，用户填，AI 不得代写）",
        "handoff": (
            "【运行结果】\n"
            "1. 调 algorithm-runner 跑 paper_output/code/modeling/ 代码\n"
            "2. 生成 results/model_results.json + metrics.json + conclusions.json + tables/table_index.json\n"
            "3. 调 math-figure / chart-recommender 出图（每张过 render_check + figqa 碰撞门）\n"
            "4. 每模型配 verify_*.py（G4.6 自证门要求）\n"
            "5. 🚪 G4.5：用户确认结果合理性（≥30字）→ 调 decision-logger 记录"
        ),
    },
    {
        "id": "S5_evidence_gate",
        "name": "证据门禁（G5 总门）",
        "type": "script",
        # check_numeric_sanity 为 v4.9 championship 接线【脚本强制】（CR-9 遗留接线项）
        "scripts": [
            {"cmd": [PY, str(QA_SCRIPTS / "evidence_gate.py"), "--mode", "official"], "label": "G5 evidence_gate",
             "report": "qa/evidence_gate_report.json"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_parameter_consistency.py")], "label": "参数一致性",
             "report": "qa/parameter_consistency_report.json"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_result_reasonableness.py")], "label": "结果合理性",
             "report": "qa/result_reasonableness_report.json"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_number_consistency.py")], "label": "数字一致性",
             "report": "qa/number_consistency_report.json"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_numeric_sanity.py")], "label": "数值合理性（inf/nan/量级，championship 接线）",
             "report": "qa/numeric_sanity_report.json"},
        ],
    },
]
STAGES += [
    {
        "id": "S6_paper_writing",
        "name": "正式写作",
        "type": "agent",
        "skills": ["paper-formal-writer", "humanizer-zh-academic", "citation-tracer", "ai-failure-checker"],
        "produces": ["final_paper_source.md"],
        "handoff": (
            "【正式写作】\n"
            "1. 对照 section-architecture.md + evidence-pyramid.md + scoring_rubric.md，写 plan/writing_alignment_check.md（G5.4 写作对照门）\n"
            "2. 调 paper-formal-writer 出大纲 → Agent 全局写作 final_paper_source.md\n"
            "3. 调 humanizer-zh-academic 降AI味（G5.5 门，≥58/60）→ 生成 qa/humanizer_report.json\n"
            "4. 调 citation-tracer 引用验证（G5.8 门）\n"
            "5. 调 ai-failure-checker AI失败模式检查（G5.7 门，blocking=0）\n"
            "6. 🏆 championship 必做项（v4.9 默认模式）：\n"
            "   - figqa 碰撞门：live matplotlib 检测（无离线批量模式，此处不接脚本）——出图脚本内调用 "
            "assert_no_overlap(fig)（from .claude/skills/math-figure/scripts/figqa import assert_no_overlap），"
            "或提交前用 math-figure/scripts/pdf_qa.sh 复核编译 PDF\n"
            "   - blind-panel 3 座盲评将在 S8 终检前验收（qa/blind_panel_report.json 缺失则 S8 不得 approved），"
            "建议本阶段完稿后即启动（输入 final_paper.docx/PDF + 产物清单）"
        ),
    },
    {
        "id": "S7_format_gate",
        "name": "排版格式门",
        "type": "script",
        "scripts": [
            {"cmd": [PY, str(SKILLS_DIR / "paper-formal-writer" / "scripts" / "format_formal_docx.py")], "label": "Word 排版（OMML 公式 + 图片）"},
            {"cmd": [PY, str(SKILLS_DIR / "consistency-auditor" / "scripts" / "audit.py")], "label": "一致性审计（三审计层第1层）"},
            {"cmd": [PY, str(SKILLS_DIR / "completeness-auditor" / "scripts" / "audit.py")], "label": "完整性审计（三审计层第2层）"},
        ],
    },
    {
        "id": "S8_final_qa",
        "name": "最终QA（一键终检 + skill 调用门 + championship）",
        "type": "script",
        # freshness_check 为 v4.9 championship 接线【脚本强制】，置于终检前：
        # 源（赛题/代码）变化后旧 qa 报告标记 STALE，须重生成再终检
        "scripts": [
            {"cmd": [PY, str(SKILLS_DIR / "context-memory-keeper" / "scripts" / "freshness_check.py"), "check"],
             "label": "报告新鲜度 SHA-256（championship 接线，STALE 报告须重生成）"},
            {"cmd": [PY, str(TOOLS_QG / "final_gate_runner.py")], "label": "FINAL_GATE_RUNNER（实物+自证+证据+数字+公式+图片+skill）",
             "report": "qa/final_gate_report.json"},
        ],
        # championship 证据文件存在性检查（非脚本强制：只验产物存在与基本形态，
        # 不替 blind-panel skill 跑盲评——盲评本体是认知环节，由 Agent 调 skill 完成）
        "championship_evidence": [
            {
                "file": "qa/blind_panel_report.json",
                "item": "blind-panel 3 座盲评聚合报告（skill 定义产物：seats A/B/C + verdict）",
                "how": "调 blind-panel skill：3 座并行盲评 → Lead 聚合写 paper_output/qa/blind_panel_report.json（见 .claude/skills/blind-panel/SKILL.md）",
            },
        ],
        # figqa 无离线批量检查模式（live matplotlib import 门），不硬接脚本，仅在此显式提示
        "championship_handoff_only": [
            "figqa 碰撞门：出图时 assert_no_overlap(fig)（.claude/skills/math-figure/scripts/figqa.py）——live 检测无法离线重放，需在出图阶段（S4/S6）执行",
            "4 层反馈 L1-L4（L1 阶段 Critic / L2 跨阶段回检 / L3 Panel / L4 证据校准）：认知环节，由 Agent 按 qa-auditor feedback_layer1-4 参考文档执行，状态机不强制",
        ],
    },
]


# ── 状态读写（兼容 pipeline_manager.py 的 pipeline.json 格式）──
def load_state() -> dict | None:
    if not PIPELINE_FILE.exists():
        return None
    try:
        return json.loads(PIPELINE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    PIPELINE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def stage_status(state: dict, stage_id: str) -> str:
    return state.get("stages", {}).get(stage_id, {}).get("status", "not_started")


def set_stage_status(state: dict, stage_id: str, status: str) -> None:
    state.setdefault("stages", {}).setdefault(stage_id, {})["status"] = status
    save_state(state)


# ── 产出检查（判断 agent 阶段是否完成；CR-5 强化）──
def check_produces(stage: dict) -> tuple[bool, list[str]]:
    """返回 (是否齐备, 未达标清单)。

    强化点（CR-5 / G-05）：
      - 目录型 produce：必须存在且非空（空目录 = 未完成）
      - 文件型 produce：≥10 字节；.json 还必须 json.loads 成功（坏 JSON = 未完成）
    """
    produces = stage.get("produces", [])
    if not produces:
        return False, ["该阶段未定义 produces，无法判定完成"]
    problems: list[str] = []
    for p in produces:
        path = OUTPUT_DIR / p
        if not path.exists():
            problems.append(f"{p}: 不存在")
            continue
        if path.is_dir():
            try:
                empty = not any(path.iterdir())
            except OSError as exc:
                problems.append(f"{p}: 目录不可读（{exc}）")
                continue
            if empty:
                problems.append(f"{p}: 目录为空（空目录 ≠ 完成）")
            continue
        size = path.stat().st_size
        if size < 10:
            problems.append(f"{p}: 文件 {size} 字节 < 10（疑似空壳）")
            continue
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                problems.append(f"{p}: JSON 不可解析（坏 JSON = 未完成）：{exc}")
    return (not problems), problems


# ── 脚本执行 ──
def run_one_script(cmd: list[str], label: str) -> tuple[int, str, str]:
    """执行一个子脚本，返回 (returncode, stdout, 输出尾部)。"""
    print(f"  ▶ {label}")
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            cwd=str(WORK_DIR), timeout=900,
        )
    except Exception as exc:
        return 1, "", f"执行异常: {exc}"
    out = proc.stdout or ""
    tail = (out + (proc.stderr or ""))[-500:]
    return proc.returncode, out, tail


def _report_status(report_rel: str | None) -> str | None:
    """读子脚本报告 JSON 的 status 字段（相对 paper_output/）；读不到返回 None。"""
    if not report_rel:
        return None
    path = OUTPUT_DIR / report_rel
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(data, dict):
        raw = str(data.get("status", "")).strip()
        return raw.upper() or None
    return None


def classify_script_result(rc: int, stdout: str, script: dict) -> tuple[str, str]:
    """把子脚本运行结果分类为 PASS / SKIP / WARN / FAIL（CR-5 三态展示）。

    SKIP 识别（缺 qa_config 场景实测）：
      - check_parameter_consistency / check_result_reasonableness 在缺配置时
        stdout 打印 "SKIP：<原因>" 且 rc=0，报告 JSON status="SKIP"
      - check_numeric_sanity 在结果目录缺失时 stdout 打印 "[skip] ..." 且 rc=0
      - PASS_WITH_SKIP（render_check 部分检查项跳过）归 SKIP 侧，绝不显示成纯 PASS

    第二轮审查 D 兜底：rc=0 不再无条件当 PASS——
      - 报告 status 命中 FAIL 词表 → FAIL（子脚本 rc 与磁盘报告矛盾时，以报告为准）
      - 报告 status 是未知词（不在 SKIP/WARN/FAIL/PASS 任一名单）→ 至少 WARN
    """
    if rc != 0:
        return "FAIL", ""
    for ln in stdout.splitlines():
        low = ln.strip().lower()
        if low.startswith("skip") or low.startswith("[skip]"):
            return "SKIP", ln.strip()
    status = _report_status(script.get("report"))
    if status in SKIP_STATUSES:
        return "SKIP", f"报告 status={status}"
    if status in WARN_STATUSES:
        return "WARN", f"报告 status={status}"
    if status in FAIL_STATUSES:
        return "FAIL", f"报告 status={status}（子脚本 rc=0 但报告明示失败，以磁盘报告为准）"
    if status is None or status in PASS_STATUSES:
        return "PASS", ""
    return "WARN", f"报告 status={status} 不在已知名单（SKIP/WARN/FAIL/PASS），按 WARN 兜底"


# ── championship 证据检查（存在性检查，非脚本强制）──
def championship_missing_evidence(stage: dict) -> list[tuple[dict, str]]:
    """检查 championship_evidence 声明的产物文件。返回 [(evidence, 原因)]。"""
    missing: list[tuple[dict, str]] = []
    for ev in stage.get("championship_evidence", []):
        path = OUTPUT_DIR / ev["file"]
        if not path.exists():
            missing.append((ev, "文件不存在"))
            continue
        size = path.stat().st_size
        if size < 10:
            missing.append((ev, f"文件仅 {size} 字节（疑似占位）"))
            continue
        if path.suffix.lower() == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                missing.append((ev, f"JSON 不可解析：{exc}"))
                continue
            if not isinstance(data, dict):
                missing.append((ev, "JSON 顶层不是对象——不符合 blind-panel 聚合 schema"))
                continue
            # verdict 真消费（第二轮审查 HIGH-2）：旧版只查"键存在"，
            # 12 字节矛盾 JSON（三座互异+verdict=block）照样过；现在必须命中放行枚举
            verdict = str(data.get("verdict", "")).strip().lower()
            if verdict not in BLIND_PANEL_VERDICTS:
                missing.append((ev, f"verdict={data.get('verdict')!r} 不在枚举 pass|refine|block 内"
                                   f"（见 .claude/skills/blind-panel/SKILL.md 聚合 schema）"))
            elif verdict not in BLIND_PANEL_PASS_VERDICTS:
                missing.append((ev, f"盲评 verdict='{verdict}'（≠pass）——按 SKILL.md 须先按 bottleneck/"
                                   f"fix_one_thing 修改后重评，未解决的 refine/block 不得推进"))
            # seats：≥3 座且每座必须有数值 weighted_total（scorecard 核心字段）
            seats = data.get("seats")
            if not isinstance(seats, dict) or len(seats) < 3:
                missing.append((ev, "JSON 缺 seats（不足 3 座）——不符合 blind-panel 聚合 schema"))
            else:
                bad = [f"{sid}: weighted_total 非数值"
                       for sid, seat in seats.items()
                       if not (isinstance(seat, dict)
                               and isinstance(seat.get("weighted_total"), (int, float))
                               and not isinstance(seat.get("weighted_total"), bool))]
                if bad:
                    missing.append((ev, "座位加权总分校验失败：" + "; ".join(bad)))
            # 20 分冲突未仲裁 → 不得 clean pass（SKILL.md 聚合规则）
            agg = data.get("aggregate")
            conflicts = agg.get("evidence_conflicts") if isinstance(agg, dict) else None
            if conflicts:
                missing.append((ev, f"aggregate.evidence_conflicts 非空（{len(conflicts)} 处 >20 分冲突"
                                   f"未经 lead 仲裁）——未解决的证据冲突不得放行"))
    return missing


def print_championship_handoff(stage: dict, missing: list[tuple[dict, str]]) -> None:
    print(f"\n❌ [{stage['id']}] championship 证据缺失或不达标 — 该阶段不得 approved（v4.9 championship 为默认模式）")
    for ev, why in missing:
        print(f"    ✗ {ev['file']}（{why}）")
        print(f"      用途: {ev['item']}")
        print(f"      做法: {ev['how']}")
    only_notes = stage.get("championship_handoff_only", [])
    if only_notes:
        print(f"\n{'─' * 60}")
        print(">>> championship 必做项（无脚本可强制，需 Agent/人工执行）<<<")
        for line in only_notes:
            print(f"  • {line}")
        print(f"{'─' * 60}")
    print(f"\n{'─' * 60}")
    print(">>> AGENT_HANDOFF：完成上述 championship 必做项后重新运行 pipeline_runner.py <<<")
    print(f"{'─' * 60}\n")


def run_script_stage(stage: dict) -> int:
    print(f"\n═══ [{stage['id']}] {stage['name']} — 脚本自动 ═══")
    state = load_state()
    set_stage_status(state, stage["id"], "in_progress")

    n_pass = n_skip = n_warn = 0
    skipped_steps: list[str] = []
    for s in stage["scripts"]:
        rc, out, tail = run_one_script(s["cmd"], s["label"])
        status, note = classify_script_result(rc, out, s)
        if status == "PASS":
            n_pass += 1
            print("    ✅ PASS")
        elif status == "SKIP":
            n_skip += 1
            skipped_steps.append(s["label"])
            print(f"    ⏭️ SKIP — 未实际检查（≠ PASS）：{note[:200] or '子脚本显式跳过'}")
        elif status == "WARN":
            n_warn += 1
            print(f"    ⚠️ WARN — {note[:200]}")
        else:  # FAIL
            print("    ❌ FAIL")
            print(f"       输出尾部: {tail[-400:]}")
            set_stage_status(load_state(), stage["id"], "rework")
            print(f"\n❌ [{stage['id']}] 门禁未通过 — 请 Agent 修复后重跑 pipeline_runner.py")
            return 1

    # championship 证据文件存在性检查（非脚本强制；无产物 → 不得 approved）
    missing = championship_missing_evidence(stage)
    if missing:
        set_stage_status(load_state(), stage["id"], "in_progress")
        print_championship_handoff(stage, missing)
        return 2

    state = load_state() or {}
    entry = state.setdefault("stages", {}).setdefault(stage["id"], {})
    if n_skip > 0:
        # 总体标 SKIP：可见、不阻断、≠ approved；新增字段只增不改（向后兼容）
        entry["status"] = "skipped"
        entry["skip_count"] = n_skip
        entry["skipped_steps"] = skipped_steps
        save_state(state)
        print(f"⏭️ [{stage['id']}] 推进 — 含 {n_skip} 项 SKIP（SKIP≠PASS；"
              f"补齐 paper_output/plan/qa_config.json 等配置后可 --stage {stage['id']} 重跑补查）")
    else:
        entry["status"] = "approved"
        save_state(state)
        if n_warn:
            print(f"⚠️ [{stage['id']}] approved — 含 {n_warn} 项 WARN（见上）")
        else:
            print(f"✅ [{stage['id']}] approved — 推进下一阶段")
    return 0


# ── Agent 接力 ──
def agent_handoff(stage: dict) -> int:
    print(f"\n═══ [{stage['id']}] {stage['name']} — 🤖 Agent 接力 ═══")
    state = load_state()
    if stage_status(state, stage["id"]) == "not_started":
        set_stage_status(state, stage["id"], "in_progress")

    print(f"\n{'─'*60}\n>>> AGENT_HANDOFF <<<\n{'─'*60}")
    print(stage["handoff"])
    print(f"\n  调用 skill: {', '.join(stage.get('skills', []))}")
    if stage.get("decision_gate"):
        print(f"  🚪 用户决策门: {stage['decision_gate']}")
    print(f"{'─'*60}")
    print(f">>> 完成后重新运行: python tools/quality_gate/pipeline_runner.py <<<")
    print(f"{'─'*60}\n")
    return 2


# ── 状态打印 ──
def print_status() -> int:
    state = load_state()
    if not state:
        print(f"[runner] 流水线未初始化，请先: python tools/quality_gate/pipeline_runner.py init")
        return 1
    print(f"\n{'═'*60}\n  PIPELINE STATUS（v4.9）\n{'═'*60}")
    sym = {"not_started": "·", "in_progress": "▶", "approved": "✓", "rework": "↩", "skipped": "⏭"}
    for s in STAGES:
        st = stage_status(state, s["id"])
        typ = "脚本" if s["type"] == "script" else "Agent"
        note = ""
        if st == "skipped":
            n = state.get("stages", {}).get(s["id"], {}).get("skip_count")
            note = f"  ⏭ 含 {n} 项 SKIP（未检查≠通过）" if n else "  ⏭ 含 SKIP（未检查≠通过）"
        print(f"  {sym.get(st, '?')} [{s['id']}] {s['name']}  ({typ}){note}")
    approved = sum(1 for s in STAGES if stage_status(state, s["id"]) == "approved")
    skipped = sum(1 for s in STAGES if stage_status(state, s["id"]) == "skipped")
    print(f"{'─'*60}")
    line = f"  进度: {approved}/{len(STAGES)} approved"
    if skipped:
        line += f"，另有 {skipped} 个阶段含 SKIP（未检查≠通过）"
    print(line)
    nxt = next((s for s in STAGES if stage_status(state, s["id"]) not in ADVANCED_STATUSES), None)
    if nxt:
        print(f"  下一步: [{nxt['id']}] {nxt['name']} ({'脚本自动' if nxt['type']=='script' else 'Agent 接力'})")
    return 0


# ── 初始化 ──
def init_pipeline() -> int:
    if PIPELINE_FILE.exists():
        existing = load_state()
        if existing and existing.get("stages"):
            print(f"[runner] pipeline.json 已存在且含阶段状态：{PIPELINE_FILE}")
            print(f"[runner] 如需重置，删掉该文件再 init")
            return 0
    state = {
        "version": "v4.9",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "runner": "pipeline_runner.py v4.9",
        "stages": {s["id"]: {"status": "not_started"} for s in STAGES},
    }
    save_state(state)
    n_script = sum(1 for s in STAGES if s["type"] == "script")
    n_agent = sum(1 for s in STAGES if s["type"] == "agent")
    print(f"[runner] 流水线已初始化：{PIPELINE_FILE}")
    print(f"[runner] {len(STAGES)} 阶段 = {n_script} 脚本自动 + {n_agent} Agent 接力")
    print(f"[runner] 下一步: python tools/quality_gate/pipeline_runner.py  开始推进")
    return 0


# ── 主循环 ──
def main() -> int:
    ap = argparse.ArgumentParser(
        description="一键流水线调度器（v4.9）：脚本环节自动跑，认知环节 Agent 接力",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("command", nargs="?", default="run",
                    choices=["run", "init", "status"],
                    help="init=初始化 / status=看状态 / run=推进（默认）")
    # CR-5 修复：未知 stage id 由 argparse 直接拒绝（退出码 2），
    # 不会再落进 "🎉 全流水线 approved" 分支；显式 --stage 时已 approved/skipped 的阶段也会重跑
    ap.add_argument("--stage", choices=[s["id"] for s in STAGES],
                    help="只跑指定阶段（如 S5_evidence_gate）")
    args = ap.parse_args()

    if args.command == "init":
        return init_pipeline()
    if args.command == "status":
        return print_status()

    state = load_state()
    if not state:
        print(f"[runner] 流水线未初始化，请先: python tools/quality_gate/pipeline_runner.py init")
        return 1

    # 找下一个未 approved 的阶段（skipped = 带 SKIP 推进过，视为已越过，可 --stage 重跑补查）
    for stage in STAGES:
        sid = stage["id"]
        if args.stage and sid != args.stage:
            continue
        st = stage_status(state, sid)
        if st in ADVANCED_STATUSES and not args.stage:
            continue

        if stage["type"] == "script":
            return run_script_stage(stage)
        else:  # agent
            # 产出齐备 → 自动推进（Agent 已经在上一轮做完了）
            ok, problems = check_produces(stage)
            if ok:
                set_stage_status(load_state(), sid, "approved")
                print(f"✅ [{sid}] 产出已齐备 — 自动推进")
                continue
            for p in problems:
                print(f"  ✗ 产出未达标: {p}")
            return agent_handoff(stage)

    state = load_state() or {}
    skipped_stages = [s["id"] for s in STAGES if stage_status(state, s["id"]) == "skipped"]
    if skipped_stages:
        # 谨慎口径：SKIP ≠ PASS，存在 SKIP 时不打 "全流水线 approved"
        print(f"\n⚠️ 流水线推进完成 — 但 {len(skipped_stages)} 个阶段含 SKIP：{', '.join(skipped_stages)}")
        print(f"    SKIP = 未实际检查（多为缺 paper_output/plan/qa_config.json 等配置），不等于通过；")
        print(f"    补齐配置后运行: python tools/quality_gate/pipeline_runner.py --stage <阶段ID> 重跑补查")
    else:
        print(f"\n🎉 全流水线 approved — 所有 {len(STAGES)} 阶段通过")
    print(f"    最终交付: paper_output/final_paper.docx + code/ + figures/ + 答辩材料")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
