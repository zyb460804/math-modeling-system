#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MATLAB 执行器：无头运行 .m 脚本，捕获输出，自动收集 .mat/.png 产物并转 JSON。

本项目 MATLAB 模板齐全（14 必备 + 50 算法）但缺执行入口；本脚本补齐"生成→执行→收结果"
链路末端。MATLAB 强项（ODE45/曲线拟合/优化工具箱/符号计算/Simulink）借此可被流水线直接调用。

用法：
  python matlab_runner.py --script q1_model                # 跑 q1_model.m（在 workdir 下）
  python matlab_runner.py --script e:/path/x.m --workdir paper_output/code/matlab
  python matlab_runner.py --script q1 --collect-json        # 额外把 .mat 转 JSON
依赖：MATLAB ≥ R2019a（支持 -batch）在 PATH 中。

产出：
  paper_output/code/matlab/run_report.json   执行报告（stdout/退出码/产物清单）
  paper_output/code/matlab/*.png *.mat        脚本自己 save/exportgraphics 的产物
  paper_output/code/matlab/*.json             .mat 转 JSON（--collect-json 时）
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

DEFAULT_WORKDIR = Path("paper_output/code/matlab")


def find_matlab() -> str | None:
    return shutil.which("matlab")


def mat_to_json(mat_path: Path, out_path: Path) -> list[str]:
    """把 .mat 顶层变量转 JSON（数值数组降为 list）。返回已转出的变量名。"""
    try:
        from scipy.io import loadmat
        import numpy as np  # type: ignore
    except ImportError:
        return []
    data = loadmat(str(mat_path), squeeze_me=True, struct_as_record=False)
    out: dict = {}
    keys = []
    for k, v in data.items():
        if k.startswith("__"):
            continue
        try:
            if isinstance(v, np.ndarray):
                out[k] = v.tolist()
            else:
                out[k] = v if isinstance(v, (int, float, str)) else str(v)
            keys.append(k)
        except Exception:
            out[k] = str(v)
            keys.append(k)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return keys


def main() -> int:
    p = argparse.ArgumentParser(description="MATLAB 无头执行器")
    p.add_argument("--script", required=True, help="脚本名（不含 .m）或 .m 绝对路径")
    p.add_argument("--workdir", default=str(DEFAULT_WORKDIR), help="工作目录（脚本所在 + 产出去向）")
    p.add_argument("--collect-json", action="store_true", help="把产出的 .mat 转 JSON 供 Python 读")
    p.add_argument("--timeout", type=int, default=300, help="执行超时秒（默认 300）")
    args = p.parse_args()

    matlab_bin = find_matlab()
    if not matlab_bin:
        print("[matlab] ✗ PATH 中找不到 matlab。确认 MATLAB 已装且 bin 在 PATH。", file=sys.stderr)
        return 2

    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    # 解析脚本名：若给的是 .m 路径，取 stem 并确保文件在 workdir
    script_arg = args.script
    sp = Path(script_arg)
    if sp.suffix == ".m":
        name = sp.stem
        if sp.parent.resolve() != workdir and sp.exists():
            shutil.copy2(sp, workdir / sp.name)
    else:
        name = script_arg
    if not (workdir / f"{name}.m").exists():
        print(f"[matlab] ✗ 找不到脚本: {workdir / (name + '.m')}", file=sys.stderr)
        return 2

    # 记录执行前已有产物（便于识别新生成的）
    before = {p.name for p in workdir.iterdir()} if workdir.exists() else set()

    print(f"[matlab] ▶ 执行 {name}.m（工作目录 {workdir}）")
    started = datetime.now().isoformat(timespec="seconds")
    try:
        proc = subprocess.run(
            [matlab_bin, "-batch", name, "-sd", str(workdir)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"[matlab] ✗ 超时（>{args.timeout}s）", file=sys.stderr)
        return 1

    ok = proc.returncode == 0
    mark = "✓" if ok else "✗"
    print(f"[matlab] {mark} 退出码 {proc.returncode}")
    if proc.stdout:
        print(proc.stdout[-1500:])
    if proc.stderr:
        print("[stderr]", proc.stderr[-600:], file=sys.stderr)

    # 收集新生成的产物
    after = {p.name for p in workdir.iterdir()}
    new_files = sorted(after - before - {f"{name}.m"})
    artifacts: list[dict] = []
    for fn in new_files:
        fp = workdir / fn
        art = {"name": fn, "size": fp.stat().st_size, "type": fp.suffix.lstrip(".")}
        if fn.endswith(".mat") and args.collect_json:
            keys = mat_to_json(fp, fp.with_suffix(".json"))
            art["mat_vars"] = keys
            art["json"] = fp.with_suffix(".json").name
        artifacts.append(art)

    report = {
        "script": f"{name}.m",
        "workdir": str(workdir).replace("\\", "/"),
        "started_at": started,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "returncode": proc.returncode,
        "success": ok,
        "stdout_tail": proc.stdout[-800:],
        "stderr_tail": proc.stderr[-400:] if proc.stderr else "",
        "artifacts": artifacts,
    }
    report_path = workdir / "run_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[matlab] 报告 → {report_path}")
    if artifacts:
        print(f"[matlab] 新产物 {len(artifacts)} 个：")
        for a in artifacts:
            extra = f" (vars={a.get('mat_vars')})" if a.get("mat_vars") else ""
            print(f"    {a['type']:4} {a['name']}{extra}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())