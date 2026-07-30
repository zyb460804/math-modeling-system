#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扫描 resources/15_Typst模板/ 生成 typst_index.json。
融合自 jihe520/MathModelAgent 模板结构。
用法: python build_typst_index.py [--root <resources_dir>] [--out <json_path>]
"""
import os, sys, json, re

# 赛事识别关键词 → 标准 competition key
COMPETITION_MAP = {
    "cumcm": "CUMCM 国赛",
    "mcm": "MCM/ICM 美赛",
    "apmcm": "APMCM 亚太",
    "huashubei": "华数杯",
    "huaweibei": "华为杯",
    "changsanjiao": "长三角",
    "default": "默认通用",
}

def detect_competition(name):
    n = name.lower()
    for k, v in COMPETITION_MAP.items():
        if k in n:
            return v
    return "未知"

def scan_template_set(set_dir):
    """扫描一个模板集（如 zh/cumcm），返回结构信息。"""
    info = {"path": set_dir.replace("\\", "/"), "files": []}
    for root, _, files in os.walk(set_dir):
        for f in files:
            if f.endswith((".typ", ".tex", ".bib")):
                rel = os.path.relpath(os.path.join(root, f), set_dir).replace("\\", "/")
                info["files"].append(rel)
    info["has_main_typ"] = "main.typ" in info["files"]
    info["section_count"] = sum(1 for x in info["files"] if x.startswith("sections/"))
    return info

def main():
    root = "e:/数学建模/resources/15_Typst模板"
    out = "e:/数学建模/resources/15_Typst模板/typst_index.json"
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--root" and i + 1 < len(args):
            root = args[i + 1]
        if a == "--out" and i + 1 < len(args):
            out = args[i + 1]

    index = {"templates": {}, "stats": {}}
    typ_count = tex_count = 0
    if not os.path.isdir(root):
        print(f"[WARN] 模板根目录不存在: {root}")
        sys.exit(1)

    for lang in sorted(os.listdir(root)):
        lang_dir = os.path.join(root, lang)
        if not os.path.isdir(lang_dir):
            continue
        index["templates"].setdefault(lang, {})
        for name in sorted(os.listdir(lang_dir)):
            set_dir = os.path.join(lang_dir, name)
            if not os.path.isdir(set_dir):
                continue
            info = scan_template_set(set_dir)
            info["competition"] = detect_competition(name)
            info["format"] = "typst" if name.endswith(("-typ",)) or not name.endswith("-latex") else "latex"
            # 修正：目录名以 -latex 结尾的是 LaTeX 版，否则是 Typst 版
            info["format"] = "latex" if name.endswith("-latex") else "typst"
            index["templates"][lang][name] = info
            if info["format"] == "typst":
                typ_count += 1
            else:
                tex_count += 1

    index["stats"] = {
        "typst_sets": typ_count,
        "latex_sets": tex_count,
        "competitions": sorted(set(COMPETITION_MAP.values())),
    }

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"[OK] 索引已生成: {out}")
    print(f"     Typst 集: {typ_count}  LaTeX 集: {tex_count}")
    # 打印赛事覆盖
    covered = set()
    for lang, sets in index["templates"].items():
        for name, info in sets.items():
            if info["format"] == "typst":
                covered.add(info["competition"])
    print(f"     Typst 赛事覆盖: {sorted(covered)}")

if __name__ == "__main__":
    main()
