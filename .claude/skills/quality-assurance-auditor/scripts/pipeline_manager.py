#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GitOps 流水线状态机（适配本项目 S1-S8 工作流）。

融合自 AutoMCM-Pro/scripts/pipeline_manager.py（RealSeaberry/AutoMCM-Pro, 144★）。
适配要点：
  - 状态目录 paper_output/state/（对齐本项目输出约定，非 CUMCM_Workspace/）
  - 阶段对齐 S1-S8（读题→模型路线→代码→结果→证据门禁→写作→格式门禁→最终QA）
  - 去除 contest_git 硬依赖，Git 快照改为可选（复用本项目 git-snapshot skill）
  - 保留：not_started→in_progress→pending_review→approved↔rework 状态机
         + Markdown 注入防护 + 返工上限 + AP/Manual 双模式 + 并行阶段

与 quality-assurance-auditor/scripts/pipeline.py（路径/IO 工具）互补，不冲突：
  pipeline.py 负责"读什么文件"；pipeline_manager.py 负责"阶段推进与审查"。

命令：
  init --mode AP|MANUAL --contest CUMCM|MCM|ICM [--problems N] [--max-reworks 5]
  status
  start-stage <stage>
  request-review --stage S --summary "..." [--results ... --concerns ... --next ...]
  check-approval [--stage S]          → 打印 APPROVED / REWORK / PENDING
  advance <stage>
  rework <stage> [--feedback "..."]
  checkpoint-banner [--stage S]
  parallel-start <s1> <s2> ...
  parallel-status <s1> <s2> ...
  parallel-all-done <s1> ...          → 退出码 0=全完成 1=未完成
  suggest-parallel                    → 输出可并行的下一批阶段
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows GBK 控制台兼容：强制 stdout/stderr 走 utf-8，避免 emoji/中文崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# ── 路径（对齐本项目 paper_output/ 约定）──────────────────────────
OUTPUT_DIR = Path("paper_output")
STATE_DIR = OUTPUT_DIR / "state"
PIPELINE_FILE = STATE_DIR / "pipeline.json"
REVIEW_REQ_FILE = STATE_DIR / "review_request.md"
HUMAN_FILE = STATE_DIR / "human_intervention.md"
EVAL_LOG_FILE = OUTPUT_DIR / "qa" / "evaluation_log.md"

# ── 阶段顺序（对齐 S1-S8 工作流）─────────────────────────────────
STAGE_ORDER: list[str] = [
    "S1_problem_analysis",
    "S2_modeling_route",
    "S3_code_generation",
    "S3b_code_verify",      # 强制代码自证（G4.6 门）
    "S4_run_results",
    "S5_evidence_gate",
    "S6_paper_writing",
    "S7_format_gate",
    "S8_final_qa",
]

# 可并行阶段组：同组内可由不同 Agent 同时处理；prerequisite 必须 approved 后才能启动
PARALLEL_GROUPS: dict[str, dict] = {
    # 多子问题建模可并行（运行时按 problem_count 动态生成）
    "code_per_problem": {
        "stages": [],  # 动态
        "prerequisite": "S2_modeling_route",
        "description": "各子问题代码生成（互相独立，可并行）",
    },
}

STATUS_SYMBOLS: dict[str, str] = {
    "not_started": "·",
    "in_progress": "▶",
    "pending_review": "⏸",
    "approved": "✓",
    "rework": "↩",
    "skipped": "—",
}

# 注入防护：防止用户/AI 在状态文件中伪造控制标记
# （第二轮审查 B7 附带：全角形态与半角一并拦截，防全角标记对扫描隐身）
_INJECTION_PATTERNS = [
    "[APPROVED]", "[REWORK]", "[MANUAL_SPEC]",
    "【APPROVED】", "【REWORK】", "【MANUAL_SPEC】",
]

# ── HIL 审批标记（CR-6 修复）──────────────────────────────────
# 批准/返工标记必须独占一行：该行 strip 后恰好等于下列标记之一
# （行内不得含反引号或任何其它字符）。模板占位符改用全角【APPROVED】，
# 模板说明文字中不再出现可与匹配规则命中的半角 [APPROVED] 子串，
# 防止"全新模板文件天然 APPROVED"的绕过（CR-6）。
APPROVED_MARKS = ("[APPROVED]", "【APPROVED】")
REWORK_MARKS = ("[REWORK]", "【REWORK】")
# 指定形态（审批令牌绑定，第二轮审查 B-①）：全局 [APPROVED] 对任意在审阶段生效；
# [APPROVED S5] / 【APPROVED S5_evidence_gate】 只对记号匹配的阶段生效。
_BOUND_TOKEN = r"[A-Za-z0-9_\-\.]+"
_APPROVED_BOUND_RE = re.compile(rf"^[\[【]APPROVED[ \t　]+({_BOUND_TOKEN})[\]】]$")
_REWORK_BOUND_RE = re.compile(rf"^[\[【]REWORK[ \t　]+({_BOUND_TOKEN})[\]】]$")


def _marker_line_index(content: str, marks: tuple) -> int:
    """返回第一处"单独一行恰为某标记"的行号（0 起）；无则 -1。"""
    for i, raw in enumerate(content.splitlines()):
        if raw.strip() in marks:
            return i
    return -1


def _token_matches_stage(token: str, stage: str) -> bool:
    """绑定记号与目标阶段的匹配：全等，或记号恰为阶段 id 的下划线前缀。

    例：S5 ↔ S5_evidence_gate 匹配；S3 不匹配 S3b_code_verify（只认 '_' 边界，
    防前缀撞车误绑）。比较不区分大小写。
    """
    t, s = token.strip().upper(), stage.strip().upper()
    return t == s or s.startswith(t + "_")


def _scan_marker_lines(content: str) -> list[tuple[int, str, str]]:
    """扫描全部"独占一行"的审批标记，按行号升序返回 [(行号, APPROVED|REWORK, 绑定记号)]。

    绑定记号：全局形态为 ""；指定形态为记号本身。行内混排（模板说明、
    反引号包裹、前后缀文字）一律不命中——与 _marker_line_index 同源判定。
    """
    found: list[tuple[int, str, str]] = []
    for i, raw in enumerate(content.splitlines()):
        s = raw.strip()
        if s in APPROVED_MARKS:
            found.append((i, "APPROVED", ""))
            continue
        m = _APPROVED_BOUND_RE.match(s)
        if m:
            found.append((i, "APPROVED", m.group(1)))
            continue
        if s in REWORK_MARKS:
            found.append((i, "REWORK", ""))
            continue
        m = _REWORK_BOUND_RE.match(s)
        if m:
            found.append((i, "REWORK", m.group(1)))
    return found


def _replace_line(content: str, line_idx: int, replacement: str) -> str:
    """把指定行整行替换为 replacement（B7 修复：行级精确消费核心）。

    旧的 str.replace(mark, ..., 1) 会命中模板说明行里的标记子串，真标记行
    未被消费 → 一次人工批准连放两个阶段（第二轮审查 B7）。此处只动
    "整行恰为标记"的那一行，模板说明行里的子串不受影响。
    每次替换保持行数不变（整行→整行），因此对多个行号顺序替换不互相错位。
    """
    lines = content.splitlines()
    if not (0 <= line_idx < len(lines)):
        return content
    lines[line_idx] = replacement
    out = "\n".join(lines)
    return out + "\n" if content.endswith("\n") else out


def _consume_markers(content: str, relevant: list, stage: str) -> str:
    """把该阶段全部生效标记行整行改写为带时间戳的消费记录（第三轮审查 MEDIUM-A）。

    旧逻辑只消费 _approval_state 返回的 relevant[-1]（生效行）——同阶段文件中
    存在两个 [APPROVED S5] 时前一个残留，该阶段 rework 再入 pending_review 后
    无需人工即被残留标记自动放行。此处把 relevant 中每一行（全局形态 + 记号
    匹配该阶段的每一行）一并消费。消费记录形如 "[APPROVED — stage @ time]"，
    不等于任何标记形态（em dash 不在绑定记号字符类内），不会二次放行。
    """
    out = content
    for line_idx, kind, _tok in relevant:
        out = _replace_line(out, line_idx, f"[{kind} — {stage} @ {now()}]")
    return out


def _read_human_file() -> str | None:
    """单次读取 HUMAN_FILE，返回内容快照；不存在/读失败返回 None。

    B7 TOCTOU 修复（第三轮审查 LOW）：advance 的判定与消费必须共享同一份
    content 快照（读-改-写原子化到单进程视角）——旧实现 _approval_state 读
    一次、消费前再读一次，两次读之间文件被外部改动会 _replace_line 改错行。
    """
    if not HUMAN_FILE.exists():
        return None
    try:
        return HUMAN_FILE.read_text(encoding="utf-8")
    except OSError:
        return None


def _sanitize(text: str) -> str:
    """去除可能注入流水线控制标记的内容（[X] → ⟦X⟧）。"""
    for pat in _INJECTION_PATTERNS:
        text = text.replace(pat, pat.replace("[", "⟦").replace("]", "⟧"))
    return text


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load() -> dict:
    if not PIPELINE_FILE.exists():
        sys.exit("[pipeline] 流水线未初始化，请先运行: pipeline_manager.py init ...")
    try:
        return json.loads(PIPELINE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(
            f"[pipeline] pipeline.json 损坏，无法解析: {e}\n"
            f"  请检查文件或删除后重新 init: {PIPELINE_FILE}"
        )


def save(state: dict) -> None:
    state["updated_at"] = now()
    PIPELINE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _stage_entry(status: str = "not_started") -> dict:
    return {
        "status": status,
        "started_at": None,
        "completed_at": None,
        "approved_at": None,
        "review_round": 0,
        "notes": "",
    }


# ── 命令实现 ─────────────────────────────────────────────────────
def cmd_init(args: argparse.Namespace) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "qa").mkdir(parents=True, exist_ok=True)

    problem_count = int(args.problems)
    max_reworks = int(args.max_reworks)
    stages = {s: _stage_entry() for s in STAGE_ORDER}
    state = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "mode": args.mode.upper(),         # AP | MANUAL
        "contest": args.contest.upper(),   # CUMCM | MCM | ICM
        "created_at": now(),
        "updated_at": now(),
        "current_stage": "S1_problem_analysis",
        "blocked_at": None,
        "block_reason": "",
        "stages": stages,
        "total_reworks": 0,
        "problem_count": problem_count,
        "max_reworks": max_reworks,
    }
    save(state)

    if not REVIEW_REQ_FILE.exists():
        REVIEW_REQ_FILE.write_text(
            "# Review Request\n\n_(no review pending)_\n", encoding="utf-8"
        )
    if not HUMAN_FILE.exists():
        _write_intervention_template(args.mode.upper())

    print("[pipeline] 流水线初始化完成")
    print(f"  会话 ID  : {state['session_id']}")
    print(f"  模式     : {state['mode']}")
    print(f"  竞赛     : {state['contest']}")
    print(f"  子问题数 : {problem_count}"
          + (" → AP 多 Agent 并行已开启" if problem_count > 1 else "（顺序执行）"))
    print(f"  最大返工 : {max_reworks} 次/阶段")


def _write_intervention_template(mode: str) -> None:
    manual_spec = ""
    if mode == "MANUAL":
        manual_spec = """
---

## [MANUAL_SPEC]

> 请在此区块中填写每个问题的数学规格，AI 将 100% 按此实现。

### 问题一
- **模型类型**: （如：非线性规划 / 线性规划 / ODE / 回归）
- **决策变量**: （列举所有变量及含义）
- **目标函数**: （精确数学表达式，LaTeX 语法亦可）
- **约束条件**:
  - 约束一
  - 约束二
- **求解方法**: （如 scipy.optimize.minimize, method='SLSQP'）
- **特殊处理**: （如 数据对数变换、特殊初始值设定）

### 问题二
（同上）
"""
    HUMAN_FILE.write_text(
        f"# Human Intervention Log\n\n"
        f"> **模式**: {mode}\n"
        f"> **说明**: 在各阶段 AI 停下来等待时，在此文件填写审查结果。\n\n"
        f"## 审查结果区\n\n"
        f"_(AI 停下来时，把下面占位行改成 【APPROVED】（同意）或 【REWORK】（返工，"
        f"意见写在标记行的下一行起）。标记必须独占一行，行内不得有其它字符；"
        f"多阶段同时在审时用指定形态 【APPROVED 阶段ID】（如 【APPROVED S5_evidence_gate】，"
        f"前缀记号 【APPROVED S5】 亦可）。)_\n"
        f"\n【待填写：APPROVED 或 REWORK】\n"
        f"{manual_spec}",
        encoding="utf-8",
    )


def cmd_status(args: argparse.Namespace) -> tuple[str, str]:
    state = load()
    mode_badge = "🤖 AP" if state["mode"] == "AP" else "👤 MANUAL"
    print(f"\n{'═' * 58}")
    print(f"  Pipeline  [{mode_badge}]  {state['contest']}  会话 {state['session_id']}")
    print(f"{'═' * 58}")
    print(f"  当前阶段: {state['current_stage']}")
    if state.get("blocked_at"):
        print(f"  ⏸ 阻塞于: {state['blocked_at']}  ({state['block_reason']})")
    print("\n  阶段一览:")
    for stage, info in state["stages"].items():
        sym = STATUS_SYMBOLS.get(info["status"], "?")
        rw = f" (rework×{info['review_round']})" if info["review_round"] > 0 else ""
        print(f"    {sym}  {stage:<30} {info['status']}{rw}")
    print(f"{'═' * 58}\n")
    return state["current_stage"], state["stages"].get(
        state["current_stage"], {}
    ).get("status", "unknown")


def cmd_start_stage(args: argparse.Namespace) -> None:
    state = load()
    stage = args.stage
    if stage not in state["stages"]:
        state["stages"][stage] = _stage_entry()
    state["stages"][stage]["status"] = "in_progress"
    state["stages"][stage]["started_at"] = now()
    state["current_stage"] = stage
    state["blocked_at"] = None
    state["block_reason"] = ""
    save(state)
    print(f"[pipeline] ▶ 阶段开始: {stage}")


def cmd_request_review(args: argparse.Namespace) -> None:
    state = load()
    stage = args.stage
    if stage not in state["stages"]:
        state["stages"][stage] = _stage_entry()
    state["stages"][stage]["status"] = "pending_review"
    state["stages"][stage]["completed_at"] = now()
    state["stages"][stage]["review_round"] += 1
    state["blocked_at"] = now()
    state["block_reason"] = f"awaiting human review of {stage}"
    save(state)

    round_n = state["stages"][stage]["review_round"]
    summary = _sanitize(args.summary)
    results = _sanitize(args.results)
    concerns = _sanitize(args.concerns or "（无）")
    next_s = _sanitize(args.next or "（待定）")
    report = f"""# Review Request — Round {round_n}

**阶段**: `{stage}`
**时间**: {now()}
**模式**: {state['mode']}
**状态**: AWAITING HUMAN APPROVAL

---

## 本阶段工作摘要

{summary}

---

## 关键结果 / 验证数据

{results}

---

## 问题与不确定点

{concerns}

---

## 拟进入的下一阶段

{next_s}

---

## 审查指引

请阅读上述报告，然后在 `paper_output/state/human_intervention.md` 中填写：

- 同意继续 → 单独一行写 【APPROVED】（多阶段同时在审时用指定形态 【APPROVED {stage}】）
- 需要修改 → 单独一行写 【REWORK】，并在下一行起写明具体修改意见

填写完毕后，在终端输入「**继续**」并按 Enter 唤醒 AI。
"""
    REVIEW_REQ_FILE.write_text(report, encoding="utf-8")

    EVAL_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with EVAL_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(
            f"\n\n---\n\n## [{now()}] Review 请求 — {stage} (Round {round_n})\n\n"
            f"### 摘要\n{summary}\n\n### 结果\n{results}\n"
        )
    print("[pipeline] review_request.md 已更新")
    cmd_checkpoint_banner(args)


def cmd_check_approval(args: argparse.Namespace) -> str:
    """行级精确匹配（CR-6）+ 阶段绑定（第二轮审查 B-①）：
    必须存在单独一行恰为 [APPROVED]/【APPROVED】（或指定形态
    [APPROVED <stage>]/【APPROVED <stage>】）才算批准；行内混排一律不算。
    --stage 指定阶段时，绑定其它阶段的标记对本阶段不生效。"""
    stage = (args.stage or "").strip()
    verdict, detail, bound, _line_idx, _relevant = _approval_state(stage)
    print(verdict)
    if bound:
        print(f"(标记绑定阶段记号: {bound})")
    if detail:
        print(detail)
    return verdict


def _approval_state(
    stage: str = "", content: str | None = None
) -> tuple[str, str, str, int, list]:
    """读取 HUMAN_FILE 判定审批状态（检测器与消费端共用同一解析器）。

    返回 (verdict, detail, bound, line_idx, relevant)：
      - verdict ∈ {APPROVED, REWORK, PENDING}
      - detail：REWORK 时为标记行下一行起的修改意见；PENDING 时为原因说明
      - bound：生效标记的绑定记号（""=全局形态）
      - line_idx：生效标记行号（-1=无标记），advance 据此做行级精确消费
      - relevant：该阶段全部生效标记 [(行号, APPROVED|REWORK, 绑定记号)]——
        消费端（advance/rework）必须整组一并消费：只消费 relevant[-1] 会留下
        前面的同阶段重复标记（第三轮审查 MEDIUM-A：残留标记在 rework 再入
        pending_review 后无需人工即自动放行）

    规则（CR-6 + 第二轮审查 B + 第三轮审查 A/B）：
      - 标记必须独占一行；支持全局 [APPROVED] 与指定 [APPROVED <stage>] 两种形态
      - stage 非空时只统计与该阶段相关的标记（全局形态 + 记号匹配该阶段）；
        绑定其它阶段的标记对本阶段不生效
      - 最后写入优先：APPROVED 与 REWORK 并存时，文件中位置靠后的标记生效
      - content 非 None 时直接基于该快照判定，不再重读文件（B7 TOCTOU：读与
        写之间文件被外部改动会导致 _replace_line 改错行；消费端应传同一份快照）
    """
    if content is None:
        if not HUMAN_FILE.exists():
            return "PENDING", "（human_intervention.md 不存在）", "", -1, []
        try:
            content = HUMAN_FILE.read_text(encoding="utf-8")
        except OSError as e:
            return "PENDING", f"（human_intervention.md 读取失败: {e}）", "", -1, []
    markers = _scan_marker_lines(content)
    if not markers:
        return "PENDING", "（未检测到任何独占一行的审批标记）", "", -1, []
    if stage:
        relevant = [m for m in markers if not m[2] or _token_matches_stage(m[2], stage)]
    else:
        relevant = list(markers)
    if not relevant:
        others = "、".join(f"{kind}@{tok or '全局'}" for _, kind, tok in markers)
        return "PENDING", f"现有标记均绑定其它阶段（{others}），与 {stage} 无关", "", -1, []
    line_idx, kind, bound = relevant[-1]  # 行号升序 → 最后一个即文件中最靠后者
    if kind == "APPROVED":
        return "APPROVED", "", bound, line_idx, relevant
    feedback = "\n".join(content.splitlines()[line_idx + 1:]).strip()
    return "REWORK", feedback, bound, line_idx, relevant


def _print_approval_guidance(reason: str) -> None:
    print(
        f"[pipeline] ✗ advance 被拒绝：{reason}\n"
        f"  请在 paper_output/state/human_intervention.md 的「审查结果区」单独一行填写：\n"
        f"      【APPROVED】                  （仅一个阶段在审时的全局形态）\n"
        f"      【APPROVED <阶段ID>】         （多阶段同时在审时的指定形态，\n"
        f"                                     如 【APPROVED S5_evidence_gate】 或其前缀记号 【APPROVED S5】）\n"
        f"  （标记必须独占一行，行内不得含反引号或其它字符；需要修改则单独一行写 【REWORK】，"
        f"   并在下一行起写修改意见）\n"
        f"  然后重新运行: pipeline_manager.py advance <stage>",
        file=sys.stderr,
    )


def cmd_advance(args: argparse.Namespace) -> None:
    # CR-6：advance 不是绕过审批的旁门；第二轮审查 B：令牌绑定 + 乱序跳级封死
    state = load()
    stage = args.stage
    if stage not in state["stages"]:
        sys.exit(f"[pipeline] 未知阶段: {stage}")

    # 乱序跳级封死：审批令牌只对"已提交审查"（pending_review）的阶段生效
    cur_status = state["stages"][stage].get("status")
    if cur_status != "pending_review":
        print(
            f"[pipeline] ✗ advance 被拒绝：{stage} 当前状态为 '{cur_status}'（非 pending_review）。\n"
            f"  审批令牌与阶段绑定，不能跨阶段/跨状态套用——请先提交审查：\n"
            f"      pipeline_manager.py request-review --stage {stage} --summary \"...\"",
            file=sys.stderr,
        )
        sys.exit(1)

    # B7 TOCTOU 修复（第三轮审查 LOW）：读-判-写共享同一份 content 快照。
    # 旧实现 _approval_state 读一次、消费前再读一次，两次读之间文件被外部
    # 改动会 _replace_line 改错行；现判定与消费均基于同一份快照。
    content = _read_human_file()
    verdict, detail, bound, _line_idx, relevant = _approval_state(stage, content)
    if verdict != "APPROVED":
        reason = {
            "REWORK": f"审查结论为 REWORK（请先按修改意见返工，再重新提交审查）\n{detail}",
            "PENDING": detail or "未检测到人工批准标记",
        }.get(verdict, verdict)
        _print_approval_guidance(reason)
        sys.exit(1)

    # 多阶段同时 pending_review 时，全局标记无法定位批准对象 → 必须用指定形态
    pending = [s for s, info in state["stages"].items()
               if isinstance(info, dict) and info.get("status") == "pending_review"]
    if not bound and len(pending) > 1:
        print(
            f"[pipeline] ✗ advance 被拒绝：当前有 {len(pending)} 个阶段同时 pending_review"
            f"（{'、'.join(pending)}），全局 【APPROVED】 无法定位批准对象。\n"
            f"  请改用指定形态（单独一行）：\n"
            f"      【APPROVED {stage}】",
            file=sys.stderr,
        )
        sys.exit(1)

    state["stages"][stage]["status"] = "approved"
    state["stages"][stage]["approved_at"] = now()
    state["blocked_at"] = None
    state["block_reason"] = ""

    if stage in STAGE_ORDER:
        idx = STAGE_ORDER.index(stage)
        if idx + 1 < len(STAGE_ORDER):
            nxt = STAGE_ORDER[idx + 1]
            state["current_stage"] = nxt
            state["stages"][nxt]["status"] = "in_progress"
            state["stages"][nxt]["started_at"] = now()
            print(f"[pipeline] ✓ {stage} → approved")
            print(f"[pipeline] ▶ 推进至: {nxt}")
        else:
            state["current_stage"] = "complete"
            print(f"[pipeline] ✓ {stage} → approved")
            print("[pipeline] 🏁 流水线全部完成！")
    save(state)

    # B7 修复：行级精确消费——把"生效标记行"整行改写为带时间戳的消费记录。
    # 旧 str.replace(mark, ..., 1) 会命中模板说明行里的标记子串，真标记行
    # 未被消费 → 一次批准连放两个阶段。改写后的行不再等于任何标记，不会二次放行。
    # 第三轮审查 MEDIUM-A：消费的是该阶段全部生效标记行（含绑定匹配的每一行），
    # 且基于开头读入的同一份 content 快照改写——同阶段残留的重复 [APPROVED S5]
    # 一并清除，rework 再入 pending_review 后不会免人工自动放行。
    if content is not None and relevant:
        HUMAN_FILE.write_text(_consume_markers(content, relevant, stage), encoding="utf-8")


def cmd_rework(args: argparse.Namespace) -> None:
    state = load()
    stage = args.stage
    if stage not in state["stages"]:
        sys.exit(f"[pipeline] 未知阶段: {stage}")
    current_round = state["stages"][stage].get("review_round", 0)
    max_reworks = state.get("max_reworks", 5)
    if current_round >= max_reworks:
        print(
            f"[pipeline] ⚠ {stage} 已达返工上限 ({max_reworks} 次)。请人工介入，"
            f"或用 --max-reworks 提高上限重新 init。",
            file=sys.stderr,
        )
        sys.exit(2)

    state["stages"][stage]["status"] = "rework"
    state["total_reworks"] = state.get("total_reworks", 0) + 1
    state["current_stage"] = stage
    state["blocked_at"] = None
    save(state)

    EVAL_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with EVAL_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(
            f"\n\n---\n\n## [{now()}] Rework 开始 — {stage}\n\n"
            f"**修改意见**: {args.feedback or '（见 human_intervention.md）'}\n"
        )
    print(f"[pipeline] ↩ {stage} → rework")
    print("[pipeline] 请阅读 human_intervention.md 中的修改意见后开始 Rework")

    if HUMAN_FILE.exists():
        # B7 同源修复：与 advance 同口径——只把"生效 REWORK 标记行"整行消费为
        # "[REWORK — stage @ time]"，绝不 str.replace（会命中模板说明行子串）。
        # 第三轮审查 A/B 同步：整组 relevant 一并消费 + 读-判-写共享同一份快照
        content = _read_human_file()
        verdict, _detail, _bound, _line_idx, relevant = _approval_state(stage, content)
        if verdict == "REWORK" and content is not None and relevant:
            HUMAN_FILE.write_text(
                _consume_markers(content, relevant, stage), encoding="utf-8"
            )


def cmd_checkpoint_banner(args: argparse.Namespace) -> None:
    stage = getattr(args, "stage", "unknown") or "unknown"
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║  ⏸  CHECKPOINT — 等待人类审查                            ║
╠══════════════════════════════════════════════════════════╣
║  阶段：{stage:<50}║
║  报告：paper_output/state/review_request.md              ║
╠══════════════════════════════════════════════════════════╣
║  请操作：                                                ║
║  1. 阅读 paper_output/state/review_request.md            ║
║  2. 在 paper_output/state/human_intervention.md 填写意见 ║
║     • 同意继续  →  单独一行写入 【APPROVED】             ║
║     • 需要修改  →  单独一行写入 【REWORK】 + 具体指令    ║
║  3. 在终端输入「继续」后按 Enter 唤醒 AI                 ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def cmd_parallel_start(args: argparse.Namespace) -> None:
    state = load()
    started: list[str] = []
    for stage in args.stages:
        if stage not in state["stages"]:
            state["stages"][stage] = _stage_entry()
        state["stages"][stage]["status"] = "in_progress"
        state["stages"][stage]["started_at"] = now()
        started.append(stage)
    state["current_stage"] = " | ".join(started)
    state["blocked_at"] = None
    state["block_reason"] = ""
    save(state)
    print(f"[pipeline] ▶ 并行启动 {len(started)} 个阶段:")
    for s in started:
        print(f"    • {s}")
    print("[pipeline] 请为每个阶段分配独立的 Agent 子进程。")


def cmd_parallel_status(args: argparse.Namespace) -> bool:
    state = load()
    print(f"\n  并行阶段状态 ({len(args.stages)} 个)")
    print(f"  {'─' * 40}")
    all_approved = True
    for s in args.stages:
        info = state["stages"].get(s, {"status": "not_started", "review_round": 0})
        sym = STATUS_SYMBOLS.get(info["status"], "?")
        rw = f" (rework×{info['review_round']})" if info.get("review_round", 0) > 0 else ""
        print(f"  {sym}  {s:<32} {info['status']}{rw}")
        if info["status"] != "approved":
            all_approved = False
    print(f"  {'─' * 40}")
    print(f"  全部完成: {'✓ YES' if all_approved else '✗ NO (仍有未完成阶段)'}\n")
    return all_approved


def cmd_parallel_all_done(args: argparse.Namespace) -> None:
    state = load()
    done = all(
        state["stages"].get(s, {}).get("status") == "approved" for s in args.stages
    )
    if done:
        print(f"[pipeline] ✓ 并行组全部完成: {args.stages}")
        sys.exit(0)
    pending = [s for s in args.stages if state["stages"].get(s, {}).get("status") != "approved"]
    print(f"[pipeline] ✗ 尚未完成: {pending}")
    sys.exit(1)


def cmd_suggest_parallel(args: argparse.Namespace) -> None:
    """输出可并行启动的下一批阶段名（空格分隔）。退出码 0=有 / 1=无。"""
    state = load()
    n = state.get("problem_count", 1)
    if n <= 1:
        sys.exit(1)
    codes = [f"S3_code_generation_p{i}" for i in range(1, n + 1)]

    def st(stage: str) -> str:
        return state["stages"].get(stage, {}).get("status", "not_started")

    if st("S2_modeling_route") == "approved" and all(st(s) == "not_started" for s in codes):
        print(" ".join(codes))
        sys.exit(0)
    sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser(description="GitOps Pipeline Manager (本项目 S1-S8)")
    sub = p.add_subparsers(dest="command")

    pi = sub.add_parser("init")
    pi.add_argument("--mode", required=True, choices=["ap", "AP", "manual", "MANUAL"])
    pi.add_argument("--contest", required=True, choices=["cumcm", "CUMCM", "mcm", "MCM", "icm", "ICM"])
    pi.add_argument("--problems", type=int, default=1)
    pi.add_argument("--max-reworks", type=int, default=5, dest="max_reworks")

    sub.add_parser("status")

    ps = sub.add_parser("start-stage")
    ps.add_argument("stage")

    pr = sub.add_parser("request-review")
    pr.add_argument("--stage", required=True)
    pr.add_argument("--summary", required=True)
    pr.add_argument("--results", default="（见 review_request.md）")
    pr.add_argument("--concerns", default="")
    pr.add_argument("--next", default="")

    sub.add_parser("check-approval").add_argument("--stage", default="")

    pav = sub.add_parser("advance")
    pav.add_argument("stage")

    prw = sub.add_parser("rework")
    prw.add_argument("stage")
    prw.add_argument("--feedback", default="")

    pcb = sub.add_parser("checkpoint-banner")
    pcb.add_argument("--stage", default="")

    pps = sub.add_parser("parallel-start")
    pps.add_argument("stages", nargs="+")

    ppst = sub.add_parser("parallel-status")
    ppst.add_argument("stages", nargs="+")

    ppad = sub.add_parser("parallel-all-done")
    ppad.add_argument("stages", nargs="+")

    sub.add_parser("suggest-parallel")

    args = p.parse_args()
    dispatch = {
        "init": cmd_init,
        "status": cmd_status,
        "start-stage": cmd_start_stage,
        "request-review": cmd_request_review,
        "check-approval": cmd_check_approval,
        "advance": cmd_advance,
        "rework": cmd_rework,
        "checkpoint-banner": cmd_checkpoint_banner,
        "parallel-start": cmd_parallel_start,
        "parallel-status": cmd_parallel_status,
        "parallel-all-done": cmd_parallel_all_done,
        "suggest-parallel": cmd_suggest_parallel,
    }
    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
