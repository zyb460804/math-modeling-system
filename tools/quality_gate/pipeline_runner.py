#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PIPELINE RUNNER — 一键流水线调度器（v4.9）

把 paper-workflow-orchestrator 的路由逻辑代码化：
  - 脚本型环节（门禁/审计/格式）：自动 subprocess 跑，PASS 才推进
  - 认知型环节（审题/写作/盲评）：输出 AGENT_HANDOFF 指令，交 Agent 接力
  - 状态推进：复用 pipeline_manager.py 的 pipeline.json（GitOps 状态机）

设计哲学：
  脚本环节无感通过（不会再被 Agent 疏忽跳过）
  认知环节保留 LLM 判断质量（不强行脚本化）
  Agent 接力点明确（runner 停下输出指令，Agent 干完重跑 runner）

用法：
  python tools/quality_gate/pipeline_runner.py init              # 初始化流水线
  python tools/quality_gate/pipeline_runner.py                   # 自动推进到下一个接力点
  python tools/quality_gate/pipeline_runner.py status            # 只看当前状态
  python tools/quality_gate/pipeline_runner.py --stage S5_evidence_gate  # 只跑指定阶段

退出码：
  0 = 当前批次推进完成（全 approved，或脚本阶段 PASS）
  1 = 有门禁 FAIL（需 Agent 修复后重跑）
  2 = 到 Agent 接力点（等 Agent 完成 + 用户决策后重跑）
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


# ── 阶段定义（对齐 pipeline_manager.py STAGE_ORDER）──
# type=script  → runner 自动 subprocess 跑，PASS 才推进
# type=agent   → runner 输出 AGENT_HANDOFF，交 Agent 接力（产出齐备后下次自动推进）
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
        "produces": ["code/modeling"],  # 目录存在即可
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
            {"cmd": [PY, str(QA_SCRIPTS / "verify_gate.py")], "label": "G4.6 verify_gate（每模型 verify_*.py 全 PASS）"},
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
        "scripts": [
            {"cmd": [PY, str(QA_SCRIPTS / "evidence_gate.py"), "--mode", "official"], "label": "G5 evidence_gate"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_parameter_consistency.py")], "label": "参数一致性"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_result_reasonableness.py")], "label": "结果合理性"},
            {"cmd": [PY, str(QA_SCRIPTS / "check_number_consistency.py")], "label": "数字一致性"},
        ],
    },
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
            "5. 调 ai-failure-checker AI失败模式检查（G5.7 门，blocking=0）"
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
        "name": "最终QA（一键终检 + skill 调用门）",
        "type": "script",
        "scripts": [
            {"cmd": [PY, str(TOOLS_QG / "final_gate_runner.py")], "label": "FINAL_GATE_RUNNER（实物+自证+证据+数字+公式+图片+skill）"},
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


# ── 产出检查（判断 agent 阶段是否完成）──
def check_produces(stage: dict) -> bool:
    produces = stage.get("produces", [])
    if not produces:
        return False
    for p in produces:
        path = OUTPUT_DIR / p
        if not path.exists():
            return False
        if path.is_file() and path.stat().st_size < 10:
            return False
    return True


# ── 脚本执行 ──
def run_one_script(cmd: list[str], label: str) -> tuple[bool, str]:
    print(f"  ▶ {label}")
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            cwd=str(WORK_DIR), timeout=900,
        )
    except Exception as exc:
        return False, f"执行异常: {exc}"
    tail = ((proc.stdout or "") + (proc.stderr or ""))[-500:]
    return proc.returncode == 0, tail


def run_script_stage(stage: dict) -> int:
    print(f"\n═══ [{stage['id']}] {stage['name']} — 脚本自动 ═══")
    state = load_state()
    set_stage_status(state, stage["id"], "in_progress")

    for s in stage["scripts"]:
        ok, tail = run_one_script(s["cmd"], s["label"])
        if ok:
            print(f"    ✅ PASS")
        else:
            print(f"    ❌ FAIL")
            print(f"       输出尾部: {tail[-400:]}")
            set_stage_status(load_state(), stage["id"], "rework")
            print(f"\n❌ [{stage['id']}] 门禁未通过 — 请 Agent 修复后重跑 pipeline_runner.py")
            return 1

    set_stage_status(load_state(), stage["id"], "approved")
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
    print(f"\n{'─'*60}")
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
    sym = {"not_started": "·", "in_progress": "▶", "approved": "✓", "rework": "↩", "skipped": "—"}
    for s in STAGES:
        st = stage_status(state, s["id"])
        typ = "脚本" if s["type"] == "script" else "Agent"
        print(f"  {sym.get(st, '?')} [{s['id']}] {s['name']}  ({typ})")
    approved = sum(1 for s in STAGES if stage_status(state, s["id"]) == "approved")
    print(f"{'─'*60}")
    print(f"  进度: {approved}/{len(STAGES)} approved")
    if approved < len(STAGES):
        nxt = next((s for s in STAGES if stage_status(state, s["id"]) != "approved"), None)
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
    ap.add_argument("--stage", help="只跑指定阶段（如 S5_evidence_gate）")
    args = ap.parse_args()

    if args.command == "init":
        return init_pipeline()
    if args.command == "status":
        return print_status()

    state = load_state()
    if not state:
        print(f"[runner] 流水线未初始化，请先: python tools/quality_gate/pipeline_runner.py init")
        return 1

    # 找下一个未 approved 的阶段
    for stage in STAGES:
        sid = stage["id"]
        if args.stage and sid != args.stage:
            continue
        st = stage_status(state, sid)
        if st == "approved":
            continue

        if stage["type"] == "script":
            return run_script_stage(stage)
        else:  # agent
            # 产出齐备 → 自动推进（Agent 已经在上一轮做完了）
            if check_produces(stage):
                set_stage_status(load_state(), sid, "approved")
                print(f"✅ [{sid}] 产出已齐备 — 自动推进")
                continue
            return agent_handoff(stage)

    print(f"\n🎉 全流水线 approved — 所有 {len(STAGES)} 阶段通过")
    print(f"    最终交付: paper_output/final_paper.docx + code/ + figures/ + 答辩材料")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
