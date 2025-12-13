import faiss
import json
import os
import numpy as np

def create_index(dim: int):
    return faiss.IndexFlatIP(dim)

def add_embeddings(index, embeddings):
    index.add(np.asarray(embeddings, dtype="float32"))

def save_index(index, metadata, path: str):
    os.makedirs(path, exist_ok=True)
    index_path = os.path.join(path, "index.faiss")
    meta_path = os.path.join(path, "meta.json")
    faiss.write_index(index, index_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

def load_index(path: str):
    index_path = os.path.join(path, "index.faiss")
    meta_path = os.path.join(path, "meta.json")
    if not os.path.exists(index_path):
        raise FileNotFoundError(
            f"FAISS index not found at {index_path}"
        )
    if not os.path.exists(meta_path):
        raise FileNotFoundError(
            f"Metadata file not found at {meta_path}."
        )
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata
