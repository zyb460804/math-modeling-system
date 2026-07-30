#!/usr/bin/env python3
"""
证据自动补齐器
检测缺失证据 → 自动生成占位证据 → 标记为 needs_review

用法:
    python evidence_auto_filler.py --errors path/to/errors.json
    python evidence_auto_filler.py --check-all
"""

import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[5]
PAPER_OUTPUT = ROOT / "paper_output"
RESULTS_DIR = PAPER_OUTPUT / "results"
FIGURES_DIR = PAPER_OUTPUT / "figures"
TABLES_DIR = PAPER_OUTPUT / "tables"
CODE_DIR = PAPER_OUTPUT / "code"

# 必须存在的证据文件
REQUIRED_EVIDENCE = {
    "model_results.json": {
        "dir": RESULTS_DIR,
        "description": "模型结果",
        "template": {
            "questions": [],
            "generated_at": datetime.now().isoformat(),
            "status": "needs_review",
        },
    },
    "metrics.json": {
        "dir": RESULTS_DIR,
        "description": "评价指标",
        "template": {
            "metrics": {},
            "generated_at": datetime.now().isoformat(),
            "status": "needs_review",
        },
    },
    "conclusions.json": {
        "dir": RESULTS_DIR,
        "description": "结构化结论",
        "template": {
            "conclusions": [],
            "generated_at": datetime.now().isoformat(),
            "status": "needs_review",
        },
    },
    "figure_index.json": {
        "dir": PAPER_OUTPUT,
        "description": "图表索引",
        "template": {
            "figures": [],
            "generated_at": datetime.now().isoformat(),
            "status": "needs_review",
        },
    },
    "table_index.json": {
        "dir": TABLES_DIR,
        "description": "表格索引",
        "template": {
            "tables": [],
            "generated_at": datetime.now().isoformat(),
            "status": "needs_review",
        },
    },
    "frozen_numbers.json": {
        "dir": PAPER_OUTPUT,
        "description": "冻结数字",
        "template": {
            "frozen_at": datetime.now().isoformat(),
            "frozen_by_skill": "auto_corrector",
            "numbers": [],
            "status": "needs_review",
        },
    },
}

# 必须存在的目录结构
REQUIRED_DIRS = [
    CODE_DIR / "data_processing",
    CODE_DIR / "modeling",
    CODE_DIR / "visualization",
    CODE_DIR / "qa",
    RESULTS_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    PAPER_OUTPUT / "step1",
    PAPER_OUTPUT / "plan",
]


def check_missing_evidence() -> list:
    """检查缺失的证据文件"""
    missing = []

    # 检查目录
    for dir_path in REQUIRED_DIRS:
        if not dir_path.exists():
            missing.append({
                "type": "directory",
                "path": str(dir_path),
                "description": f"缺失目录: {dir_path.relative_to(ROOT)}",
            })

    # 检查文件
    for filename, config in REQUIRED_EVIDENCE.items():
        file_path = config["dir"] / filename
        if not file_path.exists():
            missing.append({
                "type": "file",
                "path": str(file_path),
                "description": f"缺失文件: {config['description']}",
                "template": config["template"],
            })

    return missing


def create_missing_evidence(missing: list) -> int:
    """创建缺失的证据文件"""
    created = 0

    for item in missing:
        path = Path(item["path"])

        if item["type"] == "directory":
            path.mkdir(parents=True, exist_ok=True)
            # 创建 README
            readme_path = path / "README.md"
            if not readme_path.exists():
                readme_path.write_text(
                    f"# {path.name}\n\n自动生成于 {datetime.now().isoformat()}\n\n状态: needs_review\n",
                    encoding="utf-8",
                )
            print(f"    [OK] 创建目录: {path.relative_to(ROOT)}")
            created += 1

        elif item["type"] == "file":
            path.parent.mkdir(parents=True, exist_ok=True)
            template = item.get("template", {})
            path.write_text(
                json.dumps(template, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"    [OK] 创建文件: {path.relative_to(ROOT)} (needs_review)")
            created += 1

    return created


def check_problem_analysis() -> bool:
    """检查 problem_analysis.json 是否存在"""
    pa_file = PAPER_OUTPUT / "step1" / "problem_analysis.json"
    if not pa_file.exists():
        print("    [!] 缺失 problem_analysis.json，需要先运行审题")
        return False
    return True


def check_model_route() -> bool:
    """检查 model_route.json 是否存在"""
    mr_file = PAPER_OUTPUT / "plan" / "model_route.json"
    if not mr_file.exists():
        print("    [!] 缺失 model_route.json，需要先运行选模")
        return False
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="证据自动补齐器")
    parser.add_argument("--errors", help="错误信息 JSON 文件路径")
    parser.add_argument("--check-all", action="store_true", help="检查并补齐所有缺失证据")
    args = parser.parse_args()

    print("[*] 证据完整性检查")

    # 检查缺失
    missing = check_missing_evidence()

    if not missing:
        print("[OK] 所有必需证据文件存在")
        sys.exit(0)

    print(f"\n发现 {len(missing)} 项缺失:")
    for item in missing:
        print(f"  - {item['description']}")

    if args.check_all or args.errors:
        # 自动补齐
        print(f"\n[#] 自动补齐...")
        created = create_missing_evidence(missing)
        print(f"\n[OK] 已创建 {created} 项（标记为 needs_review）")

        # 检查前置依赖
        check_problem_analysis()
        check_model_route()

        print("\n[!] 自动生成的文件标记为 needs_review，需要后续 Agent 填充真实内容")
        sys.exit(0)
    else:
        print("\n使用 --check-all 自动补齐")
        sys.exit(1)


if __name__ == "__main__":
    main()