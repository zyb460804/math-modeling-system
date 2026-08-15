"""代码工厂：根据 problem_analysis.json 和 model_route.json 生成赛题专用代码。

用法：
    python code_factory.py                    # 生成所有子问题的代码
    python code_factory.py --question Q1      # 只生成 Q1 的代码
    python code_factory.py --stage data       # 只生成数据处理代码
    python code_factory.py --stage model      # 只生成建模代码
    python code_factory.py --stage plot       # 只生成图表代码

生成的代码写入 paper_output/code/ 对应子目录。

建模代码生成策略（v3.4 改进）：
    - 不再生成描述统计 stub
    - 委托给 result_contract_io.py 的算法选择器
    - 算法选择器从 algorithm_registry.json 匹配真实算法代码
    - 匹配失败时回退到 7 种脚手架
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def configure_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def get_project_root() -> Path:
    return Path.cwd().resolve()


def detect_data_files(root: Path) -> list[dict]:
    files = []
    for scan_dir in [root / "problem_files", root / "crawled_data"]:
        if not scan_dir.exists():
            continue
        for p in sorted(scan_dir.rglob("*")):
            if not p.is_file():
                continue
            ext = p.suffix.lower()
            if ext in {".csv", ".tsv", ".xlsx", ".xls", ".json"}:
                files.append({
                    "path": p.relative_to(root).as_posix(),
                    "name": p.name,
                    "ext": ext,
                    "size_kb": round(p.stat().st_size / 1024, 1),
                })
    return files


def generate_data_processing_code(question_id: str, question: dict, data_files: list[dict]) -> str:
    task_type = question.get("task_type", "unknown")
    model_name = question.get("recommended_model", "unknown")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    csv_files = [f for f in data_files if f["ext"] in {".csv", ".tsv"}]
    xlsx_files = [f for f in data_files if f["ext"] in {".xlsx", ".xls"}]

    lines = []
    lines.append('"""数据处理：' + question_id + ' - ' + task_type)
    lines.append('')
    lines.append('自动生成于 ' + ts)
    lines.append('任务类型：' + task_type)
    lines.append('推荐模型：' + model_name)
    lines.append('"""')
    lines.append('import sys')
    lines.append('import pandas as pd')
    lines.append('import numpy as np')
    lines.append('import os')
    lines.append('import json')
    lines.append('')
    lines.append('BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))')
    lines.append('PROBLEM_DIR = os.path.join(BASE_DIR, "problem_files")')
    lines.append('OUTPUT_DIR = os.path.join(BASE_DIR, "paper_output", "data_cleaned")')
    lines.append('os.makedirs(OUTPUT_DIR, exist_ok=True)')
    lines.append('')
    lines.append('')
    lines.append('def load_data():')
    lines.append('    """加载所有数据文件，返回字典。"""')
    lines.append('    data = {}')

    for i, f in enumerate(csv_files[:10]):
        var_name = f["name"].replace(".csv", "").replace(".tsv", "").replace(" ", "_")[:30]
        rel_path = f["path"]  # 包含子目录的相对路径，如 problem_files/A题/附件1.csv
        fname = f["name"]
        lines.append('')
        lines.append('    # ' + fname)
        lines.append('    try:')
        lines.append('        df_' + str(i) + ' = pd.read_csv(os.path.join(BASE_DIR, "' + rel_path + '"))')
        lines.append('        data["' + var_name + '"] = df_' + str(i))
        lines.append('        print(f"  加载 ' + fname + ': {len(df_' + str(i) + ')} 行, {len(df_' + str(i) + '.columns)} 列")')
        lines.append('    except Exception as e:')
        lines.append('        print(f"  警告: ' + fname + ' 加载失败: {e}")')

    for i, f in enumerate(xlsx_files[:10]):
        var_name = f["name"].replace(".xlsx", "").replace(".xls", "").replace(" ", "_")[:30]
        rel_path = f["path"]  # 包含子目录的相对路径
        fname = f["name"]
        lines.append('')
        lines.append('    # ' + fname)
        lines.append('    try:')
        lines.append('        df_x' + str(i) + ' = pd.read_excel(os.path.join(BASE_DIR, "' + rel_path + '"))')
        lines.append('        data["' + var_name + '"] = df_x' + str(i))
        lines.append('        print(f"  加载 ' + fname + ': {len(df_x' + str(i) + ')} 行, {len(df_x' + str(i) + '.columns)} 列")')
        lines.append('    except Exception as e:')
        lines.append('        print(f"  警告: ' + fname + ' 加载失败: {e}")')

    lines.append('')
    lines.append('    return data')
    lines.append('')
    lines.append('')
    lines.append('def clean_data(data):')
    lines.append('    """清洗数据：处理缺失值、异常值、类型转换。"""')
    lines.append('    cleaned = {}')
    lines.append('    for name, df in data.items():')
    lines.append('        if not isinstance(df, pd.DataFrame):')
    lines.append('            cleaned[name] = df')
    lines.append('            continue')
    lines.append('        df_clean = df.copy()')
    lines.append('        df_clean = df_clean.dropna(how="all", axis=0)')
    lines.append('        df_clean = df_clean.dropna(how="all", axis=1)')
    lines.append('        num_cols = df_clean.select_dtypes(include=[np.number]).columns')
    lines.append('        for col in num_cols:')
    lines.append('            if df_clean[col].isna().any():')
    lines.append('                df_clean[col] = df_clean[col].fillna(df_clean[col].median())')
    lines.append('        cat_cols = df_clean.select_dtypes(include=["object"]).columns')
    lines.append('        for col in cat_cols:')
    lines.append('            if df_clean[col].isna().any():')
    lines.append('                mode_val = df_clean[col].mode()')
    lines.append('                if len(mode_val) > 0:')
    lines.append('                    df_clean[col] = df_clean[col].fillna(mode_val[0])')
    lines.append('        cleaned[name] = df_clean')
    lines.append('        print(f"  清洗 {name}: {len(df)} -> {len(df_clean)} 行")')
    lines.append('    return cleaned')
    lines.append('')
    lines.append('')
    lines.append('def save_cleaned(cleaned):')
    lines.append('    """保存清洗后的数据。"""')
    lines.append('    for name, df in cleaned.items():')
    lines.append('        if isinstance(df, pd.DataFrame):')
    lines.append('            out_path = os.path.join(OUTPUT_DIR, f"{name}_cleaned.csv")')
    lines.append('            df.to_csv(out_path, index=False, encoding="utf-8-sig")')
    lines.append('            print(f"  保存: {out_path}")')
    lines.append('')
    lines.append('')
    lines.append('def main():')
    lines.append('    print("[' + question_id + '] 数据处理开始")')
    lines.append('    data = load_data()')
    lines.append('    if not data:')
    lines.append('        print("  错误: 未加载到任何数据")')
    lines.append('        return False')
    lines.append('    cleaned = clean_data(data)')
    lines.append('    save_cleaned(cleaned)')
    lines.append('    print("[' + question_id + '] 数据处理完成")')
    lines.append('    return True')
    lines.append('')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    success = main()')
    lines.append('    sys.exit(0 if success else 1)')

    return "\n".join(lines)


def generate_modeling_code(question_id: str, question: dict, data_files: list[dict]) -> str:
    """生成建模代码：委托给 result_contract_io.py 的算法选择器。

    不再生成描述统计 stub，而是调用 build_result_contracts.py 生成的
    result_contract_io.py 中的 run_question_scaffold()，该函数会：
    1. 从 algorithm_registry.json 匹配真实算法
    2. 运行真实算法代码
    3. 失败时回退到脚手架
    """
    task_type = question.get("task_type", "unknown")
    model_name = question.get("recommended_model") or question.get("main_model", "unknown")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    question_json = json.dumps(question, ensure_ascii=False, indent=2)

    lines = []
    lines.append(f'"""建模：{question_id} - {task_type}')
    lines.append(f'')
    lines.append(f'自动生成于 {ts}')
    lines.append(f'任务类型：{task_type}')
    lines.append(f'推荐模型：{model_name}')
    lines.append(f'')
    lines.append(f'本文件委托给 result_contract_io.py 的算法选择器执行。')
    lines.append(f'算法选择器会从 algorithm_registry.json 匹配真实算法代码，失败时回退到脚手架。')
    lines.append(f'"""')
    lines.append('import sys')
    lines.append('import os')
    lines.append('import json')
    lines.append('from pathlib import Path')
    lines.append('')
    lines.append('# 将建模代码目录加入 path，以便导入 result_contract_io')
    lines.append('THIS_DIR = Path(__file__).resolve().parent')
    lines.append('sys.path.insert(0, str(THIS_DIR))')
    lines.append('')
    lines.append('')
    lines.append('def main():')
    lines.append(f'    print("[{question_id}] 建模开始 (算法选择器模式)")')
    lines.append('')
    lines.append('    # 从 result_contract_io 导入算法选择器')
    lines.append('    try:')
    lines.append('        from result_contract_io import run_question_scaffold')
    lines.append('    except ImportError:')
    lines.append('        print("  错误: result_contract_io.py 不存在，请先运行 build_result_contracts.py")')
    lines.append('        print("  运行命令: python .claude/skills/model-code-and-result-generator/scripts/build_result_contracts.py"')
    lines.append('        return False')
    lines.append('')
    lines.append(f'    # 问题定义')
    lines.append(f'    QUESTION = {question_json}')
    lines.append('')
    lines.append('    # 运行算法选择器')
    lines.append('    exit_code = run_question_scaffold(QUESTION)')
    lines.append('')
    lines.append('    if exit_code == 0:')
    lines.append(f'        print("[{question_id}] 建模完成")')
    lines.append('    else:')
    lines.append(f'        print("[{question_id}] 建模失败 (exit={{exit_code}})")')
    lines.append('')
    lines.append('    return exit_code == 0')
    lines.append('')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    success = main()')
    lines.append('    sys.exit(0 if success else 1)')

    return "\n".join(lines)


def generate_plotting_code(question_id: str, question: dict) -> str:
    task_type = question.get("task_type", "unknown")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append('"""图表生成：' + question_id + ' - ' + task_type)
    lines.append('')
    lines.append('自动生成于 ' + ts)
    lines.append('任务类型：' + task_type)
    lines.append('"""')
    lines.append('import sys')
    lines.append('import pandas as pd')
    lines.append('import numpy as np')
    lines.append('import matplotlib')
    lines.append('matplotlib.use("Agg")')
    lines.append('import matplotlib.pyplot as plt')
    lines.append('import seaborn as sns')
    lines.append('import os')
    lines.append('import json')
    lines.append('')
    lines.append('BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))')
    lines.append('CLEANED_DIR = os.path.join(BASE_DIR, "paper_output", "data_cleaned")')
    lines.append('RESULTS_DIR = os.path.join(BASE_DIR, "paper_output", "results")')
    lines.append('FIGURES_DIR = os.path.join(BASE_DIR, "paper_output", "figures")')
    lines.append('os.makedirs(FIGURES_DIR, exist_ok=True)')
    lines.append('')
    lines.append('plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]')
    lines.append('plt.rcParams["axes.unicode_minus"] = False')
    lines.append('plt.rcParams["figure.dpi"] = 150')
    lines.append('plt.rcParams["savefig.bbox"] = "tight"')
    lines.append('')
    lines.append('')
    lines.append('def load_results():')
    lines.append('    """加载建模结果。"""')
    lines.append('    result_file = os.path.join(RESULTS_DIR, "' + question_id.lower() + '_results.json")')
    lines.append('    if os.path.exists(result_file):')
    lines.append('        with open(result_file, encoding="utf-8") as f:')
    lines.append('            return json.load(f)')
    lines.append('    return {}')
    lines.append('')
    lines.append('')
    lines.append('def load_cleaned_data():')
    lines.append('    """加载清洗后的数据。"""')
    lines.append('    data = {}')
    lines.append('    if os.path.exists(CLEANED_DIR):')
    lines.append('        for f in os.listdir(CLEANED_DIR):')
    lines.append('            if f.endswith(".csv"):')
    lines.append('                name = f.replace("_cleaned.csv", "")')
    lines.append('                data[name] = pd.read_csv(os.path.join(CLEANED_DIR, f))')
    lines.append('    return data')
    lines.append('')
    lines.append('')
    lines.append('def plot_data_distribution(data):')
    lines.append('    """绘制数据分布图。"""')
    lines.append('    for name, df in data.items():')
    lines.append('        if not isinstance(df, pd.DataFrame):')
    lines.append('            continue')
    lines.append('        num_cols = df.select_dtypes(include=[np.number]).columns[:6]')
    lines.append('        if len(num_cols) == 0:')
    lines.append('            continue')
    lines.append('        n = min(len(num_cols), 3)')
    lines.append('        fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))')
    lines.append('        if n == 1:')
    lines.append('            axes = [axes]')
    lines.append('        for i, col in enumerate(num_cols[:3]):')
    lines.append('            axes[i].hist(df[col].dropna(), bins=30, edgecolor="black", alpha=0.7)')
    lines.append('            axes[i].set_title(col)')
    lines.append('        plt.suptitle(f"{name} 数据分布")')
    lines.append('        out_path = os.path.join(FIGURES_DIR, "' + question_id.lower() + '_data_dist_{name}.png")')
    lines.append('        plt.savefig(out_path)')
    lines.append('        plt.close()')
    lines.append('        print(f"  保存图表: {out_path}")')
    lines.append('')
    lines.append('')
    lines.append('def plot_correlation_heatmap(data):')
    lines.append('    """绘制相关性热力图。"""')
    lines.append('    for name, df in data.items():')
    lines.append('        if not isinstance(df, pd.DataFrame):')
    lines.append('            continue')
    lines.append('        num_df = df.select_dtypes(include=[np.number])')
    lines.append('        if num_df.shape[1] < 2:')
    lines.append('            continue')
    lines.append('        corr = num_df.corr()')
    lines.append('        fig, ax = plt.subplots(figsize=(8, 6))')
    lines.append('        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)')
    lines.append('        ax.set_title(f"{name} 相关性矩阵")')
    lines.append('        out_path = os.path.join(FIGURES_DIR, "' + question_id.lower() + '_corr_{name}.png")')
    lines.append('        plt.savefig(out_path)')
    lines.append('        plt.close()')
    lines.append('        print(f"  保存图表: {out_path}")')
    lines.append('')
    lines.append('')
    lines.append('def main():')
    lines.append('    print("[' + question_id + '] 图表生成开始")')
    lines.append('    data = load_cleaned_data()')
    lines.append('    results = load_results()')
    lines.append('    if data:')
    lines.append('        plot_data_distribution(data)')
    lines.append('        plot_correlation_heatmap(data)')
    lines.append('    print("[' + question_id + '] 图表生成完成")')
    lines.append('    return True')
    lines.append('')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    success = main()')
    lines.append('    sys.exit(0 if success else 1)')

    return "\n".join(lines)


def main():
    configure_utf8()
    # 解析参数（v4.9.3 argparse 化：--help/-h 不再触发生成逻辑；接口与原手写解析兼容）
    parser = argparse.ArgumentParser(description="代码工厂：根据 problem_analysis.json 和 model_route.json 生成赛题专用代码")
    parser.add_argument("--question", default=None, help="只生成指定子问题（如 Q1）的代码")
    parser.add_argument("--stage", default=None, help="只生成指定阶段（data / model / plot）代码")
    args = parser.parse_args()
    target_question = args.question
    target_stage = args.stage

    root = get_project_root()

    analysis = load_json(root / "paper_output" / "step1" / "problem_analysis.json")
    if not analysis:
        print("[ERROR] 未找到 problem_analysis.json，请先运行 problem-doc-model-selector")
        return 1

    route = load_json(root / "paper_output" / "plan" / "model_route.json")
    route_questions = {}
    if route and "questions" in route:
        for q in route["questions"]:
            route_questions[q.get("question_id", "")] = q

    data_files = detect_data_files(root)
    print("数据文件: {} 个".format(len(data_files)))

    questions = analysis.get("questions", [])
    if not questions:
        print("[ERROR] problem_analysis.json 中没有子问题")
        return 1

    code_dir = root / "paper_output" / "code"
    generated = 0

    for q in questions:
        qid = q.get("question_id", "Q{}".format(generated + 1))
        if target_question and qid != target_question:
            continue

        if qid in route_questions:
            q.update(route_questions[qid])

        print("\n" + "=" * 50)
        print("生成 {} 代码...".format(qid))

        if not target_stage or target_stage == "data":
            dp_dir = code_dir / "data_processing"
            dp_dir.mkdir(parents=True, exist_ok=True)
            dp_code = generate_data_processing_code(qid, q, data_files)
            dp_file = dp_dir / "{}_clean.py".format(qid.lower())
            dp_file.write_text(dp_code, encoding="utf-8")
            print("  数据处理: {}".format(dp_file.relative_to(root)))

        if not target_stage or target_stage == "model":
            md_dir = code_dir / "modeling"
            md_dir.mkdir(parents=True, exist_ok=True)
            md_code = generate_modeling_code(qid, q, data_files)
            md_file = md_dir / "{}_model.py".format(qid.lower())
            md_file.write_text(md_code, encoding="utf-8")
            print("  建模代码: {}".format(md_file.relative_to(root)))

        if not target_stage or target_stage == "plot":
            vz_dir = code_dir / "visualization"
            vz_dir.mkdir(parents=True, exist_ok=True)
            vz_code = generate_plotting_code(qid, q)
            vz_file = vz_dir / "{}_plot.py".format(qid.lower())
            vz_file.write_text(vz_code, encoding="utf-8")
            print("  图表代码: {}".format(vz_file.relative_to(root)))

        generated += 1

    print("\n" + "=" * 50)
    print("共生成 {} 个子问题的代码".format(generated))
    print("代码位置: paper_output/code/")
    print("\n下一步: python .claude/skills/paper-workflow-orchestrator/scripts/run_and_verify.py")

    # v4.1: advisory feedback-layer hook（L1 代码机械检查；永不破坏流水线）
    try:
        import subprocess as _sp, sys as _sys
        _fl = Path(__file__).resolve().parents[2] / "quality-assurance-auditor" / "scripts" / "run_feedback_layers.py"
        if _fl.exists():
            _sp.run([_sys.executable, str(_fl), "--stage", "code"],
                    capture_output=True, text=True, timeout=120, cwd=str(root))
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
