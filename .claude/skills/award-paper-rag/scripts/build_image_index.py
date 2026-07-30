#!/usr/bin/env python
"""
build_image_index.py — 图片向量库构建脚本（离线版）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描 resources/ 下所有 PNG/JPG 图片，用 TF-IDF + 路径语义信息
生成多模态向量，存入 LlamaIndex 兼容的 image__vector_store.json。

策略（离线优先）:
  1. 尝试 CLIP（需网络下载 ~600MB）→ 失败则 fallback
  2. 尝试 paraphrase-multilingual-MiniLM-L12-v2（384维）→ 失败则 fallback
  3. TF-IDF（sklearn，纯本地）→ 永远可用

用法:
  python build_image_index.py                    # 自动选择最佳可用模型
  python build_image_index.py --rebuild           # 删除旧索引重建
  python build_image_index.py --limit 50          # 先索引 50 张测试
  python build_image_index.py --model tfidf       # 强制指定模型

依赖: torch torchvision transformers scikit-learn Pillow llama-index
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── 路径 ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # award-paper-rag/
STORAGE_DIR = PROJECT_ROOT / "storage"
RESOURCES_DIR = Path(__file__).resolve().parents[4] / "resources"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def _find_images(
    image_dir: Path, limit: Optional[int] = None
) -> list[Path]:
    """递归扫描图片文件。"""
    images: list[Path] = []
    for root, dirs, files in os.walk(image_dir):
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "__pycache__"}]
        for fname in sorted(files):
            if Path(fname).suffix.lower() in IMAGE_EXTS:
                images.append(Path(root) / fname)
    images.sort()
    if limit:
        images = images[:limit]
    return images


def _parse_metadata(img_path: Path, resources_root: Path) -> dict:
    """从图片路径中提取竞赛/题型/算法等元数据。"""
    try:
        rel = img_path.relative_to(resources_root)
    except ValueError:
        rel = img_path
    path_str = str(rel).lower()

    meta: dict = {
        "source_path": str(img_path),
        "relative_path": str(rel),
    }

    # 竞赛
    if "mcm" in path_str or "icm" in path_str or "美赛" in path_str:
        meta["competition"] = "MCM-ICM"
    elif "cumcm" in path_str or "国赛" in path_str:
        meta["competition"] = "CUMCM"
    elif "mathorcup" in path_str:
        meta["competition"] = "MathorCup"
    elif "电工杯" in path_str:
        meta["competition"] = "电工杯"
    else:
        meta["competition"] = "unknown"

    # 题型
    if any(kw in path_str for kw in ["评价", "evaluation", "topsis", "ahp", "熵权", "dea", "模糊"]):
        meta["task_type"] = "evaluation"
    elif any(kw in path_str for kw in ["预测", "prediction", "lstm", "arima", "prophet", "elman", "narx"]):
        meta["task_type"] = "prediction"
    elif any(kw in path_str for kw in ["优化", "optimization", "pso", "遗传算法", "粒子群", "模拟退火", "蚁群"]):
        meta["task_type"] = "optimization"
    elif any(kw in path_str for kw in ["聚类", "clustering", "kmeans", "k-means", "dbscan"]):
        meta["task_type"] = "clustering"
    elif any(kw in path_str for kw in ["分类", "classification", "svm", "支持向量", "som", "pnn"]):
        meta["task_type"] = "classification"
    elif any(kw in path_str for kw in ["图表", "绘图", "可视化", "plot", "chart", "figure"]):
        meta["task_type"] = "visualization"
    elif any(kw in path_str for kw in ["神经网络", "neural", "bp", "rbf", "cnn"]):
        meta["task_type"] = "neural_network"
    else:
        meta["task_type"] = "other"

    # 算法关键词
    algo_keywords: list[str] = []
    algo_map = {
        "遗传": "genetic_algorithm", "粒子群": "pso", "蚁群": "aco",
        "模拟退火": "simulated_annealing", "bp神经网络": "bp_nn",
        "svm": "svm", "支持向量": "svm", "随机森林": "random_forest",
        "xgboost": "xgboost", "lightgbm": "lightgbm",
        "topsis": "topsis", "熵权": "entropy_weight", "pca": "pca",
        "lstm": "lstm", "nsga": "nsga_ii", "rbf": "rbf_nn",
        "elman": "elman_nn", "narx": "narx_nn", "som": "som", "pnn": "pnn",
        "灰色": "grey_model", "马尔可夫": "markov", "贝叶斯": "bayesian",
        "聚类": "clustering", "dea": "dea", "k-means": "kmeans", "knn": "knn",
        "dijkstra": "dijkstra", "floyd": "floyd", "arima": "arima",
        "prophet": "prophet", "微分": "differential_equation",
        "蒙特卡洛": "monte_carlo", "层次分析": "ahp",
    }
    for cn, en in algo_map.items():
        if cn in path_str:
            algo_keywords.append(en)
    meta["algorithms"] = list(set(algo_keywords))

    # 文件信息
    try:
        stat = img_path.stat()
        meta["file_size_kb"] = round(stat.st_size / 1024, 1)
    except OSError:
        meta["file_size_kb"] = 0

    return meta


def _build_rich_description(img_path: Path, meta: dict) -> str:
    """为图片生成丰富的文本描述（用于 embedding）。"""
    # 从路径各部分提取关键词
    parts = list(img_path.parts)
    keywords: list[str] = []

    for p in parts[-6:]:
        p_clean = p.replace("_", " ").replace("-", " ")
        # 提取中英文混合的关键词片段
        keywords.append(p_clean)

    # 组合描述
    lines = [
        f"图片: {img_path.stem}",
        f"路径: {' > '.join(keywords[-4:])}",
    ]
    if meta.get("competition", "unknown") != "unknown":
        lines.append(f"竞赛: {meta['competition']}")
    if meta.get("task_type", "other") != "other":
        lines.append(f"题型: {meta['task_type']}")
    if meta.get("algorithms"):
        lines.append(f"算法: {', '.join(meta['algorithms'])}")
    lines.append(f"文件名: {img_path.name}")

    return "\n".join(lines)


# ── Embedding 模型选择 ────────────────────────────────────────

class _EmbedderBase:
    """embedding 基类。"""
    def encode(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @property
    def dim(self) -> int:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError


class TFIDFEmbedder(_EmbedderBase):
    """TF-IDF 向量化器（永远离线可用）。"""

    def __init__(self, max_features: int = 512):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._max_features = max_features
        self._name = "tfidf"

    @property
    def name(self) -> str:
        return self._name

    @property
    def dim(self) -> int:
        return self._max_features

    def encode(self, texts: list[str]) -> list[list[float]]:
        if self._vectorizer is None:
            raise RuntimeError("TFIDFEmbedder not fitted. Call fit_transform first.")
        X = self._vectorizer.transform(texts)
        # 归一化到单位向量
        from sklearn.preprocessing import normalize
        X_norm = normalize(X, norm="l2")
        return X_norm.toarray().tolist()

    def fit_transform(self, texts: list[str]) -> list[list[float]]:
        from sklearn.feature_extraction.text import TfidfVectorizer
        self._vectorizer = TfidfVectorizer(
            max_features=self._max_features,
            analyzer="char_wb",
            ngram_range=(2, 4),
            lowercase=True,
        )
        X = self._vectorizer.fit_transform(texts)
        from sklearn.preprocessing import normalize
        X_norm = normalize(X, norm="l2")
        return X_norm.toarray().tolist()

    def is_fitted(self) -> bool:
        return self._vectorizer is not None


class MiniLMEmbedder(_EmbedderBase):
    """HuggingFace sentence-transformers embedding（384 维）。"""

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self._name = "minilm"
        self._model = None
        self._model_name = model_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def dim(self) -> int:
        return 384

    def _load(self):
        if self._model is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(
            self._model_name,
            device="cpu",
        )

    def encode(self, texts: list[str]) -> list[list[float]]:
        self._load()
        return self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()


class CLIPTextEmbedder(_EmbedderBase):
    """CLIP text encoder（512 维）。"""

    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self._name = "clip"
        self._model = None
        self._processor = None
        self._model_name = model_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def dim(self) -> int:
        return 512

    def _load(self):
        if self._model is not None:
            return
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self._model = CLIPModel.from_pretrained(self._model_name)
        self._processor = CLIPProcessor.from_pretrained(self._model_name)
        self._model.eval()

    def encode(self, texts: list[str]) -> list[list[float]]:
        self._load()
        import torch
        inputs = self._processor(
            text=texts, return_tensors="pt", padding=True, truncation=True
        )
        with torch.no_grad():
            text_features = self._model.get_text_features(**inputs)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy().tolist()


def _select_embedder(preferred: Optional[str] = None) -> _EmbedderBase:
    """按优先级尝试加载 embedding 模型。

    优先级: CLIP > MiniLM > TF-IDF
    """
    if preferred == "tfidf":
        print("[embed] 强制使用 TF-IDF", file=sys.stderr)
        return TFIDFEmbedder(max_features=512)

    if preferred == "clip":
        try:
            emb = CLIPTextEmbedder()
            emb._load()
            print(f"[embed] ✓ CLIP (512-dim)", file=sys.stderr)
            return emb
        except Exception as e:
            print(f"[embed] ✗ CLIP 不可用: {e}", file=sys.stderr)
            print("[embed] → fallback TF-IDF", file=sys.stderr)
            return TFIDFEmbedder(max_features=512)

    if preferred == "minilm":
        try:
            emb = MiniLMEmbedder()
            emb._load()
            print(f"[embed] ✓ MiniLM (384-dim)", file=sys.stderr)
            return emb
        except Exception as e:
            print(f"[embed] ✗ MiniLM 不可用: {e}", file=sys.stderr)
            print("[embed] → fallback TF-IDF", file=sys.stderr)
            return TFIDFEmbedder(max_features=512)

    # 自动选择
    for name, factory in [
        ("CLIP", lambda: CLIPTextEmbedder()),
        ("MiniLM", lambda: MiniLMEmbedder()),
    ]:
        try:
            emb = factory()
            emb._load()
            print(f"[embed] ✓ {name} ({emb.dim}-dim)", file=sys.stderr)
            return emb
        except Exception:
            continue

    print("[embed] ⚠ 无神经网络模型可用，使用 TF-IDF (512-dim)", file=sys.stderr)
    return TFIDFEmbedder(max_features=512)


# ── 核心逻辑 ──────────────────────────────────────────────────

def build_image_index(
    image_dir: Path = RESOURCES_DIR,
    persist_dir: Path = STORAGE_DIR,
    rebuild: bool = False,
    limit: Optional[int] = None,
    model: Optional[str] = None,
) -> int:
    """构建图片向量索引。

    Returns:
        索引的图片数量
    """
    # 清理旧索引
    if rebuild:
        for fname in ["image__vector_store.json"]:
            fp = persist_dir / fname
            if fp.exists():
                fp.unlink()
                print(f"[build_image] 删除: {fp.name}", file=sys.stderr)

    # 扫描图片
    images = _find_images(image_dir, limit=limit)
    if not images:
        print("[build_image] 未找到任何图片文件。", file=sys.stderr)
        return 0

    print(f"[build_image] 找到 {len(images)} 张图片", file=sys.stderr)

    # 选 embedding 模型
    embedder = _select_embedder(preferred=model)

    # ── 生成文本描述 ──────────────────────────────────────
    texts: list[str] = []
    metas: list[dict] = []
    valid_images: list[Path] = []

    for img_path in images:
        try:
            from PIL import Image
            img_obj = Image.open(img_path)
            img_obj.verify()
            _w, _h = img_obj.size
        except Exception as e:
            print(f"  ⚠ 跳过损坏图片: {img_path.name} ({e})", file=sys.stderr)
            continue

        meta = _parse_metadata(img_path, image_dir)
        text = _build_rich_description(img_path, meta)
        texts.append(text)
        metas.append(meta)
        valid_images.append(img_path)

    if not valid_images:
        print("[build_image] 无有效图片。", file=sys.stderr)
        return 0

    # ── 生成向量 ──────────────────────────────────────────
    t0 = time.perf_counter()
    print(f"[build_image] 使用 {embedder.name} 生成 {len(texts)} 个向量 ...", file=sys.stderr)

    if isinstance(embedder, TFIDFEmbedder):
        embeddings = embedder.fit_transform(texts)
    else:
        # batch embed
        batch_size = 32
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings.extend(embedder.encode(batch))
            if (i + batch_size) % 256 == 0 or i + batch_size >= len(texts):
                elapsed = time.perf_counter() - t0
                done = min(i + batch_size, len(texts))
                rate = done / elapsed if elapsed > 0 else 0
                print(f"  [{done}/{len(texts)}] {rate:.0f} texts/s", file=sys.stderr)

    elapsed = time.perf_counter() - t0
    print(f"[build_image] 向量化完成: {elapsed:.1f}s  dim={len(embeddings[0])}", file=sys.stderr)

    # ── 构建 LlamaIndex 兼容的 JSON ────────────────────────
    embedding_dict: dict[str, list[float]] = {}
    text_id_to_ref_doc_id: dict[str, str] = {}
    metadata_dict: dict[str, dict] = {}

    for i, (img_path, meta, emb) in enumerate(zip(valid_images, metas, embeddings)):
        rel_path = meta.get("relative_path", str(img_path))
        node_id = f"img__{i:05d}__{rel_path.replace(chr(92), '/').replace(' ', '_')}"[:250]

        embedding_dict[node_id] = emb
        text_id_to_ref_doc_id[node_id] = node_id
        metadata_dict[node_id] = {
            **meta,
            "text": texts[i],
            "image_index": i,
        }

    vector_store_data = {
        "embedding_dict": embedding_dict,
        "text_id_to_ref_doc_id": text_id_to_ref_doc_id,
        "metadata_dict": metadata_dict,
        "_model": embedder.name,
        "_dim": len(embeddings[0]),
        "_num_images": len(valid_images),
    }

    # ── 持久化 ─────────────────────────────────────────────
    persist_dir.mkdir(parents=True, exist_ok=True)
    output_path = persist_dir / "image__vector_store.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vector_store_data, f, ensure_ascii=False)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\n[build_image] ✓ 图片索引已保存!", file=sys.stderr)
    print(f"  文件: {output_path}", file=sys.stderr)
    print(f"  大小: {size_mb:.1f} MB", file=sys.stderr)
    print(f"  图片: {len(valid_images)}  向量维度: {len(embeddings[0])}  模型: {embedder.name}", file=sys.stderr)

    return len(valid_images)


# ── CLI ────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build image vector index for math-model papers (auto model selection)."
    )
    p.add_argument("--image-dir", default=str(RESOURCES_DIR), help="Image root directory")
    p.add_argument("--persist-dir", default=str(STORAGE_DIR), help="Persist directory")
    p.add_argument("--rebuild", action="store_true", help="Delete old index and rebuild")
    p.add_argument("--limit", type=int, default=None, help="Limit images (for testing)")
    p.add_argument(
        "--model",
        default=None,
        choices=["tfidf", "minilm", "clip"],
        help="Force specific embedding model (default: auto-select best available)",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    if not image_dir.exists():
        print(f"✗ 图片目录不存在: {image_dir}", file=sys.stderr)
        return 1

    try:
        count = build_image_index(
            image_dir=image_dir,
            persist_dir=Path(args.persist_dir),
            rebuild=args.rebuild,
            limit=args.limit,
            model=args.model,
        )
        if count == 0:
            return 1
    except KeyboardInterrupt:
        print("\n[build_image] 用户中断", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())