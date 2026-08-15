"""LaTeX 公式渲染器：扫描 .md 文件中的公式，渲染为 PNG 图片。

用法：
    python render_formulas.py                          # 渲染 paper_output/ 中所有公式
    python render_formulas.py --input paper.md         # 渲染指定文件
    python render_formulas.py --dpi 300                # 指定分辨率
"""
import re
import os
import sys
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def configure_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def extract_formulas(text: str) -> list[dict]:
    """从 Markdown 文本中提取 LaTeX 公式。"""
    formulas = []
    
    # 行间公式 $$...$$
    for match in re.finditer(r'\$\$(.*?)\$\$', text, re.DOTALL):
        formulas.append({
            "latex": match.group(1).strip(),
            "type": "display",
            "start": match.start(),
            "end": match.end(),
        })
    
    # 行内公式 $...$（排除转义的 \$）
    for match in re.finditer(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', text):
        formulas.append({
            "latex": match.group(1).strip(),
            "type": "inline",
            "start": match.start(),
            "end": match.end(),
        })
    
    return formulas


def render_formula(latex: str, output_path: str, dpi: int = 150, fontsize: int = 14) -> bool:
    """渲染单个公式为 PNG 图片。"""
    try:
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, ha="center", va="center",
                transform=ax.transAxes, math_fontfamily="cm")
        ax.axis("off")
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight", pad_inches=0.1)
        plt.close()
        return True
    except Exception as e:
        plt.close()
        print(f"  渲染失败: {e}")
        return False


def main(input_file=None, dpi=150):
    configure_utf8()
    
    root = Path.cwd()
    figures_dir = root / "paper_output" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # 找到要处理的文件
    if input_file:
        md_files = [root / Path(input_file)] if not Path(input_file).is_absolute() else [Path(input_file)]
    else:
        md_files = sorted((root / "paper_output").rglob("*.md"))
    
    all_formulas = []
    formula_index = []
    formula_counter = 0
    
    for md_file in md_files:
        if not md_file.exists():
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        
        formulas = extract_formulas(text)
        if not formulas:
            continue
        
        print(f"  {md_file.name}: {len(formulas)} 个公式")
        
        for f in formulas:
            formula_counter += 1
            img_name = f"formula_{formula_counter:03d}.png"
            img_path = figures_dir / img_name
            
            success = render_formula(f["latex"], str(img_path), dpi=dpi)
            if success:
                formula_index.append({
                    "id": formula_counter,
                    "latex": f["latex"],
                    "type": f["type"],
                    "source_file": str(md_file.relative_to(root)),
                    "image_path": str(img_path.relative_to(root)),
                })
                all_formulas.append(f["latex"])
    
    # 保存公式索引
    index_path = root / "paper_output" / "tables" / "formula_index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_formulas": len(formula_index),
            "formulas": formula_index,
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n  共渲染 {len(formula_index)} 个公式")
    print(f"  公式索引: {index_path.relative_to(root)}")
    print(f"  图片目录: {figures_dir.relative_to(root)}")
    
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LaTeX 公式渲染器：扫描 .md 文件中的公式，渲染为 PNG 图片并生成公式索引。",
    )
    parser.add_argument("--input", default=None, help="指定要渲染的 .md 文件路径（默认扫描 paper_output/ 全部 .md）")
    parser.add_argument("--dpi", type=int, default=150, help="渲染分辨率（默认 150）")
    args = parser.parse_args()
    raise SystemExit(main(args.input, args.dpi))
