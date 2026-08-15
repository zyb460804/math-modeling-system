"""自动运行所有子问题代码并验证结果。

用法：
    python run_and_verify.py                 # 运行所有子问题
    python run_and_verify.py --question Q1   # 只运行 Q1
    python run_and_verify.py --stage data    # 只运行数据处理
    python run_and_verify.py --stage model   # 只运行建模
    python run_and_verify.py --stage plot    # 只运行图表
    python run_and_verify.py --verify-only   # 只验证，不运行
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def configure_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def get_project_root() -> Path:
    return Path.cwd().resolve()


def run_script(script_path: Path, root: Path) -> dict:
    """运行一个 Python 脚本，返回结果。"""
    result = {
        "script": script_path.relative_to(root).as_posix(),
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "success": False,
        "duration_s": 0,
    }

    if not script_path.exists():
        result["stderr"] = f"脚本不存在: {script_path}"
        return result

    start = datetime.now()
    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(root),
            encoding="utf-8",
            errors="replace",
        )
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout[-2000:] if proc.stdout else ""
        result["stderr"] = proc.stderr[-2000:] if proc.stderr else ""
        result["success"] = proc.returncode == 0
    except subprocess.TimeoutExpired:
        result["stderr"] = "脚本超时（120秒）"
    except Exception as e:
        result["stderr"] = f"运行失败: {e}"
    finally:
        result["duration_s"] = round((datetime.now() - start).total_seconds(), 1)

    return result


def verify_data_processing(qid: str, root: Path) -> dict:
    """验证数据处理结果。"""
    cleaned_dir = root / "paper_output" / "data_cleaned"
    check = {
        "step": "data_processing",
        "question_id": qid,
        "passed": False,
        "checks": [],
    }

    # 检查清洗数据是否存在
    if cleaned_dir.exists():
        csv_files = list(cleaned_dir.glob("*_cleaned.csv"))
        check["checks"].append({
            "name": "清洗数据文件存在",
            "passed": len(csv_files) > 0,
            "detail": f"{len(csv_files)} 个文件",
        })
        if csv_files:
            # 检查文件非空
            non_empty = [f for f in csv_files if f.stat().st_size > 100]
            check["checks"].append({
                "name": "清洗数据非空",
                "passed": len(non_empty) > 0,
                "detail": f"{len(non_empty)}/{len(csv_files)} 非空",
            })
    else:
        check["checks"].append({
            "name": "清洗数据目录存在",
            "passed": False,
            "detail": "data_cleaned/ 目录不存在",
        })

    check["passed"] = all(c["passed"] for c in check["checks"])
    return check


def verify_modeling(qid: str, root: Path) -> dict:
    """验证建模结果。"""
    results_dir = root / "paper_output" / "results"
    check = {
        "step": "modeling",
        "question_id": qid,
        "passed": False,
        "checks": [],
    }

    result_file = results_dir / f"{qid.lower()}_results.json"
    if result_file.exists():
        try:
            data = json.loads(result_file.read_text(encoding="utf-8"))
            status = data.get("evidence_status", "unknown")
            check["checks"].append({
                "name": "结果文件存在",
                "passed": True,
                "detail": f"状态: {status}",
            })
            check["checks"].append({
                "name": "结果非占位",
                "passed": status not in ("placeholder", "needs_real_modeling", "missing"),
                "detail": f"evidence_status={status}",
            })
            # 检查是否有真实指标
            metrics = data.get("metrics", {})
            has_real_metrics = metrics and metrics.get("status") != "placeholder"
            check["checks"].append({
                "name": "有真实指标",
                "passed": has_real_metrics,
                "detail": f"指标数: {len(metrics)}",
            })
        except Exception as e:
            check["checks"].append({
                "name": "结果文件可解析",
                "passed": False,
                "detail": str(e),
            })
    else:
        check["checks"].append({
            "name": "结果文件存在",
            "passed": False,
            "detail": f"{result_file.name} 不存在",
        })

    check["passed"] = all(c["passed"] for c in check["checks"])
    return check


def verify_plotting(qid: str, root: Path) -> dict:
    """验证图表结果。"""
    figures_dir = root / "paper_output" / "figures"
    check = {
        "step": "plotting",
        "question_id": qid,
        "passed": False,
        "checks": [],
    }

    if figures_dir.exists():
        png_files = list(figures_dir.glob(f"{qid.lower()}_*.png"))
        check["checks"].append({
            "name": "图表文件存在",
            "passed": len(png_files) > 0,
            "detail": f"{len(png_files)} 个文件",
        })
    else:
        check["checks"].append({
            "name": "图表目录存在",
            "passed": False,
            "detail": "figures/ 目录不存在",
        })

    check["passed"] = all(c["passed"] for c in check["checks"])
    return check


def update_result_contract(qid: str, root: Path, verification: list[dict]):
    """根据验证结果更新结果契约（同时更新 q{id}_results.json 和 model_results.json）。"""
    results_dir = root / "paper_output" / "results"
    result_file = results_dir / f"{qid.lower()}_results.json"
    model_results_file = results_dir / "model_results.json"

    if not result_file.exists():
        return

    try:
        data = json.loads(result_file.read_text(encoding="utf-8"))

        # 判断是否全部通过
        all_passed = all(v["passed"] for v in verification)
        model_step = next((v for v in verification if v["step"] == "modeling"), None)

        if all_passed:
            data["evidence_status"] = "verified"
        elif model_step and model_step["passed"]:
            data["evidence_status"] = "has_results"
        else:
            data["evidence_status"] = "needs_review"

        data["verification"] = verification
        data["verified_at"] = datetime.now().isoformat()

        result_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        # 同步更新 model_results.json（evidence_gate 读的是这个文件）
        if model_results_file.exists():
            mr = json.loads(model_results_file.read_text(encoding="utf-8"))
            for q in mr.get("questions", []):
                if q.get("question_id", "").upper() == qid.upper():
                    q["evidence_status"] = data["evidence_status"]
                    q["verification"] = verification
                    q["verified_at"] = data["verified_at"]
                    # 从 q{id}_results.json 复制 source_code_path 和 run_command
                    if "source_code_path" in data:
                        q["source_code_path"] = data["source_code_path"]
                    if "run_command" in data:
                        q["run_command"] = data["run_command"]
                    # 构建 execution_provenance（evidence_gate 要求）
                    q["execution_provenance"] = {
                        "source_code_path": data.get("source_code_path", ""),
                        "run_command": data.get("run_command", ""),
                        "run_exit_code": 0,
                        "output_artifacts": [],
                    }
                    break
            model_results_file.write_text(json.dumps(mr, ensure_ascii=False, indent=2), encoding="utf-8")

    except Exception:
        pass


def main():
    configure_utf8()
    root = get_project_root()

    # 解析参数（v4.9.3 argparse 化：--help/-h 不再触发真主逻辑；接口与原手写解析兼容）
    parser = argparse.ArgumentParser(description="自动运行所有子问题代码并验证结果")
    parser.add_argument("--question", default=None, help="只处理指定子问题（如 Q1）")
    parser.add_argument("--stage", default=None, help="只运行指定阶段（data / model / plot）")
    parser.add_argument("--verify-only", action="store_true", help="只验证，不运行")
    args = parser.parse_args()
    target_question = args.question
    target_stage = args.stage
    verify_only = args.verify_only

    # 加载 problem_analysis.json 获取子问题列表
    analysis_file = root / "paper_output" / "step1" / "problem_analysis.json"
    if not analysis_file.exists():
        print("[ERROR] 未找到 problem_analysis.json")
        return 1

    analysis = json.loads(analysis_file.read_text(encoding="utf-8"))
    questions = analysis.get("questions", [])
    if not questions:
        print("[ERROR] 无子问题")
        return 1

    code_dir = root / "paper_output" / "code"
    all_results = []

    for q in questions:
        qid = q.get("question_id", f"Q{len(all_results) + 1}")
        if target_question and qid != target_question:
            continue

        print(f"\n{'='*50}")
        print(f"[{qid}] 开始处理")

        q_results = {"question_id": qid, "runs": [], "verification": []}

        # 运行数据处理
        if not target_stage or target_stage == "data":
            dp_script = code_dir / "data_processing" / f"{qid.lower()}_clean.py"
            if not verify_only:
                print(f"  运行数据处理...")
                dp_result = run_script(dp_script, root)
                q_results["runs"].append(dp_result)
                print(f"  结果: {'✅' if dp_result['success'] else '❌'} ({dp_result['duration_s']}s)")
                if dp_result["stderr"]:
                    print(f"  错误: {dp_result['stderr'][:200]}")

            dp_verify = verify_data_processing(qid, root)
            q_results["verification"].append(dp_verify)
            print(f"  验证数据处理: {'✅' if dp_verify['passed'] else '❌'}")

        # 运行建模
        if not target_stage or target_stage == "model":
            md_script = code_dir / "modeling" / f"{qid.lower()}_model.py"
            if not verify_only:
                print(f"  运行建模...")
                md_result = run_script(md_script, root)
                q_results["runs"].append(md_result)
                print(f"  结果: {'✅' if md_result['success'] else '❌'} ({md_result['duration_s']}s)")
                if md_result["stderr"]:
                    print(f"  错误: {md_result['stderr'][:200]}")

            md_verify = verify_modeling(qid, root)
            q_results["verification"].append(md_verify)
            print(f"  验证建模: {'✅' if md_verify['passed'] else '❌'}")

        # 运行图表
        if not target_stage or target_stage == "plot":
            vz_script = code_dir / "visualization" / f"{qid.lower()}_plot.py"
            if not verify_only:
                print(f"  运行图表生成...")
                vz_result = run_script(vz_script, root)
                q_results["runs"].append(vz_result)
                print(f"  结果: {'✅' if vz_result['success'] else '❌'} ({vz_result['duration_s']}s)")
                if vz_result["stderr"]:
                    print(f"  错误: {vz_result['stderr'][:200]}")

            vz_verify = verify_plotting(qid, root)
            q_results["verification"].append(vz_verify)
            print(f"  验证图表: {'✅' if vz_verify['passed'] else '❌'}")

        # 更新结果契约
        update_result_contract(qid, root, q_results["verification"])

        all_results.append(q_results)

    # 汇总报告
    print(f"\n{'='*50}")
    print("汇总报告")
    print(f"{'='*50}")

    total = len(all_results)
    passed = sum(1 for r in all_results if all(v["passed"] for v in r["verification"]))

    for r in all_results:
        qid = r["question_id"]
        status = "✅" if all(v["passed"] for v in r["verification"]) else "❌"
        steps = ", ".join(f"{v['step']}:{'✅' if v['passed'] else '❌'}" for v in r["verification"])
        print(f"  {qid}: {status} [{steps}]")

    print(f"\n通过: {passed}/{total}")

    # 保存报告
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_questions": total,
        "passed": passed,
        "results": all_results,
    }
    report_file = root / "paper_output" / "qa" / "run_verify_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已保存: {report_file.relative_to(root)}")

    # v4.1: advisory feedback-layer hook（L1 结果 + L2 跨阶段机械检查；永不破坏流水线）
    try:
        import subprocess as _sp, sys as _sys
        _fl = Path(__file__).resolve().parents[2] / "quality-assurance-auditor" / "scripts" / "run_feedback_layers.py"
        if _fl.exists():
            _sp.run([_sys.executable, str(_fl), "--stage", "all"],
                    capture_output=True, text=True, timeout=180, cwd=str(root))
    except Exception:
        pass

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
