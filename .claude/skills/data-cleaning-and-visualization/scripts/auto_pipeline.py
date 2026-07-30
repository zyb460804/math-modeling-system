"""自动数据处理流水线：从 problem_files/ 读取 Excel，清洗后输出到 paper_output/。

用法：python auto_pipeline.py [--problem-dir DIR] [--output-dir DIR]

功能：
1. 扫描 problem_files/ 下所有 Excel/CSV 文件
2. 自动识别数据类型（时序/截面/面板）
3. 清洗：缺失值处理、异常值检测、单位统一
4. 特征工程：标幺化、差分、滚动统计
5. 输出：clean_data.csv + data_summary.json + data_quality_report.md
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def find_data_files(problem_dir: str) -> list[dict]:
    """扫描目录下所有数据文件。"""
    files = []
    for root, _, filenames in os.walk(problem_dir):
        for f in filenames:
            ext = f.lower().split('.')[-1]
            if ext in ('xlsx', 'xls', 'csv', 'json'):
                path = os.path.join(root, f)
                files.append({
                    'path': path,
                    'name': f,
                    'ext': ext,
                    'size': os.path.getsize(path),
                })
    return files


def load_file(file_info: dict) -> pd.DataFrame:
    """加载单个文件为 DataFrame。"""
    path = file_info['path']
    ext = file_info['ext']
    try:
        if ext in ('xlsx', 'xls'):
            return pd.read_excel(path)
        elif ext == 'csv':
            # 尝试多种编码
            for enc in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    return pd.read_csv(path, encoding=enc)
                except (UnicodeDecodeError, UnicodeError):
                    continue
            return pd.read_csv(path)
        elif ext == 'json':
            return pd.read_json(path)
    except Exception as e:
        print(f"  Warning: Failed to load {path}: {e}")
        return pd.DataFrame()
    return pd.DataFrame()


def detect_data_type(df: pd.DataFrame) -> str:
    """检测数据类型：时序/截面/面板。"""
    # 检查是否有时间列
    for col in df.columns:
        if '时间' in str(col) or '日期' in str(col) or 'date' in str(col).lower():
            return 'time_series'
        if '时段' in str(col) or 'hour' in str(col).lower():
            return 'time_series'
    # 检查是否有 ID 列
    for col in df.columns:
        if 'id' in str(col).lower() or '编号' in str(col):
            return 'panel'
    return 'cross_section'


def clean_data(df: pd.DataFrame, file_name: str) -> tuple[pd.DataFrame, dict]:
    """清洗数据：缺失值、异常值、单位统一。"""
    report = {
        'file': file_name,
        'original_shape': df.shape,
        'missing_before': int(df.isnull().sum().sum()),
        'issues': [],
    }

    # 1. 删除全空行/列
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    # 2. 缺失值处理
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing = df[col].isnull().sum()
        if missing > 0:
            if missing / len(df) < 0.3:
                # 缺失率<30%，用中位数填充
                df[col] = df[col].fillna(df[col].median())
                report['issues'].append(f"{col}: {missing} missing, filled with median")
            else:
                # 缺失率>=30%，标记
                report['issues'].append(f"{col}: {missing} missing ({missing/len(df)*100:.0f}%), kept as-is")

    # 3. 异常值检测（IQR法）
    outlier_count = 0
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            outlier_count += outliers
            # 不删除，只标记
            report['issues'].append(f"{col}: {outliers} outliers (3*IQR)")

    report['missing_after'] = int(df.isnull().sum().sum())
    report['outlier_count'] = int(outlier_count)
    report['final_shape'] = df.shape

    return df, report


def generate_summary(dfs: dict[str, pd.DataFrame]) -> dict:
    """生成数据摘要。"""
    summary = {
        'generated_at': datetime.now().isoformat(),
        'files': {},
    }
    for name, df in dfs.items():
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        summary['files'][name] = {
            'shape': list(df.shape),
            'columns': list(df.columns),
            'numeric_columns': numeric_cols,
            'dtypes': {col: str(df[col].dtype) for col in df.columns},
            'stats': {},
        }
        for col in numeric_cols[:10]:  # 最多统计10列
            summary['files'][name]['stats'][col] = {
                'mean': round(float(df[col].mean()), 4),
                'std': round(float(df[col].std()), 4),
                'min': round(float(df[col].min()), 4),
                'max': round(float(df[col].max()), 4),
                'median': round(float(df[col].median()), 4),
            }
    return summary


def generate_quality_report(reports: list[dict]) -> str:
    """生成数据质量报告 Markdown。"""
    lines = [
        "# Data Quality Report",
        "",
        f"- Generated: {datetime.now().isoformat()}",
        f"- Files processed: {len(reports)}",
        "",
    ]
    for r in reports:
        lines.append(f"## {r['file']}")
        lines.append(f"- Original shape: {r['original_shape']}")
        lines.append(f"- Final shape: {r['final_shape']}")
        lines.append(f"- Missing before: {r['missing_before']}")
        lines.append(f"- Missing after: {r['missing_after']}")
        lines.append(f"- Outliers: {r['outlier_count']}")
        if r['issues']:
            lines.append("- Issues:")
            for issue in r['issues']:
                lines.append(f"  - {issue}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Auto data processing pipeline")
    parser.add_argument('--problem-dir', default='problem_files', help='Problem files directory')
    parser.add_argument('--output-dir', default='paper_output', help='Output directory')
    args = parser.parse_args()

    problem_dir = args.problem_dir
    output_dir = args.output_dir
    results_dir = os.path.join(output_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    print("=" * 60)
    print("AUTO DATA PROCESSING PIPELINE")
    print("=" * 60)

    # 1. 扫描文件
    print("\n[1] Scanning data files...")
    files = find_data_files(problem_dir)
    print(f"  Found {len(files)} files")
    for f in files:
        print(f"    {f['name']} ({f['size']/1024:.0f} KB)")

    if not files:
        print("  No data files found!")
        return

    # 2. 加载数据
    print("\n[2] Loading data...")
    dfs = {}
    for f in files:
        df = load_file(f)
        if not df.empty:
            name = f['name'].split('.')[0]
            dfs[name] = df
            print(f"  {name}: {df.shape}")

    # 3. 清洗
    print("\n[3] Cleaning data...")
    cleaned_dfs = {}
    reports = []
    for name, df in dfs.items():
        cleaned, report = clean_data(df, name)
        cleaned_dfs[name] = cleaned
        reports.append(report)
        print(f"  {name}: {report['original_shape']} -> {report['final_shape']}")

    # 4. 输出
    print("\n[4] Saving results...")
    # 保存清洗后的数据
    for name, df in cleaned_dfs.items():
        out_path = os.path.join(results_dir, f"clean_{name}.csv")
        df.to_csv(out_path, index=False, encoding='utf-8-sig')
        print(f"  Saved: {out_path}")

    # 保存摘要
    summary = generate_summary(cleaned_dfs)
    summary_path = os.path.join(results_dir, "data_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {summary_path}")

    # 保存质量报告
    report_path = os.path.join(results_dir, "data_quality_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(generate_quality_report(reports))
    print(f"  Saved: {report_path}")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
