#!/usr/bin/env python3
"""
PoC验证脚本

验证候选方法的PoC代码是否能在真实数据上运行并产出具体结果。

用法：
    python poc_validator.py --question Q1 --method method_name
    python poc_validator.py --question Q1 --validate-all
    python poc_validator.py --archive-rejected --question Q1 --method method_name --reason "..."
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 配置 UTF-8 输出
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 路径配置
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "paper_output"
METHODS_DIR = OUTPUT_DIR / "methods"
ARCHIVED_DIR = OUTPUT_DIR / "archived"
DATA_DIR = OUTPUT_DIR / "data_cleaned"


def find_poc_file(question_id: str, method_name: str) -> Path:
    """查找PoC文件"""
    poc_dir = METHODS_DIR / question_id / "poc"
    poc_file = poc_dir / f"{method_name}_poc.py"

    if poc_file.exists():
        return poc_file

    # 尝试其他可能的命名
    patterns = [
        f"{method_name}_poc.py",
        f"{method_name.lower()}_poc.py",
        f"poc_{method_name}.py",
        f"{method_name}.py",
    ]

    for pattern in patterns:
        if (poc_dir / pattern).exists():
            return poc_dir / pattern

    return None


def validate_poc(poc_file: Path, timeout: int = 60) -> dict:
    """验证PoC代码"""
    result = {
        "file": str(poc_file),
        "exists": poc_file.exists(),
        "runnable": False,
        "has_output": False,
        "uses_real_data": False,
        "line_count": 0,
        "metrics": {},
        "error": None,
        "stdout": "",
        "stderr": ""
    }

    if not result["exists"]:
        result["error"] = "PoC文件不存在"
        return result

    # 检查代码行数
    content = poc_file.read_text(encoding="utf-8")
    lines = [l for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]
    result["line_count"] = len(lines)

    # 检查是否使用真实数据
    if "data_cleaned" in content or "cleaned_data" in content:
        result["uses_real_data"] = True

    # 运行PoC
    try:
        proc = subprocess.run(
            [sys.executable, str(poc_file)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR)
        )

        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        result["returncode"] = proc.returncode

        if proc.returncode == 0:
            result["runnable"] = True

            # 检查是否有具体输出
            if proc.stdout.strip():
                result["has_output"] = True

                # 尝试提取指标
                metrics = extract_metrics(proc.stdout)
                if metrics:
                    result["metrics"] = metrics

        else:
            result["error"] = f"运行失败，退出码: {proc.returncode}"

    except subprocess.TimeoutExpired:
        result["error"] = f"运行超时（{timeout}秒）"
    except Exception as e:
        result["error"] = f"运行异常: {str(e)}"

    return result


def extract_metrics(output: str) -> dict:
    """从输出中提取指标"""
    metrics = {}

    # 尝试解析JSON输出
    try:
        # 查找JSON格式的输出
        lines = output.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                data = json.loads(line)
                if "metrics" in data:
                    return data["metrics"]
                if "result" in data:
                    return {"result": data["result"]}
    except:
        pass

    # 尝试提取 key=value 格式
    import re
    patterns = [
        r'(\w+)\s*[=:]\s*([\d.]+)',
        r'指标[：:]\s*(\w+)\s*[=:]\s*([\d.]+)',
        r'结果[：:]\s*(\w+)\s*[=:]\s*([\d.]+)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, output)
        for key, value in matches:
            try:
                metrics[key] = float(value)
            except:
                pass

    return metrics


def validate_all_pocs(question_id: str) -> dict:
    """验证某个子问题的所有PoC"""
    poc_dir = METHODS_DIR / question_id / "poc"

    if not poc_dir.exists():
        return {
            "question": question_id,
            "error": "poc目录不存在",
            "results": {}
        }

    results = {}
    poc_files = list(poc_dir.glob("*_poc.py"))

    if not poc_files:
        return {
            "question": question_id,
            "error": "未找到PoC文件",
            "results": {}
        }

    for poc_file in poc_files:
        method_name = poc_file.stem.replace("_poc", "")
        print(f"\n验证 {method_name}...")
        results[method_name] = validate_poc(poc_file)

        # 输出结果
        status = "✅ PASS" if results[method_name]["runnable"] else "❌ FAIL"
        print(f"  状态: {status}")

        if results[method_name]["metrics"]:
            print(f"  指标: {results[method_name]['metrics']}")

        if results[method_name]["error"]:
            print(f"  错误: {results[method_name]['error']}")

    return {
        "question": question_id,
        "total": len(poc_files),
        "passed": sum(1 for r in results.values() if r["runnable"]),
        "failed": sum(1 for r in results.values() if not r["runnable"]),
        "results": results
    }


def archive_rejected_method(question_id: str, method_name: str, reason: str):
    """将淘汰方法归档"""
    src_dir = METHODS_DIR / question_id / method_name
    dst_dir = ARCHIVED_DIR / question_id / f"{method_name}_REJECTED"

    # 创建归档目录
    dst_dir.mkdir(parents=True, exist_ok=True)

    # 移动PoC文件
    poc_src = METHODS_DIR / question_id / "poc" / f"{method_name}_poc.py"
    poc_dst = dst_dir / f"{method_name}_poc.py"

    if poc_src.exists():
        shutil.copy2(poc_src, poc_dst)
        print(f"✅ PoC文件已归档: {poc_dst}")

    # 移动PoC结果
    result_src = METHODS_DIR / question_id / "poc" / f"{method_name}_poc_result.json"
    result_dst = dst_dir / f"{method_name}_poc_result.json"

    if result_src.exists():
        shutil.copy2(result_src, result_dst)
        print(f"✅ PoC结果已归档: {result_dst}")

    # 记录归档原因
    reason_file = dst_dir / "rejection_reason.md"
    reason_file.write_text(f"""# 方法淘汰记录

**方法**: {method_name}
**子问题**: {question_id}
**淘汰时间**: {datetime.now().isoformat()}
**淘汰原因**: {reason}

## PoC验证结果

详见 `{method_name}_poc_result.json`
""", encoding="utf-8")

    print(f"✅ 淘汰记录已保存: {reason_file}")

    # 如果有方法目录，也归档
    if src_dir.exists():
        for item in src_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dst_dir / item.name)
        print(f"✅ 方法文件已归档: {dst_dir}")

    return dst_dir


def generate_report(validation_results: dict, output_path: Path):
    """生成验证报告"""
    question = validation_results.get("question", "Unknown")
    total = validation_results.get("total", 0)
    passed = validation_results.get("passed", 0)
    failed = validation_results.get("failed", 0)
    results = validation_results.get("results", {})

    report = f"""# PoC验证报告

**子问题**: {question}
**验证时间**: {datetime.now().isoformat()}
**总计**: {total}个方法
**通过**: {passed}个
**失败**: {failed}个

## 验证结果

| 方法 | 状态 | 可运行 | 有输出 | 使用真实数据 | 代码行数 | 指标 |
|------|------|--------|--------|-------------|---------|------|
"""

    for method_name, result in results.items():
        status = "✅ PASS" if result["runnable"] else "❌ FAIL"
        runnable = "✅" if result["runnable"] else "❌"
        has_output = "✅" if result["has_output"] else "❌"
        uses_real = "✅" if result["uses_real_data"] else "❌"
        lines = result["line_count"]
        metrics = str(result.get("metrics", {}))[:30]

        report += f"| {method_name} | {status} | {runnable} | {has_output} | {uses_real} | {lines} | {metrics} |\n"

    report += """
## 详细结果

"""

    for method_name, result in results.items():
        status = "✅ PASS" if result["runnable"] else "❌ FAIL"
        report += f"### {method_name} [{status}]\n\n"

        if result["metrics"]:
            report += f"**指标**: {result['metrics']}\n\n"

        if result["error"]:
            report += f"**错误**: {result['error']}\n\n"

        if result["stdout"]:
            report += f"**标准输出**:\n```\n{result['stdout'][:500]}\n```\n\n"

        if result["stderr"]:
            report += f"**错误输出**:\n```\n{result['stderr'][:500]}\n```\n\n"

    # 保存报告
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"\n报告已保存: {output_path}")

    # 保存JSON
    json_path = output_path.with_suffix(".json")
    json_path.write_text(json.dumps(validation_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON已保存: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="PoC验证脚本")

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 验证单个PoC
    validate_parser = subparsers.add_parser("validate", help="验证单个PoC")
    validate_parser.add_argument("--question", type=str, required=True, help="子问题（如Q1）")
    validate_parser.add_argument("--method", type=str, required=True, help="方法名")
    validate_parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")

    # 验证所有PoC
    validate_all_parser = subparsers.add_parser("validate-all", help="验证所有PoC")
    validate_all_parser.add_argument("--question", type=str, required=True, help="子问题（如Q1）")
    validate_all_parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")

    # 归档淘汰方法
    archive_parser = subparsers.add_parser("archive", help="归档淘汰方法")
    archive_parser.add_argument("--question", type=str, required=True, help="子问题（如Q1）")
    archive_parser.add_argument("--method", type=str, required=True, help="方法名")
    archive_parser.add_argument("--reason", type=str, required=True, help="淘汰原因")

    args = parser.parse_args()

    if args.command == "validate":
        poc_file = find_poc_file(args.question, args.method)
        if not poc_file:
            print(f"❌ 未找到 {args.method} 的PoC文件")
            sys.exit(1)

        result = validate_poc(poc_file, args.timeout)
        status = "✅ PASS" if result["runnable"] else "❌ FAIL"
        print(f"\n{status} {args.method}")
        print(f"指标: {result['metrics']}")

        if result["error"]:
            print(f"错误: {result['error']}")

        sys.exit(0 if result["runnable"] else 1)

    elif args.command == "validate-all":
        results = validate_all_pocs(args.question)

        # 生成报告
        report_path = METHODS_DIR / args.question / "poc_validation_report.md"
        generate_report(results, report_path)

        print(f"\n总计: {results['total']}")
        print(f"通过: {results['passed']}")
        print(f"失败: {results['failed']}")

        sys.exit(0 if results["failed"] == 0 else 1)

    elif args.command == "archive":
        archive_rejected_method(args.question, args.method, args.reason)
        print(f"\n✅ 方法 {args.method} 已归档")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()