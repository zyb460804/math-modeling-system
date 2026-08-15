#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BLIND PANEL SCHEMA — championship 盲评聚合报告共用校验（第三轮审查 P0-1）

此前 final_gate_runner 与 pipeline_runner 各写一套口径，对同一份报告给出相反结论：
  - final_gate_runner.check_blind_panel_championship 只查 seats≥3 + verdict 键存在
    → 三座数值分 + verdict="block" 照样 PASS（交叉验证表 HIGH）
  - pipeline_runner.championship_missing_evidence 查 verdict 枚举，但每座
    weighted_total 只查 isinstance(int,float) → NaN/-50 照过；空座对象照过

本模块把校验收敛为唯一实现，两链 import 同一函数（同 verify_gate 的
missing_verify_for_models 被 final_gate_runner 复用的共用模式）：
  - tools/quality_gate/final_gate_runner.py   check_blind_panel_championship
  - tools/quality_gate/pipeline_runner.py     championship_missing_evidence

schema 依据 .claude/skills/blind-panel/SKILL.md：
  {"seats": {"A": {"weighted_total": 78.5, ...}, "B": {...}, "C": {...}},
   "verdict": "pass" | "refine" | "block",
   "aggregate": {"evidence_conflicts": [...]}}

校验口径（两链一致）：
  - verdict 必须命中枚举 {pass, refine, block}，且仅 pass 放行
    （第四轮审查：顶层与 aggregate.verdict 双位置都认，顶层优先；双写不一致 → 拒）
  - seats ≥3 座；每座 weighted_total 必须是有限数值且 ≥0
    （bool/NaN/inf/负数/缺失/非数值/座值为非对象 一律拒）
  - aggregate.evidence_conflicts 非空（>20 分冲突未经 lead 仲裁）→ 拒

第五轮复审（MEDIUM，2026-08-15）：校验器健壮性——evidence_conflicts 为非列表真值
（如 int 5）时旧版 len() 直接 TypeError 崩穿两链（final_gate_runner 整脚本
traceback、final_gate_report.json 都写不出来）。现约定：本模块对任何输入只产出
"问题条目"，绝不抛未捕获异常；校验器自身故障按 fail-closed 处理（记一条问题，
等价于不合规），消费方据此给结构化 FAIL step。
"""
from __future__ import annotations

import json
import math
from pathlib import Path

BLIND_PANEL_VERDICTS = {"pass", "refine", "block"}
BLIND_PANEL_PASS_VERDICTS = {"pass"}
MIN_SEATS = 3
MIN_REPORT_BYTES = 10


def validate_blind_panel_data(data: object) -> list[str]:
    """校验已解析的盲评聚合 JSON（dict）。返回问题清单（空列表 = 合格且 verdict=pass）。

    第五轮复审（MEDIUM）：整体兜底——实现层任何内部异常都在此收敛为一条问题
    条目（fail-closed，等价于不合规），绝不以 traceback 穿透
    final_gate_runner / pipeline_runner 两条消费链。
    """
    try:
        return _validate_blind_panel_data_impl(data)
    except Exception as exc:  # noqa: BLE001 —— 校验器自身故障也必须以"问题条目"落地
        return [f"盲评校验器内部异常（fail-closed，按不合规处理）: {type(exc).__name__}: {exc}"]


def _validate_blind_panel_data_impl(data: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["JSON 顶层不是对象——不符合 blind-panel 聚合 schema"]
    # 第四轮审查：verdict 双位置兼容——SKILL.md 示例为顶层，但 2026-08-15 现场
    # blind-panel 实跑产物把 verdict 落在 aggregate.verdict（顶层无此键），旧校验
    # 只读顶层会把这类报告一律判"verdict 缺失"。现两处都认（顶层优先），
    # 双写且不一致 → 拒（自相矛盾的聚合报告不得放行）；两处皆缺/非法 → 拒。
    agg = data.get("aggregate")
    top_verdict = data.get("verdict")
    agg_verdict = agg.get("verdict") if isinstance(agg, dict) else None

    def _norm(v) -> str:
        return str(v).strip().lower() if v is not None else ""

    tv, av = _norm(top_verdict), _norm(agg_verdict)
    if tv and av and tv != av:
        problems.append(
            f"顶层 verdict={top_verdict!r} 与 aggregate.verdict={agg_verdict!r} 不一致"
            f"——聚合报告自相矛盾，不得放行"
        )
        verdict = ""
    else:
        verdict = tv or av
    if verdict not in BLIND_PANEL_VERDICTS:
        problems.append(
            f"verdict={top_verdict if top_verdict is not None else agg_verdict!r} 不在枚举 "
            f"pass|refine|block 内（顶层与 aggregate.verdict 均缺失或非法；"
            f"见 .claude/skills/blind-panel/SKILL.md 聚合 schema）"
        )
    elif verdict not in BLIND_PANEL_PASS_VERDICTS:
        problems.append(
            f"盲评 verdict='{verdict}'（≠pass）——按 SKILL.md 须先按 bottleneck/"
            f"fix_one_thing 修改后重评，未解决的 refine/block 不得放行"
        )
    seats = data.get("seats")
    if not isinstance(seats, dict) or len(seats) < MIN_SEATS:
        n_seats = len(seats) if isinstance(seats, dict) else 0
        problems.append(
            f"缺 seats（不足 {MIN_SEATS} 座，实际 {n_seats}）——不符合 blind-panel 聚合 schema"
        )
    else:
        bad: list[str] = []
        for sid, seat in seats.items():
            if not isinstance(seat, dict):
                bad.append(f"{sid}: 座位值非对象")
                continue
            wt = seat.get("weighted_total")
            # 第三轮审查 MEDIUM：weighted_total 必须是有限非负数值——
            # bool 是 int 子类须排除；NaN/inf 过 isinstance(float) 须 isfinite 拦；
            # -50 之类负分无合法来源须下界拦
            if (isinstance(wt, bool) or not isinstance(wt, (int, float))
                    or not math.isfinite(wt) or wt < 0):
                bad.append(f"{sid}: weighted_total={wt!r} 非有限非负数值（NaN/负分/缺失/非数值一律拒）")
        if bad:
            problems.append("座位加权总分校验失败：" + "; ".join(bad))
    conflicts = agg.get("evidence_conflicts") if isinstance(agg, dict) else None
    if conflicts:
        if isinstance(conflicts, list):
            problems.append(
                f"aggregate.evidence_conflicts 非空（{len(conflicts)} 处 >20 分冲突"
                f"未经 lead 仲裁）——未解决的证据冲突不得放行"
            )
        else:
            # 第五轮复审（MEDIUM）：非列表真值（int 5 / 非空 dict / 非空 str 等）旧版
            # len() 直接 TypeError 崩穿两链——现归入问题清单（schema 应为冲突条目数组）
            problems.append(
                f"aggregate.evidence_conflicts 非列表（实际类型 {type(conflicts).__name__}）"
                f"——不符合 blind-panel 聚合 schema（应为冲突条目数组），不得放行"
            )
    return problems


def blind_panel_report_problems(path: Path) -> tuple[list[str], object]:
    """文件级 + schema 级校验。返回 (问题清单, 解析出的 JSON 对象或 None)。

    文件级：不存在 / 小于 10 字节疑似占位 / JSON 不可解析。
    问题清单为空 = 报告在案、可解析、且通过 validate_blind_panel_data 全部校验。
    """
    if not path.exists():
        return [f"文件不存在：{path}"], None
    try:
        size = path.stat().st_size
    except OSError as exc:  # 并发删除等竞态：fail-closed 记问题，不崩穿
        return [f"文件状态不可读: {exc}"], None
    if size < MIN_REPORT_BYTES:
        return [f"文件仅 {size} 字节（疑似占位）"], None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"JSON 不可解析：{exc}"], None
    return validate_blind_panel_data(data), data
