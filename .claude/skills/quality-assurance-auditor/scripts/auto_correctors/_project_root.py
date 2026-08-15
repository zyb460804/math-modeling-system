#!/usr/bin/env python3
"""项目根锚定 —— M-13 统一方案（未收口 #9）。

格式链四个脚本此前三种锚定并存：
  - check_paper_format.py / format_formal_docx.py 用 ``Path.cwd()``：
    从错误 cwd 运行会读错源稿 / 写错报告，甚至凭空创建 paper_output/ 树；
  - latex_auto_fixer.py / citation_auto_fixer.py 用 ``Path(__file__).parents[5]``：
    硬编码层级，脚本被复制到其它深度后第 5 级祖先会指向沙箱外或真实树
    —— 即实测病灶「空沙箱却扫到/写到真实树」。

统一方案：从 ``Path(__file__)`` 逐级上溯，取首个同时满足以下双标志的祖先为项目根：
  1) 含 ``.claude`` 目录；
  2) 含 ``CLAUDE.md`` 文件或 ``paper_output`` 目录（项目标志）。
找不到（脚本被复制到项目树外，或只遇到 home 目录形态的 ``.claude``）时抛
ProjectRootNotFoundError，绝不静默回退 cwd / 固定层级 / 最近单标志。

双标志设计用于防误锚：用户 home（如 ``C:/Users/<user>/.claude``）满足标志 1
但不满足标志 2，不是本项目根，不能作为锚（否则沙箱在 home 下时会写穿到 home）。

（本文件与 paper-formal-writer/scripts/_project_root.py 内容一致——格式链脚本
分属两个 skill 目录，各自持一份；模块按 __file__ 自定位，两份行为完全相同。）
"""

from __future__ import annotations

from pathlib import Path


class ProjectRootNotFoundError(RuntimeError):
    """项目根无法定位 —— 硬失败而非静默猜。"""


def find_project_root(start: Path | None = None) -> Path:
    """定位项目根（设计与病灶背景见模块 docstring）。

    Args:
        start: 上溯的起点路径，默认本模块文件自身位置；测试可显式传入。

    Returns:
        定位到的项目根（resolved 绝对路径）。

    Raises:
        ProjectRootNotFoundError: 上溯到盘符仍未找到满足双标志的祖先。
    """
    origin = (start if start is not None else Path(__file__)).resolve()
    for candidate in (origin, *origin.parents):
        if not (candidate / ".claude").is_dir():
            continue
        if (candidate / "CLAUDE.md").is_file() or (candidate / "paper_output").is_dir():
            return candidate
        # 裸 .claude 但无项目标志（home 目录形态）：不是根，跳过继续上溯
    raise ProjectRootNotFoundError(
        f"无法定位项目根：从 {origin} 逐级上溯未找到同时含 .claude 目录"
        "与 CLAUDE.md / paper_output 项目标志的祖先。脚本很可能被复制到了项目树之外"
        "（或在沙箱内运行）——请从项目树内运行，或通过命令行参数显式指定输入输出路径。"
    )


# 惰性求值（PEP 562）：import 时不定位、首次访问 PROJECT_ROOT 属性才求值。
# 若在模块级直接求值，import 本身就会因锚定失败而炸——调用方（四个格式链
# 脚本）的 try/except ProjectRootNotFoundError 便永远走不到，只能拿裸 traceback。
# 惰性化后"找不到根"统一由调用方决定退出方式（CLI 脚本 → [ANCHOR FAILED] + rc=2）。
_PROJECT_ROOT_CACHE: Path | None = None


def __getattr__(name: str) -> Path:
    if name == "PROJECT_ROOT":
        global _PROJECT_ROOT_CACHE
        if _PROJECT_ROOT_CACHE is None:
            _PROJECT_ROOT_CACHE = find_project_root()
        return _PROJECT_ROOT_CACHE
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
