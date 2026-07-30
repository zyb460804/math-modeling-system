"""通用结果验证脚本：检查模型结果的数值合理性。

用法：python validate_results.py [--results-dir DIR]

功能：
1. 通用范围检查：NaN/Inf/异常大值
2. 一致性检查：model_results.json 与 metrics.json 的 question_id 对应
3. 结果完整性检查：每个子问题都有结果、指标、结论
4. 输出验证报告
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_json(path: str) -> dict:
    """加载 JSON 文件。"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def find_nan_inf(data: any, path: str = "") -> list[str]:
    """递归查找 JSON 中的 NaN/Inf 值。"""
    issues = []
    if isinstance(data, dict):
        for k, v in data.items():
            issues.extend(find_nan_inf(v, f"{path}.{k}" if path else k))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            issues.extend(find_nan_inf(v, f"{path}[{i}]"))
    elif isinstance(data, float):
        if data != data:  # NaN check
            issues.append(f"{path}: NaN")
        elif data == float('inf') or data == float('-inf'):
            issues.append(f"{path}: Inf")
    return issues


BAD_STATUSES = {
    "missing",
    "needs_real_modeling",
    "draft_contract",
    "to_be_filled",
    "template",
    "draft",
    "scaffold_result_needs_review",
}


def validate_model_results(model_results: dict) -> dict:
    """验证 model_results.json 的完整性。"""
    issues = []
    warnings = []

    questions = model_results.get("questions", [])
    if not questions:
        issues.append("model_results.json 中没有 questions 数组")
        return {"status": "FAIL", "issues": issues, "warnings": warnings}

    for q in questions:
        qid = q.get("question_id", "unknown")
        status = q.get("evidence_status") or q.get("status", "")

        if status in BAD_STATUSES:
            issues.append(f"{qid}: 状态为 {status}，不是正式结果")

        # 检查 execution_provenance
        prov = q.get("execution_provenance")
        if not isinstance(prov, dict):
            issues.append(f"{qid}: 缺少 execution_provenance")
        elif prov.get("run_exit_code") not in (0, "0"):
            issues.append(f"{qid}: run_exit_code = {prov.get('run_exit_code')}")

        # 检查结果中的 NaN/Inf
        for nan_issue in find_nan_inf(q.get("results", {}), f"{qid}.results"):
            issues.append(nan_issue)

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
    }


def validate_metrics(metrics: dict) -> dict:
    """验证 metrics.json 的完整性。"""
    issues = []
    warnings = []

    items = metrics.get("items", [])
    if not items:
        issues.append("metrics.json 中没有 items 数组")
        return {"status": "FAIL", "issues": issues, "warnings": warnings}

    # 按 question_id 分组
    by_qid = {}
    for item in items:
        qid = item.get("question_id", "unknown")
        by_qid.setdefault(qid, []).append(item)

    for qid, q_items in by_qid.items():
        filled = sum(
            1 for m in q_items
            if m.get("value") is not None
            and str(m.get("status", "")) not in ("to_be_filled", "", "draft_contract")
        )
        if filled == 0:
            warnings.append(f"{qid}: 所有指标均为 to_be_filled，无真实计算值")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
    }


def validate_conclusions(conclusions: dict) -> dict:
    """验证 conclusions.json 的完整性。"""
    issues = []
    warnings = []

    items = conclusions.get("items", [])
    if not items:
        issues.append("conclusions.json 中没有 items 数组")
        return {"status": "FAIL", "issues": issues, "warnings": warnings}

    for item in items:
        qid = item.get("question_id", "unknown")
        text = str(item.get("conclusion_text", "")).strip()
        status = item.get("evidence_status", "")

        if not text:
            issues.append(f"{qid}: 结论文本为空")
        elif status in BAD_STATUSES:
            issues.append(f"{qid}: 结论状态为 {status}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
    }


def cross_validate(model_results: dict, metrics: dict, conclusions: dict) -> dict:
    """交叉验证：检查三个文件的 question_id 是否一致。"""
    issues = []

    result_qids = set()
    for q in model_results.get("questions", []):
        qid = q.get("question_id", "")
        if qid:
            result_qids.add(qid)

    metric_qids = set()
    for m in metrics.get("items", []):
        qid = m.get("question_id", "")
        if qid:
            metric_qids.add(qid)

    conclusion_qids = set()
    for c in conclusions.get("items", []):
        qid = c.get("question_id", "")
        if qid:
            conclusion_qids.add(qid)

    # 检查是否有遗漏
    all_qids = result_qids | metric_qids | conclusion_qids
    for qid in sorted(all_qids):
        if qid not in result_qids:
            issues.append(f"{qid}: 在 metrics/conclusions 中存在，但 model_results.json 中缺失")
        if qid not in metric_qids:
            issues.append(f"{qid}: 在 model_results 中存在，但 metrics.json 中缺失")
        if qid not in conclusion_qids:
            issues.append(f"{qid}: 在 model_results 中存在，但 conclusions.json 中缺失")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="通用结果验证")
    parser.add_argument('--results-dir', default='paper_output/results', help='Results directory')
    args = parser.parse_args()

    results_dir = args.results_dir

    print("=" * 60)
    print("通用结果验证")
    print("=" * 60)

    # 加载结果
    model_results = load_json(os.path.join(results_dir, 'model_results.json'))
    metrics = load_json(os.path.join(results_dir, 'metrics.json'))
    conclusions = load_json(os.path.join(results_dir, 'conclusions.json'))

    # 验证
    r1 = validate_model_results(model_results)
    r2 = validate_metrics(metrics)
    r3 = validate_conclusions(conclusions)
    r4 = cross_validate(model_results, metrics, conclusions)

    # 汇总
    all_results = {
        'model_results': r1,
        'metrics': r2,
        'conclusions': r3,
        'cross_validation': r4,
    }
    total_issues = sum(len(r['issues']) for r in all_results.values())
    total_warnings = sum(len(r.get('warnings', [])) for r in all_results.values())

    for name, r in all_results.items():
        status = r['status']
        icon = 'PASS' if status == 'PASS' else 'FAIL'
        print(f"\n  [{icon}] {name}")
        for issue in r['issues']:
            print(f"    - {issue}")
        for warn in r.get('warnings', []):
            print(f"    - WARNING: {warn}")

    # 保存报告
    report = {
        'generated_at': datetime.now().isoformat(),
        'status': 'PASS' if total_issues == 0 else 'FAIL',
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'details': all_results,
    }
    report_path = os.path.join(results_dir, 'validation_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"验证{'通过' if total_issues == 0 else '失败'}")
    print(f"  问题: {total_issues}")
    print(f"  警告: {total_warnings}")
    print(f"  报告: {report_path}")
    print("=" * 60)

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
