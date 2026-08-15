import argparse
import json
import math
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
QA_DIR = OUTPUT_DIR / "qa"
MODEL_ROUTE_FILE = OUTPUT_DIR / "plan" / "model_route.json"
# P2-16（H-7 部分）：figure/table 索引双候选（根 + figures//tables/ 子目录），
# 与 consistency-auditor / completeness-auditor（ARTIFACT_FALLBACKS）对齐同一契约
FIGURE_INDEX_CANDIDATES = [OUTPUT_DIR / "figure_index.json", OUTPUT_DIR / "figures" / "figure_index.json"]
TABLE_INDEX_CANDIDATES = [OUTPUT_DIR / "tables" / "table_index.json", OUTPUT_DIR / "table_index.json"]
MODEL_RESULTS_FILE = OUTPUT_DIR / "results" / "model_results.json"
METRICS_FILE = OUTPUT_DIR / "results" / "metrics.json"
CONCLUSIONS_FILE = OUTPUT_DIR / "results" / "conclusions.json"
TASKS_FILE = OUTPUT_DIR / "tasks.json"
REPORT_JSON = QA_DIR / "evidence_gate_report.json"
REPORT_MD = QA_DIR / "evidence_gate_report.md"


def reconfigure_paths(paper_dir: str) -> None:
    """--paper-dir 重定向（R1）：统一重绑所有 paper_output 路径常量。

    - 默认值 "paper_output" 与模块级初值一致 → 无参调用行为与旧版完全相同（兼容）；
    - 传相对路径时相对当前工作目录解析（BASE_DIR / paper_dir），传绝对路径时
      pathlib 拼接天然取绝对值——用户把作品目录放到桌面等场景可指向正确对象；
    - 各函数均在调用时读取这些模块级常量，故 main() 里 parse_args 后重绑即全局生效。
    """
    global OUTPUT_DIR, QA_DIR, MODEL_ROUTE_FILE, FIGURE_INDEX_CANDIDATES, TABLE_INDEX_CANDIDATES
    global MODEL_RESULTS_FILE, METRICS_FILE, CONCLUSIONS_FILE, TASKS_FILE, REPORT_JSON, REPORT_MD
    OUTPUT_DIR = BASE_DIR / paper_dir
    QA_DIR = OUTPUT_DIR / "qa"
    MODEL_ROUTE_FILE = OUTPUT_DIR / "plan" / "model_route.json"
    FIGURE_INDEX_CANDIDATES = [OUTPUT_DIR / "figure_index.json", OUTPUT_DIR / "figures" / "figure_index.json"]
    TABLE_INDEX_CANDIDATES = [OUTPUT_DIR / "tables" / "table_index.json", OUTPUT_DIR / "table_index.json"]
    MODEL_RESULTS_FILE = OUTPUT_DIR / "results" / "model_results.json"
    METRICS_FILE = OUTPUT_DIR / "results" / "metrics.json"
    CONCLUSIONS_FILE = OUTPUT_DIR / "results" / "conclusions.json"
    TASKS_FILE = OUTPUT_DIR / "tasks.json"
    REPORT_JSON = QA_DIR / "evidence_gate_report.json"
    REPORT_MD = QA_DIR / "evidence_gate_report.md"

# freshness_check.py 位置（同仓 .claude/skills/ 下，按 __file__ 定位，不依赖 cwd）
FRESHNESS_SCRIPT = (
    Path(__file__).resolve().parents[2] / "context-memory-keeper" / "scripts" / "freshness_check.py"
)

# P2-13：provenance.source_code_path 必须是真实源码后缀（此前任意存在文件都算数）
SOURCE_CODE_SUFFIXES = (".py", ".m")

# CR-8/G-02：增补 "TBD" 与 "待补"（手写索引/结果常用占位写法，此前不在坏状态表内直接放行）
BAD_STATUSES = {
    "missing",
    "needs_real_modeling",
    "draft_contract",
    "to_be_filled",
    "template",
    "draft",
    "scaffold_result_needs_review",
    "TBD",
    "待补",
}

# figures/ 目录视为"图片"的扩展名（双向 diff 用）
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tif", ".tiff", ".pdf"}

# 判断来源字符串是否"像一个文件路径"（含路径分隔符，或以扩展名结尾）
_PATH_LIKE_RE = re.compile(r"\.[A-Za-z0-9]{1,6}$")


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__error__": str(exc)}


def first_existing(candidates: list[Path]) -> Path:
    """返回第一个存在的候选路径；全不存在时返回首选候选（供报错信息使用）。"""
    return next((c for c in candidates if c.exists()), candidates[0])


def question_ids(model_route: Any) -> list[str]:
    questions = model_route.get("questions") if isinstance(model_route, dict) else []
    if not isinstance(questions, list):
        return []
    result = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("question_id") or item.get("id") or "").strip()
        if qid:
            result.append(qid)
    return sorted(set(result))


def grouped_items(data: Any, key: str) -> dict[str, list[dict[str, Any]]]:
    items = data.get(key) if isinstance(data, dict) else []
    grouped: dict[str, list[dict[str, Any]]] = {}
    if not isinstance(items, list):
        return grouped
    for item in items:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("question_id") or "").strip()
        if qid:
            grouped.setdefault(qid, []).append(item)
    return grouped


def result_items(data: Any) -> dict[str, dict[str, Any]]:
    questions = data.get("questions") if isinstance(data, dict) else []
    grouped: dict[str, dict[str, Any]] = {}
    if not isinstance(questions, list):
        return grouped
    for item in questions:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("question_id") or "").strip()
        if qid:
            grouped[qid] = item
    return grouped


def figure_items(data: Any) -> dict[str, list[dict[str, Any]]]:
    return grouped_items(data, "figures")


def table_items(data: Any) -> dict[str, list[dict[str, Any]]]:
    return grouped_items(data, "tables")


def status_of(item: dict[str, Any] | None) -> str:
    if not item:
        return "missing"
    return str(item.get("evidence_status") or item.get("status") or "").strip()


def artifact_candidates(path_text: object) -> list[Path]:
    """条目/来源路径的磁盘候选位置：仓库根相对、paper_output 相对；绝对路径原样。

    CR-8：一切存在性判断以"候选命中磁盘"为准，不再信任 JSON 自报的 exists 字段。
    兼容 tasks.json 的 "file.json#Q1" 指针写法——# 后为 JSON 内锚点，不属于路径。
    """
    text = str(path_text or "").strip().strip("<>").split("#")[0].strip()
    if not text:
        return []
    path = Path(text)
    if path.is_absolute():
        return [path]
    return [BASE_DIR / path, OUTPUT_DIR / path]


def resolve_artifact(path_text: object) -> Path:
    """返回第一个存在的候选路径；全不存在时返回首选候选（供报错信息使用）。"""
    candidates = artifact_candidates(path_text)
    if not candidates:
        return BASE_DIR
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def looks_like_file_path(text: str) -> bool:
    """粗判来源字符串是否为文件路径（含分隔符或带扩展名结尾）。

    table_index 的 source 允许写「论文正文」这类非文件来源——无法用磁盘事实核验，
    降为 WARNING 提示，而不是误判成"文件不存在"的 FAIL。
    """
    return ("/" in text) or ("\\" in text) or bool(_PATH_LIKE_RE.search(text))


def index_entry_path(entry: dict[str, Any]) -> str | None:
    """取索引条目的产物路径字段（figure 条目用 path，table 条目用 source，兼容别名）。"""
    for field in ("path", "source", "file", "file_path"):
        text = str(entry.get(field) or "").strip()
        if text:
            return text
    return None


def check_index_entries_disk(entries: list[dict[str, Any]], kind: str) -> tuple[list[str], list[str]]:
    """逐条核验 figure/table 索引条目声明的产物文件在磁盘真实存在。

    定级（CR-8 + P1-7 幽灵链收口）：
    - 未声明 path/source 路径 → FAIL（CRITICAL）：索引条目必须声明可核验的产物路径，
      无路径=不可核验，不装作已核验（旧 WARNING 会让"正文见图N + 索引无 path + 磁盘无实物"
      的幽灵图表链全链零 FAIL）；
    - 来源非文件（如「论文正文」）→ FAIL（CRITICAL）：同上，非文件来源同样不可核验；
    - 声明了文件路径但磁盘不存在 → FAIL（CRITICAL）：论文引用了不存在的证据。
    条目自报的 exists 字段一律忽略，只认磁盘事实。
    """
    failures: list[str] = []
    warnings: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        qid = str(entry.get("question_id") or "ALL")
        ident = str(entry.get("figure_id") or entry.get("id") or entry.get("title") or "?")
        text = index_entry_path(entry)
        if text is None:
            failures.append(
                f"{qid}: {kind}条目 [{ident}] 未声明 path/source 产物路径——"
                f"索引条目必须声明可核验的产物路径（无路径=不可核验，不装作已核验）"
            )
            continue
        if not looks_like_file_path(text):
            failures.append(
                f"{qid}: {kind}条目 [{ident}] 来源「{text}」非文件路径——"
                f"索引条目必须声明可核验的产物路径（非文件来源=不可核验，不装作已核验）"
            )
            continue
        if not any(candidate.exists() for candidate in artifact_candidates(text)):
            failures.append(f"{qid}: {kind}条目 [{ident}] 指向的文件不存在（磁盘事实）：{text}")
    return failures, warnings


def diff_figures_dir_vs_index(figure_entries: list[dict[str, Any]]) -> list[str]:
    """figures/ 目录实际图片清单 vs figure_index.json 条目的双向 diff（CR-8/M-12）。

    定级斟酌：
    - 索引有条目但磁盘无图 → FAIL：由 check_index_entries_disk 承担（引用不存在的证据=伪造风险）；
    - 磁盘有图但索引无条目 → WARNING：图已产出但未登记，属可追溯性缺口（可能是废稿/未用图），
      不必然是造假，故提示而不阻断；索引同步由 figure skill 收口。
    """
    figures_dir = OUTPUT_DIR / "figures"
    disk_images: set[str] = set()
    if figures_dir.is_dir():
        for path in figures_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                disk_images.add(os.path.normcase(str(path.resolve())))

    indexed: set[str] = set()
    for entry in figure_entries:
        if not isinstance(entry, dict):
            continue
        text = index_entry_path(entry)
        if text is None or not looks_like_file_path(text):
            continue
        candidates = artifact_candidates(text)
        if not candidates:
            continue
        hit = next((c for c in candidates if c.exists()), candidates[0])
        indexed.add(os.path.normcase(str(hit.resolve())))

    disk_only = disk_images - indexed
    return [
        f"figures/ 目录存在未登记进 figure_index.json 的图片（可追溯性缺口）：{path}"
        for path in sorted(disk_only)
    ]


def check_task_artifacts(task_map: dict[str, list[dict[str, Any]]]) -> list[str]:
    """tasks.json 每条 artifact 路径验磁盘存在（容忍 #锚点 后缀）。

    定级斟酌：缺失记 WARNING 而非 FAIL——tasks.json 是任务追踪的辅助证据；
    主证据链（model_results 的 provenance.output_artifacts 缺失）已是 FAIL 级，
    辅助记录缺文件提示即可，避免对合法中间状态误杀。
    """
    warnings: list[str] = []
    for qid, entries in task_map.items():
        for entry in entries:
            raw = str(entry.get("artifact") or "").strip()
            if not raw:
                continue
            if not any(candidate.exists() for candidate in artifact_candidates(raw)):
                warnings.append(f"{qid}: tasks.json artifact 不存在（磁盘事实）：{raw}")
    return warnings


def provenance_failures(item: dict[str, Any]) -> list[str]:
    provenance = item.get("execution_provenance")
    if not isinstance(provenance, dict):
        return ["缺少 execution_provenance，无法证明结果来自实际代码运行"]

    failures: list[str] = []
    source_code = resolve_artifact(provenance.get("source_code_path"))
    if not provenance.get("source_code_path"):
        failures.append("execution_provenance.source_code_path 为空")
    elif not source_code.exists():
        failures.append(f"source_code_path 不存在：{source_code}")
    elif source_code.suffix.lower() not in SOURCE_CODE_SUFFIXES:
        # P2-13：此前任意存在文件都算"有源码"（如 .txt/.json），现在必须是真实源码后缀
        failures.append(
            f"source_code_path 必须为 .py/.m 源码文件，当前后缀「{source_code.suffix or '无后缀'}」：{source_code}"
        )

    if provenance.get("run_exit_code") not in (0, "0"):
        failures.append(f"run_exit_code 不是 0：{provenance.get('run_exit_code')}")

    if not str(provenance.get("run_command") or "").strip():
        failures.append("execution_provenance.run_command 为空")

    for artifact in provenance.get("output_artifacts", []) or []:
        artifact_path = resolve_artifact(artifact)
        if not artifact_path.exists():
            failures.append(f"输出产物不存在：{artifact}")
    return failures


def provenance_drift_warnings(item: dict[str, Any]) -> list[str]:
    """源文件 mtime 晚于任一输出产物 → 改码未重跑的漂移信号（P2-13）。

    分级：WARNING 不 FAIL——源比产物新只是"结果可能过期"的线索（重跑前的正常
    中间态、或产物由别的入口生成都可能触发），如实提示而非阻断。
    """
    provenance = item.get("execution_provenance")
    if not isinstance(provenance, dict):
        return []
    if not str(provenance.get("source_code_path") or "").strip():
        return []
    source = resolve_artifact(provenance.get("source_code_path"))
    if not source.exists() or source.suffix.lower() not in SOURCE_CODE_SUFFIXES:
        return []  # 后缀/存在性问题由 provenance_failures 以 FAIL 级报告，此处不重复
    try:
        source_mtime = source.stat().st_mtime
    except OSError:
        return []
    warnings: list[str] = []
    for artifact in provenance.get("output_artifacts", []) or []:
        artifact_path = resolve_artifact(artifact)
        if not artifact_path.exists():
            continue
        try:
            artifact_mtime = artifact_path.stat().st_mtime
        except OSError:
            continue
        if source_mtime > artifact_mtime:
            warnings.append(
                f"源码 {source.name} 比产物 {artifact} 新（源 mtime 晚于产物）——"
                f"源码改后可能未重跑，结果可能过期，建议重跑后再冻结数字"
            )
    return warnings


def check_code_quality(item: dict[str, Any]) -> list[str]:
    """检查源代码是否为 stub（包含 TODO 标记、文件过小等）。"""
    warnings: list[str] = []
    provenance = item.get("execution_provenance")
    if not isinstance(provenance, dict):
        return warnings

    source_path = resolve_artifact(provenance.get("source_code_path"))
    if not source_path.exists():
        return warnings

    try:
        content = source_path.read_text(encoding="utf-8")
        # 检查是否包含 stub 标记
        stub_markers = ["# TODO", "scaffold", "auto_generated", "needs_real_modeling"]
        found_markers = [m for m in stub_markers if m.lower() in content.lower()]
        if found_markers:
            warnings.append(f"源代码可能为脚手架/占位代码，包含标记：{', '.join(found_markers)}")

        # 检查文件大小（stub 通常很小）
        file_size = source_path.stat().st_size
        if file_size < 200:
            warnings.append(f"源代码文件过小 ({file_size} bytes)，可能为占位代码")
    except Exception:
        pass

    return warnings


def check_question_coverage(
    model_route: Any,
    result_map: dict[str, dict[str, Any]],
) -> list[str]:
    """检查 model_route 中的所有子问题是否都在 model_results 中有覆盖。"""
    failures: list[str] = []
    route_questions = model_route.get("questions") if isinstance(model_route, dict) else []
    if not isinstance(route_questions, list):
        return failures

    for item in route_questions:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("question_id") or item.get("id") or "").strip()
        if not qid:
            continue
        if qid not in result_map:
            failures.append(f"{qid}: model_route.json 中定义了该子问题，但 model_results.json 中缺少对应结果")

    return failures


# 嵌套 metrics schema 下的占位字符串（小写比较）；出现即视为"无真实值"
_PLACEHOLDER_STRINGS = {
    "", "to_be_filled", "tbd", "待补", "待填", "待定", "missing", "draft",
    "draft_contract", "template", "n/a", "na", "nan", "none",
}


def is_real_metric_value(value: Any) -> bool:
    """嵌套 metrics schema 下的"真实值"判定：数值/布尔/非空列表/非占位字符串。"""
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return value == value and not math.isinf(value)  # 排除 NaN/inf
    if isinstance(value, (list, tuple)):
        return len(value) > 0
    if isinstance(value, str):
        return value.strip().lower() not in _PLACEHOLDER_STRINGS
    return True


def check_metric_richness(
    metric_items: list[dict[str, Any]],
    qid: str,
) -> list[str]:
    """指标丰富度检查（M-14 修复：双 schema 兼容）。

    - 现行嵌套 schema：条目形如 {"question_id": "Q1", "metrics": {name: 真实数值}}，
      无 status/value 字段——metrics 下每个"真实值"键计 filled。旧逻辑只认
      status/value，对该 schema 完全空转，还对满真值的条目误报"均为 to_be_filled"。
    - 旧扁平 schema：条目带 {"status": ..., "value": ...}，沿用旧口径，保持兼容。
    """
    warnings: list[str] = []
    if not metric_items:
        return warnings

    filled_count = 0
    total_count = 0
    for item in metric_items:
        nested = item.get("metrics") if isinstance(item, dict) else None
        if isinstance(nested, dict):
            # 现行嵌套 schema：metrics 子键即指标
            for value in nested.values():
                total_count += 1
                if is_real_metric_value(value):
                    filled_count += 1
            continue
        # 旧扁平 schema
        total_count += 1
        if (
            str(item.get("status", "")).strip() not in ("to_be_filled", "", "draft_contract")
            and item.get("value") is not None
        ):
            filled_count += 1

    # 注意：调用方合并进全局 warnings 时统一加 "{qid}: " 前缀，消息本身不再自带
    if total_count == 0:
        warnings.append("metrics 条目既无 metrics 键也无 value 字段，为空转条目")
    elif filled_count == 0:
        warnings.append("所有指标均为占位值（to_be_filled/TBD/待补等），无真实计算结果")
    elif filled_count < total_count:
        warnings.append(f"仅 {filled_count}/{total_count} 个指标有真实值")

    return warnings


def has_bad_status(items: list[dict[str, Any]]) -> bool:
    for item in items:
        status = status_of(item)
        if status in BAD_STATUSES:
            return True
    return False


def conclusion_text_exists(items: list[dict[str, Any]]) -> bool:
    return any(str(item.get("conclusion_text") or "").strip() for item in items)


def task_items(data: Any) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    if not isinstance(data, list):
        return grouped
    for item in data:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("question_id") or "").strip()
        if qid:
            grouped.setdefault(qid, []).append(item)
    return grouped


def evaluate() -> dict[str, Any]:
    figure_index_path = first_existing(FIGURE_INDEX_CANDIDATES)
    table_index_path = first_existing(TABLE_INDEX_CANDIDATES)
    model_route = load_json(MODEL_ROUTE_FILE)
    figure_index = load_json(figure_index_path)
    model_results = load_json(MODEL_RESULTS_FILE)
    metrics = load_json(METRICS_FILE)
    conclusions = load_json(CONCLUSIONS_FILE)
    table_index = load_json(table_index_path)
    tasks = load_json(TASKS_FILE)

    failures: list[str] = []
    warnings: list[str] = []

    for path, data, candidates in (
        (MODEL_ROUTE_FILE, model_route, None),
        (figure_index_path, figure_index, FIGURE_INDEX_CANDIDATES),
        (MODEL_RESULTS_FILE, model_results, None),
        (METRICS_FILE, metrics, None),
        (CONCLUSIONS_FILE, conclusions, None),
        (table_index_path, table_index, TABLE_INDEX_CANDIDATES),
        (TASKS_FILE, tasks, None),
    ):
        if data is None:
            # P2-16：双候选索引缺失时把候选清单列进报错，与 completeness 口径互认
            if candidates:
                tried = " / ".join(
                    str(c.relative_to(BASE_DIR)) if c.is_relative_to(BASE_DIR) else str(c)
                    for c in candidates
                )
                failures.append(f"缺少证据门禁输入文件：{tried}（已查全部候选均不存在）")
            else:
                failures.append(
                    f"缺少证据门禁输入文件：{path.relative_to(BASE_DIR) if path.is_relative_to(BASE_DIR) else path}"
                )
        elif isinstance(data, dict) and data.get("__error__"):
            failures.append(f"无法读取证据门禁输入文件：{path} ({data['__error__']})")

    qids = question_ids(model_route)
    if not qids:
        failures.append("model_route.json 中没有可追溯的 question_id，无法执行正式证据门禁。")

    # ★ 新增：子问题覆盖检查
    result_map_for_coverage = result_items(model_results)
    for coverage_failure in check_question_coverage(model_route, result_map_for_coverage):
        failures.append(coverage_failure)

    result_map = result_items(model_results)
    metric_map = grouped_items(metrics, "items")
    conclusion_map = grouped_items(conclusions, "items")
    figure_map = figure_items(figure_index)
    table_map = table_items(table_index)
    task_map = task_items(tasks)

    # ★ CR-8：从"只读自报字段"改为"碰磁盘事实"（全局做一次，避免 ALL 条目按问重复）：
    # 1) figure/table 索引条目声明的文件必须在磁盘存在（自报 exists 字段不可信）；
    # 2) figures/ 实际图片清单与 figure_index.json 双向 diff；
    # 3) tasks.json 每条 artifact 验磁盘存在。
    figure_entries = figure_index.get("figures") if isinstance(figure_index, dict) else []
    figure_entries = figure_entries if isinstance(figure_entries, list) else []
    table_entries = table_index.get("tables") if isinstance(table_index, dict) else []
    table_entries = table_entries if isinstance(table_entries, list) else []

    fig_failures, fig_path_warnings = check_index_entries_disk(figure_entries, "figure")
    tbl_failures, tbl_path_warnings = check_index_entries_disk(table_entries, "table")
    failures.extend(fig_failures)
    failures.extend(tbl_failures)
    warnings.extend(fig_path_warnings)
    warnings.extend(tbl_path_warnings)
    warnings.extend(diff_figures_dir_vs_index(figure_entries))
    warnings.extend(check_task_artifacts(task_map))

    question_reports = []
    for qid in qids:
        q_failures: list[str] = []
        q_warnings: list[str] = []
        result = result_map.get(qid)
        q_metrics = metric_map.get(qid, [])
        q_conclusions = conclusion_map.get(qid, [])
        q_figures = figure_map.get(qid, [])
        q_tables = table_map.get(qid, []) + table_map.get("ALL", [])
        q_tasks = task_map.get(qid, [])

        if not result:
            q_failures.append("缺少 model_results.json 中的模型结果")
        elif status_of(result) in BAD_STATUSES:
            q_failures.append(f"模型结果状态仍不可作为正式证据：{status_of(result)}")
        else:
            for failure in provenance_failures(result):
                q_failures.append(f"模型结果缺少真实运行来源：{failure}")
            # ★ 新增：代码质量检查
            for code_warning in check_code_quality(result):
                q_warnings.append(code_warning)
            # ★ P2-13：源码 mtime 晚于产物的漂移检测（WARNING 级：如实分级，不 FAIL）
            for drift_warning in provenance_drift_warnings(result):
                q_warnings.append(drift_warning)

        if not q_metrics:
            q_failures.append("缺少 metrics.json 中的评价指标")
        elif has_bad_status(q_metrics):
            q_failures.append("评价指标仍包含草稿、模板或待补状态")
        # ★ 新增：指标丰富度检查
        for metric_warning in check_metric_richness(q_metrics, qid):
            q_warnings.append(metric_warning)

        if not q_conclusions or not conclusion_text_exists(q_conclusions):
            q_failures.append("缺少 conclusions.json 中可回扣原题的结论文本")
        elif has_bad_status(q_conclusions):
            q_failures.append("结论证据仍包含草稿、模板或待补状态")

        if not q_figures and not q_tables:
            q_failures.append("缺少图表或表格证据")
        if q_tables and has_bad_status(q_tables):
            q_failures.append("表格证据仍包含草稿、模板或待补状态")

        if not q_tasks:
            q_warnings.append("tasks.json 中没有对应问题任务，正式写作时需补齐任务追踪")

        # ★ CR-8：status_of 返回空串（status/evidence_status 字段缺失）按"未声明"处理并提示，
        # 不再当作正常放行（每问聚合成一条，避免逐条刷屏）。
        status_gap_sources: list[str] = []
        if result is not None and not status_of(result):
            status_gap_sources.append("model_results")
        if q_metrics and not any(status_of(m) for m in q_metrics):
            status_gap_sources.append("metrics")
        if q_conclusions and not any(status_of(m) for m in q_conclusions):
            status_gap_sources.append("conclusions")
        if q_tables and not any(status_of(t) for t in q_tables):
            status_gap_sources.append("tables")
        if status_gap_sources:
            # 注意：合并进全局 warnings 时会统一加 "{qid}: " 前缀，此处不再自带
            q_warnings.append(
                f"证据条目缺少 status/evidence_status 字段（按未声明处理，磁盘存在性已另行核验）："
                f"{', '.join(status_gap_sources)}"
            )

        for message in q_failures:
            failures.append(f"{qid}: {message}")
        for message in q_warnings:
            warnings.append(f"{qid}: {message}")

        question_reports.append(
            {
                "question_id": qid,
                "status": "FAIL" if q_failures else "PASS",
                "failures": q_failures,
                "warnings": q_warnings,
                "has_result": bool(result),
                "metric_count": len(q_metrics),
                "conclusion_count": len(q_conclusions),
                "figure_count": len(q_figures),
                "table_count": len(q_tables),
            }
        )

    return {
        "schema_version": "1.0",
        "generated_by": "quality-assurance-auditor/scripts/evidence_gate.py",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": warnings,
        "questions": question_reports,
    }


def write_reports(report: dict[str, Any], mode: str) -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Evidence Gate Report",
        "",
        f"- Mode: `{mode}`",
        f"- Status: `{report['status']}`",
        f"- Generated at: `{report['generated_at']}`",
        "",
    ]
    if report["failures"]:
        lines.append("## Failures")
        lines.extend(f"- {item}" for item in report["failures"])
        lines.append("")
    if report["warnings"]:
        lines.append("## Warnings")
        lines.extend(f"- {item}" for item in report["warnings"])
        lines.append("")
    lines.append("## Questions")
    for item in report["questions"]:
        lines.append(
            f"- {item['question_id']}: {item['status']} "
            f"(results={item['has_result']}, metrics={item['metric_count']}, "
            f"conclusions={item['conclusion_count']}, figures={item['figure_count']}, tables={item['table_count']})"
        )
    REPORT_MD.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def record_freshness(report_path: Path, sources: list[Path]) -> list[str]:
    """报告落盘后为其记录源哈希（P1-11 真接线，消灭 record 空转）。

    - 只绑定本门禁的核心依赖（索引/tasks/results 关键件），不绑定全量源；
    - 失败不 FAIL：freshness 记录是附加元数据，失败降级为报告内 warning 一行
      + stdout 提示，绝不改变门禁本身的 PASS/FAIL 判定（如实分级）；
    - 返回需并入报告 warnings 的降级消息（空列表 = 记录成功）。
    """
    existing = [s for s in sources if s.exists()]
    if not existing or not FRESHNESS_SCRIPT.exists():
        print("[fresh] 跳过 source_hash 记录（无已存在的依赖源或 freshness_check.py 不存在）")
        return []
    try:
        proc = subprocess.run(
            [sys.executable, str(FRESHNESS_SCRIPT), "record", str(report_path),
             "--sources", *[str(s) for s in existing]],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
        )
        if proc.returncode == 0:
            tail = (proc.stdout or "").strip().splitlines()
            msg = tail[-1].removeprefix("[fresh] ") if tail else "source_hash 已记录"
            print(f"[fresh] {msg}")
            return []
        lines = (proc.stderr or proc.stdout or "").strip().splitlines()
        reason = lines[-1] if lines else f"rc={proc.returncode}"
    except Exception as exc:  # noqa: BLE001 —— 记录失败必须降级，不得击穿门禁
        reason = str(exc)
    print(f"[fresh] ⚠ 记录哈希失败（不阻断门禁）：{reason}")
    return [f"freshness record 失败，本报告未绑定 source_hash：{reason}"]


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Check whether MathModel Skill evidence is ready for formal writing.")
    parser.add_argument(
        "--mode",
        choices=("official", "quickstart"),
        default=os.environ.get("MATHMODEL_EVIDENCE_GATE_MODE", "official"),
        help="official returns non-zero on missing evidence; quickstart only warns.",
    )
    parser.add_argument(
        "--paper-dir",
        default="paper_output",
        help="论文产物目录（相对当前工作目录或绝对路径；默认 paper_output，无参行为不变）",
    )
    args = parser.parse_args()

    reconfigure_paths(args.paper_dir)

    report = evaluate()
    write_reports(report, args.mode)

    # P1-11：报告落地即绑定源哈希——只绑本门禁的核心依赖（索引/tasks/results 关键件）；
    # record 失败降级为 warning，不改变门禁判定。
    downgrade = record_freshness(
        REPORT_JSON,
        [
            MODEL_ROUTE_FILE,
            first_existing(FIGURE_INDEX_CANDIDATES),
            MODEL_RESULTS_FILE,
            METRICS_FILE,
            CONCLUSIONS_FILE,
            first_existing(TABLE_INDEX_CANDIDATES),
            TASKS_FILE,
        ],
    )
    if downgrade:
        # record 可能已改写 JSON；重读追加 warning 后同步双写（JSON + MD）
        try:
            on_disk = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
            if isinstance(on_disk, dict):
                on_disk.setdefault("warnings", []).extend(downgrade)
                REPORT_JSON.write_text(json.dumps(on_disk, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
        try:
            with REPORT_MD.open("a", encoding="utf-8") as fh:
                fh.write("\n## Warnings (freshness record)\n\n")
                for message in downgrade:
                    fh.write(f"- {message}\n")
        except Exception:
            pass

    print(f"证据门禁报告：{REPORT_MD}")
    if report["status"] == "PASS":
        print("✅ 证据门禁通过，可以进入正式全局写作与最终 QA。")
        return 0

    print("⚠️ 证据门禁未通过。正式论文不得把当前 Word 称为最终稿。")
    for failure in report["failures"][:12]:
        print(f" - {failure}")
    if len(report["failures"]) > 12:
        print(f" - 其余 {len(report['failures']) - 12} 项见报告。")
    return 0 if args.mode == "quickstart" else 1


if __name__ == "__main__":
    raise SystemExit(main())
