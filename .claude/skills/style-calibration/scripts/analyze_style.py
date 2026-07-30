#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_style.py — 写作风格画像分析（style-calibration skill）

从 1..N 个用户过往作品文本中提取可离线计量的风格指标，输出 style_profile.json：
  - 句长分布（均值/中位数/P90）
  - 段落长度（每段字符数、每段句数）
  - 标点密度（逗号/顿号/分号/冒号/破折号/括号/问号，每千字）
  - 高频句子开头词
  - 连接词偏好（每千字密度 + Top 列表）
  - 中英文混排比例（英文字母/数字/汉字占比）
  - 四字成语密度（基于内置常用成语表的近似统计）

仅依赖 Python 标准库。示例：
    python analyze_style.py --samples user_papers/ --output paper_output/qa/style_profile.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter
from datetime import datetime

TOOL_VERSION = "analyze_style.py v1.1"
TEXT_EXTS = {".txt", ".md", ".markdown", ".text"}

# 连接词表（已去除互为子串的项，避免重复计数）
CONNECTIVES = (
    "因此 然而 此外 同时 由于 从而 进而 综上 首先 其次 再次 最后 另外 并且 "
    "但是 所以 因而 于是 其中 例如 一方面 总之 换言之 相比之下 事实上 特别地 "
    "值得注意的是 需要指出的是 不难看出 由此可见 基于此 据此 进一步 不仅 而且 "
    "同样 类似地 反之 否则"
).split()
CONNECTIVES_BY_LEN = sorted(CONNECTIVES, key=len, reverse=True)

# 内置常用四字成语表（学术/建模论文常见，近似统计用）
IDIOMS = (
    "层出不穷 举足轻重 至关重要 息息相关 密不可分 相辅相成 环环相扣 有的放矢 因地制宜 因势利导 "
    "统筹兼顾 权衡利弊 扬长避短 精益求精 循序渐进 有条不紊 井然有序 一目了然 显而易见 不言而喻 "
    "毋庸置疑 恰到好处 恰如其分 行之有效 卓有成效 事半功倍 得不偿失 顾此失彼 相得益彰 迎刃而解 "
    "水到渠成 有目共睹 屡见不鲜 与日俱增 日新月异 突飞猛进 方兴未艾 不可或缺 不容忽视 举一反三 "
    "触类旁通 融会贯通 深入浅出 言简意赅 面面俱到 以此类推 由表及里 由浅入深 去粗取精 去伪存真 "
    "集思广益 博采众长 取长补短 优胜劣汰 供不应求 此消彼长 大同小异 千差万别 参差不齐 泾渭分明 "
    "一脉相承 殊途同归 异曲同工 如出一辙 大势所趋 势在必行 迫在眉睫 刻不容缓 任重道远 前车之鉴 "
    "未雨绸缪 防患未然 有备无患 稳扎稳打 齐头并进 双管齐下 并行不悖 一以贯之 自圆其说 言之有物 "
    "有章可循 有据可依 独树一帜 别具一格 恰逢其时 立竿见影 一举两得 数以万计 微乎其微 举重若轻"
).split()

SENT_SPLIT_RE = re.compile(r"[。！？!?]+")
CJK_RE = re.compile(r"[一-鿿]")
LEAD_STRIP_RE = re.compile(r"^[\s“”\"'‘’「」《》（()）\[\]【】\d.\-、:：]+")


def read_text(path: str) -> str:
    """读取文本文件：优先 utf-8，回退 gbk，最终替换非法字节。"""
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read()
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            raise SystemExit(f"[错误] 无法读取文件 {path}: {exc}")
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def collect_sample_files(inputs) -> list:
    """展开文件/目录参数，目录递归收集 .txt/.md 文本。"""
    files = []
    for item in inputs:
        if os.path.isdir(item):
            for root, _dirs, names in os.walk(item):
                for name in sorted(names):
                    if os.path.splitext(name)[1].lower() in TEXT_EXTS:
                        files.append(os.path.join(root, name))
        elif os.path.isfile(item):
            files.append(item)
        else:
            raise SystemExit(f"[错误] 样本路径不存在: {item}")
    files = list(dict.fromkeys(files))
    if not files:
        raise SystemExit("[错误] 未找到任何样本文本（目录中需含 .txt/.md 文件）")
    return files


def clean_text(text: str) -> str:
    """去掉代码块/标题/表格/引用等干扰行，仅保留正文。"""
    text = re.sub(r"```.*?```", "\n", text, flags=re.S)
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", ">", "---", "![", "```")):
            out.append("")
            continue
        stripped = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", stripped)
        stripped = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", stripped)
        out.append(stripped)
    return "\n".join(out)


def split_paragraphs(text: str) -> list:
    """段落 = 清洗后以空行分隔的文本块（块内换行直接拼接）。"""
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        joined = "".join(ln.strip() for ln in block.splitlines())
        if joined:
            paragraphs.append(joined)
    return paragraphs


def split_sentences(paragraph: str) -> list:
    """按中文句末标点（。！？!?）切句。"""
    return [p.strip() for p in SENT_SPLIT_RE.split(paragraph) if p.strip()]


def sentence_starter(sentence: str) -> str:
    """取句子开头词：优先匹配连接词，其次英文单词，否则前 2 个汉字。"""
    s = LEAD_STRIP_RE.sub("", sentence)
    if not s:
        return ""
    for conn in CONNECTIVES_BY_LEN:
        if s.startswith(conn):
            return conn
    match = re.match(r"[A-Za-z]+", s)
    if match:
        return match.group(0)
    return s[:2]


def percentile(values: list, q: float) -> float:
    """最近邻分位数（无外部依赖）。"""
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(round(q * (len(ordered) - 1))))
    return float(ordered[idx])


def text_metrics(text: str, already_clean: bool = False):
    """对整篇或单段文本计算风格指标；无有效正文时返回 None。"""
    if not already_clean:
        text = clean_text(text)
    paragraphs = split_paragraphs(text)
    sentences = [s for p in paragraphs for s in split_sentences(p)]
    joined = "".join(paragraphs)
    n_chars = len(re.sub(r"\s+", "", joined))
    if n_chars == 0 or not sentences:
        return None

    sent_lens = [len(re.sub(r"\s+", "", s)) for s in sentences]
    para_lens = [len(re.sub(r"\s+", "", p)) for p in paragraphs]
    para_sents = [len(split_sentences(p)) for p in paragraphs]

    def per_k(count: float) -> float:
        return round(count * 1000.0 / n_chars, 2)

    punctuation = {
        "逗号": per_k(joined.count("，") + joined.count(",")),
        "顿号": per_k(joined.count("、")),
        "分号": per_k(joined.count("；") + joined.count(";")),
        "冒号": per_k(joined.count("：") + joined.count(":")),
        "破折号": per_k(len(re.findall(r"——|—|--", joined))),
        "括号": per_k(joined.count("（") + joined.count("(")),
        "问号": per_k(joined.count("？") + joined.count("?")),
    }

    starters = Counter(w for w in (sentence_starter(s) for s in sentences) if w)
    conn_counts = {c: joined.count(c) for c in CONNECTIVES if c in joined}
    idiom_counts = {i: joined.count(i) for i in IDIOMS if i in joined}
    n_letters = len(re.findall(r"[A-Za-z]", joined))
    n_digits = len(re.findall(r"[0-9]", joined))

    return {
        "n_chars": n_chars,
        "n_sentences": len(sentences),
        "n_paragraphs": len(paragraphs),
        "sentence_length": {
            "mean": round(statistics.mean(sent_lens), 1),
            "median": round(statistics.median(sent_lens), 1),
            "p90": round(percentile(sent_lens, 0.9), 1),
        },
        "paragraph": {
            "mean_chars": round(statistics.mean(para_lens), 1),
            "median_chars": round(statistics.median(para_lens), 1),
            "mean_sentences": round(statistics.mean(para_sents), 2),
        },
        "punctuation_per_1000": punctuation,
        "starters_top": [[w, c, round(c / len(sentences), 3)]
                         for w, c in starters.most_common(10)],
        "connective_per_1000": per_k(sum(conn_counts.values())),
        "connectives_top": sorted(conn_counts.items(), key=lambda kv: -kv[1])[:10],
        "english_ratio": round(n_letters / n_chars, 4),
        "digit_ratio": round(n_digits / n_chars, 4),
        "cjk_ratio": round(len(CJK_RE.findall(joined)) / n_chars, 4),
        "idiom_per_1000": per_k(sum(idiom_counts.values())),
        "idioms_found": sorted(idiom_counts.items(), key=lambda kv: -kv[1])[:15],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="写作风格画像分析：从用户过往作品统计可离线计量的风格指标，"
                    "输出 style_profile.json（句长/段落/标点/开头词/连接词/中英混排/成语密度）。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--samples", "--input", dest="samples", nargs="+", required=True,
                        metavar="PATH",
                        help="1..N 个样本文件或目录（目录递归收集 .txt/.md；--input 为兼容别名）")
    parser.add_argument("--output", "-o", default="paper_output/qa/style_profile.json",
                        help="风格画像输出路径（JSON）")
    parser.add_argument("--min-chars", type=int, default=500,
                        help="语料总字数低于该值时给出可信度警告（不中止）")
    return parser


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    files = collect_sample_files(args.samples)

    sample_infos, cleaned_parts = [], []
    for path in files:
        cleaned = clean_text(read_text(path))
        metrics = text_metrics(cleaned, already_clean=True)
        if metrics is None:
            print(f"[警告] 样本无有效正文，已跳过: {path}")
            continue
        sample_infos.append({"path": path, "chars": metrics["n_chars"],
                             "sentences": metrics["n_sentences"]})
        cleaned_parts.append(cleaned)
    if not cleaned_parts:
        raise SystemExit("[错误] 所有样本均无有效正文，无法生成画像")

    corpus = text_metrics("\n\n".join(cleaned_parts), already_clean=True)
    warnings = []
    if corpus["n_chars"] < args.min_chars:
        warnings.append(f"语料仅 {corpus['n_chars']} 字（<{args.min_chars}），"
                        "画像可信度有限，建议补充样本")

    profile = {
        "tool": TOOL_VERSION,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "samples": sample_infos,
        "warnings": warnings,
        "metrics": corpus,
        "note": "所有指标均为离线可计量统计；成语密度基于内置常用成语表，为近似值。",
    }
    out_dir = os.path.dirname(os.path.abspath(args.output))
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(profile, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise SystemExit(f"[错误] 无法写入输出文件 {args.output}: {exc}")

    sl = corpus["sentence_length"]
    print(f"[完成] 风格画像已写入: {args.output}")
    print(f"  样本数: {len(sample_infos)} | 总字数: {corpus['n_chars']}"
          f" | 句子数: {corpus['n_sentences']} | 段落数: {corpus['n_paragraphs']}")
    print(f"  句长 均值/中位/P90: {sl['mean']}/{sl['median']}/{sl['p90']} 字")
    print(f"  逗号 {corpus['punctuation_per_1000']['逗号']}/千字 | "
          f"连接词 {corpus['connective_per_1000']}/千字 | "
          f"成语 {corpus['idiom_per_1000']}/千字 | "
          f"英文占比 {corpus['english_ratio']:.1%}")
    for warning in warnings:
        print(f"[警告] {warning}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
