from __future__ import annotations

import argparse
import locale
import os
import shutil
import sys
from pathlib import Path

# Windows GBK 控制台兼容：强制 stdout/stderr 走 utf-8，避免数学符号/中文崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

# Load .env from project root
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)
load_dotenv(override=False)

from llama_index.core import Settings, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from mmqa.node_export import load_text_nodes_jsonl
from mmqa.postprocessors import DropLowInfoNodesPostprocessor


def _safe_input(prompt: str) -> str:
    """Read one line from stdin with readline support (backspace, arrows).
    Falls back to raw buffer reading for non-UTF8 terminals (e.g. GBK/GB18030).
    """
    try:
        return input(prompt).strip()
    except UnicodeDecodeError:
        pass

    # Fallback: manual decoding for broken terminal encodings
    sys.stdout.write(prompt)
    sys.stdout.flush()
    data = sys.stdin.buffer.readline()
    if not data:
        raise EOFError
    data = data.rstrip(b"\r\n")

    candidates = [
        sys.stdin.encoding,
        locale.getpreferredencoding(False),
        "utf-8",
        "gb18030",
    ]
    for enc in candidates:
        if not enc:
            continue
        try:
            return data.decode(enc).strip()
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace").strip()


def _get_env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)


def _get_api_key_optional() -> str | None:
    """返回 OPENAI_API_KEY 或 None（缺失时返回 None，不退出）。"""
    return _get_env("OPENAI_API_KEY")


def _init_models() -> None:
    api_key = _get_api_key_optional()
    api_base = _get_env("OPENAI_API_BASE") or _get_env("OPENAI_BASE_URL")

    if api_key:
        # 在线模式：OpenAI embed + LLM
        Settings.llm = OpenAI(
            model=_get_env("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=api_key,
            api_base=api_base,
        )
        Settings.embed_model = OpenAIEmbedding(
            model=_get_env("OPENAI_EMBED_MODEL", "text-embedding-3-large"),
            api_key=api_key,
            api_base=api_base,
        )
    else:
        # 离线模式：HuggingFace 本地 embedding（build 向量索引可用；chat 生成需另配 LLM）
        try:
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        except ImportError:
            print(
                "无 OPENAI_API_KEY 且未安装 llama-index-embeddings-huggingface。\n"
                "二选一：\n"
                "  (在线) 设 OPENAI_API_KEY 环境变量\n"
                "  (离线) pip install llama-index-embeddings-huggingface sentence-transformers",
                file=sys.stderr,
            )
            raise SystemExit(2)
        model_name = _get_env(
            "HF_EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )  # 384 维，中英混合语料；换模型需重建索引
        print(f"[rag] 无 API key → 离线模式，本地 embedding: {model_name}", file=sys.stderr)
        Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
        Settings.llm = None  # build 不需要 LLM；chat 命令会提示需配 LLM


def _build_filters(args: argparse.Namespace) -> MetadataFilters | None:
    filters: list[MetadataFilter] = []
    if args.year is not None:
        filters.append(MetadataFilter(key="year", value=int(args.year)))
    if args.problem is not None:
        filters.append(MetadataFilter(key="problem", value=str(args.problem)))
    if args.problem_id is not None:
        filters.append(MetadataFilter(key="problem_id", value=str(args.problem_id)))
    if args.section is not None:
        filters.append(MetadataFilter(key="section", value=str(args.section)))
    if args.doc_id is not None:
        filters.append(MetadataFilter(key="doc_id", value=str(args.doc_id)))
    if not filters:
        return None
    return MetadataFilters(filters=filters)


def _load_or_build_index(
    *,
    nodes_jsonl: Path,
    persist_dir: Path,
    rebuild: bool,
    show_progress: bool,
) -> VectorStoreIndex:
    if rebuild and persist_dir.exists():
        shutil.rmtree(persist_dir)

    if persist_dir.exists():
        storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
        return load_index_from_storage(storage_context)

    nodes = load_text_nodes_jsonl(nodes_jsonl)
    index = VectorStoreIndex(nodes, show_progress=show_progress)
    persist_dir.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(persist_dir))
    return index


def cmd_build(args: argparse.Namespace) -> int:
    _init_models()

    index = _load_or_build_index(
        nodes_jsonl=Path(args.nodes_jsonl),
        persist_dir=Path(args.persist_dir),
        rebuild=args.rebuild,
        show_progress=args.show_progress,
    )
    # silence unused variable warnings
    _ = index
    print(f"Index ready at: {args.persist_dir}")
    return 0


def cmd_retrieve(args: argparse.Namespace) -> int:
    """纯检索（不调用 LLM，完全离线）：读向量库 + HF 嵌入 query + 余弦相似度 + 过滤 + top-k。

    绕过 llama_index 的 retriever/MockLLM，直接对 default__vector_store.json 做相似度。
    """
    _init_models()  # 设置 embed_model（离线模式用 HuggingFace）

    import json as _json
    import numpy as np

    vs_path = Path(args.persist_dir) / "default__vector_store.json"
    ds_path = Path(args.persist_dir) / "docstore.json"
    if not vs_path.exists():
        print(f"[retrieve] 向量库不存在: {vs_path}（先运行 build）", file=sys.stderr)
        return 2

    vs = _json.loads(vs_path.read_text(encoding="utf-8"))
    embedding_dict: dict[str, list[float]] = vs.get("embedding_dict", {})
    metadata_dict: dict[str, dict] = vs.get("metadata_dict", {})
    ds = _json.loads(ds_path.read_text(encoding="utf-8"))
    ds_data = ds.get("docstore/data", {})
    texts: dict[str, str] = {
        nid: (node.get("__data__", {}).get("text") or "")
        for nid, node in ds_data.items()
    }

    if not embedding_dict:
        print("[retrieve] 向量库为空（先 build）", file=sys.stderr)
        return 2

    # 元数据过滤
    node_ids = []
    for nid, meta in metadata_dict.items():
        if args.year is not None and int(meta.get("year") or 0) != args.year:
            continue
        if args.problem and str(meta.get("problem") or "") != args.problem:
            continue
        if args.section and str(meta.get("section") or "") != args.section:
            continue
        node_ids.append(nid)
    if not node_ids:
        print(f"[retrieve] 过滤后无节点（year={args.year} problem={args.problem} section={args.section}）")
        return 0

    # 嵌入 query + 余弦相似度
    q_emb = Settings.embed_model.get_query_embedding(args.query)
    qvec = np.asarray(q_emb, dtype=np.float32)
    rows = []
    for nid in node_ids:
        vec = np.asarray(embedding_dict[nid], dtype=np.float32)
        denom = (np.linalg.norm(qvec) * np.linalg.norm(vec)) + 1e-9
        sim = float(np.dot(qvec, vec) / denom)
        rows.append((sim, nid))
    rows.sort(key=lambda x: x[0], reverse=True)
    top_k = int(args.top_k or 10)
    print(f"[retrieve] query={args.query!r}  候选={len(node_ids)}  top_k={top_k}\n")
    for rank, (sim, nid) in enumerate(rows[:top_k], 1):
        meta = metadata_dict.get(nid, {})
        text = texts.get(nid, "").replace("\n", " ")[:120]
        print(f"  #{rank} score={sim:.4f}  {meta.get('competition','?')} {meta.get('year','?')} {meta.get('problem','?')} [{meta.get('section','?')}]")
        print(f"       {text}")
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    _init_models()

    if Settings.llm is None:
        print(
            "[rag] chat 需要生成式 LLM，但当前为离线模式（无 OPENAI_API_KEY）。\n"
            "请设置 OPENAI_API_KEY 后再用 chat，或先单独用 build 建好向量索引。",
            file=sys.stderr,
        )
        return 2

    index = _load_or_build_index(
        nodes_jsonl=Path(args.nodes_jsonl),
        persist_dir=Path(args.persist_dir),
        rebuild=False,
        show_progress=args.show_progress,
    )

    filters = _build_filters(args)
    token_limit = int(_get_env("CHAT_TOKEN_LIMIT", "400000"))
    memory = ChatMemoryBuffer.from_defaults(token_limit=token_limit)

    node_postprocessors = [
        DropLowInfoNodesPostprocessor(
            drop_heading_only=not args.keep_heading_only,
            drop_toc=not args.keep_toc,
        )
    ]

    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        similarity_top_k=int(args.top_k or _get_env("SIMILARITY_TOP_K", "18")),
        filters=filters,
        memory=memory,
        node_postprocessors=node_postprocessors,
    )

    print("Chat ready. Type 'quit' to exit.")
    if filters is not None:
        print(f"Filters: {filters}")

    while True:
        try:
            q = _safe_input("Q> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        if q.lower() in {"quit", "exit"}:
            break
        resp = chat_engine.chat(q)
        print(resp.response)
        if args.show_sources and getattr(resp, "source_nodes", None):
            print("\n[SOURCES]")
            for i, sn in enumerate(resp.source_nodes[: args.show_sources]):
                md = sn.metadata or {}
                print(
                    f"{i+1}. doc_id={md.get('doc_id')} year={md.get('year')} "
                    f"problem={md.get('problem')} section={md.get('section')} heading={md.get('heading')}"
                )
            print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MCM papers RAG CLI (build index + interactive chat).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument(
            "--nodes-jsonl",
            default=str(PROJECT_ROOT / "data/nodes/text_nodes.block.jsonl"),
            help="Input nodes JSONL (default: data/nodes/text_nodes.block.jsonl)",
        )
        sp.add_argument(
            "--persist-dir",
            default=str(PROJECT_ROOT / "storage"),
            help="Persisted index directory (default: storage/)",
        )
        sp.add_argument("--show-progress", action="store_true", help="Show embedding/build progress.")

    sp_build = sub.add_parser("build", help="Build (or load) the vector index.")
    add_common(sp_build)
    sp_build.add_argument("--rebuild", action="store_true", help="Delete and rebuild persisted index.")
    sp_build.set_defaults(func=cmd_build)

    sp_ret = sub.add_parser("retrieve", help="纯检索（离线，不调 LLM）：query + 过滤 + top-k。")
    add_common(sp_ret)
    sp_ret.add_argument("--query", required=True, help="检索查询串")
    sp_ret.add_argument("--year", type=int, default=None)
    sp_ret.add_argument("--problem", type=str, default=None, help="A/B/C/D/E/F")
    sp_ret.add_argument("--section", type=str, default=None, help="如 Body / Summary / Sensitivity")
    sp_ret.add_argument("--top-k", type=int, default=10)
    sp_ret.set_defaults(func=cmd_retrieve)

    sp_chat = sub.add_parser("chat", help="Start an interactive chat session (continuous Q&A).")
    add_common(sp_chat)
    sp_chat.add_argument("--year", type=int, default=None)
    sp_chat.add_argument("--problem", type=str, default=None, help="A/B/C/D/E/F")
    sp_chat.add_argument("--problem-id", type=str, default=None, help="e.g. 2025C")
    sp_chat.add_argument("--section", type=str, default=None, help="Canonical section name (exact match).")
    sp_chat.add_argument("--doc-id", type=str, default=None, help="e.g. 2025C_1")
    sp_chat.add_argument("--top-k", type=int, default=None, help="Override similarity_top_k (default from local_settings).")
    sp_chat.add_argument(
        "--show-sources",
        type=int,
        default=0,
        help="Print top N retrieved source nodes after each answer (0=off).",
    )
    sp_chat.add_argument(
        "--keep-heading-only",
        action="store_true",
        help="Do not drop heading-only nodes (default: drop them except Title & Summary).",
    )
    sp_chat.add_argument(
        "--keep-toc",
        action="store_true",
        help="Do not drop 'Contents'/'Content' nodes (default: drop them).",
    )
    sp_chat.set_defaults(func=cmd_chat)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
